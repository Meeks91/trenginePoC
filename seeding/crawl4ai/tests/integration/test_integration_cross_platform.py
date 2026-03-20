"""
TRUE E2E Test: Cross-Platform Handle Preservation
====================================================

Tests the FULL pipeline path for the modash_uk_food fixture:

  HTML fixture → Regex Extract → Classify → Merge → Enrich (mocked DDG) → Dedup → Final Output

Verifies that when targeting Instagram, TikTok handles found on the same
page survive all layers and appear as separate entries in the final output.

This is the ONLY test that covers Extraction + Enrichment together.
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from config.schema import Influencer, PageResult, Platform
from services.audit.AuditService import AuditLog
from services.extraction.HandleExtractionService import HandleExtractionService
from services.extraction.RegexHandleExtractor import extract_handles_from_html
from services.enrichment.NameToHandleService import NameToHandleService


FIXTURE = Path(__file__).resolve().parent.parent / "fixtures" / "modash_uk_food.html"
PAGE_URL = "https://www.modash.io/find-influencers/united-kingdom/food"

# Handles known to exist on BOTH Instagram and TikTok on this page
CROSS_PLATFORM_HANDLES = {
    "charlotteannaw",
    "dianas.delicacies",
    "jenny_francis01",
    "letsget.em",
    "londonfoodieexpat",
    "lungisalwaysbaking",
    "sophiehlbrown",
}

# Instagram-only handles (no TikTok link on this page)
IG_ONLY_HANDLES = {
    "aton_of_food",
    "clareccole",
    "colesyboy93",
    "emsbalance",
    "evejwinstanley",
    "foodfeaturedofficial",
    "hannahsfamilylife",
    "heatherjamesofficial",
    "stargrazingco",
    "thehouseupstairs",
    "thom_foodery",
    "tinygirleatsworld",
}

# TikTok-only handles (different TikTok handle from IG)
TT_ONLY_HANDLES = {
    "christomkins123",  # IG is christomkins1
}


def _all_handles_lower(influencers: list[Influencer]) -> set[tuple[str, str]]:
    """Extract all (handle_lower, platform_value) from a list of Influencers."""
    result = set()
    for inf in influencers:
        for plat, handle in inf.handles.items():
            result.add((handle.lower().rstrip("."), plat.value))
    return result


@pytest.fixture(scope="module")
def html():
    return FIXTURE.read_text(errors="replace")


@pytest.fixture(scope="module")
def page_result(html):
    """Build a PageResult as CrawlService would produce."""
    return PageResult(
        url=PAGE_URL,
        query="manual_override",
        raw_markdown=html,
        fit_markdown=html,
        raw_token_estimate=len(html) // 4,
        fit_token_estimate=len(html) // 4,
        success=True,
    )


# ══════════════════════════════════════════════════════════════════════
# 1. Full pipeline: Extract → Classify → Merge → Enrich → Dedup
# ══════════════════════════════════════════════════════════════════════


class TestCrossPlatformE2E:
    """True e2e: every layer from extraction to final enriched output."""

    def test_cross_platform_handles_survive_enrichment(self, page_result):
        """Cross-platform handles must appear as entries with handles for each
        platform in the final output."""
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test_cross_platform")

            # ── Layer 1: Extract (HandleExtractionService) ──
            handle_svc = HandleExtractionService(audit)

            # Mock the LLM extraction to avoid real API calls
            with patch("services.extraction.LLMExtractionService.litellm"):
                extract_result = asyncio.run(handle_svc.extract_all_handles(
                    [page_result],
                    platform=Platform.Instagram,
                    category_key="FOOD",
                    sub_name="Food",
                    region="United Kingdom",
                    year="2026",
                    direct_handles=[],
                    sample_n=0,  # Skip LLM entirely
                ))

            merged = extract_result.all_merged

            # Sanity check: extraction found handles
            assert len(merged) > 20, (
                f"Expected 20+ handles from extraction, got {len(merged)}"
            )

            # Verify cross-platform handles are in merged output
            all_pairs = _all_handles_lower(merged)
            for handle in CROSS_PLATFORM_HANDLES:
                assert (handle, "Instagram") in all_pairs, (
                    f"Missing Instagram entry for {handle} after extraction"
                )
                assert (handle, "TikTok") in all_pairs, (
                    f"Missing TikTok entry for {handle} after extraction"
                )

            # ── Layer 2: Enrich + Dedup ──
            enrich_svc = NameToHandleService(audit, delay_seconds=0)

            # Mock DDG to return nothing — we're testing that cross-platform
            # handles survive, not that DDG backfill works
            mock_ddgs = MagicMock()
            mock_ddgs.text.return_value = []
            enrich_svc._ddgs = mock_ddgs

            final = enrich_svc.resolve_cross_account_handles(merged, platform=Platform.Instagram, min_sources=0)

            # ── Assertions on final output ──
            final_pairs = _all_handles_lower(final)

            # Cross-platform handles: BOTH IG and TT entries must survive
            for handle in CROSS_PLATFORM_HANDLES:
                assert (handle, "Instagram") in final_pairs, (
                    f"{handle}: Instagram entry lost after enrichment!"
                )
                assert (handle, "TikTok") in final_pairs, (
                    f"{handle}: TikTok entry lost after enrichment! "
                    f"Found: {final_pairs}"
                )

            # IG-only handles: still present
            for handle in IG_ONLY_HANDLES:
                assert (handle, "Instagram") in final_pairs, (
                    f"IG-only handle {handle} missing from final output"
                )

            # TT-only handles: still present
            for handle in TT_ONLY_HANDLES:
                assert (handle, "TikTok") in final_pairs, (
                    f"TT-only handle {handle} missing from final output"
                )

    def test_no_duplicate_handle_platform_pairs(self, page_result):
        """Same (handle, platform) must not appear twice in final output."""
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test_no_dupes")

            handle_svc = HandleExtractionService(audit)
            with patch("services.extraction.LLMExtractionService.litellm"):
                extract_result = asyncio.run(handle_svc.extract_all_handles(
                    [page_result],
                    platform=Platform.Instagram,
                    category_key="FOOD",
                    sub_name="Food",
                    region="United Kingdom",
                    year="2026",
                    direct_handles=[],
                    sample_n=0,
                ))

            enrich_svc = NameToHandleService(audit, delay_seconds=0)
            mock_ddgs = MagicMock()
            mock_ddgs.text.return_value = []
            enrich_svc._ddgs = mock_ddgs

            final = enrich_svc.resolve_cross_account_handles(
                extract_result.all_merged, platform=Platform.Instagram,
                min_sources=0,
            )

            seen = set()
            for inf in final:
                for plat, handle in inf.handles.items():
                    key = (handle.lower().rstrip("."), plat.value.lower())
                    assert key not in seen, (
                        f"Duplicate (handle, platform) in final output: {key}"
                    )
                    seen.add(key)

    def test_enrichment_adds_target_platform_entry(self, page_result):
        """When DDG finds a target-platform handle for a cross-platform
        influencer, a NEW entry is added — the original is NOT overwritten."""
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test_enrich_adds")

            handle_svc = HandleExtractionService(audit)
            with patch("services.extraction.LLMExtractionService.litellm"):
                extract_result = asyncio.run(handle_svc.extract_all_handles(
                    [page_result],
                    platform=Platform.Instagram,
                    category_key="FOOD",
                    sub_name="Food",
                    region="United Kingdom",
                    year="2026",
                    direct_handles=[],
                    sample_n=0,
                ))

            # Build a list with ONLY TikTok entries (simulate cross-platform)
            tt_only = [
                Influencer(name="Tom Miller", handles={Platform.TikTok: "testcreator"}),
            ]

            enrich_svc = NameToHandleService(audit, delay_seconds=0)

            # Mock DDG to find an Instagram handle
            def mock_text(query, max_results=2, **kwargs):
                if "Tom Miller" in query:
                    return [{"href": "https://www.instagram.com/testcreator_ig/",
                             "title": "Tom Miller", "body": ""}]
                return []

            with patch.object(enrich_svc._ddgs, "text", side_effect=mock_text):
                final = enrich_svc.resolve_cross_account_handles(tt_only, platform=Platform.Instagram, min_sources=0)

            # Should have 2 entries: original TikTok + new Instagram
            assert len(final) == 2, (
                f"Expected 2 entries (TT + IG), got {len(final)}: "
                f"{[(inf.name, inf.handles) for inf in final]}"
            )

            all_pairs = _all_handles_lower(final)
            assert ("testcreator", "TikTok") in all_pairs, (
                "Original TikTok entry was lost"
            )
            assert ("testcreator_ig", "Instagram") in all_pairs, (
                "New Instagram entry was not added"
            )
