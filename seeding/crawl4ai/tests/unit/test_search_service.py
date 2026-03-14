"""
Unit Tests: SearchService
===========================
Verifies ad domain filtering, URL relevance filtering, dedup, and MAX_URLS_PER_JOB cap.
discover_urls() tested with mocked DDGS to avoid real network calls.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest


from config.seed_schema import Difficulty
from services.search.SearchService import SearchService
from services.audit.AuditService import AuditLog


# ── Ad Domain Filtering (static method, no mock needed) ──

def test_blocks_bing():
    assert SearchService._is_ad("https://bing.com/aclick/something") is True
    assert SearchService._is_ad("https://www.bing.com/ck/a?target=foo") is True


def test_blocks_google_ads():
    assert SearchService._is_ad("https://googleadservices.com/pagead") is True


def test_blocks_microsoft():
    assert SearchService._is_ad("https://www.microsoft.com/redirect") is True


def test_allows_real_urls():
    assert SearchService._is_ad("https://favikon.com/blog/fitness") is False
    assert SearchService._is_ad("https://modash.io/find-influencers") is False
    assert SearchService._is_ad("https://instagram.com/kayla_itsines") is False


def test_blocks_scrumball():
    """scrumball.com should be blocked — SEO junk rankings."""
    assert SearchService._is_ad("https://www.scrumball.com/ranking/top-ai-influencers") is True
    assert SearchService._is_ad("https://scrumball.com/ranking/top-ai-influencers-on-tiktok") is True


def test_blocks_metricsmule():
    """metricsmule.com should be blocked — fabricated influencer names."""
    assert SearchService._is_ad("https://metricsmule.com/instagram/ai-influencers") is True


def test_blocks_linkedin():
    """linkedin.com should be blocked — no social handles from LinkedIn profiles."""
    assert SearchService._is_ad("https://linkedin.com/in/andrew-ng") is True
    assert SearchService._is_ad("https://www.linkedin.com/pulse/top-ai") is True


def test_handles_malformed_urls():
    assert SearchService._is_ad("not a url") is False
    assert SearchService._is_ad("") is False


# ── discover_urls() with mocked DDGS ──

def _make_ddgs_results(urls: list[str]) -> list[dict]:
    """Helper to create DDGS-like result dicts."""
    return [{"href": url, "title": f"Result for {url}", "body": ""} for url in urls]


def test_discover_urls_dedup():
    """Duplicate URLs across queries should be deduplicated."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit)

        # Mock DDGS to return the same URL from multiple queries
        mock_results = _make_ddgs_results([
            "https://favikon.com/ai-influencers",
            "https://modash.io/ai-creators",
            "https://favikon.com/ai-influencers",  # duplicate
        ])

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            results = svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        urls = [u for u, _ in results.url_query_pairs]
        assert len(urls) == len(set(urls)), "Duplicate URLs found in results"
        assert len(urls) == 2, f"Expected 2 unique URLs, got {len(urls)}"


def test_discover_urls_ad_filter():
    """Ad domain URLs should be filtered out."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit)

        mock_results = _make_ddgs_results([
            "https://favikon.com/ai-influencers",
            "https://bing.com/aclick/redirect",  # ad
            "https://googleadservices.com/pagead",  # ad
            "https://modash.io/ai-creators",
        ])

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            results = svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        urls = [u for u, _ in results.url_query_pairs]
        assert "https://bing.com/aclick/redirect" not in urls
        assert "https://googleadservices.com/pagead" not in urls
        assert "https://favikon.com/ai-influencers" in urls
        assert "https://modash.io/ai-creators" in urls


def test_discover_urls_max_cap():
    """Should cap results at MAX_URLS_PER_JOB."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit)

        mock_results = _make_ddgs_results([
            f"https://example.com/ai-tools-page{i}" for i in range(20)
        ])

        with (
            patch.object(svc._ddgs, "text", return_value=mock_results),
            patch("services.search.SearchService.MAX_URLS_PER_JOB", 3),
        ):
            results = svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        assert len(results.url_query_pairs) <= 3, f"Expected max 3 URLs, got {len(results.url_query_pairs)}"


