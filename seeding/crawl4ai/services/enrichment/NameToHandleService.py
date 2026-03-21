"""NameToHandleService — THE single service for name → handle DDG resolution.

Two modes:
  1. resolve_cross_account_handles()       — per-job cross-platform enrichment only.
                                Name-only influencers are NOT DDG'd here.
  2. resolve_handles_for_top_mentioned_names()  — post-all-jobs, uses NameMentionTracker to:
                                ① group names by sub-category
                                ② filter ≥ min_mentions (default 2)
                                ③ take top max_per_sub (default 5) per sub
                                ④ DDG-resolve only those names
                                This is the ONLY path for name-only → handle.

Supports Instagram, TikTok, YouTube.
Includes exponential backoff for rate limiting.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import deque
    from services.extraction.NameMentionTracker import NameMention, NameMentionTracker

from services.audit.AuditService import AuditLog
from services.search.SearchClient import SearchClient

logger = logging.getLogger(__name__)
from config.schema import Influencer, Platform, NameMentionRecord
from services.enrichment.CategoryProvenanceTagger import CategoryProvenanceTagger
from services.extraction.NameCleaner import NameCleaner
from config import (
    ENRICH_DELAY_SECONDS,
    NAME_RESOLUTION_MIN_MENTIONS, NAME_RESOLUTION_MAX_PER_SUB,
    CROSS_PLATFORM_MAX_LOOKUPS,
)
from services.enrichment.patterns import (
    extract_handle_from_url,
    extract_handle_from_text,
    PLATFORM_DOMAINS,
)




class NameToHandleService:
    """Single service for all name → handle DDG resolution.

    resolve_cross_account_handles()      → cross-platform enrichment (per-job)
    resolve_handles_for_top_mentioned_names() → tracker-filtered name resolution (post-all-jobs)
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

    # ── Internal helpers (static, pure — independently testable) ──

    @staticmethod
    def _needs_resolution(inf: Influencer, platform: Platform) -> bool:
        """Determine if an influencer needs handle resolution.

        Returns True when:
          - No handles at all
          - Doesn't have a handle for the target platform
        """
        if not inf.handles:
            return True
        return platform not in inf.handles

    # ── Mode 1: Per-Job Cross-Platform Enrichment ──

    def resolve_cross_account_handles(
        self,
        influencers: list[Influencer],
        platform: Platform,
        skip_cross_platform: bool = False,
        max_lookups: int = CROSS_PLATFORM_MAX_LOOKUPS,
        min_sources: int = 2,
    ) -> list[Influencer]:
        """Cross-platform enrichment ONLY. Name-only influencers are NOT DDG'd.

        Cross-platform handles are PRESERVED as separate entries. If targeting
        Instagram and we find a TikTok handle, the TikTok entry stays and a new
        Instagram entry is added (if DDG finds one).

        Name-only influencers (no handles at all) are SKIPPED here — they go
        through resolve_handles_for_top_mentioned_names() after all jobs complete.

        Rate limit budget is managed internally:
          1. Only entries cited on ≥ ``min_sources`` pages qualify
          2. Sorted by frequency (most-cited first)
          3. Capped at ``max_lookups`` DDG queries per call

        Since each call = 1 job = 1 subCat × 1 region, total DDG budget
        across a full run = numSubCats × max_lookups × numRegions.

        Args:
            skip_cross_platform: If True, skip all DDG lookups entirely.
            max_lookups: Maximum DDG queries per call (default 5).
            min_sources: Minimum source_urls count to qualify (default 2).

        Returns:
            The enriched list (same list, possibly with new entries appended).
        """
        logger.info(f"\n  --- Resolve Handles ({platform.value}) ---")
        if skip_cross_platform:
            logger.info("  Cross-platform lookup: SKIPPED (--no-cross-platform-lookup)")
            return influencers

        # Only enrich cross-platform: has handle on another platform, needs target
        candidates = [
            inf for inf in influencers
            if inf.handles  # MUST have at least one handle
            and self._needs_resolution(inf, platform)
        ]

        # Filter by minimum source frequency
        qualified = [
            inf for inf in candidates
            if len(inf.source_urls) >= min_sources
        ]
        below_threshold = len(candidates) - len(qualified)

        # Sort by frequency (most-cited first) and cap
        qualified.sort(key=lambda inf: len(inf.source_urls), reverse=True)
        to_resolve = qualified[:max_lookups]
        _capped = len(qualified) - len(to_resolve)

        name_only_count = sum(1 for inf in influencers if not inf.handles)
        logger.info(f"  {len(candidates)} need cross-platform, "
              f"{below_threshold} below min sources ({min_sources}), "
              f"{len(to_resolve)} queued (top {max_lookups} by frequency), "
              f"{name_only_count} name-only deferred to tracker")

        new_entries = self._ddg_lookup_batch(to_resolve, platform)
        influencers.extend(new_entries)

        return influencers

    def _ddg_lookup_batch(
        self,
        entries: list[Influencer],
        platform: Platform,
    ) -> list[Influencer]:
        """DDG-search each entry for a target-platform handle.

        Returns new Influencer entries (one per successful lookup) with
        only the target-platform handle. Does NOT modify the input entries.
        """
        domain = PLATFORM_DOMAINS.get(platform)
        if not entries or not domain:
            if not domain and entries:
                logger.warning(f"Unknown platform '{platform.value}' — skipping handle backfill")
            return []

        new_entries: list[Influencer] = []
        for inf in entries:
            handle = self._search_handle(inf.name, platform, domain)
            if handle:
                existing_summary = ", ".join(
                    f"{p.value}: {h}" for p, h in inf.handles.items()
                )
                new_entries.append(Influencer(
                    name=inf.name,
                    handles={platform: handle.lstrip("@")},
                ))
                self._audit.log_handle_found(inf.name, handle)
                logger.info(f"    {inf.name} -> {handle} (kept {existing_summary})")
            time.sleep(self._delay)

        logger.info(f"\n  Filled {len(new_entries)}/{len(entries)} cross-platform handles")
        return new_entries

    # ── Mode 2: Post-All-Jobs Tracker-Filtered Resolution ──

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
                    name=NameCleaner.clean_name(h.name) or "",
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
                    name=NameCleaner.clean_name(handle_obj.name or name) or "",
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

    # ── Internal Search ──

    def _search_handle(self, name: str, platform: Platform, domain: str) -> str | None:
        """Search for an influencer's handle via the injected search client."""
        query = f'"{name}" {domain}'
        results = self._search_client.search_text(query, max_results=2)
        for r in results:
            handle = extract_handle_from_url(r.get("href", ""), platform.value)
            if handle:
                return handle
            text = r.get("title", "") + " " + r.get("body", "")
            handle = extract_handle_from_text(text)
            if handle:
                return handle
        return None
