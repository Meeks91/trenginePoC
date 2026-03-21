"""
Unit Tests: OpenSearchClient
==============================
Verifies query building for DDG-backed search client.
Tests use mocked DDGS to avoid real network calls.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from config.seed_schema import (
    Difficulty, Platform, Region, RegionCode, SubCategory, SeedJob,
)
from services.audit.AuditService import AuditLog
from services.search.OpenSearchClient import OpenSearchClient
from services.search.SearchClient import QueryType
from services.search.SearchCache import SearchCache


# ── Helpers ──

def _make_job(**overrides) -> SeedJob:
    """Create a minimal SeedJob for testing."""
    sub = SubCategory(
        sub_name=overrides.pop("sub_name", "Fitness"),
        search_prompt=overrides.pop("search_prompt", "top fitness influencers"),
        alt_search_terms=overrides.pop("alt_search_terms", ["best gym creators"]),
        known_sources=overrides.pop("known_sources", ["favikon.com"]),
        difficulty=overrides.pop("difficulty", Difficulty.EASY),
        strict_slugs=overrides.pop("strict_slugs", []),
        is_top_level=True,
        platform_notes="",
        region_notes="",
    )
    return SeedJob(
        platform=overrides.pop("platform", Platform.Instagram),
        region=overrides.pop("region", Region(code=RegionCode.US, language="en", label="United States")),
        category_key=overrides.pop("category_key", "FITNESS"),
        sub=sub,
        year=overrides.pop("year", "2026"),
    )


def _make_client(tmp_path: Path, ddgs_mock: MagicMock) -> OpenSearchClient:
    """Create OpenSearchClient with mocked DDGS."""
    audit = AuditLog(tmp_path / "audit", "test")
    return OpenSearchClient(audit, ddgs=ddgs_mock, delay_seconds=0)


# ── Query Building ──

class TestQueryBuilding:
    """Verify query generation for all query types."""

    def test_primary_open_quotes_sub_name(self, tmp_path):
        """Primary query must wrap sub_name in quotes."""
        ddgs = MagicMock()
        ddgs.text.return_value = []
        client = _make_client(tmp_path, ddgs)
        job = _make_job(sub_name="AI", alt_search_terms=[], known_sources=[])

        queries = client._build_queries(job)
        primary = [q for q in queries if q.query_type == QueryType.PRIMARY_OPEN]

        assert len(primary) == 1
        assert primary[0].query.startswith('"AI"'), (
            f"Primary query must start with quoted sub_name, got: {primary[0].query}"
        )

    def test_alt_open_quotes_sub_name(self, tmp_path):
        """Alt queries must wrap sub_name in quotes."""
        ddgs = MagicMock()
        ddgs.text.return_value = []
        client = _make_client(tmp_path, ddgs)
        job = _make_job(sub_name="AI", alt_search_terms=["best AI creators"], known_sources=[])

        queries = client._build_queries(job)
        alt = [q for q in queries if q.query_type == QueryType.ALT_OPEN]

        assert len(alt) == 1
        assert alt[0].query.startswith('"AI"'), (
            f"Alt query must start with quoted sub_name, got: {alt[0].query}"
        )

    def test_site_targeted_uses_site_operator(self, tmp_path):
        """Site queries must start with site: operator."""
        ddgs = MagicMock()
        ddgs.text.return_value = []
        client = _make_client(tmp_path, ddgs)
        job = _make_job(alt_search_terms=[], known_sources=["favikon.com"])

        queries = client._build_queries(job)
        site = [q for q in queries if q.query_type == QueryType.SITE_TARGETED]

        assert len(site) == 1
        assert site[0].query.startswith("site:favikon.com"), (
            f"Site query must start with site:, got: {site[0].query}"
        )

    def test_query_count(self, tmp_path):
        """Total queries = 1 primary + N alt + M site."""
        ddgs = MagicMock()
        ddgs.text.return_value = []
        client = _make_client(tmp_path, ddgs)
        job = _make_job(
            alt_search_terms=["term1", "term2"],
            known_sources=["favikon.com", "modash.io"],
        )

        queries = client._build_queries(job)
        assert len(queries) == 5, f"Expected 1+2+2=5, got {len(queries)}"

    def test_no_inurl_in_queries(self, tmp_path):
        """DDG client should never use inurl: operator."""
        ddgs = MagicMock()
        ddgs.text.return_value = []
        client = _make_client(tmp_path, ddgs)
        job = _make_job(strict_slugs=["fitness", "workout"])

        queries = client._build_queries(job)
        for q in queries:
            assert "inurl:" not in q.query, f"DDG query must not use inurl:, got: {q.query}"


# ── Regression: every category quotes sub_name ──

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
def test_every_category_quotes_sub_name(category: str, tmp_path):
    """REGRESSION: Every category's primary query must contain quoted sub_name."""
    ddgs = MagicMock()
    ddgs.text.return_value = []
    client = _make_client(tmp_path, ddgs)
    job = _make_job(sub_name=category, search_prompt=f"top {category} influencers")

    queries = client._build_queries(job)
    primary = [q for q in queries if q.query_type == QueryType.PRIMARY_OPEN]

    assert len(primary) == 1
    assert f'"{category}"' in primary[0].query, (
        f"Category '{category}': quoted sub_name missing from query: {primary[0].query}"
    )


