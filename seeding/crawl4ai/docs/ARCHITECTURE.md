# Crawl4AI Seed Crawler — Architecture

> Exhaustive reference for the crawl4ai CLI seed pipeline.
> Last updated: 2026-03-16

---

## 1. What Is a "Job"?

A **Job** (`SeedJob`) is the smallest unit of work in the pipeline. It represents one
combination of:

```
  Job = SubCategory × Platform × Region

  Example:  Yoga × Instagram × US  =  1 Job
            Yoga × TikTok   × US  =  1 Job  (different platform)
            Yoga × Instagram × UK  =  1 Job  (different region)
```

Each job carries everything needed to search, crawl, and extract:

| Field | Source | Example |
|-------|--------|---------|
| `category_key` | Parent category | `FITNESS` |
| `sub.sub_name` | Sub-category niche | `Yoga` |
| `sub.search_prompt` | Primary DDG query | `best yoga fitness influencers` |
| `sub.alt_search_terms` | Alt DDG queries | `["yoga content creators", "yoga bloggers"]` |
| `sub.known_sources` | Site-targeted DDG domains | `["modash.io", "heepsy.com"]` |
| `platform` | Target social platform | `Instagram` |
| `region.code` | Target geography | `US` |
| `region.search_label` | Label for DDG queries | `United States` |

**Scale:** The full category file has 12 categories × ~6 subs × 3 platforms × 2 regions ≈ **432 jobs**.

Jobs are generated from `all_categories.json` by `seed_schema.generate_seed_jobs()`.

---

## 2. System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              cli.py — Entry Point                              │
│  argparse: --job / --category / --all / --url / --phase / --sample / --bfs     │
│            --search-client open|strict / --name-resolution                     │
└────────────┬──────────────────────┬───────────────────────┬─────────────────────┘
             │ (default)            │ --phase               │ --url
             ▼                      ▼                       │
┌─────────────────────┐  ┌──────────────────────────┐       │
│   pipeline.py       │  │  phase_pipeline.py       │       │
│   PerJobPipelineRunner│  │  PhasePipelineRunner     │◄──────┘
│   (per-job S→C→E→E) │  │  (4 global phases)      │
└─────────┬───────────┘  └────────────┬─────────────┘
          │                           │
          └──────────┬────────────────┘
                     │ Both extend BasePipelineRunner:
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│  base_pipeline.py — BasePipelineRunner (Template Method)                       │
│                                                                                │
│  Shared: __init__, stats, _run_deferred_name_resolution,                       │
│          _run_canary_validation, report, save                                  │
│                                                                                │
│  Template: run(jobs)                                                           │
│    1. _search_and_extract_influencers(jobs) → GatherResult  ◄─ ABSTRACT        │
│    2. Deferred name resolution                                                 │
│    3. Global dedup (InfluencerMerger.to_seeds)                                 │
│    4. Canary validation (IngestionValidator)                                   │
│    5. Report (PipelineReporter)                                                │
│    6. Save seeds (ResultAssembler)                                             │
└────────────────────────────────┬────────────────────────────────────────────────┘
                                 │ Composes these services:
                     ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            services/                                           │
