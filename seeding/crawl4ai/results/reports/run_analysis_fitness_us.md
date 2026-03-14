# Run Analysis — FITNESS / US (9/18 Jobs)

## Run Stats
| Metric | Value |
|--------|-------|
| Jobs completed | 9/18 (crashed at `Powerlifting / Strength` — **fixed**) |
| DDG queries fired | 138 |
| DDG queries with results | 92 (67%) |
| DDG queries with 0 results | 46 (33%) |
| DDG retries (rate limiting) | 145 |
| Pages crawled | 404 |
| Pages failed | 2 (0.5%) |
| LLM extraction | 0 (API key invalid) |
| Total handles found | ~4,178 (2,835 IG + 1,157 TK + 186 YT) |

## Canary Handles
| Name | Found | Mentions |
|------|-------|----------|
| Jeff Nippard | ✅ | 51 pages, `@jeffnippard` |
| Mike Israetel | ✅ | 8 pages, `@renaissanceperiodization` |
| Kayla Itsines | ✅ | 11 cites, `@kayla_itsines` |
| Simeon Panda | ✅ | 7 cites, `@simeonpanda` |
| CBum | ✅ | 5 cites, `@cbum` |

## Reddit via DDG
**9/15 (60%) success rate.**

| Subreddit | IG | YT | TK | Notes |
|-----------|----|----|-----|-------|
| r/Fitness | ✅ 2 | ✅ 5 | ❌ 0 | TikTok not discussed there |
| r/bodyweightfitness | ✅ 5 | ✅ 5 | ✅ 5 | Works well — active fitness sub |
| r/Calisthenic | ❌ 0 | ❌ 0 | ❌ 0 | **Dead sub** — only 3K members |
| r/weightroom | ✅ 5 | ✅ 5 | ✅ 5 | Works well |
| r/Fitness (science) | ❌ 0 | ✅ 5 | ❌ 0 | Too generic for niche queries |

**Why Reddit fails for DDG:**
1. **Small subs** — `r/Calisthenic` has ~3K members vs `r/bodyweightfitness` at ~3M. DDG can't find content on tiny subs.
2. **TikTok queries on Reddit** — Reddit fitness communities skew YouTube/IG. TikTok discussion is rare on traditional fitness subs.
3. **`2026` in query** — Reddit posts don't usually include the current year in titles. DDG site-search matches against page text, so year filtering hurts Reddit results.

**Recommendation:** Drop `2026` from Reddit site: queries. Consider `r/bodyweightfitness` over `r/Calisthenic` (already in knownSources, the small one is dead weight).

## Name Resolution
**Not tested** — `--name-resolution` was OFF (default). Only 1 `direct_handle` event recorded in the entire run.

To test: run with `--name-resolution`:
```bash
python cli.py --category FITNESS --region US --name-resolution
```

## URL Discovery by Platform
| Job | IG URLs | YT URLs | TK URLs |
|-----|---------|---------|---------|
| Fitness | 114 | 115 | 35 |
| Calisthenics | 20 | 19 | 20 |
| Science-Based | 21 | 40 | 22 |

**TikTok is 3x thinner** for the `Fitness` top-level sub (35 vs 114 IG). TikTok influencer listicles are less common on the open web.

## Bugs Found & Fixed
| Bug | Status |
|-----|--------|
| `Powerlifting / Strength` slash in filename → crash | ✅ Fixed in `pipeline.py` (source), `AuditService.py`, `ResultAssembler.py` |
| Gemini API key invalid → all LLM extraction fails | ⚠️ Not fixed (user issue) |

## Architectural Insights
1. **DDG rate limiting is the #1 bottleneck** — 145 retries at 2-8s each = ~15 min wasted
2. **33% of site: queries return nothing** — mostly TikTok queries and small Reddit subs
3. **Crawl success rate is near-perfect (99.5%)** — crawl4ai is solid
4. **Regex extraction alone pulls 4K+ handles** — LLM fallback is nice-to-have, not critical
5. **Runtime for all US:** ~48h at current rate, ~12h with SearchCache on re-runs
