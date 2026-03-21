"""PerJobPipelineRunner — Per-job orchestration: Search → Crawl → Extract → Enrich per job.

After all jobs complete, shared post-gather logic (name resolution, dedup,
canary validation, report, save) runs via BasePipelineRunner.run().

Also supports a single-URL override mode that skips Search entirely.
"""

from __future__ import annotations

import logging
from typing import Any

from config.seed_schema import SeedJob

from services.audit.AuditService import AuditLog
from config import (
    AUDIT_DIR, CURRENT_YEAR, LLM_PROVIDER, REPORTS_DIR,
)
from config.schema import SubResult, RegionResult, Influencer, Platform

from services.influencerProvenance.CategoryProvenanceTaggerService import CategoryProvenanceTagger
from services.search.SearchService import SearchResults
from services.crawling.CrawlService import CrawlService
from services.extraction.HandleExtractionService import HandleExtractionService
from services.extraction.NameMentionTracker import NameMentionTracker
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService
from services.reporting.PipelineReporter import PipelineReporter

from base_pipeline import BasePipelineRunner, GatherResult


logger = logging.getLogger(__name__)


class PerJobPipelineRunner(BasePipelineRunner):
    """Per-job pipeline: runs Search→Crawl→Extract→Enrich independently per job.

    Extends BasePipelineRunner — shared post-gather logic (name resolution,
    dedup, canary validation, report, save) is inherited via run().

    Search is handled by base class via _search_all_configs().
    This class implements _on_config_search_finished() to crawl, extract,
    and enrich immediately after each config's search completes.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Cross-job accumulator for the per-job loop
        self._all_influencers: list[Influencer] = []
        # Cross-job name tracker for deferred resolution
        self._global_name_tracker = NameMentionTracker()

    # ── Template Method overrides ─────────────────────────────────────────

    async def _search_and_extract_influencers(
        self, jobs: list[SeedJob],
    ) -> GatherResult:
        """Per-job strategy: base runs search, we crawl+extract per job."""
        self._all_influencers.clear()
        self._global_name_tracker = NameMentionTracker()

        # Base class owns search iteration + circuit breaker
        outcomes = await self._search_all_configs(jobs)

        return GatherResult(
            influencers=list(self._all_influencers),
            name_tracker=self._global_name_tracker,
            job_outcomes=outcomes,
        )

    async def _on_config_search_finished(
        self,
        job: SeedJob,
        search_results: SearchResults,
    ) -> None:
        """Crawl → extract → enrich for a single successful config."""
        job_key = f"{job.category_key}_{job.sub.sub_name}_{job.platform.value}_{job.region.code.value}"
        job_key = job_key.replace("/", "-").replace(" ", "_")

        url_query_pairs = search_results.url_query_pairs
        direct_handles = search_results.direct_handles

        self._assembler.save_search_urls(job_key, url_query_pairs)

        if not url_query_pairs and not direct_handles:
            logger.warning("  No URLs found")
            return

        # Crawl
        audit = AuditLog(AUDIT_DIR, job_key)
        crawl_svc = CrawlService(audit)
        if self.no_bfs:
            pages = await crawl_svc.crawl_urls(url_query_pairs)
        else:
            pages = await crawl_svc.crawl_urls_bfs(url_query_pairs)
        self._stats.record_crawl(
            pages,
            dropped=crawl_svc.dropped_count,
            retries=crawl_svc.retry_count,
        )

        # Extract handles
        handle_svc = HandleExtractionService(audit)
        extract_result = await handle_svc.extract_all_handles(
            pages,
            platform=job.platform.value,
            category_key=job.category_key,
            sub_name=job.sub.sub_name,
            region=job.region.label,
            year=CURRENT_YEAR,
            direct_handles=direct_handles,
            sample_n=self.sample_n,
        )
        self._stats.record_extraction(extract_result)

        # Merge per-job name tracker into global tracker
        if extract_result.name_tracker is not None:
            self._global_name_tracker.merge(extract_result.name_tracker)

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

        # Build SourceResult list
        _sources = self._assembler.build_source_results(
            pages, extract_result.llm_handles,
        )

        logger.info("  Audit log: %s", audit.path)

        # Accumulate for global dedup
        CategoryProvenanceTagger.tag_from_job(
            influencers=unique,
            category_key=job.category_key,
            sub_name=job.sub.sub_name,
        )
        for inf in unique:
            self._all_influencers.append(inf)

    # ── run_jobs (legacy wrapper) ────────────────────────────────────────

    async def run_jobs(self, jobs: list[SeedJob]) -> list[RegionResult]:
        """Run multiple jobs, build nested RegionResult output, then finalize.

        This is the per-job entry point called by cli.py (default mode).
        It delegates orchestration to _search_and_extract_influencers() and
        finalization to the base template, but also builds the nested
        RegionResult structure that is unique to per-job mode.
        """
        # Run the template (search+extract → name res → dedup → canary → report → save)
        _seeds = await self.run(jobs)

        # Build nested RegionResult output from the SubResults created during
        # _on_config_search_finished() — this structure is per-job mode only
        regions: dict[str, dict] = {}
        for job in jobs:
            region_code = job.region.code.value
            plat = job.platform.value
            cat = job.category_key
            sub = job.sub.sub_name

            regions.setdefault(region_code, {}) \
                   .setdefault(plat, {}) \
                   .setdefault(cat, {})[sub] = SubResult(
                       is_top_level=job.sub.is_top_level,
                   )

        output = [
            RegionResult(region=region, platforms=platforms)
            for region, platforms in regions.items()
        ]

        return output

    # ── Single-URL override mode ─────────────────────────────────────────

    async def run_single_url(
        self,
        url: str,
        *,
        platform: str = "Instagram",
        category_key: str = "UNKNOWN",
        sub_name: str = "Unknown",
        region: str = "US",
    ) -> SubResult:
        """Run the pipeline against a single URL, skipping Search entirely.

        Useful for debugging, testing extraction on a specific page, or
        one-off runs. Does not require a SeedJob — uses sensible defaults.
        """
        job_key = f"single_url_{platform}_{region}"
        logger.info("="*70)
        logger.info("  SINGLE URL: %s", url)
        logger.info("  Context: %s / %s / %s / %s", platform, category_key, sub_name, region)
        logger.info("="*70)

        audit = AuditLog(AUDIT_DIR, job_key)

        # Skip Search — go straight to Crawl
        logger.info("  --- Search: SKIPPED (single URL override) ---")
        url_query_pairs = [(url, "manual_override")]

        # Crawl
        crawl_svc = CrawlService(audit)
        if self.no_bfs:
            pages = await crawl_svc.crawl_urls(url_query_pairs)
        else:
            pages = await crawl_svc.crawl_urls_bfs(url_query_pairs)
        self._stats.record_crawl(pages)

        # Extract handles
        handle_svc = HandleExtractionService(audit)
        extract_result = await handle_svc.extract_all_handles(
            pages,
            platform=platform,
            category_key=category_key,
            sub_name=sub_name,
            region=region,
            year=CURRENT_YEAR,
            direct_handles=[],
            sample_n=self.sample_n,
        )
        self._stats.record_extraction(extract_result)

        # Deferred Name Resolution (single-URL mode)
        resolved_influencers: list[Influencer] = []
        name_records = self._run_deferred_name_resolution(
            tracker=extract_result.name_tracker,
            audit=audit,
            sub_name=sub_name,
            platform=Platform(platform),
            influencers=resolved_influencers,
            sub_to_category={sub_name: category_key},
        )
        extract_result.all_merged.extend(resolved_influencers)

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

        # Build SourceResult list
        sources = self._assembler.build_source_results(
            pages, extract_result.llm_handles,
        )

        # Generate Report + Save
        yield_warnings = self._stats.check_yield_warnings()
        run_id = self._assembler.generate_run_id(region)
        run_dir = REPORTS_DIR / run_id

        reporter = PipelineReporter()
        reporter.generate(
            run_dir=run_dir,
            stats=self.stats,
            validation_results={},
            model=LLM_PROVIDER,
            mode="single-url",
            influencers=unique,
            name_mentions=name_records,
            warnings=yield_warnings,
        )

        logger.info("  Audit log: %s", audit.path)
        logger.info("  Result: %d unique influencers", len(unique))

        return SubResult(
            is_top_level=True,
            sources=sources,
            all_influencers=unique,
        )


# Backward compatibility alias
PipelineRunner = PerJobPipelineRunner
