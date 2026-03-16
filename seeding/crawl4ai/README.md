# Seed Crawler Pipeline v6

> Last updated: 2026-03-16

## What This Does

Discovers and extracts influencer handles across **N platforms × N regions × N subs** to seed TrendPuppy's database. Platforms, regions, and subcategories are all extensible via `seed_schema.py` — add a new region or platform and the pipeline picks it up automatically.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Playwright (auto-installed by Crawl4AI) | latest |
| Gemini API key | `GEMINI_API_KEY` env var |
| Serper API key (optional, for `--search-client strict`) | `SERPER_API_KEY` env var |

> [!NOTE]
> **English only.** Search queries, title-matching, and slug-matching are currently English-only. Multi-language support is not yet implemented.

## Installation

```bash
# 1. Clone the repo and cd into the crawler
cd seeding/crawl4ai

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up Crawl4AI's browser (downloads Chromium via Playwright)
crawl4ai-setup

# 5. Set your Gemini API key (or export in .bashrc/.zshrc)
export GEMINI_API_KEY="your-key-here"

# 6. Verify everything works
crawl4ai-doctor
python3 -m pytest tests/unit -x -q   # Unit tests (fast, no API calls)
```

> **Optional — Local LLM:** Set `USE_OLLAMA=1` to use a local Ollama model (`gemma3:4b`) instead of Gemini. No API key needed.

## Structure


```
seeding/crawl4ai/
│
├── cli.py ·················· CLI entry point
├── pipeline.py ·············· Per-job orchestrator — PerJobPipelineRunner (Search → Crawl → Extract → Enrich)
├── phase_pipeline.py ········ Phase-based orchestrator — PhasePipelineRunner (Search All → Dedupe → Crawl → Merge)
├── config/
│   ├── __init__.py ·········· Re-exports settings
│   ├── settings.py ·········· API keys, paths, rate limits, feature flags
│   ├── schema.py ············ Shared types (Influencer, SubResult, RegionResult, NameMentionRecord)
│   ├── seed_schema.py ······· Seed architecture (SeedJob, Platform, Region, Category)
│   ├── canary_influencers.json  Known influencers for regression detection
│   └── categories/
│       └── all_categories.json  72 subs × known_sources, search_prompts, alt_terms
│
├── services/
│   ├── search/
│   │   ├── SearchClient.py ······ Protocol + RawSearchResult + SearchQuery + QueryType
│   │   ├── OpenSearchClient.py ·· DDG backend (free, no dork operators beyond site:)
│   │   ├── StrictSearchClient.py  Serper/Google backend (paid, full intitle:/OR/site: dorks)
│   │   ├── SearchService.py ····· Client-agnostic filtering: ads, platform URLs, relevance
│   │   └── SearchCache.py ······· Disk-backed DDG result cache (SHA-256 keyed, 24h TTL)
│   ├── crawling/
│   │   ├── CrawlService.py ······ Crawl4AI headless browser, BFS link-following
│   │   └── filters.py ··········· PruningContentFilter factory
│   ├── extraction/
│   │   ├── HandleExtractionService.py  Orchestrates regex → classify → YT → clean → LLM → merge
│   │   ├── RegexHandleExtractor.py ··· 10 regex patterns, ~200-entry ignore list
│   │   ├── PlatformClassifier.py ····· Mechanical 5-step cascade for naked @handles
│   │   ├── HandleClassifier.py ······· LLM fallback for ambiguous naked @handles
│   │   ├── LLMExtractionService.py ··· LLM full-page extraction (Gemini 2.5 Flash Lite)
│   │   ├── NameCleaner.py ············ Shared name cleanup + brand/country/news blocklists
│   │   ├── LLMResponseParser.py ······ LLM JSON → Influencer[] with handle validation
│   │   ├── PageTruncator.py ·········· Fit-markdown token budget truncation
│   │   ├── YouTubeChannelResolver.py · UC... → @handle via HTTP
│   │   ├── NameExtractor.py ·········· Reddit name extraction (regex + blocklists)
│   │   ├── NameMentionTracker.py ····· Cross-page name frequency + sub grouping
│   │   ├── NameResolver.py ··········· DDG name → handle resolution + confidence check
│   │   └── prompts.py ················ LLM prompt template
│   ├── enrichment/
│   │   ├── InfluencerMerger.py ······ Identity merge + SeedInfluencer conversion
│   │   ├── NameToHandleService.py ··· DDG gate: cross-platform + deferred name resolution
│   │   └── patterns.py ·············· Platform URL + @handle text regexes
│   ├── audit/
│   │   └── AuditService.py ·········· JSONL append-only audit log per job
│   ├── reporting/
│   │   ├── PipelineReporter.py ······ Markdown report generator
│   │   ├── StatsCollector.py ········ Centralized PipelineStats accumulator
│   │   └── ResultAssembler.py ······· File I/O: search URLs, output JSON, global seeds
│   └── validation/
│       └── IngestionValidator.py ··· Canary influencer pass-rate validation
│
├── docs/
│   ├── ARCHITECTURE.md ··········· Exhaustive architecture reference
│   └── business_rules.md ········ Comprehensive decision rules reference
│
├── tests/
│   ├── unit/ ················· 40+ suites, ~720 tests (no API calls)
│   ├── integration/ ·········· 15 suites, ~260 tests (mocked DDG/LLM)
│   ├── e2e/ ·················· Live crawl tests
│   └── fixtures/ ············· 61 saved real pages
│
└── results/ ·················· search/, pages/, raw/, audit/, reports/, search_cache/, unresolved_names.json
```

