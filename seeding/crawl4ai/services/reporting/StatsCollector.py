"""
StatsCollector — Centralised pipeline metrics accumulator.

Replaces scattered ``self.stats.X += Y`` mutations that were inline
in PipelineRunner.run_job().  Each pipeline step calls one method here.
"""

from __future__ import annotations

import logging

from config.schema import PageResult, PipelineStats
from config.settings import YIELD_WARNING_THRESHOLD
from services.extraction.HandleExtractionService import HandleExtractionResult

logger = logging.getLogger(__name__)


class StatsCollector:
    """Accumulates pipeline metrics across pipeline steps."""

    def __init__(self) -> None:
        self.stats = PipelineStats()
        self.validation_results: dict = {}

    # ── Step recorders ──

    def record_search(
        self,
        url_count: int,
        direct_handle_count: int,
        retries: int,
        failures: int,
    ) -> None:
        """Record search metrics."""
        self.stats.urls_discovered += url_count + direct_handle_count
        self.stats.search_retries += retries
        self.stats.search_failures += failures

    def record_crawl(
        self,
        pages: list[PageResult],
        dropped: int = 0,
        retries: int = 0,
    ) -> None:
        """Record crawl metrics from page results."""
        self.stats.pages_crawled += sum(1 for p in pages if p.success)
        self.stats.pages_failed += sum(1 for p in pages if not p.success)
        self.stats.pages_dropped += dropped
        self.stats.crawl_retries += retries

    def record_extraction(self, result: HandleExtractionResult) -> None:
        """Record extraction metrics."""
        extracted_count = sum(1 for v in result.llm_handles.values() if v)
        self.stats.pages_extracted += extracted_count
        self.stats.influencers_raw += len(result.all_merged)
        self.stats.regex_handles_total += len(result.regex_handles)
        self.stats.total_input_tokens += result.llm_input_tokens
        self.stats.total_output_tokens += result.llm_output_tokens

    def record_enrichment(
        self,
        unique_count: int,
        handles_filled: int,
        retries: int,
        failures: int,
    ) -> None:
        """Record enrichment metrics."""
        self.stats.influencers_deduped += unique_count
        self.stats.handles_filled += handles_filled
        self.stats.enrich_retries += retries
        self.stats.enrich_failures += failures

    # ── Yield monitoring ──

    def check_yield_warnings(self) -> list[str]:
        """Check extraction yield and return warning strings if below threshold.

        Returns an empty list when everything looks healthy.
        Warnings are also emitted via logger.warning for CLI visibility.
        """
        warnings: list[str] = []
        pages = self.stats.pages_crawled
        if pages == 0:
            return warnings

        yield_ratio = self.stats.regex_handles_total / pages
        if yield_ratio < YIELD_WARNING_THRESHOLD:
            msg = (
                f"LOW YIELD: {yield_ratio:.1f} regex handles/page "
                f"(threshold: {YIELD_WARNING_THRESHOLD:.1f}). "
                f"Platform URL patterns may need updating."
            )
            logger.warning(msg)
            warnings.append(msg)

        return warnings
