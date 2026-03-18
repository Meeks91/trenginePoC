"""
test_pipeline_dedup — Regression test proving merge() is called in base_pipeline.run().

Mocks _search_and_extract_influencers to return duplicate influencers,
then asserts that:
  1. InfluencerMerger.merge() is called pre-NR (Step 3)
  2. InfluencerMerger.merge() is called post-NR (Step 5)
  3. Duplicate influencers are actually deduped in final seeds
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from config.schema import Influencer, Platform
from config.seed_schema import (
    SeedJob, SubCategory, Difficulty, Region, RegionCode,
)
from base_pipeline import BasePipelineRunner, GatherResult, JobOutcome
from services.extraction.NameMentionTracker import NameMentionTracker


class _StubPipeline(BasePipelineRunner):
    """Concrete stub subclass so we can instantiate and test run()."""

    def __init__(self, gather: GatherResult) -> None:
        super().__init__(name_resolution=False)
        self._gather = gather

    async def _search_and_extract_influencers(
        self, jobs: list[SeedJob],
    ) -> GatherResult:
        return self._gather

    async def _on_config_search_finished(self, job, search_results) -> None:
        pass

    def _report_mode(self) -> str:
        return "test"


def _make_job() -> SeedJob:
    """Minimal SeedJob for testing."""
    sub = SubCategory(
        sub_name="Gym",
        is_top_level=True,
        search_prompt="gym fitness influencers",
        alt_search_terms=[],
        known_sources=[],
        platform_notes="",
        region_notes="",
        difficulty=Difficulty.EASY,
        strict_slugs=[],
    )
    return SeedJob(
        platform=Platform.Instagram,
        category_key="FITNESS",
        sub=sub,
        region=Region(code=RegionCode.US, language="en", label="United States"),
    )


def _jeff_nippard(handle: str = "jeffnippard") -> Influencer:
    """Create a Jeff Nippard influencer — used for dedup testing."""
    return Influencer(
        name="Jeff Nippard",
        handles={Platform.Instagram: handle},
        categories_found_in=["FITNESS"],
    )


class TestMergeCalledInRun:
    """InfluencerMerger.merge() must be called pre-NR and post-NR in run()."""

    @pytest.mark.asyncio
    async def test_merge_called_twice(self) -> None:
        """merge() is called at Step 3 (pre-NR) and Step 5 (post-NR)."""
        dupes = [_jeff_nippard(), _jeff_nippard(), _jeff_nippard()]
        gather = GatherResult(
            influencers=dupes,
            name_tracker=NameMentionTracker(),
            job_outcomes=[],
        )
        runner = _StubPipeline(gather)
        runner._assembler = MagicMock()
        runner._assembler.generate_run_id.return_value = "test-run"

        with (
            patch("base_pipeline.InfluencerMerger") as mock_merger,
            patch("base_pipeline.PipelineReporter"),
            patch("base_pipeline.AuditLog"),
        ):
            mock_merger.merge.side_effect = lambda infs: infs
            mock_merger.filter_blocked.side_effect = lambda infs, **kw: infs

            await runner.run([_make_job()])

            assert mock_merger.merge.call_count == 2, (
                f"Expected merge() called twice (pre-NR + post-NR), "
                f"got {mock_merger.merge.call_count}"
            )

    @pytest.mark.asyncio
    async def test_duplicates_actually_deduped(self) -> None:
        """3 identical Jeff Nippard entries → merge reduces to 1 identity."""
        dupes = [_jeff_nippard(), _jeff_nippard(), _jeff_nippard()]
        gather = GatherResult(
            influencers=dupes,
            name_tracker=NameMentionTracker(),
            job_outcomes=[],
        )
        runner = _StubPipeline(gather)
        runner._assembler = MagicMock()
        runner._assembler.generate_run_id.return_value = "test-run"

        with (
            patch("base_pipeline.PipelineReporter"),
            patch("base_pipeline.AuditLog"),
        ):
            # Use REAL InfluencerMerger — no mock — to prove dedup happens
            seeds = await runner.run([_make_job()])
            # 3 identical entries → 1 seed
            assert len(seeds) == 1
            assert seeds[0].name == "Jeff Nippard"

    @pytest.mark.asyncio
    async def test_pre_nr_merge_reduces_duplicates(self) -> None:
        """Pre-NR merge: 3 Jeff Nippard entries with same handle → 1 identity."""
        from services.enrichment.InfluencerMerger import InfluencerMerger

        dupes = [_jeff_nippard(), _jeff_nippard(), _jeff_nippard()]
        merged = InfluencerMerger.merge(dupes)
        assert len(merged) == 1
        assert merged[0].name == "Jeff Nippard"
        assert merged[0].handles[Platform.Instagram] == "jeffnippard"
        assert "FITNESS" in merged[0].categories_found_in
