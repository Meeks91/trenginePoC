"""
Add LIFE_HACKERS category to all_categories.json.
Insert at position 6 (after BUSINESS_AND_FINANCE) to maintain the master list order.
"""

import json

path = "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories/all_categories.json"

with open(path) as f:
    categories = json.load(f)

life_hackers = {
    "category": "LIFE_HACKERS",
    "subs": [
        {
            "subName": "Life Hackers",
            "isTopLevel": True,
            "searchPrompt": "top life hack influencers",
            "altSearchTerms": [
                "best hack creators",
                "favorite life tips accounts"
            ],
            "knownSources": [
                "favikon.com",
                "amraandelma.com",
                "feedspot.com",
                "socialbook.io",
                "lifehacker.com",
                "theinfluenceagency.com",
                "izea.com",
                "collabstr.com",
                "modash.io",
                "thesocialshepherd.com"
            ],
            "platformNotes": "TikTok dominates — quick-format tips and hacks go viral fastest. YouTube for longer 'hack compilation' formats.",
            "regionNotes": "Both UK and US return rich results. Product availability for hacks differs by region.",
            "difficulty": "Easy"
        },
        {
            "subName": "Money Saving / Budget Hacks",
            "isTopLevel": False,
            "searchPrompt": "best money saving tip creators",
            "altSearchTerms": [
                "top cash stuffing influencers",
                "budget hack accounts"
            ],
            "knownSources": [
                "reddit.com/r/Frugal",
                "reddit.com/r/povertyfinance",
                "favikon.com",
                "feedspot.com",
                "amraandelma.com",
                "collabstr.com",
                "theinfluenceagency.com"
            ],
            "platformNotes": "TikTok is the absolute king of quick money-saving tips. YouTube for full budget breakdowns and 'no spend' challenges.",
            "regionNotes": "Currency, tax systems, and store availability are strictly regional. Region essential.",
            "difficulty": "Easy"
        },
        {
            "subName": "CleanTok / Cleaning",
            "isTopLevel": False,
            "searchPrompt": "top CleanTok creators",
            "altSearchTerms": [
                "best cleaning influencers",
                "favorite cleaning hack accounts"
            ],
            "knownSources": [
                "socialbook.io",
                "favikon.com",
                "garfieldbrooklyn.com",
                "lifehacker.com",
                "amraandelma.com",
                "theinfluenceagency.com",
                "izea.com",
                "reddit.com/r/CleaningTips"
            ],
            "platformNotes": "TikTok is THE platform for CleanTok (#CleanTok 71B+ views). Instagram for aesthetic 'before and after' content.",
            "regionNotes": "Cleaning products and brands differ massively by region (e.g. Mrs Hinch UK vs. Go Clean Co US). Region important.",
            "difficulty": "Easy"
        },
        {
            "subName": "Home Organisation / Decluttering",
            "isTopLevel": False,
            "searchPrompt": "best home organization influencers",
            "altSearchTerms": [
                "top decluttering creators",
                "favorite pantry organization accounts"
            ],
            "knownSources": [
                "feedspot.com",
                "favikon.com",
                "hellomagazine.com",
                "amraandelma.com",
                "izea.com",
                "reddit.com/r/declutter",
                "reddit.com/r/organization"
            ],
            "platformNotes": "Instagram and TikTok dominate for satisfying 'before and after' transformations. YouTube for full room makeovers.",
            "regionNotes": "Storage products (IKEA, Target, etc.) are region-specific. Both UK and US return well.",
            "difficulty": "Easy"
        },
        {
            "subName": "DIY / Home Repair",
            "isTopLevel": False,
            "searchPrompt": "top DIY home repair creators",
            "altSearchTerms": [
                "best home renovation influencers",
                "favorite handyman accounts"
            ],
            "knownSources": [
                "influencer-hero.com",
                "beacons.ai",
                "cheapism.com",
                "slashgear.com",
                "izea.com",
                "feedspot.com",
                "reddit.com/r/DIY",
                "reddit.com/r/HomeImprovement"
            ],
            "platformNotes": "YouTube dominates for long-form tutorials. TikTok for quick before-and-after transformation clips.",
            "regionNotes": "Building codes, electrical standards, and hardware stores are entirely region-locked. Region essential.",
            "difficulty": "Medium"
        },
        {
            "subName": "Life & Productivity Hacks",
            "isTopLevel": False,
            "searchPrompt": "best productivity hack creators",
            "altSearchTerms": [
                "top everyday tips influencers",
                "life hack accounts"
            ],
            "knownSources": [
                "favikon.com",
                "amraandelma.com",
                "feedspot.com",
                "hireharbour.com",
                "reddit.com/r/LifeProTips",
                "reddit.com/r/productivity",
                "sproutsocial.com"
            ],
            "platformNotes": "TikTok for viral quick tips. YouTube for structured productivity systems and morning routines.",
            "regionNotes": "Productivity tools and apps can be region-specific. Both UK and US return well.",
            "difficulty": "Easy"
        }
    ]
}

# Find insert position: after BUSINESS_AND_FINANCE (index 5), making LIFE_HACKERS index 6
cat_names = [c["category"] for c in categories]
print(f"Current order: {cat_names}")

# BUSINESS_AND_FINANCE should be at index 5
biz_idx = cat_names.index("BUSINESS_AND_FINANCE")
print(f"BUSINESS_AND_FINANCE at index {biz_idx}")

# Insert LIFE_HACKERS after it
categories.insert(biz_idx + 1, life_hackers)

# Verify order
cat_names = [c["category"] for c in categories]
print(f"New order: {cat_names}")
print(f"Total categories: {len(categories)}")
total_subs = sum(len(c["subs"]) for c in categories)
print(f"Total subs: {total_subs}")

# Verify no templates
for cat in categories:
    for sub in cat["subs"]:
        for field in ["searchPrompt"] + sub["altSearchTerms"]:
            assert "{platform}" not in field, f"Template in {sub['subName']}"
            assert "{region}" not in field, f"Template in {sub['subName']}"
            assert "{year}" not in field, f"Template in {sub['subName']}"

# Write
with open(path, "w") as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

print(f"\n✅ Wrote {path} with {len(categories)} categories, {total_subs} subs")

# Print final order
for i, c in enumerate(categories, 1):
    top = next(s for s in c["subs"] if s.get("isTopLevel"))
    children = [s["subName"] for s in c["subs"] if not s.get("isTopLevel")]
    print(f"  {i:2d}. {c['category']} ({top['subName']}) → {', '.join(children)}")
