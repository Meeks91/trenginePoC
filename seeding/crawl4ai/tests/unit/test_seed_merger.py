"""Tests for InfluencerMerger — merge() + filter_blocked() + Influencer.to_dict().

Influencer carries computed properties (ig_handle, tk_handle, yt_handle)
and to_dict() for DB serialization.
"""

from config.schema import Influencer, Platform
from services.enrichment.InfluencerMerger import InfluencerMerger


class TestInfluencerMergeAndSerialize:
    """Tests for merge() + filter_blocked() + to_dict() pipeline."""

    def test_single_influencer_single_platform(self):
        """One person with one platform → 1 result after filter."""
        influencers = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                categories_found_in=["FITNESS"],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "kayla_itsines"
        assert sorted(result[0].categories_found_in) == ["FITNESS"]

    def test_multi_platform_single_result(self):
        """One person with handles on 3 platforms → 1 result with all handles."""
        influencers = [
            Influencer(
                name="Adriene Mishler",
                handles={
                    Platform.Instagram: "adrienelouise",
                    Platform.YouTube: "yogawithadriene",
                    Platform.TikTok: "adrienelouise",
                },
                categories_found_in=["FITNESS", "YOGA"],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        assert sorted(result[0].categories_found_in) == ["FITNESS", "YOGA"]

    def test_merge_then_filter_deduplicates(self):
        """merge() + filter_blocked() pipeline: same person on 3 platforms → 1 result."""
        raw = [
            Influencer(
                name="Adriene Mishler",
                handles={Platform.Instagram: "adrienelouise"},
                categories_found_in=["FITNESS"],
            ),
            Influencer(
                name="Adriene Mishler",
                handles={Platform.YouTube: "yogawithadriene"},
                categories_found_in=["FITNESS"],
            ),
            Influencer(
                name="Adriene Mishler",
                handles={Platform.TikTok: "adrienelouise"},
                categories_found_in=["YOGA"],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        result = InfluencerMerger.filter_blocked(merged)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        assert sorted(result[0].categories_found_in) == ["FITNESS", "YOGA"]

    def test_categories_from_influencer(self):
        """Categories read from categories_found_in."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "chef_x"},
                categories_found_in=["FOOD", "FITNESS", "HEALTH"],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert sorted(result[0].categories_found_in) == ["FITNESS", "FOOD", "HEALTH"]

    def test_at_sign_stripped_in_to_dict(self):
        """Leading @ does not affect computed properties (handles stored raw)."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "@chefanna"},
                categories_found_in=["FOOD"],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "@chefanna"

    def test_empty_input(self):
        """Empty input returns empty output."""
        assert InfluencerMerger.filter_blocked([]) == []

    def test_handleless_influencer_skipped(self):
        """Influencer with no handles → skipped."""
        influencers = [
            Influencer(name="X", handles={}, categories_found_in=["FOOD"]),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 0

    def test_enrichment_fields_carried(self):
        """source_urls and extraction_methods carried through filter."""
        influencers = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://modash.io/yoga", "https://favikon.com/fitness"},
                extraction_methods={"regex", "llm"},
                categories_found_in=["FITNESS"],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        inf = result[0]
        assert sorted(inf.source_urls) == ["https://favikon.com/fitness", "https://modash.io/yoga"]
        assert sorted(inf.extraction_methods) == ["llm", "regex"]
        assert inf.citation_count == 2

    def test_merge_unions_enrichment(self):
        """merge() + filter_blocked(): source_urls and extraction_methods unioned."""
        raw = [
            Influencer(
                name="Kayla",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://a.com"},
                extraction_methods={"regex"},
                categories_found_in=["FITNESS"],
            ),
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://b.com"},
                extraction_methods={"llm"},
                categories_found_in=["FOOD"],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        result = InfluencerMerger.filter_blocked(merged)
        assert len(result) == 1
        inf = result[0]
        assert sorted(inf.source_urls) == ["https://a.com", "https://b.com"]
        assert sorted(inf.extraction_methods) == ["llm", "regex"]
        assert inf.citation_count == 2
        assert inf.name == "Kayla Itsines"

    def test_influencer_to_dict(self):
        """Influencer.to_dict() produces DB-ready shape."""
        inf = Influencer(
            name="Kayla Itsines",
            handles={
                Platform.Instagram: "kayla_itsines",
                Platform.TikTok: "kayla_tt",
                Platform.YouTube: "kaylayt",
            },
            categories_found_in=["FITNESS", "FOOD"],
            source_urls={"https://a.com"},
            extraction_methods={"regex"},
        )
        d = inf.to_dict()
        assert d["ig_handle"] == "kayla_itsines"
        assert d["tk_handle"] == "kayla_tt"
        assert d["yt_handle"] == "kaylayt"
        assert d["categories"] == ["FITNESS", "FOOD"]
        assert d["source_urls"] == ["https://a.com"]
        assert d["extraction_methods"] == ["regex"]
        assert d["citation_count"] == 1
