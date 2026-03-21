"""
Seed Crawler Pipeline v6 — CLI Entry Point

Usage:
    python cli.py --job FITNESS/Fitness/Instagram/US
    python cli.py --job FITNESS/Fitness/Instagram/US --sample 3
    python cli.py --category FITNESS
    python cli.py --all
    python cli.py --all --sample 5
    python cli.py --url https://example.com/top-influencers
    python cli.py --url https://example.com/top-influencers --platform TikTok
"""

import argparse
import asyncio
import os
import sys


from config.seed_schema import (
    SeedJob, Platform, RegionCode, REGIONS, load_categories,
)
from config import INPUT_COST_PER_1M, OUTPUT_COST_PER_1M, RESULTS_DIR, CURRENT_YEAR
from base_pipeline import SearchClientType
from pipeline import PerJobPipelineRunner
from phase_pipeline import PhasePipelineRunner
from services.search.SearchCache import SearchCache


def parse_job_key(key: str) -> tuple[str, str, str, str]:
    """Parse 'FITNESS/Fitness/Instagram/US' into (category, sub, platform, region)."""
    parts = key.split("/")
    if len(parts) != 4:
        raise ValueError(f"Job key must be CATEGORY/Sub/Platform/Region, got: {key}")
    return parts[0], parts[1], parts[2], parts[3]


