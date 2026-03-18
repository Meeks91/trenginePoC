"""
NameMentionTracker — Aggregate influencer name mentions across all pages.

Extracts candidate names from every crawled page, groups them into
fuzzy-similarity buckets (≥ 90% ratio via difflib), and tracks:
  - mention_count  : total occurrences across all pages
  - source_types   : which extraction methods contributed (SourceType enum)
  - source_urls    : which page URLs contributed
  - platforms      : which platforms this name appeared under
  - categories     : which categories
  - sub_names      : which sub-categories
  - regions        : which regions

Usage:
    tracker = NameMentionTracker()
    tracker.record_names_in_url(
        names_with_counts={"Jeff Nippard": 3},
        source_url="https://reddit.com/r/fitness/...",
        source_type=SourceType.REDDIT,
        platform="Instagram",
        category="Fitness",
        sub_name="Gym",
        region="US",
    )
    mentions = tracker.all_names
    reddit_top = tracker.top_reddit_names(max_per_group=5)
"""

from __future__ import annotations

import difflib
from collections import defaultdict, deque
from collections.abc import Iterator
from dataclasses import dataclass, field

from config.schema import Influencer, SourceType

# Type aliases for bucket parallel-list elements
type VariantCounts = dict[str, int]
type StringSet = set[str]
type BucketRow = tuple[
    VariantCounts, bool, StringSet, StringSet,
    StringSet, StringSet, StringSet, StringSet,
]
type GroupKey = tuple[str, str, str, str]  # (platform, category, sub, region)

from services.extraction.NameCleaner import _ALL_NON_PERSON as _CLEANER_BLOCKLIST

# Belt-and-suspenders: names in _CLEANER_BLOCKLIST are already filtered
# upstream by NameCleaner.clean_name(), but we re-check here to guard
# against any code path that bypasses the cleaner.
_NOISE_LOWER: frozenset[str] = _CLEANER_BLOCKLIST



# ══════════════════════════════════════════════════════════════════════
# Data Model
# ══════════════════════════════════════════════════════════════════════

@dataclass
class NameMention:
    """A single fuzzy-merged name bucket."""
    canonical: str
    variants: list[str]
    mention_count: int
    was_searched: bool
    source_types: list[str] = field(default_factory=list)
    source_urls: set[str] = field(default_factory=set)
    sub_names: list[str] = field(default_factory=list)
    platforms: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    regions: list[str] = field(default_factory=list)


# ══════════════════════════════════════════════════════════════════════
# Tracker
# ══════════════════════════════════════════════════════════════════════

_FUZZY_THRESHOLD = 0.90


