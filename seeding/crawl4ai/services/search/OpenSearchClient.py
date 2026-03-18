"""
OpenSearchClient — DDG-backed search client.

Generates simplified queries (no inurl:, no OR chains, site: only for known sources).
Returns raw results for SearchService to filter.

This client is free and fast — suitable for testing and development.
For production with strict dorking, use StrictSearchClient.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass

from ddgs import DDGS

from config import (
    SEARCH_DELAY_SECONDS,
    MAX_SEARCH_RESULTS,
    SEARCH_BACKEND,
    SEARCH_REGION,
    MAX_RETRIES,
    BACKOFF_BASE_SECONDS,
    BACKOFF_MAX_SECONDS,
)
from config.seed_schema import SeedJob
from services.audit.AuditService import AuditLog
from services.search.SearchCache import SearchCache
from services.search.SearchClient import (
    QueryType,
    RawSearchResult,
    SearchClient,
    SearchQuery,
)


logger = logging.getLogger(__name__)


class OpenSearchClient:
    """DDG-backed search client. No inurl:, site: only for known sources.

    Query types (3):
      1. PRIMARY OPEN:  "{sub_name}" {search_prompt} {platform} influencers list {year}
      2. ALT OPEN:      "{sub_name}" {alt_term} {platform} influencers {region} {year}
      3. SITE TARGETED: site:{source} {search_prompt} {platform} {year}

    No dorking operators beyond site: — DDG handles them unreliably.
    """

    def __init__(
        self,
        audit: AuditLog,
        cache: SearchCache | None = None,
        *,
        ddgs: DDGS | None = None,
        delay_seconds: float = SEARCH_DELAY_SECONDS,
    ) -> None:
        self._audit = audit
        self._cache = cache
        self._ddgs = ddgs or DDGS()
        self._delay = delay_seconds

    # ── API ──

    def search(self, job: SeedJob) -> list[RawSearchResult]:
        """Build queries for job, execute them, return raw results."""
        queries = self._build_queries(job)
        results: list[RawSearchResult] = []

        for i, sq in enumerate(queries, 1):
            print(f"  [{i}/{len(queries)}] ({sq.query_type}) {sq.query}")
            raw, _retries, _failed = self._execute_with_retry(sq)
            results.extend(raw)
            time.sleep(self._delay)

        return results

    def nr_query_template(self) -> str:
        """DDG-optimized NR template — no site: scoping (DDG hates it)."""
        return '{name} Instagram YouTube TikTok'

    # ── Internal ──

    def _build_queries(self, job: SeedJob) -> list[SearchQuery]:
        """Generate DDG-safe queries — no inurl:, no OR chains."""
        queries: list[SearchQuery] = []
        queries.extend(self._open_queries(job))
        queries.extend(self._site_targeted(job))
        return queries

    def _open_queries(self, job: SeedJob) -> list[SearchQuery]:
        """Open-web queries — primary + all alt terms share one formula."""
        terms: list[tuple[str, QueryType]] = [
            (
                f'{job.sub.search_prompt} {job.platform.value} influencers list {job.year}',
                QueryType.PRIMARY_OPEN,
            ),
        ]
        for alt in job.sub.alt_search_terms:
            terms.append((
                f'{alt} {job.platform.value} influencers {job.region.search_label} {job.year}',
                QueryType.ALT_OPEN,
            ))

        return [
            SearchQuery(
                query=f'"{job.sub.sub_name}" {suffix}'.strip(),
                query_type=qtype,
            )
            for suffix, qtype in terms
        ]

    def _site_targeted(self, job: SeedJob) -> list[SearchQuery]:
        """site:{source} queries — one per known source."""
        return [
            SearchQuery(
                query=(
                    f'site:{source} {job.sub.search_prompt} '
                    f'{job.platform.value} {job.year}'
                ),
                query_type=QueryType.SITE_TARGETED,
            )
            for source in job.sub.known_sources
        ]

    def _execute_with_retry(
        self, sq: SearchQuery,
    ) -> tuple[list[RawSearchResult], int, bool]:
        """Execute a DDG query with cache check + exponential backoff.

        Returns (results, retry_count, permanently_failed).
        """
        max_results = (
            MAX_SEARCH_RESULTS
            if sq.query_type == QueryType.SITE_TARGETED
            else 5
        )

        if self._cache:
            cached = self._cache.get(sq.query)
            if cached is not None:
                self._audit.log("search", "cache_hit", query=sq.query, results=len(cached))
                return self._to_raw_results(cached, sq.query), 0, False

        query_retries = 0
        for attempt in range(MAX_RETRIES + 1):
            try:
                ddg_results = list(self._ddgs.text(
                    sq.query,
                    max_results=max_results,
                    backend=SEARCH_BACKEND,
                    region=SEARCH_REGION,
                ))
                if self._cache:
                    self._cache.put(sq.query, ddg_results)
                return self._to_raw_results(ddg_results, sq.query), query_retries, False
            except Exception as e:
                if attempt < MAX_RETRIES:
                    delay = min(
                        BACKOFF_BASE_SECONDS * (2 ** attempt) + random.uniform(0, 1),
                        BACKOFF_MAX_SECONDS,
                    )
                    query_retries += 1
                    logger.warning(
                        "Search error (attempt %d/%d): %s — backing off %.1fs",
                        attempt + 1, MAX_RETRIES + 1, e, delay,
                    )
                    self._audit.log(
                        "search", "retry",
                        query=sq.query, attempt=attempt + 1, error=str(e),
                    )
                    time.sleep(delay)
                else:
                    logger.exception("Search permanently failed for query: %s", sq.query)
                    self._audit.log(
                        "search", "permanent_failure",
                        query=sq.query, error=str(e),
                    )
                    return [], query_retries, True

        return [], 0, True

    @staticmethod
    def _to_raw_results(
        ddg_results: list[dict[str, str]],
        query: str,
    ) -> list[RawSearchResult]:
        """Convert DDG dict results to RawSearchResult."""
        return [
            RawSearchResult(
                url=r.get("href", ""),
                title=r.get("title", ""),
                query=query,
            )
            for r in ddg_results
        ]
