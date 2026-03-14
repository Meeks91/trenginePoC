# Bright Data — Instagram PoC Research Notes

> Primary mission: **Discover trending Instagram Reels by hashtag or search term, with regional targeting.**

---

## ❌ Verdict: Bright Data Cannot Do This

Bright Data's Instagram Web Scraper API **does not support discovery by hashtag or search term**. It only scrapes content from known URLs (profiles, individual posts/reels). This was confirmed through:

1. **API test** — passing `https://www.instagram.com/explore/tags/fitness/` returned a 400 validation error. The API enforces a regex that only allows profile-style URLs (`instagram.com/username/`).
2. **SDK source code** — `InstagramSearchScraper` only supports `discover_by: url` (profile URL) or `discover_by: user_name`. No hashtag or keyword discovery.
3. **Third-party sources** — confirm that Bright Data does not support direct Instagram search. Workaround: use an external tool to find profile URLs, then feed those to Bright Data.
4. **Comparison with TikTok** — Bright Data's TikTok scraper DOES support `discover_by: keyword` and `search_url`. Instagram's does not.

### What About "Direct URL of the search" in Their Docs?

The [Instagram overview page](https://docs.brightdata.com/api-reference/web-scraper-api/social-media-apis/instagram/overview) lists "Direct URL of the search" as a discovery option. However:

- The tooltip on that line shows `"Oops.. No translation found."` — likely a broken/placeholder entry
- The [detailed Posts API page](https://docs.brightdata.com/api-reference/web-scraper-api/social-media-apis/instagram/posts) omits it entirely
- The actual API rejects any URL that doesn't match a profile pattern

**This appears to be a documentation error.**

---

## What Bright Data's Instagram API Actually Does

### Two SDK Classes (from source code)

|              | `client.scrape.instagram`         | `client.search.instagram`                             |
| ------------ | --------------------------------- | ----------------------------------------------------- |
| **Class**    | `InstagramScraper`                | `InstagramSearchScraper`                              |
| **Input**    | Direct post/reel/profile URL      | Profile URL                                           |
| **Purpose**  | Scrape data from a specific URL   | Discover content from a profile                       |
| **Filters**  | None (just `url`, `timeout`)      | `num_of_posts`, `start_date`, `end_date`, `post_type` |
| **Use case** | "Get me data for this exact reel" | "Get me the latest reels from @nasa"                  |

### Geo-targeting / Country

- The `country` field is **explicitly rejected** for Instagram (`"This input should not contain a country field"`)
- TikTok and YouTube support `country` in their payloads — Instagram does not
- Bright Data's residential proxy geo-targeting is a separate product, not available through the Datasets/Scraper API

### `post_type` Values

- API docs say: `post`, `reel` (lowercase)
- SDK source code says: `Post`, `Reel` (capitalized)
- Untested — the API rejected our request before reaching this parameter

---

## Bright Data's Hashtag Dataset (Separate Product)

Bright Data sells pre-built Instagram Hashtag Datasets (970M+ records). This is a **bulk data purchase**, not a query API:

- Starts around $500
- Subscription model (daily/weekly/monthly updates)
- Formats: JSON, CSV, Parquet
- Not suitable for a lightweight, on-demand PoC

---

## API Test Results

### Test 1: Hashtag explore URL + country field

```
URL:    https://www.instagram.com/explore/tags/fitness/
Region: gb (United Kingdom)
Result: HTTP 400 — validation_error
```

Errors:

- `country`: "This input should not contain a country field"
- `url`: regex mismatch — only allows `instagram.com/[username]/[optional-path]/`

**No credit was charged** (request rejected before processing).

---

## Response Fields (from SDK source — untested)

### Reels

`post_id`, `shortcode`, `description`, `hashtags`, `date_posted`, `likes`, `views`, `video_play_count`, `num_comments`, `length`, `video_url`, `audio_url`, `thumbnail`, `user_posted`, `followers`, `is_verified`, `tagged_users`, `is_paid_partnership`

### Posts

`post_id`, `description`, `hashtags`, `date_posted`, `num_comments`, `likes`, `content_type`, `video_view_count`, `video_play_count`, `user_posted`, `followers`, `profile_url`, `photos`, `thumbnail`

---

## Technical Details

| Item                  | Value                                     |
| --------------------- | ----------------------------------------- |
| SDK                   | `brightdata-sdk` (pip)                    |
| Auth                  | `BRIGHTDATA_API_TOKEN` env var            |
| API base              | `https://api.brightdata.com/datasets/v3/` |
| Cost                  | $0.002/record                             |
| Dataset ID (Posts)    | `gd_lk5ns7kz21pck8jpis`                   |
| Dataset ID (Reels)    | `gd_lyclm20il4r5helnj`                    |
| Dataset ID (Profiles) | `gd_l1vikfch901nx3by4`                    |

---

## Next Steps: Alternative Providers for Hashtag Discovery

Since Bright Data can't do hashtag/keyword Instagram search, alternatives to evaluate:

1. **Apify** — Instagram Hashtag Scraper actor (pay per compute unit)
2. **RapidAPI** — multiple Instagram scraper APIs with hashtag search
3. **Bright Data TikTok** — does support keyword discovery if TikTok is also relevant
4. **Hybrid approach** — use another tool for hashtag discovery → get reel URLs → feed to Bright Data for enriched data
