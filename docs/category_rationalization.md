# TrendPuppy — Final 12 Categories, Subcategories & Strategic Analysis

## System Constraints

- **Max categories:** 12
- **Seeds per category per platform:** 30
- **Seed distribution:** `totalSeeds / (numSubcategories + 1)` — each grouping gets equal share
- **Hard limit:** Max 5 subcategories per category (ensures ≥5 seeds per grouping)
- **Seed selection:** Biggest accounts sourced from articles/lists (cannot scan IG directly)
- **Atomic test:** Every subcategory must represent a concrete, searchable creator identity that does not need to be further broken down.

### Scoring Framework

Each category is rated 1-5 on four criteria. Total score out of 20.

- **Derivative Potential (1-5):** How likely is a creator to see seeded content and say "I can make my version of this"?
- **Platform Density (1-5):** How large and active is this niche's creator pool across social platforms?
- **Virality (1-5):** How often does content in this niche spike and go viral (vs steady/evergreen)?
- **12h Scan Value (1-5):** How much does TrendPuppy's 12-hour scan cycle add value? (Fast-moving niches score higher)

| Category | Derivative | Density | Virality | 12h Scan | Total |
|---|---|---|---|---|---|
| Fitness | 5 — "I tried X program for 30 days" | 5 — millions of creators | 4 — challenges/transformations spike | 5 — new programs spike fast | **19** |
| Food & Cooking | 5 — see recipe, make your version | 5 — massive pool | 5 — recipes most viral TikTok format | 4 — food trends over days not hours | **19** |
| AI | 5 — "I tried [new tool]" is the mode | 4 — growing fast, smaller than beauty | 5 — tool launches go viral instantly | 5 — fastest-moving category | **19** |
| Beauty | 5 — dupe culture originated here | 5 — most-discussed on TikTok | 4 — transformations/dupes go viral | 4 — product launches spike, many trends steady | **18** |
| Tech | 4 — reviews derivative, less "make yours" | 4 — solid pool | 4 — product launches spike | 5 — announcements highly time-sensitive | **17** |
| Business & Finance | 3 — side hustles derivative, finance less so | 4 — large pool | 4 — financial news/drama spikes | 4 — side hustle/startup trends move fast | **15** |
| Life Hackers | 5 — see hack, make your version | 4 — CleanTok 71B+ views | 4 — hacks go viral on TikTok | 4 — new hacks/products trend fast | **17** |
| Reactors | 5 — reaction IS derivative by definition | 4 — large across platforms | 4 — reactions to viral content go viral | 3 — reactive, not self-generating trends | **16** |
| Fashion | 4 — hauls/GRWM derivative, styling less so | 4 — large pool | 3 — less viral spike than beauty/food | 4 — seasonal drops time-sensitive | **15** |
| Gaming | 4 — trending game → cover it | 5 — massive pool | 4 — game launches/drama spike fast | 2 — title-specific, harder to catch with 30 seeds | **15** |
| Health & Wellness | 3 — "I tried X supplement" narrower | 4 — growing fast | 3 — less viral spike than fitness | 4 — supplement launches time-sensitive | **14** |
| Travel | 3 — tips derivative, destinations aren't | 4 — large pool | 3 — aspirational, less spike | 4 — destination/deal trends time-sensitive | **14** |

---

## The Final 12 (Overview)

| # | Category | Score | Sub 1 | Sub 2 | Sub 3 | Sub 4 | Sub 5 | Brand Spend |
|---|---|---|---|---|---|---|---|---|
| 1 | Fitness | 19 | Calisthenics | Science-Based Training | Powerlifting / Strength | Women's Fitness | Yoga / Mobility | 🟢🟢🟢🟢 |
| 2 | Food & Cooking | 19 | Quick Recipes | Protein / Macros | Healthy / Diet | Restaurant Reviews | Street Food | 🟢🟢🟢🟢 |
| 3 | AI | 19 | Tools & Reviews | News & Commentary | AI Creative Tools | AI Coding / Dev Tools | Automation / Agents | 🟢🟢 |
| 4 | Beauty | 18 | Makeup Tutorials | Skincare Routines | Haircare | Budget / Dupes | Men's Grooming | 🟢🟢🟢🟢🟢 |
| 5 | Tech | 17 | Smartphones | Laptops & Desktop Reviews | Audio / Headphones | Apps / Software | Wearables / Smart Home | 🟢🟢🟢🟢 |
| 6 | Business & Finance | 15 | Personal Finance | Investing | Side Hustles | Career / Productivity | Financial News | 🟢🟢 |
| 7 | Life Hackers | 17 | Money Saving | CleanTok / Cleaning | Home Organisation | DIY / Home Repair | Life & Productivity Hacks | 🟢🟢🟢 |
| 8 | Reactors | 16 | Film / TV | Music Reactions | Sports | Food / Try | Celebrity News & Gossip | 🟢🟢🟢🟢 |
| 9 | Fashion | 15 | Women's Fashion | Women's Hauls / Try-Ons | Women's Thrift / Budget | Men's Fashion / Style | Men's Sneakers / Streetwear | 🟢🟢🟢🟢🟢 |
| 10 | Gaming | 15 | Game Reviews | Guides / Tutorials | Streaming / Let's Play | Esports / Competitive | Gaming Clips | 🟢🟢🟢🟢 |
| 11 | Health & Wellness | 14 | Supplements / Biohacking | Mental Health Tips | Longevity / Anti-Aging | Nutrition Science | Women's Health | 🟢🟢🟢 |
| 12 | Travel | 14 | Budget Tips | City Guides | Travel Hacks | Solo / Nomad | Adventure / Outdoor | 🟢🟢🟢 |

