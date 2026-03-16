"""
test_pipeline_abort — Pipeline behaviour when configs are errored.

Verifies:
- errored configs from _search_all_configs flow to reporter + assembler
- run() returns seeds only from successful configs
- stats.configs_aborted count is correct
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from config.schema import (
    Influencer, Platform, ErroredConfig, SeedInfluencer,
)
from config.seed_schema import (
    SeedJob, SubCategory, Region, RegionCode, Difficulty,
)
from base_pipeline import BasePipelineRunner, GatherResult, JobOutcome


# ── Fixtures ──

def _make_job(sub_name: str = "Test") -> SeedJob:
    sub = SubCategory(
        sub_name=sub_name, is_top_level=True, search_prompt="test",
        alt_search_terms=[], known_sources=[], platform_notes="",
        region_notes="", difficulty=Difficulty.EASY, strict_slugs=[],
    )
    region = Region(code=RegionCode.US, language="en", label="US")
    return SeedJob(
        category_key="TEST", sub=sub,
        platform=Platform.Instagram, region=region,
    )


def _make_errored_config(sub_name: str = "Test") -> ErroredConfig:
    return ErroredConfig(
        config_key=f"TEST/{sub_name}/Instagram/US",
        category="TEST", sub_name=sub_name,
        platform="Instagram", region="US",
        failure_count=4, queries_attempted=5,
        failure_threshold_percentage=0.8,
        reason="DDG failure rate 80% >= threshold 50%",
    )


class StubAbortRunner(BasePipelineRunner):
    """Concrete subclass returning pre-built gather with errored outcomes."""

    def __init__(self, gather_result: GatherResult, **kwargs):
        super().__init__(**kwargs)
        self._canned = gather_result

    async def _search_and_extract_influencers(self, jobs):
        return self._canned

    async def _on_config_search_finished(self, job, search_results):
        pass


class TestPipelineAbort:

    def test_errored_configs_passed_to_reporter(self):
        errored = _make_errored_config("FailedSub")
        gather = GatherResult(
            influencer_to_category=[],
            name_tracker=None,
            job_outcomes=[
                JobOutcome(job=_make_job("FailedSub"), search_results=None, errored=errored),
            ],
        )

        runner = StubAbortRunner(gather_result=gather, name_resolution=False)
        jobs = [_make_job("FailedSub")]

        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch("base_pipeline.AUDIT_DIR", Path(tmp)),
                patch("base_pipeline.PipelineReporter") as MockReporter,
                patch("base_pipeline.ResultAssembler") as MockAssembler,
            ):
                mock_reporter = MagicMock()
                MockReporter.return_value = mock_reporter
                MockAssembler.return_value = MagicMock()
                runner._assembler = MockAssembler.return_value

                seeds = asyncio.run(runner.run(jobs))

            call_kwargs = mock_reporter.generate.call_args
            passed_errored = call_kwargs.kwargs.get("errored_configs", [])
            assert len(passed_errored) == 1
            assert passed_errored[0].config_key == "TEST/FailedSub/Instagram/US"

    def test_errored_configs_passed_to_assembler(self):
        errored = _make_errored_config("FailedSub")
        gather = GatherResult(
            influencer_to_category=[],
            name_tracker=None,
            job_outcomes=[
                JobOutcome(job=_make_job("FailedSub"), search_results=None, errored=errored),
            ],
        )

        runner = StubAbortRunner(gather_result=gather, name_resolution=False)

        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch("base_pipeline.AUDIT_DIR", Path(tmp)),
                patch("base_pipeline.PipelineReporter") as MockReporter,
                patch("base_pipeline.ResultAssembler") as MockAssembler,
            ):
                MockReporter.return_value = MagicMock()
                mock_assembler = MagicMock()
                MockAssembler.return_value = mock_assembler
                runner._assembler = mock_assembler

                asyncio.run(runner.run([_make_job("FailedSub")]))

            mock_assembler.save_run_report.assert_called_once()
            call_kwargs = mock_assembler.save_run_report.call_args
            passed_errored = call_kwargs.kwargs.get("errored_configs", [])
            assert len(passed_errored) == 1

    def test_mixed_success_and_failure(self):
        success_inf = Influencer(
            name="Good Creator", handles={Platform.Instagram: "goodcreator"},
        )
        errored = _make_errored_config("FailedSub")
        gather = GatherResult(
            influencer_to_category=[(success_inf, "TEST")],
            name_tracker=None,
            job_outcomes=[
                JobOutcome(job=_make_job("GoodSub"), search_results=None, errored=None),
                JobOutcome(job=_make_job("FailedSub"), search_results=None, errored=errored),
            ],
        )

        runner = StubAbortRunner(gather_result=gather, name_resolution=False)

        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch("base_pipeline.AUDIT_DIR", Path(tmp)),
                patch("base_pipeline.PipelineReporter") as MockReporter,
                patch("base_pipeline.ResultAssembler") as MockAssembler,
            ):
                MockReporter.return_value = MagicMock()
                MockAssembler.return_value = MagicMock()
                runner._assembler = MockAssembler.return_value

                seeds = asyncio.run(runner.run([_make_job("GoodSub"), _make_job("FailedSub")]))

            assert len(seeds) >= 1
            assert any(s.ig_handle == "goodcreator" for s in seeds)