│                                                                                │
│  ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐   │
│  │    search/       │  │   crawling/       │  │       extraction/            │   │
│  │                  │  │                   │  │                              │   │
│  │  SearchClient    │  │  CrawlService     │  │  HandleExtractionService     │   │
│  │  (Protocol)      │  │  filters          │  │    ├── RegexHandleExtractor  │   │
│  │  OpenSearchCli.  │  │                   │  │    ├── PlatformClassifier    │   │
│  │  StrictSearchCli.│  │                   │  │    ├── HandleClassifier      │   │
│  │  SearchService   │  │                   │  │    ├── LLMExtractionService  │   │
│  │  SearchCache     │  │                   │  │    ├── YouTubeChannelRes.    │   │
│  ┌─────────────────┐  ┌──────────────────┐  │    ├── NameCleaner           │   │
│  │  enrichment/     │  │    audit/         │  │    ├── NameExtractor         │   │
│  │                  │  │                   │  │    ├── NameMentionTracker   │   │
│  │  InfluencerMerger│  │  AuditService     │  │    ├── NameResolver         │   │
│  │  NameToHandleSvc │  │  (JSONL logging)  │  │    ├── LLMResponseParser    │   │
│  │  patterns        │  │                   │  │    └── prompts              │   │
│  └─────────────────┘  └──────────────────┘  └──────────────────────────────┘   │
│                                                                                │
│  ┌─────────────────┐  ┌──────────────────┐                                     │
│  │   reporting/     │  │   validation/     │                                    │
│  │                  │  │                   │                                    │
│  │  PipelineReporter│  │  InfluencerValid. │                                    │
│  │  StatsCollector  │  │  (canary checks)  │                                    │
│  │  ResultAssembler │  │                   │                                    │
│  └─────────────────┘  └──────────────────┘                                     │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Per-Job Pipeline (`PerJobPipelineRunner`, default)

This is the step-by-step flow for `pipeline.py`. Each job runs all steps independently,
then after ALL jobs finish, deferred resolution + global dedup runs.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ FOR EACH JOB (e.g. "FITNESS/Yoga × Instagram × US"):                            │
│                                                                                  │
│  STEP 1: SEARCH                                                                  │
│  ┌──────────────────────────────────────────────────────────┐                     │
│  │ SearchClient protocol wraps the backend.             │                     │
│  │ Default: OpenSearchClient (free DDG).                 │                     │
│  │ --search-client strict: StrictSearchClient (Serper).   │                     │
│  │                                                        │                     │
│  │ Both clients generate 3 query types per job:           │                     │
│  │   • primary: "{sub} {search_prompt} {platform}         │                     │
│  │               influencers list {year}"                 │                     │
│  │   • alt:     "{sub} {alt_term} {platform} influencers  │                     │
│  │               {region} {year}"                         │                     │
│  │   • site:    "site:{source} {search_prompt} {platform} │                     │
│  │               {year}"                                  │                     │
│  │                                                        │                     │
│  │ StrictSearchClient adds Google dork operators:         │                     │
│  │   (intitle:influencer OR intitle:creator OR intitle:top │                     │
│  │    OR site:reddit.com) + (slug1 OR slug2) + terms      │                     │
│  │                                                        │                     │
│  │ SearchService filters results (client-agnostic):       │                     │
│  │   1. Remove ad/tracking URLs                           │                     │
│  │   2. DDG dorking: extract handles from platform URLs   │                     │
│  │   3. _is_relevant() OR filter:                         │                     │
│  │      mandatory word in title OR slug in URL path       │                     │
│  │      OR sub_name in title OR category in title         │                     │
│  │      OR domain is reddit.com                           │                     │
│  │                                                        │                     │
│  │ OUTPUT → list of (url, query) pairs to crawl           │                     │
│  │        → list of direct handles (no crawl needed)      │                     │
│  └────────────────────────────────────────────────────────┘                     │
│                                                                                  │
│  STEP 2: CRAWL                                                                   │
│  ┌──────────────────────────────────────────────────────────┐                     │
│  │ CrawlService opens a headless browser (Crawl4AI).        │                     │
│  │ Fetches each URL concurrently (max 5 at once).           │                     │
│  │ PruningContentFilter strips navs, footers, noise.        │                     │
│  │                                                          │                     │
│  │ Optional BFS: if a crawled page links to same-domain     │                     │
│  │ listicle pages, those are crawled too (depth-limited).   │                     │
│  │                                                          │                     │
│  │ OUTPUT → raw_markdown (full page text)                   │                     │
│  │        → fit_markdown  (pruned, 60-80% smaller)          │                     │
│  └──────────────────────────────────────────────────────────┘                     │
│                                                                                  │
│  STEP 3: EXTRACT HANDLES                                                         │
│  ┌──────────────────────────────────────────────────────────┐                     │
│  │ HandleExtractionService orchestrates per-page:           │                     │
│  │                                                          │                     │
│  │   a) RegexHandleExtractor (10 patterns)                  │                     │
│  │      → URL-tagged handles (known platform)               │                     │
│  │      → naked @handles (unknown platform)                 │                     │
│  │      → YT channel IDs (need HTTP resolution)             │                     │
│  │                                                          │                     │
│  │   b) PlatformClassifier: assigns platform to naked       │                     │
│  │      handles mechanically (5-step cascade)               │                     │
│  │                                                          │                     │
│  │   c) HandleClassifier LLM: only if still-ambiguous       │                     │
│  │      handles exist AND page has zero URL-tagged handles   │                     │
│  │                                                          │                     │
│  │   d) YouTubeChannelResolver: converts /channel/UC...     │                     │
│  │      IDs to @handles via HTTP                            │                     │
│  │                                                          │                     │
│  │   e) NameExtractor: pulls 2-3 word proper names from     │                     │
│  │      page text, feeds into NameMentionTracker             │                     │
│  │                                                          │                     │
│  │   f) LLMExtractionService: only fires if page has       │                     │
│  │      ZERO handles (URL + naked) AND URL looks like a     │                     │
│  │      listicle. Sends fit_markdown to Gemini.             │                     │
│  │                                                          │                     │
│  │   g) All handles merged into Influencer list per page    │                     │
│  │                                                          │                     │
│  │ OUTPUT → all_merged: Influencer[] (per job)              │                     │
│  │        → name_tracker: names seen across pages           │                     │
│  └──────────────────────────────────────────────────────────┘                     │
│                                                                                  │
│  STEP 4: PER-JOB ENRICHMENT (cross-platform DDG)                                 │
│  ┌──────────────────────────────────────────────────────────┐                     │
│  │ NameToHandleService.resolve_cross_account_handles()      │                     │
│  │                                                          │                     │
│  │ If an influencer has a TikTok handle but the job         │                     │
│  │ targets Instagram: DDG "{name}" instagram.com            │                     │
│  │                                                          │                     │
│  │ Rules:                                                   │                     │
│  │   • Only influencers with ≥2 source page citations       │                     │
│  │   • Max 5 DDG lookups per job (budget cap)               │                     │
│  │   • Sorted by citation count (most-cited first)          │                     │
│  │   • Name-only influencers are SKIPPED here (deferred)    │                     │
│  │                                                          │                     │
│  │ New handles are added as NEW Influencer entries.          │                     │
│  │                                                          │                     │
│  │ OUTPUT → enriched Influencer[] for this job              │                     │
│  └──────────────────────────────────────────────────────────┘                     │
│                                                                                  │
│  STEP 5: ACCUMULATE                                                         │
│  ┌──────────────────────────────────────────────────────────┐                     │
│  │ All (Influencer, category) pairs accumulated globally.   │                     │
│  │ Per-job name tracker merged into global name tracker.    │                     │
│  └──────────────────────────────────────────────────────────┘                     │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘

  After ALL jobs complete:

