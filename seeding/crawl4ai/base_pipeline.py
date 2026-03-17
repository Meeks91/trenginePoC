"""BasePipelineRunner — Shared base for all pipeline orchestrators.

Implements the Template Method pattern:
  1. _search_all_configs(jobs) — shared search loop with circuit breaker
  2. _on_config_search_finished() — ABSTRACT, subclass-specific post-search
  3. _search_and_extract_influencers(jobs) — ABSTRACT, subclass-specific gather
  4. Deferred name resolution
  5. Global dedup (InfluencerMerger.to_seeds)
  6. Canary validation (IngestionValidator)
  7. Report generation (PipelineReporter)
  8. Save seeds + errored configs (ResultAssembler)

Subclasses implement steps 2–3. Everything else is shared.
"""

from __future__ import annotations

import abc
import logging
from dataclasses import dataclass, field
from enum import Enum

from config.seed_schema import SeedJob
from config import (
    AUDIT_DIR, CURRENT_YEAR, LLM_PROVIDER, REPORTS_DIR, RESULTS_DIR,
    NAME_RESOLUTION_ENABLED, NAME_RESOLUTION_MIN_MENTIONS, NAME_RESOLUTION_MAX_PER_SUB,
    DDG_FAILURE_THRESHOLD_PCT, DDG_FAILURE_MIN_QUERIES, DDG_KILL_AFTER_N,
)
from config.schema import (
    Influencer, SeedInfluencer, NameMentionRecord, PipelineStats, Platform,
    ErroredConfig,
)

from services.audit.AuditService import AuditLog
from services.search.SearchService import SearchService, SearchResults
from services.search.SearchCache import SearchCache
from services.search.OpenSearchClient import OpenSearchClient
from services.search.StrictSearchClient import StrictSearchClient
from services.extraction.NameMentionTracker import NameMentionTracker
from services.enrichment.NameToHandleService import NameToHandleService
from services.enrichment.InfluencerMerger import InfluencerMerger
from services.validation.IngestionValidator import IngestionValidator, ValidationResult
from services.reporting.PipelineReporter import PipelineReporter
from services.reporting.StatsCollector import StatsCollector
from services.reporting.ResultAssembler import ResultAssembler


logger = logging.getLogger(__name__)


@dataclass
class JobOutcome:
    """Per-config search outcome — bundles job, results, and error status."""
    job: SeedJob
    search_results: SearchResults | None  # None if killed before search ran
    errored: ErroredConfig | None = None  # None = success


@dataclass
class GatherResult:
    """Output of _search_and_extract_influencers() — the convergence point.

    Both pipeline strategies (per-job and phase) produce this same shape
    after their search+crawl+extract phase completes.
    """
    influencers: list[Influencer] = field(default_factory=list)
    name_tracker: NameMentionTracker | None = None
    job_outcomes: list[JobOutcome] = field(default_factory=list)


class SearchClientType(str, Enum):
    """Which search backend to use."""
    OPEN = "open"      # DDG (free)
    STRICT = "strict"  # Serper (paid)