---

### Category Architecture Note: Derived Top-Levels via Subcategories

Some subcategories act as "periscopes" — they surface content from adjacent niches that don't warrant their own top-level category, effectively giving TrendPuppy coverage of those niches without burning a category slot. Key examples:

- **Reactors → Music Reactions** surfaces music trends to the top level. Music doesn't need its own category because music trend data flows up through reactor seeds covering album drops, song virality, and artist moments.
- **Reactors → Sports Reactions** surfaces sports moments. Sports commentary and highlight reactions make sports trends visible without a dedicated Sports category.
- **Reactors → Celebrity News & Gossip** surfaces celebrity culture, internet culture, and pop culture trends. Comedy was rejected as a standalone category, but comedy-adjacent content is captured here.
- **Reactors → Film/TV** surfaces entertainment trends — new releases, trailer reactions, show discourse.

This means **Reactors is architecturally the most valuable category** — it doesn't just serve reactor creators, it extends TrendPuppy's effective coverage to Music, Sports, Comedy, Celebrity Culture and Entertainment without additional category slots. When selecting seeds for Reactors, prioritise diversity across these sub-niches to maximise periscope coverage.

The same principle applies elsewhere at a smaller scale: **Tech → Apps/Software** surfaces some AI-adjacent tools. **Life Hackers → DIY/Home Repair** surfaces home/interior trends. **Food → Restaurant Reviews** surfaces local/city food trends. When seeding, consider the periscope value of each sub — some subs earn their place not just for their own niche but for what they surface from adjacent territories.

---

## The Final 12

### 1. FITNESS — Score: 19/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Calisthenics | Chris Heria, FitnessFAQs — pure bodyweight accounts | Atomic ✅ |
| Science-Based Training | Jeff Nippard, Renaissance Periodization | Atomic ✅ |
| Powerlifting / Strength | Compound lifts, programming, PRs | Atomic ✅ |
| Women's Fitness | Krissy Cela, Whitney Simmons, Blogilates, Tammy Hembrow | Atomic ✅. Massive creator pool, high brand spend (Gymshark built on this niche), distinct from general fitness |
| Yoga / Mobility | Flows, flexibility, pose tutorials | Mostly evergreen content. Lower trend velocity but strong creator identity |

**Category note:** "Transformations/Progress" was rejected — fails atomic test. No creator's entire channel IS transformations; it's occasional content within fitness channels. "Gym" also rejected as a sub — it's a branching node that breaks into calisthenics, science-based, powerlifting etc. Running was replaced by Women's Fitness — running had lower viral velocity and weaker trend signal. Running creators still surface if they trend across other seeds.

**Platform data:** HypeAuditor: Fitness & Gym = 3.16% of IG influencers. Sprout Social: Fitness nano-influencers achieve 14.61% TikTok ER. Uscreen: Fitness creators earn avg $11,900/month — highest of any niche.

**Dupe/derivative mode:** "I tried [creator]'s program for 30 days" — highly derivative niche, natural sub-mode.

---

### 2. FOOD & COOKING — Score: 19/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Quick Recipes | 15-min meals, air fryer, one-pot — format-driven accounts | Atomic ✅ |
| Protein / Macros | Greg Doucette, Remington James, "anabolic cooking" | Own atomic niche with dedicated creator identity ✅ |
| Healthy / Diet | Clean eating, meal prep, specific diet accounts | Atomic ✅ |
| Restaurant Reviews | Dedicated food review channels | Atomic ✅ |
| Street Food | Street food accounts — massive on YouTube and TikTok | Atomic ✅. Distinct from restaurant reviews (sit-down dining). Clear searchable identity. Replaces "Cuisine Exploration" which was too vague |

**Category note:** "Cuisine Exploration" was replaced by Street Food — no creators identify as "cuisine exploration influencers." Street food accounts are a genuine, searchable creator identity with dedicated channels and large followings.

**Platform data:** Sprout Social: Food & drink nano-influencers achieve 18.36% TikTok ER — highest of any category. 70% of Gen Z list TikTok as top platform for food recommendations.

**Dupe/derivative mode:** Peak derivative — see recipe, make your version. Strongest dupe culture of any category.

---

### 3. AI — Score: 19/20 ⭐ Highest TrendPuppy Value

| Sub | Creator Identity | Notes |
|---|---|---|
| AI Tools & Reviews | Matt Wolfe 694K, Skill Leap AI, The AI Advantage | Atomic ✅. General AI tool roundup channels |
| AI News & Commentary | Wes Roth, AI Explained, Two Minute Papers | Atomic ✅ |
| AI Creative Tools | Midjourney, Stable Diffusion, Runway, Sora, Kling tutorials | Atomic ✅. Merged Art/Image Gen + Video/Music Production — tools are converging, creators increasingly cover both |
| AI Coding / Dev Tools | Cursor, Copilot, Devin, coding agent tutorials | Atomic ✅. Massive and growing creator pool. These creators are the MOST likely to pay £8/month |
| AI Automation / Agents | AI Foundations, Liam Ottley, no-code workflow builders | Atomic ✅ |

