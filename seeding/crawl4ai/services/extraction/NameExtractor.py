"""
NameExtractor — Extract candidate influencer names from text using regex.

Targets Reddit-style content where influencers are mentioned by name
(e.g. "Alex Leonidas", "Basement Bodybuilding") rather than by @handle.

Only activated for reddit.com pages.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

from services.extraction.NameCleanerService import NameCleaner

# Strip leading numbering: "1. ", "23) ", "100. "
_NUMBER_PREFIX_RE = re.compile(r'^\d+[.)\-]\s*')


# ══════════════════════════════════════════════════════════════════════
# Config
# ══════════════════════════════════════════════════════════════════════

MAX_NAMES_PER_PAGE = 50  # Safety valve only; blocklist does the real filtering

# Common sentence-starter words that, when they begin a multi-word match,
# indicate the capture is noise (e.g. "Also Alex Leonidas" is not a name).
_SENTENCE_STARTERS = frozenset({
    "also", "plus", "and", "but", "or", "so", "yet", "then", "though",
    "while", "when", "where", "because", "since", "although", "however",
    "therefore", "moreover", "furthermore", "meanwhile", "instead",
    "even", "just", "still", "again", "already", "another",
    "this", "that", "these", "those", "any", "some", "all",
    "each", "both", "many", "most", "few", "very", "quite",
    "here", "there", "today", "now", "recently", "currently",
    "new", "my", "our", "his", "her", "their", "your", "its",
    "great", "best", "top", "well", "good", "key", "main", "only",
    "other", "similar", "such", "via", "per", "non",
})

# Regex: exactly 2 capitalized words, allowing hyphens and apostrophes.
_NAME_RE = re.compile(
    r"\b("
    r"[A-Z][a-zA-Z'\u2019-]+"  # First word (capitalized, allows O'Brien, Omni-man)
    r"\s[A-Z][a-zA-Z'\u2019-]+"  # Exactly 1 more capitalized word
    r")\b"
)

# Individual words that reject a candidate name if found ANYWHERE in it.
# E.g. "US Food Instagram" is blocked because it contains "food" and "instagram".
_WORD_BLOCKLIST = frozenset({
    # Social media platforms
    "instagram", "tiktok", "youtube", "twitter", "facebook",
    "snapchat", "pinterest", "linkedin", "reddit", "twitch",
    # Social media jargon
    "handle", "handles", "followers", "subscriber", "subscribers",
    "influencer", "influencers", "account", "accounts",
    "channel", "channels", "page", "pages",
    # Niche / category words (not names)
    "food", "fitness", "beauty", "fashion", "travel",
    "lifestyle", "wellness", "health", "cooking", "recipe",
    "recipes", "workout", "diet", "nutrition",
    # Generic content words
    "cookbook", "blog", "vlog", "podcast", "author", "authors",
    "creator", "creators", "ambassador", "ambassadors",
    "sponsored", "advertisement", "affiliate",
    "pre-order", "order",
    # Noise from article headings / scraped page elements
    "training", "evidence", "research", "science", "daily",
    "front", "expert", "approved", "certified",
    "download", "chrome", "tips", "tricks",
    # Adult / spam
    "cams", "adult", "porn", "xxx", "nsfw",
    # UI elements
    "login", "register", "signup", "subscribe",
    "cookie", "cookies", "privacy", "preferences",
    # Nationality+gender patterns (favikon.com noise)
    "female", "male",
    # Platform-type suffixes
    "youtubers", "tiktokers",
    # UI/CTA fragments
    "calculator", "generator",
    # Site chrome
    "favikon", "modash", "collabstr",
})

# Common proper noun phrases to skip (not influencer names)
_NAME_BLOCKLIST = frozenset({
    # Countries / regions / cities
    "united states", "united kingdom", "new york", "los angeles",
    "san francisco", "new zealand", "south africa", "hong kong",
    "north america", "south america", "north carolina", "south carolina",
    "grand rapids", "san diego", "las vegas", "san antonio",
    "el paso", "fort worth", "st louis", "salt lake",
    "buenos aires", "rio de janeiro", "sao paulo",
    "costa rica", "puerto rico", "dominican republic",
    "sri lanka", "saudi arabia", "south korea", "north korea",

    # Common Reddit/forum phrases
    "thank you", "good luck", "let me", "last week", "next level",
    "this week", "the best", "my personal", "in my", "well done",
    "first time", "long time", "check out",
    "hi everybody", "morning person", "show more",
    # Reddit UI / structural noise
    "profile badge", "achievement top", "learn more", "best open",
    "top commenter", "comment deleted", "open app", "shop now",
    "open menu", "log in", "go to", "skip to", "get app",
    "view post", "view more", "see answer", "more posts",
    "create your", "more replies", "community info",
    "community diagnostic", "acrobat studio",
    "related answers", "top posts", "reddit rules",
    "privacy policy", "user agreement",
    "comments section", "community info section",
    "related answers section", "related answers best",
    "collapse navigation", "collapse video",
    "right sidebar", "back go", "get app log",
    "join natural", "public top posts",
    "continue with phone", "number by",
    "policy user agreement", "reddit rules privacy",
    "accessibility reddit",
    # Cookie consent / ad noise
    "accept all", "reject optional", "reject optional cookies",
    "dope max", "thumbnail image", "sign up",
    "parkrun learn more", "parkrun collapse",
    # Generic bodybuilding/fitness terms (not names)
    "drug free bodybuilder", "bodybuilding discussion",
    "no juice", "actual prep starts", "weeks out",
    # Fitness / exercise terms
    "pull ups", "push ups", "jm presses",
    # Scraped heading fragments
    "daily dare", "front rack", "pull day", "push day",
    "case study", "peer review", "save preferences",
    "download chrome", "accept all",
})


# ══════════════════════════════════════════════════════════════════════
# Internal
# ══════════════════════════════════════════════════════════════════════

def _clean_and_filter(name: str) -> str | None:
    """Clean a raw regex match and apply all blocklist/heuristic filters.

    Returns the cleaned name if it passes all filters, or None.
    """
    name = name.strip()
    if name.endswith("\u2019s") or name.endswith("'s"):
        name = name[:-2].rstrip()
    cleaned = NameCleaner.clean_name(name)
    if not cleaned or len(cleaned) < 4:
        return None
    key = cleaned.lower()
    first_word = key.split()[0] if key.split() else ""
    if key in _NAME_BLOCKLIST:
        return None
    words = set(key.split())
    if words & _WORD_BLOCKLIST:
        return None
    if first_word in _SENTENCE_STARTERS:
        return None
    if any(w.isupper() and len(w) > 1 for w in cleaned.split()):
        return None
    if cleaned[-1] in ".:!?,;":
        return None
    return cleaned


def _prepare_text(text: str) -> list[str]:
    """Normalize text and extract raw regex matches."""
    text = text.replace("\n", " ").replace("\r", " ")
    return _NAME_RE.findall(text)


# ══════════════════════════════════════════════════════════════════════
# Public API
# ══════════════════════════════════════════════════════════════════════

def extract_candidate_names(text: str, max_names: int = MAX_NAMES_PER_PAGE) -> list[str]:
    """Extract candidate influencer names from text.

    Returns a deduplicated list of 2-3 capitalized word sequences,
    capped at `max_names`.

    Args:
        text: Raw markdown/text content from a page.
        max_names: Maximum number of candidate names to return.
    """
    if not text:
        return []

    matches = _prepare_text(text)
    seen: set[str] = set()
    unique: list[str] = []
    for name in matches:
        cleaned = _clean_and_filter(name)
        if cleaned is None:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(cleaned)

    return unique[:max_names]


def extract_candidate_names_with_counts(
    text: str,
    max_names: int = MAX_NAMES_PER_PAGE,
) -> dict[str, int]:
    """Extract candidate names with occurrence counts.

    Like `extract_candidate_names`, but returns a dict mapping each unique
    (cleaned, blocklist-filtered) name to how many times it appeared in the text.
    Used by NameMentionTracker for cross-page frequency analysis.

    Args:
        text: Raw markdown/text content from a page.
        max_names: Maximum number of distinct candidate names to return.
    """
    if not text:
        return {}

    matches = _prepare_text(text)
    raw_counts: dict[str, int] = {}
    for name in matches:
        cleaned = _clean_and_filter(name)
        if cleaned is None:
            continue
        raw_counts[cleaned] = raw_counts.get(cleaned, 0) + 1

    sorted_items = sorted(raw_counts.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items[:max_names])


def is_reddit_page(url: str) -> bool:
    """Check if a URL is a Reddit page."""
    try:
        return "reddit.com" in urlparse(url).netloc.lower()
    except Exception:
        return False


