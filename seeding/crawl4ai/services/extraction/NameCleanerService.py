"""
NameCleaner — Shared name cleanup and handle validation.

Injected into both LLMResponseParser and NameExtractor to enforce
consistent cleanup rules at the extraction source.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING
from urllib.parse import unquote

if TYPE_CHECKING:
    from names_dataset import NameDataset

logger = logging.getLogger(__name__)

# ── Name validation thresholds ──
# First word must rank ≤ this as a given name in any country.
FIRST_NAME_MAX_RANK = 5000
# Must rank in this many countries to count (filters ultra-rare names).
FIRST_NAME_MIN_COUNTRIES = 1
# Title prefixes that precede a given name — strip before lookup.
_TITLE_PREFIXES = frozenset({"dr", "prof", "coach", "sir", "dame", "rev"})



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
    # Nationality adjectives (two-word forms that pass _NAME_RE)
    "sri lankan", "south korean", "saudi arabian", "costa rican",
    "cape verdean", "saint lucian", "central african", "papua new",
    "american new",
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
    # Fitness niche terms ("Fat Loss" etc.)
    "fat loss", "fat burn",
    # Common-noun false positives that have rare first-name ranks
    "media post",
    # CTA phrases that match _NAME_RE (two CamelCase words)
    "free trial", "free webinar", "sign up", "read more", "see more",
    "load more", "show more", "view profile", "watch now",
    "get started", "try free", "book demo", "download app",
    "browse all", "contact us", "explore more", "view all",
    "continue reading", "related articles",
    "start your", "make money", "join our", "get email",
    "learn how", "how to", "find local", "about starting",
    "start free", "plan now", "get your", "double your",
    # Generic job titles / roles
    "personal trainer", "fitness model", "fitness influencer",
    "fitness coach", "yoga teacher", "yoga instructor",
    "brand ambassador", "beauty guru",
    "managing director", "marketing agency", "award winning",
    "world champion", "powerlifting coach",
    # Section heading phrases (listicle headings now pass through clean_name)
    "food influencers", "beauty influencers", "travel influencers",
    "fitness influencers", "fashion influencers", "lifestyle influencers",
    "tech influencers", "gaming influencers", "food bloggers",
    "beauty bloggers", "travel bloggers", "fashion bloggers",
    "food creators", "beauty creators", "travel creators",
    "fitness creators", "fashion creators", "lifestyle creators",
    # Niche-list headings / aggregator noise
    "female tiktokers", "hair tiktokers", "gym tiktokers",
    "hair youtubers", "male youtubers", "calisthenics youtubers",
    "youtuber name",
    # Analytics/scraper tool metrics
    "authority score", "average reel", "avg likes",
    "click analytic", "content style", "domain rating",
    "full profile", "campaign success", "why follow",
    "highly rated", "pro tip", "case studies", "final thoughts",
    "have questions", "frequently asked", "use ai-powered",
    "real estate", "black friday",
    "maximum storage", "check audience", "primary platform",
    "ai-powered profile", "domain authority", "overall quality",
    "digital marketing", "gym marketing", "marketing agencies",
    # Site chrome / aggregator brands
    "favikon democratizing", "favikon built",
    "social snowball", "social shepherd", "sprout social",
    "imagen insights", "zen planner", "feedspot reader",
    "la redoute", "virgin voyages",
    # Cookie consent / privacy banners
    "necessaryalways active", "analytics analytical",
    "performance performance", "strictly necessary",
    "refund policy", "influence operations", "supporting information",
    # Scraper artifacts / partial phrases
    "description the", "yoga with",
    "posts coachniche", "posts athleteniche", "posts personal",
    "functional functional", "south african",
    "second test", "second bio", "male request",
    "agencies top", "agencies in", "video how", "why it",
    "business ideas", "weight loss", "bikini body",
    "insurance catch", "two months", "places ashes",
    "have been", "photos will", "have astonishing",
    "demo and", "questions thread", "study the",
    # Occupation / industry phrases extracted as names
    "marine electrical", "british climate",
    # Single-word handles that pass as names
    "favikon_",
})

# Video games, franchises, gaming brands — not people
_GAME_BLOCKLIST = frozenset({
    # The Sims / simulation
    "the sims", "the sim",
    # Open-world / action
    "far cry", "grand theft", "theft auto", "san andreas", "vice city", "liberty city",
    "red dead", "dead redemption", "black myth", "myth wukong",
    "watch dogs", "watch dog", "just cause",
    # Call of Duty family
    "call duty", "modern warfare", "advanced warfare", "black ops",
    "infinite warfare", "ghost recon",
    # Ubisoft franchises
    "assassins creed", "assassin creed", "black flag", "rainbow six",
    "splinter cell", "riders republic", "trials rising",
    # EA / sports
    "need speed", "fifa 23", "fifa 24", "madden nfl",
    "nba 2k", "wwe 2k", "tony hawk", "skate 3",
    "forza horizon", "gran turismo", "dirt rally", "assetto corsa", "project cars",
    # FromSoftware / soulslike
    "dark souls", "dark soul", "demon souls", "blood borne",
    "elden ring", "shadow erdtree",
    # Horror / survival
    "resident evil", "silent hill", "silent hills",
    "dead space", "dead island", "alan wake",
    "dying light", "last us",
    # RPG / JRPG
    "final fantasy", "dragon quest", "dragon age", "mass effect",
    "kingdom hearts", "persona 5", "shin megami", "devil may",
    "baldurs gate", "baldur gate", "outer worlds",
    "fire emblem", "xenoblade chronicles", "zero escape",
    "disco elysium",
    # Nintendo first-party
    "super mario", "mario kart", "mario party", "mario odyssey",
    "mario wonder", "mario bros", "donkey kong",
    "animal crossing", "new horizons",
    "super smash", "smash bros",
    "luigis mansion", "splatoon 2", "splatoon 3",
    "breath wild", "tears kingdom", "skyward sword",
    "twilight princess", "ocarina time", "majoras mask", "wind waker",
    "wii sports", "wii fit", "wii play",
    # Pokémon variants (two-word color names pass _NAME_RE)
    "pokemon red", "pokemon blue", "pokemon gold", "pokemon silver",
    "pokemon diamond", "pokemon pearl", "pokemon sun", "pokemon moon",
    "pokemon sword", "pokemon shield", "pokemon scarlet", "pokemon violet",
    # Sony exclusives
    "god war", "ghost tsushima", "stellar blade", "rise ronin",
    "spider man", "spiderman", "guardians galaxy",
    # Bethesda / open world
    "star field", "elder scrolls", "fallout 4", "fall out",
    "no mans", "mans sky",
    # Rockstar
    "rockstar games",
    # Fighting games
    "street fighter", "mortal kombat", "soul calibur",
    "killer instinct", "guilty gear", "virtua fighter",
    "tekken 8", "dragon ball", "jump force",
    # Shooter / BR
    "counter strike", "global offensive",
    "apex legends", "rocket league", "fall guys", "fall guy",
    "among us", "lethal company", "destiny 2",
    "battle front", "jedi fallen", "jedi survivor", "old republic",
    "star wars", "star craft", "war craft",
    # MOBA / strategy
    "league legends", "age empires", "total war",
    "company heroes", "command conquer",
    "diablo 4", "diablo 3", "hearth stone", "heroes storm",
    # Open world survival / sandbox
    "ark survival", "conan exiles", "genshin impact",
    "honkai star", "zenless zone", "deep rock",
    "stardew valley", "rim world", "dyson sphere",
    "manor lords", "manor lord", "cities skylines",
    "kerbal space", "sea thieves", "state decay",
    # Misc popular titles
    "sonic hedgehog", "pac man", "tomb raider",
    "walking dead", "metal gear", "phantom pain",
    "monster hunter", "monster hunters",
    "borderlands 2", "border lands", "tiny tina", "wonder lands",
    "hogwarts legacy", "suicide squad", "gotham knights",
    "hollow knight", "dead cells", "outer wilds",
    "slay spire", "vampire survivors",
    "just dance", "oregon trail", "human fall", "fall flat",
    "garry mod", "garrys mod",
    "indie game", "indie games",
    # Publishers / studios (two-word forms)
    "riot games", "epic games", "electronic arts", "activision blizzard",
    "square enix", "bandai namco", "cd projekt", "from software",
    "larian studios", "naughty dog", "insomniac games",
    "guerrilla games", "platinum games", "kojima productions",
    "sucker punch", "santa monica", "devolver digital",
    "paradox interactive", "creative assembly", "firaxis games",
    "gearbox software", "respawn entertainment", "supergiant games",
    "annapurna interactive", "coffee stain", "team cherry",
    "xbox games", "sony interactive", "microsoft gaming",
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
    | _GENERIC_BLOCKLIST | _CELEBRITY_BLOCKLIST | _GAME_BLOCKLIST
)

# LinkedIn slug pattern: first-last-1234567
_LINKEDIN_SLUG_RE = re.compile(r'^[a-z]+-[a-z]+(?:-[a-z0-9]+)*-\d{4,}$')


# ══════════════════════════════════════════════════════════════════════
# Name Validation (lazy-loaded names-dataset)
# ══════════════════════════════════════════════════════════════════════

_name_dataset: "NameDataset | None" = None


def _load_name_dataset() -> "NameDataset":
    """Lazy-load the NameDataset on first use."""
    global _name_dataset
    if _name_dataset is None:
        from names_dataset import NameDataset as _ND
        _name_dataset = _ND()
        logger.info("Loaded names-dataset for name validation")
    return _name_dataset


def _is_plausible_person_name(name: str) -> bool:
    """Check if the first word is a commonly-ranked given name.

    Uses the names-dataset first_name rank data. The first word
    must rank ≤ FIRST_NAME_MAX_RANK in ≥ FIRST_NAME_MIN_COUNTRIES
    countries. This filters noise phrases ("Media Post", "World Record")
    while passing real person names ("Jeff Nippard", "Stefi Cohen").

    Supports multiple languages out of the box — the dataset covers
    names across 100+ countries.
    """
    parts = name.split()
    if len(parts) < 2:
        return False
    nd = _load_name_dataset()
    first_word = parts[0]
    # Strip title prefix: "Dr Mike" → look up "Mike"
    if first_word.lower().rstrip(".") in _TITLE_PREFIXES and len(parts) >= 2:
        first_word = parts[1]
    # Strip possessive suffix: "Sophie's" → "Sophie"
    for suffix in ("\u2019s", "'s"):
        if first_word.endswith(suffix):
            first_word = first_word[: -len(suffix)]
            break
    first_word = first_word.rstrip("'\u2019")
    result = nd.search(first_word)
    fn_data = result.get("first_name")
    if not fn_data:
        return False
    ranks = fn_data.get("rank") or {}
    ranked_countries = [
        r for r in ranks.values()
        if r is not None and r <= FIRST_NAME_MAX_RANK
    ]
    return len(ranked_countries) >= FIRST_NAME_MIN_COUNTRIES



class NameCleanerService:
    """Shared name cleanup — injected into LLMResponseParser + NameExtractor."""

    @staticmethod
    def clean_name(name: str) -> str | None:
        """Clean a raw name. Returns None to reject.

        Pipeline:
          1. Decode URL-encoded strings (reject if still garbled)
          2. Extract name via _NAME_RE.search() — two CamelCase words
             (cuts through bold, numbering, emoji, markdown garbage)
          3. Reject non-person entities (countries, brands, news orgs)
          4. Reject via names-dataset — if first word is not a known given name
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
        if not extracted or len(extracted) <= 3:
            return None

        if _is_non_person(extracted):
            return None

        if not _is_plausible_person_name(extracted):
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