**Category note:** AI moves fastest of any category — new tools drop weekly. 12h scan catches announcements before most creators. 40+ dedicated AI TikTokers, 100+ AI YouTubers tracked. Art/Image Gen and Video/Music Production were merged into AI Creative Tools because the tools are converging (Midjourney does images AND video now). This freed a slot for AI Coding / Dev Tools — the highest-paying AI demographic.

**Platform data:** AI SaaS market reached $71.54B in 2024, projected $775.44B by 2031. Not yet formally categorised by HypeAuditor/Modash (too new as a distinct influencer category).

**Dupe/derivative mode:** "I tried [new tool]" is the entire content mode. Peak TrendPuppy value.

---

### 4. BEAUTY — Score: 18/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Makeup Tutorials | Step-by-step makeup accounts | Atomic ✅ |
| Skincare Routines | Dedicated skincare accounts, ingredient-focused | Atomic ✅ |
| Haircare | Hair-specific accounts — styling, treatment, product reviews | Atomic ✅ |
| Budget / Dupes | Dupe-finding accounts, drugstore alternatives | Atomic ✅. Peak actionability. "Dupe" is literally a beauty term |
| Men's Grooming | Beard care, men's skincare, men's haircare accounts | Atomic ✅. Balances Beauty with a male-skewing sub, same logic as Fashion gender split. Replaces Fragrance (too narrow, collector-oriented) |

**Category note:** Most-discussed industry on TikTok. Strongest dupe culture of any niche — "dupe" originated here.

**Platform data:** HypeAuditor: Beauty = 7.63–8.35% of IG influencers (3rd largest). 4.00% IG ER. Napolify: Beauty TikTok ER 2.46%. TikTok Shop: Beauty/skincare conversion rates reach 7% for viral products. Beauty influencers earn avg $60/hour — highest per HypeAuditor survey. 32% rise in brand collaborations vs 2023.

**Dupe/derivative mode:** "I found the $5 dupe for this $50 product" — peak derivative. The entire Budget/Dupes sub IS the derivative mode.

---

### 5. TECH — Score: 17/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Smartphones | Phone review channels, comparison accounts | Atomic ✅ |
| Laptops & Desktop Reviews | Laptop/PC/Mac review channels | Atomic ✅. Platform-agnostic — sub queries search for both PC and Mac content |
| Audio / Headphones | Headphone, speaker, audio gear review accounts | Atomic ✅. Distinct enthusiast community |
| Apps / Software | App review, productivity software accounts | Atomic ✅. Periscope value: surfaces some AI-adjacent tools |
| Wearables / Smart Home | Smartwatch, home automation, IoT accounts | Atomic ✅ |

**Category note:** Gaming was EXCLUDED from Tech — now its own top-level category. This keeps Tech focused on consumer electronics and software.

**Platform data:** HypeAuditor: Technology & Science = 0.6% of IG influencers — low competition = opportunity. Male-skewing audience (58.6% of YouTube is male). Strong purchase influence through reviews.

**Dupe/derivative mode:** "I tested [product] for 30 days" — review-driven derivative. Unboxing format is inherently derivative.

---

### 6. BUSINESS & FINANCE — Score: 15/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Personal Finance / Saving | Budgeting, saving tips, financial literacy accounts | Atomic ✅ |
| Investing | Stocks, crypto, portfolio accounts | Atomic ✅ |
| Side Hustles / Entrepreneurship | Business building, side income, startup accounts | Atomic ✅ |
| Career / Productivity | Job hunting, LinkedIn tips, workplace advice accounts | Atomic ✅ |
| Financial News / Commentary | Market commentary, economic analysis accounts | Atomic ✅ |

**Platform data:** HypeAuditor: Business & Careers = 0.7% of IG influencers — low competition. Napolify: Finance TikTok ER just 0.89% (lowest) but commands premium CPM rates. X (Twitter) is best platform for finance news.

**Dupe/derivative mode:** "I tried this side hustle for a week" — derivative format exists but mix of original and derivative creators.

---

### 7. LIFE HACKERS — Score: 17/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Money Saving / Budget Hacks | Josh Rincon 5M+, cash-stuffing creators | Atomic ✅ |
| CleanTok / Cleaning | Mrs Hinch, Jill Comes Clean 968K, Mama Mila 3M | Atomic ✅. #CleanTok 71B+ views |
| Home Organisation / Decluttering | Stacey Solomon, The Home Edit-style accounts | Atomic ✅ |
| DIY / Home Repair | Mercury Stardust, The Furniture Dr, The Gooch | Atomic ✅. Periscope value: surfaces home/interior trends |
| Life & Productivity Hacks | Armen Adamjan 9.7M, Laug 28M — tips & tricks accounts | Atomic ✅. Captures both everyday hacks and productivity tricks. Distinct from Career/Productivity in B&F which is workplace-focused |

**Category note:** Entire category IS derivative by nature — see hack, make your version. Fills the "practical actionable content" gap without being vague like Lifestyle (which was killed). "General Life Hacks/Productivity" renamed to "Life & Productivity Hacks" for clarity.

**Platform data:** HypeAuditor: Lifestyle = 13.73–14.32% of IG influencers (largest single category). Life Hackers carves out the actionable, derivative subset. TikTok: 1.6x more viral niche content (like CleanTok) vs Instagram Reels.

---