┌──────────────────────────────────────────────────────────────────────────────────┐
│ STEP 6: DEFERRED NAME RESOLUTION                                                 │
│ ┌──────────────────────────────────────────────────────────┐                      │
│ │ NameToHandleService.resolve_handles_for_top_mentioned_   │                      │
│ │ names() uses the global NameMentionTracker.              │                      │
│ │                                                          │                      │
│ │ Names from Reddit pages that were mentioned ≥2 times     │                      │
│ │ across multiple pages get DDG-resolved to handles.       │                      │
│ │                                                          │                      │
│ │ Newly-resolved influencers are APPENDED to the global    │                      │
│ │ accumulator (tagged with category "NAME_RESOLUTION").    │                      │
│ └──────────────────────────────────────────────────────────┘                      │
│                                                                                  │
│ STEP 7: GLOBAL MERGE + DEDUP (InfluencerMerger.to_seeds)                         │
│ ┌──────────────────────────────────────────────────────────┐                      │
│ │ InfluencerMerger.to_seeds() runs on the FULL list:      │                      │
│ │                                                          │                      │
│ │   ALL per-job influencers                                │                      │
│ │     + newly-resolved name influencers from Step 6        │                      │
│ │     = one combined list                                  │                      │
│ │                                                          │                      │
│ │ Deduplicates by (handle, platform). Merges cross-        │                      │
│ │ platform handles. Picks best name. Flattens to           │                      │
│ │ SeedInfluencer records with ig/tk/yt handle columns.     │                      │
│ │                                                          │                      │
│ │ OUTPUT → global_seeds.json (DB-ready)                    │                      │
│ └──────────────────────────────────────────────────────────┘                      │
│                                                                                  │
│ STEP 8: CANARY VALIDATION (global, cross-platform)                               │
│ ┌──────────────────────────────────────────────────────────┐                      │
│ │ IngestionValidator.validate() runs ONCE per unique       │                      │
│ │ (category, sub, region) against ALL accumulated seeds.   │                      │
│ │ Cross-platform: Matt Wolfe (YT-only) found via global.   │                      │
│ └──────────────────────────────────────────────────────────┘                      │
│                                                                                  │
│ STEP 9: REPORT                                                                   │
│ ┌──────────────────────────────────────────────────────────┐                      │
│ │ PipelineReporter generates pipeline_report.md            │                      │
│ │ ResultAssembler saves pipeline_output.json + seeds       │                      │
│ └──────────────────────────────────────────────────────────┘                      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### Key insight: The merger runs AFTER name resolution