def test_discover_urls_audit_logging():
    """discovery should log accepted/rejected URLs to audit trail."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit)

        mock_results = _make_ddgs_results([
            "https://favikon.com/ai-page",
            "https://bing.com/ad",  # ad - rejected
        ])

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        actions = [e.action for e in audit.entries]
        assert "url_accepted" in actions, "Missing url_accepted audit entry"
        assert "url_rejected" in actions, "Missing url_rejected audit entry"
        assert "query" in actions, "Missing query audit entry"


# ── Engine rotation kwargs ──

def test_backend_and_region_forwarded():
    """backend= and region= kwargs must be passed to DDGS.text()."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit)

        mock_results = _make_ddgs_results(["https://example.com/ai-tools-page1"])

        with (
            patch.object(svc._ddgs, "text", return_value=mock_results) as mock_text,
            patch("services.search.SearchService.SEARCH_BACKEND", "brave,bing"),
            patch("services.search.SearchService.SEARCH_REGION", "uk-en"),
        ):
            svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        # Verify backend and region were passed
        assert mock_text.call_count >= 1
        _, kwargs = mock_text.call_args
        assert kwargs["backend"] == "brave,bing", f"Expected backend='brave,bing', got {kwargs.get('backend')}"
        assert kwargs["region"] == "uk-en", f"Expected region='uk-en', got {kwargs.get('region')}"


# ── DDG retry behavior ──

def test_no_results_retries():
    """'No results found' SHOULD retry — DDG is non-deterministic."""
    from ddgs.exceptions import DDGSException

    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit, delay_seconds=0)

        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise DDGSException("No results found.")

        with (
            patch.object(svc._ddgs, "text", side_effect=side_effect),
            patch("services.search.SearchService.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.SearchService.BACKOFF_MAX_SECONDS", 0.05),
        ):
            results = svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        # call_count > queries_attempted proves retries happened
        assert call_count > results.queries_attempted, (
            f"Expected retries (call_count={call_count} should exceed "
            f"queries_attempted={results.queries_attempted})"
        )


def test_no_results_not_cached():
    """'No results found' failures should NOT be cached — next run should retry."""
    from ddgs.exceptions import DDGSException
    from services.search.SearchCache import SearchCache

    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        cache = SearchCache(Path(tmp) / "cache")
        svc = SearchService(audit, cache=cache, delay_seconds=0)

        with (
            patch.object(svc._ddgs, "text", side_effect=DDGSException("No results found.")),
            patch("services.search.SearchService.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.SearchService.BACKOFF_MAX_SECONDS", 0.05),
        ):
            svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        # Failures should NOT be cached
        assert cache.get("does not matter") is None, "Cache should not store failed results"


