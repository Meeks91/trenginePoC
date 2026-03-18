"""
Integration Test: Deferred Name Resolution
=============================================

Tests the full deferred resolution flow: multiple pages with overlapping
names → tracker aggregation → top_reddit_names gating → DDG mock → handle output.

Verifies:
  1. Multi-page names are aggregated correctly across jobs
  2. Reddit-only filtering works correctly
  3. Feature flag off = no DDG calls
  4. Name records appear in final output with source_urls
  5. Cross-job merge works end-to-end

NOTE: We mock crawl4ai at module level to avoid ImportError in test envs
      where the crawl4ai library is not installed.
"""

import sys
from types import ModuleType
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

from config.schema import NameMentionRecord, SourceType
from services.extraction.NameMentionTracker import NameMentionTracker
from pipeline import PipelineRunner


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

def _build_multi_page_tracker() -> NameMentionTracker:
    """Simulate names from 3 pages (2 Reddit, 1 non-Reddit)."""
    tracker = NameMentionTracker()

    # Reddit page 1: Jeff Nippard (3x), Alex Leonidas (1x)
    tracker.record_names_in_url(
        names_with_counts={"Jeff Nippard": 3, "Alex Leonidas": 1},
        source_url="https://reddit.com/r/fitness/page1",
        source_type=SourceType.REDDIT,
        platform="Instagram",
        category="FITNESS",
        sub_name="Fitness",
        region="US",
    )

    # Reddit page 2: Jeff Nippard (2x), Sean Nalewanyj (1x)
    tracker.record_names_in_url(
        names_with_counts={"Jeff Nippard": 2, "Sean Nalewanyj": 1},
        source_url="https://reddit.com/r/fitness/page2",
        source_type=SourceType.REDDIT,
        platform="Instagram",
        category="FITNESS",
        sub_name="Fitness",
        region="US",
    )

    # Non-Reddit page: some random name (5x — high count but non-reddit)
    tracker.record_names_in_url(
        names_with_counts={"Random Blogger": 5},
        source_url="https://blog.com/fitness-tips",
        source_type=SourceType.NON_REDDIT,
        platform="Instagram",
        category="FITNESS",
        sub_name="Fitness",
        region="US",
    )

    return tracker


# ══════════════════════════════════════════════════════════════════════
# Tests
# ══════════════════════════════════════════════════════════════════════

class TestMultiPageAggregation:
    """Names from multiple pages are correctly merged."""

    def test_cross_page_counts_accumulated(self):
        tracker = _build_multi_page_tracker()
        by_name = {m.canonical: m for m in tracker.all_names}

        assert by_name["Jeff Nippard"].mention_count == 5  # 3 + 2
        assert by_name["Alex Leonidas"].mention_count == 1
        assert by_name["Sean Nalewanyj"].mention_count == 1
        assert by_name["Random Blogger"].mention_count == 5

    def test_source_types_correct(self):
        tracker = _build_multi_page_tracker()
        by_name = {m.canonical: m for m in tracker.all_names}

        assert by_name["Jeff Nippard"].source_types == ["reddit"]
        assert by_name["Random Blogger"].source_types == ["non-reddit"]

    def test_source_urls_tracked(self):
        tracker = _build_multi_page_tracker()
        by_name = {m.canonical: m for m in tracker.all_names}

        jeff_urls = by_name["Jeff Nippard"].source_urls
        assert len(jeff_urls) == 2
        assert "https://reddit.com/r/fitness/page1" in jeff_urls
        assert "https://reddit.com/r/fitness/page2" in jeff_urls