### 8. REACTORS — Score: 16/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Film / TV Reactions | Dedicated movie/show reaction channels | Atomic ✅ |
| Music Reactions | Listening to songs for first time, album reviews | Solves the Music category problem — music consumption isn't actionable, but reactions are ✅ |
| Sports Reactions | Game commentary, highlight reactions | Atomic ✅ |
| Food / Try Reactions | "I tried the viral X", taste tests | Atomic ✅ |
| Celebrity News & Gossip | Perez Hilton, Deux Moi, Spill Sesh, Anna Oop, tea pages | Atomic ✅. Replaces "Drama/Commentary" which was too broad as a search term. "Celebrity news & gossip" returns exactly the right creators |

**Category note:** Reaction is a derivative MODE, not a content type — but it's a big enough mode to be its own top-level. Subs = what they react TO. Absorbs original Music (as Music Reactions), Comedy (via Celebrity News & Gossip), and News reaction content.

**Periscope function:** Reactors is the primary "derived top-level" category (see Category Architecture Note above). Its seeds don't just serve reactor creators — they surface trend data from Music, Sports, Celebrity Culture, Film/TV, and internet culture into TrendPuppy's top-level feed. A Music Reactions seed covering a viral album drop makes that music trend visible to ALL TrendPuppy users, not just those tracking a Music category. This makes Reactors disproportionately valuable for platform-wide trend intelligence.

**Why Music lives here, not as its own category:** Music as a standalone fails the actionability test — you can't hear a song and "make your version" unless you're a musician. Music REACTION channels, however, have massive dedicated creator pools and clear derivative paths. Labels pay DANCE creators, BEAUTY creators etc. to use songs — the spend flows through other categories. Music trend tracking works better as a cross-cutting FEATURE (trending audio feed) than burning a category slot.

**Platform data:** HypeAuditor: Shows/Entertainment = ~5.4% of IG influencers. Reaction content thrives on YouTube (long-form) and TikTok (short clips). TikTok duets and stitches are native reaction formats.

**Bounty potential — VERY HIGH:** A brand paying for 200 small reactors to all cover their product = massive value. Low cost per creator, huge aggregate reach, authentic format. This is a bounty goldmine.

---

### 9. FASHION — Score: 15/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Women's Fashion | Outfit inspo, styling, lookbooks, seasonal trend accounts | Atomic ✅. Broad anchor sub for female fashion creators |
| Women's Hauls / Try-Ons | Dedicated haul channels — Shein, ASOS, Zara try-ons | Atomic ✅. Format-specific, highly derivative |
| Women's Thrift / Budget Styling | Charity shop finds, budget outfit, thrift flip accounts | Atomic ✅. Distinct price-point identity and community |
| Men's Fashion / Style | Alex Costa, Tim Dessaint, Real Men Real Style | Atomic ✅. Dedicated men's fashion channels — fits, capsule wardrobes, styling |
| Men's Sneakers / Streetwear | Sneakerhead community, streetwear review accounts | Atomic ✅. Male-dominated subculture with own community and brands |

**Category note:** Fashion splits cleanly by gender — the creator identities, audiences, and brand partnerships are distinct. Women's fashion is the dominant market (majority of brand spend, larger creator pool). 3 women's subs / 2 men's subs reflects this. GRWM/OOTD was absorbed into the broader Women's Fashion sub since most GRWM creators are women's fashion creators using a specific format, not a distinct identity. Trend Recaps dropped — creators overlap with Women's Fashion.

**Platform data:** HypeAuditor: Clothing & Outfits ~5% of IG influencers. Sprout Social: Fashion nano-influencers 14.98% TikTok ER. Napolify: Fashion TikTok ER 2.26%. Fashion ads get 65% more engagement than tech/finance ads on TikTok. Fashion segment projected $920B revenue 2025.

---

### 10. GAMING — Score: 15/20

| Sub | Creator Identity | Action Path | Notes |
|---|---|---|---|
| Game Reviews | SkillUp, Gameranx "Before You Buy", ACG | New game trending → cover it before wave passes | Atomic ✅. "Should I buy this?" channels |
| Gaming Guides / Tutorials | Per-game strategy/build channels | Meta shifts or new game drops → make updated guide | Atomic ✅. "How to get better" channels |
| Streaming / Let's Play | Personality-driven gameplay channels | Popular game → stream it, engage audience | Atomic ✅. "Watch me play" channels — the Twitch/YouTube Live identity |
| Esports / Competitive | Tournament coverage, pro scene analysis | Esports event or meta change → analyse/report | Atomic ✅. Pro scene, competitive analysis — distinct from casual gaming |
| Gaming Clips | Clip compilation accounts, viral moment pages | Viral moment happens → clip it, compile, share | Atomic ✅. Accounts whose entire identity is posting gaming moments. Fastest trend sensor in gaming |

**Category note — Format-Based Subs Solve The Atomic Problem:** Gaming was originally parked because game-genre subs (PC, Console, Mobile, FPS, RPG) fail the atomic test catastrophically — each breaks down further. The breakthrough was structuring subs around creator FUNCTION, not game type. This mirrors how Fashion was saved (format-based subs like Hauls/GRWM, not style-based like Streetwear/High End). Seeds track the META of gaming — which games are having a moment, which clips are going viral — not individual game titles.

