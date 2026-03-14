"""Generate all_categories_table.md from all_categories.json"""
import json

path = "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories/all_categories.json"
out = "/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories/all_categories_table.md"

with open(path) as f:
    categories = json.load(f)

lines = []
lines.append("# All Categories & Subcategories — 72 Subs\n")
lines.append("| # | Category | Sub | Top? | Search Prompt | Alt Terms | Known Sources | Difficulty |")
lines.append("|---|---|---|---|---|---|---|---|")

n = 0
for cat in categories:
    for sub in cat["subs"]:
        n += 1
        alts = "; ".join(sub["altSearchTerms"])
        sources = ", ".join(sub["knownSources"][:5])
        if len(sub["knownSources"]) > 5:
            sources += f" (+{len(sub['knownSources'])-5} more)"
        top = "✅" if sub.get("isTopLevel") else ""
        lines.append(f"| {n} | {cat['category']} | {sub['subName']} | {top} | {sub['searchPrompt']} | {alts} | {sources} | {sub['difficulty']} |")

lines.append(f"\n**Total: {n} subs across {len(categories)} categories**")

# Stats
total_sources = sum(len(s["knownSources"]) for c in categories for s in c["subs"])
difficulties = {}
for c in categories:
    for s in c["subs"]:
        d = s["difficulty"]
        difficulties[d] = difficulties.get(d, 0) + 1

lines.append(f"\n| Stat | Value |")
lines.append(f"|---|---|")
lines.append(f"| Categories | {len(categories)} |")
lines.append(f"| Subs | {n} |")
lines.append(f"| Total Sources | {total_sources} |")
lines.append(f"| Avg Sources/Sub | {total_sources/n:.1f} |")
for d in ["Easy", "Medium", "Hard"]:
    lines.append(f"| {d} Difficulty | {difficulties.get(d, 0)} |")

with open(out, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote {out} with {n} rows")
print(f"   {total_sources} total sources, avg {total_sources/n:.1f}/sub")
print(f"   Difficulty: {difficulties}")
