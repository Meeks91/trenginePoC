"""
Tests for HandleExtractionService
===================================
Unit tests for the new HandleExtractionService that orchestrates
Phases 3a–3c of handle extraction.

Tests:
  - needs_llm() gating logic (canonical — replaces duplicated test helper)
  - _regex_extract() static method
  - _merge_handles() static method
"""

import pytest
from config.schema import PageResult, Influencer, Platform
from services.extraction.RegexHandleExtractor import ExtractedHandle, assign_names_from_headings
from services.extraction.HandleExtractionService import (
    HandleExtractionService,
    HandleExtractionResult,
    needs_llm,
)


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

def _page(url: str, success: bool = True, fit_md: str = "some content",
          raw_md: str = "") -> PageResult:
    """Helper to create a PageResult for testing."""
    return PageResult(
        url=url,
        query="test",
        raw_markdown=raw_md or fit_md,
        fit_markdown=fit_md,
        raw_token_estimate=100,
        fit_token_estimate=50,
        success=success,
    )


# ══════════════════════════════════════════════════════════════════════
# needs_llm() — canonical tests (single source of truth)
# ══════════════════════════════════════════════════════════════════════

class TestNeedsLlm:
    """Tests for the needs_llm() gating function."""

    def test_listicle_url_no_handles_triggers_llm(self):
        page = _page("https://example.com/top-fitness-influencers")
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is True

    def test_listicle_url_with_handles_skips_llm(self):
        page = _page("https://example.com/top-fitness-influencers")
        assert needs_llm(page, {page.url: 5}, {page.url: 0}) is False

    def test_non_listicle_url_skips_llm(self):
        page = _page("https://example.com/privacy-policy")
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is False

    def test_naked_handles_on_non_listicle_skips_llm(self):
        """Naked handles on a non-listicle page → SKIP LLMExtractionService.
        Naked handles are classified mechanically or via HandleClassifier LLM."""
        page = _page("https://some-random-blog.com/article")
        assert needs_llm(page, {page.url: 0}, {page.url: 3}) is False

    def test_naked_handles_on_listicle_with_handles_skips_llm(self):
        """Listicle page with naked handles + URL handles → SKIP.
        Regex already found URL-based handles, no need for LLMExtractionService."""
        page = _page("https://example.com/top-fitness-influencers")
        assert needs_llm(page, {page.url: 5}, {page.url: 3}) is False

    def test_naked_handles_only_on_listicle_skips_llm(self):
        """Listicle page with ONLY naked handles (no URL handles) → SKIP.
        Total handles > 0, so LLMExtractionService not needed."""
        page = _page("https://example.com/top-fitness-influencers")
        assert needs_llm(page, {page.url: 0}, {page.url: 10}) is False

    def test_failed_page_never_triggers(self):
        page = _page("https://example.com/top-influencers", success=False)
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is False

    def test_empty_content_never_triggers(self):
        page = _page("https://example.com/top-influencers", fit_md="   ")
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is False


# ══════════════════════════════════════════════════════════════════════
# _regex_extract() — static method
# ══════════════════════════════════════════════════════════════════════

class TestRegexExtract:
    """Tests for HandleExtractionService._regex_extract()."""

    def test_extracts_ig_handle_from_url(self):
        raw = '<a href="https://instagram.com/kayla_itsines">profile</a>'
        page = _page("https://listicle.com/page", raw_md=raw)
        handles, naked, yt_ids, url_counts, naked_counts = \
            HandleExtractionService._regex_extract([page])
        assert any(
            "kayla_itsines" in inf.handles.values()
            for inf in handles
        )
        assert url_counts[page.url] >= 1
        assert naked_counts[page.url] == 0

    def test_extracts_naked_handles(self):
        raw = "Follow @fit_guru_2025 and @yoga_daily for tips"
        page = _page("https://blog.com/article", raw_md=raw)
        handles, naked, yt_ids, url_counts, naked_counts = \
            HandleExtractionService._regex_extract([page])
        assert naked_counts[page.url] >= 2
        assert len(naked) >= 2

    def test_extracts_youtube_channel_ids(self):
        raw = '<a href="https://youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">channel</a>'
        page = _page("https://listicle.com/page", raw_md=raw)
        _, _, yt_ids, _, _ = HandleExtractionService._regex_extract([page])
        assert "UC4qk9TtGhBKCkoWz5qGJcGg" in yt_ids

    def test_skips_failed_pages(self):
        page = _page("https://failed.com", success=False, raw_md="@handle")
        handles, naked, yt_ids, url_counts, naked_counts = \
            HandleExtractionService._regex_extract([page])
        assert len(handles) == 0

    def test_skips_empty_pages(self):
        page = _page("https://empty.com", raw_md="")
        handles, naked, yt_ids, url_counts, naked_counts = \
            HandleExtractionService._regex_extract([page])
        assert len(handles) == 0


