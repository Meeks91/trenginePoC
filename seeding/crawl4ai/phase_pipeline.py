"""PhasePipelineRunner — Runs all jobs in 4 sequential global phases.

Phase 1: SEARCH — All configs query DDG via base class shared loop
Phase 2: DEDUPE — Remove duplicate URLs, keep config tags
Phase 3: CRAWL  — Crawl each unique URL exactly once
Phase 4: EXTRACT + MERGE — Extract handles from pages, tag with categories

This is the high-throughput alternative to PerJobPipelineRunner which
processes each job independently (search→crawl→extract). The phase runner
avoids redundant crawls when multiple configs discover the same URL.

After all 4 phases, shared post-gather logic (name resolution, dedup,
canary validation, report, save) runs via BasePipelineRunner.run().

Services are dependency-injected and reused across phases.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from config.seed_schema import SeedJob
from config import AUDIT_DIR, CURRENT_YEAR
from config.schema import CategoryCitation, Influencer, PageResult, Platform

from services.audit.AuditService import AuditLog
from services.search.SearchService import SearchResults
from services.crawling.CrawlService import CrawlService
from services.extraction.HandleExtractionService import HandleExtractionService, _to_handles
from services.extraction.RegexHandleExtractorService import ExtractedHandle
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService
from services.influencerProvenance.CategoryProvenanceTaggerService import CategoryProvenanceTagger
from services.extraction.NameCleanerService import NameCleaner

if TYPE_CHECKING:
    from services.extraction.NameMentionTracker import NameMentionTracker

from base_pipeline import BasePipelineRunner, GatherResult


logger = logging.getLogger(__name__)


@dataclass
class TaggedURL:
    """A URL discovered by one or more configs, with provenance."""
    url: str
    source_query: str             # First query that found it
    config_keys: set[str] = field(default_factory=set)  # e.g. {"FITNESS/Yoga", "FOOD/Healthy"}
    category_keys: set[str] = field(default_factory=set)  # e.g. {"FITNESS", "FOOD"}
    sub_keys: set[str] = field(default_factory=set)       # e.g. {"Yoga", "Science-Based Training"}


class PhasePipelineRunner(BasePipelineRunner):
    """Runs pipeline in 4 global phases: Search → Dedupe → Crawl → Extract.

    Extends BasePipelineRunner — shared post-gather logic (name resolution,
    dedup, canary validation, report, save) is inherited via run().

    Search is handled by base class via _search_all_configs().
    This class implements _on_config_search_finished() to accumulate URLs
    into a shared url_bag for deduped crawling.
    """

    def _report_mode(self) -> str:
        return "phase-pipeline"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Accumulators populated by _on_config_search_finished
        self._url_bag: dict[str, TaggedURL] = {}
        self._all_direct_handles: list[tuple[ExtractedHandle, str, str]] = []

    # ── Template Method overrides ─────────────────────────────────────────

    async def _search_and_extract_influencers(
        self, jobs: list[SeedJob],
    ) -> GatherResult:
        """Phase-based strategy: search all → dedupe → crawl once → extract+merge."""
        # Reset accumulators
        self._url_bag.clear()
        self._all_direct_handles.clear()

        # Phase 1: Search all configs (base class owns the loop + circuit breaker)
        logger.info("="*70)
        logger.info("  PHASE 1: SEARCH (%d configs)", len(jobs))
        logger.info("="*70)

        outcomes = await self._search_all_configs(jobs)

        if not self._url_bag and not self._all_direct_handles:
            logger.warning("  No URLs or handles found across all configs")
            return GatherResult(job_outcomes=outcomes)

        # Phase 2: Dedupe + sort URLs
        unique_urls = self.dedupe_urls(self._url_bag)

        # Phase 3: Crawl unique URLs
        pages, page_map = await self._crawl_all(unique_urls)

        # Phase 4: Extract + build influencers list
        influencers, name_tracker = await self._extract_and_build_entries(
            pages, page_map, jobs, self._all_direct_handles,
        )

        return GatherResult(
            influencers=influencers,
            name_tracker=name_tracker,
            job_outcomes=outcomes,
        )

    async def _on_config_search_finished(
        self,
        job: SeedJob,
        search_results: SearchResults,
    ) -> None:
        """Accumulate URLs into shared url_bag for later deduped crawling."""
        config_key = (
            f"{job.category_key}/{job.sub.sub_name}"
            f"/{job.platform.value}/{job.region.code.value}"
        )

        # Tag URLs with this config
        for url, query in search_results.url_query_pairs:
            if url not in self._url_bag:
                self._url_bag[url] = TaggedURL(
                    url=url,
                    source_query=query,
                    config_keys={config_key},
                    category_keys={job.category_key},
                    sub_keys={job.sub.sub_name},
                )
            else:
                self._url_bag[url].config_keys.add(config_key)
                self._url_bag[url].category_keys.add(job.category_key)
                self._url_bag[url].sub_keys.add(job.sub.sub_name)

        # Tag direct handles
        for handle in search_results.direct_handles:
            self._all_direct_handles.append((handle, job.category_key, job.sub.sub_name))

    # ── Phase 2: Dedupe URLs (already deduped by dict key) ─────────────

    @staticmethod
    def dedupe_urls(url_bag: dict[str, TaggedURL]) -> list[TaggedURL]:
        """Return unique URLs sorted by number of configs (most-wanted first).

        The URL bag is already deduplicated by dict key. This method just
        sorts for priority: URLs wanted by more configs get crawled first.
        """
        sorted_urls = sorted(
            url_bag.values(),
            key=lambda t: len(t.config_keys),
            reverse=True,
        )

        multi_config = sum(1 for t in sorted_urls if len(t.config_keys) > 1)
        logger.info("  Phase 2: %d unique URLs (%d shared across configs)", len(sorted_urls), multi_config)

        return sorted_urls

    # ── Phase 3: Crawl Once ─────────────────────────────────────────────

    async def _crawl_all(self, urls: list[TaggedURL]) -> tuple[list[PageResult], dict[str, tuple[PageResult, TaggedURL]]]:
        """Crawl each unique URL exactly once.

        Returns: (pages, dict mapping URL → (PageResult, TaggedURL)) for extraction.
        """
        logger.info("="*70)
        logger.info("  PHASE 3: CRAWL (%d unique URLs)", len(urls))
        logger.info("="*70)

        audit = AuditLog(AUDIT_DIR, "phase_crawl")
        crawl_svc = CrawlService(audit)

        url_query_pairs = [(t.url, t.source_query) for t in urls]

        if self.no_bfs:
            pages = await crawl_svc.crawl_urls(url_query_pairs)
        else:
            pages = await crawl_svc.crawl_urls_bfs(url_query_pairs)

        self._stats.record_crawl(pages)

        # Build URL → (page, tagged_url) lookup
        url_to_tagged = {t.url: t for t in urls}
        page_map = {}
        for page in pages:
            if page.success and page.url in url_to_tagged:
                page_map[page.url] = (page, url_to_tagged[page.url])

        logger.info("  Phase 3 complete: %d pages crawled successfully", len(page_map))
        return pages, page_map

    # ── Phase 4: Extract + Build entries ─────────────────────────────────

    async def _extract_and_build_entries(
        self,
        pages: list[PageResult],
        page_map: dict[str, tuple[PageResult, TaggedURL]],
        jobs: list[SeedJob],
        direct_handles: list[tuple[ExtractedHandle, str, str]],
    ) -> tuple[list[Influencer], NameMentionTracker | None]:
        """Extract handles from all pages, tag with categories.

        Returns (influencers, name_tracker).
        """

        logger.info("="*70)
        logger.info("  PHASE 4: EXTRACT + MERGE")
        logger.info("="*70)

        audit = AuditLog(AUDIT_DIR, "phase_extract")
        handle_svc = HandleExtractionService(audit)

        # Use primary platform from first job for extraction context
        primary_platform = jobs[0].platform if jobs else Platform.Instagram
        primary_category = jobs[0].category_key if jobs else "UNKNOWN"
        primary_sub = jobs[0].sub.sub_name if jobs else "Unknown"
        primary_region = jobs[0].region.label if jobs else "US"

        # Convert direct handles from phase 1
        direct_handle_objects = [h for h, _cat, _sub in direct_handles]

        extract_result = await handle_svc.extract_all_handles(
            pages,
            platform=primary_platform.value,
            category_key=primary_category,
            sub_name=primary_sub,
            region=primary_region,
            year=CURRENT_YEAR,
            direct_handles=direct_handle_objects,
            sample_n=self.sample_n,
        )
        self._stats.record_extraction(extract_result)

        # Enrich — cross-platform backfill
        if not self.no_cross_platform_lookup:
            resolver = CrossPlatformHandleResolverService(
                audit,
                search_client=self._build_search_client(audit),
            )
            extract_result.all_merged = resolver.resolve(extract_result.all_merged)
        unique = extract_result.all_merged
        self._stats.record_enrichment(
            unique_count=len(unique),
            handles_filled=sum(1 for inf in unique if inf.handles),
            retries=0,
            failures=0,
        )

        # Tag each influencer with categories from the configs that discovered its pages
        sub_to_category = SeedJob.build_sub_to_category(jobs=jobs)
        CategoryProvenanceTagger.tag_from_page_map(
            influencers=unique,
            page_map=page_map,
            sub_to_category=sub_to_category,
            fallback_category=primary_category,
            fallback_sub=primary_sub,
        )
        all_influencers: list[Influencer] = list(unique)

        # Add direct handles with their categories
        for handle, category, sub_name in direct_handles:
            inf = Influencer(
                name=NameCleaner.clean_name(handle.name) or "",
                handles=_to_handles(handle.handle, handle.platform),
                most_seen_category=sub_name,
                seen_in_categories=[
                    CategoryCitation(category=category, sub=sub_name, citations=1),
                ],
            )
            all_influencers.append(inf)

        logger.info("  Phase 4 complete: %d handles → %d entries", len(unique), len(all_influencers))

        return all_influencers, extract_result.name_tracker
