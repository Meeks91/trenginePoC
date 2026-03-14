"""
test_result_assembler_report_dir — Report directory consolidation.

Verifies save_report_directory() writes all expected files:
  - global_seeds.json (always)
  - unresolved_names.json (always)
  - errored_configs.json (only if non-empty)
  - pipeline_output.json (only if provided)
  - report copy (only if provided)
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from config.schema import (
    ErroredConfig, NameMentionRecord, SeedInfluencer,
)
from services.reporting.ResultAssembler import ResultAssembler


def _make_seed(name: str, ig: str = "") -> SeedInfluencer:
    return SeedInfluencer(
        name=name, ig_handle=ig, tk_handle="", yt_handle="",
        categories=["TEST"],
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


class TestReportDirectoryConsolidation:

    def test_all_files_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "reports"
            with patch("services.reporting.ResultAssembler.REPORTS_DIR", report_dir):
                assembler = ResultAssembler()

                report_md = report_dir / "report_test.md"
                report_dir.mkdir(parents=True, exist_ok=True)
                report_md.write_text("# Test Report")

                seeds = [_make_seed("Joe Wicks", "thebodycoach")]
                errored = [_make_errored()]
                records = [
                    _make_unresolved_record("Unknown Name"),
                    _make_resolved_record("Found Person", "found_handle"),
                ]

                assembler.save_report_directory(
                    seeds=seeds,
                    errored_configs=errored,
                    name_records=records,
                    pipeline_output=[{"test": "data"}],
                    report_path=report_md,
                )

            assert (report_dir / "global_seeds.json").exists()
            assert (report_dir / "unresolved_names.json").exists()
            assert (report_dir / "errored_configs.json").exists()
            assert (report_dir / "pipeline_output.json").exists()
            assert (report_dir / "report_test.md").exists()

    def test_errored_configs_not_written_when_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "reports"
            with patch("services.reporting.ResultAssembler.REPORTS_DIR", report_dir):
                assembler = ResultAssembler()
                assembler.save_report_directory(
                    seeds=[_make_seed("Test")],
                    errored_configs=[],
                )

            assert (report_dir / "global_seeds.json").exists()
            assert (report_dir / "unresolved_names.json").exists()
            assert not (report_dir / "errored_configs.json").exists()

    def test_unresolved_names_only_includes_unresolved(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "reports"
            with patch("services.reporting.ResultAssembler.REPORTS_DIR", report_dir):
                assembler = ResultAssembler()
                records = [
                    _make_unresolved_record("No Handle"),
                    _make_resolved_record("Has Handle", "found"),
                ]
                assembler.save_report_directory(
                    seeds=[], errored_configs=[],
                    name_records=records,
                )

            data = json.loads((report_dir / "unresolved_names.json").read_text())
            assert len(data) == 1
            assert data[0]["canonical"] == "No Handle"

    def test_global_seeds_content_correct(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "reports"
            with patch("services.reporting.ResultAssembler.REPORTS_DIR", report_dir):
                assembler = ResultAssembler()
                seeds = [_make_seed("Kayla", "kayla_itsines")]
                assembler.save_report_directory(
                    seeds=seeds, errored_configs=[],
                )

            data = json.loads((report_dir / "global_seeds.json").read_text())
            assert len(data) == 1
            assert data[0]["ig_handle"] == "kayla_itsines"

    def test_pipeline_output_not_written_when_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_dir = Path(tmp) / "reports"
            with patch("services.reporting.ResultAssembler.REPORTS_DIR", report_dir):
                assembler = ResultAssembler()
                assembler.save_report_directory(
                    seeds=[], errored_configs=[],
                )

            assert not (report_dir / "pipeline_output.json").exists()
