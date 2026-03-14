"""
Apify PoC — Instagram Reel Discovery
=====================================
CLI tool using Apify's Instagram Hashtag Scraper to find trending reels
by hashtag or keyword, with regional proxy targeting.

Actor: apify/instagram-hashtag-scraper
Docs:  https://apify.com/apify/instagram-hashtag-scraper

Usage:
    python apify_poc.py hashtag "fitness" --region uk --num 10
    python apify_poc.py keyword "london fitness trends" --region uk --num 5
    python apify_poc.py hashtag "skincare" --region us --num 10 --dry-run
"""

import argparse
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from apify_client import ApifyClient

# ─── Environment ────────────────────────────────────────────────────────────
load_dotenv()

TOKEN = os.getenv("APIFY_API_TOKEN")
if not TOKEN:
    print("❌  APIFY_API_TOKEN not found in .env")
    sys.exit(1)

# ─── Constants ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

ACTOR_ID = "apify/instagram-hashtag-scraper"

# ISO 3166-1 alpha-2 codes for proxy geo-targeting
REGIONS = {
    "uk": {"code": "GB", "name": "United Kingdom"},
    "us": {"code": "US", "name": "United States"},
    "fr": {"code": "FR", "name": "France"},
    "mx": {"code": "MX", "name": "Mexico"},
    "es": {"code": "ES", "name": "Spain"},
    "co": {"code": "CO", "name": "Colombia"},
    "br": {"code": "BR", "name": "Brazil"},
}


# ─── Run Actor ──────────────────────────────────────────────────────────────

def run_actor(query, mode, num, region_code=None):
    """
    Call the Apify Instagram Hashtag Scraper actor.

    Args:
        query: hashtag(s) or keyword string
        mode: 'hashtag' or 'keyword'
        num: max results to return
        region_code: ISO alpha-2 country code for proxy (e.g. 'GB')

    Returns:
        dict with success, data, error, run_id, cost info
    """
    client = ApifyClient(TOKEN)

    # Build actor input
    run_input = {
        "resultsType": "reels",
        "resultsLimit": num,
    }

    if mode == "hashtag":
        # Can be comma-separated or single
        hashtags = [h.strip().lstrip("#") for h in query.split(",")]
        run_input["hashtags"] = hashtags
    else:
        # Keyword/freeword mode — actor still requires hashtags field,
        # but searchKeyword broadens the search beyond exact hashtag match.
        # Extract words from query to use as hashtags too.
        words = [w.strip().lstrip("#") for w in query.split() if len(w.strip()) > 2]
        run_input["hashtags"] = words
        run_input["searchKeyword"] = query

    # Proxy configuration with country targeting
    if region_code:
        run_input["proxy"] = {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
            "apifyProxyCountry": region_code,
        }

    print(f"  📡  Running actor: {ACTOR_ID}")
    print(f"  📦  Input: {json.dumps(run_input, indent=2)}")
    print(f"  ⏳  Waiting for results", end="", flush=True)

    start_time = time.time()

    try:
        run = client.actor(ACTOR_ID).call(run_input=run_input)
    except Exception as e:
        elapsed = time.time() - start_time
        print(f" ❌ ({elapsed:.1f}s)")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "run_id": None,
            "elapsed": elapsed,
        }

    elapsed = time.time() - start_time
    print(f" ✅ ({elapsed:.1f}s)")

    # Fetch results from the run's default dataset
    dataset_id = run.get("defaultDatasetId")
    run_id = run.get("id")

    if not dataset_id:
        return {
            "success": False,
            "error": "No dataset ID returned",
            "data": [],
            "run_id": run_id,
            "elapsed": elapsed,
        }

    items = client.dataset(dataset_id).list_items().items
    print(f"  📥  Got {len(items)} results")

    return {
        "success": True,
        "error": None,
        "data": items,
        "run_id": run_id,
        "dataset_id": dataset_id,
        "elapsed": elapsed,
    }


# ─── Report ─────────────────────────────────────────────────────────────────

def save_report(args, result):
    slug = args.query.lstrip("#").replace(" ", "_").replace(",", "_")[:30]
    region = args.region or "global"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{args.command}__{slug}__{region}__{ts}.json"
    filepath = OUTPUT_DIR / filename

    report = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "query": args.query,
            "mode": args.command,
            "region": REGIONS[args.region]["name"] if args.region else None,
            "region_code": REGIONS[args.region]["code"] if args.region else None,
            "num_requested": args.num,
            "elapsed_seconds": round(result["elapsed"], 2),
        },
        "api_response": {
            "success": result["success"],
            "error": result.get("error"),
            "run_id": result.get("run_id"),
            "dataset_id": result.get("dataset_id"),
            "num_results": len(result["data"]),
        },
        "reels": result["data"],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    return filepath, report


