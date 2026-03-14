"""Platform classification for naked @handles.

Classifies handles by checking surrounding context for platform keywords
(Instagram, TikTok, YouTube) using a multi-step cascade:
  1. Count platforms on entire page → 1 platform = auto-assign
  2. If 2+ platforms, check 100-char window around @handle
  3. If 2+ in window, use closest keyword (emoji ≤5 chars, text ≤20 chars)
  4. If 0 platforms on page → check URL domain
  5. Nothing found → "" (unclassified)
"""

from __future__ import annotations

import re

from services.extraction.RegexHandleExtractor import ExtractedHandle


# ══════════════════════════════════════════════════════════════════════
# Platform Constants
# ══════════════════════════════════════════════════════════════════════

# Platform keyword patterns for mechanical classification
_PLATFORM_KW: dict[str, re.Pattern] = {
    "Instagram": re.compile(r'instagram|insta\b|\bIG\b|📸', re.IGNORECASE),
    "TikTok":    re.compile(r'tiktok|tik\s*tok|🎵', re.IGNORECASE),
    "YouTube":   re.compile(r'youtube|you\s*tube|\bYT\b|📺|🎥', re.IGNORECASE),
}

# Emoji indicators — these require tighter proximity (≤5 chars) vs keywords (≤20 chars)
_EMOJI_INDICATORS = frozenset({'📸', '🎵', '📺', '🎥'})

# URL domain → platform for page-level classification
_URL_PLATFORM_MAP: dict[str, str] = {
    "Instagram": "instagram.com",
    "TikTok":    "tiktok.com",
    "YouTube":   "youtube.com",
}


# ══════════════════════════════════════════════════════════════════════
# Classification Function
# ══════════════════════════════════════════════════════════════════════

def classify_by_context(
    handle: ExtractedHandle,
    page_text: str,
    page_url: str,
) -> str | None:
    """Try to assign platform mechanically from surrounding context.

    Classification cascade:
      1. Count platforms on entire page (title + body)
      2. If exactly 1 platform on page → auto-assign
      3. If 2+ platforms on page, check 100-char window around @handle:
         - 1 platform in window → assign that one
         - 0 or 2+ in window → ambiguous → LLM
      4. If 0 platforms on page → check URL domain
      5. Nothing found → "" (unclassified, skip LLM)

    Returns:
      - platform string (e.g. "Instagram") if assigned
      - "" (empty) if 0 platforms found → leave unclassified
      - None if ambiguous → needs LLM
    """
    if not page_text:
        return ""  # No context at all → unclassified

    # ── Step 1: Count platforms on the entire page ──
    page_platforms: set[str] = set()
    for platform, kw_pattern in _PLATFORM_KW.items():
        if kw_pattern.search(page_text):
            page_platforms.add(platform)

    if len(page_platforms) == 1:
        return page_platforms.pop()  # Only 1 platform on page → assign

    if len(page_platforms) >= 2:
        # ── Step 2: Disambiguate via 100-char window around @handle ──
        handle_pattern = f"@{re.escape(handle.handle)}"
        match = re.search(handle_pattern, page_text, re.IGNORECASE)

        if match:
            start = max(0, match.start() - 100)
            end = min(len(page_text), match.end() + 100)
            window = page_text[start:end]

            local_platforms: set[str] = set()
            for platform, kw_pattern in _PLATFORM_KW.items():
                if kw_pattern.search(window):
                    local_platforms.add(platform)

            if len(local_platforms) == 1:
                return local_platforms.pop()  # 1 platform near handle → assign

            if len(local_platforms) >= 2:
                # 2+ platforms in window — use the closest keyword
                # Emojis require ≤5 chars proximity; text keywords allow ≤20 chars
                handle_pos = match.start()
                closest_platform = None
                closest_dist = float("inf")
                closest_is_emoji = False
                for plat, kw_pattern in _PLATFORM_KW.items():
                    for kw_match in kw_pattern.finditer(page_text):
                        dist = min(
                            abs(kw_match.start() - handle_pos),
                            abs(kw_match.end() - handle_pos),
                        )
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_platform = plat
                            matched_text = kw_match.group(0)
                            closest_is_emoji = matched_text in _EMOJI_INDICATORS
                max_dist = 5 if closest_is_emoji else 20
                if closest_platform and closest_dist <= max_dist:
                    return closest_platform  # Closest within threshold → assign

        return None  # 2+ platforms, can't disambiguate → LLM

    # ── Step 3: 0 platforms on page → check URL domain ──
    url_lower = page_url.lower()
    url_platforms: set[str] = set()
    for platform, domain in _URL_PLATFORM_MAP.items():
        if domain in url_lower:
            url_platforms.add(platform)

    if len(url_platforms) == 1:
        return url_platforms.pop()
    if len(url_platforms) >= 2:
        return None  # Ambiguous URL → LLM

    # 0 platforms found anywhere → leave unclassified
    return ""
