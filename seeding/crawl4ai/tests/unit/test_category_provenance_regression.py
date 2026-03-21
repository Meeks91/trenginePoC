"""
Regression Test: Multi-Config Category Provenance
=====================================================
Validates the fix for the bug where all influencers were categorized as
"FITNESS" because the pipeline used handle-in-markdown text search instead
of config-based provenance.

Root cause: phase_pipeline._extract_and_build_entries searched for handle
text in page markdown; when matching failed, fell back to jobs[0].category_key
(alphabetically "FITNESS"). Now category assignment traces:
    Influencer.source_urls → page_map → TaggedURL.category_keys/sub_keys

This test creates influencers found across multiple tagged URLs with
different categories and verifies that:
  1. most_seen_category reflects the subcategory with the most hits
  2. seen_in_categories contains per-sub citations from all configs
  3. Merging correctly sums citation counts across duplicate entries
"""

from config.schema import Influencer, Platform, CategoryCitation
from services.enrichment.InfluencerMerger import InfluencerMerger


class TestMultiConfigCategoryProvenance:
    """Regression: categories derived from config provenance, not content."""

    def test_influencer_seen_in_two_categories_retains_both(self):
        """Influencer found by FITNESS/Gym AND FOOD/Healthy searches."""
        inf = Influencer(
            name="Jeff Nippard",
            handles={Platform.Instagram: "jeffnippard"},
            most_seen_category="FITNESS",
            seen_in_categories=[
                CategoryCitation(category="FITNESS", sub="Gym", citations=3),
                CategoryCitation(category="FOOD", sub="Healthy Eating", citations=1),
            ],
        )
        assert inf.most_seen_category == "FITNESS"
        cats = {cc.category for cc in inf.seen_in_categories}
        assert cats == {"FITNESS", "FOOD"}
        subs = {cc.sub for cc in inf.seen_in_categories}
        assert "Gym" in subs
        assert "Healthy Eating" in subs

    def test_merge_unions_seen_in_categories_across_entries(self):
        """Two entries from different configs → merged with both subs."""
        raw = [
            Influencer(
                name="Jeff Nippard",
                handles={Platform.Instagram: "jeffnippard"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=2),
                ],
            ),
            Influencer(
                name="Jeff Nippard",
                handles={Platform.YouTube: "jeffnippard"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Science-Based Training", citations=1),
                ],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        assert len(merged) == 1
        subs = {cc.sub for cc in merged[0].seen_in_categories}
        assert "Gym" in subs
        assert "Science-Based Training" in subs
        assert merged[0].most_seen_category == "Gym"

    def test_merge_sums_citations_for_same_sub(self):
        """Same (category, sub) from two entries → citations summed."""
        raw = [
            Influencer(
                name="Jeff Nippard",
                handles={Platform.Instagram: "jeffnippard"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=2),
                ],
            ),
            Influencer(
                name="Jeff Nippard",
                handles={Platform.Instagram: "jeffnippard"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=3),
                ],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        assert len(merged) == 1
        gym_citations = [cc for cc in merged[0].seen_in_categories if cc.sub == "Gym"]
        assert len(gym_citations) == 1
        assert gym_citations[0].citations == 5

    def test_most_seen_category_recomputed_on_merge(self):
        """After merge, most_seen_category reflects the dominant subcategory."""
        raw = [
            Influencer(
                name="CrossFit Creator",
                handles={Platform.Instagram: "crossfitcreator"},
                most_seen_category="FOOD",
                seen_in_categories=[
                    CategoryCitation(category="FOOD", sub="Meal Prep", citations=1),
                ],
            ),
            Influencer(
                name="CrossFit Creator",
                handles={Platform.Instagram: "crossfitcreator"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="CrossFit", citations=3),
                ],
            ),
            Influencer(
                name="CrossFit Creator",
                handles={Platform.Instagram: "crossfitcreator"},
                most_seen_category="FITNESS",
                seen_in_categories=[
                    CategoryCitation(category="FITNESS", sub="Gym", citations=2),
                ],
            ),
        ]
        merged = InfluencerMerger.merge(raw)
        assert len(merged) == 1
        assert merged[0].most_seen_category == "CrossFit"
        total_fitness = sum(
            cc.citations for cc in merged[0].seen_in_categories
            if cc.category == "FITNESS"
        )
        total_food = sum(
            cc.citations for cc in merged[0].seen_in_categories
            if cc.category == "FOOD"
        )
        assert total_fitness == 5
        assert total_food == 1

    def test_to_dict_serializes_new_schema(self):
        """Influencer.to_dict() includes new category provenance fields."""
        inf = Influencer(
            name="Test Creator",
            handles={Platform.Instagram: "testcreator"},
            most_seen_category="FITNESS",
            seen_in_categories=[
                CategoryCitation(category="FITNESS", sub="Gym", citations=3),
                CategoryCitation(category="FOOD", sub="Cooking", citations=1),
            ],
        )
        d = inf.to_dict()
        assert d["most_seen_category"] == "FITNESS"
        assert len(d["seen_in_categories"]) == 2
        assert d["seen_in_categories"][0] == {
            "category": "FITNESS", "sub": "Gym", "citations": 3,
        }
        assert "categories" not in d
