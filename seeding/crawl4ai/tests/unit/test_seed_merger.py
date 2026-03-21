"""Tests for InfluencerMerger — merge() + filter_blocked() + Influencer.to_dict().

Influencer carries computed properties (ig_handle, tk_handle, yt_handle)
and to_dict() for DB serialization.
"""

from config.schema import Influencer, Platform, CategoryCitation
from services.enrichment.InfluencerMerger import InfluencerMerger
from services.extraction.RegexHandleExtractor import is_blocked_handle


class TestInfluencerMergeAndSerialize:
    """Tests for merge() + filter_blocked() + to_dict() pipeline."""

    def test_single_influencer_single_platform(self):
        """One person with one platform → 1 result after filter."""
        influencers = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                ],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "kayla_itsines"
        assert result[0].most_seen_category == "FITNESS"

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
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                    CategoryCitation(category="YOGA", sub="Yoga", citations=1),
                ],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        assert result[0].most_seen_category == "FITNESS"

    def test_merge_then_filter_deduplicates(self):
        """merge() + filter_blocked() pipeline: same person on 3 platforms → 1 result."""
        raw = [
            Influencer(
                name="Adriene Mishler",
                handles={Platform.Instagram: "adrienelouise"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                ],
            ),
            Influencer(
                name="Adriene Mishler",
                handles={Platform.YouTube: "yogawithadriene"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                ],
            ),
            Influencer(
                name="Adriene Mishler",
                handles={Platform.TikTok: "adrienelouise"},
                most_seen_category="YOGA",
                seen_in_categories=[
                    CategoryCitation(category="YOGA", sub="Yoga", citations=1),
                ],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        result = InfluencerMerger.filter_blocked(merged)
        assert len(result) == 1
        assert result[0].ig_handle == "adrienelouise"
        assert result[0].yt_handle == "yogawithadriene"
        assert result[0].tk_handle == "adrienelouise"
        subs = {cc.sub for cc in result[0].seen_in_categories}
        assert "Gym" in subs
        assert "Yoga" in subs

    def test_categories_from_influencer(self):
        """Categories read from seen_in_categories."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "chef_x"},
                most_seen_category="FOOD",
                seen_in_categories=[
                    CategoryCitation(category="FOOD", sub="Cooking", citations=3),
                    CategoryCitation(category="FITNESS", sub="Gym", citations=2),
                    CategoryCitation(category="HEALTH", sub="Wellness", citations=1),
                ],
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].most_seen_category == "FOOD"
        cats = {cc.category for cc in result[0].seen_in_categories}
        assert cats == {"FOOD", "FITNESS", "HEALTH"}

    def test_at_sign_stripped_in_to_dict(self):
        """Leading @ does not affect computed properties (handles stored raw)."""
        influencers = [
            Influencer(
                name="X",
                handles={Platform.Instagram: "@chefanna"},
                most_seen_category="FOOD",
                seen_in_categories=[
                    CategoryCitation(category="FOOD", sub="Cooking", citations=1),
                ],
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
            Influencer(name="X", handles={}, most_seen_category="FOOD"),
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
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                ],
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
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                ],
            ),
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://b.com"},
                extraction_methods={"llm"},
                most_seen_category="FOOD",
                seen_in_categories=[
                    CategoryCitation(category="FOOD", sub="Cooking", citations=1),
                ],
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
            most_seen_category="FITNESS",
            seen_in_categories=[
                CategoryCitation(category="FITNESS", sub="Gym", citations=1),
                CategoryCitation(category="FOOD", sub="Cooking", citations=1),
            ],
            source_urls={"https://a.com"},
            extraction_methods={"regex"},
        )
        d = inf.to_dict()
        assert d["ig_handle"] == "kayla_itsines"
        assert d["tk_handle"] == "kayla_tt"
        assert d["yt_handle"] == "kaylayt"
        assert d["most_seen_category"] == "FITNESS"
        assert len(d["seen_in_categories"]) == 2
        assert d["source_urls"] == ["https://a.com"]
        assert d["extraction_methods"] == ["regex"]
        assert d["citation_count"] == 1


class TestMergeLLMNameGuard:
    """LLM-only entries must not create name-based bucket aliases."""

    def test_merge_rejects_llm_name_cross_contamination(self):
        """Angelica/Jen Selter scenario: LLM error pairs wrong name+handle.

        The LLM extracts adjacent rows on a listicle and pairs
        Angelica Teixeira's name with Jen Selter's TK handle.
        The merger must:
          1. Keep Angelica with only her IG handle
          2. Keep Jen Selter with all her handles and her own name
          3. Drop the bad LLM entry entirely (no ghost record)
        """
        raw = [
            Influencer(
                name="Angelica Teixeira",
                handles={Platform.Instagram: "angelicaht"},
                source_urls={"https://muscleandfitness.com"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Jen Selter",
                handles={Platform.Instagram: "jenselter"},
                source_urls={"https://muscleandfitness.com"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Jen Selter",
                handles={Platform.TikTok: "jenselter"},
                source_urls={"https://feedspot.com"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Jen Selter",
                handles={Platform.YouTube: "JenSelter"},
                source_urls={"https://gymfluencers.agency"},
                extraction_methods={"regex"},
            ),
            # LLM error: Angelica's name paired with Jen Selter's TK handle
            Influencer(
                name="Angelica Teixeira",
                handles={Platform.TikTok: "jenselter"},
                source_urls={"https://gymfluencers.agency"},
                extraction_methods={"llm"},
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        merged = InfluencerMerger.filter_blocked(merged)

        assert len(merged) == 2, f"Expected 2 entries, got {len(merged)}"

        angelica = [m for m in merged if m.ig_handle == "angelicaht"]
        jen = [m for m in merged if m.tk_handle == "jenselter"]

        assert len(angelica) == 1, "Angelica should have exactly 1 record"
        assert angelica[0].tk_handle == "", "Angelica must NOT have jenselter TK"
        assert angelica[0].yt_handle == "", "Angelica must NOT have JenSelter YT"

        assert len(jen) == 1, "Jen Selter should have exactly 1 record"
        assert jen[0].name == "Jen Selter", "Jen Selter must keep her own name"
        assert jen[0].tk_handle == "jenselter"
        assert jen[0].yt_handle == "JenSelter"

    def test_llm_only_entry_no_name_bucket_created(self):
        """LLM-only entry with DIFFERENT name is dropped from existing bucket.

        A regex entry owns handle B under name K. An LLM entry claims
        handle B belongs to name X. Since names differ and LLM is
        unreliable, the LLM entry is dropped.
        """
        raw = [
            Influencer(
                name="Real Person",
                handles={Platform.Instagram: "testperson_ig"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Wrong Person",
                handles={Platform.Instagram: "testperson_ig"},
                extraction_methods={"llm"},
            ),
        ]
        merged = InfluencerMerger.merge(raw)

        assert len(merged) == 1
        assert merged[0].name == "Real Person"
        assert merged[0].ig_handle == "testperson_ig"

    def test_llm_plus_regex_still_merges_by_handle(self):
        """LLM entries with the same handle as regex entries still merge normally."""
        raw = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                extraction_methods={"llm"},
            ),
        ]
        merged = InfluencerMerger.merge(raw)

        assert len(merged) == 1, "Same handle should merge regardless of source"
        assert merged[0].ig_handle == "kayla_itsines"
        assert merged[0].extraction_methods == {"regex", "llm"}


class TestBrandHandleBlocklist:
    """Analytics platform handles must be blocked."""

    def test_favikon_underscore_blocked(self):
        """favikon_ (with trailing underscore) is blocked."""
        assert is_blocked_handle("favikon_") is True

    def test_hypeauditor_blocked(self):
        """hypeauditor is blocked."""
        assert is_blocked_handle("hypeauditor") is True

    def test_influencity_blocked(self):
        """influencity is blocked."""
        assert is_blocked_handle("influencity") is True

    def test_socialbook_blocked(self):
        """socialbook is blocked."""
        assert is_blocked_handle("socialbook") is True

    def test_thesocialcat_blocked(self):
        """thesocialcat is blocked."""
        assert is_blocked_handle("thesocialcat") is True

    def test_filter_blocked_removes_brand_handles(self):
        """filter_blocked() rejects influencers with brand handles."""
        influencers = [
            Influencer(
                name="favikon_",
                handles={Platform.YouTube: "favikon_"},
            ),
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
            ),
        ]
        result = InfluencerMerger.filter_blocked(influencers)
        assert len(result) == 1
        assert result[0].ig_handle == "kayla_itsines"