```
  Per-Job Influencers ─────┐
    (from Steps 1-5)       │
                           ├──► InfluencerMerger.to_seeds() ──► global_seeds.json
  Name-Resolved Infs ──────┘
    (from Step 6)
```

So newly-found handles from deferred name resolution are included in the final
merged output. They're not siloed — they go into the same dedup pool.

---

## 4. Phase Pipeline (`PhasePipelineRunner`, `--phase`)

An alternative orchestration that avoids redundant crawls.

```
 PHASE 1: SEARCH ALL JOBS
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Run DDG queries for EVERY job. Collect all URLs into a global bag. │
 │  Each URL is tagged with which job(s) discovered it.                │
 │  Direct handles extracted via DDG Dorking.                          │
 │                                                                     │
 │  Example: Job A finds modash.io/yoga-influencers                    │
 │           Job B also finds modash.io/yoga-influencers               │
 │           → URL stored ONCE, tagged with both job A and B           │
 └──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
 PHASE 2: DEDUPE URLs
 ┌──────────────────────────────────────────────────────────────────────┐
 │  URL bag already deduped (keyed by URL string).                     │
 │  Sort by how many jobs discovered each URL (most popular first).    │
 │  This means the most broadly-relevant pages get crawled first.      │
 └──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
 PHASE 3: CRAWL ONCE
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Each unique URL is crawled EXACTLY ONCE.                           │
 │  No duplicate crawls — even if 5 jobs found the same URL.           │
 │  Saves time, bandwidth, and avoids rate limits.                     │
 └──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
 PHASE 4: EXTRACT + MERGE
 ┌──────────────────────────────────────────────────────────────────────┐
 │  HandleExtractionService runs on all crawled pages.                 │
 │  NameToHandleService cross-platform enrichment.                     │
 │  Influencers tagged with ALL categories from the jobs that found    │
 │  their source page.                                                 │
 │  Deferred name resolution.                                          │
 │  InfluencerMerger.to_seeds() → global_seeds.json                   │
 └──────────────────────────────────────────────────────────────────────┘
```

### When to use which?

| Feature | Per-Job (default) | Phase (`--phase`) |
|---------|-------------------|-------------------|
| Search | Per job | All jobs at once |
| Crawl | Per job (may crawl same URL twice) | Each URL crawled once |
| Best for | Debugging, single job runs | Full-matrix runs (saves crawl time) |

---

## 5. Data Flow

