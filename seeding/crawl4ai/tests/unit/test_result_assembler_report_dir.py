"""
test_result_assembler_report_dir — Run-scoped report directory.

Verifies save_run_report() writes all expected files:
  - seeds.json (always)
  - unresolved_names.json (always)
  - errors.json (only if non-empty)
  - report.md (only if provided)
"""

import json
import tempfile
from pathlib import Path

import pytest

from config.schema import (
    ErroredConfig, NameMentionRecord, Influencer, Platform,
)
from services.reporting.ResultAssembler import ResultAssembler


def _make_seed(name: str, ig: str = "") -> Influencer:
    handles = {Platform.Instagram: ig} if ig else {}
    return Influencer(
        name=name, handles=handles,
        categories_found_in=["TEST"],
    )


def _make_unresolved_record(name: str) -> NameMentionRecord:
    return NameMentionRecord(
        canonical=name, mention_count=3,
        source_types=["regex"], source_urls=["http://a.com"],
        was_searched=True, resolved_handle="", resolved_platform="",
    )


def _make_resolved_record(name: str, handle: str) -> NameMentionRecord:
    return NameMentionRecord(
        canonical=name, mention_count=5,
        source_types=["regex"], source_urls=["http://b.com"],
        was_searched=True, resolved_handle=handle, resolved_platform="Instagram",
    )


def _make_errored(key: str = "TEST/Sub/IG/US") -> ErroredConfig:
    return ErroredConfig(
        config_key=key, category="TEST", sub_name="Sub",
        platform="Instagram", region="US",
        failure_count=4, queries_attempted=5,
        failure_threshold_percentage=0.8, reason="test reason",
    )


class TestSaveRunReport:

    def test_all_files_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "2026-03-15_134840_US"
            report_src = Path(tmp) / "report_src.md"
            report_src.write_text("# Test Report")

            assembler = ResultAssembler()
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=[_make_seed("Joe Wicks", "thebodycoach")],
                errored_configs=[_make_errored()],
                name_records=[
                    _make_unresolved_record("Unknown Name"),
                    _make_resolved_record("Found Person", "found_handle"),
                ],
                report_path=report_src,
            )

            assert (run_dir / "seeds.json").exists()
            assert (run_dir / "unresolved_names.json").exists()
            assert (run_dir / "errors.json").exists()
            assert (run_dir / "report.md").exists()

    def test_errors_not_written_when_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "2026-03-15_134840_US"

            assembler = ResultAssembler()
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=[_make_seed("Test")],
                errored_configs=[],
            )

            assert (run_dir / "seeds.json").exists()
            assert (run_dir / "unresolved_names.json").exists()
            assert not (run_dir / "errors.json").exists()

    def test_unresolved_names_only_includes_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"

            assembler = ResultAssembler()
            records = [
                _make_unresolved_record("No Handle"),
                _make_resolved_record("Has Handle", "found"),
            ]
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=[],
                errored_configs=[],
                name_records=records,
            )

            data = json.loads((run_dir / "unresolved_names.json").read_text())
            assert len(data) == 1
            assert data[0]["canonical"] == "No Handle"

    def test_seeds_content_correct(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"

            assembler = ResultAssembler()
            seeds = [_make_seed("Kayla", "kayla_itsines")]
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=seeds,
                errored_configs=[],
            )

            data = json.loads((run_dir / "seeds.json").read_text())
            assert len(data) == 1
            assert data[0]["ig_handle"] == "kayla_itsines"

    def test_report_not_copied_when_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"

            assembler = ResultAssembler()
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=[],
                errored_configs=[],
            )

            assert not (run_dir / "report.md").exists()

    def test_seeds_json_includes_enrichment_fields(self):
        """seeds.json must serialize source_urls, extraction_methods, citation_count."""
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "run"

            seed = Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                categories_found_in=["FITNESS"],
                source_urls={"https://a.com", "https://b.com"},
                extraction_methods={"regex", "llm"},
            )
            assembler = ResultAssembler()
            assembler.save_run_report(
                run_dir=run_dir,
                seeds=[seed],
                errored_configs=[],
            )

            data = json.loads((run_dir / "seeds.json").read_text())
            assert len(data) == 1
            assert data[0]["source_urls"] == ["https://a.com", "https://b.com"]
            assert data[0]["extraction_methods"] == ["llm", "regex"]
            assert data[0]["citation_count"] == 2

class TestRunDirLocation:
    """Verify run directory is under RESULTS_DIR, not REPORTS_DIR."""

    def test_run_dir_under_results_not_reports(self):
        """base_pipeline must use RESULTS_DIR / run_id, not REPORTS_DIR / run_id."""
        from config import RESULTS_DIR, REPORTS_DIR

        run_id = ResultAssembler.generate_run_id("US")

        expected_run_dir = RESULTS_DIR / run_id
        wrong_run_dir = REPORTS_DIR / run_id

        # The expected parent must be results/, not results/reports/
        assert expected_run_dir.parent == RESULTS_DIR
        assert wrong_run_dir.parent == REPORTS_DIR
        assert RESULTS_DIR != REPORTS_DIR
