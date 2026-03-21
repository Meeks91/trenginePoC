"""
Tests for Influencer citation enrichment
==========================================

TDD tests for:
  - Influencer.citation_count property
  - Influencer.extraction_methods field
  - SubResult.to_dict() enriched serialization
  - RegionResult.to_dict() source_extraction_methods map
  - HandleExtractionService extraction method tagging
  - InfluencerMerger extraction_methods union during merge
"""

import pytest

from config.schema import Influencer, Platform, SubResult, SourceResult, RegionResult, CategoryCitation


# ══════════════════════════════════════════════════════════════════════
# __post_init__ Name Cleaning
# ══════════════════════════════════════════════════════════════════════

class TestInfluencerPostInitCleaning:
    """Influencer.__post_init__ must call NameCleaner.clean_name() on construction."""

    def test_markdown_bold_stripped(self):
        inf = Influencer(name="**Massy Arias**", handles={Platform.Instagram: "massy.arias"})
        assert inf.name == "Massy Arias"

    def test_markdown_link_stripped(self):
        inf = Influencer(name="[ Massy Arias ](https://example.com)", handles={Platform.Instagram: "massy.arias"})
        assert "[" not in inf.name
        assert "(" not in inf.name

    def test_numbered_prefix_stripped(self):
        inf = Influencer(name="6. Massy Arias", handles={Platform.Instagram: "massy.arias"})
        assert inf.name == "Massy Arias"

    def test_clean_name_passes_through(self):
        inf = Influencer(name="Jeff Nippard", handles={Platform.YouTube: "jeffnippard"})
        assert inf.name == "Jeff Nippard"

    def test_blocklist_name_blanked(self):
        """Blocklist names are blanked by clean_name → empty string."""
        inf = Influencer(name="Weight Loss", handles={Platform.Instagram: "test"})
        assert inf.name == ""

    def test_bare_handle_name_blanked(self):
        """Handle-as-name is blanked by clean_name → empty string."""
        inf = Influencer(name="kayla_itsines", handles={Platform.Instagram: "kayla_itsines"})
        assert inf.name == ""


# ══════════════════════════════════════════════════════════════════════
# Model Tests
# ══════════════════════════════════════════════════════════════════════

class TestInfluencerCitationCount:
    """Influencer.citation_count should equal len(source_urls)."""

    def test_citation_count_equals_source_url_count(self):
        inf = Influencer(
            name="Kayla Itsines",
            handles={Platform.Instagram: "kayla_itsines"},
            source_urls={"https://a.com", "https://b.com", "https://c.com"},
        )
        assert inf.citation_count == 3

    def test_citation_count_zero_when_no_sources(self):
        inf = Influencer(name="", handles={})
        assert inf.citation_count == 0

    def test_citation_count_one_source(self):
        inf = Influencer(
            name="",
            source_urls={"https://only.com"},
        )
        assert inf.citation_count == 1


class TestInfluencerExtractionMethods:
    """Influencer should carry a set of extraction methods."""

    def test_extraction_methods_field_exists(self):
        inf = Influencer(name="Test")
        assert hasattr(inf, "extraction_methods")
        assert isinstance(inf.extraction_methods, set)

    def test_extraction_methods_default_empty(self):
        inf = Influencer(name="Test")
        assert inf.extraction_methods == set()

    def test_extraction_methods_accepts_values(self):
        inf = Influencer(
            name="Test",
            extraction_methods={"regex", "llm"},
        )
        assert inf.extraction_methods == {"regex", "llm"}


# ══════════════════════════════════════════════════════════════════════
# Serialization Tests
# ══════════════════════════════════════════════════════════════════════

class TestSubResultEnrichedSerialization:
    """SubResult.to_dict() must include all enriched influencer fields."""

    @pytest.fixture
    def enriched_sub_result(self):
        """SubResult with a fully-populated Influencer."""
        inf = Influencer(
            name="Jeff Nippard",
            handles={Platform.YouTube: "jeffnippard"},
            most_seen_category="FITNESS",
            seen_in_categories=[
                CategoryCitation(category="FITNESS", sub="Bodybuilding", citations=1),
            ],
            source_urls={"https://a.com", "https://b.com"},
            extraction_methods={"regex", "llm"},
        )
        source = SourceResult(
            url="https://a.com",
            query="test query",
            md="pages/test.md",
            influencers=[inf],
        )
        return SubResult(
            is_top_level=True,
            sources=[source],
            all_influencers=[inf],
        )

    def test_all_influencers_includes_citation_count(self, enriched_sub_result):
        data = enriched_sub_result.to_dict()
        inf_dict = data["all_influencers"][0]
        assert "citation_count" in inf_dict
        assert inf_dict["citation_count"] == 2

    def test_all_influencers_includes_source_urls(self, enriched_sub_result):
        data = enriched_sub_result.to_dict()
        inf_dict = data["all_influencers"][0]
        assert "source_urls" in inf_dict
        assert set(inf_dict["source_urls"]) == {"https://a.com", "https://b.com"}

    def test_all_influencers_includes_extraction_methods(self, enriched_sub_result):
        data = enriched_sub_result.to_dict()
        inf_dict = data["all_influencers"][0]
        assert "extraction_methods" in inf_dict
        # Must be sorted for deterministic JSON
        assert inf_dict["extraction_methods"] == ["llm", "regex"]

    def test_all_influencers_includes_category_provenance(self, enriched_sub_result):
        data = enriched_sub_result.to_dict()
        inf_dict = data["all_influencers"][0]
        assert "most_seen_category" in inf_dict
        assert inf_dict["most_seen_category"] == "FITNESS"
        assert "seen_in_categories" in inf_dict
        assert len(inf_dict["seen_in_categories"]) == 1

    def test_source_influencers_also_enriched(self, enriched_sub_result):
        """Influencers under sources[] must also carry enriched fields."""
        data = enriched_sub_result.to_dict()
        source_inf = data["sources"][0]["influencers"][0]
        assert "citation_count" in source_inf
        assert "extraction_methods" in source_inf


