"""
E2E Test: YouTube Channel Resolution
======================================

Tests the full pipeline of:
  1. Extracting UC... channel IDs from HTML
  2. Resolving them to @handles via HTTP to youtube.com

Requires network access — mark with pytest.mark.network.
"""

import asyncio
import pytest
from pathlib import Path

from services.extraction.RegexHandleExtractorService import extract_youtube_channel_ids
from services.extraction.YouTubeChannelResolver import resolve_youtube_channels


FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


# Known channel ID → handle mappings (verified via live HTTP 2026-03-12)
KNOWN_CHANNELS = {
    "UCAxW1XT0iEJo0TYlRfn6rYQ": "TheBodyCoachTV",     # Joe Wicks
    "UCPbyT8IyohY6V8ZVfI9uHug": "LucyDavisFit",       # Lucy Davis
    "UCoAgFgYy2YDLqCj9aHXTXUg": "seancaseyfitness111", # Sean Casey
}


@pytest.mark.network
class TestYouTubeChannelResolution:
    """Test resolve_youtube_channels() with real HTTP to YouTube."""

    def test_resolves_known_channel_ids(self):
        """Known channel IDs should resolve to expected @handles."""
        channel_ids = list(KNOWN_CHANNELS.keys())
        results = asyncio.run(resolve_youtube_channels(channel_ids))

        for cid, expected_handle in KNOWN_CHANNELS.items():
            if cid in results:
                # Case-insensitive comparison
                assert results[cid].lower() == expected_handle.lower(), (
                    f"Channel {cid}: expected @{expected_handle}, got @{results[cid]}"
                )

        # At least some should resolve (network may be unreliable)
        assert len(results) >= 1, (
            f"Expected ≥1 resolved channel, got {len(results)}"
        )

    def test_invalid_channel_id_returns_empty(self):
        """Invalid/nonexistent channel IDs should not crash."""
        results = asyncio.run(resolve_youtube_channels([
            "UCinvalid_not_real_12345",
        ]))
        # Should either be empty or have the ID with None-like result
        assert isinstance(results, dict)

    def test_empty_input_returns_empty(self):
        """No channel IDs → empty result."""
        results = asyncio.run(resolve_youtube_channels([]))
        assert results == {}


class TestYouTubeChannelFromFixture:
    """Test extracting channel IDs from HTML fixtures then resolving."""

    def test_gymfluencers_has_channel_ids(self):
        """Gymfluencers HTML fixture should contain YouTube channel IDs."""
        html = (FIXTURES_DIR / "gymfluencers_uk_fitness.html").read_text(
            errors="replace"
        )
        channel_ids = extract_youtube_channel_ids(html)
        assert len(channel_ids) == 3, (
            f"Expected 3 channel IDs from gymfluencers, got {len(channel_ids)}"
        )
        # All should be UC... format
        for cid in channel_ids:
            assert cid.startswith("UC"), f"Invalid channel ID format: {cid}"

    def test_seekahost_has_channel_ids(self):
        """Seekahost fixture should have YouTube channel IDs."""
        html = (FIXTURES_DIR / "seekahost_uk_fitness.html").read_text(
            errors="replace"
        )
        channel_ids = extract_youtube_channel_ids(html)
        assert len(channel_ids) >= 2, (
            f"Expected ≥2 channel IDs from seekahost, got {len(channel_ids)}"
        )

    def test_modash_has_channel_ids(self):
        """Modash UK food fixture should have YouTube channel IDs."""
        html = (FIXTURES_DIR / "modash_uk_food.html").read_text(
            errors="replace"
        )
        channel_ids = extract_youtube_channel_ids(html)
        assert len(channel_ids) >= 3, (
            f"Expected ≥3 channel IDs from modash, got {len(channel_ids)}"
        )

    @pytest.mark.network
    def test_full_pipeline_fixture_to_handle(self):
        """Full pipeline: HTML fixture → extract channel IDs → resolve to @handles."""
        html = (FIXTURES_DIR / "gymfluencers_uk_fitness.html").read_text(
            errors="replace"
        )
        channel_ids = extract_youtube_channel_ids(html)
        assert len(channel_ids) >= 1

        results = asyncio.run(resolve_youtube_channels(channel_ids))

        # At least 1 should resolve
        assert len(results) >= 1, (
            f"Expected ≥1 resolved channel from gymfluencers, got {len(results)}"
        )

        # All resolved handles should be non-empty strings
        for cid, handle in results.items():
            assert isinstance(handle, str) and len(handle) > 0, (
                f"Invalid handle for {cid}: {handle}"
            )
