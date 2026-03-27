"""
Unit tests for enrichment patterns — URL handle extraction (delegated to
RegexHandleExtractor) and text @handle extraction.
"""

from __future__ import annotations

import pytest

from services.handleResolution.patterns import (
    extract_handle_from_url,
    extract_handle_from_text,
    PLATFORM_DOMAINS,
)
from config.schema import Platform


# Fixtures:

INSTAGRAM_URLS = [
    ("https://www.instagram.com/kayla_itsines/", "kayla_itsines"),
    ("https://instagram.com/Fitguru", "fitguru"),
]

TIKTOK_URLS = [
    ("https://www.tiktok.com/@charlidamelio", "charlidamelio"),
    ("https://tiktok.com/@dance_queen/", "dance_queen"),
]

YOUTUBE_URLS = [
    ("https://www.youtube.com/@mkbhd", "mkbhd"),
    ("https://youtube.com/c/PewDiePie", "pewdiepie"),
]

JUNK_URLS = [
    ("https://instagram.com/explore/", "Instagram"),
    ("https://instagram.com/reel/abc123", "Instagram"),
    ("https://tiktok.com/foryou", "TikTok"),
    ("https://youtube.com/watch?v=abc123", "YouTube"),
    ("https://youtube.com/feed/subscriptions", "YouTube"),
]

# Fixtures


class TestExtractHandleFromUrl:

    @pytest.mark.parametrize("url,expected", INSTAGRAM_URLS)
    def test_instagram_urls(self, url: str, expected: str):
        assert extract_handle_from_url(url=url, platform="Instagram") == expected

    @pytest.mark.parametrize("url,expected", TIKTOK_URLS)
    def test_tiktok_urls(self, url: str, expected: str):
        assert extract_handle_from_url(url=url, platform="TikTok") == expected

    @pytest.mark.parametrize("url,expected", YOUTUBE_URLS)
    def test_youtube_urls(self, url: str, expected: str):
        assert extract_handle_from_url(url=url, platform="YouTube") == expected

    @pytest.mark.parametrize("url,platform", JUNK_URLS)
    def test_junk_paths_return_none(self, url: str, platform: str):
        assert extract_handle_from_url(url=url, platform=platform) is None

    def test_wrong_platform_filter_returns_none(self):
        assert extract_handle_from_url(
            url="https://instagram.com/fitguru",
            platform="TikTok",
        ) is None

    def test_non_social_url_returns_none(self):
        assert extract_handle_from_url(
            url="https://example.com/fitguru",
            platform="Instagram",
        ) is None


class TestExtractHandleFromText:

    def test_extracts_at_handle(self):
        assert extract_handle_from_text("Follow @fitguru for tips") == "fitguru"

    def test_returns_none_for_no_handle(self):
        assert extract_handle_from_text("No handles here") is None

    def test_returns_none_for_short_handle(self):
        assert extract_handle_from_text("@ab is too short") is None

    def test_handles_multiple_returns_first(self):
        assert extract_handle_from_text("@first and @second") == "first"

    def test_lowercases_handle(self):
        assert extract_handle_from_text("@FitGuru") == "fitguru"


class TestPlatformDomains:

    def test_all_platforms_have_domains(self):
        assert Platform.Instagram in PLATFORM_DOMAINS
        assert Platform.TikTok in PLATFORM_DOMAINS
        assert Platform.YouTube in PLATFORM_DOMAINS

    def test_domain_values(self):
        assert PLATFORM_DOMAINS[Platform.Instagram] == "instagram.com"
        assert PLATFORM_DOMAINS[Platform.TikTok] == "tiktok.com"
        assert PLATFORM_DOMAINS[Platform.YouTube] == "youtube.com"
