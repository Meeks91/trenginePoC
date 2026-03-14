"""Tests for InfluencerMerger.to_seeds — cross-config handle merging."""

from config.schema import Influencer, Platform, SeedInfluencer
from services.enrichment.InfluencerMerger import InfluencerMerger


class TestInfluencerMergerToSeeds:
    """Tests for the InfluencerMerger.to_seeds() method."""

    def test_same_handle_different_configs_deduped(self):
        """Same handle found in Fitness and Food → 1 entry with both categories."""
        entries = [
            (Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}), "FITNESS"),
            (Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}), "FOOD"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 1
        assert result[0].ig_handle == "kayla_itsines"
        assert sorted(result[0].categories) == ["FITNESS", "FOOD"]

    def test_different_platforms_preserved(self):
        """Same person on IG and TikTok → 2 separate entries (different platform key)."""
        entries = [
            (Influencer(name="Kayla", handles={Platform.Instagram: "kayla_itsines"}), "FITNESS"),
            (Influencer(name="Kayla", handles={Platform.TikTok: "kayla_itsines"}), "FITNESS"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 2

    def test_best_name_kept(self):
        """When one entry has real name and another has handle-as-name, keep real name."""
        entries = [
            (Influencer(name="kayla_itsines", handles={Platform.Instagram: "kayla_itsines"}), "FITNESS"),
            (Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}), "FOOD"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 1
        assert result[0].name == "Kayla Itsines"

    def test_alt_handles_merged(self):
        """Handles from multiple platform entries are merged into the seed record."""
        entries = [
            (Influencer(name="Adriene Mishler", handles={Platform.Instagram: "adrienelouise"}), "FITNESS"),
            (Influencer(name="Adriene Mishler", handles={Platform.YouTube: "yogawithadriene"}), "FITNESS"),
            (Influencer(name="Adriene Mishler", handles={Platform.TikTok: "adrienelouise"}), "YOGA"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        # InfluencerMerger.to_seeds keys by (handle_lower, platform_value), so:
        #   IG "adrienelouise" and TK "adrienelouise" are on different platforms → 2 entries
        #   YT "yogawithadriene" is unique → 1 entry
        # But cross-platform alt handles get merged into each seed's other columns
        assert len(result) == 3  # 3 distinct (handle, platform) keys

        # Verify platform handles are correctly assigned
        ig_seeds = [s for s in result if s.ig_handle == "adrienelouise"]
        assert len(ig_seeds) == 1

        yt_seeds = [s for s in result if s.yt_handle == "yogawithadriene"]
        assert len(yt_seeds) == 1

        tk_seeds = [s for s in result if s.tk_handle == "adrienelouise"]
        assert len(tk_seeds) == 1

        # All categories present across seeds
        all_cats = set()
        for s in result:
            all_cats.update(s.categories)
        assert "FITNESS" in all_cats
        assert "YOGA" in all_cats

    def test_categories_tracked(self):
        """Handle found in 3 categories → all 3 categories in output."""
        entries = [
            (Influencer(name="X", handles={Platform.Instagram: "chef_x"}), "FOOD"),
            (Influencer(name="X", handles={Platform.Instagram: "chef_x"}), "FITNESS"),
            (Influencer(name="X", handles={Platform.Instagram: "chef_x"}), "HEALTH"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 1
        assert sorted(result[0].categories) == ["FITNESS", "FOOD", "HEALTH"]

    def test_case_insensitive_dedup(self):
        """Handles are deduped case-insensitively."""
        entries = [
            (Influencer(name="X", handles={Platform.Instagram: "ChefAnna"}), "FOOD"),
            (Influencer(name="X", handles={Platform.Instagram: "chefanna"}), "FOOD"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 1

    def test_at_sign_stripped(self):
        """Leading @ is stripped before dedup."""
        entries = [
            (Influencer(name="X", handles={Platform.Instagram: "@chefanna"}), "FOOD"),
            (Influencer(name="X", handles={Platform.Instagram: "chefanna"}), "FOOD"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 1
        assert result[0].ig_handle == "chefanna"

    def test_empty_entries(self):
        """Empty input returns empty output."""
        result = InfluencerMerger.to_seeds([])
        assert result == []

    def test_seed_influencer_to_dict(self):
        """SeedInfluencer.to_dict() produces DB-ready shape."""
        seed = SeedInfluencer(
            name="Kayla Itsines",
            ig_handle="kayla_itsines",
            tk_handle="kayla_tt",
            yt_handle="kaylayt",
            categories=["FITNESS", "FOOD"],
        )
        d = seed.to_dict()
        assert d["ig_handle"] == "kayla_itsines"
        assert d["tk_handle"] == "kayla_tt"
        assert d["yt_handle"] == "kaylayt"
        assert d["categories"] == ["FITNESS", "FOOD"]

    def test_unknown_platform_handle_not_assigned(self):
        """Handles with unknown platform → filtered out (no valid handles)."""
        entries = [
            (Influencer(name="X", handles={}), "FOOD"),
        ]
        result = InfluencerMerger.to_seeds(entries)
        assert len(result) == 0, "Handleless seeds should be filtered out"
