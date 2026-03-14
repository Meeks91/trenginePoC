# Web Crawler Comparison — Seed Discovery for TrendPuppy

> **Date:** 2026-03-04  
> **Goal:** Compare Firecrawl with alternatives for TrendPuppy's seed crawler. Key requirement: **agent-style endpoint** where you send a query/config and get structured results back — no manual URL management.  
> **Verdict:** Firecrawl's `/extract` and `/agent` endpoints are the best fit. No competitor matches the simplicity of config → structured JSON for this use case.

---

## What TrendPuppy Needs from a Crawler

The seed crawler runs **monthly** across categories × regions × languages, sending queries like:

```
"top science-based fitness influencers" (en)
"meilleurs influenceurs fitness scientifique" (fr)
"melhores influenciadores fitness científico" (pt)
```

**Requirements:**

1. ✅ **Agent/extract endpoint** — send a query, get structured data. No URL management
2. ✅ **Search + extract** — find articles via search, then extract structured creator data
3. ✅ **LLM-powered extraction** — pull creator names/handles from unstructured article text
4. ✅ **Multi-language** — must handle en, fr, pt, es content
5. ✅ **Reliable SaaS** — managed infrastructure, not self-hosted
6. ⚠️ **Cost-efficient** — monthly batch job, not high-volume real-time

---

## Firecrawl — Your Current Choice

| Feature              | Detail                                                                                              |
| -------------------- | --------------------------------------------------------------------------------------------------- |
| **Agent endpoint**   | ✅ `/agent` — give it a prompt + goal, it navigates the web autonomously                            |
| **Extract endpoint** | ✅ `/extract` — define JSON schema + prompt, get structured data from any URL                       |
| **Search endpoint**  | ✅ `/search` — search the web, returns full page content from results                               |
| **LLM extraction**   | ✅ Built-in, uses JSON schema for structured output                                                 |
| **Multi-language**   | ✅ Works with any language content                                                                  |
| **Anti-bot**         | ⚠️ Moderate — handles JS rendering, rotating proxies, but can struggle with heavily protected sites |
| **Pricing**          | Scrape: Free 500pg/mo → $16/mo (3K pg) → $333/mo (500K pg). Extract: $89/mo (18M tokens/yr)         |
| **SDKs**             | Python, Node.js, Go, Rust                                                                           |
| **SOC 2**            | ✅ Type 2 compliant                                                                                 |

### Why it fits your use case well:

- The **`/agent` endpoint** is exactly what your seed config needs — send your `query_terms` and let the agent find + extract creators
- The **`/extract` endpoint** with JSON schema means you can define `{name, handle, platform, followers}` and get clean data back
- **Search + extract combo** maps directly to your `get_seed_jobs()` pattern

---

## Alternatives Compared

### Tier 1: Direct Competitors (Agent/Extract Endpoints)

#### Jina Reader

| Feature              | Detail                                                      |
| -------------------- | ----------------------------------------------------------- |
| **Agent endpoint**   | ❌ No agent mode                                            |
| **Extract endpoint** | ⚠️ Simple URL → clean text. No structured JSON extraction   |
| **Search endpoint**  | ✅ `s.jina.ai/query` — search and get markdown results      |
| **LLM extraction**   | ❌ Raw text only — you'd need to add your own LLM layer     |
| **Pricing**          | Free tier generous. Paid from ~$10/mo                       |
| **Simplicity**       | ✅✅ Simplest option — just prepend `r.jina.ai/` to any URL |

**Verdict:** Too simple for your use case. Great for getting clean text from a URL, but you'd need to build the LLM extraction layer yourself. No agent, no structured output.

---

#### Crawl4AI (Open-Source)

| Feature              | Detail                                             |
| -------------------- | -------------------------------------------------- |
| **Agent endpoint**   | ❌ No hosted agent — you run it yourself           |
| **Extract endpoint** | ✅ Supports custom data schemas + multiple LLMs    |
| **Search endpoint**  | ❌ No built-in search — you provide URLs           |
| **LLM extraction**   | ✅ Integrates with OpenAI, Anthropic, Ollama, etc. |
| **Pricing**          | Free (open-source). You pay for LLM APIs + hosting |
| **Deployment**       | ⚠️ Self-hosted. Requires Python infrastructure     |

**Verdict:** Powerful but wrong model. You'd need to host it, manage infrastructure, and wire up search separately. Defeats the "hit FC with configs" simplicity you want.

---

