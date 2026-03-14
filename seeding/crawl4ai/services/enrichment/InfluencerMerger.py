"""InfluencerMerger — Single class for all influencer dedup/merge operations.

Unifies IdentityGrouper (identity-based grouping) and SeedMerger (DB-ready
flattening) into one class with two public methods:

  merge(list[Influencer]) → list[Influencer]
      Groups same-person entries by normalized handle or name.
      Merges handles dicts, picks best name, unions source_urls.

  to_seeds(list[tuple[Influencer, str]]) → list[SeedInfluencer]
      Deduplicates category-tagged influencers and converts to
      DB-ready SeedInfluencer records with ig/tk/yt handle columns.

Identity rules:
  1. Two entries have the same NORMALIZED handle → same person
  2. Two entries have the same NAME (lowercased, stripped) AND the name
     is not equal to either handle → same person
  3. Handle normalization strips @, _, dots, and common affixes
     (the, real, official, etc.)

Minimum handle length: 3 chars after normalization (catches broken
extraction artifacts like "ab").

Supported platforms: Instagram, TikTok, YouTube (config.schema.Platform).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from config.schema import Influencer, Platform, SeedInfluencer
from services.extraction.RegexHandleExtractor import is_blocked_handle


# ══════════════════════════════════════════════════════════════════════
# Constants
# ══════════════════════════════════════════════════════════════════════

# Platforms we keep in the final output
_SUPPORTED_PLATFORMS: frozenset[Platform] = frozenset(Platform)

# Minimum handle length after normalization.
# Catches truly broken handles (1-2 chars) that are never real.
_MIN_HANDLE_LENGTH = 3

# Common handle prefixes/suffixes that don't change identity
_STRIP_AFFIXES = re.compile(
    r'^(the|real|official|iam|itsme|its|im|i_am|hey|hi|mr|mrs|ms|dr|dj|mc)'
    r'|'
    r'(official|real|_official|_real|tv|hq|page)$',
    re.IGNORECASE,
)


# ══════════════════════════════════════════════════════════════════════
# Public class
# ══════════════════════════════════════════════════════════════════════

class InfluencerMerger:
    """Single class for all influencer dedup/merge operations."""

    @staticmethod
    def merge(influencers: list[Influencer]) -> list[Influencer]:
        """Merge same-person entries into single Influencers with merged handles.

        Platform-agnostic — no target_platform concept. Takes a flat list
        (potentially one entry per handle×platform) and returns a shorter
        list where each person appears once.

        Args:
            influencers: Flat list of Influencer entries.

        Returns:
            Merged list where each unique identity appears once, with all
            platform handles in the ``handles`` dict.
        """
        # ── Step 1: Build identity buckets ──
        buckets: dict[str, list[_Entry]] = {}
        for idx, inf in enumerate(influencers):
            name_lower = inf.name.strip().lower() if inf.name else ""

            # Get first handle for keying (may have 0 or more)
            first_handle = ""
            for _plat, h in inf.handles.items():
                first_handle = h.lower().strip().lstrip("@")
                break

            # Identity key: prefer normalized handle, fall back to name
            if first_handle:
                key = _normalize_handle(first_handle)
            elif name_lower:
                key = f"name:{name_lower}"
            else:
                continue  # No identity signal at all — drop

            entry = _Entry(
                handles=dict(inf.handles),
                name=inf.name,
                name_lower=name_lower,
                original_index=idx,
                source_urls=set(inf.source_urls),
                extraction_methods=set(inf.extraction_methods),
            )

            if key in buckets:
                buckets[key].append(entry)
            else:
                buckets[key] = [entry]
                # Also register by name if it's a real name (not just handle)
                if name_lower and name_lower != first_handle:
                    name_key = f"name:{name_lower}"
                    if name_key != key:
                        if name_key not in buckets:
                            buckets[name_key] = buckets[key]  # Alias same list
                        else:
                            _merge_groups(buckets, key, name_key)
                # Handle-as-name with dots: "rena.awada" → try "rena awada"
                # to merge with real-name entries like "Rena Awada".
                # Only for multi-word results (2+ words after split) to
                # avoid false merges on single-word handles.
                elif name_lower and "." in name_lower:
                    dotless = name_lower.replace(".", " ").strip()
                    if len(dotless.split()) >= 2:
                        dot_key = f"name:{dotless}"
                        if dot_key not in buckets:
                            buckets[dot_key] = buckets[key]
                        else:
                            _merge_groups(buckets, key, dot_key)

        # ── Step 2: Deduplicate bucket aliases ──
        seen_ids: set[int] = set()
        unique_groups: list[list[_Entry]] = []
        for group in buckets.values():
            group_id = id(group)
            if group_id not in seen_ids:
                seen_ids.add(group_id)
                unique_groups.append(group)

        # ── Step 3: Build grouped Influencers ──
        result: list[Influencer] = []
        for group in unique_groups:
            grouped = _build_grouped_influencer(group)
            if grouped is not None:
                result.append(grouped)

        return result

    @staticmethod
    def to_seeds(
        entries: list[tuple[Influencer, str]],
        handle_filter: Callable[[str], bool] = is_blocked_handle,
    ) -> list[SeedInfluencer]:
        """Convert category-tagged Influencers to DB-ready SeedInfluencer records.

        Deduplicates by (handle_lower, platform), picks best name, merges
        categories and cross-platform handles.

        Args:
            entries: List of (Influencer, category_key) tuples.

        Returns:
            Deduped list of SeedInfluencer records.
        """
        merged: dict[tuple[str, str], _SeedEntry] = {}

        for inf, category in entries:
            for plat, handle in inf.handles.items():
                handle_lower = handle.lower().lstrip("@")
                key = (handle_lower, plat.value.lower())

                if key not in merged:
                    merged[key] = _SeedEntry(
                        best_name=inf.name,
                        handle=handle_lower,
                        platform=plat,
                        categories={category},
                    )
                else:
                    entry = merged[key]
                    entry.categories.add(category)
                    if _is_better_name(inf.name, entry.best_name, handle_lower):
                        entry.best_name = inf.name

                # Merge other handles as alt handles
                for other_plat, other_handle in inf.handles.items():
                    if other_plat != plat:
                        merged[key].alt_handles[other_plat.value] = (
                            other_handle.lower().lstrip("@")
                        )

            # Handle influencers with no handles (name-only)
            if not inf.handles:
                name_key = ("", inf.name.lower().strip())
                if name_key not in merged:
                    merged[name_key] = _SeedEntry(
                        best_name=inf.name,
                        handle="",
                        platform=Platform.Instagram,  # Default
                        categories={category},
                    )
                else:
                    merged[name_key].categories.add(category)

        # Convert to SeedInfluencer records
        results: list[SeedInfluencer] = []
        for entry in merged.values():
            seed = SeedInfluencer(
                name=entry.best_name,
                categories=sorted(entry.categories),
            )

            # Assign handle to correct platform column
            _assign_platform_handle(seed, entry.platform.value, entry.handle)

            # Assign alt handles to their platform columns
            for plat_value, alt_handle in entry.alt_handles.items():
                _assign_platform_handle(seed, plat_value, alt_handle)

            results.append(seed)

        return [
            s for s in results
            if _has_any_handle(s) and not _is_blocked_seed(s, handle_filter)
        ]


# ══════════════════════════════════════════════════════════════════════
# Shared helpers
# ══════════════════════════════════════════════════════════════════════

def _normalize_handle(raw: str) -> str:
    """Normalize a handle for identity comparison.

    Strips @, underscores, dots, and common prefixes/suffixes so that
    ``_deliciouslyella``, ``deliciouslyella``, and ``deliciouslyella.official``
    all normalize to the same string.
    """
    h = raw.lower().strip().lstrip("@")
    # Strip underscores and dots (purely cosmetic in handles)
    h = h.replace("_", "").replace(".", "")
    # Strip common affixes (max 2 passes to handle nested e.g. 'therealcreator')
    for _ in range(2):
        stripped = _STRIP_AFFIXES.sub("", h)
        if stripped == h or not stripped:
            break
        h = stripped
    return h


def _is_better_name(candidate: str, current: str, handle: str) -> bool:
    """Check if candidate name is better than current.

    Prefers real names (not equal to handle) over handle-as-name.
    Between two real names, prefers the longer one.
    """
    candidate_is_handle = candidate.lower().lstrip("@") == handle
    current_is_handle = current.lower().lstrip("@") == handle
    if current_is_handle and not candidate_is_handle:
        return True
    if not candidate_is_handle and not current_is_handle:
        return len(candidate) > len(current)
    return False


# ══════════════════════════════════════════════════════════════════════
# merge() internals
# ══════════════════════════════════════════════════════════════════════

class _Entry:
    """Lightweight struct for identity grouping."""
    __slots__ = (
        "handles", "name", "name_lower",
        "original_index", "source_urls", "extraction_methods",
    )

    def __init__(
        self,
        handles: dict[Platform, str],
        name: str,
        name_lower: str,
        original_index: int,
        source_urls: set[str] | None = None,
        extraction_methods: set[str] | None = None,
    ) -> None:
        self.handles = handles
        self.name = name
        self.name_lower = name_lower
        self.original_index = original_index
        self.source_urls = source_urls or set()
        self.extraction_methods = extraction_methods or set()

    @property
    def has_supported_platform(self) -> bool:
        return any(p in _SUPPORTED_PLATFORMS for p in self.handles)


def _merge_groups(
    buckets: dict[str, list[_Entry]],
    key_a: str,
    key_b: str,
) -> None:
    """Merge two bucket lists into one, updating all aliases."""
    group_a = buckets[key_a]
    group_b = buckets[key_b]
    if group_a is group_b:
        return  # Already same list object
    combined = group_a + group_b
    for k, v in buckets.items():
        if v is group_a or v is group_b:
            buckets[k] = combined


def _build_grouped_influencer(
    entries: list[_Entry],
) -> Influencer | None:
    """Collapse a group of same-person entries into one Influencer.

    Returns None if no entries have a supported platform handle.
    """
    supported = [e for e in entries if e.has_supported_platform]
    if not supported:
        return None

    # Best name: prefer longest non-handle name
    all_handle_strs = set()
    for e in entries:
        for h in e.handles.values():
            all_handle_strs.add(h.lower().lstrip("@"))

    best_name = ""
    for entry in entries:
        if (
            entry.name
            and entry.name.lower().strip().lstrip("@") not in all_handle_strs
            and len(entry.name) > len(best_name)
        ):
            best_name = entry.name

    if not best_name:
        best_name = entries[0].name or next(
            (h for e in entries for h in e.handles.values()), ""
        )

    # Merge all handles from supported entries
    merged_handles: dict[Platform, str] = {}
    for entry in supported:
        for plat, handle in entry.handles.items():
            clean = handle.lstrip("@")
            # Drop short handles — extraction noise (truncated fragments)
            if len(_normalize_handle(clean)) < _MIN_HANDLE_LENGTH:
                continue
            if plat in _SUPPORTED_PLATFORMS and plat not in merged_handles:
                merged_handles[plat] = clean

    if not merged_handles:
        return None  # All handles were too short — drop group

    # Union source_urls and extraction_methods from ALL entries (including unsupported)
    all_sources: set[str] = set()
    all_methods: set[str] = set()
    for entry in entries:
        all_sources |= entry.source_urls
        all_methods |= entry.extraction_methods

    return Influencer(
        name=best_name,
        handles=merged_handles,
        source_urls=all_sources,
        extraction_methods=all_methods,
    )


# ══════════════════════════════════════════════════════════════════════
# to_seeds() internals
# ══════════════════════════════════════════════════════════════════════

@dataclass
class _SeedEntry:
    """Internal accumulator for seed merging."""
    best_name: str
    handle: str
    platform: Platform
    alt_handles: dict[str, str] = field(default_factory=dict)  # {platform_value: handle}
    categories: set[str] = field(default_factory=set)


def _assign_platform_handle(
    seed: SeedInfluencer, platform: str, handle: str,
) -> None:
    """Assign a handle to the correct platform column on SeedInfluencer."""
    plat_lower = platform.lower()
    if plat_lower in ("instagram", ""):
        if not seed.ig_handle:
            seed.ig_handle = handle
    elif plat_lower == "tiktok":
        if not seed.tk_handle:
            seed.tk_handle = handle
    elif plat_lower == "youtube":
        if not seed.yt_handle:
            seed.yt_handle = handle


def _has_any_handle(seed: SeedInfluencer) -> bool:
    """Return True if the seed has at least one non-empty handle."""
    return bool(seed.ig_handle or seed.tk_handle or seed.yt_handle)


def _is_blocked_seed(
    seed: SeedInfluencer,
    handle_filter: Callable[[str], bool] = is_blocked_handle,
) -> bool:
    """Check if any handle on a seed is blocked by the injected filter."""
    for handle in (seed.ig_handle, seed.tk_handle, seed.yt_handle):
        if not handle:
            continue
        if handle_filter(handle):
            return True
    return False

