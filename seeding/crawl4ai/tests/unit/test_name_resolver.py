"""
Unit tests for NameResolver — DDG-based name → handle resolution.

All DDG calls are mocked to avoid external network dependencies.
"""

import pytest
from unittest.mock import patch, MagicMock

from services.extraction.NameResolver import (
    resolve_names_via_ddg,
    _extract_handles_from_results,
    _score_result,
)
from services.extraction.RegexHandleExtractor import ExtractedHandle


def _mock_audit():
    """Create a mock audit log."""
    audit = MagicMock()
    audit.log = MagicMock()
    return audit


# ══════════════════════════════════════════════════════════════════════
# _extract_handles_from_results (internal helper)
# ══════════════════════════════════════════════════════════════════════

class TestExtractHandlesFromResults:
    """Test parsing DDG result URLs for platform handles."""

    def test_ig_url_extracts_handle(self):
        results = [{"href": "https://www.instagram.com/alexleonidas/"}]
        handles = _extract_handles_from_results(results)
        assert len(handles) == 1
        assert handles[0].handle == "alexleonidas"
        assert handles[0].platform == "Instagram"

    def test_tt_url_extracts_handle(self):
        results = [{"href": "https://www.tiktok.com/@jeffnippard"}]
        handles = _extract_handles_from_results(results)
        assert len(handles) == 1
        assert handles[0].handle == "jeffnippard"
        assert handles[0].platform == "TikTok"

    def test_yt_url_extracts_handle(self):
        results = [{"href": "https://www.youtube.com/@JeffNippard"}]
        handles = _extract_handles_from_results(results)
        assert len(handles) == 1
        assert handles[0].platform == "YouTube"

    def test_non_platform_url_discards(self):
        results = [
            {"href": "https://www.menshealth.com/fitness/a123/best-form-tips/"},
            {"href": "https://en.wikipedia.org/wiki/Jeff_Nippard"},
        ]
        handles = _extract_handles_from_results(results)
        assert len(handles) == 0

    def test_multiple_platform_urls(self):
        """Multiple platform URLs with DIFFERENT handles should all be kept."""
        results = [
            {"href": "https://www.instagram.com/alexleonidas/"},
            {"href": "https://www.tiktok.com/@alex_leonidas_tiktok"},
            {"href": "https://www.youtube.com/@AlexLeoFitness"},
        ]
        handles = _extract_handles_from_results(results)
        # All three have different handle strings → all kept
        assert len(handles) == 3
        platforms = {h.platform for h in handles}
        assert "Instagram" in platforms
        assert "TikTok" in platforms
        assert "YouTube" in platforms

    def test_empty_results(self):
        assert _extract_handles_from_results([]) == []

    def test_missing_href(self):
        results = [{"title": "Some result", "body": "No href key"}]
        handles = _extract_handles_from_results(results)
        assert len(handles) == 0


# ══════════════════════════════════════════════════════════════════════
# resolve_names_via_ddg (full pipeline, mocked DDG)
# ══════════════════════════════════════════════════════════════════════

