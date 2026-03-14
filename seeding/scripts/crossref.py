"""
Cross-reference all_categories.json sub names against category_sub_query_investigation.md master list.
"""
import json
import re

# Load our subs
with open("/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/categories/all_categories.json") as f:
    categories = json.load(f)

our_subs = {}
for cat in categories:
    for sub in cat["subs"]:
        key = f"{cat['category']}::{sub['subName']}"
        our_subs[key] = sub

# Load master list
with open("/Users/micahsimmons/Desktop/project millon/TrendPuppy/PoCs/trenginePoc/docs/category_sub_query_investigation.md") as f:
    master_text = f.read()

# Extract sub names from the master list (formatted as numbered sub-items)
# Pattern: lines like "   1. Fitness (top level)" or "   2. Calisthenics"
master_subs = []
current_cat = None
for line in master_text.split("\n"):
    # Category headers like "### 1. FITNESS"
    cat_match = re.match(r'###\s+\d+\.\s+(\S+)', line)
    if cat_match:
        current_cat = cat_match.group(1).upper()
        continue
    # Sub items like "   1. Fitness (top level)"
    sub_match = re.match(r'\s+\d+\.\s+(.+?)(?:\s*\(top.level\))?\s*$', line)
    if sub_match and current_cat:
        sub_name = sub_match.group(1).strip()
        master_subs.append(f"{current_cat}::{sub_name}")

print(f"Our subs: {len(our_subs)}")
print(f"Master subs: {len(master_subs)}")

# Compare
our_names = set(our_subs.keys())
master_names = set(master_subs)

# Normalize for comparison (lowercase, strip punctuation)
def normalize(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

our_normalized = {normalize(k): k for k in our_names}
master_normalized = {normalize(k): k for k in master_names}

matched = 0
unmatched_ours = []
for norm_key, orig_key in our_normalized.items():
    if norm_key in master_normalized:
        matched += 1
    else:
        # Try fuzzy match
        close = [mk for mk, mv in master_normalized.items() if mk[:15] == norm_key[:15]]
        if close:
            print(f"  Fuzzy match: {orig_key} ↔ {master_normalized[close[0]]}")
            matched += 1
        else:
            unmatched_ours.append(orig_key)

unmatched_master = []
for norm_key, orig_key in master_normalized.items():
    if norm_key not in our_normalized:
        close = [ok for ok, ov in our_normalized.items() if ok[:15] == norm_key[:15]]
        if not close:
            unmatched_master.append(orig_key)

print(f"\n✅ Matched: {matched}")
if unmatched_ours:
    print(f"\n⚠️  In our data but NOT in master list ({len(unmatched_ours)}):")
    for s in sorted(unmatched_ours):
        print(f"  - {s}")
if unmatched_master:
    print(f"\n⚠️  In master list but NOT in our data ({len(unmatched_master)}):")
    for s in sorted(unmatched_master):
        print(f"  - {s}")
if not unmatched_ours and not unmatched_master:
    print("\n✅ Perfect match — all subs accounted for")
