"""HandleFromNameService — DDG name-to-handle resolution via NameMentionTracker.

Two resolution paths:
  1. resolve_handles_for_top_mentioned_names()  — post-all-jobs, uses NameMentionTracker to:
                                ① group names by sub-category
                                ② filter ≥ min_mentions (default 2)
                                ③ take top max_per_sub (default 5) per sub
                                ④ DDG-resolve only those names
                                This is the ONLY path for name-only → handle.
  2. resolve_with_recycling() — per-group DDG resolution with known-handle collision recycling.


Supports Instagram, TikTok, YouTube.
Includes exponential backoff for rate limiting.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import deque
    from services.extraction.NameMentionTracker import NameMention, NameMentionTracker

from services.audit.AuditService import AuditLog
from services.search.SearchClient import SearchClient
from config.schema import Influencer, Platform, NameMentionRecord
from services.influencerProvenance.CategoryProvenanceTaggerService import CategoryProvenanceTagger
from services.extraction.NameCleanerService import NameCleanerService
from config import (
    ENRICH_DELAY_SECONDS,
    NAME_RESOLUTION_MIN_MENTIONS, NAME_RESOLUTION_MAX_PER_SUB,
)

logger = logging.getLogger(__name__)


class HandleFromNameService:
    """DDG name → handle resolution, gated by NameMentionTracker.

    resolve_handles_for_top_mentioned_names() → tracker-filtered name resolution (post-all-jobs)
    resolve_with_recycling()                  → per-group resolution with collision recycling
    """

    def __init__(
        self,
        audit: AuditLog,
        *,
        search_client: SearchClient,
        delay_seconds: float = ENRICH_DELAY_SECONDS,
    ):
        self._audit = audit
        self._search_client = search_client
        self._nr_query_template = search_client.nr_query_template()
        self._delay = delay_seconds
        self.retries = 0    # Owned by client; kept for interface compatibility
        self.failures = 0   # Owned by client; kept for interface compatibility

    # API:
    def resolve_handles_for_top_mentioned_names(
        self,
        tracker: NameMentionTracker | None,
        *,
        platform: Platform,
        sub_name: str,
        min_mentions: int = NAME_RESOLUTION_MIN_MENTIONS,
        max_per_group: int = NAME_RESOLUTION_MAX_PER_SUB,
    ) -> tuple[list[Influencer], list[NameMentionRecord]]:
        """Resolve names via DDG using the NameMentionTracker as the gate.

        This is the ONLY path for name-only → handle resolution.

        Steps:
          1. Get top reddit names (grouped by platform, category, sub, region)
          2. Filter by min_mentions threshold
          3. DDG-resolve only those names
          4. Return (resolved_influencers, all_mention_records)

        Args:
            tracker: NameMentionTracker instance (or None if no names tracked).
            platform: Target platform for DDG queries.
            sub_name: Category context for DDG query relevance.
            min_mentions: Minimum cross-page mentions to qualify (default 2).
            max_per_group: Max names resolved per dimension group (default 5).

        Returns:
            Tuple of (resolved_influencers, name_mention_records).
        """
        if tracker is None:
            return [], []

        top_mentions = tracker.top_reddit_names(
            max_per_group=max_per_group, min_mentions=min_mentions,
        )
        names_to_resolve = [m.canonical for m in top_mentions]

        all_mentions = tracker.all_names
        logger.info("\n  --- Name → Handle Resolution ---")
        logger.info(f"  {len(all_mentions)} total name buckets, "
              f"{len(names_to_resolve)} qualify "
              f"(≥{min_mentions} mentions, top {max_per_group}/group, reddit-sourced)")

        # Resolve via DDG
        resolved_map: dict[str, tuple[str, str]] = {}
        resolved_influencers: list[Influencer] = []

        if names_to_resolve:
            from services.extraction.NameResolver import resolve_names_via_ddg
            name_handles = resolve_names_via_ddg(
                sorted(names_to_resolve), self._audit,
                search_client=self._search_client,
                query_template=self._nr_query_template,
                category=sub_name or "Influencer",
                platform=platform,
            )
            tracker.mark_searched(set(names_to_resolve))
            mention_by_name = {m.canonical: m for m in top_mentions}

            for h in name_handles:
                resolve_key = h.name or h.handle
                resolved_map[resolve_key] = (h.handle, h.platform)
                try:
                    plat = Platform(h.platform)
                    handles: dict[Platform, str] = {plat: h.handle}
                except ValueError:
                    handles = {}
                mention = mention_by_name.get(resolve_key)
                resolved_influencers.append(Influencer(
                    name=NameCleanerService.clean_name(h.name) or "",
                    handles=handles,
                    source_urls=set(mention.source_urls) if mention else set(),
                    extraction_methods={"name_resolution"},
                ))

        # Build NameMentionRecord list for output
        records: list[NameMentionRecord] = []
        for m in tracker.all_names:
            resolved = resolved_map.get(m.canonical)
            handle = resolved[0] if resolved else ""
            plat_str = resolved[1] if resolved else ""
            records.append(NameMentionRecord(
                canonical=m.canonical,
                variants=m.variants,
                mention_count=m.mention_count,
                source_types=m.source_types,
                source_urls=sorted(m.source_urls),
                was_searched=m.was_searched,
                resolved_handle=handle,
                resolved_platform=plat_str,
            ))

        logger.info(f"  Resolved: {len(resolved_map)}/{len(names_to_resolve)} names → handles")
        return resolved_influencers, records

    def resolve_with_recycling(
        self,
        group_queues: dict[tuple[str, str, str, str], "deque[NameMention]"],
        known_handles: set[str],
        platform: Platform,
        sub_name: str,
        max_slots_per_group: int,
        sub_to_category: dict[str, str],
    ) -> tuple[list[Influencer], list[NameMentionRecord]]:
        """Per-group DDG resolution with known-handle collision recycling.

        For each group, pops candidates from the queue and DDG-resolves
        them. If the resolved handle is already in known_handles, the
        slot is recycled (next candidate from same group is tried).

        Args:
            group_queues: Per-group deques of candidates (from tracker).
            known_handles: Lowercase handles already found this run.
            platform: Target platform for DDG queries.
            sub_name: Category context for DDG query relevance.
            max_slots_per_group: Max new handles per group.

        Returns:
            Tuple of (resolved_influencers, name_mention_records).
        """
        from services.extraction.NameResolver import resolve_names_via_ddg

        all_resolved: list[Influencer] = []
        all_records: list[NameMentionRecord] = []
        total_collisions = 0
        total_new = 0

        logger.info("\n  --- Slot Recycling Name Resolution ---")
        logger.info(f"  {len(group_queues)} groups, "
              f"max {max_slots_per_group} slots/group, "
              f"{len(known_handles)} known handles")

        for group_key, queue in group_queues.items():
            slots_filled = 0
            group_collisions = 0

            while slots_filled < max_slots_per_group and queue:
                candidate = queue.popleft()
                name = candidate.canonical

                # Resolve single name via search client
                name_handles = resolve_names_via_ddg(
                    [name], self._audit,
                    search_client=self._search_client,
                    query_template=self._nr_query_template,
                    category=sub_name or "Influencer",
                    platform=platform,
                )

                if not name_handles:
                    all_records.append(self._mention_to_record(
                        candidate, searched=True,
                    ))
                    slots_filled += 1
                    continue

                handle_obj = name_handles[0]
                handle_lower = handle_obj.handle.lower()

                if handle_lower in known_handles:
                    logger.info(
                        "Slot recycled: %s → @%s (already known)",
                        name, handle_obj.handle,
                    )
                    all_records.append(self._mention_to_record(
                        candidate, searched=True,
                        handle=handle_obj.handle,
                        platform_str=handle_obj.platform,
                    ))
                    group_collisions += 1
                    total_collisions += 1
                    continue

                # New handle — create Influencer and consume slot
                try:
                    plat = Platform(handle_obj.platform)
                    handles: dict[Platform, str] = {plat: handle_obj.handle}
                except ValueError:
                    handles = {}

                inf = Influencer(
                    name=NameCleanerService.clean_name(handle_obj.name or name) or "",
                    handles=handles,
                    source_urls=set(candidate.source_urls),
                    extraction_methods={"name_resolution"},
                )
                CategoryProvenanceTagger.tag_from_name_mention(
                    inf=inf,
                    mention=candidate,
                    sub_to_category=sub_to_category,
                )
                all_resolved.append(inf)
                known_handles.add(handle_lower)
                total_new += 1

                all_records.append(self._mention_to_record(
                    candidate, searched=True,
                    handle=handle_obj.handle,
                    platform_str=handle_obj.platform,
                ))
                slots_filled += 1

            if slots_filled == 0 and group_collisions > 0:
                logger.error(
                    "Group %s: all %d candidates resolved to already-known "
                    "handles. No new influencers discovered.",
                    group_key, group_collisions,
                )

        logger.info(f"  Recycling complete: {total_new} new handles, "
              f"{total_collisions} collisions recycled")
        return all_resolved, all_records

    # ── Internal ───────────────────────────────────────────────────────

    @staticmethod
    def _mention_to_record(
        mention: "NameMention",
        searched: bool,
        handle: str = "",
        platform_str: str = "",
    ) -> NameMentionRecord:
        """Convert a NameMention to a NameMentionRecord for output."""
        return NameMentionRecord(
            canonical=mention.canonical,
            variants=mention.variants,
            mention_count=mention.mention_count,
            source_types=mention.source_types,
            source_urls=sorted(mention.source_urls),
            was_searched=searched,
            resolved_handle=handle,
            resolved_platform=platform_str,
        )

