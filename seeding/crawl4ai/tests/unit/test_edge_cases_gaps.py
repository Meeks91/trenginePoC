"""
Edge Case Tests: StatsCollector, NameMentionTracker, PageTruncator
===================================================================
Covers identified test gaps T5, T6, T7 from the code review.
"""


from config.schema import SourceType
from services.reporting.StatsCollector import StatsCollector
from services.extraction.NameMentionTracker import NameMentionTracker
from services.extraction.PageTruncator import truncate_for_llm, _MAX_TRUNCATED_CHARS


# ── T5: StatsCollector.check_yield_warnings() edge cases ──

class TestYieldWarnings:
    """Edge cases for the yield-warning threshold check."""

    def _collector_with(self, pages: int, handles: int) -> StatsCollector:
        sc = StatsCollector()
        sc.stats.pages_crawled = pages
        sc.stats.regex_handles_total = handles
        return sc

    def test_zero_pages_no_warning(self):
        """Zero pages → no warning (avoid division by zero)."""
        sc = self._collector_with(pages=0, handles=0)
        assert sc.check_yield_warnings() == []

    def test_yield_above_threshold_no_warning(self):
        """Yield ratio well above threshold → no warning."""
        sc = self._collector_with(pages=10, handles=50)  # 5.0 >> 2.0
        assert sc.check_yield_warnings() == []

    def test_yield_exactly_at_threshold_no_warning(self):
        """REGRESSION: yield ratio == threshold → no warning (not <)."""
        sc = self._collector_with(pages=10, handles=20)  # exactly 2.0
        assert sc.check_yield_warnings() == [], \
            "yield ratio == threshold should NOT trigger a warning"

    def test_yield_just_below_threshold_warns(self):
        """Yield ratio just below threshold → warning."""
        sc = self._collector_with(pages=10, handles=19)  # 1.9 < 2.0
        warnings = sc.check_yield_warnings()
        assert len(warnings) == 1
        assert "LOW YIELD" in warnings[0]

    def test_yield_zero_handles_warns(self):
        """Zero handles with pages → warning."""
        sc = self._collector_with(pages=5, handles=0)
        warnings = sc.check_yield_warnings()
        assert len(warnings) == 1


# ── T6: NameMentionTracker.merge() edge cases ──

class TestNameMentionTrackerMerge:
    """Edge cases for merging two NameMentionTrackers."""

    def test_merge_empty_into_empty(self):
        """Merging two empty trackers → empty result."""
        a = NameMentionTracker()
        b = NameMentionTracker()
        a.merge(b)
        assert len(a.all_names) == 0

    def test_merge_populated_into_empty(self):
        """Merging a populated tracker into an empty one → adopts all entries."""
        a = NameMentionTracker()
        b = NameMentionTracker()
        b.record_names_in_url(
            names_with_counts={"Alice Doe": 2},
            source_url="https://example.com",
            source_type=SourceType.LLM,
            platform="Instagram",
            category="FITNESS",
            sub_name="Gym",
            region="UK",
        )
        a.merge(b)
        names = [m.canonical for m in a.all_names]
        assert "Alice Doe" in names

    def test_merge_overlapping_names_combines_counts(self):
        """Same name in both trackers → mention counts should combine."""
        a = NameMentionTracker()
        b = NameMentionTracker()

        a.record_names_in_url(
            names_with_counts={"Alice Doe": 3},
            source_url="https://page1.com",
            source_type=SourceType.REGEX,
            platform="Instagram",
            category="FITNESS",
            sub_name="Gym",
            region="UK",
        )
        b.record_names_in_url(
            names_with_counts={"Alice Doe": 2},
            source_url="https://page2.com",
            source_type=SourceType.LLM,
            platform="TikTok",
            category="BEAUTY",
            sub_name="Skincare",
            region="US",
        )

        a.merge(b)

        # Alice should appear once with combined mentions
        alice_entries = [m for m in a.all_names if m.canonical == "Alice Doe"]
        assert len(alice_entries) == 1
        assert alice_entries[0].mention_count >= 5  # 3 + 2

    def test_merge_preserves_source_urls(self):
        """Merged tracker should have source URLs from both sides."""
        a = NameMentionTracker()
        b = NameMentionTracker()

        a.record_names_in_url(
            names_with_counts={"Bob Smith": 1},
            source_url="https://a.com",
            source_type=SourceType.REGEX,
            platform="Instagram",
            category="FITNESS",
            sub_name="Gym",
            region="UK",
        )
        b.record_names_in_url(
            names_with_counts={"Bob Smith": 1},
            source_url="https://b.com",
            source_type=SourceType.LLM,
            platform="Instagram",
            category="FITNESS",
            sub_name="Gym",
            region="UK",
        )

        a.merge(b)

        bob = [m for m in a.all_names if m.canonical == "Bob Smith"][0]
        assert "https://a.com" in bob.source_urls
        assert "https://b.com" in bob.source_urls


# ── T7: PageTruncator _MAX_TRUNCATED_CHARS safety cap ──

class TestPageTruncatorCap:
    """Verify the 8,000-char safety cap is enforced."""

    def test_short_text_not_truncated(self):
        """Text under 500 chars → returned as-is."""
        text = "Short text"
        assert truncate_for_llm(text) == text

    def test_long_text_without_headings_capped(self):
        """Long text with no person headings → capped at _MAX_TRUNCATED_CHARS."""
        long_text = "A" * 20_000
        result = truncate_for_llm(long_text)
        assert len(result) <= _MAX_TRUNCATED_CHARS

    def test_long_text_with_headings_capped(self):
        """Even with person headings, output is capped at _MAX_TRUNCATED_CHARS."""
        # Create a huge page with many person headings spaced far apart
        sections = []
        for i in range(50):
            sections.append(f"## Person {i} Smith\n" + "x" * 500)
        huge_text = "\n".join(sections)
        assert len(huge_text) > _MAX_TRUNCATED_CHARS

        result = truncate_for_llm(huge_text)
        assert len(result) <= _MAX_TRUNCATED_CHARS, (
            f"Truncated text is {len(result)} chars, exceeds cap of {_MAX_TRUNCATED_CHARS}"
        )

    def test_empty_input(self):
        """Empty string → returned as-is."""
        assert truncate_for_llm("") == ""

    def test_none_input(self):
        """None input → returned as-is."""
        assert truncate_for_llm(None) is None
