# Pipeline Report — <TIMESTAMP>

## Summary
| Metric | Value |
|--------|-------|
| URLs discovered | 0 |
| Pages crawled | 1 (0 failed, 0 dropped) |
| Pages extracted (LLM) | 1 |
| Influencers found (raw) | 16 |
| Unique (after dedup) | 16 |
| Handle fill rate | 14/16 |
| **Handle retrieval** | **0/0** |
| Estimated LLM cost | $0.0006 |
| Regex yield | 10.0 handles/page |
| **Configs** | **1 succeeded, 0 failed (1 total)** |

## Global Seed DB (Deduped)
**10 unique seeds** across all configs

| # | IG Handle | TK Handle | YT Handle | Category |
|---|-----------|-----------|-----------|----------|
| 1 | — | — | seancaseyfitness111 | Fitness / Fitness |
| 2 | — | — | LucyDavisFit | Fitness / Fitness |
| 3 | — | — | adammaxted2262 | Fitness / Fitness |
| 4 | alex.beattie | alex.beattie | — | Fitness / Fitness |
| 5 | courtneyblackfitness | courtneyblackfitness | — | Fitness / Fitness |
| 6 | esgfitness | — | esgfitness | Fitness / Fitness |
| 7 | thebodycoach | — | TheBodyCoachTV | Fitness / Fitness |
| 8 | — | bblisacross | — | Fitness / Fitness |
| 9 | — | — | mac_griffiths | Fitness / Fitness |
| 10 | — | victorianiamh | — | Fitness / Fitness |

## Canary Validation
| Sub | Canary | Found? |
|-----|--------|--------|
| FITNESS_Fitness_UK | Joe Wicks | YES |
| FITNESS_Fitness_UK | Krissy Cela | MISSING |
| FITNESS_Fitness_UK | Alice Liveing | MISSING |
| **Overall** | **1/3** | **33%** |

## Name Mentions
**20 names** tracked across all pages

| # | Name | Mentions | Source | URLs | Resolved? | Handle |
|---|------|----------|--------|------|-----------|--------|
| 1 | Courtney Black | 8 | llm, non-reddit, regex | 1 | ❌ |
| 2 | Michael Griffiths | 6 | llm, non-reddit, regex | 1 | ❌ |
| 3 | Adam Maxted | 6 | llm, non-reddit, regex | 1 | ❌ |
| 4 | Victoria Niamh | 6 | llm, non-reddit, regex | 1 | ❌ |
| 5 | Sean Casey | 5 | llm, non-reddit | 1 | ❌ |
| 6 | Love Island | 4 | non-reddit | 1 | ❌ |
| 7 | Lucy Davis | 4 | llm, non-reddit | 1 | ❌ |
| 8 | Lisa Cross | 4 | llm, non-reddit, regex | 1 | ❌ |
| 9 | Joe Wicks | 3 | llm, non-reddit | 1 | ❌ |
| 10 | Alex Beattie | 3 | llm, non-reddit, regex | 1 | ❌ |
| 11 | The Body | 2 | non-reddit | 1 | ❌ |
| 12 | Emma Storey-Gordon | 2 | llm, non-reddit | 1 | ❌ |
| 13 | Save My | 1 | non-reddit | 1 | ❌ |
| 14 | Day Plan | 1 | non-reddit | 1 | ❌ |
| 15 | The Marine | 1 | non-reddit | 1 | ❌ |
| 16 | The Glow | 1 | non-reddit | 1 | ❌ |
| 17 | Study Your | 1 | non-reddit | 1 | ❌ |
| 18 | Target Audience | 1 | non-reddit | 1 | ❌ |
| 19 | Determine Your | 1 | non-reddit | 1 | ❌ |
| 20 | To Wrap | 1 | non-reddit | 1 | ❌ |

## Token Usage
| Metric | Value |
|--------|-------|
| Total input tokens | ~3,800 |
| Total output tokens | ~500 |
| Model | gemini/gemini-2.5-flash-lite |
| Mode | e2e-test |
