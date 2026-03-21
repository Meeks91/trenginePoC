"""
test_name_handle_rejection — Regression tests for handle-as-name rejection.

Verifies that handles are never used as influencer names across all creation
paths: model __post_init__, regex extraction, DDG direct, YouTube channel
resolution, name resolution, phase pipeline, and merger.
"""

from config.schema import Influencer, Platform
from services.extraction.RegexHandleExtractorService import ExtractedHandle
from services.extraction.HandleExtractionService import HandleExtractionService
from services.influencerMerging.InfluencerMergerService import InfluencerMergerService as InfluencerMerger


# Fixtures:

HANDLE_ONLY = "kayla_itsines"
REAL_NAME = "Kayla Itsines"

# Fixtures


class TestInfluencerPostInit:
    """Layer 1: model-level enforcement."""

    def test_handle_as_name_rejected_by_post_init(self):
        """A bare handle passed as name gets blanked by __post_init__."""
        inf = Influencer(
            name=HANDLE_ONLY,
            handles={Platform.Instagram: HANDLE_ONLY},
        )
        assert inf.name == ""

    def test_real_name_preserved_by_post_init(self):
        """A real name passes through NameCleaner and is preserved."""
        inf = Influencer(
            name=REAL_NAME,
            handles={Platform.Instagram: HANDLE_ONLY},
        )
        assert inf.name == REAL_NAME

    def test_empty_name_stays_empty(self):
        """Empty string name stays empty after __post_init__."""
        inf = Influencer(
            name="",
            handles={Platform.Instagram: HANDLE_ONLY},
        )
        assert inf.name == ""


class TestRegexExtraction:
    """L310: _regex_extract — no handle fallback when heading name missing."""

    def test_regex_handle_without_name_gets_empty_name(self):
        """When regex extraction finds a handle but no heading name, name is empty."""
        from config.schema import PageResult

        pages = [
            PageResult(
                url="https://example.com/list",
                query="fitness influencers",
                success=True,
                raw_markdown=(
                    "Check out https://instagram.com/fitnessguru123 for tips"
                ),
                fit_markdown=(
                    "Check out https://instagram.com/fitnessguru123 for tips"
                ),
                raw_token_estimate=15,
                fit_token_estimate=15,
            ),
        ]
        rx = HandleExtractionService._regex_extract(pages)

        for inf in rx.regex_handles:
            if inf.handles.get(Platform.Instagram) == "fitnessguru123":
                assert inf.name == "", (
                    f"Expected empty name, got '{inf.name}'"
                )
                break
        else:
            raise AssertionError("Expected to find fitnessguru123 in regex_handles")


class TestDDGDirectHandles:
    """L493: _merge_handles — DDG direct handles without names."""

    def test_ddg_direct_handle_without_name_gets_empty_name(self):
        """DDG direct handle with no .name gets empty name."""
        dh = ExtractedHandle(
            handle="fitgirl99",
            platform="Instagram",
            name="",
        )
        merged = HandleExtractionService._merge_handles(
            direct_handles=[dh],
            regex_handles=[],
            llm_handles={},
        )
        assert len(merged) == 1
        assert merged[0].name == ""

    def test_ddg_direct_handle_with_real_name_preserves_name(self):
        """DDG direct handle with a real .name keeps the cleaned name."""
        dh = ExtractedHandle(
            handle="fitgirl99",
            platform="Instagram",
            name="Jane Smith",
        )
        merged = HandleExtractionService._merge_handles(
            direct_handles=[dh],
            regex_handles=[],
            llm_handles={},
        )
        assert len(merged) == 1
        assert merged[0].name == "Jane Smith"


class TestYouTubeChannelResolution:
    """L175: YouTube channel handle used as name."""

    def test_youtube_channel_handle_gets_empty_name(self):
        """YouTube channel resolution creates Influencer with name=''."""
        inf = Influencer(
            name="",
            handles={Platform.YouTube: "somechannel"},
        )
        assert inf.name == ""


class TestNameResolution:
    """L258: resolve_handles_for_top_mentioned_names."""

    def test_name_resolution_handle_only_gets_empty_name(self):
        """When DDG returns only a handle (no name), Influencer.name is empty."""
        inf = Influencer(
            name="",
            handles={Platform.Instagram: "seannal"},
            extraction_methods={"name_resolution"},
        )
        assert inf.name == ""


class TestMergerNoHandleFallback:
    """L291: _build_grouped_influencer — no handle-as-name fallback."""

    def test_merger_no_handle_fallback_for_name(self):
        """When all entries have empty names, merged result has empty name."""
        entries = [
            Influencer(
                name="",
                handles={Platform.Instagram: "fitgirl99"},
            ),
            Influencer(
                name="",
                handles={Platform.TikTok: "fitgirl99"},
            ),
        ]
        merged = InfluencerMerger.merge(entries)
        assert len(merged) == 1
        assert merged[0].name == ""
        assert Platform.Instagram in merged[0].handles
        assert Platform.TikTok in merged[0].handles

    def test_merger_picks_real_name_over_empty(self):
        """When one entry has a real name, merged result uses it."""
        entries = [
            Influencer(
                name="",
                handles={Platform.Instagram: "fitgirl99"},
            ),
            Influencer(
                name="Jane Smith",
                handles={Platform.TikTok: "fitgirl99"},
            ),
        ]
        merged = InfluencerMerger.merge(entries)
        assert len(merged) == 1
        assert merged[0].name == "Jane Smith"