class TestTopRedditNamesGating:
    """Only reddit names are selected via top_reddit_names()."""

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_reddit_names_resolved_non_reddit_excluded(self, mock_sleep, mock_ddgs_cls):
        """Reddit names should be resolved; non-reddit excluded."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard)"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        runner = PipelineRunner(name_resolution=True)
        tracker = _build_multi_page_tracker()
        audit = MagicMock()
        audit.log = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform="Instagram",
            influencers=[],
        )

        by_name = {r.canonical: r for r in records}

        # Jeff Nippard: reddit source → resolved
        jeff = by_name["Jeff Nippard"]
        assert jeff.was_searched is True
        assert jeff.resolved_handle == "jeffnippard"

        # Random Blogger: non-reddit → not resolved
        random = by_name["Random Blogger"]
        assert random.was_searched is False

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_non_reddit_only_names_not_ddged(self, mock_sleep, mock_ddgs_cls):
        """Non-reddit-only names should not trigger DDG calls."""
        mock_ddgs = MagicMock()
        call_tracker = {"queries": []}

        def track_text(query, **kwargs):
            call_tracker["queries"].append(query)
            return [{"href": "https://www.instagram.com/someone/",
                      "title": "Someone"}]

        mock_ddgs.text = track_text
        mock_ddgs_cls.return_value = mock_ddgs

        tracker = NameMentionTracker()
        tracker.record_names_in_url(
            names_with_counts={"Blog Only": 100},
            source_url="https://blog.com/1",
            source_type=SourceType.NON_REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )

        runner = PipelineRunner(name_resolution=True)
        audit = MagicMock()
        audit.log = MagicMock()

        runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform="Instagram",
            influencers=[],
        )

        assert len(call_tracker["queries"]) == 0


class TestFeatureFlagOff:
    """Feature flag off = no DDG, but records still returned."""

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_flag_off_no_ddg_calls(self, mock_resolve):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_multi_page_tracker()
        audit = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=audit,
            sub_name="Fitness",
            platform="Instagram",
            influencers=[],
        )

        mock_resolve.assert_not_called()
        assert len(records) == 4  # All 4 names still returned as raw records
        assert all(r.was_searched is False for r in records)


class TestCrossJobMerge:
    """Name trackers from multiple jobs merge into global tracker."""

    def test_trackers_merge_correctly(self):
        t1 = NameMentionTracker()
        t1.record_names_in_url(
            names_with_counts={"Jeff Nippard": 2},
            source_url="https://reddit.com/1",
            source_type=SourceType.REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )

        t2 = NameMentionTracker()
        t2.record_names_in_url(
            names_with_counts={"Jeff Nippard": 3},
            source_url="https://reddit.com/2",
            source_type=SourceType.REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )
        t2.record_names_in_url(
            names_with_counts={"Alex Leonidas": 1},
            source_url="https://reddit.com/3",
            source_type=SourceType.REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )

        global_tracker = NameMentionTracker()
        global_tracker.merge(t1)
        global_tracker.merge(t2)

        mentions = global_tracker.all_names
        by_name = {m.canonical: m for m in mentions}

        assert by_name["Jeff Nippard"].mention_count == 5
        assert by_name["Alex Leonidas"].mention_count == 1
        assert len(mentions) == 2

        # Source URLs should be merged
        jeff_urls = by_name["Jeff Nippard"].source_urls
        assert len(jeff_urls) == 2

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    def test_merged_tracker_resolves_correctly(self, mock_sleep, mock_ddgs_cls):
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard)"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        t1 = NameMentionTracker()
        t1.record_names_in_url(
            names_with_counts={"Jeff Nippard": 1},
            source_url="https://reddit.com/1",
            source_type=SourceType.REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )

        t2 = NameMentionTracker()
        t2.record_names_in_url(
            names_with_counts={"Jeff Nippard": 2},
            source_url="https://reddit.com/2",
            source_type=SourceType.REDDIT,
            platform="Instagram",
            category="FITNESS",
            sub_name="Fitness",
            region="US",
        )

        global_tracker = NameMentionTracker()
        global_tracker.merge(t1)
        global_tracker.merge(t2)

        runner = PipelineRunner(name_resolution=True)
        audit = MagicMock()
        audit.log = MagicMock()

        records = runner._run_deferred_name_resolution(
            tracker=global_tracker,
            audit=audit,
            sub_name="Fitness",
            platform="Instagram",
            influencers=[],
        )

        assert len(records) == 1
        assert records[0].resolved_handle == "jeffnippard"


class TestNameRecordsInOutput:
    """Verify NameMentionRecord serialization for final output."""

    def test_records_serialize_to_dict(self):
        runner = PipelineRunner(name_resolution=False)
        tracker = _build_multi_page_tracker()
        records = runner._run_deferred_name_resolution(
            tracker=tracker,
            audit=MagicMock(),
            sub_name="Fitness",
            platform="Instagram",
            influencers=[],
        )

        dicts = [r.to_dict() for r in records]
        assert all("canonical" in d for d in dicts)
        assert all("mention_count" in d for d in dicts)
        assert all("source_types" in d for d in dicts)
        assert all("source_urls" in d for d in dicts)
        assert all("was_searched" in d for d in dicts)
