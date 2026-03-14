"""
SociaVault PoC — Instagram Reel Discovery
==========================================
CLI tool using SociaVault's API to find trending reels
by hashtag, with audio trend data.

API: https://api.sociavault.com/v1/instagram/hashtag/reels
Docs: https://sociavault.com/blog/bypass-instagram-graph-api-reels

Usage:
    python sociavault_poc.py hashtag "fitness" --num 10
    python sociavault_poc.py hashtag "londongym" --num 5
    python sociavault_poc.py hashtag "fitness" --num 5 --dry-run
    python sociavault_poc.py profile "nike" --num 10
"""

import argparse
import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# ─── Environment ────────────────────────────────────────────────────────────
load_dotenv()

API_KEY = os.getenv("SOCIAVAULT_API_KEY")
if not API_KEY:
    print("❌  SOCIAVAULT_API_KEY not found in .env")
    sys.exit(1)

# ─── Constants ──────────────────────────────────────────────────────────────
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

BASE_URL = "https://api.sociavault.com/v1/instagram"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


# ─── API Calls ──────────────────────────────────────────────────────────────

def fetch_hashtag_reels(hashtag, limit):
    """Fetch reels for a given hashtag via SociaVault API."""
    url = f"{BASE_URL}/hashtag/reels"
    params = {"hashtag": hashtag.lstrip("#"), "limit": limit}

    print(f"  📡  GET {url}")
    print(f"  📦  Params: {json.dumps(params)}")
    print(f"  ⏳  Waiting for results", end="", flush=True)

    start = time.time()
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        elapsed = time.time() - start
        print(f" ✅ ({elapsed:.1f}s) — HTTP {resp.status_code}")

        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}: {resp.text[:500]}",
                "data": [],
                "elapsed": elapsed,
                "status_code": resp.status_code,
            }

        body = resp.json()
        reels = body.get("data", body if isinstance(body, list) else [])
        print(f"  📥  Got {len(reels)} results")

        return {
            "success": True,
            "error": None,
            "data": reels,
            "elapsed": elapsed,
            "status_code": resp.status_code,
            "raw_keys": list(body.keys()) if isinstance(body, dict) else "list",
        }

    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        print(f" ❌ ({elapsed:.1f}s)")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "elapsed": elapsed,
            "status_code": None,
        }


def fetch_profile_posts(username, limit):
    """Fetch posts/reels from a profile via SociaVault API."""
    url = f"{BASE_URL}/profile/posts"
    params = {"username": username.lstrip("@"), "limit": limit}

    print(f"  📡  GET {url}")
    print(f"  📦  Params: {json.dumps(params)}")
    print(f"  ⏳  Waiting for results", end="", flush=True)

    start = time.time()
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        elapsed = time.time() - start
        print(f" ✅ ({elapsed:.1f}s) — HTTP {resp.status_code}")

        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP {resp.status_code}: {resp.text[:500]}",
                "data": [],
                "elapsed": elapsed,
                "status_code": resp.status_code,
            }

        body = resp.json()
        posts = body.get("data", body if isinstance(body, list) else [])
        print(f"  📥  Got {len(posts)} results")

        return {
            "success": True,
            "error": None,
            "data": posts,
            "elapsed": elapsed,
            "status_code": resp.status_code,
            "raw_keys": list(body.keys()) if isinstance(body, dict) else "list",
        }

    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        print(f" ❌ ({elapsed:.1f}s)")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "elapsed": elapsed,
            "status_code": None,
        }


# ─── Report ─────────────────────────────────────────────────────────────────

def save_report(args, result):
    query = args.query.lstrip("#@").replace(" ", "_")[:30]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{args.command}__{query}__{ts}.json"
    filepath = OUTPUT_DIR / filename

    report = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "query": args.query,
            "mode": args.command,
            "num_requested": args.num,
            "elapsed_seconds": round(result["elapsed"], 2),
        },
        "api_response": {
            "success": result["success"],
            "error": result.get("error"),
            "status_code": result.get("status_code"),
            "num_results": len(result["data"]),
            "raw_keys": result.get("raw_keys"),
        },
        "results": result["data"],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    return filepath, report


