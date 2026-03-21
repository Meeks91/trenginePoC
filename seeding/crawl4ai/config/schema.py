from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterator, Optional


# ── Enums ──

class Platform(str, Enum):
    """Supported social media platforms."""
    Instagram = "Instagram"
    YouTube = "YouTube"
    TikTok = "TikTok"


class SourceType(str, Enum):
    """Provenance of a name mention extraction."""
    REGEX = "regex"
    LLM = "llm"
    REDDIT = "reddit"
    NON_REDDIT = "non-reddit"


# ── Crawl Output ──

@dataclass
class PageResult:
    """Result of crawling a single URL."""
    url: str
    query: str                  # The search query that discovered this URL
    raw_markdown: str           # Full unfiltered page
    fit_markdown: str           # After PruningContentFilter
    raw_token_estimate: int     # len(raw) // 4
    fit_token_estimate: int     # len(fit) // 4
    success: bool
    error: Optional[str] = None
    md_path: Optional[str] = None  # Path where fit_markdown was saved
    handles_in_source: int = 0     # Unique handles found in raw HTML via regex


# ── Category Provenance ──

@dataclass
class CategoryCitation:
    """One subcategory search that surfaced an influencer.

    Provenance is config-based: the influencer inherits the category/sub
    of the config (SeedJob) that discovered the URL it was extracted from.
    """
    category: str   # Top-level category key, e.g. "FITNESS"
    sub: str        # Subcategory name, e.g. "Science-Based Training"
    citations: int  # Pages from this sub's search that cited this influencer

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "sub": self.sub,
            "citations": self.citations,
        }


# ── Extraction Output ──

@dataclass
class Influencer:
    """A single extracted influencer.

    Attributes:
        name: Display name (real name only, empty string if unknown).
        handles: Platform-to-handle mapping, e.g. {Platform.Instagram: "foodgod"}.
        most_seen_category: Subcategory name with the most page hits.
        seen_in_categories: All subcategory searches that surfaced this
            influencer, with per-sub citation counts. Populated by config
            provenance tracing during pipeline processing.
        source_urls: Distinct page URLs where this influencer was found.
        extraction_methods: How this influencer was discovered
            (e.g. {"regex", "llm", "ddg_direct"}).
    """
    name: str
    handles: dict[Platform, str] = field(default_factory=dict)
    most_seen_category: str = ""
    seen_in_categories: list[CategoryCitation] = field(default_factory=list)
    source_urls: set[str] = field(default_factory=set)
    extraction_methods: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        from services.extraction.NameCleaner import NameCleaner
        cleaned = NameCleaner.clean_name(self.name)
        self.name = cleaned or ""

    @property
    def ig_handle(self) -> str:
        """Instagram handle (empty string if not present)."""
        return self.handles.get(Platform.Instagram, "")

    @property
    def tk_handle(self) -> str:
        """TikTok handle (empty string if not present)."""
        return self.handles.get(Platform.TikTok, "")

    @property
    def yt_handle(self) -> str:
        """YouTube handle (empty string if not present)."""
        return self.handles.get(Platform.YouTube, "")

    @property
    def citation_count(self) -> int:
        """Number of distinct source pages citing this influencer."""
        return len(self.source_urls)

    def to_dict(self) -> dict:
        """Serialize to DB-ready dict with flattened platform handle columns."""
        return {
            "name": self.name,
            "ig_handle": self.ig_handle,
            "tk_handle": self.tk_handle,
            "yt_handle": self.yt_handle,
            "most_seen_category": self.most_seen_category,
            "seen_in_categories": [
                cc.to_dict() for cc in self.seen_in_categories
            ],
            "source_urls": sorted(self.source_urls),
            "extraction_methods": sorted(self.extraction_methods),
            "citation_count": self.citation_count,
        }


# ── Name Mention Output ──

