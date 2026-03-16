"""
Unit Tests: StrictSearchClient
================================
Verifies dork query building, mandatory clause structure, slug composition,
and Serper response parsing. All tests use mocked HTTP — no real API calls.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from config.seed_schema import (
    Difficulty, Platform, Region, RegionCode, SubCategory, SeedJob,
)
from services.audit.AuditService import AuditLog
from services.search.SearchClient import QueryType, RawSearchResult, SearchQuery
from services.search.StrictSearchClient import StrictSearchClient


# ── Helpers ──

def _make_job(**overrides) -> SeedJob:
    """Create a minimal SeedJob for testing."""
    sub = SubCategory(
        sub_name=overrides.pop("sub_name", "Fitness"),
        search_prompt=overrides.pop("search_prompt", "top fitness influencers"),
        alt_search_terms=overrides.pop("alt_search_terms", ["best gym creators"]),
        known_sources=overrides.pop("known_sources", ["favikon.com"]),
        difficulty=overrides.pop("difficulty", Difficulty.MEDIUM),
        strict_slugs=overrides.pop("strict_slugs", ["fitness", "workout", "gym"]),
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


def _make_client(tmp_path) -> StrictSearchClient:
    """Create a StrictSearchClient with fake API key."""
    audit = AuditLog(tmp_path, "test")
    return StrictSearchClient(audit, api_key="test-key-123", delay_seconds=0)


# ── Mandatory Clause ──

def test_mandatory_clause_contains_intitle_and_reddit():
    """Mandatory clause must have all 3 intitle: terms + site:reddit.com."""
    clause = StrictSearchClient._mandatory_clause()

    assert clause.startswith("(")
    assert clause.endswith(")")
    assert "intitle:influencer" in clause
    assert "intitle:creator" in clause
    assert "intitle:top" in clause
    assert "site:reddit.com" in clause
    assert clause.count("OR") == 3


def test_mandatory_clause_no_reddit_excludes_site():
    """Site-targeted variant must NOT include site:reddit.com."""
    clause = StrictSearchClient._mandatory_clause_no_reddit()

    assert "intitle:influencer" in clause
    assert "intitle:creator" in clause
    assert "intitle:top" in clause
    assert "site:reddit.com" not in clause
    assert clause.count("OR") == 2


# ── Slug Clause ──

def test_slug_clause_joins_with_or():
    """Slugs should be OR-joined inside parentheses."""
    clause = StrictSearchClient._slug_clause(["fitness", "workout", "gym"])

    assert clause == "(fitness OR workout OR gym)"


def test_slug_clause_empty_returns_empty_string():
    """No slugs → empty string (not empty parens)."""
    clause = StrictSearchClient._slug_clause([])

    assert clause == ""


# ── Query Building ──

def test_primary_query_has_mandatory_slugs_and_terms(tmp_path):
    """PRIMARY query must contain mandatory clause, slug clause, and search terms."""
    client = _make_client(tmp_path)
    job = _make_job()

    queries = client._build_queries(job)
    primary = [q for q in queries if q.query_type == QueryType.PRIMARY_OPEN]

    assert len(primary) == 1
    q = primary[0].query
    assert "(intitle:influencer OR intitle:creator OR intitle:top OR site:reddit.com)" in q
    assert "(fitness OR workout OR gym)" in q
    assert '"Fitness"' in q
    assert "Instagram" in q
    assert "2026" in q


def test_alt_query_includes_alt_term_and_region(tmp_path):
    """ALT queries use alt_search_terms and include region label."""
    client = _make_client(tmp_path)
    job = _make_job(alt_search_terms=["best gym creators", "top workout channels"])

    queries = client._build_queries(job)
    alts = [q for q in queries if q.query_type == QueryType.ALT_OPEN]

    assert len(alts) == 2
    assert "best gym creators" in alts[0].query
    assert "top workout channels" in alts[1].query
    assert "United States" in alts[0].query


def test_site_targeted_has_site_prefix_and_no_reddit(tmp_path):
    """SITE queries must start with site:X and use no-reddit mandatory clause."""
    client = _make_client(tmp_path)
    job = _make_job(known_sources=["favikon.com", "modash.io"])

    queries = client._build_queries(job)
    sites = [q for q in queries if q.query_type == QueryType.SITE_TARGETED]

    assert len(sites) == 2
    assert sites[0].query.startswith("site:favikon.com")
    assert sites[1].query.startswith("site:modash.io")
    assert "site:reddit.com" not in sites[0].query
    assert "site:reddit.com" not in sites[1].query
    assert "(intitle:influencer OR intitle:creator OR intitle:top)" in sites[0].query


def test_query_count_matches_config(tmp_path):
    """Total queries = 1 primary + N alt + M site."""
    client = _make_client(tmp_path)
    job = _make_job(
        alt_search_terms=["term1", "term2"],
        known_sources=["favikon.com", "modash.io"],
    )

    queries = client._build_queries(job)

    assert len(queries) == 5  # 1 primary + 2 alt + 2 site


def test_no_slugs_omits_slug_clause(tmp_path):
    """With no strict_slugs, queries should not have empty parens."""
    client = _make_client(tmp_path)
    job = _make_job(strict_slugs=[])

    queries = client._build_queries(job)
    primary = queries[0].query

    assert "()" not in primary
    assert "(intitle:influencer" in primary


# ── Serper Response Parsing ──

@patch("services.search.StrictSearchClient.requests.post")
def test_execute_parses_serper_response(mock_post, tmp_path):
    """_execute should map Serper organic results to RawSearchResult."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "organic": [
            {"title": "Top Fitness Influencers", "link": "https://favikon.com/fitness", "snippet": "..."},
            {"title": "Best Gym Creators", "link": "https://modash.io/gym", "snippet": "..."},
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    client = _make_client(tmp_path)
    sq = SearchQuery(query="test query", query_type=QueryType.PRIMARY_OPEN)
    results = client._execute(sq)

    assert len(results) == 2
    assert results[0].url == "https://favikon.com/fitness"
    assert results[0].title == "Top Fitness Influencers"
    assert results[0].query == "test query"
    assert results[1].url == "https://modash.io/gym"


@patch("services.search.StrictSearchClient.requests.post")
def test_search_aggregates_all_query_results(mock_post, tmp_path):
    """search() should aggregate results from all query types."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "organic": [
            {"title": "Result", "link": "https://example.com/page", "snippet": "..."},
        ]
    }
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    client = _make_client(tmp_path)
    job = _make_job(
        alt_search_terms=["alt1"],
        known_sources=["favikon.com"],
    )

    results = client.search(job)

    # 1 primary + 1 alt + 1 site = 3 queries, each returning 1 result
    assert len(results) == 3
    assert mock_post.call_count == 3


@patch("services.search.StrictSearchClient.requests.post")
def test_execute_handles_api_error_gracefully(mock_post, tmp_path):
    """API errors should return empty list, not raise."""
    mock_post.side_effect = requests.ConnectionError("Connection refused")

    client = _make_client(tmp_path)
    sq = SearchQuery(query="test query", query_type=QueryType.PRIMARY_OPEN)
    results = client._execute(sq)

    assert results == []
