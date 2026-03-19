# Pipeline Report — <TIMESTAMP>

## Summary
| Metric | Value |
|--------|-------|
| URLs discovered | 0 |
| Pages crawled | 1 (0 failed, 0 dropped) |
| Pages extracted (LLM) | 1 |
| Influencers found (raw) | 20 |
| Unique (after dedup) | 20 |
| Handle fill rate | 14/20 |
| **Handle retrieval** | **0/0** |
| Estimated LLM cost | $0.0006 |
| Regex yield | 16.0 handles/page |
| **Configs** | **1 succeeded, 0 failed (1 total)** |

## Global Seed DB (Deduped)
**10 unique seeds** across all configs

| # | IG Handle | TK Handle | YT Handle | Categories |
|---|-----------|-----------|-----------|------------|
| 1 | — | — | adammaxted2262 | FITNESS |
| 2 | alex.beattie | alex.beattie | — | FITNESS |
| 3 | courtneyblackfitness | courtneyblackfitness | — | FITNESS |
| 4 | esgfitness | — | esgfitness | FITNESS |
| 5 | thebodycoach | — | TheBodyCoachTV | FITNESS |
| 6 | — | bblisacross | — | FITNESS |
| 7 | — | — | LucyDavisFit | FITNESS |
| 8 | — | — | mac_griffiths | FITNESS |
| 9 | — | — | seancaseyfitness111 | FITNESS |
| 10 | — | victorianiamh | — | FITNESS |

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
| 1 | Courtney Black | 9 | llm, non-reddit, regex | 1 | ❌ |
| 2 | Michael Griffiths | 7 | llm, non-reddit, regex | 1 | ❌ |
| 3 | Adam Maxted | 7 | llm, non-reddit, regex | 1 | ❌ |
| 4 | Victoria Niamh | 6 | llm, non-reddit, regex | 1 | ❌ |
| 5 | Sean Casey | 6 | llm, non-reddit, regex | 1 | ❌ |
| 6 | Lucy Davis | 5 | llm, non-reddit, regex | 1 | ❌ |
| 7 | Love Island | 4 | non-reddit | 1 | ❌ |
| 8 | Joe Wicks | 4 | llm, non-reddit, regex | 1 | ❌ |
| 9 | Lisa Cross | 4 | llm, non-reddit, regex | 1 | ❌ |
| 10 | Alex Beattie | 3 | llm, non-reddit, regex | 1 | ❌ |
| 11 | Emma Storey-Gordon | 3 | llm, non-reddit, regex | 1 | ❌ |
| 12 | The Body | 2 | non-reddit | 1 | ❌ |
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
