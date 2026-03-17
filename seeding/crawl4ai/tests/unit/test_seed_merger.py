"""Tests for InfluencerMerger.to_seeds — merged Influencer → SeedInfluencer.

to_seeds() now accepts list[Influencer] (already merged, one per person).
Deduplication is done by merge() upstream.
"""

from config.schema import Influencer, Platform, SeedInfluencer
from services.enrichment.InfluencerMerger import InfluencerMerger


class TestInfluencerMergerToSeeds:
    """Tests for the simplified InfluencerMerger.to_seeds() method."""

    def test_single_influencer_single_platform(self):
        """One person with one platform → 1 seed."""
        influencers = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                categories_found_in=["FITNESS"],
            ),
        ]
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "kayla_itsines"
        assert result[0].categories == ["FITNESS"]

    def test_multi_platform_single_seed(self):
        """One person with handles on 3 platforms → 1 seed with all handles."""
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
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        assert sorted(result[0].categories) == ["FITNESS", "YOGA"]

    def test_merge_then_to_seeds_deduplicates(self):
        """merge() + to_seeds() pipeline: same person on 3 platforms → 1 seed."""
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
        result = InfluencerMerger.to_seeds(merged)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        assert sorted(result[0].categories) == ["FITNESS", "YOGA"]

    def test_categories_from_influencer(self):
        """Categories read from categories_found_in, not tuple."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "chef_x"},
                categories_found_in=["FOOD", "FITNESS", "HEALTH"],
            ),
        ]
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 1
        assert sorted(result[0].categories) == ["FITNESS", "FOOD", "HEALTH"]

    def test_at_sign_stripped(self):
        """Leading @ is stripped."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "@chefanna"},
                categories_found_in=["FOOD"],
            ),
        ]
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "chefanna"

    def test_empty_input(self):
        """Empty input returns empty output."""
        assert InfluencerMerger.to_seeds([]) == []

    def test_handleless_influencer_skipped(self):
        """Influencer with no handles → skipped."""
        influencers = [
            Influencer(name="X", handles={}, categories_found_in=["FOOD"]),
        ]
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 0

    def test_enrichment_fields_carried(self):
        """source_urls and extraction_methods carried to SeedInfluencer."""
        influencers = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://modash.io/yoga", "https://favikon.com/fitness"},
                extraction_methods={"regex", "llm"},
                categories_found_in=["FITNESS"],
            ),
        ]
        result = InfluencerMerger.to_seeds(influencers)
        assert len(result) == 1
        seed = result[0]
        assert sorted(seed.source_urls) == ["https://favikon.com/fitness", "https://modash.io/yoga"]
        assert sorted(seed.extraction_methods) == ["llm", "regex"]
        assert seed.citation_count == 2

    def test_merge_unions_enrichment(self):
        """merge() + to_seeds(): source_urls and extraction_methods unioned."""
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
        result = InfluencerMerger.to_seeds(merged)
        assert len(result) == 1
        seed = result[0]
        assert sorted(seed.source_urls) == ["https://a.com", "https://b.com"]
        assert sorted(seed.extraction_methods) == ["llm", "regex"]
        assert seed.citation_count == 2
        assert seed.name == "Kayla Itsines"

    def test_seed_to_dict(self):
        """SeedInfluencer.to_dict() produces DB-ready shape."""
        seed = SeedInfluencer(
            name="Kayla Itsines",
            ig_handle="kayla_itsines",
            tk_handle="kayla_tt",
            yt_handle="kaylayt",
            categories=["FITNESS", "FOOD"],
            source_urls=["https://a.com"],
            extraction_methods=["regex"],
        )
        d = seed.to_dict()
        assert d["ig_handle"] == "kayla_itsines"
        assert d["tk_handle"] == "kayla_tt"
        assert d["yt_handle"] == "kaylayt"
        assert d["categories"] == ["FITNESS", "FOOD"]
        assert d["source_urls"] == ["https://a.com"]
        assert d["extraction_methods"] == ["regex"]
        assert d["citation_count"] == 1
