"""
Unit tests for deferred name resolution — the pipeline-level logic that
resolves names → handles via DDG after all jobs complete.

Tests the PipelineRunner._run_deferred_name_resolution() method and the
CLI flag propagation. All DDG calls are mocked.

NOTE: We mock crawl4ai at module level to avoid ImportError in test envs
      where the crawl4ai library is not installed.
"""

import sys
from unittest.mock import patch, MagicMock

import pytest

# Mock crawl4ai before any pipeline imports (it's a C-extension dep)
_mock_crawl4ai = MagicMock()
for _sub in [
    "crawl4ai",
    "crawl4ai.content_filter_strategy",
    "crawl4ai.markdown_generation_strategy",
]:
    sys.modules.setdefault(_sub, _mock_crawl4ai)

from config.schema import NameMentionRecord, Influencer, Platform, SourceType
from services.extraction.NameMentionTracker import NameMentionTracker
from pipeline import PipelineRunner


# ══════════════════════════════════════════════════════════════════════
# Helper
# ══════════════════════════════════════════════════════════════════════

def _build_tracker(
    names: dict[str, dict],
) -> NameMentionTracker:
    """Build a tracker from a name config dict.

    Args:
        names: {"Jeff Nippard": {"count": 3, "source": "reddit", "sub": "Fitness"}, ...}
    """
    tracker = NameMentionTracker()
    for name, cfg in names.items():
        source_str = cfg.get("source", "non-reddit")
        source_type = SourceType(source_str)
        tracker.record_names_in_url(
            names_with_counts={name: cfg["count"]},
            source_url=f"https://example.com/{name.lower().replace(' ', '-')}",
            source_type=source_type,
            platform="Instagram",
            category="FITNESS",
            sub_name=cfg.get("sub", "Fitness"),
            region="US",
        )
    return tracker


# ══════════════════════════════════════════════════════════════════════
# Resolution disabled explicitly
# ══════════════════════════════════════════════════════════════════════

class TestResolutionDisabled:
    """When name_resolution=False (explicit), no DDG calls fire."""

    def test_default_resolution_is_on(self):
        runner = PipelineRunner()
        assert runner.name_resolution is True

    def test_disabled_returns_records_without_resolution(self):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 5, "source": "reddit"},
        })
        audit = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )
        assert len(records) == 1
        assert records[0].canonical == "Jeff Nippard"
        assert records[0].was_searched is False
        assert records[0].resolved_handle == ""

    def test_disabled_records_include_source_urls(self):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 5, "source": "reddit"},
        })
        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=MagicMock(),
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )
        assert len(records[0].source_urls) > 0

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_disabled_does_not_call_ddg(self, mock_resolve):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 5, "source": "reddit"},
        })
        audit = MagicMock()

        runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )
        mock_resolve.assert_not_called()

    def test_none_tracker_returns_empty(self):
        runner = PipelineRunner(name_resolution=True)
        records = runner._run_deferred_name_resolution(
            tracker=None,
            audit=MagicMock(),
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )
        assert records == []


# ══════════════════════════════════════════════════════════════════════
# Resolution enabled — top_reddit_names gating
# ══════════════════════════════════════════════════════════════════════

class TestResolutionEnabled:
    """When name_resolution=True, DDG fires only for top reddit names."""

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_reddit_names_resolved(self, mock_sleep, mock_ddgs_cls):
        """Reddit names should be DDG-searched."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard)"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        runner = PipelineRunner(name_resolution=True)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 3, "source": "reddit"},
        })
        audit = MagicMock()
        audit.log = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )

        assert len(records) == 1
        assert records[0].was_searched is True
        assert records[0].resolved_handle == "jeffnippard"
        assert records[0].resolved_platform == "Instagram"

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_non_reddit_excluded_from_resolution(self, mock_sleep, mock_ddgs_cls):
        """Non-reddit names should never be resolved."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard"}
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        runner = PipelineRunner(name_resolution=True)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 10, "source": "non-reddit"},
        })
        audit = MagicMock()
        audit.log = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )

        assert len(records) == 1
        assert records[0].was_searched is False

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_resolved_handles_merged_into_entries(self, mock_sleep, mock_ddgs_cls):
        """Resolved handles should be appended to _all_influencer_entries."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/alexleonidas/",
             "title": "Alex Leonidas (@alexleonidas)"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        runner = PipelineRunner(name_resolution=True)
        tracker = _build_tracker({
            "Alex Leonidas": {"count": 3, "source": "reddit"},
        })
        audit = MagicMock()
        audit.log = MagicMock()

        

        entries: list = []
        runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=entries,
        )

        assert len(entries) == 1
        inf = entries[0]
        assert "alexleonidas" in inf.handles.values()
        assert inf.categories_found_in == ["NAME_RESOLUTION"]
        assert inf.source_urls == {"https://example.com/alex-leonidas"}
        assert inf.extraction_methods == {"name_resolution"}
        assert inf.citation_count == 1


# ══════════════════════════════════════════════════════════════════════
# NameMentionRecord output
# ══════════════════════════════════════════════════════════════════════

class TestNameMentionRecordOutput:
    """Verify NameMentionRecord fields are correctly populated."""

    def test_disabled_records_have_correct_fields(self):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_tracker({
            "Jeff Nippard": {"count": 5, "source": "reddit"},
            "Alex Leonidas": {"count": 2, "source": "non-reddit"},
        })
        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=MagicMock(),
            sub_name="Fitness",
            platform=Platform.Instagram,
            influencers=[],
        )

        assert len(records) == 2
        by_name = {r.canonical: r for r in records}

        jeff = by_name["Jeff Nippard"]
        assert jeff.mention_count == 5
        assert jeff.source_types == ["reddit"]
        assert jeff.was_searched is False

        alex = by_name["Alex Leonidas"]
        assert alex.source_types == ["non-reddit"]

    def test_record_to_dict_includes_source_urls(self):
        record = NameMentionRecord(
            canonical="Jeff Nippard",
            variants=["Jeff Nippard"],
            mention_count=5,
            source_types=["reddit"],
            source_urls=["https://reddit.com/1"],
            was_searched=True,
            resolved_handle="jeffnippard",
            resolved_platform="Instagram",
        )
        d = record.to_dict()
        assert d["canonical"] == "Jeff Nippard"
        assert d["source_urls"] == ["https://reddit.com/1"]
        assert d["was_searched"] is True


# ══════════════════════════════════════════════════════════════════════
# CLI flag propagation
# ══════════════════════════════════════════════════════════════════════

class TestCLIFlagPropagation:
    """Verify that CLI flags reach the PipelineRunner."""

    def test_name_resolution_flag_defaults(self):
        runner = PipelineRunner()
        assert runner.name_resolution is True
        assert runner.name_resolution_min_mentions == 2

    def test_name_resolution_flag_override(self):
        runner = PipelineRunner(
            name_resolution=True,
            name_resolution_min_mentions=5,
        )
        assert runner.name_resolution is True
        assert runner.name_resolution_min_mentions == 5

    def test_phase_pipeline_flag_defaults(self):
        from phase_pipeline import PhasePipelineRunner
        runner = PhasePipelineRunner()
        assert runner.name_resolution is True
        assert runner.name_resolution_min_mentions == 2

    def test_phase_pipeline_flag_override(self):
        from phase_pipeline import PhasePipelineRunner
        runner = PhasePipelineRunner(
            name_resolution=True,
            name_resolution_min_mentions=3,
        )
        assert runner.name_resolution is True
        assert runner.name_resolution_min_mentions == 3
