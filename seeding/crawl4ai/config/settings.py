"""
Pipeline Configuration
======================
Constants, API keys, paths, and rate limits for the seed crawler pipeline.

TERMINOLOGY
-----------
  Job = 1 subcategory × 1 platform × 1 region.
        A subcategory is one of ~6 niches within a category
        (e.g. FITNESS → Yoga, Calisthenics, Powerlifting, etc.)
        Example job: "FITNESS/Yoga/Instagram/US"
        A full run across 12 categories × ~6 subcats × 3 platforms × 2 regions ≈ 432 jobs.
        Each job runs all 4 pipeline phases (Search → Crawl → Extract → Enrich).
"""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


# ── Paths ──
# PIPELINE_ROOT = seeding/ (parent of crawl4ai/)
# All output is written under results/, shared across crawl methods.
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PIPELINE_ROOT / "results"       # Root for all pipeline output
SEARCH_DIR = RESULTS_DIR / "search"           # Saved DDG search result URLs per job
PAGES_DIR = RESULTS_DIR / "pages"             # Crawled page markdown (fit_markdown)
RAW_DIR = RESULTS_DIR / "raw"                 # Raw LLM JSON responses, saved for debugging
AUDIT_DIR = RESULTS_DIR / "audit"             # JSONL audit trail per job
REPORTS_DIR = RESULTS_DIR / "reports"          # Generated pipeline summary reports

# ── API Keys ──
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

# ── LLM Config ──
# Model name in litellm format: "provider/model-name"
LLM_PROVIDER = "gemini/gemini-2.5-flash-lite"
# Set USE_OLLAMA=1 to use a local Ollama model instead (free, no API key)
USE_OLLAMA = os.getenv("USE_OLLAMA", "").lower() in ("1", "true", "yes")
if USE_OLLAMA:
    LLM_PROVIDER = "ollama/gemma3:4b"

# ── Rate Limits & Throughput ──
# Search
SEARCH_DELAY_SECONDS = 2         # Pause between search queries to avoid rate limits
MAX_SEARCH_RESULTS = 5           # Max results per individual query string

# Engine rotation — "auto" tries all backends in random order
# (DuckDuckGo, Brave, Bing, Google, Mojeek, Yandex, Yahoo, Wikipedia, Grokipedia).
# Can also be a single engine: "duckduckgo", "brave", "bing", "google", etc.
# Or a comma-delimited subset: "duckduckgo,brave,bing"
SEARCH_BACKEND = "auto"

# Region code for search queries (e.g. "us-en", "uk-en", "de-de")
SEARCH_REGION = "us-en"
MAX_URLS_PER_JOB = 120           # Hard cap on total unique URLs discovered per job
                                 # (1 job = 1 subcat × 1 platform × 1 region)
                                 # Raised from 40 → 120 because regex extraction is
                                 # free — more URLs = more handles at zero LLM cost.
                                 # The pipeline generates ~9 queries per job, each
                                 # returning up to MAX_SEARCH_RESULTS URLs.

# Crawl
CRAWL_CONCURRENCY = 5            # Max concurrent browser instances for crawl4ai
CRAWL_MAX_RETRIES = 3            # Max retries per page (crawl4ai RateLimiter)
BFS_MAX_DEPTH = 1                # Max link-following depth (0=no BFS, 1=follow one level)
BFS_MAX_PAGES = 20               # Max extra pages to crawl per BFS pass

# Extract
LLM_DELAY_SECONDS = 0 if USE_OLLAMA else 2  # Pause between LLM calls (API rate limit)

# Enrich
ENRICH_DELAY_SECONDS = 1         # Pause between DDG handle-backfill queries

# Retry / Backoff (applies to DDG search + enrich, and LLM calls)
MAX_RETRIES = 3                  # Max retry attempts before giving up on a request
BACKOFF_BASE_SECONDS = 2         # Base delay for exponential backoff (2, 4, 8, ...)
BACKOFF_MAX_SECONDS = 30         # Cap on backoff delay to avoid extremely long waits

# DDG Failure Handling — circuit breaker for search
# Per-config: if this fraction of queries fail permanently, skip crawl/extract.
DDG_FAILURE_THRESHOLD_PCT = 0.5  # Abort config if ≥50% of queries fail
DDG_FAILURE_MIN_QUERIES = 3      # Don't evaluate threshold until N queries attempted
# Global kill switch: stop all search after N consecutive config failures.
DDG_KILL_AFTER_N = 3             # Kill search after 3 configs fail in a row

# ── Cost Estimation ──
# Gemini 2.5 Flash Lite pricing (USD per 1M tokens)
# Update these when switching models!
INPUT_COST_PER_1M = 0.10         # $0.10 per 1M input tokens
OUTPUT_COST_PER_1M = 0.40        # $0.40 per 1M output tokens
# Fallback estimate when the API doesn't return actual token counts
OUTPUT_TOKENS_PER_INFLUENCER = 50  # ~50 tokens per influencer JSON object

# ── Content Filtering ──
# Tags stripped before markdown generation, reducing noise for the LLM
EXCLUDED_TAGS = ["nav", "footer", "header", "aside"]
# PruningContentFilter threshold: higher = more aggressive pruning
PRUNING_THRESHOLD = 0.48
# Minimum word count for a text block to survive pruning
WORD_COUNT_THRESHOLD = 10

# ── Name Resolution ──
# Deferred name → handle resolution (Reddit names → DDG → social handles).
# On by default; disable via --no-name-resolution CLI flag.
NAME_RESOLUTION_ENABLED = True
# Minimum cross-page mentions before DDG fires for a name.
# Higher = fewer false positives but misses single-mention names.
NAME_RESOLUTION_MIN_MENTIONS = 2
# Max names resolved per sub-category (caps DDG calls).
NAME_RESOLUTION_MAX_PER_SUB = 5

# ── Yield Monitoring ──
# If average regex handles per page drops below this threshold,
# the pipeline report flags a ⚠️ LOW YIELD warning.
# Typical healthy runs produce ~10-15 handles/page.
YIELD_WARNING_THRESHOLD = 2.0

# ── Misc ──
CURRENT_YEAR = str(datetime.now().year)  # Used in search queries and SeedJob defaults

