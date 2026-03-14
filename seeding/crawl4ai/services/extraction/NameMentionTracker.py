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
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import dataclass, field

from config.schema import SourceType

# Type aliases for bucket parallel-list elements
VariantCounts = dict[str, int]
StringSet = set[str]
BucketRow = tuple[
    VariantCounts, bool, StringSet, StringSet,
    StringSet, StringSet, StringSet, StringSet,
]


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
                self._buckets.append({name: count})
                self._searched.append(False)
                self._source_types.append({source_type.value})
                self._source_urls.append({source_url})
                self._sub_names.append({sub_name} if sub_name else set())
                self._platforms.append({platform} if platform else set())
                self._categories.append({category} if category else set())
                self._regions.append({region} if region else set())
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
            self._build_mention(b, s, st, su, sn, p, c, r)
            for b, s, st, su, sn, p, c, r in self._iter_buckets()
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    @property
    def reddit_names(self) -> list[NameMention]:
        """Buckets where "reddit" ∈ source_types, sorted by mention_count DESC."""
        result = [
            self._build_mention(b, s, st, su, sn, p, c, r)
            for b, s, st, su, sn, p, c, r in self._iter_buckets()
            if SourceType.REDDIT.value in st
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    @property
    def non_reddit_names(self) -> list[NameMention]:
        """Buckets where "reddit" ∉ source_types, sorted by mention_count DESC."""
        result = [
            self._build_mention(b, s, st, su, sn, p, c, r)
            for b, s, st, su, sn, p, c, r in self._iter_buckets()
            if SourceType.REDDIT.value not in st
        ]
        result.sort(key=lambda m: m.mention_count, reverse=True)
        return result

    def top_reddit_names(self, max_per_group: int, min_mentions: int) -> list[NameMention]:
        """Top N reddit names per (platform, category, sub, region) group.

        Uses TOTAL additive mention_count (reddit + non-reddit merged
        via fuzzy bucket identity). Only names with count >= min_mentions qualify.
        """
        reddit = [m for m in self.reddit_names if m.mention_count >= min_mentions]

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

    def merge(self, other: NameMentionTracker) -> None:
        """Merge another tracker's buckets into this one."""
        for b, s, st, su, sn, p, c, r in other._iter_buckets():
            for name, count in b.items():
                idx = self._find_bucket(name)
                if idx is None:
                    self._buckets.append({name: count})
                    self._searched.append(s)
                    self._source_types.append(set(st))
                    self._source_urls.append(set(su))
                    self._sub_names.append(set(sn))
                    self._platforms.append(set(p))
                    self._categories.append(set(c))
                    self._regions.append(set(r))
                else:
                    self._buckets[idx][name] = (
                        self._buckets[idx].get(name, 0) + count
                    )
                    if s:
                        self._searched[idx] = True
                    self._source_types[idx].update(st)
                    self._source_urls[idx].update(su)
                    self._sub_names[idx].update(sn)
                    self._platforms[idx].update(p)
                    self._categories[idx].update(c)
                    self._regions[idx].update(r)

    # ── Internal helpers ────────────────────────────────────────────────

    def _iter_buckets(self) -> Iterator[BucketRow]:
        """Iterate all parallel lists as tuples."""
        return zip(
            self._buckets, self._searched, self._source_types,
            self._source_urls, self._sub_names, self._platforms,
            self._categories, self._regions,
        )

    def _find_bucket(self, name: str) -> int | None:
        """Return index of an existing bucket that name fuzzy-matches, or None."""
        name_lower = name.lower()
        for idx, bucket in enumerate(self._buckets):
            canonical = max(bucket, key=lambda v: bucket[v])
            ratio = difflib.SequenceMatcher(
                None, name_lower, canonical.lower()
            ).ratio()
            if ratio >= _FUZZY_THRESHOLD:
                return idx
        return None