```
 ┌──────────────────────┐
 │ all_categories.json  │─────── 12 categories × ~6 subs
 └──────────┬───────────┘            × 3 platforms × 2 regions
            │                        = ~432 SeedJobs
            ▼
   ┌────────────────┐
   │ DDG Search     │
   │ (3 query types │
   │  per job)      │
   └──┬──────────┬──┘
      │          │
      │          ▼ If result URL is on a social platform:
      │    ┌─────────────────────┐
      │    │ DDG Dorking:        │
      │    │ Extract handle from │─────────────────────────────┐
      │    │ URL, skip crawling  │                             │
      │    └─────────────────────┘                             │
      │                                                        │
      ▼ Non-platform URLs queued for crawling:                 │
   ┌────────────────┐                                          │
   │ Crawl4AI       │                                          │
   │ (headless      │                                          │
   │  browser)      │                                          │
   └──┬──────────┬──┘                                          │
      │          │                                             │
      ▼          ▼                                             │
 raw_markdown  fit_markdown                                    │
      │         (pruned)                                       │
      │          │                                             │
      │          │ (only zero-handle listicle pages)            │
      │          ▼                                             │
      │    ┌────────────────┐                                  │
      │    │ ExtractionSvc  │                                  │
      │    │ (Gemini LLM)   │─────────────────┐                │
      │    └────────────────┘                 │                │
      │                                       │                │
      ▼                                       │                │
 ┌─────────────────────┐                      │                │
 │ RegexHandleExtract  │                      │                │
 │ (10 regex patterns) │                      │                │
 └──┬──────────┬───────┘                      │                │
    │          │                              │                │
    ▼          ▼                              │                │
 URL-tagged  Naked @handles                   │                │
 handles     → NameCleaner                    │                │
 (known      → PlatformClassifier             │                │
  platform)  → HandleClassifier (LLM)         │                │
    │             │                           │                │
    │             │                           │                │
    │     YT channel IDs                      │                │
    │     → YouTubeChannelResolver            │                │
    │          │                              │                │
    ▼          ▼                              ▼                ▼
 ┌───────────────────────────────────────────────────────────────┐
 │            InfluencerMerger.merge() — per-job identity dedup  │
 └────────────────────────────┬──────────────────────────────────┘
                              │
                              ▼
 ┌───────────────────────────────────────────────────────────────┐
 │  NameToHandleService — cross-platform DDG enrichment          │
 │  "Has TikTok, needs Instagram" → DDG "{name}" instagram.com  │
 │  (max 5 per job, only ≥2-cited influencers)                   │
 └────────────────────────────┬──────────────────────────────────┘
                              │
              accumulate (Influencer, category) into global pool
                              │
                    ┌─────────┴──── after ALL jobs ──────────────┐
                    │                                            │
                    ▼                                            │
 ┌──────────────────────────────────┐                            │
 │ Deferred Name Resolution         │                            │
 │                                  │                            │
 │ NameMentionTracker aggregated    │                            │
 │ across ALL pages from ALL jobs.  │                            │
 │ Names from Reddit with ≥2 cross- │                            │
 │ page mentions get DDG-resolved.  │                            │
 │                                  │                            │
 │ Resolved handles APPENDED to     │──── new Influencers ───────┤
 │ the global pool.                 │                            │
 └──────────────────────────────────┘                            │
                                                                 │
                                                                 ▼
                              ┌──────────────────────────────────────────┐
                              │ InfluencerMerger.to_seeds()              │
                              │                                          │
                              │ Runs on EVERYTHING:                      │
                              │   • All per-job influencers              │
                              │   • All name-resolved influencers        │
                              │                                          │
                              │ Dedup by (handle, platform).             │
                              │ Merge cross-platform handles.            │
                              │ Pick best name. Flatten to DB columns.   │
                              │                                          │
                              │ → global_seeds.json                      │
                              └──────────────────────────────────────────┘
```

---

## 6. Directory Layout

