"""
NameCleaner — Shared name cleanup and handle validation.

Injected into both LLMResponseParser and NameExtractor to enforce
consistent cleanup rules at the extraction source.
"""

from __future__ import annotations

import re
from urllib.parse import unquote



# Regex: exactly 2 capitalized words, allowing hyphens, apostrophes, and accented chars.
# Uses broader ranges than NameExtractor since LLM output contains international names.
_NAME_RE = re.compile(
    r"\b("
    r"[A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'\u2019-]+"  # First word
    r"\s[A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'\u2019-]+"  # Second word
    r")\b"
)
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
    "nike training club", "nike training", "firecrawl", "scrapegraph ai",
    "meta ai", "inworld ai", "jasper ai", "stability ai",
    "copy ai", "synthesia ai", "runway ml", "perplexity ai",
    "gymshark", "claude", "gemini", "dalle",
    "modash", "favikon", "collabstr",
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
    # Scrape artifact names — section headings/labels extracted as names
    "table of contents", "read more", "engagement rate benchmark",
    "why it works", "execution", "trust & transparency",
    "trust and transparency", "company", "videos",
    "strength training:", "pilates:", "free webinar",
    "people brands and", "gaming and esport",
    # CTA phrases that match _NAME_RE (two CamelCase words)
    "free trial", "free webinar", "sign up", "read more", "see more",
    "load more", "show more", "view profile", "watch now",
    "get started", "try free", "book demo", "download app",
    "browse all", "contact us", "explore more", "view all",
    "continue reading", "related articles",
})

# Non-content-creator celebrities — NOT Arnold, The Rock, Gordon Ramsay
_CELEBRITY_BLOCKLIST = frozenset({
    "taylor swift", "beyonce", "rihanna", "ariana grande",
    "billie eilish", "dua lipa", "shakira", "cardi b",
    "olivia rodrigo", "lady gaga", "justin bieber",
    "drake", "neymar", "david beckham", "will smith",
    "emma watson", "harry styles", "adele",
    "robert downey jr", "tom holland", "narendra modi",
    "bts", "jack black", "rosalia",
    "cristiano ronaldo", "lionel messi",
    "daft punk", "take my breath", "love theme",
    "pewdiepie", "mr beast", "samsung galaxy",
    "shreya ghoshal", "neha kakkar", "diljit dosanjh",
    "selena gomez", "kim kardashian", "kylie jenner",
})

# Combined lowercase set for efficient lookup
_ALL_NON_PERSON = (
    _BRAND_BLOCKLIST | _COUNTRY_BLOCKLIST | _NEWS_ORG_BLOCKLIST
    | _GENERIC_BLOCKLIST | _CELEBRITY_BLOCKLIST
)

# LinkedIn slug pattern: first-last-1234567
_LINKEDIN_SLUG_RE = re.compile(r'^[a-z]+-[a-z]+(?:-[a-z0-9]+)*-\d{4,}$')


class NameCleaner:
    """Shared name cleanup — injected into LLMResponseParser + NameExtractor."""

    @staticmethod
    def clean_name(name: str) -> str | None:
        """Clean a raw name. Returns None to reject.

        Pipeline:
          1. Decode URL-encoded strings (reject if still garbled)
          2. Extract name via _NAME_RE.search() — two CamelCase words
             (cuts through bold, numbering, emoji, markdown garbage)
          3. Reject non-person entities (countries, brands, news orgs)
        """
        if not name or not name.strip():
            return None

        if _URL_ENCODED_RE.search(name):
            decoded = unquote(name)
            if decoded == name or _URL_ENCODED_RE.search(decoded):
                return None
            if not re.search(r'[a-zA-Z]', decoded):
                return None
            name = decoded

        match = _NAME_RE.search(name)
        if not match:
            return None

        extracted = match.group(1).strip()
        if not extracted:
            return None

        if _is_non_person(extracted):
            return None

        return extracted

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