**Twitch ecosystem insight — Gamers already pay for trend tools:** Streamers already use analytics platforms like SullyGnome, Streams Charts, TwitchTracker, and TwitchMetrics to identify trending games and optimise content strategy. The core pain point is "what should I stream/cover right now?" TrendPuppy offers the same trend intelligence but from TikTok/IG/YouTube angles, where gaming short-form content now lives. £8/month is an easy sell to creators already paying for Twitch analytics tools.

**Replaced Dance because:** TrendPuppy is a paid product with no free tier. Dance demographic (16-22, low income, inconsistent monetisation) won't convert at £8/month. Gaming demographic is older, already pays for SaaS tools, and has a clear action path from trend data to content.

**Platform data:** Napolify: Gaming TikTok ER 2.19%, IG ER 3.15%. Gaming = 11.9% of brand influencer strategies (2nd highest). Twitch: 2.55M avg concurrent viewers, 7.4M monthly active streamers.

---

### 11. HEALTH & WELLNESS — Score: 14/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Supplements / Biohacking | "I tried X for 30 days" accounts, Bryan Johnson crowd | Atomic ✅ |
| Mental Health Tips | ADHD hacks, anxiety management accounts | NOT meditation — actionable mental health tips that trend ✅ |
| Longevity / Anti-Aging | Biohacking, age-reversal, longevity protocols | Growing niche, distinct from general fitness ✅ |
| Nutrition Science | Gut health, microbiome, evidence-based nutrition | Distinct from Food/Cooking — these are science accounts, not recipe accounts ✅ |
| Women's Health | Hormone coaches, fertility journey accounts, menopause advocates | Atomic ✅. Replaces "30-Day Challenges" which failed atomic test (no creator's entire channel IS challenges). Distinct from Women's Fitness (under Fitness) — this is medical/hormonal, not training-focused |

**Category note:** Original subs included Meditation/Mindfulness and Sleep — both rejected as too slow-burn for 12h trend scanning. "30-Day Challenges" replaced by Women's Health — challenges are a content FORMAT, not a creator identity. Women's Health is distinct from Women's Fitness under Fitness: one is medical/hormonal, the other is training-focused.

**Platform data:** HypeAuditor 2025: Medicine, healthy food, and medical education are the fastest-growing Instagram niches. Uscreen: Yoga & Wellness creators earn avg $8,300/month (2nd highest). Global wellness market projected $7T by 2025.

---

### 12. TRAVEL — Score: 14/20

| Sub | Creator Identity | Notes |
|---|---|---|
| Budget Travel Tips | "How I flew to X for £50" accounts | Location-independent, actionable ✅ |
| City Guides | City-specific exploration and guide channels | Atomic ✅. Replaces "Hidden Gems/City Guides" — "City Guides" is how these creators actually identify. Searchable, clear |
| Travel Hacks | Packing, booking, airport tips — not destination-dependent | Location-independent, actionable ✅ |
| Solo / Digital Nomad | Solo travel and remote work lifestyle accounts | Growing niche, distinct identity ✅ |
| Adventure / Outdoor | Hiking, camping, extreme travel accounts | Atomic ✅ |

**Category note:** Actionability works ONLY with format-based subs. Destination-based subs (Europe, Asia) were rejected. "Hidden Gems" replaced by "City Guides" — hidden gems is a content angle, not a creator identity. "City guide creator" is what these creators actually call themselves.

**Platform data:** Napolify: Travel TikTok ER 3.21% — highest average of any category. YouTube: Travel ER 1.83% (highest). 60% of consumers rate travel content most useful for purchase decisions. Estimated 40M digital nomads worldwide. 50% of Gen Z follow travel influencers.

---

## Cross-Cutting: "Dupe/Derivative" as a Content Mode

This is NOT a category — it's a sub-mode within every category. TrendPuppy's core user is a creator who operates in derivative mode.

| Tier | Categories | Why |
|---|---|---|
| Tier 1 — Peak dupe | Beauty, Food, AI, Reactors, Fashion, Life Hackers | The entire creator behaviour IS derivative |
| Tier 2 — Strong derivative | Fitness, Business & Finance, Tech, Gaming | Mix of original and derivative creators. Gaming: see trending game → cover it, see drama → react |
| Tier 3 — Derivative exists but weaker | Health & Wellness, Travel | More original creation, derivative path is narrower |

**Product implication:** Consider surfacing "most duped/recreated" content as a metric — not just "what's trending" but "what are people copying most right now."

---

## Brand-Spend Analysis for Bounties Platform

### Brand Spend by Category (2025 Data)

| Category | Brand Spend Signal | Alignment |
|---|---|---|
| **Fashion & Beauty** | #1 spending vertical. 21.6% of brands use as core strategy. SHEIN had 37,500 TikTok mentions. | 🟢 Perfect — Beauty + Fashion |
| **Food & Beverage** | 3% TikTok ER (highest). Cooking recipes lead global preferences at 51%. | 🟢 Perfect — Food & Cooking |
| **Fitness & Sports** | DTC fitness brands allocate 25-40% of marketing to influencer. | 🟢 Perfect — Fitness |
| **Tech & Gaming** | Gaming 11.9% of brand strategies (2nd highest). | 🟢 Perfect — Tech ✅, Gaming ✅ |
| **Health & Wellness** | Fastest-growing per HypeAuditor. Supplement brands booming. | 🟢 Perfect — Health & Wellness |
| **Travel** | 60% of consumers rate travel content most useful for purchases. | 🟢 Perfect — Travel |
| **Home / Cleaning / DIY** | CleanTok 71B+ views. Strong affiliate potential. | 🟢 Perfect — Life Hackers |
| **Reaction / UGC** | Brands want authentic reactions at scale. 200 small reactors = massive social proof. | 🟢 HIGH — Reactors |

