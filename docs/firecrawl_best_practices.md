# Firecrawl Agent — Best Practices

> For TrendPuppy's seed crawler. Based on [Firecrawl /agent docs](https://docs.firecrawl.dev/features/agent) and `crawler_comparison.md`.

---

## Pydantic Models

```python
from pydantic import BaseModel, Field

class Influencer(BaseModel):
    name: str = Field(description="Creator display name")
    handle: str = Field(description="Platform handle (e.g. @username)")

class SeedResults(BaseModel):
    influencers: list[Influencer] = Field(description="Discovered influencer list")
```

**Why Pydantic?** Firecrawl converts your Pydantic schema → JSON schema internally. Structured output means no parsing — you get typed objects back.

---

## Agent Parameters

| Param | Type | Purpose |
|---|---|---|
| `prompt` | str | Natural language task. **Be specific:** include platform, region, year |
| `schema` | BaseModel | Pydantic model defining output shape |
| `urls` | list[str] | *Optional.* Seed URLs to start from — maps to our `knownSources` |
| `model` | str | `spark-1-mini` (default, cheaper) or `spark-1-pro` (complex tasks) |
| `maxCredits` | int | Hard cost ceiling per call. Agent stops when reached |

---

## Credit Tiers (Difficulty-Based)

| Difficulty | maxCredits | Reasoning |
|---|---|---|
| Easy (44 subs) | 30 | Abundant sources, mainstream niches. Agent finds results fast |
| Medium (26 subs) | 40 | Fewer dedicated directories, requires more navigation |
| Hard (2 subs) | 50 | Very niche, sparse results. Agent needs to dig deeper |

---

## Model Selection

| Model | Use When | Cost |
|---|---|---|
| `spark-1-mini` | **All subs for now.** Good enough for directory scraping | ~60% cheaper |
| `spark-1-pro` | Complex multi-step navigation, login-walled sites | Full price |

**Current policy:** `spark-1-mini` for everything. Upgrade specific subs to `pro` only if `mini` fails to deliver ≥10 results.

---

## Prompt Engineering Patterns

### ✅ Do

- **Be task-oriented:** "Find the top Instagram influencers" not "Search for influencers"
- **Include all query context in prompt:** platform, region, year, niche language
- **Use `urls` for seeding:** Pass `knownSources` as `urls` — this is the native way to give the agent starting points
- **Let schema handle output format:** Don't describe JSON shape in the prompt

### ❌ Don't

- **Don't say what NOT to do:** "Don't include brands" → Agent ignores negatives. Instead: "Only include individual creators"
- **Don't embed platform/region in sub data:** Parent prompt handles injection per-call
- **Don't over-constrain:** Let the agent explore beyond your seed URLs
- **Don't set maxCredits too low:** Under-crediting causes partial results

---

## Job Matrix Math

```
72 subs × 3 platforms × 2 regions = 432 calls/month

Credit budget (worst case):
  44 Easy × 30  = 1,320 × 6 (platforms × regions) = 7,920
  26 Medium × 40 = 1,040 × 6 = 6,240
   2 Hard × 50   =   100 × 6 = 600
                              -------
                 Total: 14,760 credits/month (worst case)
```

**Actual cost** will be lower — agent rarely uses full maxCredits.

---

## Failure Modes & Mitigations

| Failure | Symptoms | Mitigation |
|---|---|---|
| Source site blocks crawl | 0 results from that source | Agent navigates to other URLs. Add more `knownSources` |
| Agent returns < threshold | Fewer than 10 influencers | Retry with `spark-1-pro` or increase `maxCredits` |
| Hallucinated handles | Handles don't exist on platform | Post-validation step: spot-check 3 handles per job |
| Duplicate influencers | Same person across multiple subs | Deduplicate by handle at aggregation layer |
| Credit exhaustion | Agent stops mid-search | Increase maxCredits for that difficulty tier |

---

## Result Output Structure

Each completed job writes a `SeedJobResult`:

```python
@dataclass
class SeedJobResult:
    # Job spec (what was requested)
    category_key: str
    sub_name: str
    platform: str
    region: str
    difficulty: str
    credits_used: int
    model: str
    prompt: str          # Full prompt sent to agent
    urls_sent: list[str] # knownSources sent as urls param

    # Results
    influencers: list[dict]  # [{name, handle}, ...]
    count: int
    timestamp: str

    # Quality
    meets_threshold: bool    # count >= 10
```

**Output files:**
- `results/{category}_{sub}_{platform}_{region}.json` — one per job
- `results/summary_report.md` — aggregated MD report with all jobs

---

## Recommended Workflow

1. **Test first:** Run 5 representative calls from the test plan
2. **Validate:** Check handles manually for 3 results per test
3. **Tune:** Adjust maxCredits or model for subs that underperform
4. **Batch run:** Execute full 432-call matrix
5. **Report:** Generate MD summary report from JSON results
6. **Deduplicate:** Aggregate across subs, remove duplicate handles
