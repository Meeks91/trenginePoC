# Instagram Reel Discovery — Provider Research Report

> **Date:** 2026-03-03  
> **Goal:** Find a SaaS-grade API to discover trending Instagram Reels by hashtag, keyword (freeword), and region — supplementary to TrendPuppy's seed crawler architecture.  
> **Verdict:** No provider reliably solves this. Seed architecture is the right approach for V1.

---

## Architecture Context

TrendPuppy's trend engine uses a **seed-based architecture**:

| Layer                       | Tool               | Purpose                                                                        |
| --------------------------- | ------------------ | ------------------------------------------------------------------------------ |
| Seed Discovery              | **Firecrawl**      | Monthly crawl of articles to find top creators by category × region × platform |
| Profile Monitoring          | **ScrapeCreators** | Track seed creators' content over time                                         |
| **Supplementary Discovery** | **???**            | Catch trending content from non-seeded creators                                |

This research was to fill the supplementary layer for Instagram specifically.

---

## Providers Tested Hands-On

### 1. Bright Data — ❌ No IG Search

**What we tested:** Instagram Data Collector API  
**Result:** Only accepts profile URLs as input. No hashtag search, no keyword search. The `country` parameter for geo-targeting was rejected by the API.

**Bottom line:** Bright Data is for scraping known profiles at scale, not for content discovery.

---

### 2. Apify `instagram-hashtag-scraper` — ⚠️ Partial

**What we tested:** Hashtag search with reels filter, UK proxy geo-targeting  
**Results:**

- ✅ Hashtag search **works** — returns real reel data (views, likes, comments, audio, video URL)
- ✅ Reel-only filter **works** — `resultsType: "reels"`
- ❌ **Freeword search doesn't exist** — the "keyword" mode just splits words into separate hashtags
- ❌ **Geo-targeting via proxy doesn't work** — UK proxy returned identical results to no proxy (Spanish/Indian/global content for `#gym`)
- ⚠️ Location-specific hashtags work (`#londongym`) but the pool is tiny

**Key finding:** Instagram's `/explore/tags/` page is **not geo-personalized**. It shows globally trending content regardless of IP. The URL redirects to `/popular/` in-browser, which IS personalized — but only for logged-in sessions. No scraper can access the personalized view without cookies.

**Pricing:** ~$2.60/1K results, $5 free credit

---

### 3. SociaVault — ❌ Fake Endpoints

**What we tested:** Their blog post's API examples for hashtag/reels search  
**Result:** The endpoint `api.sociavault.com/v1/instagram/hashtag/reels` returns **404 "Route not found"**. Tested 5 URL patterns — all 404.

**Their actual API only supports:** profile lookup, posts from a profile, post/reel info by URL. **No hashtag or keyword search exists.**

> [!CAUTION]
> SociaVault's blog contains fabricated code examples with non-existent endpoints. Same owner as ScrapeCreators. Avoid.

---

### 4. Apify `instagram-scraper` (general) — ⚠️ No Reel Filter

**Researched (not tested):** Supports hashtag search via `searchType: "hashtag"` but returns mixed post types (images, carousels, reels). No `resultsType` filter for reels only.

**Pricing:** ~$2.30/1K results

---

### 5. Apify `instagram-search-scraper` — ❌ Metadata Only

**Researched (not tested):** Returns **hashtag metadata** (name, post count, related hashtags, difficulty). Does NOT return actual posts or reels.

---

## Provider Sweep — Could Any Fill the Gap?

### Enterprise / SaaS-Grade

