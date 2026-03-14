"""
Firecrawl Seed Test Runner
===========================
Runs the 3-call test plan: 1 Easy + 2 Hard
Writes per-job JSON and a summary MD report.

Usage:
  cd seeding/
  source .venv/bin/activate
  python run_test.py
"""

import json
import os
import sys
from datetime import datetime
from firecrawl import FirecrawlApp

# Add parent dir to path so we can import schema
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seed_architecture_schema import (
    Category, SeedJob, SeedJobResult, SeedResults,
    Platform, RegionCode, REGIONS,
    load_categories,
)

# ── Config ──
API_KEY = os.getenv("FIRECRAWL_API_KEY", "fc-a3cdbaeb9bd1452ca5679bb7d047b1c0")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories", "all_categories.json")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

# Test matrix: 1 Easy only (validation run)
TESTS = [
    ("FITNESS", "Fitness", Platform.IG, RegionCode.US),
]

# Override max credits for budget-safe validation (normally set by difficulty tier)
MAX_CREDITS_OVERRIDE = 20


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("=" * 60)
    print("Firecrawl Seed Test Runner")
    print("=" * 60)

    # Init Firecrawl
    app = FirecrawlApp(api_key=API_KEY)
    print(f"✅ Firecrawl client initialized")

    # Load categories
    categories = load_categories(CATEGORIES_PATH)
    print(f"✅ Loaded {len(categories)} categories")

    results: list[SeedJobResult] = []

    for i, (cat_key, sub_name, platform, region_code) in enumerate(TESTS, 1):
        print(f"\n{'─' * 60}")
        print(f"Test {i}/3: {cat_key}/{sub_name} ({platform.value} × {region_code.value})")
        print(f"{'─' * 60}")

        # Find category and sub
        cat = next(c for c in categories if c.category_key == cat_key)
        sub = next(s for s in cat.all_subs if s.sub_name == sub_name)

        # Build job
        job = SeedJob(
            platform=platform,
            region=REGIONS[region_code],
            category_key=cat_key,
            sub=sub,
        )

        print(f"  Difficulty: {sub.difficulty.value} → {sub.difficulty.max_credits} credits")
        print(f"  Model: {sub.difficulty.model}")
        print(f"  URLs: {len(sub.known_sources)} sources")
        print(f"  Prompt (first 150 chars):")
        print(f"    {job.prompt[:150]}...")
        print(f"\n  ⏳ Calling Firecrawl agent...")

        safe_name = f"{cat_key}_{sub_name}_{platform.value}_{region_code.value}".replace(" ", "_").replace("/", "_")

        try:
            config = job.agent_config
            raw = app.agent(
                prompt=config["prompt"],
                urls=config["urls"],
                schema=SeedResults,
                model=config["model"],
                max_credits=MAX_CREDITS_OVERRIDE or config["maxCredits"],
            )

            # ── ALWAYS dump raw response first (never lose data) ──
            raw_dump = {
                "success": raw.success,
                "id": raw.id,
                "status": raw.status,
                "data": raw.data,
                "error": raw.error,
                "model": raw.model,
                "credits_used": raw.credits_used,
                "expires_at": str(raw.expires_at) if raw.expires_at else None,
            }
            raw_path = os.path.join(RESULTS_DIR, f"{safe_name}_raw.json")
            with open(raw_path, "w") as f:
                json.dump(raw_dump, f, indent=2, ensure_ascii=False, default=str)
            print(f"  📋 Raw response saved to {raw_path}")
            print(f"  Status: {raw.status} | Credits: {raw.credits_used} | Error: {raw.error}")

            # ── Check for agent failure ──
            if raw.status == "failed" or raw.error:
                print(f"  ⚠️  Agent failed: {raw.error}")
                seed_results = SeedResults(influencers=[])
            elif raw.data is None:
                print(f"  ⚠️  No data returned (agent may have hit credit limit)")
                seed_results = SeedResults(influencers=[])
            elif isinstance(raw.data, dict):
                # Data is a dict — parse into SeedResults
                if "influencers" in raw.data:
                    seed_results = SeedResults(**raw.data)
                else:
                    print(f"  ⚠️  Data dict has unexpected keys: {list(raw.data.keys())}")
                    seed_results = SeedResults(influencers=[])
            elif isinstance(raw.data, list):
                # Sometimes agent returns a list directly
                seed_results = SeedResults(influencers=[
                    {"name": item.get("name", ""), "handle": item.get("handle", "")}
                    for item in raw.data if isinstance(item, dict)
                ])
            elif isinstance(raw.data, SeedResults):
                seed_results = raw.data
            else:
                print(f"  ⚠️  Unexpected data type: {type(raw.data)}")
                seed_results = SeedResults(influencers=[])

            credits_used = raw.credits_used or 0

            result = SeedJobResult.from_job(
                job=job,
                raw_result=seed_results,
                credits_used=credits_used,
                timestamp=datetime.now().isoformat(),
            )

            print(f"  ✅ Found {result.count} influencers (credits: {result.credits_used})")
            print(f"  Threshold: {'✅ PASS' if result.meets_threshold else '❌ FAIL'} ({result.count}/10)")

            if result.influencers:
                print(f"  First 5:")
                for inf in result.influencers[:5]:
                    print(f"    - {inf['name']} ({inf['handle']})")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            traceback.print_exc()
            result = SeedJobResult(
                category_key=cat_key,
                sub_name=sub_name,
                platform=platform.value,
                region=region_code.value,
                difficulty=sub.difficulty.value,
                model=sub.difficulty.model,
                credits_used=0,
                prompt=job.prompt,
                urls_sent=sub.known_sources,
                influencers=[],
                count=0,
                timestamp=datetime.now().isoformat(),
                meets_threshold=False,
            )

        results.append(result)


        json_path = os.path.join(RESULTS_DIR, f"{safe_name}.json")
        with open(json_path, "w") as f:
            json.dump(result.to_json(), f, indent=2, ensure_ascii=False)
        print(f"  📄 Wrote {json_path}")

    # Generate summary report
    print(f"\n{'=' * 60}")
    print("Summary")
    print(f"{'=' * 60}")

    report = SeedJobResult.to_md_report(results)
    report_path = os.path.join(RESULTS_DIR, "summary_report.md")
    with open(report_path, "w") as f:
        f.write(report)
    print(f"📄 Wrote {report_path}")

    # Print summary
    passed = sum(1 for r in results if r.meets_threshold)
    total_influencers = sum(r.count for r in results)
    total_credits = sum(r.credits_used for r in results)

    print(f"\n  Tests: {passed}/{len(results)} passed threshold")
    print(f"  Influencers found: {total_influencers}")
    print(f"  Credits used: {total_credits}")

    for r in results:
        icon = "✅" if r.meets_threshold else "❌"
        print(f"  {icon} {r.category_key}/{r.sub_name} ({r.platform} × {r.region}): {r.count} influencers, {r.credits_used} credits")

    print(f"\nDone! Review results at: {RESULTS_DIR}/")


if __name__ == "__main__":
    main()
