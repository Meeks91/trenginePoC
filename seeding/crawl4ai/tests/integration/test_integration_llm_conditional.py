"""
E2E Test: HandleExtractionService — LLM Conditional Trigger
===============================================================

Tests the FULL orchestration flow in HandleExtractionService.extract_all_handles():

  1. Regex extraction on real fixture HTML
  2. Mechanical classification of naked @handles (100-char context window)
  3. needs_llm() gating — LLM fires only for naked handles OR zero-handle listicles
  4. LLM is SKIPPED when regex handles are sufficient

Uses real fixtures + mocked LLM to verify behavior without API costs.
"""

import asyncio
import tempfile
from pathlib import Path
from unittest.mock import MagicMock


from config.schema import PageResult, Platform
from services.audit.AuditService import AuditLog
from services.extraction.HandleExtractionService import (
    HandleExtractionService,
    needs_llm,
)
from services.extraction.RegexHandleExtractorService import ExtractedHandle
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService

# Pre-import LLMExtractionService so its module is in sys.modules for mocking
import services.extraction.LLMExtractionService as _ext_svc_mod  # noqa: F401

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def _page(url: str, md: str, success: bool = True) -> PageResult:
    return PageResult(
        url=url, query="test", raw_markdown=md, fit_markdown=md,
        raw_token_estimate=len(md) // 4, fit_token_estimate=len(md) // 4,
        success=success,
    )


# ══════════════════════════════════════════════════════════════════════
# Test 1: needs_llm() gating with REAL fixture data
# ══════════════════════════════════════════════════════════════════════

class TestNeedsLLMGatingWithFixtures:
    """Verify needs_llm() correctly gates LLM using real fixture data."""

    def test_page_with_url_handles_skips_llm(self):
        """Page with URL-based handles and NO naked handles → LLM skipped."""
        page = _page(
            url="https://www.clickanalytic.com/10-french-fitness-influencers/",
            md="Some fitness content with IG links...",
        )
        # clickanalytic has 15 IG handles, 0 naked
        assert needs_llm(page, {page.url: 15}, {page.url: 0}) is False

    def test_page_with_naked_handles_skips_llm(self):
        """Page with naked @handles → ExtractionService LLM SKIPPED.
        Naked handles are classified mechanically, not via ExtractionService."""
        page = _page(
            url="https://www.seekahost.co.uk/top-uk-fitness-influencers",
            md="Follow @thebodycoach and @tomdaley for fitness content",
        )
        # seekahost has both URL handles and naked handles → total > 0 → skip
        assert needs_llm(page, {page.url: 7}, {page.url: 15}) is False

    def test_listicle_zero_handles_triggers_llm(self):
        """Listicle page (keyword in URL) with zero regex handles → LLM fires."""
        page = _page(
            url="https://example.com/top-fitness-influencers",
            md="Best fitness creators to follow in 2025...",
        )
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is True

    def test_non_listicle_zero_handles_skips_llm(self):
        """Non-listicle page with zero handles → LLM skipped (not worth it)."""
        page = _page(
            url="https://example.com/privacy-policy",
            md="This is our privacy policy...",
        )
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is False


# ══════════════════════════════════════════════════════════════════════
# Test 2: Mechanical classification of naked handles
# ══════════════════════════════════════════════════════════════════════

class TestMechanicalClassification:
    """Verify classify_by_context() auto-assigns platform correctly."""

    def test_instagram_keyword_nearby(self):
        """'Instagram' within 100 chars → auto-assigns Instagram."""
        handle = ExtractedHandle(handle="fit_guru", platform="")
        result = HandleExtractionService.classify_by_context(
            handle,
            "Follow on Instagram: @fit_guru for workouts",
            "https://blog.com/article",
        )
        assert result == "Instagram"

    def test_tiktok_keyword_nearby(self):
        """'TikTok' within 100 chars → auto-assigns TikTok."""
        handle = ExtractedHandle(handle="dancer99", platform="")
        result = HandleExtractionService.classify_by_context(
            handle,
            "Top TikTok creator @dancer99 goes viral",
            "https://blog.com/article",
        )
        assert result == "TikTok"

    def test_youtube_keyword_nearby(self):
        """'YouTube' within 100 chars → auto-assigns YouTube."""
        handle = ExtractedHandle(handle="vlogger_x", platform="")
        result = HandleExtractionService.classify_by_context(
            handle,
            "Subscribe to @vlogger_x on YouTube for daily content",
            "https://blog.com/article",
        )
        assert result == "YouTube"

    def test_no_context_returns_empty(self):
        """No platform keyword nearby → unclassified."""
        handle = ExtractedHandle(handle="mystery_user", platform="")
        result = HandleExtractionService.classify_by_context(
            handle,
            "@mystery_user posts cool stuff every day",
            "https://random-blog.com/article",
        )
        assert result == ""

    def test_two_platforms_returns_closest(self):
        """Two platforms mentioned nearby → disambiguated by closest keyword."""
        handle = ExtractedHandle(handle="crossplat", platform="")
        result = HandleExtractionService.classify_by_context(
            handle,
            "Follow @crossplat on Instagram and TikTok for more",
            "https://blog.com/article",
        )
        # "Instagram" is closer to @crossplat than "TikTok" → picks Instagram
        assert result == "Instagram"