def print_report(report, filepath):
    meta = report["meta"]
    api = report["api_response"]
    reels = report.get("reels", [])

    print()
    print("─" * 60)
    print("  📊  SEARCH REPORT")
    print("─" * 60)
    print(f"  Query:       {meta['query']}")
    print(f"  Mode:        {meta['mode']}")
    print(f"  Region:      {meta['region'] or 'Global (no proxy)'}")
    print(f"  Requested:   {meta['num_requested']} reels")
    print()
    print(f"  Success:     {api['success']}")
    print(f"  Results:     {api['num_results']}")
    print(f"  Time:        {meta['elapsed_seconds']}s")
    if api.get("run_id"):
        print(f"  Run ID:      {api['run_id']}")
    if api["error"]:
        print(f"  ⚠️  Error:    {api['error']}")
    print()

    if reels:
        print("  📹  REELS:")
        print("  " + "-" * 56)
        for i, reel in enumerate(reels[:20]):  # show max 20 in console
            if not isinstance(reel, dict):
                continue
            username = reel.get("ownerUsername", reel.get("user_posted", "?"))
            print(f"  #{i+1:2d} | @{username}")

            views = reel.get("videoPlayCount", reel.get("igPlayCount", "?"))
            likes = reel.get("likesCount", reel.get("likes", "?"))
            comments = reel.get("commentsCount", reel.get("num_comments", "?"))
            reshares = reel.get("reshareCount", "")
            stats = f"👁 {views}  ❤️ {likes}  💬 {comments}"
            if reshares:
                stats += f"  🔄 {reshares}"
            print(f"      | {stats}")

            caption = (reel.get("caption", "") or "")[:80]
            if caption:
                full_caption = reel.get("caption", "") or ""
                print(f"      | {caption}{'...' if len(full_caption) > 80 else ''}")

            url = reel.get("url", "")
            if url:
                print(f"      | 🔗 {url}")

            hashtags = reel.get("hashtags", [])
            if hashtags:
                print(f"      | 🏷  {' '.join(f'#{t}' for t in hashtags[:5])}")

            duration = reel.get("videoDuration")
            if duration:
                print(f"      | ⏱  {duration:.1f}s")

            print()

        if len(reels) > 20:
            print(f"  ... and {len(reels) - 20} more (see full report)")
            print()
    else:
        print("  (No reels returned)")
        print()

    print(f"  💾  Report: {filepath}")
    print("─" * 60)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="apify_poc",
        description="Apify PoC — Search Instagram Reels by hashtag or keyword",
    )
    sub = parser.add_subparsers(dest="command")

    # Hashtag subcommand
    ht = sub.add_parser("hashtag", help="Search by hashtag (e.g. 'fitness' or 'fitness,gym')")
    ht.add_argument("query", help="Hashtag(s), comma-separated (# optional)")
    ht.add_argument("--region", choices=list(REGIONS.keys()), default=None,
                     help="Proxy country for geo-targeted results")
    ht.add_argument("--num", type=int, default=10,
                     help="Number of reels to request (default: 10)")
    ht.add_argument("--dry-run", action="store_true",
                     help="Show config without calling the API")

    # Keyword subcommand
    kw = sub.add_parser("keyword", help="Search by freeword keyword")
    kw.add_argument("query", help="Keyword/phrase (e.g. 'london fitness trends')")
    kw.add_argument("--region", choices=list(REGIONS.keys()), default=None,
                     help="Proxy country for geo-targeted results")
    kw.add_argument("--num", type=int, default=10,
                     help="Number of reels to request (default: 10)")
    kw.add_argument("--dry-run", action="store_true",
                     help="Show config without calling the API")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    region_info = REGIONS.get(args.region) if args.region else None
    region_name = region_info["name"] if region_info else "Global (no proxy)"
    region_code = region_info["code"] if region_info else None
    cost_est = args.num * 0.0026  # $2.60/1K on free plan

    print()
    print(f"  🔍  Query:    {args.query}")
    print(f"  📋  Mode:     {args.command}")
    print(f"  🌍  Region:   {region_name}")
    print(f"  🔢  Count:    {args.num}")
    print(f"  💰  Est cost: ~${cost_est:.3f}")

    if args.dry_run:
        print("\n  ⏸  Dry run — no API call made.")
        sys.exit(0)

    print()

    result = run_actor(
        query=args.query,
        mode=args.command,
        num=args.num,
        region_code=region_code,
    )

    filepath, report = save_report(args, result)
    print_report(report, filepath)


if __name__ == "__main__":
    main()
