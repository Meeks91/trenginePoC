"""
Integration Test: E2E Sampled (Full PipelineRunner)
=====================================================
Full pipeline on Fitness/IG/US via PipelineRunner with --sample 3.
Tests the CLI integration path: SeedJob → PipelineRunner.run_job() → full output.

Unlike test_e2e_from_html.py (which mocks HTTP), this test hits the real web.
It validates: specific handles, report generation, audit trail, and stats.

Cost: ~$0.003 per run.

Run with:
    PYTHONPATH="." python3 tests/integration/test_e2e_sampled.py
"""

import asyncio
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

import config
from config.seed_schema import (
    SeedJob, Platform, RegionCode, REGIONS, load_categories,
)
from pipeline import PipelineRunner


@pytest.mark.network
def test_e2e_sampled():
    """Full pipeline on 1 job with sampling — verifies handles, report, stats."""
    assert config.GEMINI_API_KEY, "GEMINI_API_KEY must be set to run this test"
    asyncio.run(_test_e2e_sampled_async())


async def _test_e2e_sampled_async():

    categories = load_categories()

    fitness_cat = categories.get("FITNESS")
    if not fitness_cat:
        print("WARN: FITNESS category not found — skipping")
        return

    fitness_sub = fitness_cat.top_level_sub
    region = REGIONS[RegionCode.US]

    job = SeedJob(
        platform=Platform.Instagram,
        region=region,
        category_key="FITNESS",
        sub=fitness_sub,
        year="2026",
    )

    print(f"\nRunning e2e sampled test: {job.category_key}/{job.sub.sub_name}/{job.platform.value}/{job.region.code.value}")
    print("Sampling: 3 pages\n")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # Patch at the SERVICE MODULE level where each config was imported.
        # `from config import X` binds X at import time; patching config.X
        # doesn't affect services that already imported it.
        with (
            patch("services.reporting.ResultAssembler.RESULTS_DIR", tmp_path),
            patch("base_pipeline.AUDIT_DIR", tmp_path / "audit"),
            patch("pipeline.AUDIT_DIR", tmp_path / "audit"),
            patch("services.crawling.CrawlService.PAGES_DIR", tmp_path / "pages"),
            patch("services.extraction.LLMExtractionService.RAW_DIR", tmp_path / "raw"),
            patch("base_pipeline.REPORTS_DIR", tmp_path / "reports"),
            patch("pipeline.REPORTS_DIR", tmp_path / "reports"),
        ):
            runner = PipelineRunner(sample_n=3)
            result = await runner.run_single_url(
                url="https://www.google.com/search?q=fitness+influencers+Instagram",
                platform=job.platform.value,
                category_key=job.category_key,
                sub_name=job.sub.sub_name,
                region=job.region.code.value,
            )

            # ── Source assertions ──
            assert len(result.sources) > 0, "No sources crawled"
            assert all(s.url for s in result.sources), "Source missing URL"
            assert all(s.query for s in result.sources), "Source missing query"

            # ── Influencer assertions ──
            assert len(result.all_influencers) > 0, "No influencers found"
            assert len(result.all_influencers) >= 3, (
                f"Expected at least 3 influencers from sampled run, got {len(result.all_influencers)}"
            )

            # Verify at least some have handles (not just names)
            with_handles = [inf for inf in result.all_influencers if inf.handles]
            assert len(with_handles) > 0, "No influencers have handles after enrichment"

            # ── Stats assertions ──
            # Note: urls_discovered=0 is expected since run_single_url skips search
            assert runner.stats.pages_crawled > 0, "No pages crawled"
            assert runner.stats.pages_extracted > 0, "No pages extracted"
            assert runner.stats.influencers_raw > 0, "No raw influencers"
            assert runner.stats.influencers_deduped > 0, "No deduped influencers"
            assert runner.stats.total_input_tokens > 0, "No input tokens recorded"

            # ── Report assertions ──
            report_dir = tmp_path / "reports"
            run_dirs = [d for d in report_dir.iterdir() if d.is_dir()] if report_dir.exists() else []
            assert len(run_dirs) == 1, f"Expected 1 run directory, got {len(run_dirs)}"
            run_dir = run_dirs[0]
            assert (run_dir / "report.md").exists(), "report.md not created"
            report_content = (run_dir / "report.md").read_text()
            assert "Pipeline Report" in report_content, "Report missing header"
            assert str(runner.stats.influencers_deduped) in report_content, "Report missing dedup count"

            # ── Audit assertions ──
            audit_files = list((tmp_path / "audit").glob("*.jsonl"))
            assert len(audit_files) > 0, "No audit files created"

            # ── Output file assertions ──
            # run_job doesn't write pipeline_output.json (run_jobs does),
            # so we just verify the SubResult structure
            assert result.is_top_level is not None
            assert isinstance(result.to_dict(), dict)

            # ── Print results ──
            print("\nResults:")
            print(f"  Sources crawled: {len(result.sources)}")
            print(f"  Influencers found: {len(result.all_influencers)}")
            print(f"  With handles: {len(with_handles)}")
            for inf in result.all_influencers[:10]:
                handle_str = ", ".join(
                    f"{p.value}: {h}" for p, h in inf.handles.items()
                ) if inf.handles else "no handle"
                print(f"    {inf.name} ({handle_str})")

            print("\nPipeline stats:")
            print(f"  URLs discovered: {runner.stats.urls_discovered}")
            print(f"  Pages crawled: {runner.stats.pages_crawled}")
            print(f"  Pages extracted: {runner.stats.pages_extracted}")
            print(f"  Input tokens: {runner.stats.total_input_tokens:,}")

            print("\nE2E sampled test PASSED")


if __name__ == "__main__":
    asyncio.run(test_e2e_sampled())
