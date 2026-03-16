"""
Unit tests for NameMentionTracker — tests for record_names_in_url(),
source_urls tracking, SourceType enum, top_reddit_names(), all_names,
reddit_names, non_reddit_names, and merge().
"""

import pytest

from config.schema import SourceType
from services.extraction.NameMentionTracker import NameMentionTracker, NameMention


def _record(tracker, name, count, url, source_type, platform="Instagram",
            category="FITNESS", sub="Gym", region="US"):
    """Helper to reduce test boilerplate."""
    tracker.record_names_in_url(
        names_with_counts={name: count},
        source_url=url,
        source_type=source_type,
        platform=platform,
        category=category,
        sub_name=sub,
        region=region,
    )


class TestRecordNamesInUrl:
    """record_names_in_url() stores source_urls, source_types, and dimensions."""

    def test_empty_tracker(self):
        tracker = NameMentionTracker()
        assert tracker.all_names == []

    def test_single_name_recorded(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 2, "https://reddit.com/r/fitness/1", SourceType.REDDIT)
        mentions = tracker.all_names
        assert len(mentions) == 1
        assert mentions[0].canonical == "Jeff Nippard"
        assert mentions[0].mention_count == 2

    def test_source_url_stored(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://reddit.com/r/fitness/1", SourceType.REDDIT)
        assert "https://reddit.com/r/fitness/1" in tracker.all_names[0].source_urls

    def test_source_type_stored_as_enum_value(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://reddit.com/r/fitness/1", SourceType.REDDIT)
        assert "reddit" in tracker.all_names[0].source_types

    def test_dimensions_stored(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://example.com/1", SourceType.REGEX,
                platform="Instagram", category="FITNESS", sub="Gym", region="UK")
        m = tracker.all_names[0]
        assert "Instagram" in m.platforms
        assert "FITNESS" in m.categories
        assert "Gym" in m.sub_names
        assert "UK" in m.regions

    def test_multiple_urls_accumulated(self):
        """Same name from two different URLs → both URLs stored."""
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://reddit.com/r/fitness/1", SourceType.REDDIT)
        _record(tracker, "Jeff Nippard", 2, "https://blog.com/fitness", SourceType.NON_REDDIT)
        m = tracker.all_names[0]
        assert len(m.source_urls) == 2
        assert m.mention_count == 3

    def test_multiple_source_types_from_different_sources(self):
        """Same name from regex + LLM → both source types."""
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://example.com/1", SourceType.REGEX)
        _record(tracker, "Jeff Nippard", 1, "https://example.com/1", SourceType.LLM)
        m = tracker.all_names[0]
        assert sorted(m.source_types) == ["llm", "regex"]

    def test_sorted_by_count_descending(self):
        tracker = NameMentionTracker()
        _record(tracker, "Alex Leonidas", 1, "https://a.com", SourceType.REDDIT)
        _record(tracker, "Jeff Nippard", 5, "https://b.com", SourceType.REDDIT)
        _record(tracker, "Sean Nalewanyj", 3, "https://c.com", SourceType.REDDIT)
        counts = [m.mention_count for m in tracker.all_names]
        assert counts == sorted(counts, reverse=True)


class TestFuzzyGrouping:
    """90%+ similarity grouping behaviour."""

    def test_exact_string_merged(self):
        tracker = NameMentionTracker()
        _record(tracker, "Joshua Weissman", 2, "https://a.com", SourceType.REDDIT)
        _record(tracker, "Joshua Weissman", 1, "https://b.com", SourceType.NON_REDDIT)
        assert len(tracker.all_names) == 1
        assert tracker.all_names[0].mention_count == 3
        assert len(tracker.all_names[0].source_urls) == 2

    def test_different_names_separate(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://a.com", SourceType.REDDIT)
        _record(tracker, "Sam Way", 1, "https://b.com", SourceType.REDDIT)
        assert len(tracker.all_names) == 2


class TestWasSearched:
    """mark_searched() flag propagation."""

    def test_not_searched_by_default(self):
        tracker = NameMentionTracker()
        _record(tracker, "Alex Leonidas", 1, "https://a.com", SourceType.REDDIT)
        assert tracker.all_names[0].was_searched is False

    def test_mark_searched_upgrades_bucket(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 3, "https://a.com", SourceType.REDDIT)
        assert tracker.all_names[0].was_searched is False
        tracker.mark_searched({"Jeff Nippard"})
        assert tracker.all_names[0].was_searched is True

    def test_mark_searched_unknown_name_is_noop(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://a.com", SourceType.REDDIT)
        tracker.mark_searched({"No One Known"})
        assert tracker.all_names[0].was_searched is False


class TestRedditNonRedditProperties:
    """reddit_names and non_reddit_names properties."""

    def test_reddit_names_filters_to_reddit(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://reddit.com/1", SourceType.REDDIT)
        _record(tracker, "Blog Person", 1, "https://blog.com/1", SourceType.NON_REDDIT)
        assert len(tracker.reddit_names) == 1
        assert tracker.reddit_names[0].canonical == "Jeff Nippard"

    def test_non_reddit_names_excludes_reddit(self):
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 1, "https://reddit.com/1", SourceType.REDDIT)
        _record(tracker, "Blog Person", 1, "https://blog.com/1", SourceType.NON_REDDIT)
        assert len(tracker.non_reddit_names) == 1
        assert tracker.non_reddit_names[0].canonical == "Blog Person"

    def test_mixed_name_appears_in_reddit(self):
        """Name from both reddit + non-reddit appears in reddit_names."""
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 2, "https://reddit.com/1", SourceType.REDDIT)
        _record(tracker, "Jeff Nippard", 3, "https://blog.com/1", SourceType.NON_REDDIT)
        reddit = tracker.reddit_names
        assert len(reddit) == 1
        assert reddit[0].mention_count == 5  # additive counts


class TestTopRedditNames:
    """top_reddit_names(max_per_group) — groups by 4 dims, picks top N."""

    def test_top_5_per_group(self):
        tracker = NameMentionTracker()
        for i in range(8):
            _record(tracker, f"Person {i}", 10 - i, f"https://reddit.com/{i}",
                    SourceType.REDDIT, sub="Fitness")
        result = tracker.top_reddit_names(max_per_group=5, min_mentions=1)
        assert len(result) == 5
        canonicals = {m.canonical for m in result}
        assert "Person 0" in canonicals  # highest count
        assert "Person 5" not in canonicals  # 6th

    def test_non_reddit_excluded(self):
        tracker = NameMentionTracker()
        _record(tracker, "Blog Only", 100, "https://blog.com/1", SourceType.NON_REDDIT)
        assert len(tracker.top_reddit_names(max_per_group=5, min_mentions=1)) == 0

    def test_different_groups_get_separate_allocations(self):
        tracker = NameMentionTracker()
        _record(tracker, "Fitness Person", 5, "https://reddit.com/1",
                SourceType.REDDIT, sub="Fitness", category="FITNESS")
        _record(tracker, "Yoga Person", 5, "https://reddit.com/2",
                SourceType.REDDIT, sub="Yoga", category="FITNESS")
        result = tracker.top_reddit_names(max_per_group=5, min_mentions=1)
        assert len(result) == 2  # different sub groups

    def test_additive_counts_with_non_reddit(self):
        """Reddit name with non-reddit mentions uses total count for sorting."""
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 2, "https://reddit.com/1", SourceType.REDDIT)
        _record(tracker, "Jeff Nippard", 8, "https://blog.com/1", SourceType.NON_REDDIT)
        _record(tracker, "Small Person", 1, "https://reddit.com/2", SourceType.REDDIT)
        result = tracker.top_reddit_names(max_per_group=5, min_mentions=1)
        assert result[0].canonical == "Jeff Nippard"
        assert result[0].mention_count == 10  # 2 + 8 additive

    def test_empty_tracker(self):
        tracker = NameMentionTracker()
        assert tracker.top_reddit_names(max_per_group=5, min_mentions=1) == []


class TestTopRedditNamesByGroup:
    """top_reddit_names_by_group() — returns per-group deques for slot recycling."""

    def test_returns_deques_per_group(self):
        from collections import deque
        tracker = NameMentionTracker()
        _record(tracker, "Jeff Nippard", 5, "https://reddit.com/1",
                SourceType.REDDIT, sub="Gym", category="FITNESS",
                platform="Instagram", region="US")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=10, min_mentions=1,
        )
        assert len(result) == 1
        key = ("Instagram", "FITNESS", "Gym", "US")
        assert key in result
        assert isinstance(result[key], deque)
        assert result[key][0].canonical == "Jeff Nippard"

    def test_sorted_by_total_mention_count(self):
        tracker = NameMentionTracker()
        _record(tracker, "Low Person", 2, "https://reddit.com/1",
                SourceType.REDDIT, sub="Gym")
        _record(tracker, "High Person", 10, "https://reddit.com/2",
                SourceType.REDDIT, sub="Gym")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=10, min_mentions=1,
        )
        group = list(result.values())[0]
        assert group[0].canonical == "High Person"
        assert group[1].canonical == "Low Person"

    def test_min_mentions_filters(self):
        tracker = NameMentionTracker()
        _record(tracker, "Rare Person", 1, "https://reddit.com/1",
                SourceType.REDDIT, sub="Gym")
        _record(tracker, "Popular Person", 5, "https://reddit.com/2",
                SourceType.REDDIT, sub="Gym")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=10, min_mentions=3,
        )
        group = list(result.values())[0]
        assert len(group) == 1
        assert group[0].canonical == "Popular Person"

    def test_max_candidates_caps_queue(self):
        tracker = NameMentionTracker()
        for i in range(10):
            _record(tracker, f"Person {i}", 10 - i, f"https://reddit.com/{i}",
                    SourceType.REDDIT, sub="Gym")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=3, min_mentions=1,
        )
        group = list(result.values())[0]
        assert len(group) == 3

    def test_non_reddit_excluded(self):
        tracker = NameMentionTracker()
        _record(tracker, "Blog Only", 100, "https://blog.com/1",
                SourceType.NON_REDDIT, sub="Gym")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=10, min_mentions=1,
        )
        assert len(result) == 0

    def test_separate_groups_for_different_subs(self):
        tracker = NameMentionTracker()
        _record(tracker, "Gym Person", 5, "https://reddit.com/1",
                SourceType.REDDIT, sub="Gym")
        _record(tracker, "Yoga Person", 5, "https://reddit.com/2",
                SourceType.REDDIT, sub="Yoga")
        result = tracker.top_reddit_names_by_group(
            max_candidates_per_group=10, min_mentions=1,
        )
        assert len(result) == 2


