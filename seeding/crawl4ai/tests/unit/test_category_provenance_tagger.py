"""
Unit Tests: CategoryProvenanceTagger
========================================
Tests each entry point and the shared _apply_provenance logic.

Covers:
  - tag_from_job: single (category, sub) assignment
  - tag_from_page_map: URL-based provenance via sub_to_category lookup
  - tag_from_name_mention: NameMention-based provenance via sub_to_category lookup
  - _apply_provenance: shared citation builder + most_seen_category derivation
  - Cross-product prevention: multi-config URLs produce only real pairs
"""

from dataclasses import dataclass, field
from typing import Any


from config.schema import CategoryCitation, Influencer, PageResult, Platform
from services.enrichment.CategoryProvenanceTagger import CategoryProvenanceTagger


# Fixtures:

FALLBACK_CATEGORY = "UNKNOWN"
FALLBACK_SUB = "General"

SUB_TO_CATEGORY = {
    "Gym": "FITNESS",
    "Yoga": "FITNESS",
    "Cooking": "FOOD",
    "Science-Based Training": "FITNESS",
}


@dataclass
class _MockTaggedURL:
    """Minimal TaggedURL stand-in for testing."""
    url: str
    source_query: str = ""
    config_keys: set[str] = field(default_factory=set)
    category_keys: set[str] = field(default_factory=set)
    sub_keys: set[str] = field(default_factory=set)


@dataclass
class _MockNameMention:
    """Minimal NameMention stand-in for testing."""
    canonical: str
    variants: list[str] = field(default_factory=list)
    mention_count: int = 1
    was_searched: bool = False
    source_types: list[str] = field(default_factory=list)
    source_urls: set[str] = field(default_factory=set)
    sub_names: list[str] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)


def gen_influencer(
    name: str = "Test Creator",
    source_urls: set[str] | None = None,
) -> Influencer:
    return Influencer(
        name=name,
        handles={Platform.Instagram: name.lower().replace(" ", "")},
        source_urls=source_urls or set(),
    )


