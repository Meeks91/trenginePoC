"""
Unit tests for NameResolver — search client-based name → handle resolution.

All search_client calls are mocked to avoid external network dependencies.
"""

from unittest.mock import MagicMock

from services.extraction.NameResolver import (
    resolve_names_via_ddg,
    _extract_handles_from_results,
    _score_result,
)
from services.extraction.RegexHandleExtractor import ExtractedHandle


# Fixtures:

def _mock_audit() -> MagicMock:
    audit = MagicMock()
    audit.log = MagicMock()
    return audit


def _mock_search_client(results: list[dict] | None = None) -> MagicMock:
    """Create a SearchClient mock that returns fixed search_text results."""
    client = MagicMock()
    client.search_text.return_value = results if results is not None else []
    client.nr_query_template.return_value = '{name} Instagram YouTube TikTok'
    return client

# Fixtures


# ══════════════════════════════════════════════════════════════════════
# _extract_handles_from_results (internal helper)
# ══════════════════════════════════════════════════════════════════════

class TestExtractHandlesFromResults:
    """Test parsing search result URLs for platform handles."""

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
# resolve_names_via_ddg (full pipeline, mocked search client)
# ══════════════════════════════════════════════════════════════════════

class TestResolveNamesViaDdg:
    """Test the full resolution pipeline with mocked search client."""

    def test_resolves_name_to_ig_handle(self):
        """When client returns an Instagram URL, handle is extracted."""
        client = _mock_search_client(results=[
            {"href": "https://www.instagram.com/alexleonidas/",
             "title": "Alex Leonidas (@alexleonidas) • Instagram"},
        ])
        audit = _mock_audit()

        handles = resolve_names_via_ddg(
            ["Alex Leonidas"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        )

        assert len(handles) == 1
        assert handles[0].handle == "alexleonidas"
        assert handles[0].platform == "Instagram"
        assert handles[0].name == "Alex Leonidas"

    def test_no_platform_url_discards(self):
        """When client returns no platform URLs, name is discarded."""
        client = _mock_search_client(results=[
            {"href": "https://www.wikipedia.org/wiki/United_States"},
        ])
        audit = _mock_audit()

        handles = resolve_names_via_ddg(
            ["United States"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        )
        assert len(handles) == 0

    def test_deduplicates_across_names(self):
        """Same handle from different names shouldn't duplicate."""
        client = _mock_search_client(results=[
            {"href": "https://www.instagram.com/jeffnippard/"},
        ])
        audit = _mock_audit()

        handles = resolve_names_via_ddg(
            ["Jeff Nippard", "Jeffrey Nippard"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        )
        ig_handles = [h for h in handles if h.handle == "jeffnippard"]
        assert len(ig_handles) == 1

    def test_empty_names_returns_empty(self):
        client = _mock_search_client()
        audit = _mock_audit()

        assert resolve_names_via_ddg(
            [], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        ) == []

    def test_client_failure_returns_empty(self):
        """Client returning [] shouldn't crash; name is simply skipped."""
        client = _mock_search_client(results=[])
        audit = _mock_audit()

        handles = resolve_names_via_ddg(
            ["Some Name"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        )
        assert len(handles) == 0

    def test_injected_template_formats_query(self):
        """query_template param is used to format the actual query."""
        client = _mock_search_client(results=[])
        audit = _mock_audit()

        resolve_names_via_ddg(
            ["Jeff Nippard"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
            category="Fitness",
        )

        call_args = client.search_text.call_args
        query = call_args.args[0] if call_args.args else call_args.kwargs.get("query", "")
        assert "Jeff Nippard" in query
        assert "Instagram" in query
        assert "site:" not in query

    def test_strict_template_formats_with_site(self):
        """When using strict template, query should contain site: prefixes."""
        client = _mock_search_client(results=[])
        audit = _mock_audit()

        resolve_names_via_ddg(
            ["Jeff Nippard"], audit,
            search_client=client,
            query_template='{name} {category} site:instagram.com OR site:tiktok.com OR site:youtube.com',
            category="Fitness",
        )

        call_args = client.search_text.call_args
        query = call_args.args[0] if call_args.args else call_args.kwargs.get("query", "")
        assert "Jeff Nippard" in query
        assert "site:instagram.com" in query

    def test_search_client_is_invoked(self):
        """resolve_names_via_ddg must call search_client.search_text for each name."""
        client = _mock_search_client(results=[])
        audit = _mock_audit()

        resolve_names_via_ddg(
            ["Name One", "Name Two"], audit,
            search_client=client,
            query_template='{name} Instagram YouTube TikTok',
        )

        assert client.search_text.call_count == 2


# ══════════════════════════════════════════════════════════════════════
# Polymorphic NR query templates
# ══════════════════════════════════════════════════════════════════════

class TestPolymorphicQueryTemplate:
    """Verify SearchClient implementations return correct NR templates."""

    def test_strict_client_uses_site_scoping(self):
        """StrictSearchClient template contains site: prefixes for Google."""
        from services.search.StrictSearchClient import StrictSearchClient
        client = StrictSearchClient(MagicMock(), api_key="fake")
        template = client.nr_query_template()
        assert "site:instagram.com" in template
        assert "site:tiktok.com" in template
        assert "site:youtube.com" in template
        assert "{name}" in template

    def test_open_client_uses_platform_keywords(self):
        """OpenSearchClient template uses platform names (no site: scoping)."""
        from services.search.OpenSearchClient import OpenSearchClient
        client = OpenSearchClient(MagicMock())
        template = client.nr_query_template()
        assert "site:" not in template
        assert "Instagram" in template
        assert "YouTube" in template
        assert "TikTok" in template
        assert "{name}" in template


# ══════════════════════════════════════════════════════════════════════
# NAME_DDG_MAX_RETRIES (kept for compatibility)
# ══════════════════════════════════════════════════════════════════════

class TestRetryConstant:
    """Verify NAME_DDG_MAX_RETRIES constant is kept for interface compatibility."""

    def test_max_retries_is_four(self):
        from services.extraction.NameResolver import NAME_DDG_MAX_RETRIES
        assert NAME_DDG_MAX_RETRIES == 4

    def test_total_tries_at_least_five(self):
        from services.extraction.NameResolver import NAME_DDG_MAX_RETRIES
        total = NAME_DDG_MAX_RETRIES + 1
        assert total >= 5


# ══════════════════════════════════════════════════════════════════════
# _score_result priority scoring
# ══════════════════════════════════════════════════════════════════════

class TestScoreResult:
    """Test search result priority scoring."""

    def test_profile_page_scores_higher_than_post(self):
        profile_handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        post_handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")

        profile_score = _score_result(
            "https://www.instagram.com/jeffnippard/", profile_handle, "Jeff Nippard",
        )
        post_score = _score_result(
            "https://www.instagram.com/p/ABC123/", post_handle, "Jeff Nippard",
        )
        assert profile_score > post_score

    def test_reel_url_penalized(self):
        handle = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        reel_score = _score_result(
            "https://www.instagram.com/reel/ABC123/", handle, "Jeff Nippard",
        )
        profile_score = _score_result(
            "https://www.instagram.com/jeffnippard/", handle, "Jeff Nippard",
        )
        assert profile_score > reel_score

    def test_shorts_url_penalized(self):
        handle = ExtractedHandle(handle="jeffnippard", platform="YouTube")
        shorts_score = _score_result(
            "https://www.youtube.com/shorts/ABC123", handle, "Jeff Nippard",
        )
        profile_score = _score_result(
            "https://www.youtube.com/@jeffnippard", handle, "Jeff Nippard",
        )
        assert profile_score > shorts_score

    def test_name_in_handle_bonus(self):
        matching = ExtractedHandle(handle="jeffnippard", platform="Instagram")
        random = ExtractedHandle(handle="xyz_random_user", platform="Instagram")

        matching_score = _score_result(
            "https://www.instagram.com/jeffnippard/", matching, "Jeff Nippard",
        )
        random_score = _score_result(
            "https://www.instagram.com/xyz_random_user/", random, "Jeff Nippard",
        )
        assert matching_score > random_score

    def test_empty_name_no_crash(self):
        handle = ExtractedHandle(handle="someone", platform="Instagram")
        score = _score_result(
            "https://www.instagram.com/someone/", handle, "",
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
        """Result for 'John Smith' returning 'Matilda Djerf' profile should be rejected."""
        results = [
            {"href": "https://www.instagram.com/matildadjerf/",
             "title": "Matilda Djerf (@matildadjerf) • Instagram",
             "body": "Fashion influencer"},
        ]
        handles = _extract_handles_from_results(results, candidate_name="John Smith")
        assert len(handles) == 0

    def test_accepts_matching_name_in_title(self):
        """Result with matching name should be accepted."""
        results = [
            {"href": "https://www.instagram.com/jeffnippard/",
             "title": "Jeff Nippard (@jeffnippard) • Instagram",
             "body": "Fitness YouTuber and coach"},
        ]
        handles = _extract_handles_from_results(results, candidate_name="Jeff Nippard")
        assert len(handles) == 1
        assert handles[0].handle == "jeffnippard"
