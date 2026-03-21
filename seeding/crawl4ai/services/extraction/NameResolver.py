"""
NameResolver — Resolve candidate influencer names to social media handles via DDG.

For each candidate name, queries DDG with:
    "{name} Instagram TikTok YouTube Influencer"

Parses result URLs for known platform domains (instagram.com, tiktok.com, youtube.com)
and extracts handles using the existing RegexHandleExtractor.
"""

from __future__ import annotations

import logging
import random
import time

from ddgs import DDGS

from services.audit.AuditService import AuditLog

logger = logging.getLogger(__name__)

from services.extraction.RegexHandleExtractor import (
    extract_handles_from_url,
    ExtractedHandle,
)
from config import (
    SEARCH_DELAY_SECONDS, SEARCH_BACKEND, SEARCH_REGION,
    BACKOFF_BASE_SECONDS, BACKOFF_MAX_SECONDS,
)


# Platform domains that indicate a social media profile
_PLATFORM_DOMAINS = {"instagram.com", "tiktok.com", "youtube.com"}



# Internal retry count for DDG queries (all retries handled here, callers don't retry)
# 5 total attempts with fresh DDGS instances = robust against DDG non-determinism
NAME_DDG_MAX_RETRIES = 4  # 5 total tries (initial + 4 retries)


def resolve_names_via_ddg(
    names: list[str],
    audit: AuditLog,
    *,
    query_template: str,
    category: str = "Influencer",
    platform: str = "Instagram",
    max_results_per_query: int = 5,
    delay_seconds: float = SEARCH_DELAY_SECONDS,
) -> list[ExtractedHandle]:
    """Resolve candidate names to social media handles via DDG search.

    For each name, queries DDG and parses result URLs for platform handles.
    Includes rate limiting and retry logic.

    Args:
        names: Deduplicated candidate names to search.
        audit: Audit log for tracking queries.
        category: Category/niche context (e.g. "Fitness", "Beauty") for better DDG relevance.
        platform: Target platform (e.g. "Instagram", "TikTok") for fallback queries.
        max_results_per_query: Max DDG results to inspect per name.

    Returns:
        List of confirmed ExtractedHandle objects with platform set.
    """
    if not names:
        return []

    logger.info("  --- Reddit Name Resolution ---")
    logger.info("  Resolving %d candidate names via DDG", len(names))

    resolved: list[ExtractedHandle] = []
    seen_handles: set[tuple[str, str]] = set()  # Avoid duplicates across names

    for i, name in enumerate(names, 1):
        query = query_template.format(name=name, category=category)
        results = _query_with_retry(query, max_results_per_query)
        handles_for_name = _extract_handles_from_results(results, candidate_name=name)

        if handles_for_name:
            for handle in handles_for_name:
                key = (handle.handle.lower(), handle.platform)
                if key not in seen_handles:
                    seen_handles.add(key)
                    handle.name = name
                    resolved.append(handle)
                    logger.info("    [%d/%d] %-30s → @%s (%s)",
                                i, len(names), name, handle.handle, handle.platform)
                    audit.log("name_resolution", "resolved",
                             name=name, handle=handle.handle,
                             platform=handle.platform)
        else:
            audit.log("name_resolution", "no_match", name=name)

        # Rate limiting between names
        if i < len(names):
            time.sleep(delay_seconds)

    logger.info("  Resolved: %d/%d names → handles", len(resolved), len(names))
    return resolved


def _score_result(url: str, handle: ExtractedHandle, candidate_name: str) -> int:
    """Score a DDG result for name resolution priority.

    Higher score = more likely to be the correct profile page.
    Profile pages rank above posts/reels/shorts.
    Handles containing name words rank above random handles.
    """
    score = 0
    # Profile page (not a post/reel/video) = highest priority
    url_lower = url.lower()
    if "/p/" not in url_lower and "/reel/" not in url_lower and "/shorts/" not in url_lower:
        score += 10
    # Handle contains name words = strong signal
    name_words = {w.lower() for w in candidate_name.split() if len(w) >= 3}
    if any(w in handle.handle.lower() for w in name_words):
        score += 5
    return score


def _extract_handles_from_results(
    results: list[dict],
    candidate_name: str = "",
) -> list[ExtractedHandle]:
    """Parse DDG result URLs for platform handles.

    When candidate_name is provided, applies a confidence check:
    at least one word from the candidate name must appear in the
    DDG result title. This kills false positives like
    "Jerf Nipples" → @matildadjerf (title: "Matilda Djerf").

    Results are scored and returned in priority order (profile pages
    and name-matching handles first).
    """
    scored: list[tuple[int, ExtractedHandle]] = []
    seen: set[str] = set()

    # Build name-word set for confidence check
    name_words = {w.lower() for w in candidate_name.split() if len(w) >= 3} if candidate_name else set()

    for result in results:
        url = result.get("href", "")
        if not url:
            continue

        # Check if any platform domain appears in the URL
        if not any(domain in url.lower() for domain in _PLATFORM_DOMAINS):
            continue

        # DDG confidence check: does the candidate name appear in the result?
        # Only applies when DDG provides title/body metadata.
        if name_words:
            title = result.get("title", "").lower()
            body = result.get("body", "").lower()
            text = f"{title} {body}".strip()
            # If DDG provided metadata, at least one name-word must appear
            if text and not any(w in text for w in name_words):
                continue

        handle = extract_handles_from_url(url)
        if handle and handle.handle.lower() not in seen:
            seen.add(handle.handle.lower())
            score = _score_result(url, handle, candidate_name)
            scored.append((score, handle))

    # Sort by score descending — best matches first
    scored.sort(key=lambda x: x[0], reverse=True)
    return [handle for _, handle in scored]


def _query_with_retry(
    query: str,
    max_results: int,
    max_retries: int = NAME_DDG_MAX_RETRIES,
) -> list[dict]:
    """Execute a DDG query with exponential backoff on failure.

    All retry logic is internal — callers should NOT wrap this in
    their own retry loops. Uses fresh DDGS instances on each attempt
    to avoid stale sessions (DDG is non-deterministic).
    """
    for attempt in range(max_retries + 1):
        ddgs = DDGS()  # fresh instance each attempt
        try:
            return list(ddgs.text(
                query, max_results=max_results,
                backend=SEARCH_BACKEND, region=SEARCH_REGION,
            ))
        except Exception:
            if attempt < max_retries:
                delay = min(
                    BACKOFF_BASE_SECONDS * (2 ** attempt) + random.uniform(0, 1),
                    BACKOFF_MAX_SECONDS,
                )
                logger.warning("DDG error (attempt %d/%d), backing off %.1fs",
                               attempt + 1, max_retries + 1, delay)
                time.sleep(delay)
            else:
                logger.exception("DDG failed after %d attempts", max_retries + 1)
                return []
    return []  # unreachable, satisfies mypy
