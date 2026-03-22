"""
RegexHandleExtractor — Fast, deterministic handle extraction from HTML.

Extracts social media handles from raw HTML or markdown using regex.
Runs before the LLM fallback to capture structured data cheaply.

NOTE: Similar URL patterns exist in enrichment/patterns.py — keep in sync.

Regex patterns sourced from:
  - lorey/social-media-profiles-regexs (GitHub, 1.4K stars)
  - Real-world research across 5+ listicle sites (see docs/handle_patterns.md)

Proven patterns:
 1. instagram.com/{handle} + instagr.am/{handle}    — IG profile links
 2. tiktok.com/@{handle}                            — TikTok profile links
 3. youtube.com/@{handle}                           — YouTube @handle links
 4. youtube.com/c/{handle}                          — YouTube custom URL
 5. youtube.com/user/{handle}                       — YouTube legacy user URL
 6. youtube.com/channel/UC...                       — YouTube channel ID (for resolution)
 7. x.com/{handle} + twitter.com/{handle}           — X/Twitter profile links
 8. [@handle](https://instagram.com/...)             — markdown link (crawl4ai output)
 9. @handle in plain text                            — inline mention
10. A post shared by Name (@handle)                  — embedded IG posts
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from services.extraction.NameCleanerService import NameCleanerService



# ══════════════════════════════════════════════════════════════════════
# Compiled Patterns — sourced from lorey/social-media-profiles-regexs
# + TikTok and extra YouTube patterns added for our use case
# ══════════════════════════════════════════════════════════════════════

# Instagram: instagram.com/{handle} and instagr.am/{handle}
# Lorey pattern: no consecutive dots allowed, max 30 chars
_IG_PROFILE = re.compile(
    r'(?:instagram\.com|instagr\.am)/([A-Za-z0-9_](?:[A-Za-z0-9_.](?!\.\.)){0,28}[A-Za-z0-9_])(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# TikTok: tiktok.com/@{handle}
_TT_PROFILE = re.compile(
    r'tiktok\.com/@([A-Za-z0-9_.]{2,30})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# YouTube @handle: youtube.com/@{handle}
_YT_AT_HANDLE = re.compile(
    r'youtube\.com/@([A-Za-z0-9_.\-]{2,30})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# YouTube custom URL: youtube.com/c/{handle}
_YT_CUSTOM = re.compile(
    r'youtube\.com/c/([A-Za-z0-9_.\-]{2,30})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# YouTube legacy user: youtube.com/user/{handle}
_YT_USER = re.compile(
    r'youtube\.com/user/([A-Za-z0-9_.\-]{2,30})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# YouTube channel ID: youtube.com/channel/UC... (for later resolution)
_YT_CHANNEL_ID = re.compile(
    r'youtube\.com/channel/(UC[A-Za-z0-9_\-]{20,26})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# X/Twitter: x.com/{handle} or twitter.com/{handle}
# Lorey pattern: alphanumeric + underscore only, exclude known paths
_TWITTER_PROFILE = re.compile(
    r'(?:twitter\.com|x\.com)/(@?[A-Za-z0-9_]{1,15})(?:/|\b|"|\'|\)|\?)',
    re.IGNORECASE,
)

# URL-based patterns grouped: (pattern, platform_name)
_URL_PATTERNS: list[tuple[re.Pattern, str]] = [
    (_IG_PROFILE,    "Instagram"),
    (_TT_PROFILE,    "TikTok"),
    (_YT_AT_HANDLE,  "YouTube"),
    (_YT_CUSTOM,     "YouTube"),
    (_YT_USER,       "YouTube"),
    (_TWITTER_PROFILE, "Twitter"),
]

# Plain text @handle (e.g. "Instagram: @run_with_tom")
# Uses (?<!\S) — not preceded by ANY non-whitespace char — so
# "*****@evolved.gg" and "user@email.com" are both blocked.
_AT_MENTION = re.compile(r'(?<!\S)@([A-Za-z0-9_.]{3,30})(?!\w)')

# Email pattern: <nonwhitespace>@<word chars>.<tld>
# Pre-filter: we strip these from text before running _AT_MENTION
# to provide belt-and-suspenders coverage for any edge cases
# (e.g. emails at start-of-string where (?<!\S) would also pass).
_EMAIL_PATTERN = re.compile(r'[^\s@]+@[A-Za-z0-9._-]+\.[A-Za-z]{2,}')

# Instagram embed: "A post shared by Name (@handle)" or "A post shared by (@handle)"
_IG_EMBED = re.compile(
    r'(?:A post shared by|shared by)\s+(.+?)?\s*\(@([A-Za-z0-9_.]{2,30})\)',
    re.IGNORECASE,
)

# ══════════════════════════════════════════════════════════════════════
# Ignore Lists
# ══════════════════════════════════════════════════════════════════════

# Handles to ignore — organized into named categories for readability & testing.

# ── Path segments (not handles, just URL parts) ──
_IGNORE_PATH_SEGMENTS = frozenset({
    # Instagram
    "p", "reel", "reels", "stories", "explore", "tv", "accounts",
    "about", "directory", "developer", "legal", "shopping", "blog",
    "nametag", "press", "branded_content",
    # TikTok
    "foryou", "following", "live", "discover", "upload",
    # YouTube
    "channel", "watch", "playlist", "shorts", "feed", "gaming",
    "music", "premium", "results",
    # Twitter/X
    "home", "share", "privacy", "tos", "search", "hashtag",
    "i", "settings", "notifications", "messages", "compose",
    "intent", "login", "signup",
    # Generic
    "tag", "tags", "embed", "help", "terms",
})

# ── CSS / JSON-LD at-rules (leaked from page source) ──
_IGNORE_CSS_ATRULES = frozenset({
    "context", "type", "media", "font", "keyframes", "import",
    "charset", "supports", "namespace", "page", "layer",
    "font-face", "document", "counter-style", "property",
    "container", "scope", "starting-style",
    "id", "value", "list", "set", "language", "reverse",  # JSON-LD @graph residuals
    # Tailwind CSS breakpoint classes
    "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl", "6xl", "7xl",
    "xs", "xxl", "xxxl",
})

# ── JS frameworks / bundlers (leaked from source code) ──
_IGNORE_JS_FRAMEWORKS = frozenset({
    "vue", "babel", "license", "nuxt", "webpack", "vite",
    "react", "angular", "svelte", "next", "remix",
    "tailwind", "postcss", "eslint", "prettier", "typescript",
    "rollup", "parcel", "jest", "mocha", "cypress",
})

# ── Template placeholders / generic ──
_IGNORE_PLACEHOLDERS = frozenset({
    "username", "handle", "user", "example", "test",
    "your_username", "yourhandle", "sample", "your_handle",
    "graph",  # JSON-LD @graph
})

# ── Platform names as naked handles ──
_IGNORE_PLATFORM_NAMES = frozenset({
    "instagram", "tiktok", "youtube", "twitter",
    "facebook", "snapchat", "pinterest",
})

# ── Listicle / aggregator site accounts ──
_IGNORE_AGGREGATORS = frozenset({
    "gymfluencers", "gymfluencers.agency",
    "feedspot", "feedspotdotcom", "modash", "modash.io",
    "seekahost", "trainerize", "favikon", "favikon_",
    "popularpays", "collabstr", "heepsy",
    "lefty", "socialtradia", "socialtradia_", "ugcfactory",
    "insense", "clickanalytic", "theinfluenceroom",
    "izea", "disrupt", "disruptmkting",
    "popular-pays", "popularpays9201",
    "feedspotofficial", "_feedspot",
    "influencer-hero", "influencerhero",
    "hypeauditor", "influencity", "socialbook", "thesocialcat",
})

# ── Brands: Media & news ──
_IGNORE_BRANDS_MEDIA = frozenset({
    # ── Wire services / agencies ──
    "reuters", "apnews", "afp",
    # ── US TV networks ──
    "cnn", "msnbc", "nbcnews", "nbcnightlynews", "nbcnewyork", "todayshow",
    "abcnews", "abc7news", "abc7ny",
    "cbsnews", "cbseveningnews",
    "foxnews", "foxbusiness", "fox5ny", "livenowfox", "ktvufox2", "kmphfox26",
    "fox10news",
    "espn", "dazn", "cspan",
    "pbs", "npr",
    "pix11news", "news12", "news4jax", "news6wkmg", "news19wltx",
    "wflanewschannel8", "firstcoastnews", "newscentermaine", "kslnews",
    "gulfcoastnewsnow", "wqadnews8",
    # ── US newspapers / digital ──
    "nytimes", "washingtonpost", "wsj", "nypost",
    "usatoday", "latimes", "chicagotribune", "bostonglobe",
    "sfchronicle", "dallasnews", "politico",
    # ── UK TV networks ──
    "bbc", "bbcnews", "bbcworld", "bbcbreaking",
    "skynews", "skynewsaustralia", "skysports", "skysportsnews",
    "channel4news", "5newsuk", "itvnews",
    "stvnews", "lbc", "lbcnews",
    # ── UK newspapers ──
    "guardian", "theguardian", "guardiannews",
    "financialtimes", "telegraph", "dailytelegraph",
    "thetimes", "dailymail", "mailonline",
    "thesun", "mirror", "dailymirror",
    "independent", "theindependent",
    "eveningstandard", "metro", "scottishdailyrecord",
    # ── Europe ──
    "dwnews", "deutschewelle", "euronews",
    "lemonde", "lefigaro", "leparisien",
    "derspiegel", "baborevista", "elpais", "elmundo",
    "corriere", "repubblica", "rtenews",
    "france24", "france24english",
    # ── Australia / NZ ──
    "7news", "9newsaus", "1newsnz",
    "abcnewsaustralia", "abcnewsindepth",
    "newscomauhq", "nzheraldtv", "forces_news",
    "sabcdigitalnews",
    # ── Canada ──
    "cbcnews", "cbcbritishcolumbia", "cbcthenational",
    "globalnews", "ctvnews", "torontostar",
    # ── LATAM ──
    "telemundo", "univision", "globonews", "globoplay",
    "bbcmundo", "bbcbrasil", "tvcnewsnigeria",
    # ── Africa / Middle East ──
    "aljazeera", "aljazeeraenglish",
    "newscentralafrica", "kenyadigitalnews", "newscentral",
    # ── Business / Tech press ──
    "forbes", "bloomberg", "bloombergtechnology",
    "businessinsider", "cnbc",
    "buzzfeed", "huffpost", "vice", "vicenews", "vox", "wired", "techcrunch",
    "engadget", "theverge", "mashable",
    # ── Misc news YT channels ──
    "ainewsofficial", "artificialintelligencenews1373",
    "safetyworldnews", "nextnewsnetwork", "rebelnewsonline",
    "786live",
    # ── News-like generic ──
    "federalnewsnet",
})

# ── Brands: Sports organizations ──
_IGNORE_BRANDS_SPORTS = frozenset({
    "nba", "nfl", "nhl", "mlb", "ufc", "wwe", "fifa", "uefa",
    "premierleague", "laliga", "seriea", "bundesliga", "ligue1",
    "realmadrid", "fcbarcelona", "manchesterunited", "chelseafc",
    "arsenal", "liverpoolfc", "tottenham",
    "championsleague", "olympics", "formula1", "f1",
})

# ── Brands: Tech / platforms ──
_IGNORE_BRANDS_TECH = frozenset({
    "google", "apple", "microsoft", "amazon", "meta", "netflix",
    "spotify", "samsung", "sony", "nvidia", "intel", "amd", "tesla",
    "openai", "tiktok_us", "whatsapp", "telegram",
    "primevideo", "amazonprime", "disneyplus", "hbomax", "hulu",
    "paramount", "peacock",
})

# ── Brands: AI companies / products ──
_IGNORE_BRANDS_AI = frozenset({
    "chatgpt", "chatopenai", "metaai", "metademolab",
    "midjourney", "midjourneyartwork", "midjourneyai",
    "anthropic", "claude", "claudeai",
    "gemini", "googleai", "googledeepmind", "deepmind",
    "stability", "stabilityai", "stablediffusion",
    "runway", "runwayml", "runwayai",
    "inworldai", "inworld",
    "jasper", "jasperai",
    "copy.ai", "copyai",
    "synthesia", "synthesiaai",
    "dallE", "dall_e", "dalle",
    "perplexity", "perplexityai",
    "huggingface", "replicate",
    "cohere", "coherai",
    "copilot", "githubcopilot",
    "objectiveinc",
    "skim-ai", "skimai",
})

# ── Brands: Fashion & beauty ──
_IGNORE_BRANDS_FASHION = frozenset({
    "nike", "adidas", "puma", "underarmour", "newbalance", "reebok",
    "gucci", "louisvuitton", "chanel", "dior", "prada", "hermes",
    "zara", "hm", "uniqlo", "shein", "asos",
    "victoriassecret", "fentybeauty", "elfcosmetics", "sephora",
    "lorealparis", "maybelline", "maccosmetics", "nars", "rarebeauty",
    "gymshark", "lululemon",
    "ehplabs", "insanelabz", "aloyoga", "hooters",
})

# ── Brands: Food & drink ──
_IGNORE_BRANDS_FOOD = frozenset({
    "mcdonalds", "starbucks", "cocacola", "pepsi", "redbull",
    "chipotle", "wendys", "burgerking", "kfc", "pizzahut",
    "dominos", "dunkin", "popeyes", "nandos", "greggs",
    "budweiser", "heineken", "absolut",
})

# ── Brands: Entertainment ──
_IGNORE_BRANDS_ENTERTAINMENT = frozenset({
    "disney", "marvel", "dccomics", "starwars", "pixar",
    "universalpictures", "warnerbrosmovies", "paramountpics",
    "nationalgeographic", "natgeo", "nasa",
    "cocomelon", "tseries",
})

# ── Brands: Airlines & travel ──
_IGNORE_BRANDS_TRAVEL = frozenset({
    "ryanair", "easyjet", "britishairways", "emirates", "qantas",
    "delta", "united", "americanair", "southwest",
    "airbnb", "booking", "tripadvisor", "expedia",
})

# ── Brands: Auto ──
_IGNORE_BRANDS_AUTO = frozenset({
    "bmw", "mercedesbenz", "porsche", "ferrari", "lamborghini",
    "audi", "volkswagen", "toyota", "honda", "ford",
})

# ── Brands: Retail & other ──
_IGNORE_BRANDS_RETAIL = frozenset({
    "walmart", "target", "costco", "ikea", "homedepot",
    "scrubdaddy", "duolingo", "crocs",
})

# ── Generic non-person terms ──
_IGNORE_GENERIC = frozenset({
    "hotel", "hotels", "hostel", "resort",
    # Scraped data labels (not handles)
    "followers", "followers.weekly",
    # Country names & codes
    "usa", "uk", "nz", "au", "ca", "de", "fr", "es", "it", "jp",
    "australia", "canada", "germany", "france", "spain", "italy",
    "japan", "india", "brazil", "mexico", "china",
    "ireland", "scotland", "wales", "england",
    "dubai", "singapore", "hongkong",
    # Major city names
    "london", "newyork", "nyc", "losangeles", "la",
    "paris", "tokyo", "sydney", "melbourne", "toronto",
    "berlin", "amsterdam", "barcelona", "dubai", "mumbai",
    # Language codes
    "en",
})

# ── Non-fitness celebrities, politicians, comedians ──
_IGNORE_CELEBRITIES: frozenset[str] = frozenset({
    "kamalaharris", "barbie", "charliekirk1776", "officialbenshapiro",
    "miakhalifa", "halleberry", "djpaulyd", "fluffyguy", "canelo",
    "wwerollins", "deepakchopra", "medicalmedium", "khloekardashian",
    "kimkardashian", "kyliejenner", "taylorswift", "therock",
    "selenagomez", "arianagrande", "beyonce", "justinbieber",
    "cristiano", "leomessi", "neymarjr", "viaborges",
    "jenniferaniston", "dualipa", "badgalriri", "zendaya",
    "vindiesel", "priyankachopra", "tomholland2013",
})

# ── Fitness-adjacent brands / product lines ──
_IGNORE_BRANDS_FITNESS: frozenset[str] = frozenset({
    "fashionnova", "balenciaga", "pockyusa", "tastemade",
    "kerastase_official", "amazonfashioneu", "monsterenergy",
    "jbwwatches", "buffbunny", "hydrojug", "popsugar",
    "thealiveapp", "fitnessculturegym", "younglaforher",
    "tier1supplements", "plantfitapp", "gymgirlslockerroom",
    "enroutejewelry_", "roamlosangeles", "avancusofficial",
    "james_cosmetics", "shopform",
})

# ── Combined ignore set ──
_IGNORE_HANDLES = frozenset(
    _IGNORE_PATH_SEGMENTS
    | _IGNORE_CSS_ATRULES
    | _IGNORE_JS_FRAMEWORKS
    | _IGNORE_PLACEHOLDERS
    | _IGNORE_PLATFORM_NAMES
    | _IGNORE_AGGREGATORS
    | _IGNORE_BRANDS_MEDIA
    | _IGNORE_BRANDS_SPORTS
    | _IGNORE_BRANDS_TECH
    | _IGNORE_BRANDS_AI
    | _IGNORE_BRANDS_FASHION
    | _IGNORE_BRANDS_FOOD
    | _IGNORE_BRANDS_ENTERTAINMENT
    | _IGNORE_BRANDS_TRAVEL
    | _IGNORE_BRANDS_AUTO
    | _IGNORE_BRANDS_RETAIL
    | _IGNORE_GENERIC
    | _IGNORE_CELEBRITIES
    | _IGNORE_BRANDS_FITNESS
)

_IGNORE_PREFIXES = ("utm_", "ig_", "ref=", "img_", "case-study-")

# Substring patterns — any handle/name containing these is rejected
_IGNORE_SUBSTRINGS = (
    "uncensored",
    # ── Profanity / vulgarity ──
    "fuck", "shit", "bitch", "damn", "crap", "piss",
    # ── Sexual / NSFW ──
    "sex", "porn", "xxx", "nsfw", "nude", "onlyfans",
    "hentai", "fetish", "bdsm", "slut", "whore", "stripper", "thot", "milf",
    "dildo", "orgasm", "erotic", "penis", "vagina",
    "blowjob", "cumshot", "creampie", "cum", "tits", "boob", "pussy",
    # ── Gross-out ──
    "fart", "booty", "diaper", "poop",
    # ── Slurs / hate ──
    "nigga", "nigger", "faggot", "retard",
    # NOTE: excluded due to false positives on common words:
    #   "ass" (classic, bass, pass)    "pee" (speed, peep, peer)
    #   "cock" (peacock, hancock)      "dick" (dickenson)
    #   "naked" (nakednutrition, nakedpalette)
)

# Domain-like suffixes that indicate leaked email/domain fragments, not handles
_DOMAIN_SUFFIXES = (
    ".com", ".co", ".uk", ".io", ".org", ".net", ".me",
    ".co.uk", ".com.au", ".de", ".fr", ".es", ".it",
    ".academy", ".app", ".dev", ".info", ".tv", ".ai", ".xyz",
    ".agency", ".blog", ".store", ".shop", ".site",
)


# ══════════════════════════════════════════════════════════════════════
# Data Classes
# ══════════════════════════════════════════════════════════════════════

@dataclass
class ExtractedHandle:
    """A single handle extracted from HTML/markdown."""
    handle: str       # Bare handle without @
    platform: str     # "Instagram", "TikTok", "YouTube", "Twitter", or "" (unknown)
    name: str = ""    # Name if extractable from context (embed, heading)
    source_url: str = ""  # Origin URL (set by DDG direct extraction)




# ══════════════════════════════════════════════════════════════════════
# Service
# ══════════════════════════════════════════════════════════════════════

class RegexHandleExtractorService:
    """Fast, deterministic handle extraction from HTML/markdown via regex.

    All methods are stateless and exposed as static methods.
    Regex patterns are compiled once at module load time.
    """

    # API:

    @staticmethod
    def extract_handles_from_html(html: str) -> list[ExtractedHandle]:
        """Extract all social media handles from raw HTML or markdown.

        Returns a deduplicated list of ExtractedHandle objects.
        Extraction priority: IG embeds (have names) → URLs → @mentions.
        """
        seen: set[tuple[str, str]] = set()   # (lowercase handle, platform) → dedup key
        seen_handles: set[str] = set()        # all seen handles (for @mention dedup)
        results: list[ExtractedHandle] = []

        def _add(handle: str, platform: str, name: str = "") -> None:
            handle_clean = handle.lower().rstrip(".")
            key = (handle_clean, platform)
            if key not in seen and RegexHandleExtractorService.is_valid_handle(handle_clean):
                seen.add(key)
                seen_handles.add(handle_clean)
                results.append(ExtractedHandle(
                    handle=handle.rstrip("."),
                    platform=platform,
                    name=name.strip() if name else "",
                ))

        # 1. Instagram embed pattern FIRST (highest value — carries name)
        #    "A post shared by Name (@handle)"
        for match in _IG_EMBED.finditer(html):
            name_raw = match.group(1) or ""
            handle = match.group(2)
            # Clean name: remove trailing " |" and similar
            name = re.sub(r'\s*[|/\\].*$', '', name_raw).strip()
            _add(handle, "Instagram", NameCleanerService.clean_name(name) or "")

        # 2. URL-based extraction (high confidence, platform identified)
        for pattern, platform in _URL_PATTERNS:
            for match in pattern.finditer(html):
                handle = match.group(1).lstrip("@")  # Twitter handles may have @
                _add(handle, platform)

        # 3. @mention extraction (lower confidence — no platform info)
        #    Skip handles already seen from URL-based extraction (any platform).
        #    Pre-filter: remove email addresses (word@domain.tld) before scanning
        #    so that obfuscated emails like "*****@evolved.gg" cannot match.
        html_without_emails = _EMAIL_PATTERN.sub(" ", html)
        for match in _AT_MENTION.finditer(html_without_emails):
            handle = match.group(1)
            if handle.lower().rstrip(".") not in seen_handles:
                _add(handle, "", "")  # Empty platform = unknown

        return results

    @staticmethod
    def extract_youtube_channel_ids(html: str) -> list[str]:
        """Extract YouTube channel IDs (UC...) from HTML for later resolution.

        These need an HTTP request to youtube.com/channel/UC... to resolve
        the channel's @handle. Returns a list of unique channel IDs.
        """
        seen: set[str] = set()
        ids: list[str] = []
        for match in _YT_CHANNEL_ID.finditer(html):
            cid = match.group(1)
            if cid not in seen:
                seen.add(cid)
                ids.append(cid)
        return ids

    @staticmethod
    def extract_handles_from_url(url: str) -> ExtractedHandle | None:
        """Extract a handle from a single URL (for DDG search result processing).

        Used by SearchService to extract handles directly from DDG result URLs
        before crawling — e.g. if DDG returns instagram.com/kayla_itsines,
        extract the handle immediately.
        """
        for pattern, platform in _URL_PATTERNS:
            match = pattern.search(url)
            if match:
                handle = match.group(1).lstrip("@")
                if RegexHandleExtractorService.is_valid_handle(handle.lower().rstrip(".")):
                    return ExtractedHandle(handle=handle, platform=platform)
        return None

    @staticmethod
    @staticmethod
    def is_blocked_handle(handle: str) -> bool:
        """Check if a handle string is in the blocklist.

        Single source of truth for handle-level blocking.
        Used by both RegexHandleExtractorService (during extraction) and
        InfluencerMerger (during seed filtering, via DI).
        """
        h = handle.lower().rstrip(".")
        if h in _IGNORE_HANDLES:
            return True
        if any(h.startswith(prefix) for prefix in _IGNORE_PREFIXES):
            return True
        if any(sub in h for sub in _IGNORE_SUBSTRINGS):
            return True
        return False

    @staticmethod
    def is_valid_handle(handle: str) -> bool:
        """Return True if the handle passes all validity checks.

        Filters out URL path segments, tracking params, pure numerics,
        domain leaks, and anything in the blocklist.
        """
        h_lower = handle.lower().rstrip(".")
        if RegexHandleExtractorService.is_blocked_handle(handle):
            return False
        if len(h_lower) < 2:
            return False
        # Pure numeric = post IDs, not handles
        if h_lower.isdigit():
            return False
        # Consecutive dots = invalid on most platforms (lorey rule)
        if ".." in h_lower:
            return False
        # Domain-suffix filter: handles ending in .com, .co.uk etc. are email/domain leaks
        if any(h_lower.endswith(suffix) for suffix in _DOMAIN_SUFFIXES):
            return False
        # Handles containing .com anywhere (e.g. "brookeence.comUse") are email fragments
        if ".com" in h_lower and not h_lower.endswith(".com"):
            return False
        return True

    @staticmethod
    def count_handles(html: str) -> int:
        """Count unique social media handles in HTML."""
        return len(RegexHandleExtractorService.extract_handles_from_html(html))

    # Internal:


# ══════════════════════════════════════════════════════════════════════
# Module-level aliases — restores pre-refactor public API surface
# Tests and callers may import these directly from this module.
# ══════════════════════════════════════════════════════════════════════

extract_handles_from_html = RegexHandleExtractorService.extract_handles_from_html
extract_youtube_channel_ids = RegexHandleExtractorService.extract_youtube_channel_ids
extract_handles_from_url = RegexHandleExtractorService.extract_handles_from_url