class TestResolveNamesViaDdg:
    """Test the full resolution pipeline with mocked DDG."""

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_resolves_name_to_ig_handle(self, mock_sleep, mock_ddgs_cls):
        """When DDG returns an Instagram URL, handle is extracted."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/alexleonidas/",
             "title": "Alex Leonidas (@alexleonidas) • Instagram"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        handles = resolve_names_via_ddg(["Alex Leonidas"], audit)

        assert len(handles) == 1
        assert handles[0].handle == "alexleonidas"
        assert handles[0].platform == "Instagram"
        assert handles[0].name == "Alex Leonidas"

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_no_platform_url_discards(self, mock_sleep, mock_ddgs_cls):
        """When DDG returns no platform URLs, name is discarded."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.wikipedia.org/wiki/United_States"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        handles = resolve_names_via_ddg(["United States"], audit)
        assert len(handles) == 0

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_deduplicates_across_names(self, mock_sleep, mock_ddgs_cls):
        """Same handle from different names shouldn't duplicate."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        handles = resolve_names_via_ddg(
            ["Jeff Nippard", "Jeffrey Nippard"], audit,
        )
        ig_handles = [h for h in handles if h.handle == "jeffnippard"]
        assert len(ig_handles) == 1

    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_rate_limiting_between_queries(self, mock_sleep, mock_ddgs_cls):
        """Rate-limit sleep (SEARCH_DELAY_SECONDS) should be called between queries (not after last)."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = []
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        resolve_names_via_ddg(["Name One", "Name Two", "Name Three"], audit)

        # Should have exactly 2 rate-limit sleeps (between 3 queries)
        from config import SEARCH_DELAY_SECONDS
        rate_limit_sleeps = [
            c for c in mock_sleep.call_args_list
            if c.args == (SEARCH_DELAY_SECONDS,)
        ]
        assert len(rate_limit_sleeps) == 2, (
            f"Expected 2 rate-limit sleeps, got {len(rate_limit_sleeps)} "
            f"(total sleeps: {mock_sleep.call_count})"
        )

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_empty_names_returns_empty(self, mock_sleep, mock_ddgs_cls):
        audit = _mock_audit()
        assert resolve_names_via_ddg([], audit) == []

    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_ddg_failure_handled_gracefully(self, mock_sleep, mock_ddgs_cls):
        """DDG exceptions shouldn't crash; name is simply skipped."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.side_effect = Exception("DDG rate limited")
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        # Should not raise, just return empty
        handles = resolve_names_via_ddg(["Some Name"], audit)
        assert len(handles) == 0

    @patch("services.extraction.NameResolver.SEARCH_BACKEND", "brave,google")
    @patch("services.extraction.NameResolver.SEARCH_REGION", "uk-en")
    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_backend_and_region_forwarded(self, mock_sleep, mock_ddgs_cls):
        """backend= and region= kwargs must be passed to DDGS.text()."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = [
            {"href": "https://www.instagram.com/testuser/",
             "title": "Test User Instagram"},
        ]
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        resolve_names_via_ddg(["Test User"], audit)

        _, kwargs = mock_ddgs.text.call_args
        assert kwargs["backend"] == "brave,google"
        assert kwargs["region"] == "uk-en"


# ══════════════════════════════════════════════════════════════════════
# Site-scoped DDG queries (item 2a)
# ══════════════════════════════════════════════════════════════════════

class TestSiteScopedQueries:
    """Verify DDG queries use site: prefix for better results."""

    def test_query_template_uses_site_prefix(self):
        """Query template should include site:instagram.com etc."""
        from services.extraction.NameResolver import _QUERY_TEMPLATE
        assert "site:instagram.com" in _QUERY_TEMPLATE
        assert "site:tiktok.com" in _QUERY_TEMPLATE
        assert "site:youtube.com" in _QUERY_TEMPLATE

    @patch("services.extraction.NameResolver.NAME_DDG_MAX_RETRIES", 0)
    @patch("services.extraction.NameResolver.DDGS")
    @patch("services.extraction.NameResolver.time.sleep")
    def test_query_contains_name_and_site(self, mock_sleep, mock_ddgs_cls):
        """Actual DDG query should contain the name and site: prefixes."""
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = []
        mock_ddgs_cls.return_value = mock_ddgs

        audit = _mock_audit()
        resolve_names_via_ddg(["Jeff Nippard"], audit, category="Fitness")

        call_args = mock_ddgs.text.call_args
        query = call_args.args[0] if call_args.args else call_args.kwargs.get("keywords", "")
        assert "Jeff Nippard" in query
        assert "site:" in query


# ══════════════════════════════════════════════════════════════════════
# DDG_ZERO_RETRIES reduction (item 2d)
# ══════════════════════════════════════════════════════════════════════

