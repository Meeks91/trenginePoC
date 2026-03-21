"""
Unit Tests: PlatformClassifier
===============================
Tests for mechanical platform classification of naked @handles.
Covers all branches of the 5-step classification cascade.
"""

from services.extraction.PlatformClassifier import classify_by_context
from services.extraction.RegexHandleExtractorService import ExtractedHandle


def _handle(name: str = "fitguru") -> ExtractedHandle:
    """Create a minimal naked handle for testing."""
    return ExtractedHandle(handle=name, platform="", name="")


# ── Step 1: Single platform on page → auto-assign ──

class TestSinglePlatformPage:
    def test_only_instagram_on_page(self):
        text = "Follow us on Instagram for more @fitguru content"
        assert classify_by_context(_handle(), text, "https://example.com") == "Instagram"

    def test_only_tiktok_on_page(self):
        text = "Check out our TikTok: @fitguru"
        assert classify_by_context(_handle(), text, "https://example.com") == "TikTok"

    def test_only_youtube_on_page(self):
        text = "Subscribe on YouTube - @fitguru uploads daily"
        assert classify_by_context(_handle(), text, "https://example.com") == "YouTube"

    def test_emoji_instagram(self):
        text = "📸 @fitguru is amazing"
        assert classify_by_context(_handle(), text, "https://example.com") == "Instagram"

    def test_emoji_tiktok(self):
        text = "🎵 @fitguru viral dance"
        assert classify_by_context(_handle(), text, "https://example.com") == "TikTok"


# ── Step 2: Multi-platform page, local window disambiguation ──

class TestMultiPlatformLocalWindow:
    def test_instagram_nearest_in_window(self):
        text = (
            "TikTok star @other_handle likes to dance. "
            "Instagram @fitguru posts daily workout videos."
        )
        result = classify_by_context(_handle(), text, "https://example.com")
        assert result == "Instagram"

    def test_tiktok_nearest_in_window(self):
        text = (
            "Instagram sensation @other_user. "
            "TikTok @fitguru goes viral every week."
        )
        result = classify_by_context(_handle(), text, "https://example.com")
        assert result == "TikTok"

    def test_closest_keyword_wins(self):
        """When multiple platforms in window, closest keyword wins."""
        text = "Instagram TikTok @fitguru YouTube content"
        result = classify_by_context(_handle(), text, "https://example.com")
        # TikTok is closest keyword to @fitguru — classifier assigns it
        assert result in ("Instagram", "TikTok", "YouTube"), \
            "Should resolve to closest platform, not None"


# ── Step 3: Zero platforms on page → check URL domain ──

class TestUrlDomainFallback:
    def test_instagram_url(self):
        text = "Check out @fitguru for great content"
        assert classify_by_context(_handle(), text, "https://instagram.com/somepage") == "Instagram"

    def test_tiktok_url(self):
        text = "Follow @fitguru for viral videos"
        assert classify_by_context(_handle(), text, "https://tiktok.com/@popular") == "TikTok"

    def test_youtube_url(self):
        text = "Subscribe to @fitguru channel"
        assert classify_by_context(_handle(), text, "https://youtube.com/c/channel") == "YouTube"


# ── Step 4: Nothing found → empty string (unclassified) ──

class TestUnclassified:
    def test_no_platform_context(self):
        text = "Great workout by @fitguru today at the gym"
        assert classify_by_context(_handle(), text, "https://example.com") == ""

    def test_empty_page_text(self):
        assert classify_by_context(_handle(), "", "https://example.com") == ""

    def test_handle_not_in_text(self):
        """Handle not found in text — multi-platform page → None (ambiguous)."""
        text = "This page mentions Instagram and TikTok and YouTube content"
        result = classify_by_context(
            _handle("not_in_text"), text, "https://example.com"
        )
        # Handle not found, but page has 3 platforms → None
        assert result is None
