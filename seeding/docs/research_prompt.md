# Research Task: Reverse-Engineer Optimal Search Prompts for Influencer Discovery

review this prompt guide and confirm your understanding before we behin work. this is research for my start up and it isi critical we ge tthis rihgght. your are my lead engineer and researcher 





## Context

We are building TrendPuppy, a trend-tracking tool for social media creators. The product monitors top influencers ("seeds") across specific niches to surface trending content.

To populate our seed database, we use the Firecrawl `/agent` endpoint — an AI-powered web research API that searches the internet, visits pages, and returns structured data. We give it a prompt, it goes and finds what we asked for.

**The problem:** Our internal category/subcategory names may not match how the internet talks about these niches. If our prompt uses the wrong language, the agent wastes credits visiting unhelpful pages or returns poor results.

**Your job:** For each of our 72 subcategories, discover through research what search terms, phrasing, and source sites produce the best results for finding influencer names and handles. Then build the optimised sub-query prompt that will be injected into our master Firecrawl agent prompt.

Note:

 you do have access to the entire internet. This should be your primary form of research for this task. We're using your internet research to look ahead for the firecrawl. YOU MUST LOOK VERY DEEPLY, do not stop at first results.

## Why Reverse Engineering Matters

We do NOT want to guess what search terms work. We want to:

1. Actually search for each subcategory using our internal name
2. See what comes back — what sources appear, what language those sources use, whether handles are present
3. If results are thin or mismatched, test alternative phrasings until we find what works
4. Test with AND without region — run searches both with region (e.g. "UK", "US") and without. Document whether region helps or hurts result quality for each sub
5. Search Reddit specifically — check relevant subreddits for creator recommendation threads (e.g. r/fitness, r/BeautyGuruChatter, r/gaming). These often surface different creators than listicles
6. Record the WINNING search terms — the ones that reliably return pages listing influencer names and handles
7. Note which source sites consistently appear — build toward the master site list
8. Build the prompt from proven results, not assumptions

The output should be grounded in what you actually found, not what you think might work.

**Critical rule:** Always test the internal sub name FIRST before trying alternatives. Don't assume it won't work — many internal names match article language perfectly. Only explore synonyms if the internal name returns thin or mismatched results. Document what you tried in order.

## Source Types to Consider

Don't limit yourself to listicle articles. A key goal of this research is to **build a master collection of reliable source sites** that we can direct the Firecrawl agent to. The more good sites we know about, the less the agent wanders and the fewer credits it burns.

Useful source types include:

- **Influencer directories/platforms** (e.g. Feedspot, Modash, Favikon, HypeAuditor rankings, Collabstr, Social Cat, Influencer Hero, StarNgage)
- **Blog listicles** ("Top X influencers in Y niche")
- **Reddit threads** (r/fitness, r/yoga, r/BeautyGuruChatter, r/gaming — these often have authentic creator recommendations with handles)
- **Niche community forums** and specialty sites
- **YouTube/TikTok "who to follow" videos** (transcripts or descriptions listing handles)
- **Agency recommendation pages** (influencer marketing agencies listing creators by niche)
- **Platform-native discovery** (TikTok discover pages, Instagram explore compilations)

The more diverse the source types, the more robust the prompt.

## The Data Shape

For each subcategory, produce:

### Markdown Table Row:

| Field | Description |
|---|---|
| category | Parent category name |
| subName | Our internal subcategory name |
| searchPrompt | The optimised search phrase to inject into the master prompt (using proven language from research) |
| altSearchTerms | Alternative phrasings tested that also returned useful results |
| knownSources | List of specific sites/source types that returned influencer handles for this sub (these feed into the master site list) |
| platformNotes | Any differences in how this sub should be searched per platform (TikTok vs Instagram vs YouTube) |
| regionNotes | Results of testing with/without region — does adding "UK" or "US" help or make results too thin? |
| difficulty | Easy / Medium / Hard — based on how much testing was needed and how abundant the results are |