### Bounty Priority

| # | Category | Brand Spend | Bounty Potential |
|---|---|---|---|
| 1 | Beauty | 🟢🟢🟢🟢🟢 | Highest — product seeding, reviews, tutorials |
| 2 | Food & Cooking | 🟢🟢🟢🟢 | Very high — recipe integration, product features |
| 3 | Fashion | 🟢🟢🟢🟢🟢 | Very high — hauls, try-ons, styling with products |
| 4 | Reactors | 🟢🟢🟢🟢 | **VERY HIGH** — 200 reactors covering one product = goldmine |
| 5 | Fitness | 🟢🟢🟢🟢 | High — supplement, gear, app partnerships |
| 6 | Tech | 🟢🟢🟢🟢 | High — product reviews, unboxings |
| 7 | Life Hackers | 🟢🟢🟢 | High — cleaning products, home products, Amazon finds |
| 8 | Gaming | 🟢🟢🟢🟢 | High — game studios, hardware, peripherals, energy drinks |
| 9 | Health & Wellness | 🟢🟢🟢 | Growing — supplements, wellness brands, apps |
| 10 | Travel | 🟢🟢🟢 | High — tourism boards, booking platforms, gear |
| 11 | Business & Finance | 🟢🟢 | Medium — fintech apps, course creators, banks |
| 12 | AI | 🟢🟢 | Growing — AI tool companies, SaaS |

---

## Quantified Platform Data: Sources & Key Metrics

### HypeAuditor — Instagram Influencer Distribution (2023–2025)

- **Lifestyle:** 13.73–14.32% of IG influencers (largest category — we deliberately excluded this as too vague)
- **Music:** 8.50% (covered via Reactors → Music Reactions periscope)
- **Beauty:** 7.63–8.35% (Category 4 ✅)
- **Family:** 5.74% (evaluated, rejected — weak atomic structure, slow trends)
- **Shows/Entertainment:** 5.37–5.49% (covered via Reactors periscope)
- **Fitness & Gym:** 3.16% (Category 1 ✅)
- **Clothing & Outfits:** ~5% (Category 9: Fashion ✅)
- **Business & Careers:** 0.7% (Category 6 ✅ — low competition = opportunity)
- **Technology & Science:** 0.6% (Category 5: Tech ✅ — low competition = opportunity)

Engagement rates by category (IG): Winter Sports 5.46%, Extreme Sports 4.12%, Beauty 4.00%, Family 3.89%, Photography 3.21%, Shows 3.08%

### TikTok Engagement Rates by Niche (2024–2025)

- **Food & Drink (nano):** 18.36% — highest of any category (Sprout Social)
- **Fashion (nano):** 14.98% (Sprout Social)
- **Fitness (nano):** 14.61% (Sprout Social)
- **Travel (avg):** 3.21% — highest average ER (Napolify)
- **Beauty (avg):** 2.46% (Napolify)
- **Fashion (avg):** 2.26% (Napolify)
- **Gaming (avg):** 2.19% TikTok, 3.15% Instagram (Napolify)
- **Finance (avg):** 0.89% — lowest, but premium CPM (Napolify)
- **Platform average:** 4–5% overall. Nano-influencers: 10.3% (HypeAuditor). Declining from 5.77% (2023) to 4.64% (2024).

### YouTube Category Data (HypeAuditor 2025)

- **Top categories:** Music & Dance (16.5%), Animation (16.2%)
- **Creator distribution:** 69.4% are nano-influencers, 85.2% of channels average <10K views
- **Audience:** 64% aged 18–34, 58.6% male

### Creator Economy Income Data

- **Fitness creators:** $11,900/month avg (Uscreen — highest)
- **Yoga & Wellness:** $8,300/month avg (Uscreen)
- **Beauty influencers:** $60/hour avg (HypeAuditor survey — highest hourly)
- **Avg creator 10K–50K followers:** $378 per sponsored TikTok post
- **Overall:** >50% of creators earn <$15K/year. Only ~5% earn >$100K/year.

### Industry Market Sizing

- **Creator economy:** $250B (2024), projected $480–500B by 2027 (Goldman Sachs/Uscreen)
- **Influencer marketing:** $19.8B (2024), projected $31.2B by 2027 (HypeAuditor)
- **AI SaaS market:** $71.54B (2024), projected $775.44B by 2031
- **Fashion segment:** Projected $920.19B revenue 2025
- **Global wellness market:** Projected $7T by 2025
- **TikTok global revenue:** $15.4B (2025), up from $12.1B (2024)

---

## Categories We Considered and Cut (with full sub breakdowns)

### LIFESTYLE / VLOGGERS — KILLED

**Why explored:** HypeAuditor's #1 category at 14.3% of Instagram influencers.

| Proposed Sub | Why It Failed |
|---|---|
| Day in the Life | Format, not identity — everyone does DITL occasionally, nobody's entire channel IS DITL |
| Shopping / Hauls | Overlaps Fashion (Hauls sub) directly |
| Exploring / Adventures | Overlaps Travel (Adventure sub) |
| Productivity / Routines | Overlaps Business & Finance (Career / Productivity sub) |
| Moving / Home Setup | Life event, not a niche — you move once, content ends |
| Personality / Entertainment | Not searchable — "personality creator" isn't a thing you search for |

