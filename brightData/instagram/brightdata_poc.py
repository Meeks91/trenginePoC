"""
Bright Data PoC — Direct API call for Instagram Reel discovery.

Bypasses the SDK's InstagramSearchScraper (which doesn't expose a country param)
and calls the Datasets API directly with country in the payload.

Usage:
    source venv/bin/activate
    python brightdata_poc.py search "fitness" --method hashtag --region gb --num 5
"""

import argparse
import os
import sys
import json
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

# ─── Environment ────────────────────────────────────────────────────────────
load_dotenv()

TOKEN = os.getenv("BRIGHTDATA_API_TOKEN")
if not TOKEN:
    print("❌  BRIGHTDATA_API_TOKEN not found in .env")
    sys.exit(1)

# ─── Constants ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# From SDK source: brightdata/scrapers/instagram/scraper.py
DATASET_ID_POSTS = "gd_lk5ns7kz21pck8jpis"

# Bright Data Datasets API v3 endpoints (from SDK source: scrapers/api_client.py)
TRIGGER_URL = "https://api.brightdata.com/datasets/v3/trigger"
STATUS_URL = "https://api.brightdata.com/datasets/v3/progress"
RESULT_URL = "https://api.brightdata.com/datasets/v3/snapshot"

REGIONS = {
    "gb": "United Kingdom",
    "us": "United States",
    "ca": "Canada",
    "au": "Australia",
    "de": "Germany",
    "fr": "France",
    "br": "Brazil",
    "in": "India",
    "mx": "Mexico",
    "ng": "Nigeria",
}


# ─── Direct API Call ────────────────────────────────────────────────────────

async def call_brightdata_api(url, num, post_type, start_date, end_date, country=None):
    """
    Call Bright Data Datasets API directly.
    This bypasses the SDK's Instagram method so we can include country in the payload.
    """
    # Build payload — same structure as SDK, but with country field added
    payload_item = {
        "url": url,
        "num_of_posts": num,
        "post_type": post_type,
        "start_date": start_date,
        "end_date": end_date,
    }
    if country:
        payload_item["country"] = country

    payload = [payload_item]

    # Trigger params — same as SDK's InstagramSearchScraper._execute_discovery
    params = {
        "dataset_id": DATASET_ID_POSTS,
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "url",
    }

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        # Step 1: Trigger the job
        print("  📡  Triggering API request...")
        async with session.post(TRIGGER_URL, json=payload, params=params, headers=headers) as resp:
            if resp.status != 200:
                error = await resp.text()
                return {"success": False, "error": f"Trigger failed (HTTP {resp.status}): {error}", "data": None}
            trigger_data = await resp.json()
            snapshot_id = trigger_data.get("snapshot_id")
            print(f"  📋  Snapshot ID: {snapshot_id}")

        # Step 2: Poll for completion
        print("  ⏳  Waiting for results", end="", flush=True)
        max_wait = 240  # seconds
        poll_interval = 5
        elapsed = 0
        while elapsed < max_wait:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
            print(".", end="", flush=True)

            status_url = f"{STATUS_URL}/{snapshot_id}"
            async with session.get(status_url, headers=headers) as resp:
                if resp.status == 200:
                    status_data = await resp.json()
                    status = status_data.get("status", "unknown")
                    if status == "ready":
                        print(f" ✅ ready ({elapsed}s)")
                        break
                    elif status == "error":
                        print(f" ❌ error ({elapsed}s)")
                        return {"success": False, "error": f"Snapshot error: {status_data}", "data": None}
                else:
                    pass  # keep polling
        else:
            print(f" ⏰ timeout ({max_wait}s)")
            return {"success": False, "error": f"Timed out after {max_wait}s", "data": None}

        # Step 3: Fetch results
        print("  📥  Fetching results...")
        result_url = f"{RESULT_URL}/{snapshot_id}"
        async with session.get(result_url, params={"format": "json"}, headers=headers) as resp:
            if resp.status == 200:
                data = await resp.json()
                return {"success": True, "error": None, "data": data, "snapshot_id": snapshot_id}
            else:
                error = await resp.text()
                return {"success": False, "error": f"Fetch failed (HTTP {resp.status}): {error}", "data": None}


# ─── URL Builder ─────────────────────────────────────────────────────────────

def build_ig_url(query, method):
    clean = query.lstrip("#").strip().lower().replace(" ", "")
    if method == "hashtag":
        return f"https://www.instagram.com/explore/tags/{clean}/"
    else:
        return query


# ─── Report ─────────────────────────────────────────────────────────────────

