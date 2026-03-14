"""
Post-validation cleanup:
1. Remove bad Gemini sources from LIFE_HACKERS
2. Add new sources to weak categories (AI, Business, Reactors)
3. Regenerate all_categories.json
"""
import json

path = "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/seeding/categories/all_categories.json"

with open(path) as f:
    categories = json.load(f)

# Bad Gemini sources to remove from LIFE_HACKERS
BAD_GEMINI = {
    "cremarc.com", "ocedar.com", "ridgid.com", "adsoftheworld.com",
    "bold-awards.com", "storagecafe.com", "apple.com/podcasts",
}

# ── Clean LIFE_HACKERS ──
for cat in categories:
    if cat["category"] == "LIFE_HACKERS":
        removed = []
        for sub in cat["subs"]:
            before = len(sub["knownSources"])
            sub["knownSources"] = [s for s in sub["knownSources"] if s not in BAD_GEMINI]
            diff = before - len(sub["knownSources"])
            if diff:
                removed.append(f"{sub['subName']}: {diff} removed")
        print(f"LIFE_HACKERS cleanup: {removed}")

# ── Strengthen AI Coding / Dev Tools (Hard, 6→more sources) ──
for cat in categories:
    if cat["category"] == "AI":
        for sub in cat["subs"]:
            if sub["subName"] == "AI Coding / Dev Tools":
                new = [
                    "lkiconsulting.io",   # AI influencer lists
                    "analyticsvidhya.com", # ML creator lists (already in AI top)
                    "skimai.com",          # AI creator directory
                    "digitalocean.com",    # AI/ML creator roundups
                ]
                existing = set(sub["knownSources"])
                added = [s for s in new if s not in existing]
                sub["knownSources"].extend(added)
                print(f"AI Coding/Dev: added {len(added)} → {len(sub['knownSources'])} total")

# ── Strengthen Side Hustles / Entrepreneurship (Hard, 4→more sources) ──
for cat in categories:
    if cat["category"] == "BUSINESS_AND_FINANCE":
        for sub in cat["subs"]:
            if sub["subName"] == "Side Hustles / Entrepreneurship":
                new = [
                    "favikon.com",
                    "feedspot.com",
                    "trendyphrase.com",     # side hustle creator lists
                    "collabstr.com",
                    "modash.io",
                    "influencer-hero.com",
                ]
                existing = set(sub["knownSources"])
                added = [s for s in new if s not in existing]
                sub["knownSources"].extend(added)
                print(f"Side Hustles: added {len(added)} → {len(sub['knownSources'])} total")

# ── Strengthen REACTORS overall (add favoree.io — great reactor directory) ──
for cat in categories:
    if cat["category"] == "REACTORS":
        for sub in cat["subs"]:
            new = []
            if sub["subName"] == "Reactors":
                new = ["favoree.io"]
            elif sub["subName"] == "Film / TV Reactions":
                new = ["favoree.io"]
            elif sub["subName"] == "Music Reactions":
                new = ["favoree.io"]
            elif sub["subName"] == "Sports Reactions":
                new = ["favoree.io"]
            if new:
                existing = set(sub["knownSources"])
                added = [s for s in new if s not in existing]
                sub["knownSources"].extend(added)
                if added:
                    print(f"REACTORS/{sub['subName']}: added {added}")

# ── Write ──
with open(path, "w") as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

# Also update the copy in docs/categories
import shutil
shutil.copy(path, "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories/all_categories.json")

# Stats
total_sources = sum(len(s["knownSources"]) for c in categories for s in c["subs"])
print(f"\n✅ Updated: {total_sources} total sources")

# Print weak category stats
for cat in categories:
    if cat["category"] in ("AI", "BUSINESS_AND_FINANCE", "REACTORS", "LIFE_HACKERS"):
        for sub in cat["subs"]:
            print(f"  {cat['category']}/{sub['subName']}: {len(sub['knownSources'])} sources")
