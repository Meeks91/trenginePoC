# Seed Crawler Architecture

> **Purpose:** Monthly discovery of top creators across categories × regions × platforms.  
> **Backbone tools:** Firecrawl (agent endpoint) for search + extraction, ScrapeCreators for ongoing profile monitoring.

---

## Design Principles

- Each category operates across **all regions** — no region scoping at category level
- Every category must have `query_terms` for every language present in `REGIONS`
- Every subcategory must have `query_terms` for every language present in `REGIONS`
- Labels must be translated for every language present in `REGIONS`
- These are **config-load-time constraints** — violated configs fail immediately, never at runtime
- Supported locales: `en`, `fr`, `pt`, `es`

---

## Registry Definitions

### Platforms

```python
PLATFORMS = {
    "IG": { "label": { "en": "Instagram", "fr": "Instagram", "pt": "Instagram", "es": "Instagram" } },
    "YT": { "label": { "en": "YouTube",   "fr": "YouTube",   "pt": "YouTube",   "es": "YouTube"   } },
    "TK": { "label": { "en": "TikTok",    "fr": "TikTok",    "pt": "TikTok",    "es": "TikTok"    } },
}
```

### Regions

```python
REGIONS = {
    "US": { "language": "en", "label": { "en": "United States", "fr": "États-Unis",    "pt": "Estados Unidos", "es": "Estados Unidos" } },
    "UK": { "language": "en", "label": { "en": "United Kingdom", "fr": "Royaume-Uni",  "pt": "Reino Unido",    "es": "Reino Unido"    } },
    "FR": { "language": "fr", "label": { "en": "France",         "fr": "France",       "pt": "França",         "es": "Francia"        } },
    "BR": { "language": "pt", "label": { "en": "Brazil",         "fr": "Brésil",       "pt": "Brasil",         "es": "Brasil"         } },
    "ES": { "language": "es", "label": { "en": "Spain",          "fr": "Espagne",      "pt": "Espanha",        "es": "España"         } },
}
```

### Seed Strategy

```python
SEED_STRATEGY = {
    "IG": { "sources": ["FC"],           "min_threshold": 10 },
    "YT": { "sources": ["FC", "YT_API"], "min_threshold": 10 },
    "TK": { "sources": ["FC"],           "min_threshold": 10 },
}
```

- `FC` = Firecrawl (search articles for top creators)
- `YT_API` = YouTube Data API (supplementary source for YT seeds)
- `min_threshold` = minimum number of seeds required per category × region

---

## Categories (Example: Fitness)

```python
CATEGORIES = {
    "fitness": {
        "label": {
            "en": "Fitness",
            "fr": "Fitness",
            "pt": "Fitness",
            "es": "Fitness",
        },
        "query_terms": {
            "en": ["top fitness influencers instagram", "best fitness content creators"],
            "fr": ["meilleurs influenceurs fitness"],
            "pt": ["melhores influenciadores fitness"],
            "es": ["mejores influencers de fitness"],
        },
        "subcategories": {
            "science_based": {
                "label": {
                    "en": "Science-Based",
                    "fr": "Basé sur la science",
                    "pt": "Baseado em ciência",
                    "es": "Basado en ciencia",
                },
                "query_terms": {
                    "en": [
                        "top science-based fitness influencers",
                        "best evidence-based fitness creators",
                        "top natural bodybuilding influencers",
                    ],
                    "fr": ["meilleurs influenceurs fitness scientifique"],
                    "pt": ["melhores influenciadores fitness científico"],
                    "es": ["mejores influencers fitness basado en ciencia"],
                },
            },
            "bodybuilding": {
                "label": {
                    "en": "Bodybuilding",
                    "fr": "Bodybuilding",
                    "pt": "Fisiculturismo",
                    "es": "Culturismo",
                },
                "query_terms": {
                    "en": ["top bodybuilding influencers", "best bodybuilding creators instagram"],
                    "fr": ["meilleurs influenceurs bodybuilding"],
                    "pt": ["melhores influenciadores fisiculturismo"],
                    "es": ["mejores influencers de culturismo"],
                },
            },
        },
    },
}
```

---

## Job Generation

```python
def get_seed_jobs(categories: dict) -> list:
    jobs = []

    for platform_key in PLATFORMS:
        strategy = SEED_STRATEGY[platform_key]

        for region_key, region in REGIONS.items():
            language = region["language"]

            for cat_key, cat in categories.items():

                # Top level category job
                jobs.append({
                    "platform":    platform_key,
                    "region":      region_key,
                    "category":    cat_key,
                    "subcategory": None,
                    "queries":     cat["query_terms"][language],
                    "strategy":    strategy,
                })

                # One job per subcategory
                for sub_key, sub in cat["subcategories"].items():
                    jobs.append({
                        "platform":    platform_key,
                        "region":      region_key,
                        "category":    cat_key,
                        "subcategory": sub_key,
                        "queries":     sub["query_terms"][language],
                        "strategy":    strategy,
                    })

    return jobs
```

---

## Job Matrix (for Fitness alone)

With 3 platforms × 5 regions × (1 category + 2 subcategories) = **45 seed jobs**

Each job runs its `queries` through Firecrawl's agent endpoint to discover and extract creator profiles.

---

## Data Flow

```
┌─────────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│ CATEGORIES  │────▶│ get_seed_    │────▶│   Firecrawl    │────▶│  Seed DB     │
│ config      │     │ jobs()       │     │   /agent       │     │  (creators)  │
└─────────────┘     └──────────────┘     └────────────────┘     └──────┬───────┘
                                                                       │
                                                                       ▼
                                                                ┌──────────────┐
                                                                │ ScrapeCreators│
                                                                │ (monitoring) │
                                                                └──────┬───────┘
                                                                       │
                                                                       ▼
                                                                ┌──────────────┐
                                                                │ TrendPuppy   │
                                                                │ Dashboard    │
                                                                └──────────────┘
```

**Monthly cycle:** Config → Jobs → Firecrawl discovers creators → Store seeds → ScrapeCreators monitors their content → TrendPuppy surfaces what's hot