```
crawl4ai/
├── cli.py                          # argparse entry point
├── base_pipeline.py                # BasePipelineRunner — shared template (name res, canary, report, save)
├── pipeline.py                     # Per-job orchestrator (PerJobPipelineRunner extends base)
├── phase_pipeline.py               # Phase-based orchestrator (PhasePipelineRunner extends base)
│
├── config/
│   ├── __init__.py                 # Re-exports settings constants
│   ├── settings.py                 # All constants: API keys, paths, rate limits, thresholds
│   ├── schema.py                   # Domain models: Influencer, PageResult, SeedInfluencer, ...
│   ├── seed_schema.py              # Job models: SeedJob, Category, SubCategory, Region, ...
│   ├── canary_influencers.json     # Expected influencers for validation
│   └── categories/
│       └── all_categories.json     # 12 categories × ~6 subs = 72 niches
│
├── services/
│   ├── search/
│   │   ├── SearchClient.py         # Protocol + RawSearchResult + SearchQuery + QueryType
│   │   ├── OpenSearchClient.py     # DDG backend (free, no dork ops beyond site:)
│   │   ├── StrictSearchClient.py   # Serper/Google backend (paid, full intitle:/OR/site: dorks)
│   │   ├── SearchService.py        # Client-agnostic: ads, platform URLs, _is_relevant()
│   │   └── SearchCache.py          # Disk-backed DDG result cache (SHA-256 keyed, 24h TTL)
│   │
│   ├── crawling/
│   │   ├── CrawlService.py         # Crawl4AI headless browser, BFS link-following
│   │   └── filters.py              # PruningContentFilter setup
│   │
│   ├── extraction/
│   │   ├── HandleExtractionService.py  # Orchestrator: regex → clean → classify → YT → LLM → merge
│   │   ├── RegexHandleExtractor.py     # 10 regex patterns, ~200-entry ignore list, heading names
│   │   ├── PlatformClassifier.py       # Mechanical 5-step cascade for naked @handles
│   │   ├── HandleClassifier.py         # LLM fallback for ambiguous naked @handles
│   │   ├── LLMExtractionService.py     # LLM full-page extraction via litellm → Gemini
│   │   ├── NameCleaner.py              # Shared name cleanup: brand/country/news/generic blocklists
│   │   ├── YouTubeChannelResolver.py   # /channel/UC... → @handle via HTTP
│   │   ├── NameExtractor.py            # Proper-name regex with blocklists
│   │   ├── NameMentionTracker.py       # Cross-page fuzzy name aggregation (≥90% similarity)
│   │   ├── NameResolver.py             # DDG name → handle resolution + confidence check
│   │   ├── LLMResponseParser.py        # LLM JSON → Influencer[] with handle validation
│   │   └── prompts.py                  # LLM prompt template
│   │
│   ├── enrichment/
│   │   ├── InfluencerMerger.py         # Identity merge + SeedInfluencer conversion
│   │   ├── NameToHandleService.py      # DDG gate: cross-platform + deferred name resolution
│   │   └── patterns.py                 # Platform URL + @handle text regexes
│   │
│   ├── audit/
│   │   └── AuditService.py             # JSONL append-only audit log per job
│   │
│   ├── reporting/
│   │   ├── PipelineReporter.py         # Markdown report generator
│   │   ├── StatsCollector.py           # Centralized PipelineStats accumulator
│   │   └── ResultAssembler.py          # File I/O: search URLs, output JSON, global seeds
│   │
│   └── validation/
│       └── IngestionValidator.py       # Canary influencer pass-rate validation
│
├── tests/                          # unit / integration / e2e + fixtures
│
├── results/                        # Runtime output (gitignored)
│   ├── search/                     # Saved DDG URLs per job
│   ├── pages/                      # Crawled fit_markdown files
│   ├── raw/                        # Raw LLM JSON responses
│   ├── audit/                      # JSONL audit trails
│   ├── reports/                    # Pipeline summary reports
│   ├── search_cache/               # Disk-backed DDG cache
│   ├── pipeline_output.json        # Nested per-job output
│   ├── unresolved_names.json       # Names discovered but not resolved to handles
│   └── global_seeds.json           # DB-ready deduped influencer list
│
└── docs/
    ├── ARCHITECTURE.md             # This file
    └── business_rules.md           # Business rules & logic reference
```

