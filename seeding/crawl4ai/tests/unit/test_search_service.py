"""
Unit Tests: SearchService
===========================
Verifies ad domain filtering, URL relevance filtering, dedup, and MAX_URLS_PER_JOB cap.
discover_urls() tested with mocked SearchClient to avoid real network calls.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from config.seed_schema import (
    Difficulty, Platform, Region, RegionCode, SubCategory, SeedJob,
)
from services.audit.AuditService import AuditLog
from services.search.SearchClient import RawSearchResult, SearchClient
from services.search.SearchService import SearchService


# ── Helpers ──

def _make_raw_results(urls: list[str], query: str = "test query") -> list[RawSearchResult]:
    """Create RawSearchResult list from URLs."""
    return [
        RawSearchResult(url=url, title=f"Result for {url}", query=query)
        for url in urls
    ]


def _make_job(**overrides) -> SeedJob:
    """Create a minimal SeedJob for testing."""
    sub = SubCategory(
        sub_name=overrides.pop("sub_name", "Fitness"),
        search_prompt=overrides.pop("search_prompt", "fitness influencers"),
        alt_search_terms=overrides.pop("alt_search_terms", []),
        known_sources=overrides.pop("known_sources", []),
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


def _make_mock_client(results: list[RawSearchResult]) -> SearchClient:
    """Create a mock SearchClient that returns given results."""
    client = MagicMock(spec=SearchClient)
    client.search.return_value = results
    return client


def _make_svc(tmp_path: Path, results: list[RawSearchResult]) -> SearchService:
    """Create SearchService with mocked client."""
    audit = AuditLog(tmp_path, "test")
    client = _make_mock_client(results)
    return SearchService(audit, client=client)


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


# ── discover_urls() with mocked SearchClient ──

def test_discover_urls_dedup(tmp_path):
    """Duplicate URLs across queries should be deduplicated."""
    raw = _make_raw_results([
        "https://favikon.com/ai-influencers",
        "https://modash.io/ai-creators",
        "https://favikon.com/ai-influencers",
    ])
    svc = _make_svc(tmp_path, raw)
    job = _make_job()

    results = svc.discover_urls(job)

    urls = [u for u, _ in results.url_query_pairs]
    assert len(urls) == len(set(urls)), "Duplicate URLs found in results"
    assert len(urls) == 2, f"Expected 2 unique URLs, got {len(urls)}"


def test_discover_urls_ad_filter(tmp_path):
    """Ad domain URLs should be filtered out."""
    raw = _make_raw_results([
        "https://favikon.com/ai-influencers",
        "https://bing.com/aclick/redirect",
        "https://googleadservices.com/pagead",
        "https://modash.io/ai-creators",
    ])
    svc = _make_svc(tmp_path, raw)
    job = _make_job()

    results = svc.discover_urls(job)

    urls = [u for u, _ in results.url_query_pairs]
    assert "https://bing.com/aclick/redirect" not in urls
    assert "https://googleadservices.com/pagead" not in urls
    assert "https://favikon.com/ai-influencers" in urls
    assert "https://modash.io/ai-creators" in urls


def test_discover_urls_max_cap(tmp_path):
    """Should cap results at MAX_URLS_PER_JOB."""
    raw = _make_raw_results([
        f"https://example.com/ai-tools-page{i}" for i in range(20)
    ])
    svc = _make_svc(tmp_path, raw)
    job = _make_job()

    with patch("services.search.SearchService.MAX_URLS_PER_JOB", 3):
        results = svc.discover_urls(job)

    assert len(results.url_query_pairs) <= 3, (
        f"Expected max 3 URLs, got {len(results.url_query_pairs)}"
    )


def test_discover_urls_audit_logging(tmp_path):
    """discovery should log accepted/rejected URLs to audit trail."""
    raw = _make_raw_results([
        "https://favikon.com/ai-page",
        "https://bing.com/ad",
    ])
    audit = AuditLog(tmp_path, "test")
    client = _make_mock_client(raw)
    svc = SearchService(audit, client=client)
    job = _make_job()

    svc.discover_urls(job)

    actions = [e.action for e in audit.entries]
    assert "url_accepted" in actions, "Missing url_accepted audit entry"
    assert "url_rejected" in actions, "Missing url_rejected audit entry"


# ── Platform URL Extraction (DDG Dorking) ──

def test_discover_urls_platform_url_extraction(tmp_path):
    """Platform URLs (instagram.com, tiktok.com) should extract handles directly."""
    raw = _make_raw_results([
        "https://favikon.com/list",
        "https://instagram.com/kayla_itsines",
        "https://tiktok.com/@charlidamelio",
    ])
    svc = _make_svc(tmp_path, raw)
    job = _make_job()

    results = svc.discover_urls(job)

    urls = [u for u, _ in results.url_query_pairs]
    assert "https://instagram.com/kayla_itsines" not in urls, "Platform URL should not be in url_query_pairs"
    assert "https://tiktok.com/@charlidamelio" not in urls, "Platform URL should not be in url_query_pairs"
    assert "https://favikon.com/list" in urls
    assert len(results.direct_handles) == 2, f"Expected 2 direct handles, got {len(results.direct_handles)}"


def test_is_platform_url():
    """Static method should identify platform domains."""
    assert SearchService._is_platform_url("https://instagram.com/user") is True
    assert SearchService._is_platform_url("https://www.tiktok.com/@user") is True
    assert SearchService._is_platform_url("https://youtube.com/channel/123") is True
    assert SearchService._is_platform_url("https://twitter.com/user") is True
    assert SearchService._is_platform_url("https://x.com/user") is True
    assert SearchService._is_platform_url("https://favikon.com/blog") is False


# ── Client receives SeedJob ──

def test_client_receives_seed_job(tmp_path):
    """SearchClient.search() should receive the SeedJob directly."""
    raw = _make_raw_results(["https://example.com/page"])
    audit = AuditLog(tmp_path, "test")
    client = _make_mock_client(raw)
    svc = SearchService(audit, client=client)
    job = _make_job(sub_name="Yoga", platform=Platform.TikTok)

    svc.discover_urls(job)

    client.search.assert_called_once_with(job)


# ── Pipeline Cache DI Guard ──

class TestPipelineCacheInjection:
    """Guard tests: assert pipeline runners always inject SearchCache."""

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
        """PipelineRunner without cache= defaults to None."""
        from pipeline import PipelineRunner

        runner = PipelineRunner()
        assert runner._cache is None, "Default should be None — cli.py must always supply a cache"
