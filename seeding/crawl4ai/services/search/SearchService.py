"""
SearchService — Orchestrates search, deduplicates URLs, filters ads and platform handles.

Accepts any SearchClient implementation via dependency injection.
Applies filtering pipeline on top of raw search results:
  1. Ad filtering
  2. Platform URL handle extraction (DDG dorking)
  3. (Plan 2) Mandatory word filtering
  4. (Plan 2) Slug matching

DDG Dorking: When a search client returns platform URLs (instagram.com/handle,
tiktok.com/@handle, etc.), handles are extracted immediately from the
search result — no crawling needed. These "direct handles" are returned
alongside the URL list.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from urllib.parse import urlparse

from config import MAX_URLS_PER_JOB
from config.seed_schema import SeedJob
from services.audit.AuditService import AuditLog
from services.search.SearchClient import RawSearchResult, SearchClient
from services.extraction.RegexHandleExtractor import (
    extract_handles_from_url,
    ExtractedHandle,
)


logger = logging.getLogger(__name__)


AD_DOMAINS = {
    "bing.com", "microsoft.com", "googleadservices.com",
    "scrumball.com",
    "metricsmule.com",
    "linkedin.com",
}

_PLATFORM_DOMAINS = {
    "instagram.com", "instagr.am", "tiktok.com", "youtube.com",
    "twitter.com", "x.com",
}


@dataclass
class SearchResults:
    """Results from search discovery."""
    url_query_pairs: list[tuple[str, str]] = field(default_factory=list)
    direct_handles: list[ExtractedHandle] = field(default_factory=list)
    failure_count: int = 0
    queries_attempted: int = 0

    @property
    def failure_threshold_percentage(self) -> float:
        """Fraction of queries that permanently failed."""
        if self.queries_attempted == 0:
            return 0.0
        return self.failure_count / self.queries_attempted


class SearchService:
    """Discover URLs via any SearchClient — applies uniform filtering pipeline."""

    def __init__(
        self,
        audit: AuditLog,
        client: SearchClient,
    ) -> None:
        self._audit = audit
        self._client = client

    # ── API ──

    def discover_urls(self, job: SeedJob) -> SearchResults:
        """Run search via injected client, then filter results.

        Returns SearchResults with:
          - url_query_pairs: listicle pages to crawl
          - direct_handles: handles extracted directly from result URLs
        """
        raw_results = self._client.search(job)

        discovered: list[tuple[str, str]] = []
        direct_handles: list[ExtractedHandle] = []
        seen_urls: set[str] = set()
        seen_handles: set[str] = set()

        for r in raw_results:
            if r.url in seen_urls:
                continue
            if self._is_ad(r.url):
                self._audit.log_url_rejected(r.url, reason="ad_domain")
                continue

            seen_urls.add(r.url)

            if self._is_platform_url(r.url):
                handle = extract_handles_from_url(r.url)
                if handle and handle.handle.lower() not in seen_handles:
                    seen_handles.add(handle.handle.lower())
                    direct_handles.append(handle)
                    self._audit.log(
                        "search", "direct_handle",
                        handle=handle.handle, platform=handle.platform, url=r.url,
                    )
                    print(f"      ⚡ Direct handle: @{handle.handle} ({handle.platform})")
                continue

            discovered.append((r.url, r.query))
            self._audit.log_url_accepted(r.url)
            print(f"      + {r.title[:60]}")
            print(f"        {r.url}")

        if len(discovered) > MAX_URLS_PER_JOB:
            discovered = discovered[:MAX_URLS_PER_JOB]

        print(f"\n  Discovered {len(discovered)} URLs")
        if direct_handles:
            print(f"  ⚡ {len(direct_handles)} handles extracted directly from URLs")

        return SearchResults(
            url_query_pairs=discovered,
            direct_handles=direct_handles,
        )

    # ── Internal ──

    @staticmethod
    def _is_ad(url: str) -> bool:
        """Check if URL is an ad/tracking redirect."""
        try:
            domain = urlparse(url).netloc.lower()
            return any(ad in domain for ad in AD_DOMAINS)
        except Exception:
            return False

    @staticmethod
    def _is_platform_url(url: str) -> bool:
        """Check if URL is a social media platform URL."""
        try:
            domain = urlparse(url).netloc.lower().removeprefix("www.")
            return any(pd in domain for pd in _PLATFORM_DOMAINS)
        except Exception:
            return False
