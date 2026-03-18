"""
YouTubeChannelResolver — Resolves youtube.com/channel/UC... IDs to @handles.

Sends HTTP requests to YouTube channel URLs and extracts the @handle
from the response. Uses httpx for async HTTP with backoff.

Note: YouTube requires a SOCS consent cookie to bypass the EU consent
page, and @handles are embedded in JavaScript data (canonicalBaseUrl,
vanityChannelUrl), not in standard HTML tags.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore  # Gracefully degrade if httpx not installed

from config.settings import MAX_RETRIES, BACKOFF_BASE_SECONDS

logger = logging.getLogger(__name__)


# Pattern to extract @handle from YouTube response URL or page
_YT_AT_HANDLE = re.compile(r'youtube\.com/@([A-Za-z0-9_.\-]{2,30})')
# Fallback: look for canonical URL or meta tag in HTML
_YT_CANONICAL = re.compile(
    r'<link[^>]+rel="canonical"[^>]+href="https://www\.youtube\.com/@([^"]+)"',
    re.IGNORECASE,
)
# JavaScript data patterns (YouTube embeds @handle in JSON-LD/JS)
_YT_CANONICAL_BASE = re.compile(r'"canonicalBaseUrl":"/@([^"]+)"')
_YT_VANITY_URL = re.compile(r'"vanityChannelUrl":"https?://www\.youtube\.com/@([^"]+)"')

# Cookie to bypass YouTube's EU consent page
_CONSENT_COOKIE = {
    "SOCS": "CAISNQgDEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMwODE1LjA3X3AxGgJlbiACGgYIgJnZpwY",
}


@dataclass
class ResolvedChannel:
    """A resolved YouTube channel."""
    channel_id: str  # UC...
    handle: str      # @handle (without @)


async def resolve_youtube_channels(
    channel_ids: list[str],
    concurrency: int = 3,
) -> dict[str, str]:
    """Resolve YouTube channel IDs to @handles.

    Sends GET requests to youtube.com/channel/UC... and extracts
    the @handle from redirects or page content.

    Args:
        channel_ids: List of channel IDs (e.g. "UC4qk9TtGhBKCkoWz5qGJcGg").
        concurrency: Max concurrent requests.

    Returns:
        Dict mapping channel_id -> handle (without @).
    """
    if not httpx:
        logger.warning("httpx not installed — skipping YouTube channel resolution")
        return {}

    if not channel_ids:
        return {}

    results: dict[str, str] = {}
    semaphore = asyncio.Semaphore(concurrency)

    async def _resolve_one(cid: str) -> None:
        async with semaphore:
            handle = await _fetch_channel_handle(cid)
            if handle:
                results[cid] = handle
                logger.info("YouTube resolved: %s → @%s", cid, handle)
            else:
                logger.warning("YouTube channel %s could not be resolved to @handle", cid)

    tasks = [_resolve_one(cid) for cid in channel_ids]
    await asyncio.gather(*tasks, return_exceptions=True)

    resolved = len(results)
    total = len(channel_ids)
    failed = total - resolved
    if failed > 0:
        logger.warning("YouTube resolution: %d/%d channels resolved, %d failed",
                       resolved, total, failed)
    else:
        logger.info("YouTube resolution: all %d channels resolved successfully", total)
    return results


async def _fetch_channel_handle(channel_id: str) -> str | None:
    """Fetch the @handle for a single YouTube channel ID."""
    url = f"https://www.youtube.com/channel/{channel_id}"

    for attempt in range(MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(
                follow_redirects=True,
                timeout=10.0,
                cookies=_CONSENT_COOKIE,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    ),
                },
            ) as client:
                resp = await client.get(url)

                # Check final URL after redirects
                final_url = str(resp.url)

                # If we ended up on the consent page, the cookie didn't work
                if "consent.youtube.com" in final_url:
                    return None

                match = _YT_AT_HANDLE.search(final_url)
                if match:
                    return match.group(1)

                # Check page content
                if resp.status_code == 200:
                    text = resp.text

                    # Try HTML canonical link (in head, first 10K)
                    match = _YT_CANONICAL.search(text[:10_000])
                    if match:
                        return match.group(1)

                    # Try JavaScript data (canonicalBaseUrl) —
                    # YouTube embeds this deep in the JS bundle (~600K+ chars)
                    match = _YT_CANONICAL_BASE.search(text)
                    if match:
                        return match.group(1)

                    # Try JavaScript data (vanityChannelUrl)
                    match = _YT_VANITY_URL.search(text)
                    if match:
                        return match.group(1)

                return None

        except Exception:
            if attempt < MAX_RETRIES:
                delay = BACKOFF_BASE_SECONDS * (2 ** attempt)
                logger.warning("YouTube channel %s resolve attempt %d failed, retrying in %ds",
                               channel_id, attempt + 1, delay)
                await asyncio.sleep(delay)
            else:
                logger.exception("Failed to resolve YouTube channel %s after %d attempts",
                                 channel_id, MAX_RETRIES + 1)
                return None
    return None  # unreachable, satisfies mypy
