"""
Tests for ResultAssembler
===========================
Unit tests for file I/O and result assembly.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from config.schema import (
    Influencer, NameMentionRecord, Platform, SourceResult,
    PageResult, SubResult, RegionResult,
)
from services.reporting.ResultAssembler import ResultAssembler


def _page(url, success=True, md_path="pages/test.md"):
    return PageResult(
        url=url, query="test query", raw_markdown="raw",
        fit_markdown="fit", raw_token_estimate=100,
        fit_token_estimate=50, success=success, md_path=md_path,
    )


class TestSaveSearchUrls:
    """Tests for ResultAssembler.save_search_urls()."""

    def test_saves_json_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            search_dir = Path(tmp) / "search"
            with patch("services.reporting.ResultAssembler.SEARCH_DIR", search_dir):
                assembler = ResultAssembler()
                pairs = [
                    ("https://a.com", "query a"),
                    ("https://b.com", "query b"),
                ]
                assembler.save_search_urls("FITNESS_Fitness_IG_US", pairs)

                out_file = search_dir / "FITNESS_Fitness_IG_US_urls.json"
                assert out_file.exists()
                data = json.loads(out_file.read_text())
                assert len(data) == 2
                assert data[0]["url"] == "https://a.com"
                assert data[1]["query"] == "query b"

    def test_empty_pairs_saves_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            search_dir = Path(tmp) / "search"
            with patch("services.reporting.ResultAssembler.SEARCH_DIR", search_dir):
                assembler = ResultAssembler()
                assembler.save_search_urls("key", [])
                out_file = search_dir / "key_urls.json"
                data = json.loads(out_file.read_text())
                assert data == []


class TestBuildSourceResults:
    """Tests for ResultAssembler.build_source_results()."""

    def test_builds_from_pages_and_map(self):
        assembler = ResultAssembler()
        pages = [
            _page("https://a.com"),
            _page("https://b.com"),
            _page("https://fail.com", success=False),
        ]
        url_to_inf = {
            "https://a.com": [Influencer(name="Alice", handles={Platform.Instagram: "alice"})],
            "https://b.com": [],
        }
        sources = assembler.build_source_results(pages, url_to_inf)
        assert len(sources) == 2  # failed page excluded
        assert sources[0].url == "https://a.com"
        assert len(sources[0].influencers) == 1
        assert sources[1].url == "https://b.com"
        assert len(sources[1].influencers) == 0

    def test_missing_url_in_map_returns_empty_influencers(self):
        assembler = ResultAssembler()
        pages = [_page("https://c.com")]
        sources = assembler.build_source_results(pages, {})
        assert len(sources) == 1
        assert sources[0].influencers == []


class TestSavePipelineOutput:
    """Tests for ResultAssembler.save_pipeline_output()."""

    def test_saves_output_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            results_dir = Path(tmp) / "results"
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", results_dir):
                assembler = ResultAssembler()
                output = [
                    RegionResult(
                        region="US",
                        platforms={
                            "Instagram": {
                                "FITNESS": {
                                    "Fitness": SubResult(is_top_level=True),
                                }
                            }
                        },
                    )
                ]
                path = assembler.save_pipeline_output(output)
                assert path.exists()
                data = json.loads(path.read_text())
                assert len(data) == 1
                assert data[0]["region"] == "US"


# ── Fixtures for unresolved names tests ──

def _sample_records() -> list[NameMentionRecord]:
    """Mix of resolved and unresolved records."""
    return [
        NameMentionRecord(
            canonical="Joe Wicks",
            variants=["joe wicks"],
            mention_count=5,
            source_types=["llm"],
            source_urls=["https://example.com/page1"],
            was_searched=True,
            resolved_handle="thebodycoach",
            resolved_platform="Instagram",
        ),
        NameMentionRecord(
            canonical="Lucy Davis",
            variants=["lucy davis"],
            mention_count=3,
            source_types=["llm"],
            source_urls=["https://example.com/page1", "https://example.com/page2"],
            was_searched=True,
            resolved_handle="",
            resolved_platform="",
        ),
        NameMentionRecord(
            canonical="Sean Casey",
            variants=["sean casey"],
            mention_count=1,
            source_types=["llm"],
            source_urls=["https://example.com/page1"],
            was_searched=False,
            resolved_handle="",
            resolved_platform="",
        ),
    ]


class TestSaveUnresolvedNames:
    """Tests for ResultAssembler.save_unresolved_names()."""

    def test_filters_to_unresolved_only(self):
        """Only records with no resolved handle are saved."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                data = json.loads(path.read_text())
                assert len(data) == 2
                names = {r["canonical"] for r in data}
                assert names == {"Lucy Davis", "Sean Casey"}

    def test_resolved_records_excluded(self):
        """Joe Wicks (resolved) must not appear in output."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                data = json.loads(path.read_text())
                assert "Joe Wicks" not in [r["canonical"] for r in data]

    def test_preserves_all_fields(self):
        """Each record in JSON has all NameMentionRecord fields."""
        expected_fields = {
            "canonical", "variants", "mention_count",
            "source_types", "source_urls",
            "was_searched", "resolved_handle", "resolved_platform",
        }
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                data = json.loads(path.read_text())
                for record in data:
                    assert set(record.keys()) == expected_fields

    def test_mention_count_preserved(self):
        """Mention counts and search status transfer correctly."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                data = json.loads(path.read_text())
                lucy = next(r for r in data if r["canonical"] == "Lucy Davis")
                assert lucy["mention_count"] == 3
                assert lucy["was_searched"] is True
                assert len(lucy["source_urls"]) == 2
                sean = next(r for r in data if r["canonical"] == "Sean Casey")
                assert sean["mention_count"] == 1
                assert sean["was_searched"] is False

    def test_empty_input_produces_empty_json(self):
        """No records → empty JSON array."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names([])
                assert json.loads(path.read_text()) == []

    def test_all_resolved_produces_empty_json(self):
        """If all records are resolved, output is empty array."""
        records = [
            NameMentionRecord(
                canonical="Joe Wicks",
                mention_count=5,
                was_searched=True,
                resolved_handle="thebodycoach",
                resolved_platform="Instagram",
            ),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(records)
                assert json.loads(path.read_text()) == []

    def test_output_filename(self):
        """Output file is named unresolved_names.json."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                assert path.name == "unresolved_names.json"
                assert path.parent == Path(tmp)

    def test_schema_shape(self):
        """Each record has correct field types, not just names."""
        with tempfile.TemporaryDirectory() as tmp:
            with patch("services.reporting.ResultAssembler.RESULTS_DIR", Path(tmp)):
                assembler = ResultAssembler()
                path = assembler.save_unresolved_names(_sample_records())
                data = json.loads(path.read_text())
                for record in data:
                    assert isinstance(record["canonical"], str)
                    assert isinstance(record["variants"], list)
                    assert all(isinstance(v, str) for v in record["variants"])
                    assert isinstance(record["mention_count"], int)
                    assert record["mention_count"] > 0
                    assert isinstance(record["source_types"], list)
                    assert isinstance(record["source_urls"], list)
                    assert all(isinstance(u, str) for u in record["source_urls"])
                    assert isinstance(record["was_searched"], bool)
                    assert isinstance(record["resolved_handle"], str)
                    assert record["resolved_handle"] == ""
                    assert isinstance(record["resolved_platform"], str)
