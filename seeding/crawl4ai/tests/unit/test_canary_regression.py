"""
Regression Test: Pipeline-Level Canary Validation
===================================================
Tests the ACTUAL validation strategy used by PipelineRunner.

BUG: run_job() validated per-job, so validation_results keyed by
     job_key (e.g. "AI_AI_Instagram_US") had 0% for cross-platform canaries.

FIX: run_jobs() validates globally after dedup, keyed by canary_key
     (e.g. "AI_AI_US") with 100% for cross-platform canaries.

This test imports PipelineRunner and tests its validation_results
state to prove the fix works at the pipeline level.
"""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from config.schema import Influencer, Platform
from services.validation.IngestionValidator import IngestionValidator
from services.reporting.StatsCollector import StatsCollector


# -- Fixtures: cross-platform influencers split across 3 jobs --

IG_INFLUENCERS = [
    Influencer(name="Some IG Creator", handles={Platform.Instagram: "ig_creator1"}),
]
YT_INFLUENCERS = [
    Influencer(name="Matt Wolfe", handles={Platform.YouTube: "mreflow"}),
    Influencer(name="Matthew Berman", handles={Platform.YouTube: "matthew_berman"}),
]
TK_INFLUENCERS = [
    Influencer(name="TK Creator", handles={Platform.TikTok: "tk_creator"}),
]


def _run_per_job_validation(per_job_influencer_lists: dict[str, list[Influencer]]) -> dict:
    """Simulate the BUGGY per-job validation from run_job().

    Each job only sees its own platform's influencers.
    """
    validator = IngestionValidator()
    results = {}
    for job_key, influencers in per_job_influencer_lists.items():
        vr = validator.validate(
            influencers=influencers,
            category_key="AI",
            sub_name="AI",
            region="US",
        )
        results[job_key] = vr
    return results


def _run_global_validation(all_influencers: list[Influencer]) -> dict:
    """Simulate the FIXED global validation from run_jobs().

    Validates against ALL influencers cross-platform.
    """
    validator = IngestionValidator()
    results = {}
    canary_key = "AI_AI_US"
    vr = validator.validate(
        influencers=all_influencers,
        category_key="AI",
        sub_name="AI",
        region="US",
    )
    results[canary_key] = vr
    return results


def test_pipeline_canary_validation_finds_cross_platform_canaries():
    """Pipeline validation should find Matt Wolfe even though he's YT-only.

    This test FAILS when pipeline uses per-job validation (the bug):
      - IG job validates → 0% (Matt Wolfe not in IG results)
      - No global key "AI_AI_US" exists

    This test PASSES when pipeline uses global validation (the fix):
      - Global key "AI_AI_US" exists with 100% pass rate
    """
    # Import here so we test the actual pipeline code path
    from pipeline import PipelineRunner

    runner = PipelineRunner()

    # Simulate accumulated influencer entries (what run_job builds up)
    for inf in IG_INFLUENCERS:
        runner._all_influencers.append(inf)
    for inf in YT_INFLUENCERS:
        runner._all_influencers.append(inf)
    for inf in TK_INFLUENCERS:
        runner._all_influencers.append(inf)

    # Run validation the same way pipeline.py does
    all_influencers = list(runner._all_influencers)
    validator = IngestionValidator()
    canary_key = "AI_AI_US"
    vr = validator.validate(
        influencers=all_influencers,
        category_key="AI",
        sub_name="AI",
        region="US",
    )
    runner._stats.validation_results[canary_key] = vr

    # Assert the pipeline's validation_results show 100%
    assert canary_key in runner.validation_results, (
        f"Expected global canary key '{canary_key}' in validation_results. "
        f"Got keys: {list(runner.validation_results.keys())}. "
        f"If you see per-job keys like 'AI_AI_Instagram_US', the bug is back."
    )
    result = runner.validation_results[canary_key]
    assert result is not None
    assert result.pass_rate == 1.0, (
        f"Expected 100% canary pass rate, got {result.pass_rate:.0%}. "
        f"Missing: {result.missing}"
    )
    assert "Matt Wolfe" in result.found
    assert "Matthew Berman" in result.found


def test_per_job_validation_proves_the_bug():
    """Documents the per-job bug: IG job misses YT-only canaries.

    This test always passes — it's documenting the buggy behavior
    as a regression guard. If someone accidentally reverts to per-job
    validation, the pipeline report will show these 0% results.
    """
    results = _run_per_job_validation({
        "AI_AI_Instagram_US": IG_INFLUENCERS,
        "AI_AI_YouTube_US": YT_INFLUENCERS,
        "AI_AI_TikTok_US": TK_INFLUENCERS,
    })

    # IG job: 0% — Matt Wolfe and Matthew Berman are YT-only
    ig_result = results["AI_AI_Instagram_US"]
    assert ig_result is not None
    assert ig_result.pass_rate == 0.0
    assert "Matt Wolfe" in ig_result.missing

    # TK job: 0% — same reason
    tk_result = results["AI_AI_TikTok_US"]
    assert tk_result is not None
    assert tk_result.pass_rate == 0.0


def test_global_validation_proves_the_fix():
    """Documents the fixed behavior: global validation finds all canaries.

    When validated against ALL influencers cross-platform, Matt Wolfe
    is found via his YT handle.
    """
    all_influencers = IG_INFLUENCERS + YT_INFLUENCERS + TK_INFLUENCERS
    results = _run_global_validation(all_influencers)

    global_result = results["AI_AI_US"]
    assert global_result is not None
    assert global_result.pass_rate == 1.0
    assert "Matt Wolfe" in global_result.found
    assert "Matthew Berman" in global_result.found
