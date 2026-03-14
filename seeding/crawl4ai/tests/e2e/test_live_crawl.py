"""Live crawl e2e test — actually hits the network.

Run with: pytest tests/e2e/test_live_crawl.py -v -s
These tests are marked 'slow' and 'network' so they don't run in the normal suite.
"""

import pytest

from services.audit.AuditService import AuditLog
from services.crawling.CrawlService import CrawlService
from services.extraction.HandleExtractionService import HandleExtractionService
from services.enrichment.NameToHandleService import NameToHandleService
from config.schema import Platform
from config import AUDIT_DIR


# Known handles on cloudkitchens.com/blog/top-food-influencers (verified 2026-03-12)
CLOUDKITCHENS_URL = "https://cloudkitchens.com/blog/top-food-influencers"

# ── Ground-truth handles by platform (regex-extracted, no LLM) ──
EXPECTED_HANDLES = {
    "Instagram": {
        "foodgod", "deliciouslyella", "blackforager", "davidchang",
        "foodbeast", "thejoshelkin", "starinfinitefood",
        "bingingwithbabish", "howtocakeit", "amandafrederickson",
    },
    "TikTok": {
        "foodgod", "_deliciouslyella", "alexisnikole", "davidchang",
        "yungfoodbeast", "thejoshelkin", "starinfinitefood",
        "babishculinaryuniverse",
    },
    "YouTube": {
        "foodgod", "majordomomedia", "HowToCakeIt", "TheJoshElkin",
    },
}

# Minimum counts per platform (allows slight variance in scraping)
MIN_COUNTS = {"Instagram": 8, "TikTok": 6, "YouTube": 3}
MIN_TOTAL = 20  # At least 20 across all platforms


@pytest.mark.slow
@pytest.mark.network
class TestLiveCrawl:
    """End-to-end tests that actually crawl real URLs."""

    @pytest.mark.asyncio
    async def test_cloudkitchens_crawl_succeeds(self):
        """CrawlService actually fetches the cloudkitchens page."""
        audit = AuditLog(AUDIT_DIR, "test_live")
        crawl_svc = CrawlService(audit)

        pages = await crawl_svc.crawl_urls([
            (CLOUDKITCHENS_URL, "test_query"),
        ])

        assert len(pages) == 1
        assert pages[0].success, f"Crawl failed: {pages[0].error}"
        assert len(pages[0].fit_markdown) > 500, "fit_markdown too short — content may not have loaded"
        assert pages[0].handles_in_source >= 5, "Expected at least 5 handles in raw HTML"

    @pytest.mark.asyncio
    async def test_cloudkitchens_extraction_finds_known_handles(self):
        """Crawl → regex extract → verify known handles per platform."""
        audit = AuditLog(AUDIT_DIR, "test_live_extract")
        crawl_svc = CrawlService(audit)
        handle_svc = HandleExtractionService(audit)

        pages = await crawl_svc.crawl_urls([
            (CLOUDKITCHENS_URL, "test_query"),
        ])
        assert pages[0].success, f"Crawl failed: {pages[0].error}"

        result = await handle_svc.extract_all_handles(
            pages,
            platform=Platform.Instagram,
            category_key="FOOD",
            sub_name="Food",
            region="US",
            year="2026",
            direct_handles=[],
        )

        # Build platform → set[handle] lookup from results
        by_platform: dict[str, set[str]] = {}
        for inf in result.all_merged:
            for plat, handle in inf.handles.items():
                by_platform.setdefault(plat.value, set()).add(
                    handle.lower().lstrip("@")
                )

        # ── Per-platform assertions ──
        for platform, expected in EXPECTED_HANDLES.items():
            found = by_platform.get(platform, set())
            found_lower = {h.lower() for h in found}
            expected_lower = {h.lower() for h in expected}
            hits = expected_lower & found_lower
            min_count = MIN_COUNTS[platform]
            assert len(hits) >= min_count, (
                f"{platform}: expected ≥{min_count} of {expected_lower}, "
                f"found only {hits} (all on platform: {found_lower})"
            )

        # ── Total count assertion ──
        total = sum(len(s) for s in by_platform.values())
        assert total >= MIN_TOTAL, (
            f"Expected ≥{MIN_TOTAL} total handles, got {total}: "
            f"{', '.join(f'{k}={len(v)}' for k, v in by_platform.items())}"
        )

    @pytest.mark.asyncio
    async def test_cloudkitchens_full_pipeline(self):
        """Full pipeline: crawl → extract → enrich+dedup with explicit checks."""
        audit = AuditLog(AUDIT_DIR, "test_live_full")
        crawl_svc = CrawlService(audit)
        handle_svc = HandleExtractionService(audit)
        enrich_svc = NameToHandleService(audit)

        pages = await crawl_svc.crawl_urls([
            (CLOUDKITCHENS_URL, "test_query"),
        ])
        assert pages[0].success

        result = await handle_svc.extract_all_handles(
            pages,
            platform=Platform.Instagram,
            category_key="FOOD",
            sub_name="Food",
            region="US",
            year="2026",
            direct_handles=[],
        )

        unique = enrich_svc.resolve_cross_account_handles(
            result.all_merged,
            platform=Platform.Instagram,
            skip_cross_platform=True,
        )

        # ── Explicit assertions ──
        all_handles: set[str] = set()
        for inf in unique:
            for h in inf.handles.values():
                all_handles.add(h.lower().lstrip("@"))

        # Must have at least 10 distinct influencers
        assert len(unique) >= 10, f"Expected ≥10 unique influencers, got {len(unique)}"

        # Most influencers should have a handle (live crawl has variance)
        with_handles = [inf for inf in unique if inf.handles]
        assert len(with_handles) >= len(unique) - 5, (
            f"{len(unique) - len(with_handles)} influencers missing handles"
        )

        # Core influencers that must always be present (stable across scrapes)
        must_have = {"foodgod", "davidchang", "bingingwithbabish", "deliciouslyella", "blackforager"}
        missing = must_have - all_handles
        assert not missing, f"Missing core influencers: {missing}"

        # At least 3 distinct platforms
        platforms: set[Platform] = set()
        for inf in unique:
            platforms.update(inf.handles.keys())
        assert len(platforms) >= 3, (
            f"Expected ≥3 platforms, got {platforms}"
        )