| Provider        | IG Reel Discovery?                                              | Geo-targeting?        | Pricing                             | Verdict                                                        |
| --------------- | --------------------------------------------------------------- | --------------------- | ----------------------------------- | -------------------------------------------------------------- |
| **Modash**      | ✅ AI content search                                            | ✅ Location filters   | ~$199-299/mo+                       | ❌ Too expensive (user excluded)                               |
| **HypeAuditor** | ✅ "Reels Inspiration" tool with niche/location/keyword filters | ✅ Location, language | ~$300/mo+                           | ⚠️ Possible but expensive, mainly an influencer analytics tool |
| **Upfluence**   | ⚠️ Influencer discovery, not content discovery                  | ✅ Audience filtering | ~$2,000/mo+                         | ❌ Way too expensive, wrong use case                           |
| **Phyllo**      | ⚠️ Wraps official IG Graph API                                  | Limited               | Custom pricing                      | ❌ Same Graph API limits (30 hashtags/week)                    |
| **CrowdTangle** | ⚠️ Tracks virality on linked pages                              | No real IG discovery  | Was free for newsrooms, now limited | ❌ Shutting down / merged into Meta tools                      |

### Scraping APIs

| Provider                  | IG Reel Discovery?                      | Geo-targeting?       | Pricing      | Verdict                                 |
| ------------------------- | --------------------------------------- | -------------------- | ------------ | --------------------------------------- |
| **Data365**               | ⚠️ Profile monitoring, hashtag tracking | Unknown              | Credit-based | ❌ Same limitations as Apify            |
| **RapidAPI scrapers**     | Various — some have "reels explore"     | Varies               | $10-50/mo    | ⚠️ Individual devs, unreliable for SaaS |
| **Instagrapi / Lamadava** | ⚠️ Reverse-engineers IG mobile API      | Possibly via session | Custom       | ⚠️ High maintenance, ban risk           |

### Official API

| Provider                | IG Reel Discovery?                          | Geo-targeting?      | Pricing                          | Verdict                                                                                  |
| ----------------------- | ------------------------------------------- | ------------------- | -------------------------------- | ---------------------------------------------------------------------------------------- |
| **Instagram Graph API** | ✅ `top_media` + `recent_media` per hashtag | ❌ No geo-filtering | Free (requires Business account) | ⚠️ Limited to **30 unique hashtags per 7 days**. App Review required. No audio metadata. |

---

## The Fundamental Problem

Instagram does **not expose a public content discovery API**. Every approach hits the same wall:

1. **Hashtag explore pages** (`/explore/tags/`) are globally ranked, not geo-personalized
2. **The personalized feed** (Explore, `/popular/`) requires an authenticated session
3. **The Graph API** is limited to 30 hashtags/week and requires Business account OAuth
4. **No service offers freeword search** — Instagram's search bar functionality is completely internal

This is by design. Instagram wants discovery to happen inside their app, not via APIs.

---

## Recommendation for TrendPuppy

> [!IMPORTANT]
> Your seed crawler + ScrapeCreators architecture is the right approach for V1. Don't burn credits on supplementary hashtag discovery — the data quality isn't there.

### Why seeds are enough for "what's hot when it's hot":

- Top creators are **trend amplifiers** — when something goes hot, they jump on it fast
- If no top creator has touched a trend, it's arguably _emerging_, not _hot_ yet
- Your seed crawler (Firecrawl) already finds creators across categories × regions × languages

### If you later want supplementary discovery:

1. **TikTok first** — TikTok's API actually supports keyword + country search. Use it as the trend discovery engine, cross-reference on IG
2. **Audio tracking** — Apify's reel data includes music info. Monitor which sounds your seed creators are using — that's a genuine trend signal
3. **HypeAuditor "Reels Inspiration"** — if budget allows (~$300/mo), this is the only tool that does niche + location + keyword filtered reel discovery. Worth evaluating at scale

### What to keep from today's PoCs:

- The **Apify profile scraper** could complement ScrapeCreators for IG-specific profile monitoring if needed
- The hashtag scraper works for **location-specific hashtags** (`#londongym`) if you ever need manual research

---

## Files Created

```
trenginePoc/
  apify/
    instagram/          # Apify hashtag scraper PoC (working)
      apify_poc.py
      .env
      output/           # Test results (3 runs)
  sociavault/           # SociaVault PoC (dead — API endpoints don't exist)
    sociavault_poc.py
    .env
  brightData/           # Bright Data PoC (from earlier session)
```