**Conclusion:** Catch-all bucket, not a real niche. Every sub overlaps existing categories. KILLED.

---

### MUSIC — REJECTED AS CATEGORY

**Why explored:** 8.5% of Instagram influencers. Labels spend on promotion.

| Proposed Sub | Why It Failed |
|---|---|
| Hip Hop | Not actionable — genre isn't an atomic creator identity for derivative content |
| Pop | Same — you hear pop and then what? |
| Rock / Alternative | Same problem |
| Electronic / DJ | Marginally better — DJ sets are derivable, but very narrow |
| Music Production | Only serves music producers. Very narrow audience |

**Research found:** Dedicated music review creators exist (Anthony Fantano 3.1M, Dead End Hip Hop, MalloryBros 351K). But these overlap Reactors → Music Reactions sub.

**Where it lives now:** Music Reactions sub under Reactors. Trending audio = cross-cutting feature.

---

### COMEDY — REJECTED AS CATEGORY

| Proposed Sub | Why It Failed |
|---|---|
| Skits | Breaks further — street interviews, scripted bits, improv, character comedy |
| Stand Up | Very personal — can't see stand-up and "make your version" |
| Pranks | Format-specific, overlaps Reactors |
| Commentary | Now lives under Reactors → Celebrity News & Gossip |

**Conclusion:** Low derivative potential (2/5). Actionable formats absorbed by Reactors.

---

### NEWS — REJECTED AS CATEGORY

| Proposed Sub | Why It Failed |
|---|---|
| World News | 12h scan fatally too slow. News moves in minutes. |
| Finance / Markets | Already in Business & Finance → Financial News |
| Tech News | Already in Tech + AI categories |
| Pop Culture | Overlaps Reactors → Celebrity News & Gossip |
| Sports | Overlaps Reactors → Sports Reactions |

**Conclusion:** 12h scan cycle kills this. By scan time, news is old.

---

### GAMING — PROMOTED TO FINAL 12 (Replaced Dance)

Originally parked due to atomic test failure with game-genre subs. Promoted after discovering format-based sub structure (Reviews, Guides, Streaming, Esports, Clips) solves the atomic problem. Key insight came from Twitch ecosystem research — streamers already pay for trend-tracking tools like SullyGnome and Streams Charts.

**Original failed subs (game-genre approach):**

| Proposed Sub | Why It Failed |
|---|---|
| PC Gaming | Breaks into FPS, RPG, strategy, simulation... |
| Console | Breaks into PlayStation, Xbox, Nintendo... |
| Mobile | Breaks into casual, competitive, specific titles... |
| Esports | Breaks into specific games: Valorant, CS2, League... |
| Retro / Speedrunning | Niche within niche |

**Working subs (format-based approach):** Game Reviews, Gaming Guides/Tutorials, Streaming/Let's Play, Esports/Competitive, Gaming Clips. See Category 10 for full breakdown.

---

### DANCE — REPLACED BY GAMING

Dance had strong atomic subs (Hip-Hop/Street, Contemporary, Challenges, Tutorials, K-Pop) and genuine 12h scan value — dance trends peak in 48-72 hours. However, TrendPuppy is a paid product with no free tier, and Dance's core demographic (16-22 year olds, inconsistent income, 58% struggling to monetise) won't convert at £8/month.

**The data that killed Dance:**
- 52.83% of TikTok creators aged 18-24; dance skews younger (16-22)
- Only 1/3 of TikTok influencers earn full-time income
- 68% of creators unsatisfied with income
- Comparison: Beauty/Fitness/AI creators treat content as a business and pay for tools. A 19-year-old dance TikToker does not.

**Dance could return if:** TrendPuppy introduces a free tier or lower price point aimed at younger demographics.

---

### PARENTING & FAMILY — EVALUATED AS DANCE REPLACEMENT, REJECTED

| Proposed Sub | Status |
|---|---|
| Family Vlogs / Comedy | ✅ Works — The Kabs Family, FV Family |
| Parenting Tips / Education | ✅ Works — Dr. Becky Kennedy, AlyPain, Kim Muench |
| Product Reviews / Hauls | ⚠️ Blends with general parenting, not standalone |
| Special Needs / Neurodivergent | ⚠️ Identity but not trend-driven — slow content velocity |
| Baby / Toddler | ❌ Life-stage based — seeds churn as kids age |

Right paying demographic (28-40) but scored 11/20. Slow trend velocity. 12h scan adds little value. 4.2M mom influencers, 7.30% TikTok ER but weak product-market fit.

---

### LUXURY LIFESTYLE — EVALUATED AS DANCE REPLACEMENT, REJECTED

| Proposed Sub | Why It Failed |
|---|---|
| Luxury Cars / Supercars | Dedicated accounts exist, but zero derivative potential for average creator |
| Luxury Travel / Hotels | Overlaps Travel category directly |
| Luxury Fashion / Designer | Overlaps Fashion category directly |
| Luxury Watches / Jewellery | Niche community but aspirational, not actionable |
| Luxury Real Estate / Homes | Extremely narrow creator pool |

