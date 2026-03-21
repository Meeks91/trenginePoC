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
        """Build seen_in_categories + most_seen_category from a counts dict."""
        inf.seen_in_categories = [
            CategoryCitation(category=cat, sub=sub, citations=count)
            for (cat, sub), count in sorted(
                cat_sub_counts.items(), key=lambda x: -x[1],
            )
        ]

        cat_totals: dict[str, int] = {}
        for (cat, _sub), count in cat_sub_counts.items():
            cat_totals[cat] = cat_totals.get(cat, 0) + count
        inf.most_seen_category = max(cat_totals, key=lambda k: cat_totals[k])