@dataclass
class NameMentionRecord:
    """Raw name mention data for final output.

    Captures cross-page name frequency, source provenance, and
    whether DDG resolution was attempted/successful.
    """
    canonical: str                 # Most-cited variant
    variants: list[str] = field(default_factory=list)
    mention_count: int = 0         # Total occurrences across all pages
    source_types: list[str] = field(default_factory=list)  # [SourceType values]
    source_urls: list[str] = field(default_factory=list)   # Pages that contributed
    was_searched: bool = False
    resolved_handle: str = ""      # Handle found via DDG (if any)
    resolved_platform: str = ""    # Platform of resolved handle

    def to_dict(self) -> dict:
        return {
            "canonical": self.canonical,
            "variants": self.variants,
            "mention_count": self.mention_count,
            "source_types": self.source_types,
            "source_urls": self.source_urls,
            "was_searched": self.was_searched,
            "resolved_handle": self.resolved_handle,
            "resolved_platform": self.resolved_platform,
        }


# ── Source Tracing ──

@dataclass
class HandleSource:
    """Where a specific handle was found."""
    page: str          # URL of the source page
    source_type: str   # "href", "regex", "ddg_direct", "llm"

@dataclass
class SourceResult:
    """Ties a crawled URL back to extracted influencers — for audit trail."""
    url: str
    query: str
    md: str               # Path to saved markdown file
    influencers: list[Influencer] = field(default_factory=list)


# ── Per-Config Results (flat, config-keyed) ──

@dataclass
class InfluencerResult:
    """One influencer in a config result — with all platform handles and source provenance."""
    name: str
    handles: dict[str, str] = field(default_factory=dict)       # {"Instagram": "kayla_itsines", "TikTok": "kayla_itsines"}
    sources: list[HandleSource] = field(default_factory=list)    # Where found

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "handles": self.handles,
            "sources": [{"page": s.page, "type": s.source_type} for s in self.sources],
        }


@dataclass
class ConfigResult:
    """Results for one config (category/sub/platform/region).

    Flat, self-documenting schema with full provenance:
      config → queryToUrl → influencers with source tracing.
    """
    config_key: str                                              # "FITNESS/Yoga/Instagram/US"
    config: dict = field(default_factory=dict)                   # Literal seed config
    query_to_url: dict[str, list[str]] = field(default_factory=dict)  # DDG query → URLs returned
    influencers: dict[str, InfluencerResult] = field(default_factory=dict)  # handle → InfluencerResult

    def to_dict(self) -> dict:
        return {
            "config": self.config,
            "queryToUrl": self.query_to_url,
            "influencers": {h: ir.to_dict() for h, ir in self.influencers.items()},
        }



# ── Per-Sub Results ──

@dataclass
class SubResult:
    """Results for one sub within a category/platform/region combo."""
    is_top_level: bool
    sources: list[SourceResult] = field(default_factory=list)
    all_influencers: list[Influencer] = field(default_factory=list)

    @staticmethod
    def _serialize_influencer(i: 'Influencer') -> dict:
        """Serialize an Influencer with full enrichment fields."""
        return {
            "name": i.name,
            "handles": {p.value: h for p, h in i.handles.items()},
            "most_seen_category": i.most_seen_category,
            "seen_in_categories": [cc.to_dict() for cc in i.seen_in_categories],
            "source_urls": sorted(i.source_urls),
            "citation_count": i.citation_count,
            "extraction_methods": sorted(i.extraction_methods),
        }

    def to_dict(self) -> dict:
        return {
            "is_top_level": self.is_top_level,
            "sources": [
                {
                    "url": s.url,
                    "query": s.query,
                    "md": s.md,
                    "influencers": [
                        self._serialize_influencer(i)
                        for i in s.influencers
                    ],
                }
                for s in self.sources
            ],
            "all_influencers": [
                self._serialize_influencer(i)
                for i in self.all_influencers
            ],
        }


# ── Top-Level Output ──

@dataclass
class RegionResult:
    """Top-level output object for one region."""
    region: str
    platforms: dict[str, dict[str, dict[str, SubResult]]]
    # platforms[platform_name][category_key][sub_name] = SubResult

    def _collect_source_extraction_methods(self) -> dict[str, list[str]]:
        """Build top-level url → [extraction_methods] map from all influencers."""
        url_methods: dict[str, set[str]] = {}
        for _plat, categories in self.platforms.items():
            for _cat, subs in categories.items():
                for _sub_name, sub_result in subs.items():
                    for inf in sub_result.all_influencers:
                        for url in inf.source_urls:
                            url_methods.setdefault(url, set()).update(
                                inf.extraction_methods
                            )
        return {
            url: sorted(methods)
            for url, methods in sorted(url_methods.items())
        }

    def to_dict(self) -> dict:
        return {
            "region": self.region,
            "source_extraction_methods": self._collect_source_extraction_methods(),
            "platforms": {
                plat: {
                    cat: {
                        sub_name: sub_result.to_dict()
                        for sub_name, sub_result in subs.items()
                    }
                    for cat, subs in categories.items()
                }
                for plat, categories in self.platforms.items()
            },
        }