# ══════════════════════════════════════════════════════════════════════
# _merge_handles() — static method
# ══════════════════════════════════════════════════════════════════════

class TestMergeHandles:
    """Tests for HandleExtractionService._merge_handles()."""

    def test_merges_all_sources(self):
        direct = [ExtractedHandle(handle="direct_user", platform="Instagram")]
        regex = [Influencer(name="Regex User", handles={Platform.TikTok: "regex_user"})]
        llm = {
            "https://page.com": [
                Influencer(name="LLM User", handles={Platform.Instagram: "llm_user"}),
            ]
        }
        merged = HandleExtractionService._merge_handles(
            direct_handles=direct,
            regex_handles=regex,
            llm_handles=llm,
        )
        all_handle_values = set()
        for inf in merged:
            all_handle_values.update(inf.handles.values())
        assert "direct_user" in all_handle_values
        assert "regex_user" in all_handle_values
        assert "llm_user" in all_handle_values

    def test_empty_sources_returns_empty(self):
        merged = HandleExtractionService._merge_handles(
            direct_handles=[], regex_handles=[], llm_handles={},
        )
        assert merged == []

    def test_direct_handles_converted_to_influencers(self):
        direct = [
            ExtractedHandle(handle="my_handle", platform="TikTok", name="My Name"),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=direct, regex_handles=[], llm_handles={},
        )
        assert len(merged) == 1
        assert merged[0].name == "My Name"
        assert Platform.TikTok in merged[0].handles
        assert merged[0].handles[Platform.TikTok] == "my_handle"

    def test_direct_handle_without_name_uses_handle(self):
        direct = [
            ExtractedHandle(handle="handleonly", platform="Instagram", name=""),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=direct, regex_handles=[], llm_handles={},
        )
        assert merged[0].name == "handleonly"


# ══════════════════════════════════════════════════════════════════════
# classify_by_context() — mechanical platform assignment
# ══════════════════════════════════════════════════════════════════════

