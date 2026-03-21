"""
verify_results — Post-crawl quality check for seeds.json
=========================================================
Validates pipeline output across 8 dimensions:
  1. Merge integrity (duplicate handles, missed merges)
  2. Name cleanliness (empty, blocklisted, invalid)
  3. Platform coverage (IG / TK / YT presence, per-type breakdown)
  4. Category correctness (most_seen_category is sub, not parent)
  5. Canary presence (per category/sub/region, scopeable by --category)
  6. Handle quality (URL fragments, LinkedIn slugs, etc.)
  7. Name resolution signal quality (zero-citation seeds, empty extraction_methods)
  8. Overall stats (counts, distributions, citation density warnings)

Usage:
    python verify_results.py results/2026-03-21_3.13am_US/seeds.json
    python verify_results.py results/2026-03-21_3.13am_US/seeds.json --region US
    python verify_results.py results/2026-03-21_3.13am_US/seeds.json --category FITNESS
"""

from __future__ import annotations

import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

_SCRIPT_DIR = Path(__file__).resolve().parent
_CANARY_PATH = _SCRIPT_DIR / "config" / "canary_influencers.json"
_CATEGORIES_PATH = _SCRIPT_DIR / "config" / "categories" / "all_categories.json"

_LINKEDIN_SLUG_RE = re.compile(r"^[a-z]+-[a-z]+(?:-[a-z0-9]+)*-\d{4,}$")
_NAME_RE = re.compile(
    r"\b("
    r"[A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'\u2019-]+"
    r"\s[A-ZÀ-ÖØ-Þ][a-zA-ZÀ-ÖØ-öø-ÿ'\u2019-]+"
    r")\b"
)


# ══════════════════════════════════════════════════════════════════════
# Data Loading
# ══════════════════════════════════════════════════════════════════════


def _load_seeds(path: str) -> list[dict]:
    with open(path) as f:
        return cast(list[dict], json.load(f))


def _load_canaries() -> dict:
    with open(_CANARY_PATH) as f:
        return cast(dict, json.load(f))


def _load_parent_category_keys() -> set[str]:
    with open(_CATEGORIES_PATH) as f:
        data = json.load(f)
    return {entry["category"] for entry in data}


# ══════════════════════════════════════════════════════════════════════
# Check Result
# ══════════════════════════════════════════════════════════════════════


@dataclass
class CheckResult:
    name: str
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)
        self.passed = False

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)


# ══════════════════════════════════════════════════════════════════════
# 1. Merge Integrity
# ══════════════════════════════════════════════════════════════════════


