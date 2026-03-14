"""
NameCleaner — Shared name cleanup and handle validation.

Injected into both LLMResponseParser and NameExtractor to enforce
consistent cleanup rules at the extraction source.
"""

from __future__ import annotations

import re
from urllib.parse import unquote


_MARKDOWN_BOLD_RE = re.compile(r'\*\*(.+?)\*\*')
_MARKDOWN_LINK_RE = re.compile(r'\[([^\]]+)\]\([^)]+\)')
_NUMBER_PREFIX_RE = re.compile(r'^\d+[.)\-]\s*')
_URL_ENCODED_RE = re.compile(r'%[0-9A-Fa-f]{2}')

# Brands / companies / tools / products — not people
_BRAND_BLOCKLIST = frozenset({
    "canva", "capcut", "peloton", "nike", "adidas", "lululemon",
    "myfitnesspal", "strava", "fitbit", "garmin", "whoop",
    "notion", "figma", "slack", "discord", "shopify", "squarespace",
    "openai", "chatgpt", "midjourney", "hugging face", "anthropic",
    "google", "apple", "microsoft", "amazon", "meta", "tiktok",
    "instagram", "youtube", "twitter", "facebook", "snapchat",
    "netflix", "spotify", "uber", "airbnb", "tesla",
    "nike training club", "firecrawl", "scrapegraph ai",
    "meta ai", "inworld ai", "jasper ai", "stability ai",
    "copy ai", "synthesia ai", "runway ml", "perplexity ai",
    "gymshark", "claude", "gemini", "dalle",
})

# Countries / regions — not people
_COUNTRY_BLOCKLIST = frozenset({
    "bangladesh", "india", "pakistan", "indonesia", "brazil",
    "nigeria", "mexico", "philippines", "egypt", "vietnam",
    "germany", "france", "japan", "china", "australia",
    "canada", "spain", "italy", "turkey", "argentina",
    "thailand", "south korea", "colombia", "kenya", "malaysia",
    "united states", "united kingdom", "south africa",
    "new zealand", "saudi arabia", "sri lanka",
    "north america", "south america", "latin america",
})

# News orgs, publications — not people
_NEWS_ORG_BLOCKLIST = frozenset({
    "bbc", "cnn", "forbes", "business insider", "techcrunch",
    "the verge", "wired", "mashable", "buzzfeed", "huffpost",
    "new york times", "washington post", "guardian",
    "wall street journal", "reuters", "associated press",
    "the neuron", "morning brew",
})

# Generic phrases that slip through regex name matching
_GENERIC_BLOCKLIST = frozenset({
    "body coach", "training club", "fitness pal",
    "content creator", "content creators",
    "social media", "influencer marketing",
    # Nav / tool elements scraped as names
    "fake followers", "fake follower check",
    "engagement rate calculator", "engagement rate",
    "influencer hero", "influencer search", "influencer discovery",
})

# Combined lowercase set for efficient lookup
_ALL_NON_PERSON = _BRAND_BLOCKLIST | _COUNTRY_BLOCKLIST | _NEWS_ORG_BLOCKLIST | _GENERIC_BLOCKLIST

# LinkedIn slug pattern: first-last-1234567
_LINKEDIN_SLUG_RE = re.compile(r'^[a-z]+-[a-z]+(?:-[a-z0-9]+)*-\d{4,}$')


class NameCleaner:
    """Shared name cleanup — injected into LLMResponseParser + NameExtractor."""

    @staticmethod
    def clean_name(name: str) -> str | None:
        """Clean a raw name. Returns None to reject.

        Pipeline:
          1. Strip markdown bold (**name**)
          2. Strip markdown links [text](url)
          3. Strip leading number prefix (1. Name)
          4. Decode URL-encoded strings (reject if still garbled)
          5. Reject non-person entities (countries, brands, news orgs)
          6. Strip whitespace
        """
        if not name or not name.strip():
            return None

        name = _MARKDOWN_BOLD_RE.sub(r'\1', name)
        name = _MARKDOWN_LINK_RE.sub(r'\1', name)
        name = _NUMBER_PREFIX_RE.sub('', name)

        if _URL_ENCODED_RE.search(name):
            decoded = unquote(name)
            if decoded == name or _URL_ENCODED_RE.search(decoded):
                return None
            if not re.search(r'[a-zA-Z]', decoded):
                return None
            name = decoded

        name = name.strip()
        if not name:
            return None

        if _is_non_person(name):
            return None

        return name

    @staticmethod
    def is_valid_handle(handle: str) -> bool:
        """Validate handle — rejects LinkedIn slugs, product slugs, etc."""
        if not handle:
            return False
        if _LINKEDIN_SLUG_RE.match(handle.lower()):
            return False
        if '/' in handle:
            return False
        return True


def _is_non_person(name: str) -> bool:
    """Check if a name matches any non-person blocklist."""
    key = name.lower().strip()
    return key in _ALL_NON_PERSON