class TestClassifyByContext:
    """Tests for HandleExtractionService.classify_by_context()."""

    def test_single_platform_nearby_assigns(self):
        """'Instagram: @fitguru' → auto-assign Instagram."""
        handle = ExtractedHandle(handle="fitguru", platform="")
        text = "Follow our top picks on Instagram: @fitguru for daily workouts"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com/list")
        assert result == "Instagram"

    def test_tiktok_keyword_assigns(self):
        """'TikTok @dancequeen' → auto-assign TikTok."""
        handle = ExtractedHandle(handle="dancequeen", platform="")
        text = "Best TikTok creators: @dancequeen has amazing choreography"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "TikTok"

    def test_youtube_keyword_assigns(self):
        """'YouTube @vloglife' → auto-assign YouTube."""
        handle = ExtractedHandle(handle="vloglife", platform="")
        text = "Subscribe to their YouTube channel @vloglife for weekly vlogs"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "YouTube"

    def test_two_platforms_nearby_closest_wins(self):
        """'Instagram and TikTok: @fitguru' → TikTok wins (closest within 20 chars)."""
        handle = ExtractedHandle(handle="fitguru", platform="")
        text = "Find them on Instagram and TikTok: @fitguru posts daily"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "TikTok"  # TikTok is closer to @fitguru

    def test_no_context_returns_empty(self):
        """No page text at all → '' (unclassified, no LLM)."""
        handle = ExtractedHandle(handle="mystery", platform="")
        result = HandleExtractionService.classify_by_context(handle, "", "")
        assert result == ""

    def test_no_platform_keywords_returns_empty(self):
        """Text exists but zero platform mentions → '' (unclassified)."""
        handle = ExtractedHandle(handle="fitguru", platform="")
        text = "Check out @fitguru for great content and tips every day"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com/tips")
        assert result == ""

    def test_page_url_instagram_assigns(self):
        """Page URL is instagram.com → auto-assign Instagram."""
        handle = ExtractedHandle(handle="yogalife", platform="")
        text = "@yogalife posts great content"
        result = HandleExtractionService.classify_by_context(
            handle, text, "https://www.instagram.com/explore/tags/yoga"
        )
        assert result == "Instagram"

    def test_page_url_tiktok_assigns(self):
        """Page URL is tiktok.com → auto-assign TikTok."""
        handle = ExtractedHandle(handle="dancer99", platform="")
        text = "@dancer99 goes viral"
        result = HandleExtractionService.classify_by_context(
            handle, text, "https://www.tiktok.com/discover/dance"
        )
        assert result == "TikTok"

    def test_emoji_camera_close_assigns_instagram(self):
        """📸 emoji right next to handle (≤5 chars) → Instagram."""
        handle = ExtractedHandle(handle="photo_pro", platform="")
        text = "📸 @photo_pro shares amazing shots daily"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "Instagram"

    def test_emoji_music_close_assigns_tiktok(self):
        """🎵 emoji right next to handle (≤5 chars) → TikTok."""
        handle = ExtractedHandle(handle="beatmaker", platform="")
        text = "🎵 @beatmaker drops fire content"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "TikTok"

    def test_emoji_video_far_does_not_classify(self):
        """🎥 emoji >5 chars from handle → NOT classified (the 21skillshub false positive bug).
        Page has both Instagram and YouTube (via 🎥) so proximity check fires."""
        handle = ExtractedHandle(handle="21skillshub", platform="")
        text = (
            "Top Instagram food bloggers\n"
            "Food & Lifestyle 🎥 content creator @21skillshub Co-Founder"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://joliapp.com/food")
        # 🎥 is closest but >5 chars away (emoji threshold), "Instagram" is >20 chars away
        assert result is None  # Both too far → ambiguous

    def test_yt_shorthand_assigns_youtube(self):
        """'YT' shorthand should classify as YouTube."""
        handle = ExtractedHandle(handle="vlogchannel", platform="")
        text = "Check out my YT channel @vlogchannel for weekly vlogs"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "YouTube"

    def test_platform_outside_100_chars_uses_full_page(self):
        """Platform keyword 200+ chars away not in local window, but found via full-page scan."""
        handle = ExtractedHandle(handle="faraway", platform="")
        padding = "x" * 200
        text = f"Instagram list: {padding} @faraway does stuff"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com/article")
        # Full-page scan finds "Instagram" (only platform) → auto-assign
        assert result == "Instagram"

    def test_no_platform_anywhere_returns_empty(self):
        """No platform keywords in local window, full page, or URL → unclassified."""
        handle = ExtractedHandle(handle="someone", platform="")
        text = "Check out @someone for great content and tips every day"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com/tips")
        assert result == ""


# ══════════════════════════════════════════════════════════════════════
# classify_by_context — full-page keyword frequency tests
# ══════════════════════════════════════════════════════════════════════

class TestClassifyByContextFullPage:
    """Tests for the page-level + local-window classification cascade."""

    def test_single_platform_on_page_assigns(self):
        """Only one platform keyword in entire page → auto-assign."""
        handle = ExtractedHandle(handle="faraway", platform="")
        padding = "x" * 200
        text = f"Top Instagram Influencers: {padding} @faraway does stuff"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "Instagram"

    def test_two_platforms_on_page_one_local_assigns(self):
        """2 platforms on page, but only 1 within 100 chars → assign the local one."""
        handle = ExtractedHandle(handle="fitguru", platform="")
        # TikTok near handle, Instagram far away
        text = (
            "Instagram influencers list "
            + "x" * 200
            + " TikTok: @fitguru posts daily"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result == "TikTok"  # Local disambiguator wins

    def test_two_platforms_on_page_none_local_goes_to_llm(self):
        """2 platforms on page, 0 within 100 chars → ambiguous → LLM."""
        handle = ExtractedHandle(handle="fitguru", platform="")
        text = (
            "Instagram and TikTok creators "
            + "x" * 200
            + " @fitguru posts daily"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result is None  # Ambiguous → LLM

    def test_two_platforms_on_page_both_local_equidistant(self):
        """2 platforms on page, both within 100 chars and equidistant → may resolve or ambiguous."""
        handle = ExtractedHandle(handle="creator", platform="")
        text = "Instagram and TikTok: @creator daily content"
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        # Both platforms within ~20 chars, equidistant — closest-platform may pick one
        assert result is None or result in ("Instagram", "TikTok")

    def test_two_platforms_closest_within_20_chars_wins(self):
        """2 platforms in 100-char window, but 'Instagram' is right next to handle → assign Instagram.
        This is the real joliapp sabihadivan bug reproduction."""
        handle = ExtractedHandle(handle="sabihadivan", platform="")
        text = (
            "[ @sabdivan ](https://www.tiktok.com/@sabdivan)\n"
            "Follow me on Instagram @sabihadivan for food inspo, travel blogs and reviews!"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://joliapp.com/london/food-influencers/")
        assert result == "Instagram"

    def test_two_platforms_closest_tiktok_within_20_chars_wins(self):
        """2 platforms in 100-char window, but 'TikTok' is right next to handle → assign TikTok."""
        handle = ExtractedHandle(handle="dancer99", platform="")
        text = (
            "Follow on Instagram @photopro for shots!\n"
            "Also on TikTok @dancer99 for dance content"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://listicle.com/creators")
        assert result == "TikTok"

    def test_two_platforms_both_far_from_handle_stays_ambiguous(self):
        """2 platforms in 100-char window but both > 20 chars away → ambiguous → LLM."""
        handle = ExtractedHandle(handle="ambiguous_creator", platform="")
        text = (
            "Instagram stars and TikTok legends "
            + "x" * 30
            + " @ambiguous_creator posts daily"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com")
        assert result is None  # Both > 20 chars away → LLM

    def test_title_only_platform_assigns(self):
        """Page title says 'Instagram' but handle far from title → page-level finds it."""
        handle = ExtractedHandle(handle="foodie99", platform="")
        text = (
            "<h1>Top 10 Instagram Food Influencers</h1>\n"
            + "x" * 300
            + "\n@foodie99 shares amazing recipes!"
        )
        result = HandleExtractionService.classify_by_context(handle, text, "https://blog.com/list")
        assert result == "Instagram"


# ══════════════════════════════════════════════════════════════════════
# _merge_handles — deduplication tests
# ══════════════════════════════════════════════════════════════════════

class TestMergeHandlesDedup:
    """Tests for deduplication in _merge_handles()."""

    def test_duplicate_from_ddg_and_regex_deduped(self):
        """Same handle from DDG + regex → only 1 in output."""
        direct = [ExtractedHandle(handle="kayla_itsines", platform="Instagram")]
        regex = [Influencer(name="Kayla", handles={Platform.Instagram: "kayla_itsines"})]
        merged = HandleExtractionService._merge_handles(
            direct_handles=direct, regex_handles=regex, llm_handles={},
        )
        kayla = [inf for inf in merged if "kayla_itsines" in inf.handles.values()]
        assert len(kayla) == 1

    def test_duplicate_from_llm_and_regex_deduped(self):
        """Same handle from LLM + regex → only 1 in output (LLM wins)."""
        regex = [Influencer(name="Kayla", handles={Platform.Instagram: "kayla_itsines"})]
        llm = {
            "https://page.com": [
                Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}),
            ]
        }
        merged = HandleExtractionService._merge_handles(
            direct_handles=[], regex_handles=regex, llm_handles=llm,
        )
        kayla = [inf for inf in merged if "kayla_itsines" in inf.handles.values()]
        assert len(kayla) == 1
        assert kayla[0].name == "Kayla Itsines"  # LLM version kept (first)

    def test_cross_platform_handles_preserved(self):
        """Same handle on different platforms → both kept."""
        regex = [
            Influencer(name="Lady", handles={Platform.Instagram: "ladyofashion"}),
            Influencer(name="Lady", handles={Platform.TikTok: "ladyofashion"}),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=[], regex_handles=regex, llm_handles={},
        )
        lady = [inf for inf in merged if "ladyofashion" in inf.handles.values()]
        assert len(lady) == 2
        platforms = set()
        for inf in lady:
            platforms.update(inf.handles.keys())
        assert platforms == {Platform.Instagram, Platform.TikTok}

    def test_case_insensitive_dedup(self):
        """Handles that differ only in case are deduped."""
        regex = [
            Influencer(name="MrBeast", handles={Platform.YouTube: "MrBeast"}),
            Influencer(name="mrbeast", handles={Platform.YouTube: "mrbeast"}),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=[], regex_handles=regex, llm_handles={},
        )
        beast = [inf for inf in merged
                 if any(v.lower() == "mrbeast" for v in inf.handles.values())]
        assert len(beast) == 1

    def test_triple_source_dedup(self):
        """Same handle from all 3 sources → only 1 in output."""
        direct = [ExtractedHandle(handle="fit_guru", platform="Instagram")]
        regex = [Influencer(name="FitGuru", handles={Platform.Instagram: "fit_guru"})]
        llm = {
            "https://page.com": [
                Influencer(name="Fit Guru", handles={Platform.Instagram: "fit_guru"}),
            ]
        }
        merged = HandleExtractionService._merge_handles(
            direct_handles=direct, regex_handles=regex, llm_handles=llm,
        )
        guru = [inf for inf in merged if "fit_guru" in inf.handles.values()]
        assert len(guru) == 1
        assert guru[0].name == "Fit Guru"  # LLM version kept (first priority)


# ══════════════════════════════════════════════════════════════════════
# HandleClassifier (mocked LLM — moved from test_conditional_llm.py)
# ══════════════════════════════════════════════════════════════════════

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch


class TestHandleClassifier:
    """Test HandleClassifier with mocked LLM responses."""

    def test_classifies_handles_from_llm_response(self):
        """LLM returns platform classifications → handles updated."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="kayla_itsines", platform="", name=""),
            ExtractedHandle(handle="MrBeast", platform="", name=""),
            ExtractedHandle(handle="dancequeen", platform="", name=""),
        ]

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps([
            {"handle": "kayla_itsines", "platform": "Instagram"},
            {"handle": "MrBeast", "platform": "YouTube"},
            {"handle": "dancequeen", "platform": "TikTok"},
        ])

        with patch("services.extraction.HandleClassifier.litellm") as mock_litellm, \
             patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "fake-key"):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == "Instagram"
        assert result[1].platform == "YouTube"
        assert result[2].platform == "TikTok"

    def test_unknown_platform_left_unchanged(self):
        """LLM returns 'unknown' → handle platform stays empty."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="ambiguous_user", platform="", name=""),
        ]

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps([
            {"handle": "ambiguous_user", "platform": "unknown"},
        ])

        with patch("services.extraction.HandleClassifier.litellm") as mock_litellm, \
             patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "fake-key"):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == ""  # Unchanged

    def test_empty_handles_returns_empty(self):
        """No handles to classify → returns empty."""
        from services.extraction.HandleClassifier import classify_handles
        result = asyncio.run(classify_handles([]))
        assert result == []

    def test_llm_failure_returns_unmodified(self):
        """LLM call fails → handles returned unmodified."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="fit_guru", platform="", name=""),
        ]

        with patch("services.extraction.HandleClassifier.litellm") as mock_litellm, \
             patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "fake-key"):
            mock_litellm.acompletion = AsyncMock(side_effect=Exception("API error"))
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == ""  # Unchanged
        assert result[0].handle == "fit_guru"

    def test_no_api_key_skips_classification(self):
        """No API key → skip classification, return unmodified."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="someone", platform="", name=""),
        ]

        with patch("services.extraction.HandleClassifier.GEMINI_API_KEY", ""):
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == ""

    def test_llm_markdown_code_block_response(self):
        """LLM wraps JSON in ```json``` code block → still parsed."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="yoga_life", platform="", name=""),
        ]

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '```json\n[{"handle": "yoga_life", "platform": "Instagram"}]\n```'

        with patch("services.extraction.HandleClassifier.litellm") as mock_litellm, \
             patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "fake-key"):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == "Instagram"

    def test_twitter_platform_rejected(self):
        """LLM returns 'Twitter' → handle stays unclassified (not a supported platform)."""
        from services.extraction.HandleClassifier import classify_handles

        handles = [
            ExtractedHandle(handle="news_daily", platform="", name=""),
        ]

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = json.dumps([
            {"handle": "news_daily", "platform": "Twitter"},
        ])

        with patch("services.extraction.HandleClassifier.litellm") as mock_litellm, \
             patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "fake-key"):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)
            result = asyncio.run(classify_handles(handles))

        assert result[0].platform == ""  # Twitter not supported → stays unclassified


# ══════════════════════════════════════════════════════════════════════
# assign_names_from_headings() — heading-proximity name extraction
# ══════════════════════════════════════════════════════════════════════

class TestAssignNamesFromHeadings:
    """Tests for assign_names_from_headings()."""

    def test_joliapp_style_assigns_names(self):
        """Joliapp-style markdown: heading per influencer → names assigned."""
        handles = [
            ExtractedHandle(handle="sophsplantkitchen", platform="Instagram"),
            ExtractedHandle(handle="sabihadivan", platform=""),
        ]
        text = (
            "### Sophie's Plant Kitchen\n"
            "[ @sophsplantkitchen ](https://www.instagram.com/sophsplantkitchen)\n"
            "Vegan food blogger based in London\n\n"
            "### Sabiha Divan\n"
            "Follow me on Instagram @sabihadivan for food inspo\n"
        )
        assign_names_from_headings(handles, text)
        assert handles[0].name == "Sophie's Plant Kitchen"
        assert handles[1].name == "Sabiha Divan"

    def test_existing_name_not_overwritten(self):
        """Handle with a real name (from IG embed) is not overwritten."""
        handles = [
            ExtractedHandle(handle="kayla_itsines", platform="Instagram", name="Kayla Itsines"),
        ]
        text = "### Wrong Name\n@kayla_itsines posts daily"
        assign_names_from_headings(handles, text)
        assert handles[0].name == "Kayla Itsines"  # Unchanged

    def test_section_title_headings_skipped(self):
        """Headings like 'Top 10 Food Influencers' are not person names."""
        handles = [
            ExtractedHandle(handle="fitguru", platform="Instagram"),
        ]
        text = (
            "## Top 10 Food Influencers in London\n"
            "Here are our picks:\n"
            "@fitguru is amazing\n"
        )
        assign_names_from_headings(handles, text)
        assert handles[0].name == ""  # No valid heading → unchanged

    def test_no_headings_returns_unchanged(self):
        """Page with no headings → names unchanged."""
        handles = [
            ExtractedHandle(handle="fitguru", platform="Instagram"),
        ]
        text = "@fitguru posts amazing content daily"
        assign_names_from_headings(handles, text)
        assert handles[0].name == ""  # No headings → unchanged

    def test_heading_too_far_not_assigned(self):
        """Heading more than 500 chars before handle → not assigned."""
        handles = [
            ExtractedHandle(handle="faraway", platform="Instagram"),
        ]
        text = (
            "### Some Person\n"
            + "x" * 600
            + "\n@faraway does stuff"
        )
        assign_names_from_headings(handles, text)
        assert handles[0].name == ""  # Too far → unchanged
