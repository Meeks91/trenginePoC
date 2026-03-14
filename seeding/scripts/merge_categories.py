"""
Full merge script v2:
- Reads categories_1-6.md (JSON array — 5 categories)
- Reads catergory7-12.md (separated JSON blocks — now 7 categories with LIFE_HACKERS)
- Merges Gemini's LIFE_HACKERS sources with our research (removing bad ones)
- Strips all {platform}/{region}/{year}/2025 templates
- Removes "Enforced" from regionNotes
- Extracts _removed fields
- Writes all_categories.json + _removed_sources.md
"""

import json
import re
import os

DOCS_DIR = "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories"

# Bad sources we've already validated and rejected
BAD_SOURCES = {
    "starngage.pro", "koldigital.sg", "bookingagentinfo.com", "videogamenarratives.wordpress.com",
    "beatstorapon.com", "300mind.studio", "oklabeef.org", "hearst.co.jp", "painnewsnetwork.org",
    "canadabeef.ca", "lifeboat.com", "geh.ucsd.edu", "pmc.ncbi.nlm.nih.gov",
    "marketech-apac.com", "blog.adobe.com", "gladucame.in", "trendvisionz.com",
    "affistash.com", "houseofmedics.org", "thehbgc.com", "eezycollab.com", "embold.co",
    "smarthealthclubs.com", "prenuvo.com", "listenfirstmedia.com", "tandfonline.com",
    "bacp.co.uk", "longevity.foundation", "sambadigital.com", "thisisafk.com",
    "cookies.digital", "influencers.club", "stormy.ai", "filmora.wondershare.com",
    "issuu.com/amansw.com.au", "issuu.com/kclove78",
}

# Our researched LIFE_HACKERS data (complete 6 subs)
LIFE_HACKERS_FULL = {
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
                "thesocialshepherd.com",
                "influencermatchmaker.co.uk",
                "socialchamp.com"
            ],
            "platformNotes": "TikTok dominates for short-form, rapid-fire hacks. YouTube is better for long-form 'testing viral hacks' videos.",
            "regionNotes": "Life hacks often depend on regionally available products or store chains. Both UK and US return well.",
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

# ── Load categories 1-5 ──
with open(os.path.join(DOCS_DIR, "categories_1-6.md")) as f:
    cats_1_5 = json.loads(f.read())

print(f"Loaded {len(cats_1_5)} categories from categories_1-6.md")

# ── Load categories 7-12 (+ Gemini's LIFE_HACKERS) ──
with open(os.path.join(DOCS_DIR, "catergory7-12.md")) as f:
    raw = f.read()

# Split on separator lines OR bare JSON boundaries (}  {)
blocks = re.split(r'\n\s*={3,}\s*\n|\n\}\s*\n\s*\{', raw)
cats_7_12_raw = []

for i, block in enumerate(blocks):
    block = block.strip()
    if not block:
        continue
    # Re-add braces that were consumed by the split
    if not block.startswith('{'):
        block = '{' + block
    if not block.endswith('}'):
        block = block + '}'
    try:
        obj = json.loads(block)
        cats_7_12_raw.append(obj)
    except json.JSONDecodeError as e:
        print(f"⚠️  Failed to parse block {i}: {block[:80]}...")
        print(f"   Error: {e}")

print(f"Loaded {len(cats_7_12_raw)} categories from catergory7-12.md")
for c in cats_7_12_raw:
    print(f"  - {c['category']} ({len(c['subs'])} subs)")

# ── Replace Gemini's LIFE_HACKERS with our merged version ──
cats_7_12 = []
for cat in cats_7_12_raw:
    if cat["category"] == "LIFE_HACKERS":
        print(f"\n  Replacing Gemini's LIFE_HACKERS ({len(cat['subs'])} subs) with our researched version ({len(LIFE_HACKERS_FULL['subs'])} subs)")

        # Merge any unique sources from Gemini that aren't bad
        gemini_sources = set()
        for sub in cat["subs"]:
            gemini_sources.update(sub.get("knownSources", []))
        our_sources = set()
        for sub in LIFE_HACKERS_FULL["subs"]:
            our_sources.update(sub["knownSources"])

        new_from_gemini = gemini_sources - our_sources - BAD_SOURCES
        if new_from_gemini:
            print(f"  Merged {len(new_from_gemini)} valid sources from Gemini: {new_from_gemini}")
            # Add to top-level sub
            LIFE_HACKERS_FULL["subs"][0]["knownSources"].extend(sorted(new_from_gemini))

        removed_from_gemini = gemini_sources & BAD_SOURCES
        if removed_from_gemini:
            print(f"  Removed {len(removed_from_gemini)} bad Gemini sources: {removed_from_gemini}")

        cats_7_12.append(LIFE_HACKERS_FULL)
    else:
        cats_7_12.append(cat)