### JSON Shape (after markdown approval):

```json
{
  "category": "FITNESS",
  "subs": [
    {
      "subName": "Calisthenics",
      "searchPrompt": "top calisthenics influencers {platform} {region} 2025",
      "altSearchTerms": ["bodyweight fitness influencers", "street workout influencers"],
      "knownSources": ["feedspot.com", "thesocialcat.com", "modash.io"],
      "platformNotes": "Works consistently across all platforms",
      "regionNotes": "UK results thinner than US for this niche",
      "difficulty": "easy"
    }
  ]
}
```

### Master Site List (separate deliverable)

In addition to the per-sub data, maintain a **master list of all source sites discovered** across all categories. This list is a key output — it becomes the base set of sites we can inject into every agent prompt to give it good direction.

The master site list should be structured as:

```json
{
  "masterSiteList": {
    "universal": ["sites that appeared across most/all categories"],
    "byCategory": {
      "FITNESS": ["sites specific to fitness"],
      "FOOD_AND_COOKING": ["sites specific to food"],
      ...
    }
  }
}
```


**also provide this in a MD table**

This list should grow as you work through each category. After all 12 are complete, produce the final consolidated version.

## How The Sub-Query Injects Into The Master Prompt

The Firecrawl agent receives a master prompt with the sub-query injected. Here's the structure:

### Master Prompt Template:

```
Find {platform} influencers based in {region} who create content about {sub_query}.

{source_guidance}

Extract every influencer name and their {platform} handle from the sources you find. Return as many as possible. Return only names and handles — no follower counts, no bios, no other data.
```

### Variables:
- `{platform}` — injected: "TikTok", "Instagram", or "YouTube"
- `{region}` — injected: "UK", "US" (and later "France", "Spain", "Brazil")
- `{sub_query}` — this is what YOU are designing. It's the search phrase that tells the agent what niche to search for
- `{source_guidance}` — optional line naming specific sites to prioritise, built from your `known_sources` findings

### Pydantic Schema (what the agent returns):

```python
from pydantic import BaseModel
from typing import List

class Influencer(BaseModel):
    name: str
    handle: str

class SeedResults(BaseModel):
    influencers: List[Influencer]
```

### Full API Call:

```python
result = app.agent(
    prompt=master_prompt,  # with sub_query and source_guidance injected
    schema=SeedResults,
    model="spark-1-mini",
    maxCredits=50
)
```

### Key Firecrawl Agent Best Practices:
- Prompt specificity saves credits — vague prompts cause the agent to visit more pages
- `spark-1-mini` is 60% cheaper than `spark-1-pro` and sufficient for this task
- `maxCredits` caps spending per call
- The agent visits pages autonomously — guiding it to specific source sites reduces wandering
- Each page visited costs credits, so the fewer pages needed to find good data, the better

## The 72 Subcategories

### 1. FITNESS
| # | Sub Name |
|---|---|
| 1 | Fitness (top level) |
| 2 | Calisthenics |
| 3 | Science-Based Training |
| 4 | Powerlifting / Strength |
| 5 | Women's Fitness |
| 6 | Yoga / Mobility |

### 2. FOOD & COOKING
| # | Sub Name |
|---|---|
| 7 | Food & Cooking (top level) |
| 8 | Quick Recipes |
| 9 | Protein / Macros |
| 10 | Healthy / Diet |
| 11 | Restaurant Reviews |
| 12 | Street Food |

### 3. AI
| # | Sub Name |
|---|---|
| 13 | AI (top level) |
| 14 | AI Tools & Reviews |
| 15 | AI News & Commentary |
| 16 | AI Creative Tools |
| 17 | AI Coding / Dev Tools |
| 18 | AI Automation / Agents |