class BasePipelineRunner(abc.ABC):
    """Shared base for PipelineRunner and PhasePipelineRunner.

    Subclasses implement _search_and_extract_influencers() with their
    own orchestration strategy. Everything after (name resolution,
    dedup, canary validation, reporting, saving) is inherited.
    """

    def __init__(
        self,
        *,
        sample_n: int | None = None,
        no_bfs: bool = False,
        no_cross_platform_lookup: bool = False,
        cache: SearchCache | None = None,
        search_client_type: SearchClientType = SearchClientType.OPEN,
        name_resolution: bool = NAME_RESOLUTION_ENABLED,
        name_resolution_min_mentions: int = NAME_RESOLUTION_MIN_MENTIONS,
        name_resolution_max_per_sub: int = NAME_RESOLUTION_MAX_PER_SUB,
    ) -> None:
        self.sample_n = sample_n
        self.no_bfs = no_bfs
        self.no_cross_platform_lookup = no_cross_platform_lookup
        self._cache = cache
        self._search_client_type = search_client_type
        self.name_resolution = name_resolution
        self.name_resolution_min_mentions = name_resolution_min_mentions
        self.name_resolution_max_per_sub = name_resolution_max_per_sub
        self._stats = StatsCollector()
        self._assembler = ResultAssembler()

    @property
    def stats(self) -> PipelineStats:
        """Access accumulated pipeline stats."""
        return self._stats.stats

    @property
    def validation_results(self) -> dict[str, ValidationResult | None]:
        """Access canary validation results."""
        return self._stats.validation_results

    # ── Template Method ──────────────────────────────────────────────────

    async def run(self, jobs: list[SeedJob]) -> list[SeedInfluencer]:
        """Run the full pipeline.

        1. Delegate to subclass for search+crawl+extract
        2. Handle errored configs from circuit breaker
        3. Deferred name resolution
        4. Global dedup
        5. Canary validation
        6. Report (including errored configs)
        7. Save (seeds + errored_configs.json)

        Returns: list of SeedInfluencer (DB-ready, deduped).
        """
        # Step 1: Subclass-specific search + crawl + extract
        gather = await self._search_and_extract_influencers(jobs)

        # Step 2: Collect errored configs from job outcomes
        errored_configs = [
            o.errored for o in gather.job_outcomes if o.errored is not None
        ]
        if errored_configs:
            logger.warning(
                "  %d config(s) aborted due to DDG failures",
                len(errored_configs),
            )
            self._stats.stats.configs_aborted = len(errored_configs)

        # Step 3: Merge identity groups before NR
        merged = InfluencerMerger.merge(gather.influencers)
        logger.info(
            "  Pre-NR merge: %d entries → %d identities",
            len(gather.influencers), len(merged),
        )

        # Step 4: Deferred name resolution
        audit = AuditLog(AUDIT_DIR, "name_resolution")
        name_records = self._run_deferred_name_resolution(
            tracker=gather.name_tracker,
            audit=audit,
            sub_name="Influencer",
            platform=jobs[0].platform if jobs else Platform.Instagram,
            influencers=merged,
        )

        # Step 5: Post-NR merge (fold resolved names into identities)
        merged = InfluencerMerger.merge(merged)

        # Step 6: Global dedup → seeds
        seeds = InfluencerMerger.to_seeds(merged)
        logger.info(
            "  Global dedup: %d identities → %d seeds",
            len(merged), len(seeds),
        )

        # Step 7: Canary validation
        self._run_canary_validation(jobs, merged)

        # Step 8: Report
        yield_warnings = self._stats.check_yield_warnings()
        region_label = jobs[0].region.code.value if jobs else "UNKNOWN"
        run_id = self._assembler.generate_run_id(region_label)
        run_dir = RESULTS_DIR / run_id

        reporter = PipelineReporter()
        reporter.generate(
            run_dir=run_dir,
            stats=self.stats,
            validation_results=self.validation_results,
            model=LLM_PROVIDER,
            mode=self._report_mode(),
            global_seeds=seeds,
            name_mentions=name_records,
            warnings=yield_warnings,
            errored_configs=errored_configs,
            total_configs=len(jobs),
        )

        # Step 9: Save all output into run directory
        self._assembler.save_run_report(
            run_dir=run_dir,
            seeds=seeds,
            errored_configs=errored_configs,
            name_records=name_records,
            report_path=reporter.last_report_path,
        )

        return seeds

    # ── Abstract: subclass provides search+crawl+extract ─────────────────

    @abc.abstractmethod
    async def _search_and_extract_influencers(
        self, jobs: list[SeedJob],
    ) -> GatherResult:
        """Search, crawl, extract, and enrich influencers.

        Each subclass implements its own orchestration strategy:
          - PerJobPipelineRunner: per-job (search→crawl→extract per job)
          - PhasePipelineRunner: global phases (search all→dedupe→crawl→extract)

        Returns a GatherResult with all (Influencer, category_key) pairs,
        the aggregated NameMentionTracker, and job_outcomes.
        """

    @abc.abstractmethod
    async def _on_config_search_finished(
        self,
        job: SeedJob,
        search_results: SearchResults,
    ) -> None:
        """Called by _search_all_configs after a successful search.

        Subclass implements post-search behavior:
          - PerJobPipelineRunner: crawl → extract → enrich → accumulate
          - PhasePipelineRunner: accumulate URLs in url_bag
        """

    # ── Shared search loop with circuit breaker ──────────────────────────

    async def _search_all_configs(self, jobs: list[SeedJob]) -> list[JobOutcome]:
        """Search all configs with per-config threshold + global kill switch.

        Owns the search loop, threshold check, and kill switch.
        Calls _on_config_search_finished() for each successful config.
        Returns outcomes for every config (success or errored).
        """
        outcomes: list[JobOutcome] = []
        consecutive_failures = 0
        killed = False

        for i, job in enumerate(jobs, 1):
            config_key = (
                f"{job.category_key}/{job.sub.sub_name}"
                f"/{job.platform.value}/{job.region.code.value}"
            )

            # Kill switch: too many consecutive failures
            if killed:
                logger.warning(
                    "  [%d/%d] %s — SKIPPED (DDG killed)", i, len(jobs), config_key,
                )
                outcomes.append(JobOutcome(
                    job=job,
                    search_results=None,
                    errored=ErroredConfig(
                        config_key=config_key,
                        category=job.category_key,
                        sub_name=job.sub.sub_name,
                        platform=job.platform.value,
                        region=job.region.code.value,
                        failure_count=0,
                        queries_attempted=0,
                        failure_threshold_percentage=0.0,
                        reason=(
                            f"DDG killed after {DDG_KILL_AFTER_N} "
                            f"consecutive config failures"
                        ),
                    ),
                ))
                continue

            # Search this config
            search_results = self._search_one_config(job, config_key, i, len(jobs))

            # Check failure threshold
            errored = self._evaluate_search_outcome(search_results, job, config_key)

            if errored:
                consecutive_failures += 1
                outcomes.append(JobOutcome(
                    job=job, search_results=search_results, errored=errored,
                ))
                if consecutive_failures >= DDG_KILL_AFTER_N:
                    killed = True
                    logger.error(
                        "  🛑 DDG KILL SWITCH: %d consecutive failures — "
                        "skipping remaining configs",
                        consecutive_failures,
                    )
            else:
                consecutive_failures = 0
                await self._on_config_search_finished(job, search_results)
                outcomes.append(JobOutcome(
                    job=job, search_results=search_results, errored=None,
                ))

        return outcomes

    def _search_one_config(
        self,
        job: SeedJob,
        config_key: str,
        index: int,
        total: int,
    ) -> SearchResults:
        """Execute search for a single config — shared code, no duplication."""
        logger.info("  [%d/%d] %s", index, total, config_key)

        audit = AuditLog(AUDIT_DIR, config_key.replace("/", "_"))
        client = self._build_search_client(audit)
        search_svc = SearchService(audit, client=client)

        search_results = search_svc.discover_urls(job)

        self._stats.record_search(
            url_count=len(search_results.url_query_pairs),
            direct_handle_count=len(search_results.direct_handles),
            retries=0,
            failures=search_results.failure_count,
        )

        return search_results

    def _build_search_client(self, audit: AuditLog) -> OpenSearchClient | StrictSearchClient:
        """Build the correct search client based on configured type."""
        if self._search_client_type == SearchClientType.STRICT:
            from config.settings import SERPER_API_KEY
            return StrictSearchClient(audit, api_key=SERPER_API_KEY)
        return OpenSearchClient(audit, cache=self._cache)

    @staticmethod
    def _evaluate_search_outcome(
        search_results: SearchResults,
        job: SeedJob,
        config_key: str,
    ) -> ErroredConfig | None:
        """Check if search results exceed the failure threshold."""
        if search_results.queries_attempted < DDG_FAILURE_MIN_QUERIES:
            return None
        pct = search_results.failure_threshold_percentage
        if pct < DDG_FAILURE_THRESHOLD_PCT:
            return None

        reason = (
            f"DDG failure rate {pct:.0%} >= threshold "
            f"{DDG_FAILURE_THRESHOLD_PCT:.0%} "
            f"({search_results.failure_count}/{search_results.queries_attempted} "
            f"queries failed)"
        )
        logger.warning("  ❌ %s — %s", config_key, reason)
        return ErroredConfig(
            config_key=config_key,
            category=job.category_key,
            sub_name=job.sub.sub_name,
            platform=job.platform.value,
            region=job.region.code.value,
            failure_count=search_results.failure_count,
            queries_attempted=search_results.queries_attempted,
            failure_threshold_percentage=pct,
            reason=reason,
        )

    # ── Shared post-gather steps ─────────────────────────────────────────

    def _run_canary_validation(
        self,
        jobs: list[SeedJob],
        influencers: list[Influencer],
    ) -> None:
        """Validate all accumulated influencers against canary lists.

        Runs once per unique (category, sub, region) combination.
        Results are stored in self._stats.validation_results.
        """
        validator = IngestionValidator()
        seen_canary_keys: set[str] = set()

        for job in jobs:
            canary_key = f"{job.category_key}_{job.sub.sub_name}_{job.region.code.value}"
            if canary_key in seen_canary_keys:
                continue
            seen_canary_keys.add(canary_key)

            vr = validator.validate(
                influencers=influencers,
                category_key=job.category_key,
                sub_name=job.sub.sub_name,
                region=job.region.code.value,
            )
            self._stats.validation_results[canary_key] = vr

            if vr:
                logger.info(
                    "  Canary (%s): %.0f%% (%d/%d)",
                    canary_key, vr.pass_rate * 100, len(vr.found), len(vr.expected),
                )
                if vr.missing:
                    logger.warning("     Missing: %s", ", ".join(vr.missing))

    def _build_known_handles(
        self,
        influencers: list[Influencer],
    ) -> set[str]:
        """Build set of already-resolved lowercase handles for collision detection."""
        known: set[str] = set()
        for inf in influencers:
            for _plat, handle in inf.handles.items():
                if handle:
                    known.add(handle.lower())
        return known

    def _run_deferred_name_resolution(
        self,
        *,
        tracker: NameMentionTracker | None,
        audit: AuditLog,
        sub_name: str,
        platform: Platform,
        influencers: list[Influencer],
    ) -> list[NameMentionRecord]:
        """Run deferred name → handle resolution with slot recycling.

        Builds a known-handles set from all gathered influencers, gets
        per-group candidate queues from the tracker, and resolves via
        DDG with collision-aware slot recycling.

        Resolved influencers are appended to influencer_to_category so they
        are included in the subsequent global dedup + canary validation.
        """
        if tracker is None:
            return []

        if not self.name_resolution:
            logger.info("  --- Name Resolution: DISABLED (--name-resolution to enable) ---")
            return [
                NameMentionRecord(
                    canonical=m.canonical,
                    variants=m.variants,
                    mention_count=m.mention_count,
                    source_types=m.source_types,
                    source_urls=sorted(m.source_urls),
                    was_searched=False,
                )
                for m in tracker.all_names
            ]

        known_handles = self._build_known_handles(influencers)

        group_queues = tracker.top_unresolved_reddit_names_by_group(
            max_candidates_per_group=40,
            min_mentions=self.name_resolution_min_mentions,
            known_influencers=influencers,
        )

        svc = NameToHandleService(audit)
        resolved_influencers, records = svc.resolve_with_recycling(
            group_queues=group_queues,
            known_handles=known_handles,
            platform=platform,
            sub_name=sub_name,
            max_slots_per_group=self.name_resolution_max_per_sub,
        )

        for inf in resolved_influencers:
            inf.categories_found_in = ["NAME_RESOLUTION"]
            influencers.append(inf)

        # Append records for names that were not queued (audit completeness)
        queued_canonicals = {r.canonical for r in records}
        for mention in tracker.all_names:
            if mention.canonical not in queued_canonicals:
                records.append(NameMentionRecord(
                    canonical=mention.canonical,
                    variants=mention.variants,
                    mention_count=mention.mention_count,
                    source_types=mention.source_types,
                    source_urls=sorted(mention.source_urls),
                    was_searched=False,
                ))

        return records

    def _report_mode(self) -> str:
        """Return mode label for the report. Override if needed."""
        return "sampled" if self.sample_n else "real-time"
