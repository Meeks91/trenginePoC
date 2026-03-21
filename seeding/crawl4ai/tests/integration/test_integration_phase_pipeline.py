"""
Integration Test: PhasePipelineRunner — 4-Phase Pipeline Flow
==============================================================

Exercises the full 4-phase pipeline (search → dedupe → crawl → extract+merge)
with mocked network (DDG search + crawl4ai) but real extraction services.

Uses the gymfluencers_uk_fitness.html fixture as crawl output.
Verifies that handles from multiple configs are correctly tagged, deduped,
and merged into Influencer results.
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from config.schema import Platform, PageResult
from config.seed_schema import SeedJob, SubCategory, Region, RegionCode, Difficulty
from phase_pipeline import PhasePipelineRunner, TaggedURL
from services.influencerMerging.InfluencerMergerService import InfluencerMergerService as InfluencerMerger
from services.search.SearchService import SearchResults


FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures"
GYM_HTML = (FIXTURE_DIR / "gymfluencers_uk_fitness.html").read_text(errors="replace")

# Known TikTok handles in the gymfluencers fixture
EXPECTED_TT_HANDLES = {
    "alomoves", "alexisren", "brittne_babe", "caseypatton_",
    "imre.cze", "lilybrownerr",
}


def _make_job(
    category: str = "FITNESS",
    sub_name: str = "Gym",
    platform: Platform = Platform.Instagram,
    region_code: str = "UK",
) -> SeedJob:
    """Create a minimal SeedJob for testing."""
    sub = SubCategory(
        sub_name=sub_name,
        is_top_level=True,
        search_prompt="top gym influencers",
        alt_search_terms=[],
        known_sources=[],
        platform_notes="",
        region_notes="",
        difficulty=Difficulty.EASY,
        strict_slugs=[],
    )
    region = Region(
        code=RegionCode(region_code),
        language="en",
        label="United Kingdom",
    )
    return SeedJob(
        category_key=category,
        sub=sub,
        platform=platform,
        region=region,
    )


class TestPhasePipelineSearchAndDedupe:
    """Phase 1 (search) and Phase 2 (dedupe) — unit-level within integration context."""

    def test_dedupe_sorts_by_config_count(self):
        """URLs discovered by more configs should appear first."""
        url_bag = {
            "https://a.com": TaggedURL(
                url="https://a.com", source_query="q1",
                config_keys={"A"}, category_keys={"FITNESS"},
            ),
            "https://b.com": TaggedURL(
                url="https://b.com", source_query="q2",
                config_keys={"A", "B", "C"}, category_keys={"FITNESS", "FOOD"},
            ),
            "https://c.com": TaggedURL(
                url="https://c.com", source_query="q3",
                config_keys={"A", "B"}, category_keys={"FITNESS"},
            ),
        }

        sorted_urls = PhasePipelineRunner.dedupe_urls(url_bag)

        assert len(sorted_urls) == 3
        assert sorted_urls[0].url == "https://b.com"  # 3 configs
        assert sorted_urls[1].url == "https://c.com"  # 2 configs
        assert sorted_urls[2].url == "https://a.com"  # 1 config


@pytest.mark.integration
class TestPhasePipelineFullFlow:
    """Full 4-phase pipeline with mocked search + crawl, real extraction."""

    @pytest.fixture(scope="class")
    def pipeline_result(self):
        """Run a two-job pipeline through all 4 phases."""
        job_fitness = _make_job(category="FITNESS", sub_name="Gym")
        job_food = _make_job(category="FOOD", sub_name="Food")

        runner = PhasePipelineRunner(
            sample_n=None,
            no_bfs=True,
            no_cross_platform_lookup=True,
            name_resolution=False,
        )

        page = PageResult(
            url="https://gymfluencers.agency/influencers/",
            query="top gym influencers",
            raw_markdown=GYM_HTML,
            fit_markdown=GYM_HTML,
            raw_token_estimate=len(GYM_HTML) // 4,
            fit_token_estimate=len(GYM_HTML) // 4,
            success=True,
        )

        # ── Phase 1: Mock search to return fixture URL for both jobs ──
        with tempfile.TemporaryDirectory() as tmp:
            with (
                patch("base_pipeline.AUDIT_DIR", Path(tmp)),
                patch("phase_pipeline.AUDIT_DIR", Path(tmp)),
                patch("base_pipeline.SearchService") as MockSearchSvc,
            ):
                mock_svc = MagicMock()
                mock_svc.discover_urls.return_value = SearchResults(
                    url_query_pairs=[("https://gymfluencers.agency/influencers/", "top gym influencers")],
                    direct_handles=[],
                )
                MockSearchSvc.return_value = mock_svc

                asyncio.run(runner._search_all_configs([job_fitness, job_food]))
                url_bag = runner._url_bag
                _direct_handles = runner._all_direct_handles

            # ── Phase 2: Dedupe ──
            unique_urls = runner.dedupe_urls(url_bag)

            # ── Phase 3: Mock crawl to return fixture HTML ──
            with patch("phase_pipeline.AUDIT_DIR", Path(tmp)):
                with patch("phase_pipeline.CrawlService") as MockCrawlSvc:
                    mock_crawl = AsyncMock()
                    mock_crawl.crawl_urls.return_value = [page]
                    MockCrawlSvc.return_value = mock_crawl

                    pages, page_map = asyncio.run(runner._crawl_all(unique_urls))

            # ── Phase 4: Real extraction, mocked DDG enrichment ──
            with (
                patch("phase_pipeline.AUDIT_DIR", Path(tmp)),
                patch("services.extraction.LLMExtractionService.litellm"),
                patch("phase_pipeline.CrossPlatformHandleResolverService") as MockResolverSvc,
            ):
                mock_resolver = MagicMock()
                # Pass through: return the same influencers (no DDG enrichment)
                mock_resolver.resolve.side_effect = lambda influencers: influencers
                MockResolverSvc.return_value = mock_resolver

                inf_to_cat, name_tracker = asyncio.run(runner._extract_and_build_entries(pages, page_map, [job_fitness, job_food], []))
                seeds = InfluencerMerger.filter_blocked(inf_to_cat)

        return {
            "url_bag": url_bag,
            "unique_urls": unique_urls,
            "pages": pages,
            "page_map": page_map,
            "seeds": seeds,
            "stats": runner.stats,
        }

    def test_search_tags_url_with_both_configs(self, pipeline_result):
        """Single URL discovered by two jobs should be tagged with both config keys."""
        url_bag = pipeline_result["url_bag"]
        assert len(url_bag) == 1
        tagged = url_bag["https://gymfluencers.agency/influencers/"]
        assert len(tagged.config_keys) == 2
        assert len(tagged.category_keys) == 2
        assert "FITNESS" in tagged.category_keys
        assert "FOOD" in tagged.category_keys

    def test_dedupe_returns_single_url(self, pipeline_result):
        """Two configs same URL → 1 unique URL after dedupe."""
        assert len(pipeline_result["unique_urls"]) == 1

    def test_crawl_produces_page_map(self, pipeline_result):
        """Phase 3 should produce a page_map for the crawled URL."""
        assert len(pipeline_result["page_map"]) == 1
        assert "https://gymfluencers.agency/influencers/" in pipeline_result["page_map"]

    def test_extraction_produces_seeds(self, pipeline_result):
        """Phase 4 should produce Influencer results from real extraction."""
        seeds = pipeline_result["seeds"]
        assert len(seeds) >= 1, "Expected at least 1 seed from gymfluencers fixture"

    def test_known_handles_in_seeds(self, pipeline_result):
        """Seeds should contain handles extracted from the gymfluencers fixture."""
        all_handles: set[str] = set()
        for seed in pipeline_result["seeds"]:
            for h in [seed.ig_handle, seed.tk_handle, seed.yt_handle]:
                if h:
                    all_handles.add(h.lower().lstrip("@").rstrip("."))

        # The gymfluencers fixture has TikTok handles — after filter_blocked(),
        # they should appear in tk_handle or ig_handle fields
        assert len(all_handles) >= 3, (
            f"Expected at least 3 handles in seeds from gymfluencers fixture, "
            f"found {len(all_handles)}: {all_handles}"
        )

    def test_no_duplicate_seeds(self, pipeline_result):
        """No (handle, platform) pair should appear twice in seeds."""
        seen: set[tuple[str, str]] = set()
        for seed in pipeline_result["seeds"]:
            for plat, handle in [("instagram", seed.ig_handle), ("tiktok", seed.tk_handle), ("youtube", seed.yt_handle)]:
                if handle:
                    key = (handle.lower().lstrip("@").rstrip("."), plat)
                    assert key not in seen, f"Duplicate seed: {key}"
                    seen.add(key)

    def test_stats_recorded(self, pipeline_result):
        """Pipeline stats should be populated after run."""
        stats = pipeline_result["stats"]
        assert stats.urls_discovered >= 1
        assert stats.pages_crawled >= 1