class NameMentionTracker:
    """Aggregates name occurrences across pages with fuzzy grouping."""

    def __init__(self) -> None:
        self._buckets: list[dict[str, int]] = []
        self._searched: list[bool] = []
        self._source_types: list[set[str]] = []
        self._source_urls: list[set[str]] = []
        self._sub_names: list[set[str]] = []
        self._platforms: list[set[str]] = []
        self._categories: list[set[str]] = []
        self._regions: list[set[str]] = []
        self._norm_index: dict[str, int] = {}

    # ── Public API ─────────────────────────────────────────────────────

    def record_names_in_url(
        self,
        names_with_counts: dict[str, int],
        source_url: str,
        source_type: SourceType,
        platform: str,
        category: str,
        sub_name: str,
        region: str,
    ) -> None:
        """Record names found at a specific URL.

        Args:
            names_with_counts: {name: occurrence_count} from one page.
            source_url: the page URL where these names were found.
            source_type: extraction provenance (SourceType enum).
            platform: e.g. "Instagram".
            category: e.g. "AI".
            sub_name: e.g. "AI Tools & Reviews".
            region: e.g. "US".
        """
        for name, count in names_with_counts.items():
            idx = self._find_bucket(name)
            if idx is None:
                new_idx = len(self._buckets)
                self._buckets.append({name: count})
                self._searched.append(False)
                self._source_types.append({source_type.value})
                self._source_urls.append({source_url})
                self._sub_names.append({sub_name} if sub_name else set())
                self._platforms.append({platform} if platform else set())
                self._categories.append({category} if category else set())
                self._regions.append({region} if region else set())
                self._register_bucket(name, new_idx)
            else:
                self._buckets[idx][name] = (
                    self._buckets[idx].get(name, 0) + count
                )
                self._source_types[idx].add(source_type.value)
                self._source_urls[idx].add(source_url)
                if sub_name:
                    self._sub_names[idx].add(sub_name)
                if platform:
                    self._platforms[idx].add(platform)
                if category:
                    self._categories[idx].add(category)
                if region:
                    self._regions[idx].add(region)

    def mark_searched(self, names: set[str] | list[str]) -> None:
        """Mark buckets containing any of these names as was_searched=True."""
        for name in names:
            idx = self._find_bucket(name)
            if idx is not None:
                self._searched[idx] = True

    # ── Internal ───────────────────────────────────────────────────────

    def _build_mention(
        self,
        bucket: dict[str, int],
        searched: bool,
        sources: set[str],
        urls: set[str],
        subs: set[str],
        platforms: set[str],
        categories: set[str],
        regions: set[str],
    ) -> NameMention:
        total = sum(bucket.values())
        canonical = max(bucket, key=lambda v: bucket[v])
        return NameMention(
            canonical=canonical,
            variants=sorted(bucket.keys()),
            mention_count=total,
            was_searched=searched,
            source_types=sorted(sources),
            source_urls=set(urls),
            sub_names=sorted(subs),
            platforms=sorted(platforms),
            categories=sorted(categories),
            regions=sorted(regions),
        )

    @property
    def all_names(self) -> list[NameMention]:
        """All name buckets, sorted by mention_count DESC."""
        result = [
            self._build_mention(
                bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions,
            )
            for bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions
            in self._iter_buckets()
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    @property
    def reddit_names(self) -> list[NameMention]:
        """Buckets where "reddit" ∈ source_types, sorted by mention_count DESC."""
        result = [
            self._build_mention(
                bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions,
            )
            for bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions
            in self._iter_buckets()
            if SourceType.REDDIT.value in source_types
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    @property
    def non_reddit_names(self) -> list[NameMention]:
        """Buckets where "reddit" ∉ source_types, sorted by mention_count DESC."""
        result = [
            self._build_mention(
                bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions,
            )
            for bucket, searched, source_types,
                source_urls, sub_names, platforms, categories, regions
            in self._iter_buckets()
            if SourceType.REDDIT.value not in source_types
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    def top_reddit_names(self, max_per_group: int, min_mentions: int) -> list[NameMention]:
        """Top N reddit-gated names per (platform, category, sub, region) group.

        Candidates must have at least one reddit source (quality gate).
        Ranked by total mention_count (reddit + listicle combined) so
        cross-source validation boosts genuine influencers above noise.
        """
        reddit = [m for m in self.reddit_names
                  if m.mention_count >= min_mentions
                  and m.canonical.lower() not in _NOISE_LOWER]

        groups: dict[tuple[str, ...], list[NameMention]] = defaultdict(list)
        for mention in reddit:
            for plat in mention.platforms:
                for cat in mention.categories:
                    for sub in mention.sub_names:
                        for reg in mention.regions:
                            key = (plat, cat, sub, reg)
                            groups[key].append(mention)

        seen_canonicals: set[str] = set()
        selected: list[NameMention] = []
        for _key, mentions in groups.items():
            mentions.sort(key=lambda m: m.mention_count, reverse=True)
            for mention in mentions[:max_per_group]:
                if mention.canonical not in seen_canonicals:
                    seen_canonicals.add(mention.canonical)
                    selected.append(mention)

        selected.sort(key=lambda m: m.mention_count, reverse=True)
        return selected

    def top_unresolved_reddit_names_by_group(
        self,
        max_candidates_per_group: int,
        min_mentions: int,
        known_influencers: list[Influencer],
    ) -> dict[GroupKey, deque[NameMention]]:
        """Per-group ranked queues for slot recycling.

        Returns up to max_candidates_per_group candidates per group,
        sorted by total mention_count DESC. Reddit gate applied
        (only names with at least one reddit source included).
        Names already known (have handles in extracted data) are excluded.
        """
        from services.extraction.KnownNameIndex import KnownNameIndex
        name_index = KnownNameIndex(known_influencers)

        reddit = [m for m in self.reddit_names
                  if m.mention_count >= min_mentions
                  and m.canonical.lower() not in _NOISE_LOWER
                  and not name_index.has_handles(m.canonical)]

        groups: dict[GroupKey, list[NameMention]] = defaultdict(list)
        for mention in reddit:
            for plat in mention.platforms:
                for cat in mention.categories:
                    for sub in mention.sub_names:
                        for reg in mention.regions:
                            groups[(plat, cat, sub, reg)].append(mention)

        result: dict[GroupKey, deque[NameMention]] = {}
        for key, mentions in groups.items():
            mentions.sort(key=lambda m: m.mention_count, reverse=True)
            result[key] = deque(mentions[:max_candidates_per_group])
        return result

    def merge(self, other: NameMentionTracker) -> None:
        """Merge another tracker's buckets into this one."""
        for (bucket, searched, source_types,
             source_urls, sub_names, platforms, categories, regions,
        ) in other._iter_buckets():
            for name, count in bucket.items():
                idx = self._find_bucket(name)
                if idx is None:
                    self._buckets.append({name: count})
                    self._searched.append(searched)
                    self._source_types.append(set(source_types))
                    self._source_urls.append(set(source_urls))
                    self._sub_names.append(set(sub_names))
                    self._platforms.append(set(platforms))
                    self._categories.append(set(categories))
                    self._regions.append(set(regions))
                else:
                    self._buckets[idx][name] = (
                        self._buckets[idx].get(name, 0) + count
                    )
                    if searched:
                        self._searched[idx] = True
                    self._source_types[idx].update(source_types)
                    self._source_urls[idx].update(source_urls)
                    self._sub_names[idx].update(sub_names)
                    self._platforms[idx].update(platforms)
                    self._categories[idx].update(categories)
                    self._regions[idx].update(regions)

    # ── Internal helpers ────────────────────────────────────────────────

    def _iter_buckets(self) -> Iterator[BucketRow]:
        """Iterate all parallel lists as tuples."""
        return zip(
            self._buckets, self._searched, self._source_types,
            self._source_urls, self._sub_names, self._platforms,
            self._categories, self._regions,
        )

    @staticmethod
    def _normalize_key(name: str) -> str:
        """Collapse whitespace and lowercase for exact-match indexing."""
        return " ".join(name.lower().split())

    def _register_bucket(self, name: str, idx: int) -> None:
        """Add a normalized key → bucket index mapping."""
        self._norm_index[self._normalize_key(name)] = idx

    def _find_bucket(self, name: str) -> int | None:
        """Return index of an existing bucket matching this name.

        Uses a two-tier strategy:
          1. O(1) exact lookup via normalized key index (handles 95%+ of cases)
          2. O(N) fuzzy fallback for genuinely novel names (rare after warmup)
        """
        norm = self._normalize_key(name)
        idx = self._norm_index.get(norm)
        if idx is not None:
            return idx

        name_lower = name.lower()
        for idx, bucket in enumerate(self._buckets):
            canonical = max(bucket, key=lambda v: bucket[v])
            ratio = difflib.SequenceMatcher(
                None, name_lower, canonical.lower()
            ).ratio()
            if ratio >= _FUZZY_THRESHOLD:
                self._norm_index[norm] = idx
                return idx
        return None