def save_report(args, result, elapsed):
    slug = args.query.lstrip("#").replace(" ", "_")[:30]
    region = args.region or "global"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{args.method}__{slug}__{region}__{ts}.json"
    filepath = OUTPUT_DIR / filename

    report = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "query": args.query,
            "method": args.method,
            "ig_url": args.ig_url,
            "region": REGIONS.get(args.region) if args.region else None,
            "region_code": args.region,
            "num_requested": args.num,
            "start_date": args.start_date,
            "end_date": args.end_date,
            "elapsed_seconds": round(elapsed, 2),
        },
        "api_response": {
            "success": result["success"],
            "error": result.get("error"),
            "snapshot_id": result.get("snapshot_id"),
            "num_results": len(result["data"]) if result.get("data") else 0,
        },
        "reels": result.get("data", []),
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
    print(f"  Method:      {meta['method']}")
    print(f"  IG URL:      {meta['ig_url']}")
    print(f"  Region:      {meta['region'] or 'Global'}")
    print(f"  Date Range:  {meta['start_date']} → {meta['end_date']}")
    print(f"  Requested:   {meta['num_requested']} reels")
    print()
    print(f"  Success:     {api['success']}")
    print(f"  Results:     {api['num_results']}")
    print(f"  Time:        {meta['elapsed_seconds']}s")
    if api["error"]:
        print(f"  ⚠️  Error:    {api['error']}")
    print()

    if reels:
        print("  📹  REELS:")
        print("  " + "-" * 56)
        for i, reel in enumerate(reels):
            if isinstance(reel, dict):
                print(f"  #{i+1:2d} | @{reel.get('user_posted', '?')}")
                views = reel.get('video_view_count', reel.get('views', '?'))
                likes = reel.get('likes', '?')
                comments = reel.get('num_comments', '?')
                print(f"      | 👁 {views}  ❤️ {likes}  💬 {comments}")
                desc = (reel.get("description", "") or "")[:80]
                if desc:
                    print(f"      | {desc}{'...' if len(reel.get('description', '') or '') > 80 else ''}")
                url = reel.get("url", "")
                if url:
                    print(f"      | 🔗 {url}")
                hashtags = reel.get("hashtags", [])
                if hashtags:
                    print(f"      | 🏷  {' '.join(f'#{t}' for t in hashtags[:5])}")
                print()
    else:
        print("  (No reels returned)")
        print()

    print(f"  💾  Report: {filepath}")
    print("─" * 60)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="brightdata_poc",
        description="Bright Data PoC — Search for trending Instagram Reels",
    )
    sub = parser.add_subparsers(dest="command")

    search_p = sub.add_parser("search", help="Search for trending reels")
    search_p.add_argument("query", help="Hashtag or search term (e.g. 'fitness' or 'skincare')")
    search_p.add_argument("--method", choices=["hashtag", "direct_url"], default="hashtag",
                          help="hashtag = explore/tags URL (default) | direct_url = pass a full IG URL")
    search_p.add_argument("--region", choices=list(REGIONS.keys()), default=None,
                          help="Country code for geo-targeted results (e.g. gb, us)")
    search_p.add_argument("--num", type=int, default=10,
                          help="Number of reels to request (default: 10)")
    search_p.add_argument("--days", type=int, default=30,
                          help="Lookback period in days (default: 30)")
    search_p.add_argument("--dry-run", action="store_true",
                          help="Show config without calling the API")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Compute dates
    args.end_date = datetime.now().strftime("%m-%d-%Y")
    args.start_date = (datetime.now() - timedelta(days=args.days)).strftime("%m-%d-%Y")
    args.ig_url = build_ig_url(args.query, args.method)

    region_name = REGIONS.get(args.region) if args.region else "Global"

    print()
    print(f"  🔍  Query:    {args.query}")
    print(f"  📋  Method:   {args.method}")
    print(f"  🔗  IG URL:   {args.ig_url}")
    print(f"  🌍  Region:   {region_name} ({args.region or 'none'})")
    print(f"  📅  Range:    {args.start_date} → {args.end_date} ({args.days}d)")
    print(f"  🔢  Count:    {args.num}")
    print(f"  💰  Est cost: ~${args.num * 0.002:.3f}")

    if args.dry_run:
        print("\n  ⏸  Dry run — no API call made.")
        sys.exit(0)

    print()

    start_time = time.time()
    result = asyncio.run(
        call_brightdata_api(
            url=args.ig_url,
            num=args.num,
            post_type="reel",
            start_date=args.start_date,
            end_date=args.end_date,
            country=args.region,
        )
    )
    elapsed = time.time() - start_time

    filepath, report = save_report(args, result, elapsed)
    print_report(report, filepath)


if __name__ == "__main__":
    main()