class TestRegionResultExtractionMethodMap:
    """RegionResult.to_dict() must include top-level source_extraction_methods."""

    def test_region_result_includes_source_extraction_methods(self):
        inf = Influencer(
            name="Test",
            handles={Platform.Instagram: "test"},
            source_urls={"https://a.com"},
            extraction_methods={"regex"},
        )
        sub = SubResult(
            is_top_level=True,
            sources=[],
            all_influencers=[inf],
        )
        region = RegionResult(
            region="US",
            platforms={"Instagram": {"FITNESS": {"Fitness": sub}}},
        )
        data = region.to_dict()
        assert "source_extraction_methods" in data
        assert "https://a.com" in data["source_extraction_methods"]
        assert "regex" in data["source_extraction_methods"]["https://a.com"]


# ══════════════════════════════════════════════════════════════════════
# Extraction Tagging Tests
# ══════════════════════════════════════════════════════════════════════

class TestExtractionMethodTagging:
    """HandleExtractionService must tag influencers with their extraction method."""

    def test_regex_extraction_tags_with_regex(self):
        """Influencers from _regex_extract() must have 'regex' in extraction_methods."""
        from services.extraction.HandleExtractionService import HandleExtractionService
        from config.schema import PageResult

        page = PageResult(
            url="https://example.com",
            query="test",
            raw_markdown="Follow @kayla_itsines on Instagram https://instagram.com/kayla_itsines",
            fit_markdown="Follow @kayla_itsines on Instagram",
            raw_token_estimate=100,
            fit_token_estimate=50,
            success=True,
        )
        rx = HandleExtractionService._regex_extract([page])
        # At least one influencer should be found
        assert len(rx.regex_handles) > 0
        for inf in rx.regex_handles:
            assert "regex" in inf.extraction_methods, (
                f"Influencer '{inf.name}' from regex extraction "
                f"missing 'regex' in extraction_methods: {inf.extraction_methods}"
            )

    def test_ddg_direct_tags_with_ddg_direct(self):
        """DDG direct handles in _merge_handles() must carry 'ddg_direct'."""
        from services.extraction.HandleExtractionService import HandleExtractionService
        from services.extraction.RegexHandleExtractor import ExtractedHandle

        ddg_handles = [
            ExtractedHandle(handle="kayla_itsines", platform="Instagram", name="Kayla Itsines"),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=ddg_handles,
            regex_handles=[],
            llm_handles={},
        )
        kayla = next(i for i in merged if "kayla" in (i.name.lower() or "") or "kayla_itsines" in i.handles.get(Platform.Instagram, ""))
        assert "ddg_direct" in kayla.extraction_methods

    def test_merge_handles_unions_extraction_methods_on_dedup(self):
        """When two entries dedup, their extraction_methods must union."""
        from services.extraction.HandleExtractionService import HandleExtractionService
        from services.extraction.RegexHandleExtractor import ExtractedHandle

        # Same handle from DDG and regex
        ddg_handles = [
            ExtractedHandle(handle="kayla_itsines", platform="Instagram", name="Kayla Itsines"),
        ]
        regex_handles = [
            Influencer(
                name="Kayla Itsines",
                handles={Platform.Instagram: "kayla_itsines"},
                source_urls={"https://a.com"},
                extraction_methods={"regex"},
            ),
        ]
        merged = HandleExtractionService._merge_handles(
            direct_handles=ddg_handles,
            regex_handles=regex_handles,
            llm_handles={},
        )
        # Should be deduped to one entry with both methods
        kayla = next(i for i in merged if "kayla" in i.name.lower() or "kayla_itsines" in i.handles.get(Platform.Instagram, ""))
        assert "ddg_direct" in kayla.extraction_methods
        assert "regex" in kayla.extraction_methods


# ══════════════════════════════════════════════════════════════════════
# Merger Tests
# ══════════════════════════════════════════════════════════════════════

class TestInfluencerMergerExtractionMethods:
    """InfluencerMerger.merge() must union extraction_methods."""

    def test_identity_merge_unions_extraction_methods(self):
        """Two entries for same person with different methods → union."""
        from services.enrichment.InfluencerMerger import InfluencerMerger

        entries = [
            Influencer(
                name="Jeff Nippard",
                handles={Platform.YouTube: "jeffnippard"},
                source_urls={"https://a.com"},
                extraction_methods={"regex"},
            ),
            Influencer(
                name="Jeff Nippard",
                handles={Platform.YouTube: "jeffnippard"},
                source_urls={"https://b.com"},
                extraction_methods={"llm"},
            ),
        ]
        merged = InfluencerMerger.merge(entries)
        assert len(merged) == 1
        assert merged[0].extraction_methods == {"regex", "llm"}

    def test_merge_preserves_single_extraction_method(self):
        """Single entry preserves its extraction method through merge."""
        from services.enrichment.InfluencerMerger import InfluencerMerger

        entries = [
            Influencer(
                name="Sarah Collins",
                handles={Platform.Instagram: "solocreator"},
                extraction_methods={"ddg_direct"},
            ),
        ]
        merged = InfluencerMerger.merge(entries)
        assert len(merged) == 1
        assert merged[0].extraction_methods == {"ddg_direct"}