# ── Retry and Cache ──

class TestRetryAndCache:
    """Verify DDG retry logic and cache integration."""

    def test_retries_on_ddg_error(self, tmp_path):
        """DDG errors should trigger retries."""
        ddgs = MagicMock()
        call_count = 0
        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            raise ConnectionError("DDG rate limited")

        ddgs.text.side_effect = side_effect
        client = _make_client(tmp_path, ddgs)
        job = _make_job(alt_search_terms=[], known_sources=[])

        with (
            patch("services.search.OpenSearchClient.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.OpenSearchClient.BACKOFF_MAX_SECONDS", 0.05),
        ):
            _results = client.search(job)

        assert call_count > 1, f"Expected retries, got {call_count} calls"

    def test_cache_hit_skips_ddg(self, tmp_path):
        """Cached results should skip DDG call."""
        audit = AuditLog(tmp_path / "audit", "test")
        cache = SearchCache(cache_dir=tmp_path / "cache")
        ddgs = MagicMock()
        client = OpenSearchClient(audit, cache=cache, ddgs=ddgs, delay_seconds=0)

        job = _make_job(alt_search_terms=[], known_sources=[])
        queries = client._build_queries(job)
        for sq in queries:
            cache.put(sq.query, [{"href": "https://cached.com", "title": "Cached", "body": ""}])

        _results = client.search(job)

        ddgs.text.assert_not_called()
        assert cache.hits == len(queries)

    def test_failed_queries_not_cached(self, tmp_path):
        """Failed DDG queries should NOT be cached."""
        audit = AuditLog(tmp_path / "audit", "test")
        cache = SearchCache(cache_dir=tmp_path / "cache")
        ddgs = MagicMock()
        ddgs.text.side_effect = Exception("DDG down")
        client = OpenSearchClient(audit, cache=cache, ddgs=ddgs, delay_seconds=0)

        job = _make_job(alt_search_terms=[], known_sources=[])
        with (
            patch("services.search.OpenSearchClient.MAX_RETRIES", 0),
            patch("services.search.OpenSearchClient.BACKOFF_BASE_SECONDS", 0.01),
        ):
            client.search(job)

        assert list((tmp_path / "cache").glob("*.json")) == []


# ── search_text ──

class TestSearchText:
    """Verify search_text delegates to DDGS.text and retries on failure."""

    def test_search_text_returns_results_on_success(self, tmp_path):
        """search_text returns raw dicts from DDGS.text."""
        ddgs = MagicMock()
        ddgs.text.return_value = [
            {"href": "https://www.instagram.com/jeffnippard/", "title": "Jeff Nippard", "body": "Fitness"},
        ]
        client = _make_client(tmp_path, ddgs)

        results = client.search_text("Jeff Nippard instagram.com", max_results=2)

        assert len(results) == 1
        assert results[0]["href"] == "https://www.instagram.com/jeffnippard/"
        _, kwargs = ddgs.text.call_args
        assert kwargs["max_results"] == 2

    def test_search_text_retries_on_exception(self, tmp_path):
        """search_text re-attempts DDGS.text on transient errors."""
        ddgs = MagicMock()
        ddgs.text.side_effect = ConnectionError("DDG down")
        client = _make_client(tmp_path, ddgs)

        with (
            patch("services.search.OpenSearchClient.MAX_RETRIES", 2),
            patch("services.search.OpenSearchClient.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.OpenSearchClient.BACKOFF_MAX_SECONDS", 0.05),
        ):
            results = client.search_text("Jeff Nippard instagram.com")

        assert results == []
        assert ddgs.text.call_count == 3  # 1 initial + 2 retries

    def test_search_text_returns_empty_on_permanent_failure(self, tmp_path):
        """search_text returns [] after all retries exhausted."""
        ddgs = MagicMock()
        ddgs.text.side_effect = Exception("Permanent error")
        client = _make_client(tmp_path, ddgs)

        with (
            patch("services.search.OpenSearchClient.MAX_RETRIES", 0),
            patch("services.search.OpenSearchClient.BACKOFF_BASE_SECONDS", 0.01),
        ):
            results = client.search_text("some query")

        assert results == []

    def test_search_text_succeeds_after_one_retry(self, tmp_path):
        """search_text returns results if second attempt succeeds."""
        ddgs = MagicMock()
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ConnectionError("transient")
            return [{"href": "https://www.instagram.com/user/", "title": "User", "body": ""}]

        ddgs.text.side_effect = side_effect
        client = _make_client(tmp_path, ddgs)

        with (
            patch("services.search.OpenSearchClient.MAX_RETRIES", 2),
            patch("services.search.OpenSearchClient.BACKOFF_BASE_SECONDS", 0.01),
            patch("services.search.OpenSearchClient.BACKOFF_MAX_SECONDS", 0.05),
        ):
            results = client.search_text("some query")

        assert len(results) == 1
        assert call_count == 2