def gen_page_map(
    entries: list[tuple[str, _MockTaggedURL]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for url, tagged in entries:
        page = PageResult(
            url=url, query="", raw_markdown="", fit_markdown="",
            raw_token_estimate=0, fit_token_estimate=0, success=True,
        )
        result[url] = (page, tagged)
    return result

# Fixtures


class TestTagFromJob:
    """tag_from_job — assigns single (category, sub) from job config."""

    def test_assigns_single_category(self) -> None:
        inf = gen_influencer()
        CategoryProvenanceTagger.tag_from_job(
            influencers=[inf],
            category_key="FITNESS",
            sub_name="Gym",
        )
        assert inf.most_seen_category == "Gym"
        assert len(inf.seen_in_categories) == 1
        assert inf.seen_in_categories[0].category == "FITNESS"
        assert inf.seen_in_categories[0].sub == "Gym"
        assert inf.seen_in_categories[0].citations == 1

    def test_tags_all_influencers_in_list(self) -> None:
        influencers = [gen_influencer(name=f"Person {i}") for i in range(3)]
        CategoryProvenanceTagger.tag_from_job(
            influencers=influencers,
            category_key="FOOD",
            sub_name="Cooking",
        )
        for inf in influencers:
            assert inf.most_seen_category == "Cooking"
            assert inf.seen_in_categories[0].sub == "Cooking"


class TestTagFromPageMap:
    """tag_from_page_map — trace source_urls to page_map for provenance."""

    def test_single_config_url(self) -> None:
        """URL discovered by one config → one (cat, sub) citation."""
        tagged = _MockTaggedURL(
            url="https://example.com/page1",
            sub_keys={"Gym"},
        )
        page_map = gen_page_map([("https://example.com/page1", tagged)])
        inf = gen_influencer(source_urls={"https://example.com/page1"})

        CategoryProvenanceTagger.tag_from_page_map(
            influencers=[inf],
            page_map=page_map,
            sub_to_category=SUB_TO_CATEGORY,
            fallback_category=FALLBACK_CATEGORY,
            fallback_sub=FALLBACK_SUB,
        )

        assert inf.most_seen_category in {"Gym", "Science-Based Training"}
        assert len(inf.seen_in_categories) == 1
        assert inf.seen_in_categories[0] == CategoryCitation(
            category="FITNESS", sub="Gym", citations=1,
        )

    def test_multi_config_same_category_no_phantom_pairs(self) -> None:
        """URL shared by two configs of the SAME category → two sub citations."""
        tagged = _MockTaggedURL(
            url="https://example.com/page1",
            category_keys={"FITNESS"},
            sub_keys={"Gym", "Science-Based Training"},
        )
        page_map = gen_page_map([("https://example.com/page1", tagged)])
        inf = gen_influencer(source_urls={"https://example.com/page1"})

        CategoryProvenanceTagger.tag_from_page_map(
            influencers=[inf],
            page_map=page_map,
            sub_to_category=SUB_TO_CATEGORY,
            fallback_category=FALLBACK_CATEGORY,
            fallback_sub=FALLBACK_SUB,
        )

        assert inf.most_seen_category in {"Gym", "Science-Based Training"}
        pairs = {(cc.category, cc.sub) for cc in inf.seen_in_categories}
        assert pairs == {("FITNESS", "Gym"), ("FITNESS", "Science-Based Training")}

    def test_multi_config_different_categories_no_phantom_pairs(self) -> None:
        """URL shared by FITNESS/Gym and FOOD/Cooking → only real pairs.

        REGRESSION: old cross-product code would also produce
        (FITNESS, Cooking) and (FOOD, Gym) — phantom pairs.
        """
        tagged = _MockTaggedURL(
            url="https://example.com/page1",
            category_keys={"FITNESS", "FOOD"},
            sub_keys={"Gym", "Cooking"},
        )
        page_map = gen_page_map([("https://example.com/page1", tagged)])
        inf = gen_influencer(source_urls={"https://example.com/page1"})

        CategoryProvenanceTagger.tag_from_page_map(
            influencers=[inf],
            page_map=page_map,
            sub_to_category=SUB_TO_CATEGORY,
            fallback_category=FALLBACK_CATEGORY,
            fallback_sub=FALLBACK_SUB,
        )

        pairs = {(cc.category, cc.sub) for cc in inf.seen_in_categories}
        assert pairs == {("FITNESS", "Gym"), ("FOOD", "Cooking")}
        # Must NOT contain phantom pairs
        assert ("FITNESS", "Cooking") not in pairs
        assert ("FOOD", "Gym") not in pairs

    def test_fallback_when_no_source_urls_match(self) -> None:
        """Influencer source_urls not in page_map → uses fallback."""
        page_map = gen_page_map([])
        inf = gen_influencer(source_urls={"https://unknown.com/page"})

        CategoryProvenanceTagger.tag_from_page_map(
            influencers=[inf],
            page_map=page_map,
            sub_to_category=SUB_TO_CATEGORY,
            fallback_category=FALLBACK_CATEGORY,
            fallback_sub=FALLBACK_SUB,
        )

        assert inf.most_seen_category == FALLBACK_SUB
        assert inf.seen_in_categories[0].sub == FALLBACK_SUB

    def test_multiple_source_urls_accumulate_citations(self) -> None:
        """Influencer with 2 source_urls from same config → citations summed."""
        tagged1 = _MockTaggedURL(url="https://a.com", sub_keys={"Gym"})
        tagged2 = _MockTaggedURL(url="https://b.com", sub_keys={"Gym"})
        page_map = gen_page_map([
            ("https://a.com", tagged1),
            ("https://b.com", tagged2),
        ])
        inf = gen_influencer(source_urls={"https://a.com", "https://b.com"})

        CategoryProvenanceTagger.tag_from_page_map(
            influencers=[inf],
            page_map=page_map,
            sub_to_category=SUB_TO_CATEGORY,
            fallback_category=FALLBACK_CATEGORY,
            fallback_sub=FALLBACK_SUB,
        )

        assert inf.seen_in_categories[0].citations == 2


class TestTagFromNameMention:
    """tag_from_name_mention — derives provenance from NameMention via lookup."""

    def test_single_sub_uses_lookup(self) -> None:
        inf = gen_influencer()
        mention = _MockNameMention(
            canonical="Test",
            sub_names=["Gym"],
            categories=["FITNESS"],
        )

        CategoryProvenanceTagger.tag_from_name_mention(
            inf=inf,
            mention=mention,  # type: ignore[arg-type]
            sub_to_category=SUB_TO_CATEGORY,
        )

        assert inf.most_seen_category == "Gym"
        assert inf.seen_in_categories[0].sub == "Gym"

    def test_multi_sub_different_categories_no_phantom(self) -> None:
        """REGRESSION: multiple subs from different categories must not cross-product."""
        inf = gen_influencer()
        mention = _MockNameMention(
            canonical="Multi Person",
            sub_names=["Gym", "Cooking"],
            categories=["FITNESS", "FOOD"],
        )

        CategoryProvenanceTagger.tag_from_name_mention(
            inf=inf,
            mention=mention,  # type: ignore[arg-type]
            sub_to_category=SUB_TO_CATEGORY,
        )

        pairs = {(cc.category, cc.sub) for cc in inf.seen_in_categories}
        assert pairs == {("FITNESS", "Gym"), ("FOOD", "Cooking")}
        assert ("FITNESS", "Cooking") not in pairs
        assert ("FOOD", "Gym") not in pairs

    def test_fallback_when_no_subs(self) -> None:
        """NameMention with no sub_names → falls back to NAME_RESOLUTION."""
        inf = gen_influencer()
        mention = _MockNameMention(
            canonical="Unknown",
            sub_names=[],
            categories=[],
        )

        CategoryProvenanceTagger.tag_from_name_mention(
            inf=inf,
            mention=mention,  # type: ignore[arg-type]
            sub_to_category=SUB_TO_CATEGORY,
        )

        assert inf.most_seen_category == "Name Resolution"
        assert inf.seen_in_categories[0].sub == "Name Resolution"

    def test_unknown_sub_falls_back_to_name_resolution_category(self) -> None:
        """Sub not in lookup dict → category defaults to NAME_RESOLUTION."""
        inf = gen_influencer()
        mention = _MockNameMention(
            canonical="Niche Person",
            sub_names=["Underwater Basket Weaving"],
            categories=["CRAFTS"],
        )

        CategoryProvenanceTagger.tag_from_name_mention(
            inf=inf,
            mention=mention,  # type: ignore[arg-type]
            sub_to_category=SUB_TO_CATEGORY,
        )

        assert inf.most_seen_category == "Underwater Basket Weaving"
        assert inf.seen_in_categories[0].sub == "Underwater Basket Weaving"


class TestApplyProvenance:
    """_apply_provenance — shared builder for seen_in_categories and most_seen_category."""

    def test_sorts_by_citations_descending(self) -> None:
        inf = gen_influencer()
        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts={
                ("FITNESS", "Gym"): 1,
                ("FOOD", "Cooking"): 5,
                ("FITNESS", "Yoga"): 3,
            },
        )

        assert inf.seen_in_categories[0].citations == 5
        assert inf.seen_in_categories[0].sub == "Cooking"
        assert inf.seen_in_categories[1].citations == 3
        assert inf.seen_in_categories[2].citations == 1

    def test_most_seen_category_derived_from_totals(self) -> None:
        """FITNESS total (1+3=4) vs FOOD total (5) → FOOD wins."""
        inf = gen_influencer()
        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts={
                ("FITNESS", "Gym"): 1,
                ("FITNESS", "Yoga"): 3,
                ("FOOD", "Cooking"): 5,
            },
        )

        assert inf.most_seen_category == "Cooking"

    def test_single_entry(self) -> None:
        inf = gen_influencer()
        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts={("FITNESS", "Gym"): 1},
        )

        assert inf.most_seen_category == "Gym"
        assert len(inf.seen_in_categories) == 1

    def test_most_seen_category_is_sub_not_parent(self) -> None:
        """REGRESSION: most_seen_category must be the sub name, not the parent category."""
        inf = gen_influencer()
        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts={
                ("FITNESS", "Calisthenics"): 3,
                ("FITNESS", "Yoga"): 1,
            },
        )
        assert inf.most_seen_category == "Calisthenics"

    def test_draw_broken_alphabetically(self) -> None:
        """Tied subs are broken alphabetically — deterministic regardless of insertion order."""
        inf = gen_influencer()
        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts={
                ("FITNESS", "Powerlifting"): 1,
                ("FITNESS", "Calisthenics"): 1,
                ("FITNESS", "Yoga"): 1,
            },
        )
        # "Calisthenics" sorts first among the three tied subs
        assert inf.most_seen_category == "Calisthenics"