def build_jobs(
    categories: dict,
    category_filter: str | None = None,
    job_key: str | None = None,
    region_filter: str | None = None,
) -> list[SeedJob]:
    """Build SeedJob list from filters."""
    jobs: list[SeedJob] = []

    for cat_key, cat in categories.items():
        if category_filter and cat_key != category_filter:
            continue

        for sub in cat.all_subs:
            for platform in Platform:
                for region_code in RegionCode:
                    if region_filter and region_code.value != region_filter:
                        continue
                    region = REGIONS[region_code]

                    if job_key:
                        key = f"{cat_key}/{sub.sub_name}/{platform.value}/{region_code.value}"
                        if key != job_key:
                            continue

                    jobs.append(SeedJob(
                        platform=platform,
                        region=region,
                        category_key=cat_key,
                        sub=sub,
                        year=CURRENT_YEAR,
                    ))

    return jobs


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Crawler Pipeline v6")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--job", type=str, help="Single job: CATEGORY/Sub/Platform/Region")
    group.add_argument("--category", type=str, help="All jobs for a category")
    group.add_argument("--all", action="store_true", help="All 432 jobs")
    group.add_argument("--url", type=str,
                        help="Single URL override: crawl+extract one page (skips Search)")
    parser.add_argument("--platform", type=str, default="Instagram",
                        help="Platform context for --url mode (default: Instagram)")
    parser.add_argument("--sample", type=int, default=None,
                        help="Only send N pages per job to LLM (rest crawled but not extracted)")
    parser.add_argument("--bfs", action="store_true", default=False,
                        help="Enable BFS link-following (crawl sublinks on each page)")
    parser.add_argument("--cross-platform-lookup", action="store_true", default=False,
                        help="Enable DDG lookup for cross-platform handles")
    parser.add_argument("--region", type=str, default=None,
                        help="Filter jobs by region code (e.g. US, UK)")
    parser.add_argument("--phase", action="store_true",
                        help="Use phase-based pipeline (search all → dedupe → crawl once → merge)")
    parser.add_argument("--name-resolution", action=argparse.BooleanOptionalAction, default=True,
                        help="Deferred name → handle resolution (default: on, disable with --no-name-resolution)")
    parser.add_argument("--name-min-mentions", type=int, default=2,
                        help="Minimum cross-page mentions before DDG fires for a name (default: 2)")
    parser.add_argument("--search-client", type=str, choices=["open", "strict"], default="open",
                        help="Search client: 'open' (DDG, free) or 'strict' (Serper, paid)")
    args = parser.parse_args()

    # Validate Serper API key when using strict client
    search_client_type = SearchClientType(args.search_client)
    if search_client_type == SearchClientType.STRICT:
        if not os.environ.get("SERPER_API_KEY"):
            print("ERROR: --search-client=strict requires SERPER_API_KEY env var")
            sys.exit(1)

    cache = SearchCache(cache_dir=RESULTS_DIR / "search_cache")

    runner = PerJobPipelineRunner(
        sample_n=args.sample,
        no_bfs=not args.bfs,
        no_cross_platform_lookup=not args.cross_platform_lookup,
        cache=cache,
        search_client_type=search_client_type,
        name_resolution=args.name_resolution,
        name_resolution_min_mentions=args.name_min_mentions,
    )

    # ── Single URL override — skip Search, skip job building ──
    if args.url:
        print(f"Single URL mode: {args.url}")
        print(f"  Platform: {args.platform}")
        result = await runner.run_single_url(
            args.url,
            platform=args.platform,
        )

        # Group by identity for clean CLI output
        from services.influencerMerging.InfluencerMergerService import InfluencerMergerService
        grouped = InfluencerMergerService.merge(result.all_influencers)
        grouped.sort(key=lambda inf: len(inf.source_urls), reverse=True)

        print(f"\nDone — {len(grouped)} influencers found (grouped from {len(result.all_influencers)} raw)")
        for inf in grouped:
            cites = len(inf.source_urls)
            cite_str = f" [{cites} cites]" if cites > 0 else ""
            handles_str = ", ".join(
                f"{p.value}: @{h}" for p, h in inf.handles.items()
            )
            if not handles_str:
                handles_str = inf.name
            print(f"  {handles_str}{cite_str}")
        return

    # ── Normal job mode ──
    categories = load_categories()

    if args.job:
        jobs = build_jobs(categories, job_key=args.job, region_filter=args.region)
        if not jobs:
            print(f"ERROR: No job found for key: {args.job}")
            print("  Format: CATEGORY/Sub/Platform/Region (e.g. FITNESS/Fitness/Instagram/US)")
            sys.exit(1)
    elif args.category:
        jobs = build_jobs(categories, category_filter=args.category, region_filter=args.region)
    else:
        jobs = build_jobs(categories, region_filter=args.region)

    sample_label = f" (sampled: {args.sample} pages/job)" if args.sample else ""
    print(f"Running {len(jobs)} jobs{sample_label}")

    if args.phase:
        # Phase-based pipeline: search all → dedupe URLs → crawl once → merge
        phase_runner = PhasePipelineRunner(
            sample_n=args.sample,
            no_bfs=not args.bfs,
            no_cross_platform_lookup=not args.cross_platform_lookup,
            cache=cache,
            search_client_type=search_client_type,
            name_resolution=args.name_resolution,
            name_resolution_min_mentions=args.name_min_mentions,
        )
        seeds = await phase_runner.run(jobs)

        input_cost = phase_runner.stats.total_input_tokens * INPUT_COST_PER_1M / 1_000_000
        output_cost = phase_runner.stats.total_output_tokens * OUTPUT_COST_PER_1M / 1_000_000
        print("\nPhase pipeline complete")
        print(f"  Total seeds: {len(seeds)}")
        print(f"  Cache: {cache.hits} hits, {cache.misses} misses")
        print(f"  Estimated cost: ${input_cost + output_cost:.4f}")
    else:
        # Per-job pipeline (original)
        results = await runner.run_jobs(jobs)

        input_cost = runner.stats.total_input_tokens * INPUT_COST_PER_1M / 1_000_000
        output_cost = runner.stats.total_output_tokens * OUTPUT_COST_PER_1M / 1_000_000
        print(f"\nPipeline complete — {len(results)} region(s) processed")
        print(f"  Total influencers: {runner.stats.influencers_deduped}")
        print(f"  Estimated cost: ${input_cost + output_cost:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