### 4. BEAUTY
| # | Sub Name |
|---|---|
| 19 | Beauty (top level) |
| 20 | Makeup Tutorials |
| 21 | Skincare Routines |
| 22 | Haircare |
| 23 | Budget / Dupes |
| 24 | Men's Grooming |

### 5. TECH
| # | Sub Name |
|---|---|
| 25 | Tech (top level) |
| 26 | Smartphones |
| 27 | Laptops & Desktop Reviews |
| 28 | Audio / Headphones |
| 29 | Apps / Software |
| 30 | Wearables / Smart Home |

### 6. BUSINESS & FINANCE
| # | Sub Name |
|---|---|
| 31 | Business & Finance (top level) |
| 32 | Personal Finance / Saving |
| 33 | Investing |
| 34 | Side Hustles / Entrepreneurship |
| 35 | Career / Productivity |
| 36 | Financial News / Commentary |

### 7. LIFE HACKERS
| # | Sub Name |
|---|---|
| 37 | Life Hackers (top level) |
| 38 | Money Saving / Budget Hacks |
| 39 | CleanTok / Cleaning |
| 40 | Home Organisation / Decluttering |
| 41 | DIY / Home Repair |
| 42 | Life & Productivity Hacks |

### 8. REACTORS
| # | Sub Name |
|---|---|
| 43 | Reactors (top level) |
| 44 | Film / TV Reactions |
| 45 | Music Reactions |
| 46 | Sports Reactions |
| 47 | Food / Try Reactions |
| 48 | Celebrity News & Gossip |

### 9. FASHION
| # | Sub Name |
|---|---|
| 49 | Fashion (top level) |
| 50 | Women's Fashion |
| 51 | Women's Hauls / Try-Ons |
| 52 | Women's Thrift / Budget Styling |
| 53 | Men's Fashion / Style |
| 54 | Men's Sneakers / Streetwear |

### 10. GAMING
| # | Sub Name |
|---|---|
| 55 | Gaming (top level) |
| 56 | Game Reviews |
| 57 | Gaming Guides / Tutorials |
| 58 | Streaming / Let's Play |
| 59 | Esports / Competitive |
| 60 | Gaming Clips |

### 11. HEALTH & WELLNESS
| # | Sub Name |
|---|---|
| 61 | Health & Wellness (top level) |
| 62 | Supplements / Biohacking |
| 63 | Mental Health Tips |
| 64 | Longevity / Anti-Aging |
| 65 | Nutrition Science |
| 66 | Women's Health |

### 12. TRAVEL
| # | Sub Name |
|---|---|
| 67 | Travel (top level) |
| 68 | Budget Travel Tips |
| 69 | City Guides |
| 70 | Travel Hacks |
| 71 | Solo / Digital Nomad |
| 72 | Adventure / Outdoor |

## Worked Example: FITNESS (Partially Complete — Needs Extension)

This category has been partially researched. Use it as a reference for methodology and output format, but **you need to extend it**:

- **Reddit was not searched** — revisit all Fitness subs and search Reddit (r/fitness, r/bodyweightfitness, r/yoga, r/powerlifting, r/xxfitness) for creator recommendations
- **Niche community sites were not explored** — check if there are fitness-specific forums or community sites that list creators
- **Region testing was light** — test each sub with explicit UK and US searches to see if region makes results better or worse
- Add any new sources discovered to the master site list

### Research Process (to replicate for all categories):
For each sub, I searched using the internal name first (e.g. "top calisthenics influencers TikTok Instagram 2025"), reviewed what sources came back, noted which sites returned handles, and tested alternative phrasings where the internal name didn't match article language.

### Results:

