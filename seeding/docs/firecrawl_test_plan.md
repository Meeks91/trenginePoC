# Firecrawl Agent Test Plan

> Test 3 calls: 1 Easy (baseline) + 2 Hard (stress test) to validate the pipeline.

---

## Test Matrix

| # | Category | Sub | Platform | Region | Difficulty | Purpose |
|---|---|---|---|---|---|---|
| 1 | FITNESS | Fitness (top) | Instagram | US | Easy | **Baseline** — highest-confidence, should return 15-30+ |
| 2 | AI | AI Coding / Dev Tools | YouTube | UK | Hard | **Stress test** — niche, sparse directories, recently strengthened |
| 3 | BUSINESS_AND_FINANCE | Side Hustles / Entrepreneurship | TikTok | US | Hard | **Noise test** — "fake guru" contamination, recently strengthened |

---

## Pass Criteria

| Criterion | Threshold | Fail Action |
|---|---|---|
| Influencer count | ≥ 10 | Increase `maxCredits` or switch to `spark-1-pro` |
| Handle format | All non-empty strings | Fix schema or add validation |
| No hallucinated handles | Spot-check 3 handles per job | Flag sub for source review |
| Credits used | ≤ maxCredits | Working as designed |

---

## Execution

```python
from seeding.seed_architecture_schema import *
import json
from datetime import datetime

categories = load_categories("seeding/categories/all_categories.json")

TESTS = [
    ("FITNESS", "Fitness", Platform.IG, RegionCode.US),
    ("AI", "AI Coding / Dev Tools", Platform.YT, RegionCode.UK),
    ("BUSINESS_AND_FINANCE", "Side Hustles / Entrepreneurship", Platform.TK, RegionCode.US),
]

results = []
for cat_key, sub_name, platform, region_code in TESTS:
    cat = next(c for c in categories if c.category_key == cat_key)
    sub = next(s for s in cat.all_subs if s.sub_name == sub_name)
    job = SeedJob(platform=platform, region=REGIONS[region_code],
                  category_key=cat_key, sub=sub)

    raw = app.agent(**job.agent_config)

    result = SeedJobResult.from_job(
        job=job, raw_result=raw.data,
        credits_used=raw.credits_used,
        timestamp=datetime.now().isoformat(),
    )
    results.append(result)

    with open(f"seeding/results/{cat_key}_{sub_name}_{platform.value}_{region_code.value}.json", "w") as f:
        json.dump(result.to_json(), f, indent=2)

# Generate report
report = SeedJobResult.to_md_report(results)
with open("seeding/results/summary_report.md", "w") as f:
    f.write(report)
```

### Manual Verification

For each job:
1. Pick 3 random handles from results
2. Search on the actual platform
3. Verify they exist and create content in the expected niche

---

## Expected Outcomes

| Test | Count | Confidence | Notes |
|---|---|---|---|
| FITNESS/IG/US | 15-30+ | Very High | Most abundant niche |
| AI Coding/YT/UK | 5-15 | Medium | Sparse niche, recently strengthened to 10 sources |
| Side Hustles/TK/US | 5-15 | Medium | Recently strengthened to 10 sources, but noisy niche |

---

## Post-Test Actions

Summarise results to user.
