"""
CategoryProvenanceTagger — Stamps category provenance onto Influencer objects.

Stateless utility. Called by pipeline orchestrators that hold the context
(page_map, job config, or NameMention) linking each influencer to the
search config that discovered them.

Three entry points, one shared internal:
  tag_from_page_map   — phase pipeline: source_urls → page_map → TaggedURL
  tag_from_job        — per-job pipeline: single (category, sub) from job
  tag_from_name_mention — name resolution: inherit from NameMention tracker
  _apply_provenance   — shared: build seen_in_categories + most_seen_category
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from config.schema import CategoryCitation, Influencer

if TYPE_CHECKING:
    from config.schema import PageResult
    from phase_pipeline import TaggedURL
    from services.extraction.NameMentionTracker import NameMention


class CategoryProvenanceTagger:
    """Stamps category provenance onto Influencer objects.

    Stateless utility. Called by pipeline orchestrators that have
    the context (page_map, job, or NameMention) to determine
    which config discovered each influencer.
    """

    # API:

    @staticmethod
    def tag_from_page_map(
        influencers: list[Influencer],
        page_map: dict[str, tuple[PageResult, TaggedURL]],
        sub_to_category: dict[str, str],
        fallback_category: str,
        fallback_sub: str,
    ) -> None:
        """Phase pipeline: trace source_urls → page_map → TaggedURL → provenance.

        Each influencer's source_urls are looked up in page_map to find which
        TaggedURL (and therefore which search configs) discovered that page.
        Uses sub_to_category to derive the parent category from each sub,
        avoiding cross-product of independent sets.
        """
        for inf in influencers:
            cat_sub_counts: dict[tuple[str, str], int] = {}

            for url in inf.source_urls:
                if url in page_map:
                    _page, tagged_url = page_map[url]
                    for sub in tagged_url.sub_keys:
                        cat = sub_to_category.get(sub, fallback_category)
                        key = (cat, sub)
                        cat_sub_counts[key] = cat_sub_counts.get(key, 0) + 1

            if not cat_sub_counts:
                cat_sub_counts[(fallback_category, fallback_sub)] = 1

            CategoryProvenanceTagger.apply_provenance(
                inf=inf,
                cat_sub_counts=cat_sub_counts,
            )

    @staticmethod
    def tag_from_job(
        influencers: list[Influencer],
        category_key: str,
        sub_name: str,
    ) -> None:
        """Per-job pipeline: assign single (category, sub) from the job config."""
        for inf in influencers:
            CategoryProvenanceTagger.apply_provenance(
                inf=inf,
                cat_sub_counts={(category_key, sub_name): 1},
            )

    @staticmethod
    def tag_from_name_mention(
        inf: Influencer,
        mention: NameMention,
        sub_to_category: dict[str, str],
    ) -> None:
        """Name resolution: inherit categories/subs from NameMention tracker data.

        Uses sub_to_category to derive parent category from each sub_name,
        avoiding cross-product of independent lists.
        """
        cat_sub_counts: dict[tuple[str, str], int] = {}

        for sub in mention.sub_names:
            cat = sub_to_category.get(sub, "NAME_RESOLUTION")
            key = (cat, sub)
            cat_sub_counts[key] = cat_sub_counts.get(key, 0) + 1

        if not cat_sub_counts:
            cat_sub_counts[("NAME_RESOLUTION", "Name Resolution")] = 1

        CategoryProvenanceTagger.apply_provenance(
            inf=inf,
            cat_sub_counts=cat_sub_counts,
        )

    @staticmethod
    def apply_provenance(
        inf: Influencer,
        cat_sub_counts: dict[tuple[str, str], int],
    ) -> None:
        """Build seen_in_categories + most_seen_category from a counts dict.

        Parent subs (where category.lower() == sub.lower(), e.g. BEAUTY/'Beauty')
        are excluded from the most_seen_category winner pool when specific subs
        also exist. This promotes diversity — creators fall into specific subs
        instead of the catch-all parent. The parent sub still appears in
        seen_in_categories for full audit transparency.
        """
        inf.seen_in_categories = [
            CategoryCitation(category=cat, sub=sub, citations=count)
            for (cat, sub), count in sorted(
                cat_sub_counts.items(), key=lambda x: -x[1],
            )
        ]

        sub_totals: dict[str, int] = {}
        for (_cat, sub), count in cat_sub_counts.items():
            sub_totals[sub] = sub_totals.get(sub, 0) + count

        parent_sub_names = {
            sub
            for (cat, sub) in cat_sub_counts
            if cat.lower() == sub.lower()
        }
        specific_sub_totals = {
            sub: count
            for sub, count in sub_totals.items()
            if sub not in parent_sub_names
        }
        candidate_totals = specific_sub_totals if specific_sub_totals else sub_totals

        max_count = max(candidate_totals.values())
        leading_subs = [sub for sub, count in candidate_totals.items() if count == max_count]
        if len(leading_subs) == 1:
            inf.most_seen_category = leading_subs[0]
        else:
            inf.most_seen_category = min(leading_subs)

