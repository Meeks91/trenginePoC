"""
Tests for ResultAssembler
===========================
Unit tests for file I/O and result assembly.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch


from config.schema import (
    Influencer, Platform, PageResult,
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
        assert len(sources) == 2
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


class TestGenerateRunId:
    """Tests for ResultAssembler.generate_run_id()."""

    def test_format_includes_region(self):
        run_id = ResultAssembler.generate_run_id("US")
        assert run_id.endswith("_US")

    def test_format_uses_12_hour_clock(self):
        run_id = ResultAssembler.generate_run_id("UK")
        parts = run_id.split("_")
        assert len(parts) == 3
        assert len(parts[0]) == 10  # YYYY-MM-DD
        assert "am" in parts[1] or "pm" in parts[1]
        assert "." in parts[1]  # H.MM separator
        assert parts[2] == "UK"

    def test_different_regions_produce_different_ids(self):
        us_id = ResultAssembler.generate_run_id("US")
        uk_id = ResultAssembler.generate_run_id("UK")
        assert us_id != uk_id
