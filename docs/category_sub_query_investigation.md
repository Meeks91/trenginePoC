# TrendPuppy — Seed Discovery: Research Task

## What We're Building

TrendPuppy is a trend-tracking product for social media creators. It works by monitoring the top influencers ("seeds") in specific niches and surfacing what content is performing best across those seeds.

We need to find the top influencers for each of our 72 niche groupings, across 3 platforms (TikTok, Instagram, YouTube) and 2 regions (UK, US).

We will use the Firecrawl `/agent` endpoint to automate this discovery. The agent searches the web, visits pages, and returns structured data. To make these agent calls as efficient as possible (fewer pages visited = fewer credits burned), we need to give it the best possible search prompts.

**This research task is about designing those prompts.**

## The Problem

Our 72 niche groupings use internal names (e.g. "Science-Based Training", "CleanTok / Cleaning", "Celebrity News & Gossip"). These names may NOT match how the internet talks about these niches. Articles, listicles, and influencer directories may use completely different terminology.

If we give the Firecrawl agent a prompt using our internal name and that name doesn't match how articles phrase it, the agent will waste credits searching unsuccessfully or return poor results.

## The Research Methodology

For each of the 72 groupings below, do the following:

### Step 1: Search using our internal sub name
Search the web for: `"top {sub_name} influencers {platform} 2025"` (test with TikTok and Instagram as the platform).

Note:
- What results come back? Listicles with handles? Directory pages? Nothing useful?
- Which specific sites/sources appear? (e.g. Feedspot, Social Cat, Modash, Favikon, blog posts)
- Do the results actually match our intended niche, or do they return something different?

### Step 2: If results are thin or mismatched, test alternative phrasings
Try variations of the search. For example, if "Science-Based Training influencers" returns nothing useful, try different phrasings until you find what works.

The goal is to find the search terms that reliably return listicle articles naming influencers with their social media handles.

### Step 3: Record the winning search terms
For each sub, document:
- **Our internal sub name**
- **Best search term(s)** — the phrasing that returned the most useful results
- **Alternative terms tested** — what else you tried and how it performed
- **Best source sites** — which sites consistently appeared with handle data
- **Platform notes** — does the search term need to change per platform?
- **Region notes** — does adding "UK" or "US" to the search produce good results, or does it make results too thin?
- **Difficulty** — Easy (abundant results), Medium (needed synonym testing), Hard (very thin results even with alternative terms)

### Step 4: Reverse engineer patterns
After completing all 72 groupings, look for patterns:
- Are there universal source sites that appear across most niches?
- Is there a consistent query structure that works best?
- Do certain categories need fundamentally different approaches?
- How does platform (TikTok vs Instagram vs YouTube) affect which search terms work?
- How does region (UK vs US) affect result quality?

### Step 5: Build the final prompts
Using the winning search terms and patterns discovered, construct the Firecrawl agent prompt for each sub. Each prompt should direct the agent to search efficiently and return only names and handles.

## Firecrawl Agent Technical Notes

### Schema (output structure — names and handles only)
```python
from pydantic import BaseModel
from typing import List

class Influencer(BaseModel):
    name: str
    handle: str

class SeedResults(BaseModel):
    influencers: List[Influencer]
```

### Agent call structure
```python
result = app.agent(
    prompt="<the prompt we're designing>",
    schema=SeedResults,
    model="spark-1-mini",
    maxCredits=50
)
```

### Key best practices from Firecrawl docs
- "The prompt matters more here than with the other endpoints. Be specific about what sources you want checked and what kind of information you're after."
- `spark-1-mini` is 60% cheaper than `spark-1-pro` and sufficient for straightforward extraction
- `maxCredits` caps spending per call
- The agent visits pages autonomously — fewer pages visited = cheaper, so specific prompts that guide it to the right sources quickly save credits

## The 72 Groupings to Research

