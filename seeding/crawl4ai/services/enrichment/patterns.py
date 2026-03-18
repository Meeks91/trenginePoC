"""
Handle Patterns
================
Platform-aware handle extraction for the enrichment layer.

URL extraction delegates to RegexHandleExtractor (single source of truth).
Text extraction uses a simple @handle regex for DDG result parsing.

Supports Instagram, TikTok, and YouTube.
"""

import re
from typing import Optional

from config.schema import Platform
from services.extraction.RegexHandleExtractor import (
    extract_handles_from_url as _regex_extract,
)


# ── Platform domains for DDG search ──

PLATFORM_DOMAINS: dict[Platform, str] = {
    Platform.Instagram: "instagram.com",
    Platform.TikTok:    "tiktok.com",
    Platform.YouTube:   "youtube.com",
}

# Generic @handle in text
_AT_HANDLE_PATTERN = re.compile(r"@([a-zA-Z0-9_.]{2,})")


def extract_handle_from_url(url: str, platform: str) -> Optional[str]:
    """Extract a handle from a platform URL.

    Delegates to RegexHandleExtractor for pattern matching and junk-path
    filtering — single source of truth for URL → handle extraction.

    Args:
        url: The URL to extract from.
        platform: One of "Instagram", "TikTok", "YouTube" (used to filter
            results to the requested platform only).

    Returns:
        Handle prefixed with @ (e.g. "@kayla_itsines"), or None.
    """
    result = _regex_extract(url)
    if result is None:
        return None
    if result.platform != platform:
        return None
    return f"@{result.handle.lower()}"


def extract_handle_from_text(text: str) -> Optional[str]:
    """Extract the first @handle from a block of text."""
    m = _AT_HANDLE_PATTERN.search(text)
    if m:
        handle = m.group(1).lower()
        if len(handle) > 2:
            return f"@{handle}"
    return None