## Pipeline Flow

```
SearchClient (DDG or Serper) → SearchService (ad/platform/relevance filter)
    → Crawl4AI → Regex Extract → NameCleaner → Classify Handles → LLM Fallback
    → Name Tracking → Enrich (DDG backfill) → Deferred Name Resolution
    → Global Merge + Dedup → Output
```

> **📖 For complete business rules**, see **[docs/business_rules.md](docs/business_rules.md)** — covers every decision rule with diagrams, examples, and the full blocklist.
>
> **📐 For architecture details**, see **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — exhaustive system overview, data flow, module responsibilities, and output artifacts.

## Quick Summary of Decision Rules

| Stage | Rule | Cost |
|-------|------|------|
| **Search** | 2 backends: `open` (DDG, free) or `strict` (Serper/Google, paid) | Free / ~$0.005/query |
| **Search** | 3 query types: primary open, alt open, site-targeted | — |
| **Search** | `_is_relevant()` OR filter: mandatory word OR slug OR sub_name OR category_key OR reddit | Free |
| **Search** | DDG dorking: platform URLs → extract handle immediately, skip crawl | Free |
| **Search** | Search cache: SHA-256 keyed disk cache, 24h TTL (DDG only) | Free |
| **Search** | DDG circuit breaker: skip config if ≥50% queries fail; kill after 3 consecutive failures | Free |
| **Crawl** | Crawl4AI + PruningContentFilter → 20-60% token reduction | Free |
| **Regex** | 10 patterns: IG embeds, URL patterns, @mentions | Free |
| **Regex** | ~200-entry ignore list + profanity substring filter (CSS, JS, brands, cities, platforms) | Free |
| **NameCleaner** | Brand/country/news/generic blocklists, markdown strip, URL decode, LinkedIn slug rejection | Free |
| **Classify** | 5-step cascade: page count → window → closest kw → URL → skip | Free |
| **Classify** | LLM fallback: only when 2+ platforms + 0 URL-handles + ambiguous | ~$0.001 |
| **LLM Extract** | Only when 0 handles + listicle URL keyword | ~$0.0003/pg |
| **Enrich** | DDG handle backfill for name-only influencers | Free |
| **Name Resolution** | Reddit names → fuzzy group → top 5/sub → DDG resolve | Free |
| **Merge** | Global identity dedup by normalized handle + cross-platform merge | Free |

## Usage

```bash
# Single job
PYTHONPATH="." python3 cli.py --job FITNESS/Yoga/Instagram/US

# Sample mode (3 pages to LLM)
PYTHONPATH="." python3 cli.py --job FITNESS/Yoga/Instagram/US --sample 3

# Entire category
PYTHONPATH="." python3 cli.py --category FITNESS --sample 5

# All jobs
PYTHONPATH="." python3 cli.py --all --sample 5

# Phase pipeline (search all → dedupe → crawl once)
PYTHONPATH="." python3 cli.py --category FITNESS --phase

# With name resolution
PYTHONPATH="." python3 cli.py --all --name-resolution --name-min-mentions 2

# With Serper search (paid, full Google dork operators)
SERPER_API_KEY=xxx PYTHONPATH="." python3 cli.py --job FITNESS/Fitness/Instagram/US --search-client strict

# Single URL override
PYTHONPATH="." python3 cli.py --url https://example.com/influencers
```

### CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--job` | — | Single job: `CATEGORY/Sub/Platform/Region` |
| `--category` | — | All jobs for a category |
| `--all` | — | All 432 jobs |
| `--url` | — | Single URL override (skips Search) |
| `--sample N` | All | Only N pages per job to LLM |
| `--no-bfs` | Off | Disable BFS link-following |
| `--no-cross-platform-lookup` | Off | Skip DDG for cross-platform handles |
| `--region` | All | Filter by region code (US, UK) |
| `--phase` | Off | Use phase-based pipeline |
| `--name-resolution` | Off | Enable deferred name→handle resolution |
| `--name-min-mentions` | 2 | Min mentions for name resolution |
| `--platform` | Instagram | Platform context for `--url` mode |
| `--search-client` | `open` | `open` (DDG, free) or `strict` (Serper, paid) |

## Configuration (`config/settings.py`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `LLM_PROVIDER` | `gemini/gemini-2.5-flash-lite` | LLM model |
| `SEARCH_BACKEND` | `auto` | Engine rotation (DDG, Brave, Bing, Google, etc.) |
| `MAX_URLS_PER_JOB` | 120 | Hard cap on URLs per job |
| `CRAWL_CONCURRENCY` | 5 | Max browser instances |
| `BFS_MAX_DEPTH` / `BFS_MAX_PAGES` | 1 / 20 | BFS config |
| `PRUNING_THRESHOLD` | 0.48 | Content filter aggressiveness |
| `DDG_FAILURE_THRESHOLD_PCT` | 0.5 | Abort config if ≥50% queries fail |
| `DDG_FAILURE_MIN_QUERIES` | 3 | Don't evaluate threshold until N queries |
| `DDG_KILL_AFTER_N` | 3 | Kill search after N consecutive config failures |
| `NAME_RESOLUTION_ENABLED` | False | Deferred name resolution |
| `NAME_RESOLUTION_MIN_MENTIONS` | 2 | Cross-page mention threshold |
| `NAME_RESOLUTION_MAX_PER_SUB` | 5 | Max names resolved per sub-category |
| `YIELD_WARNING_THRESHOLD` | 2.0 | Min avg handles/page before low-yield warning |

## Cost

| Component | Per page | Per job (~30pg) | Full batch (432 jobs) |
|-----------|---------|----------------|----------------------|
| DDG search (`--search-client open`) | Free | Free | Free |
| Serper search (`--search-client strict`) | ~$0.005/query | ~$0.02 | ~$8.64 |
| Crawl4AI | Free | Free | Free |
| Regex extraction | Free | Free | Free |
| Mechanical classification | Free | Free | Free |
| Gemini 2.5 Flash Lite | ~$0.0003 | ~$0.002 | ~$0.86 |
| Handle backfill (DDG) | Free | Free | Free |
| Name resolution (DDG) | Free | Free | Free |

## DDG Query Budget (Full Batch)

| Phase | Formula | 2 regions (parallel) | 2 regions (single batch) |
|-------|---------|---------------------|------------------------|
| **Search** | numSubs × numPlatforms × numRegions × queriesPerJob | 72 × 3 × 2 × ~7 = **3,024** | Same |
| **Enrichment** | Variable (per name-only influencer) | ~200-500 | Same |
| **Name Resolution** | numSubs × maxPerSub × numRegions | 72 × 5 × 2 = **720** | 72 × 5 = **360** |
| **Total** | | **~3,944-4,244** | **~3,584-3,884** |

> Name resolution multiplies by region when regions run as separate parallel streams (`--region US` + `--region UK`). In a single `--all` batch, names merge across regions → cap is `numSubs × 5 = 360`.

## Development & Testing

### Code Style

Please adhere to the project's Python coding standards. For full details on typing, assertions, and structure, view the `/code-style` workflow file:
`cat ../../.agent/workflows/code-style.md`

### Running Tests

The test suite is divided into layers using pytest markers. Run tests from the `seeding/crawl4ai` directory:

```bash
# 1. Unit tests: Fast, zero external API calls. Mocked DDG and responses.
python3 -m pytest tests/unit

# 2. Integration tests: Tests components wired together, still mocking network.
python3 -m pytest tests/integration

# 3. Network/E2E tests: Hits real DDG and Gemini APIs. (Requires GEMINI_API_KEY)
# These are excluded by default. Use the 'network' marker to run them:
python3 -m pytest -m network

# 4. Slow tests: Tests that take >10s (e.g., live crawling). Excluded by default.
python3 -m pytest -m slow
```

### Git Hooks

The repository includes tracked git hooks in the `.githooks` directory to enforce code quality:
- **`pre-commit`**: Automatically runs the fast test suite (unit tests only) before allowing a commit.
- **`pre-push`**: Automatically runs the **full comprehensive test suite** (including optional network and slow tests) before allowing a push to remote.

To install the hooks locally:
```bash
# From the repository root (TrendPuppy/PoCs/trenginePoc)
git config core.hooksPath .githooks
```