### 1. FITNESS
| # | Internal Sub Name |
|---|---|
| 1 | Fitness (top level) |
| 2 | Calisthenics |
| 3 | Science-Based Training |
| 4 | Powerlifting / Strength |
| 5 | Women's Fitness |
| 6 | Yoga / Mobility |

### 2. FOOD & COOKING
| # | Internal Sub Name |
|---|---|
| 7 | Food & Cooking (top level) |
| 8 | Quick Recipes |
| 9 | Protein / Macros |
| 10 | Healthy / Diet |
| 11 | Restaurant Reviews |
| 12 | Street Food |

### 3. AI
| # | Internal Sub Name |
|---|---|
| 13 | AI (top level) |
| 14 | AI Tools & Reviews |
| 15 | AI News & Commentary |
| 16 | AI Creative Tools |
| 17 | AI Coding / Dev Tools |
| 18 | AI Automation / Agents |

### 4. BEAUTY
| # | Internal Sub Name |
|---|---|
| 19 | Beauty (top level) |
| 20 | Makeup Tutorials |
| 21 | Skincare Routines |
| 22 | Haircare |
| 23 | Budget / Dupes |
| 24 | Men's Grooming |

### 5. TECH
| # | Internal Sub Name |
|---|---|
| 25 | Tech (top level) |
| 26 | Smartphones |
| 27 | Laptops & Desktop Reviews |
| 28 | Audio / Headphones |
| 29 | Apps / Software |
| 30 | Wearables / Smart Home |

### 6. BUSINESS & FINANCE
| # | Internal Sub Name |
|---|---|
| 31 | Business & Finance (top level) |
| 32 | Personal Finance / Saving |
| 33 | Investing |
| 34 | Side Hustles / Entrepreneurship |
| 35 | Career / Productivity |
| 36 | Financial News / Commentary |

### 7. LIFE HACKERS
| # | Internal Sub Name |
|---|---|
| 37 | Life Hackers (top level) |
| 38 | Money Saving / Budget Hacks |
| 39 | CleanTok / Cleaning |
| 40 | Home Organisation / Decluttering |
| 41 | DIY / Home Repair |
| 42 | Life & Productivity Hacks |

### 8. REACTORS
| # | Internal Sub Name |
|---|---|
| 43 | Reactors (top level) |
| 44 | Film / TV Reactions |
| 45 | Music Reactions |
| 46 | Sports Reactions |
| 47 | Food / Try Reactions |
| 48 | Celebrity News & Gossip |

### 9. FASHION
| # | Internal Sub Name |
|---|---|
| 49 | Fashion (top level) |
| 50 | Women's Fashion |
| 51 | Women's Hauls / Try-Ons |
| 52 | Women's Thrift / Budget Styling |
| 53 | Men's Fashion / Style |
| 54 | Men's Sneakers / Streetwear |

### 10. GAMING
| # | Internal Sub Name |
|---|---|
| 55 | Gaming (top level) |
| 56 | Game Reviews |
| 57 | Gaming Guides / Tutorials |
| 58 | Streaming / Let's Play |
| 59 | Esports / Competitive |
| 60 | Gaming Clips |

### 11. HEALTH & WELLNESS
| # | Internal Sub Name |
|---|---|
| 61 | Health & Wellness (top level) |
| 62 | Supplements / Biohacking |
| 63 | Mental Health Tips |
| 64 | Longevity / Anti-Aging |
| 65 | Nutrition Science |
| 66 | Women's Health |

### 12. TRAVEL
| # | Internal Sub Name |
|---|---|
| 67 | Travel (top level) |
| 68 | Budget Travel Tips |
| 69 | City Guides |
| 70 | Travel Hacks |
| 71 | Solo / Digital Nomad |
| 72 | Adventure / Outdoor |

## Deliverable

For each of the 72 groupings, a completed row in this format:

| # | Internal Sub Name | Best Search Term(s) | Alternative Terms Tested | Best Source Sites | Platform Notes | Region Notes | Difficulty | Final Agent Prompt |
|---|---|---|---|---|---|---|---|---|

Plus a summary of patterns observed across categories that could inform a universal prompt template.