---

## 7. Module Responsibilities

### CLI & Orchestration

| Module | Responsibility |
|--------|---------------|
| `cli.py` | argparse entry point. Loads `all_categories.json`, generates `SeedJob[]`, routes to PerJobPipelineRunner or PhasePipelineRunner. |
| `base_pipeline.py` | `BasePipelineRunner` — Template Method base class. Shared init, stats, search loop with DDG circuit breaker, deferred name resolution, canary validation, report generation, seed saving. Both runners extend this. |
| `pipeline.py` | `PerJobPipelineRunner(BasePipelineRunner)`. Overrides `_search_and_extract_influencers()` with per-job loop: Crawl→Extract→Enrich per job (search is shared). |
| `phase_pipeline.py` | `PhasePipelineRunner(BasePipelineRunner)`. Overrides `_search_and_extract_influencers()` with global phases: Dedupe URLs → Crawl Once → Extract+Merge (search is shared). |

### Config

| Module | Responsibility |
|--------|---------------|
| `settings.py` | All constants: API keys, model name, paths, rate limits, retry params, cost constants, thresholds. |
| `schema.py` | Domain models: `Platform`, `Influencer`, `PageResult`, `SeedInfluencer`, `PipelineStats`, etc. |
| `seed_schema.py` | Job models: `SeedJob`, `Category`, `SubCategory`, `Region`, `LLMInfluencer`. Job generation from JSON. |

### Services

| Module | What it does |
|--------|-------------|
| `SearchClient` | Protocol defining the `search(SeedJob) → RawSearchResult[]` interface. Shared types: `SearchQuery`, `RawSearchResult`, `QueryType`. |
| `OpenSearchClient` | DDG backend. Builds 3 query types (primary, alt, site). No dork operators beyond `site:`. Free, broad results. |
| `StrictSearchClient` | Serper/Google backend. Full dork operators: `intitle:`, `site:`, `OR`, `()`. Precise, paid. |
| `SearchService` | **Client-agnostic search orchestrator.** Receives a `SearchClient`, runs queries, filters: ads, platform URL dorking, `_is_relevant()` OR filter. |
| `SearchCache` | Disk-backed DDG cache. SHA-256 hash key → JSON file. 24h TTL. |
| `CrawlService` | Crawl4AI headless browser. Concurrent crawling. BFS link-following for same-domain listicle links. |
| `HandleExtractionService` | **Extraction orchestrator.** Regex → NameCleaner → Classify → YT resolve → Names → LLM gate → Merge. |
| `RegexHandleExtractor` | 10 compiled patterns. ~200-entry ignore list. Heading-based name assignment to handles. |
| `PlatformClassifier` | 5-step mechanical cascade: page platforms → window → closest keyword → URL domain → unclassified. |
| `HandleClassifier` | LLM fallback for ambiguous naked handles (2+ platforms, zero URL handles). |
| `LLMExtractionService` | Full-page LLM extraction (Gemini via litellm). Pydantic structured output. |
| `YouTubeChannelResolver` | `/channel/UC...` → `@handle` via HTTP. Checks redirects, canonical link, JS data. |
| `NameExtractor` | Proper-name regex (2-3 capitalized words). Sentence-starter filter, word + name blocklists. |
| `NameMentionTracker` | Cross-page fuzzy name aggregation (difflib ≥ 90%). Tracks canonical, variants, counts, sources. |
| `NameResolver` | DDG name → handle. Confidence check (name word in result title). 4 zero-result retries. |
| `ResponseParser` | LLM JSON → Influencer[]. Handles 3 response shapes. Validates handles via NameCleaner. |
| `NameCleaner` | Shared name cleanup injected into LLMResponseParser + NameExtractor. Brand/country/news/generic blocklists, markdown strip, URL-decode, LinkedIn slug rejection. |
| `InfluencerMerger` | `merge()`: identity grouping by normalized handle/name. `to_seeds()`: flattens to DB-ready SeedInfluencer. |
| `NameToHandleService` | **THE single DDG gate.** Mode 1: per-job cross-platform enrichment. Mode 2: post-all-jobs name resolution. |
| `AuditService` | JSONL logging of every pipeline decision. |
| `PipelineReporter` | Markdown report with summary, breakdown, roster, seeds, canaries, name mentions, token usage. |
| `StatsCollector` | Centralized `PipelineStats` accumulator. |
| `ResultAssembler` | File I/O: saves search URLs, pipeline output, global seeds. |
| `IngestionValidator` | Canary validation: checks results against expected creators per category/sub/region. |

