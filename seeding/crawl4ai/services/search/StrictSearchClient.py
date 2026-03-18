"""
StrictSearchClient — Serper-backed search client with full Google operator support.

Uses advanced Google dork operators validated by scripts/validate_serper.py:
  - intitle:    → page must be titled "Top Influencers" etc.
  - site:       → domain lock for known sources, reddit inclusion
  - OR + ()     → combine multiple intitle: terms, slug narrowing
  - plain text  → implicit AND with all operators

Query formula (validated by Serper tests):
  [site:X]  +  (intitle:influencer OR intitle:creator OR intitle:top OR site:reddit.com)
            +  (slug1 OR slug2)  +  search terms

For site-targeted queries, site:reddit.com is removed from the mandatory
clause since site: is already set to the known source domain.

NOTE: English-only language support.
"""

from __future__ import annotations

import logging
import os
import time

import requests

from config.seed_schema import SeedJob
from services.audit.AuditService import AuditLog
from services.search.SearchClient import (
    QueryType,
    RawSearchResult,
    SearchQuery,
)


logger = logging.getLogger(__name__)

SERPER_URL = "https://google.serper.dev/search"
SERPER_DELAY_SECONDS = 1.0

_MANDATORY_TERMS = ["influencer", "creator", "top"]


class StrictSearchClient:
    """Serper-backed client with full Google operator support.

    Generates 3 query types per SeedJob:
      1. PRIMARY OPEN (1): mandatory + slugs + search terms
      2. ALT OPEN (N):     mandatory + slugs + alt term
      3. SITE TARGETED (M): site:X + mandatory (no reddit) + slugs + terms
    """

    def __init__(
        self,
        audit: AuditLog,
        *,
        api_key: str,
        delay_seconds: float = SERPER_DELAY_SECONDS,
    ) -> None:
        self._audit = audit
        self._api_key = api_key
        self._delay = delay_seconds
        self._headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }

    # ── API ──

    def search(self, job: SeedJob) -> list[RawSearchResult]:
        """Build dork queries for job, execute via Serper, return raw results."""
        queries = self._build_queries(job)
        results: list[RawSearchResult] = []

        for i, sq in enumerate(queries, 1):
            print(f"  [{i}/{len(queries)}] ({sq.query_type}) {sq.query}")
            raw = self._execute(sq)
            results.extend(raw)
            self._audit.log(
                "search", "serper_query",
                query=sq.query, results=len(raw),
            )
            if i < len(queries):
                time.sleep(self._delay)

        return results

    def nr_query_template(self) -> str:
        """Google-optimized NR template — site: scoping works on Serper."""
        return '{name} {category} site:instagram.com OR site:tiktok.com OR site:youtube.com'

    # ── Internal ──

    def _build_queries(self, job: SeedJob) -> list[SearchQuery]:
        """Generate Google dork queries for all 3 types."""
        queries: list[SearchQuery] = []
        queries.extend(self._open_queries(job))
        queries.extend(self._site_targeted(job))
        return queries

    def _open_queries(self, job: SeedJob) -> list[SearchQuery]:
        """Open-web queries — primary + all alt terms share one formula."""
        mandatory = self._mandatory_clause()
        slugs = self._slug_clause(job.sub.strict_slugs)

        terms: list[tuple[str, str, QueryType]] = [
            (
                f'{job.sub.search_prompt} {job.platform.value} influencers list {job.year}',
                QueryType.PRIMARY_OPEN,
            ),
        ]
        for alt in job.sub.alt_search_terms:
            terms.append((
                f'{alt} {job.platform.value} influencers {job.region.label} {job.year}',
                QueryType.ALT_OPEN,
            ))

        return [
            SearchQuery(
                query=f'{mandatory} {slugs} "{job.sub.sub_name}" {suffix}'.strip(),
                query_type=qtype,
            )
            for suffix, qtype in terms
        ]

    def _site_targeted(self, job: SeedJob) -> list[SearchQuery]:
        """Site-locked queries — one per known source. No reddit in mandatory."""
        mandatory = self._mandatory_clause_no_reddit()
        slugs = self._slug_clause(job.sub.strict_slugs)
        return [
            SearchQuery(
                query=(
                    f'site:{source} {mandatory} {slugs} '
                    f'{job.sub.search_prompt} {job.platform.value} {job.year}'
                ).strip(),
                query_type=QueryType.SITE_TARGETED,
            )
            for source in job.sub.known_sources
        ]

    @staticmethod
    def _mandatory_clause() -> str:
        """(intitle:influencer OR intitle:creator OR intitle:top OR site:reddit.com)"""
        parts = [f"intitle:{t}" for t in _MANDATORY_TERMS] + ["site:reddit.com"]
        return "(" + " OR ".join(parts) + ")"

    @staticmethod
    def _mandatory_clause_no_reddit() -> str:
        """For site-targeted: no site:reddit.com since site: is already set."""
        return "(" + " OR ".join(f"intitle:{t}" for t in _MANDATORY_TERMS) + ")"

    @staticmethod
    def _slug_clause(slugs: list[str]) -> str:
        """(fitness OR workout OR gym) — empty string if no slugs."""
        if not slugs:
            return ""
        return "(" + " OR ".join(slugs) + ")"

    def _execute(self, sq: SearchQuery) -> list[RawSearchResult]:
        """Execute a single query via Serper API."""
        try:
            resp = requests.post(
                SERPER_URL,
                json={"q": sq.query, "num": 10},
                headers=self._headers,
                timeout=15,
            )
            resp.raise_for_status()
            organic = resp.json().get("organic", [])
            return [
                RawSearchResult(
                    url=r["link"],
                    title=r["title"],
                    query=sq.query,
                )
                for r in organic
            ]
        except requests.RequestException as e:
            logger.error("Serper API error for query %r: %s", sq.query, e)
            self._audit.log(
                "search", "serper_error",
                query=sq.query, error=str(e),
            )
            return []
