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
import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.extraction.NameMentionTracker import NameMentionTracker

from ddgs import DDGS

from services.audit.AuditService import AuditLog

logger = logging.getLogger(__name__)
from config.schema import Influencer, Platform, NameMentionRecord
from config import (
    ENRICH_DELAY_SECONDS,
    SEARCH_BACKEND, SEARCH_REGION,
    MAX_RETRIES, BACKOFF_BASE_SECONDS, BACKOFF_MAX_SECONDS,
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
        ddgs: DDGS | None = None,
        delay_seconds: float = ENRICH_DELAY_SECONDS,
    ):
        self._audit = audit
        self._ddgs = ddgs or DDGS()
        self._delay = delay_seconds
        self.retries = 0    # Total retry attempts this run
        self.failures = 0   # Handle lookups that failed after all retries

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
        print(f"\n  --- Resolve Handles ({platform.value}) ---")
        if skip_cross_platform:
            print("  Cross-platform lookup: SKIPPED (--no-cross-platform-lookup)")
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
        capped = len(qualified) - len(to_resolve)

        name_only_count = sum(1 for inf in influencers if not inf.handles)
        print(f"  {len(candidates)} need cross-platform, "
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
                print(f"  WARN: Unknown platform '{platform.value}' — skipping handle backfill")
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
                print(f"    {inf.name} -> {handle} (kept {existing_summary})")
            time.sleep(self._delay)

        print(f"\n  Filled {len(new_entries)}/{len(entries)} cross-platform handles")
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
        print(f"\n  --- Name → Handle Resolution ---")
        print(f"  {len(all_mentions)} total name buckets, "
              f"{len(names_to_resolve)} qualify "
              f"(≥{min_mentions} mentions, top {max_per_group}/group, reddit-sourced)")

        # Resolve via DDG
        resolved_map: dict[str, tuple[str, str]] = {}
        resolved_influencers: list[Influencer] = []

        if names_to_resolve:
            from services.extraction.NameResolver import resolve_names_via_ddg
            name_handles = resolve_names_via_ddg(
                sorted(names_to_resolve), self._audit,
                category=sub_name or "Influencer",
                platform=platform,
            )
            tracker.mark_searched(set(names_to_resolve))

            for h in name_handles:
                resolved_map[h.name or h.handle] = (h.handle, h.platform)
                try:
                    plat = Platform(h.platform)
                    handles: dict[Platform, str] = {plat: h.handle}
                except ValueError:
                    handles = {}
                resolved_influencers.append(Influencer(
                    name=h.name or h.handle,
                    handles=handles,
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

        print(f"  Resolved: {len(resolved_map)}/{len(names_to_resolve)} names → handles")
        return resolved_influencers, records

    # ── Internal DDG Search ──

    def _search_handle(self, name: str, platform: Platform, domain: str) -> str | None:
        """Search DuckDuckGo for an influencer's handle with exponential backoff."""
        query = f'"{name}" {domain}'

        for attempt in range(MAX_RETRIES + 1):
            try:
                results = self._ddgs.text(
                    query, max_results=2,
                    backend=SEARCH_BACKEND, region=SEARCH_REGION,
                )
                for r in results:
                    handle = extract_handle_from_url(r.get("href", ""), platform.value)
                    if handle:
                        return handle

                    text = r.get("title", "") + " " + r.get("body", "")
                    handle = extract_handle_from_text(text)
                    if handle:
                        return handle
                return None  # DDG responded but no handle found — not a failure
            except Exception as e:
                if attempt < MAX_RETRIES:
                    delay = min(
                        BACKOFF_BASE_SECONDS * (2 ** attempt) + random.uniform(0, 1),
                        BACKOFF_MAX_SECONDS,
                    )
                    self.retries += 1
                    logger.warning("DDG resolve retry %d for '%s': %s", attempt + 1, name, e)
                    self._audit.log("enrich", "retry", name=name, attempt=attempt + 1, error=str(e))
                    time.sleep(delay)
                else:
                    self.failures += 1
                    logger.exception("DDG resolve permanently failed for '%s'", name)
                    self._audit.log("enrich", "permanent_failure", name=name, error=str(e))
                    return None
        return None  # unreachable, satisfies mypy