# ── DDG Failure Tracking ──

@dataclass
class ErroredConfig:
    """A seed config whose DDG search failed above the failure threshold.

    Stored in errored_configs.json for retry in a subsequent run.
    """
    config_key: str                    # "FITNESS/HIIT/Instagram/US"
    category: str
    sub_name: str
    platform: str
    region: str
    failure_count: int
    queries_attempted: int
    failure_threshold_percentage: float
    reason: str

    def to_dict(self) -> dict:
        return {
            "config_key": self.config_key,
            "category": self.category,
            "sub_name": self.sub_name,
            "platform": self.platform,
            "region": self.region,
            "failure_count": self.failure_count,
            "queries_attempted": self.queries_attempted,
            "failure_threshold_percentage": self.failure_threshold_percentage,
            "reason": self.reason,
        }


# ── Pipeline Stats ──

@dataclass
class PipelineStats:
    """Accumulated metrics for a pipeline run."""
    urls_discovered: int = 0
    pages_crawled: int = 0
    pages_failed: int = 0
    pages_dropped: int = 0        # URLs that arun_many silently dropped (no result returned)
    pages_extracted: int = 0
    influencers_raw: int = 0
    influencers_deduped: int = 0
    handles_filled: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    # Handle retrieval tracking
    handles_in_source: int = 0    # Unique handles found in source HTML (ground truth)
    handles_retrieved: int = 0    # Handles from source that were successfully extracted
    # Failure / retry tracking
    search_retries: int = 0       # Total retry attempts across all search queries
    search_failures: int = 0      # Search queries that failed after all retries
    configs_aborted: int = 0      # Configs skipped due to DDG failure threshold
    crawl_retries: int = 0        # Total retry attempts across page crawls
    enrich_retries: int = 0       # Total retry attempts across handle enrichment
    enrich_failures: int = 0      # Handle lookups that failed after all retries
    llm_retries: int = 0          # Total retry attempts for LLM calls
    llm_failures: int = 0         # LLM calls that failed after all retries
    # Yield monitoring (regex extraction health)
    regex_handles_total: int = 0  # Total handles found by regex (across all pages)


@dataclass
class JobBreakdown:
    """Per-job influencer breakdown for the pipeline report.

    Each instance represents one pipeline job — the intersection of
    a category, sub-category, platform, and region.
    """
    category: str
    sub: str
    platform: str
    region: str
    influencers_found: int = 0
    handles_filled: int = 0
    handles_in_source: int = 0
    handles_retrieved: int = 0
    pages_crawled: int = 0


# ── Handle Counting ──

_HANDLE_PATTERNS = [
    re.compile(r'instagram\.com/([A-Za-z0-9_.]+)', re.IGNORECASE),
    re.compile(r'tiktok\.com/@([A-Za-z0-9_.]+)', re.IGNORECASE),
    re.compile(r'youtube\.com/@([A-Za-z0-9_.]+)', re.IGNORECASE),
]
_IGNORE_HANDLES = {"gymfluencers.agency", "gymfluencers"}


def count_handles_in_html(html: str) -> int:
    """Count unique social media handles in raw HTML.

    Scans for instagram.com/, tiktok.com/@, youtube.com/@ patterns.
    Returns count of unique (handle, platform) pairs found.
    """
    seen: set[str] = set()
    for pattern in _HANDLE_PATTERNS:
        for match in pattern.finditer(html):
            handle = match.group(1).lower().rstrip(".")
            if handle not in _IGNORE_HANDLES:
                seen.add(handle)
    return len(seen)


# ── Utilities ──

def iter_jobs(results: list[dict]) -> Iterator[dict]:
    """Flatten nested dict output into iterable job records."""
    for entry in results:
        for plat, categories in entry["platforms"].items():
            for cat, subs in categories.items():
                for sub_name, data in subs.items():
                    yield {
                        "region": entry["region"],
                        "platform": plat,
                        "category": cat,
                        "sub": sub_name,
                        **data,
                    }