**Three fatal problems:** (1) Overlap hell — every sub bleeds into existing categories. (2) Low derivative potential (1/5) — aspirational content, can't "make your version." (3) Product-market fit failure — luxury creators set trends, they don't chase them.

---

### CARS / AUTOMOTIVE — EVALUATED AS DANCE REPLACEMENT, NOT SELECTED

Scored 14/20. Clean atomic subs (Car Reviews, Car Mods/Builds, Detailing, Driving Content, EVs). Right demographic (22-40, disposable income). But actionability limited — mod/build trends don't spike in 48h. Lower priority than Gaming which has proven tool-paying behaviour.

---

### PETS & ANIMALS — REJECTED

Popular to watch (4/5), impossible to derive (1/5). You need the animal. Fundamental derivative test fails at category level.

---

### COUPLES — REJECTED

Too narrow, too personal, requires a partner, low derivative potential.

---

### BOOKTOK — PASSED

35M+ videos but low derivative potential (can't "dupe" a book review) and slow trend velocity. 12h scan adds minimal value.

---

### DIY / CRAFTS — PARTIALLY ABSORBED

Trend velocity too slow. Crochet patterns don't spike in 48h. Actionable subset lives in Life Hackers → DIY/Home Repair.

---

### EDUCATION / UPSKILLING — PASSED

Too fragmented. A maths teacher and a language teacher have nothing in common. No coherent atomic structure.

---

### HOME DECOR / INTERIOR DESIGN — PASSED

Seasonal trend velocity (not daily). Overlaps Life Hackers DIY sub.

---

### SELF-IMPROVEMENT / MOTIVATION — ABSORBED

Overlaps B&F (productivity), H&W (mental health), Fitness (discipline). No unique atomic space.

---

## Coverage Analysis: What TrendPuppy's 12 Categories Cover

Mapping the Final 12 against HypeAuditor's Instagram influencer distribution shows TrendPuppy covers approximately 70–80% of the creator economy by brand spend, and all major influencer categories either directly or via the Reactors periscope mechanism.

**Direct coverage:** Beauty (7.63–8.35%), Fashion/Clothing (~5%), Fitness (3.16%), Food, Tech (0.6%), Business (0.7%), Health/Wellness (growing), Travel, AI (emerging), Life Hackers (practical subset of Lifestyle 14.32%), Gaming (via format-based approach)

**Periscope coverage via Reactors:** Music (8.50%), Entertainment/Shows (5.37%), Sports, Comedy, Pop Culture

**Deliberately excluded:** Lifestyle (too vague), Parenting (weak PMF), Pets (non-derivative), Education (too fragmented)

**Gender balance:** Female-skewing: Beauty, Fashion, Food, Life Hackers. Male-skewing: Tech, Gaming, Business/Finance. Mixed: Fitness, AI, Reactors, Health & Wellness, Travel. Net: slight female skew in paying user base — worth knowing for marketing.

**Age range:** TBD. Probably male with disposable income, maybe post-uni so 22+?

---

## Summary Table (Full Subcategory Breakdown)

| # | Category | Score | Sub 1 | Sub 2 | Sub 3 | Sub 4 | Sub 5 | Brand Spend |
|---|---|---|---|---|---|---|---|---|
| 1 | Fitness | 19 | Calisthenics | Science-Based Training | Powerlifting / Strength | Women's Fitness | Yoga / Mobility | 🟢🟢🟢🟢 |
| 2 | Food & Cooking | 19 | Quick Recipes | Protein / Macros | Healthy / Diet | Restaurant Reviews | Street Food | 🟢🟢🟢🟢 |
| 3 | AI | 19 | Tools & Reviews | News & Commentary | AI Creative Tools | AI Coding / Dev Tools | Automation / Agents | 🟢🟢 |
| 4 | Beauty | 18 | Makeup Tutorials | Skincare Routines | Haircare | Budget / Dupes | Men's Grooming | 🟢🟢🟢🟢🟢 |
| 5 | Tech | 17 | Smartphones | Laptops & Desktop Reviews | Audio / Headphones | Apps / Software | Wearables / Smart Home | 🟢🟢🟢🟢 |
| 6 | Business & Finance | 15 | Personal Finance | Investing | Side Hustles | Career / Productivity | Financial News | 🟢🟢 |
| 7 | Life Hackers | 17 | Money Saving | CleanTok / Cleaning | Home Organisation | DIY / Home Repair | Life & Productivity Hacks | 🟢🟢🟢 |
| 8 | Reactors | 16 | Film / TV | Music Reactions | Sports | Food / Try | Celebrity News & Gossip | 🟢🟢🟢🟢 |
| 9 | Fashion | 15 | Women's Fashion | Women's Hauls / Try-Ons | Women's Thrift / Budget | Men's Fashion / Style | Men's Sneakers / Streetwear | 🟢🟢🟢🟢🟢 |
| 10 | Gaming | 15 | Game Reviews | Guides / Tutorials | Streaming / Let's Play | Esports / Competitive | Gaming Clips | 🟢🟢🟢🟢 |
| 11 | Health & Wellness | 14 | Supplements / Biohacking | Mental Health Tips | Longevity / Anti-Aging | Nutrition Science | Women's Health | 🟢🟢🟢 |
| 12 | Travel | 14 | Budget Tips | City Guides | Travel Hacks | Solo / Nomad | Adventure / Outdoor | 🟢🟢🟢 |