class TestMergeTrackers:
    """Merging one tracker into another."""

    def test_merge_adds_new_names(self):
        t1 = NameMentionTracker()
        _record(t1, "Jeff Nippard", 2, "https://a.com", SourceType.REDDIT)

        t2 = NameMentionTracker()
        _record(t2, "Alex Leonidas", 3, "https://b.com", SourceType.REDDIT)

        t1.merge(t2)
        assert len(t1.all_names) == 2

    def test_merge_accumulates_counts(self):
        t1 = NameMentionTracker()
        _record(t1, "Jeff Nippard", 2, "https://a.com", SourceType.REDDIT)

        t2 = NameMentionTracker()
        _record(t2, "Jeff Nippard", 3, "https://b.com", SourceType.REDDIT)

        t1.merge(t2)
        assert len(t1.all_names) == 1
        assert t1.all_names[0].mention_count == 5

    def test_merge_unions_source_urls(self):
        t1 = NameMentionTracker()
        _record(t1, "Jeff Nippard", 1, "https://a.com", SourceType.REDDIT)

        t2 = NameMentionTracker()
        _record(t2, "Jeff Nippard", 1, "https://b.com", SourceType.NON_REDDIT)

        t1.merge(t2)
        m = t1.all_names[0]
        assert sorted(m.source_urls) == ["https://a.com", "https://b.com"]
        assert sorted(m.source_types) == ["non-reddit", "reddit"]

    def test_merge_propagates_was_searched(self):
        t1 = NameMentionTracker()
        _record(t1, "Jeff Nippard", 1, "https://a.com", SourceType.REDDIT)

        t2 = NameMentionTracker()
        _record(t2, "Jeff Nippard", 1, "https://b.com", SourceType.REDDIT)
        t2.mark_searched({"Jeff Nippard"})

        t1.merge(t2)
        assert t1.all_names[0].was_searched is True


class TestExtractCandidateNamesWithCounts:
    """Test the counts-aware extractor."""

    def test_basic_counts(self):
        from services.extraction.NameExtractor import extract_candidate_names_with_counts
        text = "Jeff Nippard is great. I agree that Jeff Nippard has the best tips."
        counts = extract_candidate_names_with_counts(text)
        assert "Jeff Nippard" in counts
        assert counts["Jeff Nippard"] == 2

    def test_blocklist_excluded(self):
        from services.extraction.NameExtractor import extract_candidate_names_with_counts
        text = "Thank You for visiting. New York is beautiful."
        counts = extract_candidate_names_with_counts(text)
        assert "Thank You" not in counts
        assert "New York" not in counts

    def test_empty_text(self):
        from services.extraction.NameExtractor import extract_candidate_names_with_counts
        assert extract_candidate_names_with_counts("") == {}
