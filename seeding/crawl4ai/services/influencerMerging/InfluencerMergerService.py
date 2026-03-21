"""InfluencerMerger — Single class for all influencer dedup/merge operations.

Unifies identity-based grouping and blocked-handle filtering into one class
with two public methods:

  merge(list[Influencer]) → list[Influencer]
      Groups same-person entries by normalized handle or name.
      Merges handles dicts, picks best name, unions source_urls.

  filter_blocked(list[Influencer]) → list[Influencer]
      Removes handleless entries and entries with blocked handles.

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
from typing import Callable

from config.schema import Influencer, Platform, CategoryCitation
from services.influencerProvenance.CategoryProvenanceTaggerService import CategoryProvenanceTagger
from services.extraction.RegexHandleExtractorService import RegexHandleExtractorService
from services.extraction.NameCleanerService import NameCleanerService as NameCleaner


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

class InfluencerMergerService:
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
                most_seen_category=inf.most_seen_category,
                seen_in_categories=list(inf.seen_in_categories),
            )

            is_llm_only = inf.extraction_methods == {"llm"}

            if key in buckets:
                # Guard: LLM-only entries with a name that doesn't match
                # any existing entry in this bucket → refuse the merge.
                # LLM adjacent-row mix-ups produce wrong name-handle pairings
                # (e.g. "Angelica Teixeira" + TK:"jenselter") that would
                # contaminate the real person's bucket.
                if is_llm_only and name_lower:
                    existing_names = {
                        e.name_lower for e in buckets[key] if e.name_lower
                    }
                    if existing_names and name_lower not in existing_names:
                        continue  # LLM row mix-up — drop entirely
                buckets[key].append(entry)
            else:
                buckets[key] = [entry]
                # Also register by name if it's a real name (not just handle).
                # Skip for LLM-only entries — LLM name-handle pairings are
                # too unreliable for identity grouping (adjacent-row mix-ups
                # cause cross-handle contamination, e.g. Angelica/Jen Selter).
                if name_lower and name_lower != first_handle and not is_llm_only:
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
    def filter_blocked(
        influencers: list[Influencer],
        handle_filter: Callable[[str], bool] = RegexHandleExtractorService.is_blocked_handle,
    ) -> list[Influencer]:
        """Remove handleless entries and entries with any blocked handle.

        Args:
            influencers: Merged list where each person appears once.
            handle_filter: Callable returning True if a handle is blocked.

        Returns:
            Filtered list — only entries with at least one non-blocked handle.
        """
        return [
            inf for inf in influencers
            if inf.handles
            and not any(handle_filter(h) for h in inf.handles.values())
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
        "most_seen_category", "seen_in_categories",
    )

    def __init__(
        self,
        handles: dict[Platform, str],
        name: str,
        name_lower: str,
        original_index: int,
        source_urls: set[str] | None = None,
        extraction_methods: set[str] | None = None,
        most_seen_category: str = "",
        seen_in_categories: list[CategoryCitation] | None = None,
    ) -> None:
        self.handles = handles
        self.name = name
        self.name_lower = name_lower
        self.original_index = original_index
        self.source_urls = source_urls or set()
        self.extraction_methods = extraction_methods or set()
        self.most_seen_category = most_seen_category
        self.seen_in_categories = seen_in_categories or []

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
        # Defensive: __post_init__ already cleans, but re-clean in case
        # entries were built without going through Influencer constructor.
        best_name = NameCleaner.clean_name(entries[0].name) or ""

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

    # Union seen_in_categories from ALL entries — sum citations per (cat, sub)
    cat_sub_counts: dict[tuple[str, str], int] = {}
    for entry in entries:
        for cc in entry.seen_in_categories:
            key = (cc.category, cc.sub)
            cat_sub_counts[key] = cat_sub_counts.get(key, 0) + cc.citations

    merged = Influencer(
        name=best_name,
        handles=merged_handles,
        source_urls=all_sources,
        extraction_methods=all_methods,
    )

    if cat_sub_counts:
        CategoryProvenanceTagger.apply_provenance(
            inf=merged,
            cat_sub_counts=cat_sub_counts,
        )

    return merged