---

## 8. Key Concepts

### Extraction Priority (cheapest first)

```
 Cost $0     │ 1. IG Embed ("A post shared by Name (@handle)")
             │ 2. URL-based regex (instagram.com/X, tiktok.com/@X)
             │ 3. @mention in plain text → PlatformClassifier
             │ 4. Heading-based name assignment
 ────────────┤
 Cost ~$0.001│ 5. HandleClassifier LLM (ambiguous @handles only)
 Cost ~$0.003│ 6. LLMExtractionService (zero-handle listicles only)
```

### NameToHandleService: Two Modes

```
 MODE 1 — Per-Job Cross-Platform (runs during each job)
 ┌──────────────────────────────────────────────────────┐
 │ "This influencer has TikTok but we need Instagram"   │
 │ DDG: "{name}" instagram.com                          │
 │ Only if: has ≥1 handle, needs target platform,       │
 │          cited on ≥2 pages, max 5 lookups/job        │
 │ Name-only influencers SKIPPED (go to Mode 2)         │
 └──────────────────────────────────────────────────────┘

 MODE 2 — Deferred Name Resolution (runs once, after ALL jobs)
 ┌──────────────────────────────────────────────────────┐
 │ "This name appeared on 4 Reddit pages with no handle"│
 │ DDG: "{name} {category} Instagram TikTok YouTube"    │
 │ Only if: Reddit-sourced, ≥2 mentions, top 5 per sub  │
 │ Results appended to global pool BEFORE final merge    │
 └──────────────────────────────────────────────────────┘
```

### Identity Merge

Handles normalized by stripping `@`, `_`, `.`, and common affixes (`the`, `real`, `official`, `iam`, etc.). Two entries with the same normalized handle → same person.

### Dependency Injection

Services take `AuditLog` + optional config. Pipeline runners compose services — no global state, fully testable.

---

## 9. Output Artifacts

| File | Format | Contents |
|------|--------|----------|
| `results/global_seeds.json` | JSON | DB-ready `SeedInfluencer[]` — **the primary output** |
| `results/unresolved_names.json` | JSON | Names discovered but not resolved to handles |
| `results/pipeline_output.json` | JSON | Nested `RegionResult[]` with per-page detail |
| `results/search/{job_key}_urls.json` | JSON | DDG-discovered URLs per job |
| `results/pages/{domain}_{path}.md` | Markdown | Pruned fit_markdown per page |
| `results/audit/{ts}_{job_key}.jsonl` | JSONL | Full decision trail per job |
| `results/reports/pipeline_report_{ts}.md` | Markdown | Human-readable run summary |
| `results/search_cache/{hash}.json` | JSON | DDG cache (24h TTL) |

---

## 10. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ |
| CLI | argparse |
| Async | asyncio |
| Web Crawling | Crawl4AI (`AsyncWebCrawler`, `PruningContentFilter`) |
| Search (free) | `ddgs` (DuckDuckGo, multi-engine rotation), wrapped by `OpenSearchClient` |
| Search (paid) | Serper API (Google), wrapped by `StrictSearchClient` |
| LLM | `litellm` → Gemini 2.5 Flash Lite (Pydantic structured output) |
| HTTP | `httpx` (YouTube channel resolution) |
| Schema | dataclasses (domain), Pydantic (LLM binding) |
| Testing | pytest (unit / integration / e2e) |
| Type Checking | mypy |