#### Skrape.ai

| Feature              | Detail                                                    |
| -------------------- | --------------------------------------------------------- |
| **Agent endpoint**   | ❌ No agent mode                                          |
| **Extract endpoint** | ✅ Define JSON schema, get structured data via playground |
| **Search endpoint**  | ❌ You provide URLs                                       |
| **LLM extraction**   | ✅ Built-in                                               |
| **Pricing**          | $15-250/mo                                                |

**Verdict:** Close to Firecrawl's extract but lacks search and agent endpoints. You'd still need to find the URLs first.

---

#### Apify (Web Scraper Actor)

| Feature              | Detail                                                                |
| -------------------- | --------------------------------------------------------------------- |
| **Agent endpoint**   | ⚠️ Has actors that can search + extract, but config is actor-specific |
| **Extract endpoint** | ✅ "Website Content Crawler" converts to LLM-ready text               |
| **Search endpoint**  | ✅ Via Google SERP actors                                             |
| **LLM extraction**   | ⚠️ Not built-in — requires chaining actors or external LLM            |
| **Pricing**          | $39-999/mo + consumption costs                                        |

**Verdict:** More complex than Firecrawl. Could work but requires wiring multiple actors together. No single "send query, get structured results" endpoint.

---

### Tier 2: Different Model (No Agent/Extract)

| Provider        | What it does                                  | Why it doesn't fit                                         |
| --------------- | --------------------------------------------- | ---------------------------------------------------------- |
| **ScrapingBee** | Headless browser API, anti-bot bypass         | No LLM extraction, no agent. Raw HTML only                 |
| **Bright Data** | Enterprise proxy network + pre-built scrapers | $499/mo+. Overkill for monthly batch jobs                  |
| **Oxylabs**     | Proxy + "OxyCopilot" natural language parsing | Designed for e-commerce/SERP data, not article extraction  |
| **ScraperAPI**  | Rotating proxies + CAPTCHA handling           | Raw page data, no structured extraction                    |
| **Diffbot**     | AI entity extraction (articles, products)     | ✅ Could work for article extraction, but $899/mo for Plus |

---

## Head-to-Head: Your Use Case

For the pattern: **config → search → extract structured creator data → return**

| Capability                            | Firecrawl  | Jina           | Crawl4AI         | Skrape.ai  | Apify         |
| ------------------------------------- | ---------- | -------------- | ---------------- | ---------- | ------------- |
| Agent (autonomous browsing)           | ✅         | ❌             | ❌               | ❌         | ⚠️            |
| Search → extract in one call          | ✅         | ⚠️ search only | ❌               | ❌         | ⚠️ multi-step |
| JSON schema extraction                | ✅         | ❌             | ✅               | ✅         | ⚠️            |
| Managed SaaS (no hosting)             | ✅         | ✅             | ❌               | ✅         | ✅            |
| Multi-language                        | ✅         | ✅             | ✅               | ✅         | ✅            |
| Cost for monthly batch (~200 queries) | ~$16-89/mo | ~$10/mo        | Free + LLM costs | ~$15-50/mo | ~$39+/mo      |
| **Config-in, data-out simplicity**    | ✅✅       | ⚠️             | ❌               | ⚠️         | ⚠️            |

---

## Recommendation

> [!IMPORTANT]
> **Stick with Firecrawl.** No alternative matches the agent + extract + search combo for your use case. The `/agent` endpoint maps directly to your seed job configs.

### Why:

1. **Agent endpoint** = your `query_terms` go in, structured creator data comes out
2. **Search + extract** = one service handles both finding articles and pulling data from them
3. **JSON schema** = define `{name, handle, platform, followers}` once, reuse across all categories
4. **Managed SaaS** = no infra to maintain for a monthly batch job
5. **Pricing** = $16-89/mo is reasonable for monthly seed discovery

### Only consider alternatives if:

- **Firecrawl's anti-bot bypass fails** on specific article sites → add ScrapingBee as a fallback for those URLs
- **Cost becomes an issue at scale** → Crawl4AI is free but requires self-hosting
- **You need deeper article understanding** → Diffbot has best-in-class article entity extraction, but at $899/mo

---

## Potential Complementary Tool: Jina Reader

Even though Jina isn't a replacement, it could be useful as a **cheap fallback**:

- If Firecrawl fails on a URL, retry with `r.jina.ai/{url}` to get clean text
- Then extract with your own LLM call
- Generous free tier, nearly zero config