# ── Merge all ──
all_categories = cats_1_5 + cats_7_12
print(f"\nMerged: {len(all_categories)} categories")

# ── Reorder to match master list ──
MASTER_ORDER = [
    "FITNESS", "FOOD_AND_COOKING", "AI", "BEAUTY", "TECH",
    "BUSINESS_AND_FINANCE", "LIFE_HACKERS", "REACTORS",
    "FASHION", "GAMING", "HEALTH_AND_WELLNESS", "TRAVEL"
]

cat_map = {c["category"]: c for c in all_categories}
missing = [k for k in MASTER_ORDER if k not in cat_map]
extra = [c["category"] for c in all_categories if c["category"] not in MASTER_ORDER]
if missing:
    print(f"⚠️  Missing from master order: {missing}")
if extra:
    print(f"⚠️  Extra categories not in master order: {extra}")

all_categories = [cat_map[k] for k in MASTER_ORDER if k in cat_map]

# ── Strip templates ──
TEMPLATE_PATTERN = re.compile(r'\s*\{(?:platform|region|year)\}', re.IGNORECASE)
YEAR_PATTERN = re.compile(r'\s+2025\s*$')

strips = 0
for cat in all_categories:
    for sub in cat["subs"]:
        original = sub["searchPrompt"]
        cleaned = TEMPLATE_PATTERN.sub("", original)
        cleaned = YEAR_PATTERN.sub("", cleaned).strip()
        if cleaned != original:
            strips += 1
        sub["searchPrompt"] = cleaned

        new_alts = []
        for alt in sub["altSearchTerms"]:
            c = TEMPLATE_PATTERN.sub("", alt)
            c = YEAR_PATTERN.sub("", c).strip()
            if c != alt:
                strips += 1
            new_alts.append(c)
        sub["altSearchTerms"] = new_alts

print(f"Stripped {strips} template tokens")

# ── Clean "Enforced" from regionNotes ──
enforced_fixes = 0
for cat in all_categories:
    for sub in cat["subs"]:
        if "Enforced" in sub.get("regionNotes", ""):
            old = sub["regionNotes"]
            sub["regionNotes"] = re.sub(r'Enforced\.?\s*', '', old).strip()
            enforced_fixes += 1

print(f"Cleaned {enforced_fixes} 'Enforced' from regionNotes")

# ── Extract _removed fields ──
removed_entries = []
for cat in all_categories:
    for sub in cat["subs"]:
        if "_removed" in sub:
            removed_entries.append({
                "category": cat["category"],
                "sub": sub["subName"],
                "removed": sub["_removed"],
            })
            del sub["_removed"]

print(f"Extracted {len(removed_entries)} _removed entries")

# ── Write all_categories.json ──
output_path = os.path.join(DOCS_DIR, "all_categories.json")
with open(output_path, "w") as f:
    json.dump(all_categories, f, indent=2, ensure_ascii=False)
print(f"\n✅ Wrote {output_path}")

# ── Write _removed_sources.md ──
removed_path = os.path.join(DOCS_DIR, "_removed_sources.md")
with open(removed_path, "w") as f:
    f.write("# Removed Sources Audit Trail\n\n")
    f.write("Sources removed during validation — documented for reference.\n\n")
    f.write("| Category | Sub | Removed Sources |\n")
    f.write("|---|---|---|\n")
    for entry in removed_entries:
        f.write(f"| {entry['category']} | {entry['sub']} | {entry['removed']} |\n")
print(f"✅ Wrote {removed_path}")

# ── Verify ──
with open(output_path) as f:
    verify = json.load(f)

total_subs = sum(len(c["subs"]) for c in verify)

for cat in verify:
    for sub in cat["subs"]:
        for field_val in [sub["searchPrompt"]] + sub["altSearchTerms"]:
            assert "{platform}" not in field_val, f"Template in {sub['subName']}: {field_val}"
            assert "{region}" not in field_val, f"Template in {sub['subName']}: {field_val}"
            assert "{year}" not in field_val, f"Template in {sub['subName']}: {field_val}"
        assert "_removed" not in sub, f"_removed still in {sub['subName']}"
        assert "Enforced" not in sub.get("regionNotes", ""), f"Enforced in {sub['subName']}"
        for src in sub["knownSources"]:
            assert src not in BAD_SOURCES, f"Bad source {src} still in {sub['subName']}"

print(f"\n✅ Verification passed: {len(verify)} categories, {total_subs} subs")
print(f"   0 templates, 0 _removed fields, 0 Enforced, 0 bad sources")

print("\nFinal category order:")
for i, c in enumerate(verify, 1):
    top = next(s for s in c["subs"] if s.get("isTopLevel"))
    children = [s["subName"] for s in c["subs"] if not s.get("isTopLevel")]
    print(f"  {i:2d}. {c['category']} ({top['subName']}) → {', '.join(children)}")