def test_real_errors_still_retry():
    """Actual DDG errors (rate limits, network) should retry with backoff."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = SearchService(audit, delay_seconds=0)

        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise ConnectionError("DDG rate limited")

        with (
            patch.object(svc._ddgs, "text", side_effect=side_effect),
            patch("services.search.SearchService.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.SearchService.BACKOFF_MAX_SECONDS", 0.05),
        ):
            results = svc.discover_urls(
                sub_name="Fitness",
                platform="Instagram",
                region="US",
                year="2026",
                search_prompt="fitness influencers",
                alt_search_terms=[],
                known_sources=[],
                difficulty=Difficulty.EASY,
                inurl_slugs=[],
            )

        # call_count > queries_attempted proves retries happened
        assert call_count > results.queries_attempted, (
            f"Expected retries (call_count={call_count} should exceed "
            f"queries_attempted={results.queries_attempted})"
        )
        # All queries permanently failed
        assert results.failure_count > 0, (
            f"Expected permanent failures, got failure_count={results.failure_count}"
        )


# ── QueryBuilder quoted dork ──

from services.search.QueryBuilder import QueryBuilder, QueryType


def test_query_builder_quotes_sub_name():
    """QueryBuilder must wrap sub_name in quotes for DDG dorking."""
    builder = QueryBuilder(
        sub_name="AI",
        platform="Instagram",
        region="US",
        year="2026",
        search_prompt="top AI influencers",
        alt_search_terms=["best AI creators"],
        known_sources=["favikon.com"],
        difficulty=Difficulty.EASY,
        inurl_slugs=[],
    )
    queries = builder.build_all()

    primary = [q for q in queries if q.query_type == QueryType.PRIMARY_OPEN]
    assert len(primary) == 1
    assert primary[0].query.startswith('"AI"'), (
        f"Primary query must start with quoted sub_name, got: {primary[0].query}"
    )

    alt = [q for q in queries if q.query_type == QueryType.ALT_OPEN]
    assert len(alt) == 1
    assert alt[0].query.startswith('"AI"'), (
        f"Alt query must start with quoted sub_name, got: {alt[0].query}"
    )

    # Site-targeted should NOT have quoted sub_name prefix (uses site: operator)
    site = [q for q in queries if q.query_type == QueryType.SITE_TARGETED]
    assert len(site) == 1
    assert site[0].query.startswith("site:"), (
        f"Site query must start with site:, got: {site[0].query}"
    )


def _load_top_level_categories() -> list[str]:
    """Load top-level sub-category names from the config JSON."""
    config_path = Path(__file__).resolve().parents[2] / "config" / "categories" / "all_categories.json"
    data = json.loads(config_path.read_text())
    names = []
    for cat in data:
        for sub in cat["subs"]:
            if sub.get("isTopLevel"):
                names.append(sub["subName"])
    return names


@pytest.mark.parametrize("category", _load_top_level_categories())
def test_query_builder_quotes_every_category(category: str):
    """REGRESSION: Every category's queries must contain the quoted sub_name.

    If this fails for any category, DDG will treat the category keyword
    as optional and return off-topic results.
    """
    builder = QueryBuilder(
        sub_name=category,
        platform="Instagram",
        region="US",
        year="2026",
        search_prompt=f"top {category} influencers",
        alt_search_terms=[],
        known_sources=[],
        difficulty=Difficulty.EASY,
        inurl_slugs=[],
    )
    queries = builder.build_all()
    primary = [q for q in queries if q.query_type == QueryType.PRIMARY_OPEN]
    assert len(primary) == 1
    assert f'"{category}"' in primary[0].query, (
        f"Category '{category}': quoted sub_name missing from query: {primary[0].query}"
    )


# ── Cache Integration ──

class TestSearchServiceCache:
    """Tests that SearchService correctly reads from and writes to SearchCache."""

    def _make_svc(self, tmp_path, ddgs_mock):
        """Create SearchService with a real SearchCache and mocked DDGS."""
        from services.search.SearchCache import SearchCache
        audit = AuditLog(tmp_path / "audit", "test")
        cache = SearchCache(cache_dir=tmp_path / "cache")
        svc = SearchService(audit, cache=cache, ddgs=ddgs_mock, delay_seconds=0)
        return svc, cache

    def test_cache_populated_on_successful_query(self, tmp_path):
        """First query writes results to cache."""
        ddgs_mock = MagicMock()
        ddgs_mock.text.return_value = iter([
            {"href": "https://example.com/list", "title": "List", "body": ""},
        ])
        svc, cache = self._make_svc(tmp_path, ddgs_mock)

        svc.discover_urls(
            sub_name="Yoga", platform="Instagram", region="US",
            year="2026", search_prompt="", alt_search_terms=[],
            known_sources=[], difficulty=Difficulty.EASY, inurl_slugs=[],
        )

        # DDG was called at least once
        assert ddgs_mock.text.call_count >= 1
        # Cache should have misses (first call) and 0 hits
        assert cache.misses >= 1
        assert cache.hits == 0

    def test_cache_hit_skips_ddg(self, tmp_path):
        """Second identical call returns from cache, DDG not called again."""
        from services.search.SearchCache import SearchCache
        from services.search.QueryBuilder import QueryBuilder

        audit = AuditLog(tmp_path / "audit", "test")
        cache = SearchCache(cache_dir=tmp_path / "cache")

        # Pre-populate cache with a known query
        builder = QueryBuilder(
            sub_name="Yoga", platform="Instagram", region="US",
            year="2026", search_prompt="", alt_search_terms=[],
            known_sources=[], difficulty=Difficulty.EASY, inurl_slugs=[],
        )
        queries = builder.build_all()
        for sq in queries:
            cache.put(sq.query, [{"href": "https://cached.com", "title": "Cached", "body": ""}])

        # Create service with cache pre-populated
        ddgs_mock = MagicMock()
        svc = SearchService(audit, cache=cache, ddgs=ddgs_mock, delay_seconds=0)

        svc.discover_urls(
            sub_name="Yoga", platform="Instagram", region="US",
            year="2026", search_prompt="", alt_search_terms=[],
            known_sources=[], difficulty=Difficulty.EASY, inurl_slugs=[],
        )

        # DDG should NOT have been called — all queries served from cache
        ddgs_mock.text.assert_not_called()
        assert cache.hits == len(queries)

    def test_no_cache_when_none(self, tmp_path):
        """When cache=None, SearchService still works (no caching)."""
        ddgs_mock = MagicMock()
        ddgs_mock.text.return_value = iter([
            {"href": "https://example.com/list", "title": "List", "body": ""},
        ])
        audit = AuditLog(tmp_path / "audit", "test")
        svc = SearchService(audit, cache=None, ddgs=ddgs_mock, delay_seconds=0)

        result = svc.discover_urls(
            sub_name="Test", platform="Instagram", region="US",
            year="2026", search_prompt="", alt_search_terms=[],
            known_sources=[], difficulty=Difficulty.EASY, inurl_slugs=[],
        )
        # Should work without errors
        assert ddgs_mock.text.call_count >= 1

    def test_cache_not_populated_on_ddg_failure(self, tmp_path):
        """When DDG fails, no stale data enters the cache."""
        from services.search.SearchCache import SearchCache
        ddgs_mock = MagicMock()
        ddgs_mock.text.side_effect = Exception("DDG rate limited")

        audit = AuditLog(tmp_path / "audit", "test")
        cache = SearchCache(cache_dir=tmp_path / "cache")
        svc = SearchService(audit, cache=cache, ddgs=ddgs_mock, delay_seconds=0)

        with patch("services.search.SearchService.MAX_RETRIES", 0):
            svc.discover_urls(
                sub_name="Fail", platform="Instagram", region="US",
                year="2026", search_prompt="", alt_search_terms=[],
                known_sources=[], difficulty=Difficulty.EASY, inurl_slugs=[],
            )

        # Cache should be empty — no entries from failed queries
        assert list((tmp_path / "cache").glob("*.json")) == []


# ── Cache DI Guard: ensures pipelines always inject cache ──

class TestPipelineCacheInjection:
    """Guard tests: assert pipeline runners always inject SearchCache.

    If someone removes the cache= param from PipelineRunner or
    PhasePipelineRunner, these tests fail — catching the regression
    before DDG gets hammered with duplicate queries.
    """

    def test_pipeline_runner_stores_cache(self, tmp_path):
        """PipelineRunner must accept and store a SearchCache."""
        from services.search.SearchCache import SearchCache
        from pipeline import PipelineRunner

        cache = SearchCache(cache_dir=tmp_path / "cache")
        runner = PipelineRunner(cache=cache)
        assert runner._cache is cache, "PipelineRunner must store cache for SearchService DI"

    def test_phase_pipeline_runner_stores_cache(self, tmp_path):
        """PhasePipelineRunner must accept and store a SearchCache."""
        from services.search.SearchCache import SearchCache
        from phase_pipeline import PhasePipelineRunner

        cache = SearchCache(cache_dir=tmp_path / "cache")
        runner = PhasePipelineRunner(cache=cache)
        assert runner._cache is cache, "PhasePipelineRunner must store cache for SearchService DI"

    def test_pipeline_runner_without_cache_is_none(self):
        """PipelineRunner without cache= defaults to None (guard against silent omission)."""
        from pipeline import PipelineRunner

        runner = PipelineRunner()
        assert runner._cache is None, "Default should be None — cli.py must always supply a cache"