def print_report(report, filepath):
    meta = report["meta"]
    api = report["api_response"]
    results = report.get("results", [])

    print()
    print("─" * 60)
    print("  📊  SEARCH REPORT")
    print("─" * 60)
    print(f"  Query:       {meta['query']}")
    print(f"  Mode:        {meta['mode']}")
    print(f"  Requested:   {meta['num_requested']}")
    print()
    print(f"  Success:     {api['success']}")
    print(f"  HTTP:        {api['status_code']}")
    print(f"  Results:     {api['num_results']}")
    print(f"  Time:        {meta['elapsed_seconds']}s")
    if api.get("raw_keys"):
        print(f"  API keys:    {api['raw_keys']}")
    if api["error"]:
        print(f"  ⚠️  Error:    {api['error']}")
    print()

    if results:
        print("  📹  RESULTS:")
        print("  " + "-" * 56)
        for i, item in enumerate(results[:20]):
            if not isinstance(item, dict):
                print(f"  #{i+1:2d} | (raw item: {str(item)[:100]})")
                continue

            # Try various field name patterns
            owner = item.get("owner", {})
            username = (
                owner.get("username")
                or item.get("ownerUsername")
                or item.get("user", {}).get("username", "?")
                if isinstance(owner, dict) else str(owner)
            )
            print(f"  #{i+1:2d} | @{username}")

            views = item.get("play_count", item.get("videoPlayCount", "?"))
            likes = item.get("like_count", item.get("likesCount", "?"))
            comments = item.get("comment_count", item.get("commentsCount", "?"))
            stats = f"👁 {views}  ❤️ {likes}  💬 {comments}"
            print(f"      | {stats}")

            # Audio info (SociaVault includes this!)
            audio = item.get("audio", item.get("musicInfo"))
            if audio and isinstance(audio, dict):
                title = audio.get("title", audio.get("song_name", ""))
                artist = audio.get("artist", audio.get("artist_name", ""))
                trending = audio.get("is_trending")
                audio_str = f"🎵 {title} — {artist}"
                if trending is not None:
                    audio_str += f" {'🔥 TRENDING' if trending else ''}"
                print(f"      | {audio_str}")

            caption = (item.get("caption", "") or "")[:80]
            if caption:
                full = item.get("caption", "") or ""
                print(f"      | {caption}{'...' if len(full) > 80 else ''}")

            shortcode = item.get("shortcode", item.get("shortCode", ""))
            url = item.get("url", "")
            if shortcode and not url:
                url = f"https://instagram.com/reel/{shortcode}"
            if url:
                print(f"      | 🔗 {url}")

            post_type = item.get("type", item.get("media_type", ""))
            if post_type:
                print(f"      | 📎 {post_type}")

            print()

        if len(results) > 20:
            print(f"  ... and {len(results) - 20} more (see full report)")
            print()
    else:
        print("  (No results returned)")
        print()

    print(f"  💾  Report: {filepath}")
    print("─" * 60)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        prog="sociavault_poc",
        description="SociaVault PoC — Instagram Reel Discovery via API",
    )
    sub = parser.add_subparsers(dest="command")

    # Hashtag subcommand
    ht = sub.add_parser("hashtag", help="Search reels by hashtag")
    ht.add_argument("query", help="Hashtag (# optional)")
    ht.add_argument("--num", type=int, default=10, help="Number of results (default: 10)")
    ht.add_argument("--dry-run", action="store_true", help="Show config only")

    # Profile subcommand
    pf = sub.add_parser("profile", help="Get posts/reels from a profile")
    pf.add_argument("query", help="Username (@ optional)")
    pf.add_argument("--num", type=int, default=10, help="Number of results (default: 10)")
    pf.add_argument("--dry-run", action="store_true", help="Show config only")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    print()
    print(f"  🔍  Query:    {args.query}")
    print(f"  📋  Mode:     {args.command}")
    print(f"  🔢  Count:    {args.num}")

    if args.dry_run:
        print("\n  ⏸  Dry run — no API call made.")
        sys.exit(0)

    print()

    if args.command == "hashtag":
        result = fetch_hashtag_reels(args.query, args.num)
    elif args.command == "profile":
        result = fetch_profile_posts(args.query, args.num)
    else:
        print("Unknown command")
        sys.exit(1)

    filepath, report = save_report(args, result)
    print_report(report, filepath)


if __name__ == "__main__":
    main()