class TestRetryReduction:
    """Verify NAME_DDG_MAX_RETRIES provides ≥5 total tries."""

    def test_max_retries_is_four(self):
        from services.extraction.NameResolver import NAME_DDG_MAX_RETRIES
        assert NAME_DDG_MAX_RETRIES == 4  # 5 total tries

    def test_total_tries_at_least_five(self):
        """Total tries = NAME_DDG_MAX_RETRIES + 1 >= 5."""
        from services.extraction.NameResolver import NAME_DDG_MAX_RETRIES
        total = NAME_DDG_MAX_RETRIES + 1
        assert total >= 5, f"Total tries {total} < 5"


# ══════════════════════════════════════════════════════════════════════
# Confidence check (existing behavior — regression)
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# _score_result priority scoring (item B3)
# ══════════════════════════════════════════════════════════════════════

class TestScoreResult:
    """Test DDG result priority scoring."""

    def test_profile_page_scores_higher_than_post(self):
        """Profile page URL should score higher than post/reel URLs."""
        profile_handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        post_handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")

        profile_score = _score_result(
            "https://www.instagram.com/jeffnippard/",
            profile_handle, "Jeff Nippard",
        )
        post_score = _score_result(
            "https://www.instagram.com/p/ABC123/",
            post_handle, "Jeff Nippard",
        )
        assert profile_score > post_score

    def test_reel_url_penalized(self):
        """Reel URLs should be penalized."""
        handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        reel_score = _score_result(
            "https://www.instagram.com/reel/ABC123/",
            handle, "Jeff Nippard",
        )
        profile_score = _score_result(
            "https://www.instagram.com/jeffnippard/",
            handle, "Jeff Nippard",
        )
        assert profile_score > reel_score

    def test_shorts_url_penalized(self):
        """YouTube Shorts URLs should be penalized."""
        handle = ExtractedHandle(handle="jeffnippard", platform="YouTube")
        shorts_score = _score_result(
            "https://www.youtube.com/shorts/ABC123",
            handle, "Jeff Nippard",
        )
        profile_score = _score_result(
            "https://www.youtube.com/@jeffnippard",
            handle, "Jeff Nippard",
        )
        assert profile_score > shorts_score

    def test_name_in_handle_bonus(self):
        """Handle matching name words gets a bonus."""
        matching = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        random = ExtractedHandle(handle="xyz_random_user", platform="Instagram")

        matching_score = _score_result(
            "https://www.instagram.com/jeffnippard/",
            matching, "Jeff Nippard",
        )
        random_score = _score_result(
            "https://www.instagram.com/xyz_random_user/",
            random, "Jeff Nippard",
        )
        assert matching_score > random_score

    def test_empty_name_no_crash(self):
        """Empty candidate name should not crash."""
        handle = ExtractedHandle(handle="someone", platform="Instagram")
        score = _score_result(
            "https://www.instagram.com/someone/",
            handle, "",
        )
        assert score >= 0

    def test_sorted_results_profile_first(self):
        """_extract_handles_from_results should return profile page first."""
        results = [
            {"href": "https://www.instagram.com/p/POST123/",
             "title": "Jeff Nippard post"},
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard)"},
        ]
        handles = _extract_handles_from_results(results, candidate_name="Jeff Nippard")
        assert len(handles) >= 1
        assert handles[0].handle == "jeffnippard"


class TestConfidenceCheck:
    """Ensure name-word overlap check works correctly."""

    def test_rejects_wrong_name_in_title(self):
        """DDG result for 'John Smith' returning 'Matilda Djerf' profile should be rejected."""
        results = [
            {"href": "https://www.instagram.com/matildadjerf/",
             "title": "Matilda Djerf (@matildadjerf) • Instagram",
             "body": "Fashion influencer"},
        ]
        handles = _extract_handles_from_results(results, candidate_name="John Smith")
        assert len(handles) == 0

    def test_accepts_matching_name_in_title(self):
        """DDG result with matching name should be accepted."""
        results = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard) • Instagram",
             "body": "Fitness YouTuber and coach"},
        ]
        handles = _extract_handles_from_results(results, candidate_name="Jeff Nippard")
        assert len(handles) == 1
        assert handles[0].handle == "jeffnippard"

