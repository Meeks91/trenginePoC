"""
SearchService — Executes search queries via multi-engine rotation, deduplicates URLs, filters ads.
Includes exponential backoff for rate limiting.

DDG Dorking: When DDG returns platform URLs (instagram.com/handle,
tiktok.com/@handle, etc.), handles are extracted immediately from the
search result — no crawling needed. These "direct handles" are returned
alongside the URL list.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

from ddgs import DDGS

from services.audit.AuditService import AuditLog

logger = logging.getLogger(__name__)
from config import (
    SEARCH_DELAY_SECONDS, MAX_SEARCH_RESULTS, MAX_URLS_PER_JOB,
    SEARCH_BACKEND, SEARCH_REGION,
    MAX_RETRIES, BACKOFF_BASE_SECONDS, BACKOFF_MAX_SECONDS,
)
from config.seed_schema import Difficulty
from services.search.QueryBuilder import QueryBuilder, QueryType, SearchQuery
from services.search.SearchCache import SearchCache
from services.extraction.RegexHandleExtractor import (
    extract_handles_from_url,
    ExtractedHandle,
)


AD_DOMAINS = {
    "bing.com", "microsoft.com", "googleadservices.com",
    "scrumball.com",      # SEO-generated junk rankings with random accounts
    "metricsmule.com",    # Fabricated influencer names
    "linkedin.com",       # LinkedIn profiles don't yield social handles
}

# Platform domains — if DDG returns these, extract handle directly
_PLATFORM_DOMAINS = {"instagram.com", "instagr.am", "tiktok.com", "youtube.com",
                     "twitter.com", "x.com"}


@dataclass
class SearchResults:
    """Results from search discovery."""
    url_query_pairs: list[tuple[str, str]] = field(default_factory=list)
    direct_handles: list[ExtractedHandle] = field(default_factory=list)
    failure_count: int = 0           # Queries that failed after all retries
    queries_attempted: int = 0       # Total leaf queries executed

    @property
    def failure_threshold_percentage(self) -> float:
        """Fraction of queries that permanently failed."""
        if self.queries_attempted == 0:
            return 0.0
        return self.failure_count / self.queries_attempted


class SearchService:
    """Discover URLs via multi-engine search (DDG, Brave, Bing, Google, etc.)."""

    def __init__(
        self,
        audit: AuditLog,
        cache: SearchCache | None = None,
        *,
        ddgs: DDGS | None = None,
        delay_seconds: float = SEARCH_DELAY_SECONDS,
    ):
        self._audit = audit
        self._cache = cache
        self._ddgs = ddgs or DDGS()
        self._delay = delay_seconds

    def discover_urls(
        self,
        sub_name: str,
        platform: str,
        region: str,
        year: str,
        search_prompt: str,
        alt_search_terms: list[str],
        known_sources: list[str],
        difficulty: Difficulty,
        inurl_slugs: list[str],
    ) -> SearchResults:
        """Run all search queries. Returns SearchResults with:
        - url_query_pairs: listicle pages to crawl
        - direct_handles: handles extracted directly from DDG result URLs
        """
        builder = QueryBuilder(
            sub_name=sub_name,
            platform=platform,
            region=region,
            year=year,
            search_prompt=search_prompt,
            alt_search_terms=alt_search_terms,
            known_sources=known_sources,
            difficulty=difficulty,
            inurl_slugs=inurl_slugs,
        )

        queries = builder.build_all()
        discovered: list[tuple[str, str]] = []
        direct_handles: list[ExtractedHandle] = []
        seen_urls: set[str] = set()
        seen_handles: set[str] = set()
        retries = 0
        failures = 0

        for i, sq in enumerate(queries, 1):
            print(f"  [{i}/{len(queries)}] ({sq.query_type}) {sq.query}")
            results, query_retries, query_failed = self._query_with_retry(sq)
            retries += query_retries
            if query_failed:
                failures += 1

            result_count = 0
            for r in results:
                url = r["href"]
                if url in seen_urls:
                    continue
                if self._is_ad(url):
                    self._audit.log_url_rejected(url, reason="ad_domain")
                    continue

                seen_urls.add(url)

                # DDG Dorking: if URL is a platform profile, extract handle directly
                if self._is_platform_url(url):
                    handle = extract_handles_from_url(url)
                    if handle and handle.handle.lower() not in seen_handles:
                        seen_handles.add(handle.handle.lower())
                        direct_handles.append(handle)
                        self._audit.log("search", "direct_handle",
                                       handle=handle.handle, platform=handle.platform, url=url)
                        print(f"      ⚡ Direct handle: @{handle.handle} ({handle.platform})")
                        continue  # Don't crawl — we already got the handle

                discovered.append((url, sq.query))
                self._audit.log_url_accepted(url)
                result_count += 1
                print(f"      + {r['title'][:60]}")
                print(f"        {url}")

            self._audit.log_search_query(sq.query, result_count)
            time.sleep(self._delay)

        if len(discovered) > MAX_URLS_PER_JOB:
            discovered = discovered[:MAX_URLS_PER_JOB]

        print(f"\n  Discovered {len(discovered)} URLs from {len(queries)} queries")
        if direct_handles:
            print(f"  ⚡ {len(direct_handles)} handles extracted directly from DDG URLs")
        if retries > 0:
            print(f"  ⚠ {retries} retries, {failures} permanent failures")
        return SearchResults(
            url_query_pairs=discovered,
            direct_handles=direct_handles,
            failure_count=failures,
            queries_attempted=len(queries),
        )

    def _query_with_retry(self, sq: SearchQuery) -> tuple[list[dict], int, bool]:
        """Execute a DDG query with cache check + exponential backoff.

        Returns (results, retry_count, permanently_failed).
        """
        max_results = MAX_SEARCH_RESULTS if sq.query_type == QueryType.SITE_TARGETED else 5

        # Check cache first
        if self._cache:
            cached = self._cache.get(sq.query)
            if cached is not None:
                self._audit.log("search", "cache_hit", query=sq.query, results=len(cached))
                return cached, 0, False

        query_retries = 0
        for attempt in range(MAX_RETRIES + 1):
            try:
                results = list(self._ddgs.text(
                    sq.query, max_results=max_results,
                    backend=SEARCH_BACKEND, region=SEARCH_REGION,
                ))
                # Store in cache
                if self._cache:
                    self._cache.put(sq.query, results)
                return results, query_retries, False
            except Exception as e:
                if attempt < MAX_RETRIES:
                    delay = min(
                        BACKOFF_BASE_SECONDS * (2 ** attempt) + random.uniform(0, 1),
                        BACKOFF_MAX_SECONDS,
                    )
                    query_retries += 1
                    logger.warning("Search error (attempt %d/%d): %s — backing off %.1fs",
                                   attempt + 1, MAX_RETRIES + 1, e, delay)
                    self._audit.log("search", "retry", query=sq.query, attempt=attempt + 1, error=str(e))
                    time.sleep(delay)
                else:
                    logger.exception("Search permanently failed for query: %s", sq.query)
                    self._audit.log("search", "permanent_failure", query=sq.query, error=str(e))
                    return [], query_retries, True
        return [], 0, True  # unreachable, satisfies mypy

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

