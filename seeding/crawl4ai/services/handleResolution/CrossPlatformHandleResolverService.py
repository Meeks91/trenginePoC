"""CrossPlatformHandleResolverService — backfill handles on missing platforms.

For each influencer that already has handles on some platforms,
searches for their handles on the platforms they are missing.
Missing platforms are inferred per-influencer — no target platform needed.

Caller is responsible for deciding whether to invoke this service
(skip_cross_platform flag lives at call-site, not here).
"""

from __future__ import annotations

import logging
import time

from config.schema import Influencer, Platform
from config import (
    ENRICH_DELAY_SECONDS,
    CROSS_PLATFORM_MAX_LOOKUPS,
)
from services.audit.AuditService import AuditLog
from services.search.SearchClient import SearchClient
from services.handleResolution.patterns import (
    extract_handle_from_url,
    extract_handle_from_text,
    PLATFORM_DOMAINS,
)

logger = logging.getLogger(__name__)

_ALL_PLATFORMS = frozenset({Platform.Instagram, Platform.TikTok, Platform.YouTube})


class CrossPlatformHandleResolverService:
    """Backfill missing platform handles for influencers with existing handles.

    Constructor args fix budget and quality thresholds for the lifetime of
    this service instance. The public API is a single ``resolve()`` method.
    """

    def __init__(
        self,
        audit: AuditLog,
        *,
        search_client: SearchClient,
        max_lookups: int = CROSS_PLATFORM_MAX_LOOKUPS,
        min_sources: int = 2,
        delay_seconds: float = ENRICH_DELAY_SECONDS,
    ) -> None:
        self._audit = audit
        self._search_client = search_client
        self._max_lookups = max_lookups
        self._min_sources = min_sources
        self._delay = delay_seconds

    # API:

    def resolve(self, influencers: list[Influencer]) -> list[Influencer]:
        """For each influencer with some handles, find handles on missing platforms.

        Filters by min_sources, sorts by frequency, caps at max_lookups.
        Infers missing platforms per-influencer from their existing handles.
        Returns the original list extended with new cross-platform entries.
        """
        logger.info("\n  --- Cross-Platform Handle Resolution ---")

        candidates = [inf for inf in influencers if inf.handles]
        qualified = [inf for inf in candidates if len(inf.source_urls) >= self._min_sources]
        below_threshold = len(candidates) - len(qualified)

        qualified.sort(key=lambda inf: len(inf.source_urls), reverse=True)
        to_resolve = qualified[: self._max_lookups]
        name_only_count = sum(1 for inf in influencers if not inf.handles)

        logger.info(
            "  %d have handles, %d below min sources (%d), "
            "%d queued (top %d by frequency), %d name-only skipped",
            len(candidates),
            below_threshold,
            self._min_sources,
            len(to_resolve),
            self._max_lookups,
            name_only_count,
        )

        new_entries = self._resolve_missing_platforms(to_resolve)
        influencers.extend(new_entries)
        return influencers

    # Internal:

    def _resolve_missing_platforms(
        self,
        entries: list[Influencer],
    ) -> list[Influencer]:
        """For each influencer, search for handles on all platforms they're missing."""
        new_entries: list[Influencer] = []
        total_filled = 0

        for inf in entries:
            missing_platforms = _ALL_PLATFORMS - inf.handles.keys()
            for platform in missing_platforms:
                domain = PLATFORM_DOMAINS.get(platform)
                if not domain:
                    raise ValueError(
                        f"Platform '{platform.value}' is in _ALL_PLATFORMS but has no "
                        f"entry in PLATFORM_DOMAINS — update PLATFORM_DOMAINS to match."
                    )
                handle = self._search_handle(
                    name=inf.name,
                    platform=platform,
                    domain=domain,
                )
                if handle:
                    new_entries.append(Influencer(
                        name=inf.name,
                        handles={platform: handle.lstrip("@")},
                    ))
                    self._audit.log_handle_found(inf.name, handle)
                    existing_summary = ", ".join(
                        f"{p.value}: {h}" for p, h in inf.handles.items()
                    )
                    logger.info(
                        "    %s → %s on %s (kept %s)",
                        inf.name, handle, platform.value, existing_summary,
                    )
                    total_filled += 1
                time.sleep(self._delay)

        logger.info(
            "\n  Filled %d cross-platform handles across %d influencers",
            total_filled,
            len(entries),
        )
        return new_entries

    def _search_handle(
        self,
        name: str,
        platform: Platform,
        domain: str,
    ) -> str | None:
        """Search for an influencer's handle on a specific platform."""
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