def check_merge_integrity(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Merge Integrity")

    handle_to_seeds: dict[str, list[int]] = defaultdict(list)
    for i, seed in enumerate(seeds):
        for key in ("ig_handle", "tk_handle", "yt_handle"):
            handle = seed.get(key, "")
            if handle:
                composite = f"{key}:{handle.lower()}"
                handle_to_seeds[composite].append(i)

    dupes_found = 0
    for composite, indices in handle_to_seeds.items():
        if len(indices) > 1:
            platform, handle = composite.split(":", 1)
            names = [seeds[i].get("name", "?") for i in indices]
            result.error(
                f"Duplicate {platform} handle '{handle}' on seeds: "
                f"{', '.join(f'#{i} ({n})' for i, n in zip(indices, names))}"
            )
            dupes_found += 1

    cross_platform_map: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for i, seed in enumerate(seeds):
        for key in ("ig_handle", "tk_handle", "yt_handle"):
            handle = seed.get(key, "")
            if handle:
                cross_platform_map[handle.lower()].append((i, key))

    cross_dupes = 0
    for handle, entries in cross_platform_map.items():
        seed_indices = {i for i, _ in entries}
        if len(seed_indices) > 1:
            details = []
            for i, key in entries:
                name = seeds[i].get("name", "?") or "(no name)"
                details.append(f"#{i} {key} ({name})")
            result.error(
                f"Cross-platform dupe '{handle}': {', '.join(details)}"
            )
            cross_dupes += 1

    name_groups: dict[str, list[int]] = defaultdict(list)
    for i, seed in enumerate(seeds):
        name = seed.get("name", "").strip()
        if name:
            name_groups[name.lower()].append(i)

    missed_merges = 0
    for name_key, indices in name_groups.items():
        if len(indices) > 1:
            handle_sets = []
            for i in indices:
                s = seeds[i]
                handles = {
                    k: s.get(k, "") for k in ("ig_handle", "tk_handle", "yt_handle")
                    if s.get(k, "")
                }
                handle_sets.append(handles)

            if len(set(frozenset(h.items()) for h in handle_sets)) > 1:
                result.error(
                    f"Possible missed merge: name '{seeds[indices[0]]['name']}' "
                    f"appears {len(indices)} times with different handle sets"
                )
                missed_merges += 1

    result.add_info(f"Duplicate handles: {dupes_found}")
    result.add_info(f"Cross-platform dupes: {cross_dupes}")
    result.add_info(f"Possible missed merges: {missed_merges}")
    return result


# ══════════════════════════════════════════════════════════════════════
# 2. Name Cleanliness
# ══════════════════════════════════════════════════════════════════════


def check_name_cleanliness(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Name Cleanliness")

    empty_count = 0
    single_word = 0
    suspicious: list[str] = []

    for seed in seeds:
        name = seed.get("name", "")
        if not name.strip():
            empty_count += 1
            continue

        if len(name.split()) < 2:
            single_word += 1
            suspicious.append(name)

        if not _NAME_RE.search(name):
            suspicious.append(name)

        if len(name) > 40:
            result.warn(f"Unusually long name: '{name}'")

        if re.search(r"[<>\[\]{}|\\/@#$%^&*()+=]", name):
            result.error(f"Name contains special chars: '{name}'")

    if empty_count:
        result.add_info(f"Handle-only entries (no name): {empty_count}")
    if single_word:
        result.warn(f"Single-word names: {single_word} — {suspicious[:5]}")
    if suspicious and not single_word:
        result.warn(f"Suspicious names: {suspicious[:10]}")

    result.add_info(
        f"Named entries: {len(seeds) - empty_count}/{len(seeds)}"
    )
    return result


# ══════════════════════════════════════════════════════════════════════
# 3. Platform Coverage
# ══════════════════════════════════════════════════════════════════════


def check_platform_coverage(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Platform Coverage")
    total = len(seeds)
    if total == 0:
        result.error("No seeds found")
        return result

    ig = sum(1 for s in seeds if s.get("ig_handle"))
    tk = sum(1 for s in seeds if s.get("tk_handle"))
    yt = sum(1 for s in seeds if s.get("yt_handle"))
    no_handle = sum(
        1 for s in seeds
        if not s.get("ig_handle") and not s.get("tk_handle") and not s.get("yt_handle")
    )

    platform_counts = {"ig": 0, "tk": 0, "yt": 0}
    for s in seeds:
        present = 0
        if s.get("ig_handle"):
            platform_counts["ig"] += 1
            present += 1
        if s.get("tk_handle"):
            platform_counts["tk"] += 1
            present += 1
        if s.get("yt_handle"):
            platform_counts["yt"] += 1
            present += 1

    def platform_count(ig_req: bool, tk_req: bool, yt_req: bool) -> int:
        return sum(
            1 for s in seeds
            if bool(s.get("ig_handle")) == ig_req
            and bool(s.get("tk_handle")) == tk_req
            and bool(s.get("yt_handle")) == yt_req
        )

    multi_platform = sum(
        1 for s in seeds
        if sum(bool(s.get(k)) for k in ("ig_handle", "tk_handle", "yt_handle")) >= 2
    )
    ig_only = platform_count(ig_req=True, tk_req=False, yt_req=False)
    tk_only = platform_count(ig_req=False, tk_req=True, yt_req=False)
    yt_only = platform_count(ig_req=False, tk_req=False, yt_req=True)

    result.add_info(f"Instagram: {ig}/{total} ({ig*100//total}%)")
    result.add_info(f"TikTok:    {tk}/{total} ({tk*100//total}%)")
    result.add_info(f"YouTube:   {yt}/{total} ({yt*100//total}%)")
    result.add_info(f"Multi-platform (2+): {multi_platform}/{total} ({multi_platform*100//total}%)")
    result.add_info(f"  IG only: {ig_only}  |  TK only: {tk_only}  |  YT only: {yt_only}")

    if no_handle:
        result.error(f"Seeds with NO handles at all: {no_handle}")

    for platform, count in [("Instagram", ig), ("TikTok", tk), ("YouTube", yt)]:
        if count == 0:
            result.error(f"Zero {platform} handles found")
        elif count < total * 0.05:
            result.warn(f"Very low {platform} coverage: {count}/{total}")

    if multi_platform < total * 0.05:
        result.warn(f"Very low multi-platform yield: {multi_platform}/{total} ({multi_platform*100//total}%) — NR or TK/YT crawl coverage may be thin")

    return result


# ══════════════════════════════════════════════════════════════════════
# 4. Category Correctness
# ══════════════════════════════════════════════════════════════════════


def check_category_correctness(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Category Correctness (most_seen_category)")
    parent_keys = _load_parent_category_keys()

    parent_violations: list[str] = []
    empty_category = 0
    category_dist: Counter[str] = Counter()

    for seed in seeds:
        msc = seed.get("most_seen_category", "")
        if not msc:
            empty_category += 1
            continue

        category_dist[msc] += 1

        if msc in parent_keys:
            name = seed.get("name", "?") or "(no name)"
            parent_violations.append(f"'{name}' → {msc}")

    if parent_violations:
        result.error(
            f"{len(parent_violations)} seeds have parent category as most_seen_category"
        )
        for v in parent_violations[:10]:
            result.error(f"  {v}")
        if len(parent_violations) > 10:
            result.error(f"  ... and {len(parent_violations) - 10} more")

    if empty_category:
        result.warn(f"Seeds with empty most_seen_category: {empty_category}")

    result.add_info("Sub-category distribution (top 15):")
    for cat, count in category_dist.most_common(15):
        result.add_info(f"  {cat}: {count}")

    return result


# ══════════════════════════════════════════════════════════════════════
# 5. Canary Presence
# ══════════════════════════════════════════════════════════════════════


def check_canary_presence(
    seeds: list[dict],
    region_filter: str | None = None,
    category_filter: str | None = None,
) -> CheckResult:
    result = CheckResult(name="Canary Presence")
    canaries = _load_canaries()

    seed_names_lower = {s.get("name", "").lower() for s in seeds if s.get("name")}
    seed_handles_lower: set[str] = set()
    for s in seeds:
        for key in ("ig_handle", "tk_handle", "yt_handle"):
            h = s.get(key, "")
            if h:
                seed_handles_lower.add(h.lower())

    total_canaries = 0
    found_canaries = 0
    missing_by_group: dict[str, list[str]] = {}

    for cat_key, subs in canaries.items():
        if cat_key.startswith("_"):
            continue
        if category_filter and cat_key.upper() != category_filter.upper():
            continue
        for sub_name, regions in subs.items():
            for region_code, names in regions.items():
                if region_filter and region_code != region_filter:
                    continue
                group_key = f"{cat_key}/{sub_name}/{region_code}"
                missing: list[str] = []
                for name in names:
                    total_canaries += 1
                    name_lower = name.lower()
                    if name_lower in seed_names_lower:
                        found_canaries += 1
                    elif name_lower.replace(" ", "") in seed_handles_lower:
                        found_canaries += 1
                    else:
                        missing.append(name)
                if missing:
                    missing_by_group[group_key] = missing

    pct = (found_canaries * 100 // total_canaries) if total_canaries else 0
    result.add_info(f"Canaries found: {found_canaries}/{total_canaries} ({pct}%)")

    if missing_by_group:
        result.add_info("Missing canaries by group:")
        for group, names in sorted(missing_by_group.items()):
            result.warn(f"  {group}: {', '.join(names)}")

    if pct < 20:
        result.error(f"Very low canary hit rate: {pct}%")
    elif pct < 40:
        result.warn(f"Low canary hit rate: {pct}%")

    return result


# ══════════════════════════════════════════════════════════════════════
# 6. Handle Quality
# ══════════════════════════════════════════════════════════════════════


def check_handle_quality(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Handle Quality")

    url_fragments = 0
    linkedin_slugs = 0
    too_long = 0
    has_spaces = 0

    for seed in seeds:
        for key in ("ig_handle", "tk_handle", "yt_handle"):
            handle = seed.get(key, "")
            if not handle:
                continue

            if "/" in handle:
                result.error(
                    f"URL fragment in {key}: '{handle}' "
                    f"(seed: {seed.get('name', '?')})"
                )
                url_fragments += 1

            if _LINKEDIN_SLUG_RE.match(handle.lower()):
                result.error(
                    f"LinkedIn slug in {key}: '{handle}' "
                    f"(seed: {seed.get('name', '?')})"
                )
                linkedin_slugs += 1

            if len(handle) > 30:
                result.warn(
                    f"Long handle ({len(handle)} chars) in {key}: '{handle}' "
                    f"(seed: {seed.get('name', '?')})"
                )
                too_long += 1

            if " " in handle:
                result.error(
                    f"Space in {key}: '{handle}' "
                    f"(seed: {seed.get('name', '?')})"
                )
                has_spaces += 1

    result.add_info(f"URL fragments: {url_fragments}")
    result.add_info(f"LinkedIn slugs: {linkedin_slugs}")
    result.add_info(f"Handles > 30 chars: {too_long}")
    result.add_info(f"Handles with spaces: {has_spaces}")
    return result


# ══════════════════════════════════════════════════════════════════════
# 7. Name Resolution Signal Quality
# ══════════════════════════════════════════════════════════════════════


def check_name_resolution_quality(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Name Resolution Signal Quality")
    total = len(seeds)

    zero_citation = [s for s in seeds if s.get("citation_count", 0) == 0]
    no_methods = [s for s in seeds if not s.get("extraction_methods")]
    nr_seeds = [
        s for s in seeds
        if "name_resolution" in s.get("extraction_methods", [])
    ]
    nr_zero_citation = [
        s for s in nr_seeds if s.get("citation_count", 0) == 0
    ]

    result.add_info(f"Name-resolved seeds (NR path): {len(nr_seeds)}/{total}")
    result.add_info(f"Zero-citation seeds: {len(zero_citation)} ({len(zero_citation)*100//total}%)")
    result.add_info(f"  Of which via NR path: {len(nr_zero_citation)}")
    result.add_info(f"Seeds with empty extraction_methods: {len(no_methods)}")

    if len(no_methods) > 0:
        sample = [
            s.get("ig_handle") or s.get("tk_handle") or s.get("yt_handle") or "?"
            for s in no_methods[:5]
        ]
        result.warn(
            f"{len(no_methods)} seeds have no extraction_methods recorded "
            f"(provenance gap) — sample: {sample}"
        )

    zero_pct = len(zero_citation) * 100 // total if total else 0
    if zero_pct > 10:
        result.warn(
            f"High zero-citation rate: {zero_pct}% — "
            "consider whether NR threshold or page crawl depth needs tuning"
        )

    return result


# ══════════════════════════════════════════════════════════════════════
# 7. Overall Stats
# ══════════════════════════════════════════════════════════════════════


def check_overall_stats(seeds: list[dict]) -> CheckResult:
    result = CheckResult(name="Overall Stats")
    total = len(seeds)
    result.add_info(f"Total seeds: {total}")

    extraction_methods: Counter[str] = Counter()
    citations: list[int] = []
    source_counts: list[int] = []
    category_dist: Counter[str] = Counter()

    for seed in seeds:
        for method in seed.get("extraction_methods", []):
            extraction_methods[method] += 1
        citations.append(seed.get("citation_count", 0))
        source_counts.append(len(seed.get("source_urls", [])))

        for cat_entry in seed.get("seen_in_categories", []):
            category_dist[cat_entry.get("category", "?")] += 1

    result.add_info("Extraction methods:")
    for method, count in extraction_methods.most_common():
        result.add_info(f"  {method}: {count} seeds")

    if citations:
        median_citations = statistics.median(citations)
        result.add_info(
            f"Citations: min={min(citations)}, "
            f"median={median_citations:.0f}, "
            f"mean={statistics.mean(citations):.1f}, "
            f"max={max(citations)}"
        )
        if median_citations <= 1:
            result.warn(
                "Median citation count is 1 — most seeds seen on only one page. "
                "Signal is thin; consider adding more crawl sources or deeper crawls."
            )

    if source_counts:
        result.add_info(
            f"Source URLs: min={min(source_counts)}, "
            f"median={statistics.median(source_counts):.0f}, "
            f"mean={statistics.mean(source_counts):.1f}, "
            f"max={max(source_counts)}"
        )

    result.add_info("Category distribution (by citation entries):")
    for cat, count in category_dist.most_common():
        result.add_info(f"  {cat}: {count}")

    return result


# ══════════════════════════════════════════════════════════════════════
# Report Printer
# ══════════════════════════════════════════════════════════════════════


_GREEN = "\033[92m"
_YELLOW = "\033[93m"
_RED = "\033[91m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def _print_result(check: CheckResult) -> None:
    icon = f"{_GREEN}✅" if check.passed and not check.warnings else (
        f"{_YELLOW}⚠️" if check.passed else f"{_RED}❌"
    )
    print(f"\n{_BOLD}{icon}  {check.name}{_RESET}")
    print("─" * 60)

    for msg in check.errors:
        print(f"  {_RED}✗ {msg}{_RESET}")
    for msg in check.warnings:
        print(f"  {_YELLOW}⚠ {msg}{_RESET}")
    for msg in check.info:
        print(f"  {msg}")


def _print_summary(results: list[CheckResult]) -> None:
    print(f"\n{'═' * 60}")
    print(f"{_BOLD}Summary{_RESET}")
    print(f"{'═' * 60}")

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    for r in results:
        icon = f"{_GREEN}✅" if r.passed and not r.warnings else (
            f"{_YELLOW}⚠️" if r.passed else f"{_RED}❌"
        )
        err_str = f" ({len(r.errors)} errors)" if r.errors else ""
        warn_str = f" ({len(r.warnings)} warnings)" if r.warnings else ""
        print(f"  {icon} {r.name}{_RED}{err_str}{_YELLOW}{warn_str}{_RESET}")

    print()
    if total_errors:
        print(f"  {_RED}{_BOLD}ERRORS: {total_errors}{_RESET}")
    if total_warnings:
        print(f"  {_YELLOW}{_BOLD}WARNINGS: {total_warnings}{_RESET}")
    if not total_errors and not total_warnings:
        print(f"  {_GREEN}{_BOLD}ALL CHECKS PASSED{_RESET}")
    print()


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════


def run_verification(
    seeds_path: str,
    region_filter: str | None = None,
    category_filter: str | None = None,
) -> int:
    seeds = _load_seeds(seeds_path)
    print(f"{_BOLD}Verifying: {seeds_path}{_RESET}")
    print(f"Seeds loaded: {len(seeds)}")
    if region_filter:
        print(f"Region filter: {region_filter}")
    if category_filter:
        print(f"Category filter: {category_filter}")

    results = [
        check_merge_integrity(seeds),
        check_name_cleanliness(seeds),
        check_platform_coverage(seeds),
        check_category_correctness(seeds),
        check_canary_presence(seeds, region_filter=region_filter, category_filter=category_filter),
        check_handle_quality(seeds),
        check_name_resolution_quality(seeds),
        check_overall_stats(seeds),
    ]

    for r in results:
        _print_result(r)

    _print_summary(results)

    total_errors = sum(len(r.errors) for r in results)
    total_warnings = sum(len(r.warnings) for r in results)

    if total_errors:
        return 2
    if total_warnings:
        return 1
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <seeds.json> [--region US|UK] [--category FITNESS]")
        sys.exit(1)

    seeds_path = sys.argv[1]
    region_filter = None
    category_filter = None

    if "--region" in sys.argv:
        idx = sys.argv.index("--region")
        if idx + 1 < len(sys.argv):
            region_filter = sys.argv[idx + 1]

    if "--category" in sys.argv:
        idx = sys.argv.index("--category")
        if idx + 1 < len(sys.argv):
            category_filter = sys.argv[idx + 1]

    exit_code = run_verification(
        seeds_path=seeds_path,
        region_filter=region_filter,
        category_filter=category_filter,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
