"""
Handle Patterns
================
Platform-aware regex patterns for extracting social media handles from URLs and text.
Supports Instagram, TikTok, and YouTube.

NOTE: Similar URL patterns also defined in extraction/RegexHandleExtractor.py — keep in sync.
"""

import re
from typing import Optional

from config.schema import Platform


# ── Platform URL Patterns ──
# Each maps a URL to a handle extracted from the path.

PLATFORM_URL_PATTERNS: dict[str, re.Pattern] = {
    "Instagram": re.compile(r"instagram\.com/([a-zA-Z0-9_.]+)/?"),
    "TikTok":    re.compile(r"tiktok\.com/@([a-zA-Z0-9_.]+)/?"),
    "YouTube":   re.compile(r"youtube\.com/(?:@|c/|channel/)([a-zA-Z0-9_.\-]+)/?"),
}

# ── Platform domains for DDG search ──

PLATFORM_DOMAINS: dict[Platform, str] = {
    Platform.Instagram: "instagram.com",
    Platform.TikTok:    "tiktok.com",
    Platform.YouTube:   "youtube.com",
}

# ── Junk paths per platform (not real user handles) ──

PLATFORM_JUNK_PATHS: dict[str, set[str]] = {
    "Instagram": {
        "p", "reel", "reels", "explore", "accounts", "stories",
        "tv", "about", "directory", "developer", "legal",
    },
    "TikTok": {
        "foryou", "following", "live", "discover", "upload",
        "explore", "about", "legal", "transparency",
    },
    "YouTube": {
        "watch", "playlist", "feed", "gaming", "music", "premium",
        "channel", "results", "about", "t", "shorts",
    },
}

# Generic @handle in text
AT_HANDLE_PATTERN = re.compile(r"@([a-zA-Z0-9_.]{2,})")


def extract_handle_from_url(url: str, platform: str) -> Optional[str]:
    """
    Extract a handle from a platform URL.

    Args:
        url: The URL to extract from.
        platform: One of "Instagram", "TikTok", "YouTube".

    Returns:
        Handle prefixed with @ (e.g. "@kayla_itsines"), or None.
    """
    pattern = PLATFORM_URL_PATTERNS.get(platform)
    if not pattern:
        return None

    m = pattern.search(url)
    if not m:
        return None

    handle = m.group(1).lower()
    junk = PLATFORM_JUNK_PATHS.get(platform, set())
    if handle in junk:
        return None

    return f"@{handle}"


def extract_handle_from_text(text: str) -> Optional[str]:
    """Extract the first @handle from a block of text."""
    m = AT_HANDLE_PATTERN.search(text)
    if m:
        handle = m.group(1).lower()
        if len(handle) > 2:
            return f"@{handle}"
    return None
