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
**46 names** tracked across all pages

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
| 13 | Dirty Harry | 2 | non-reddit | 1 | ❌ |
| 14 | Niche The | 2 | non-reddit | 1 | ❌ |
| 15 | Email Address | 1 | non-reddit | 1 | ❌ |
| 16 | Password Remember | 1 | non-reddit | 1 | ❌ |
| 17 | Lost Your | 1 | non-reddit | 1 | ❌ |
| 18 | Customize Consent | 1 | non-reddit | 1 | ❌ |
| 19 | Reject All | 1 | non-reddit | 1 | ❌ |
| 20 | Save My | 1 | non-reddit | 1 | ❌ |
| 21 | Day Plan | 1 | non-reddit | 1 | ❌ |
| 22 | Former Newcastle | 1 | non-reddit | 1 | ❌ |
| 23 | Achievable Academy | 1 | non-reddit | 1 | ❌ |
| 24 | International Bodybuilding | 1 | non-reddit | 1 | ❌ |
| 25 | The Marine | 1 | non-reddit | 1 | ❌ |
| 26 | Navy Seal | 1 | non-reddit | 1 | ❌ |
| 27 | International Federation | 1 | non-reddit | 1 | ❌ |
| 28 | Scintillate Marbella | 1 | non-reddit | 1 | ❌ |
| 29 | The Glow | 1 | non-reddit | 1 | ❌ |
| 30 | Up Project | 1 | non-reddit | 1 | ❌ |
| 31 | Discover Your | 1 | non-reddit | 1 | ❌ |
| 32 | Study Your | 1 | non-reddit | 1 | ❌ |
| 33 | Know Your | 1 | non-reddit | 1 | ❌ |
| 34 | Target Audience | 1 | non-reddit | 1 | ❌ |
| 35 | Determine Your | 1 | non-reddit | 1 | ❌ |
| 36 | Competitive Edge | 1 | non-reddit | 1 | ❌ |
| 37 | Define Your | 1 | non-reddit | 1 | ❌ |
| 38 | Strategies Long-term | 1 | non-reddit | 1 | ❌ |
| 39 | Monetize Your | 1 | non-reddit | 1 | ❌ |
| 40 | Brand You | 1 | non-reddit | 1 | ❌ |
| 41 | To Wrap | 1 | non-reddit | 1 | ❌ |
| 42 | It Up | 1 | non-reddit | 1 | ❌ |
| 43 | Gymfluencers Lifts | 1 | non-reddit | 1 | ❌ |
| 44 | Neutonic Creatine | 1 | non-reddit | 1 | ❌ |
| 45 | First Last | 1 | non-reddit | 1 | ❌ |
| 46 | Send Message | 1 | non-reddit | 1 | ❌ |

## Token Usage
| Metric | Value |
|--------|-------|
| Total input tokens | ~3,800 |
| Total output tokens | ~500 |
| Model | gemini/gemini-2.5-flash-lite |
| Mode | e2e-test |