| sub_name | search_prompt | alt_search_terms | known_sources | platform_notes | region_notes | difficulty |
|---|---|---|---|---|---|---|
| Fitness (top level) | `top fitness influencers {platform} {region} 2025` | gym influencers, GymTok influencers, workout influencers | feedspot.com, thesocialcat.com, modash.io, wod.guru, euka.ai, insense.pro, favikon.com, collabstr.com, influencer-hero.com | "GymTok" works well as alt term for TikTok specifically | Both UK and US return abundant results | Easy |
| Calisthenics | `top calisthenics influencers {platform} {region} 2025` | bodyweight fitness influencers, street workout influencers | feedspot.com, thesocialcat.com, modash.io, influencer-hero.com, calisthentials.com, autogather.ai | Consistent across platforms | UK thinner than US but still viable | Easy |
| Science-Based Training | `top science based fitness influencers {platform} {region} 2025` | evidence based fitness influencers, science backed training influencers | theinfluenceagency.com, girlsloveevidence.com, trainerize.com, async.com | YouTube strongest for this sub (long-form science content) | Region doesn't affect results much — niche is global | Easy but needs synonym — internal name doesn't match article language |
| Powerlifting / Strength | `top powerlifting influencers {platform} {region} 2025` | strength training influencers, weightlifting influencers | feedspot.com, thesocialcat.com, modash.io, collabstr.com, influencer-hero.com | Consistent across platforms | US much richer than UK | Easy |
| Women's Fitness | `top female fitness influencers {platform} {region} 2025` | women's workout influencers, gym girl influencers | feedspot.com, thesocialcat.com, modash.io, afluencer.com, stackinfluence.com, influencity.com, favikon.com | "gym girl" works well for TikTok specifically | Both regions abundant | Easy but needs reframing — search "female fitness" not "women's fitness" |
| Yoga / Mobility | `top yoga influencers {platform} {region} 2025` | yoga creators, yoga teachers | feedspot.com, thesocialcat.com, modash.io, collabstr.com, favikon.com, theinfluenceagency.com, ainfluencer.com, vagaro.com | Consistent across platforms | Both regions abundant | Easy — let yoga dominate, don't search "mobility" separately (too thin) |

### Key Observations From Fitness Research:
- "top [niche] influencers {platform} {region} 2025" was the most reliable query structure
- Some internal sub names don't match article language and need synonyms (Science-Based Training → "science based fitness", Women's Fitness → "female fitness")
- Certain source sites appeared across every sub — these will form the basis of the master site list
- Reddit was NOT tested — this is a gap you need to fill for Fitness and all subsequent categories
- Region testing was not thorough — for each sub, explicitly test WITH and WITHOUT region to document the impact

## Deliverables Summary

1. **Per-sub data** — markdown table then JSON for each category (72 rows total)
2. **Master site list** — all source sites discovered, organised by universal + per-category, growing as you work through categories
3. **Pattern summary** — after completing all 12 categories, summarise what you learned about query structure, synonym needs, source reliability, platform differences, and region impact

## Execution Plan

Work through the categories **one at a time**. For each:

1. **Propose your research approach** for that category before searching (any subs you expect to be tricky?)
2. **Wait for my approval** before proceeding with searches
3. **Run the research** — search for each sub, test alternatives, record findings
4. **Present results as a markdown table** (same format as the Fitness example)
5. **Wait for my approval** before moving to JSON
6. **Output approved results as JSON**
7. **Move to the next category**

### Category Order:
1. 🔄 Fitness (partially done — extend with Reddit, niche sites, and region testing)
2. Food & Cooking
3. AI
4. Beauty
5. Tech
6. Business & Finance
7. Life Hackers
8. Reactors
9. Fashion
10. Gaming
11. Health & Wellness
12. Travel

Start by extending Fitness (add Reddit and niche sources), then move to Food & Cooking. Propose your approach first — which subs do you expect to be straightforward and which might need synonym exploration?

## Final Deliverables (after all 12 categories complete)

1. **Per-category JSON** — 12 JSON objects, one per category, with all sub-query data
2. **Consolidated master site list JSON** — all discovered sites, organised universal + by category
3. **Summary of patterns** — what query structures worked best, which categories were hardest, any universal observations about platform/region differences