# ══════════════════════════════════════════════════════════════════════
# Test 3: Full extract_all_handles() with mocked LLM
# ══════════════════════════════════════════════════════════════════════

class TestExtractAllHandlesE2E:
    """TRUE E2E: HandleExtractionService.extract_all_handles() → HandleFromNameService.

    No Gemini mock — LLM won't fire for handle-rich pages.
    DDG mocked to avoid rate limiting.
    """

    def test_url_handles_skip_llm_and_survive_enrichment(self):
        """URL-based handles → LLM skipped → enrichment preserves them."""
        html = '''
        <html><body>
        <a href="https://instagram.com/kayla_itsines">Kayla</a>
        <a href="https://instagram.com/jeff_seid">Jeff</a>
        <a href="https://tiktok.com/@dancer99">Dancer</a>
        </body></html>
        '''
        page = _page(url="https://example.com/fitness-page", md=html)

        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test")
            handle_svc = HandleExtractionService(audit)

            result = asyncio.run(handle_svc.extract_all_handles(
                pages=[page],
                platform=Platform.Instagram,
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
                direct_handles=[],
            ))

            # LLM should have been skipped (regex was sufficient)
            assert result.llm_pages_skipped >= 1
            assert len(result.regex_handles) >= 3

            # Enrich + Dedup
            resolver = CrossPlatformHandleResolverService(
                audit, search_client=MagicMock(), delay_seconds=0,
            )

            final = resolver.resolve(result.all_merged)

            # All 3 handles must survive enrichment
            final_handles: set[str] = set()
            for inf in final:
                for h in inf.handles.values():
                    final_handles.add(h.lower().lstrip("@"))
            assert "kayla_itsines" in final_handles
            assert "jeff_seid" in final_handles
            assert "dancer99" in final_handles

            # Cross-platform: dancer99 is TikTok, should be preserved
            dancer_entries = [
                inf for inf in final
                if any("dancer99" in h.lower() for h in inf.handles.values())
            ]
            assert len(dancer_entries) >= 1
            tt_entry = [inf for inf in dancer_entries if Platform.TikTok in inf.handles]
            assert len(tt_entry) >= 1, "TikTok entry for dancer99 was lost"

    def test_naked_handles_classified_and_survive_enrichment(self):
        """Naked @handles → mechanically classified → survive enrichment."""
        html = '''
        <html><body>
        <h1>Top Instagram fitness creators</h1>
        <p>Follow these amazing creators:</p>
        <p>@fit_guru_2025 - Amazing workouts</p>
        <p>@yoga_queen - Best yoga content</p>
        </body></html>
        '''
        page = _page(url="https://example.com/top-influencers", md=html)

        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test")
            handle_svc = HandleExtractionService(audit)

            result = asyncio.run(handle_svc.extract_all_handles(
                pages=[page],
                platform=Platform.Instagram,
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
                direct_handles=[],
            ))

            # Handles should be mechanically classified (page title says Instagram)
            classified = [h for h in result.regex_handles
                          if Platform.Instagram in h.handles]
            assert len(classified) >= 2

            # LLM should be SKIPPED
            assert result.llm_pages_used == 0
            assert result.llm_pages_skipped >= 1

            # Enrich + Dedup
            resolver = CrossPlatformHandleResolverService(
                audit, search_client=MagicMock(), delay_seconds=0,
            )

            final = resolver.resolve(result.all_merged)

            # Both handles must survive
            final_handles: set[str] = set()
            for inf in final:
                for h in inf.handles.values():
                    final_handles.add(h.lower().lstrip("@"))
            assert "fit_guru_2025" in final_handles
            assert "yoga_queen" in final_handles

    def test_gymfluencers_fixture_full_pipeline(self):
        """Real gymfluencers fixture → extract → enrich → verify handles."""
        html = (FIXTURES_DIR / "gymfluencers_uk_fitness.html").read_text(
            errors="replace"
        )
        page = _page(url="https://gymfluencers.agency/fitness", md=html)

        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test")
            handle_svc = HandleExtractionService(audit)

            result = asyncio.run(handle_svc.extract_all_handles(
                pages=[page],
                platform=Platform.Instagram,
                category_key="FITNESS",
                sub_name="Fitness",
                region="UK",
                year="2026",
                direct_handles=[],
            ))

            # Regex should find TT + YT handles
            assert len(result.regex_handles) >= 7
            # LLM should be SKIPPED
            assert result.llm_pages_used == 0

            # Enrich + Dedup
            resolver = CrossPlatformHandleResolverService(
                audit, search_client=MagicMock(), delay_seconds=0,
            )

            final = resolver.resolve(result.all_merged)

            # TikTok handles must survive as separate entries
            tt_entries = [inf for inf in final if Platform.TikTok in inf.handles]
            assert len(tt_entries) >= 1, (
                "TikTok handles lost after enrichment"
            )
            # YouTube handles must survive
            yt_entries = [inf for inf in final if Platform.YouTube in inf.handles]
            assert len(yt_entries) >= 1, (
                "YouTube handles lost after enrichment"
            )
            # No (handle, platform) duplicates
            seen: set[tuple[str, Platform]] = set()
            for inf in final:
                for plat, handle in inf.handles.items():
                    key = (handle.lower().lstrip("@"), plat)
                    assert key not in seen, f"Duplicate: {key}"
                    seen.add(key)

