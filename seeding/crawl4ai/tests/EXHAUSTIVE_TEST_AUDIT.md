# Exhaustive E2E Test Audit: Social Media Handle Extraction Crawler

## Your Role

You are a QA auditor for a social media handle extraction pipeline. Your job is to **exhaustively verify** that the crawler correctly extracts, classifies, and deduplicates social media handles from real-world HTML and markdown pages. You must treat every handle in every fixture as a test case — no shortcuts, no minimum-count assertions, no trusting that "it probably works."

## Codebase Location

```
seeding/crawl4ai/
├── services/extraction/
│   ├── RegexHandleExtractor.py      # Core regex extraction + blocklist
│   ├── HandleExtractionService.py   # Orchestrator: regex → classify → LLM gate
│   ├── HandleClassifier.py          # LLM fallback for ambiguous handles
│   └── YouTubeChannelResolver.py    # UC... channel ID → @handle resolution
├── tests/
│   ├── fixtures/                    # Real HTML/MD files from live sites
│   ├── unit/                        # Unit tests
│   └── integration/                 # E2E tests
```

---

## Phase 1: Fixture Inventory & Ground Truth

For EVERY fixture file in `tests/fixtures/`:

1. **Open the raw HTML/MD file** and manually count how many real social media handles exist. Document:
   - Total influencer handles (real people/creators, not brands or nav elements)
   - Per-platform breakdown: Instagram, TikTok, YouTube (@handles), YouTube (UC... channel IDs), Twitter/X
   - Naked @handles (no URL context)
   - Brand/company accounts vs influencer accounts
   - False positives present in the raw text (JS framework names, CSS at-rules, URL path segments, template placeholders, navigation elements)

2. **Create a ground truth spreadsheet/table** for each fixture:

```
| Fixture | Real IG | Real TT | Real YT | Real X | YT IDs | Brands | JS Noise | CSS Noise | Nav Noise |
```

3. **If a fixture yields <5 real influencer handles**, flag it as low-value and recommend replacement with a better source page.

---

## Phase 2: Blocklist Completeness Audit

### 2a. Run extraction on every fixture and capture ALL output handles

For each fixture, run:
```python
from services.extraction.RegexHandleExtractor import extract_handles_from_html
results = extract_handles_from_html(html)
```

Then categorize EVERY extracted handle into:
- ✅ **True positive**: Real influencer social media handle
- ❌ **False positive — JS/bundler noise**: e.g. `@vue`, `@babel`, `@webpack`, `@nuxt`, `@react`, `@angular`, `@svelte`, `@next`, `@remix`, `@vite`, `@postcss`, `@eslint`, `@prettier`, `@typescript`, `@rollup`, `@parcel`, `@jest`, `@mocha`, `@cypress`
- ❌ **False positive — CSS at-rule**: e.g. `@media`, `@font-face`, `@keyframes`, `@import`, `@charset`, `@supports`, `@namespace`, `@page`, `@layer`, `@counter-style`, `@property`, `@document`, `@container`
- ❌ **False positive — JSON-LD/Schema**: e.g. `@context`, `@type`, `@graph`, `@id`, `@value`, `@list`, `@set`, `@language`, `@reverse`
- ❌ **False positive — URL path segment**: e.g. `@shopping`, `@blog`, `@explore`, `@reels`, `@stories`, `@accounts`, `@developer`, `@legal`, `@press`, `@branded_content`, `@nametag`
- ❌ **False positive — template/placeholder**: e.g. `@username`, `@handle`, `@user`, `@example`, `@test`, `@your_username`, `@yourhandle`, `@sample`
- ❌ **False positive — platform self-reference**: e.g. `@instagram`, `@tiktok`, `@youtube`, `@twitter`, `@facebook`, `@snapchat`, `@pinterest`
- ❌ **False positive — pure brand/company**: Real accounts but not influencers (e.g. `@virgin`, `@itv`, `@marksandspencerfood`). Note: these are extracted correctly but are NOT influencers — flag whether downstream filtering handles this.
- ❌ **False positive — site's own account**: e.g. `@modash.io`, `@gymfluencers`, `@seekahost`, `@feedspot`, `@trainerize`, `@favikon`
- ❌ **False positive — email/domain leaks**: e.g. `@gmail.com`, `@jeffseid.com`, `@gftdmgmt.com`

### 2b. For every false positive found:

1. Check if it's already in `_IGNORE_HANDLES` in `RegexHandleExtractor.py`
2. If NOT in the blocklist → add it
3. If it's a pattern (e.g. all `.com` handles) → add a regex filter to `_is_valid_handle()`
4. Document which fixtures exposed which gaps

### 2c. Verify the blocklist doesn't block real handles

Check that no real influencer handle is accidentally in the blocklist. Common risks:
- `@next` could be the Next.js framework OR a real influencer
- `@live` could be TikTok nav OR a real handle
- `@music` could be YouTube nav OR a real handle

For any ambiguous entries, check if the handle exists as a real social account.

---

## Phase 3: URL-Based Extraction Accuracy

### 3a. For each fixture, verify URL pattern extraction:

- **Instagram**: `instagram.com/{handle}`, `instagr.am/{handle}`, markdown `[@handle](instagram.com/...)` 
- **TikTok**: `tiktok.com/@{handle}`
- **YouTube @handle**: `youtube.com/@{handle}`
- **YouTube custom**: `youtube.com/c/{handle}`
- **YouTube user**: `youtube.com/user/{handle}`
- **YouTube channel**: `youtube.com/channel/UC...` (ID extraction, not handle)
- **Twitter/X**: `twitter.com/{handle}`, `x.com/{handle}`

### 3b. Check URL path segments are NOT extracted as handles:

Run against each fixture and verify these are NOT extracted:
- `instagram.com/p/CydR62MqhqM` → should NOT extract `CydR62MqhqM` (post ID)
- `instagram.com/reel/...` → should NOT extract `reel`
- `instagram.com/shopping/` → should NOT extract `shopping`
- `youtube.com/watch?v=...` → should NOT extract `watch`
- `youtube.com/results?...` → should NOT extract `results`
- `twitter.com/intent/tweet` → should NOT extract `intent`
- `twitter.com/share` → should NOT extract `share`

### 3c. Check handles with special characters:

- Handles with dots: `@kayla.itsines` (valid), `@a..b` (invalid — consecutive dots)
- Handles with underscores: `@jeff_seid` (valid)
- Handles at max length: 30 chars for IG, 15 for Twitter
- Handles that are pure numbers: should be rejected (post IDs, not handles)

---

## Phase 4: Multi-Platform Deduplication

### 4a. Verify the dedup key is `(handle, platform)` not just `handle`

Find fixtures where the same handle appears on multiple platforms (e.g. `@lungisalwaysbaking` on both IG and TT). Verify:
- Both entries are preserved (one per platform)
- The platform assignment is correct for each

### 4b. Verify same-handle same-platform dedup works

When `instagram.com/kayla_itsines` appears 3 times in the HTML, verify only 1 entry is produced.

### 4c. Count test

For every fixture, assert the EXACT number of handles per platform — not `>=N`, but `== N`. This catches both false positives AND false negatives.

---

## Phase 5: Naked Handle Classification

### 5a. Verify `classify_by_context()` cascade

Test each step of the classification cascade with fixture data:

1. **100-char window, 1 platform keyword** → auto-assign (e.g. "Follow on Instagram: @handle")
2. **100-char window, 2+ platforms** → fall through to full-page check
3. **Full page, 1 dominant platform** → auto-assign
4. **Full page, 2+ platforms tied** → ambiguous → return `None` (LLM fallback)
5. **Full page, 1 platform 2x+ dominant** → auto-assign dominant
6. **Page URL domain** → e.g. `instagram.com` in URL → auto-assign
7. **Nothing found** → return `""` (unclassified, skip LLM)

### 5b. For each fixture with naked handles:

- List every naked handle
- What platform was assigned by mechanical classification?
- Was the assignment correct? (manually verify)
- Were any handles that SHOULD have been classified left unclassified?
- Were any handles classified to the WRONG platform?

### 5c. Verify emoji classification works:

- 📸 near handle → Instagram
- 🎵 near handle → TikTok
- 📺 or 🎥 near handle → YouTube

---

## Phase 6: `needs_llm()` Gating

### 6a. For each fixture page, verify `needs_llm()` returns correct result:

| Page | URL handles | Naked handles | Is listicle? | Expected needs_llm | Actual |
|------|-------------|---------------|--------------|---------------------|--------|

**ExtractionService LLM Rules** (expensive, full-page extraction):
- Zero total handles (URL + naked) AND listicle keyword in URL → `True`
- ANY handles found (URL or naked) → `False` — handles exist, no need for expensive extraction
- Failed page or empty markdown → `False`

> ⚠️ The old rule `naked handles present → True` was WRONG and has been fixed.
> Naked handles are classified mechanically via `classify_by_context()`.

**HandleClassifier LLM Rules** (cheap, per-handle classification in `_classify_naked_handles`):
Fires ONLY when ALL THREE conditions are true:
1. **2+ platforms** mentioned on page (ambiguous)
2. **Zero URL-tagged handles** on page
3. **Naked handles present** after mechanical classification fails

If page has URL-tagged handles → discard ambiguous naked handles (likely brand/sponsor mentions).

### 6b. Verify ExtractionService LLM is NOT called when handles exist

Mock the LLM and assert it is never invoked when regex found any handles.

### 6c. Verify HandleClassifier LLM fires only for the 3-condition scenario

Mock HandleClassifier and assert it is only invoked when 2+ platforms + 0 URL-tagged + naked present.

---

## Phase 7: YouTube Channel ID Resolution

### 7a. Extract channel IDs from every fixture

For each fixture, run `extract_youtube_channel_ids()` and verify:
- All `UC...` IDs in the fixture are found
- No false positives (non-channel-ID strings matching the pattern)
- Channel IDs are all 22-28 chars long starting with `UC`

### 7b. Resolution pipeline (network test)

For at least 3 known channel IDs, verify:
- `resolve_youtube_channels()` returns the correct `@handle`
- Invalid channel IDs return empty/gracefully handled
- Empty input returns empty output

---

## Phase 8: Full Pipeline E2E (per fixture)

For EVERY real fixture, run the full `HandleExtractionService.extract_all_handles()` with mocked LLM:

1. Verify `regex_handles` count is exact (not `>=`)
2. Verify `llm_pages_used` is correct (LLM fires only when expected)
3. Verify `llm_pages_skipped` is correct
4. Verify naked handles got classified (or were correctly left ambiguous)
5. Verify YouTube channel IDs were collected for resolution
6. Verify `all_merged` contains no duplicates
7. Verify NO false positives from Phase 2 appear in final output

---

## Phase 9: Edge Cases & Adversarial Tests

### 9a. Create synthetic HTML fixtures for:

- Page with ONLY naked @handles (no URLs) → verify classification cascade
- Page with 100+ handles of mixed platforms → verify performance and dedup
- Page with handles inside JS `<script>` tags → should these be extracted?
- Page with handles inside HTML comments `<!-- @handle -->` → should these be extracted?
- Page with handles in `alt` text, `title` attributes → verify extraction
- Page with malformed URLs: `instagram.com//handle`, `tiktok.com/@` → verify graceful handling
- Page with Unicode handles: `@café_lover`, `@运动达人` → verify rejection or handling
- Page with very long handles (50+ chars) → verify max-length filter
- Empty page → verify no crash
- Page with only JS (no visible text) → verify no crash

### 9b. Instagram embed patterns:

- `A post shared by Name (@handle)` → verify name + handle extraction
- `A post shared by @handle` → verify handle extraction without name
- Verify Instagram post URLs (`/p/...`, `/reel/...`) are NOT extracted as handles

### 9c. Markdown-specific patterns:

- `[@handle](https://instagram.com/handle)` → verify both handle and platform
- `[Some Text](https://tiktok.com/@handle)` → verify handle extraction from link target
- `![image](https://instagram.com/handle/media/...)` → verify handle extraction, NOT image path

---

## Phase 10: Test Quality Standards

Every test MUST:

1. **Assert exact counts** (`== N`), not minimums (`>= N`)
2. **Assert absence of known false positives** — explicitly check that blocked handles are NOT in results
3. **Assert platform correctness** — not just "handle found" but "handle found on correct platform"
4. **Be deterministic** — no random data, no network calls (except explicitly marked `@pytest.mark.network`)
5. **Use real fixture data** (curled HTML or crawler markdown), never LLM-generated HTML
6. **Document the ground truth** — comments above each test class should state exactly how many handles exist on the page and what they are

---

## Deliverables

1. **Ground truth table** for every fixture (Phase 1)
2. **False positive report** listing every leaked handle and its category (Phase 2)
3. **Updated blocklist** in `RegexHandleExtractor.py` (Phase 2b)
4. **Updated/rewritten test file** with exact count assertions and false positive checks (all phases)
5. **New edge case test file** for adversarial/synthetic tests (Phase 9)
6. **Summary report** with:
   - Precision: what % of extracted handles are real influencers?
   - Recall: what % of real influencer handles in the HTML were extracted?
   - Per-fixture quality score
   - Recommendations for fixture improvements or replacements

---

## Ground Truth Table (as of 2026-03-12)

| Fixture | IG | TT | YT | X | Naked | YTID | Total |
|---------|---:|---:|---:|--:|------:|-----:|------:|
| modash_uk_food.html | 20 | 8 | 1 | 0 | 56 | 5 | 85 |
| feedspot_fitness_ig.html | 101 | 0 | 2 | 1 | 133 | 2 | 237 |
| seekahost_uk_fitness.html | 6 | 0 | 4 | 1 | 14 | 2 | 25 |
| clickanalytic_fitness.html | 15 | 0 | 0 | 0 | 0 | 0 | 15 |
| theinfluenceroom_uk.html | 19 | 14 | 1 | 2 | 3 | 2 | 39 |
| gymfluencers_uk_fitness.html | 0 | 4 | 3 | 0 | 6 | 3 | 13 |
| disruptmarketing.md | 8 | 7 | 0 | 2 | 2 | 1 | 19 |
| modash_us_la.md | 20 | 4 | 1 | 0 | 41 | 4 | 66 |
| popularpays.md | 15 | 0 | 11 | 0 | 1 | 1 | 27 |
| seekahost_male.md | 0 | 0 | 0 | 22 | 0 | 0 | 22 |
| theinfluenceroom.md | 19 | 14 | 1 | 2 | 3 | 2 | 39 |
| **TOTAL** | **225** | **52** | **26** | **34** | **272** | **23** | **609** |

**Dead fixtures** (re-crawled, still yield 0-1 handles — JS-rendered or gated):
- `collabstr_beauty.html` — Cloudflare-blocked, JS-rendered influencer cards
- `heepsy_food.html` — Cloudflare-blocked, still returns stub
- `socialtradia_fitness.html` — Cloudflare-blocked, JS-rendered
- `ugcfactory_fitness.html` — Next.js SSR shell, handles loaded via JS
- `reddit_fitness_yt.html` — Reddit wiki page, not an influencer listicle

---

## Tips for Next Agent

### Architecture
- **Two separate LLM call sites** in `HandleExtractionService.py`:
  1. `needs_llm()` gates **ExtractionService** (expensive, full-page) — only fires for zero-handle listicle pages
  2. `_classify_naked_handles()` gates **HandleClassifier** (cheap, per-handle) — fires ONLY when 2+ platforms + 0 URL-tagged + naked present
- These should ideally be consolidated into a single decision tree

### Blocklist (`RegexHandleExtractor._IGNORE_HANDLES`)
- Currently ~50 entries covering JS/CSS/JSON-LD/site accounts/template placeholders
- Domain-suffix filter catches `.com`, `.co.uk`, `.io`, `.net`, `.org` leaked email handles
- **Watch out for**: `@next` (framework vs real handle), `@live` (nav vs handle)
- Site account blocklist must be updated when new fixture sources are added

### Fixtures
- 5 fixtures are dead (JS-rendered or Cloudflare-blocked) — see table above
- Heavy bias toward fitness + UK. Need more: food, beauty, gaming, US/EU categories
- Some fixtures have FP naked handles like `@The`, `@Sean`, `@Michael` (first-name-only, from gymfluencers) — these are not blocklist candidates, they're genuinely ambiguous
- `feedspot_fitness_ig.html` has 133 naked handles — many are brand accounts, not influencers

### Test Quality
- 335 tests total: 287 unit/integration + 38 edge case + 12 HTTP verification
- E2E multi-site tests (`test_regex_e2e_multi_site.py`) use `>= N` assertions — should be exact `== N`
- The `test_e2e_from_html.py` test requires `GEMINI_API_KEY` and real LLM — should be mocked
- Network tests (`@pytest.mark.network`) require internet + are rate-limited by platforms

### Known Remaining Issues
1. **First-name naked handles** (`@Sean`, `@Michael`, `@Lucy`) — too common to blocklist, too ambiguous to classify. Consider a minimum-handle-length filter (e.g. ≥5 chars for naked handles)
2. **Brand vs influencer**: The pipeline extracts brand accounts correctly but has no downstream filter to separate brands from influencers
3. **Consecutive dot handles** like `@a..b` are technically invalid on IG but the regex accepts them
4. **Twitter/X `intent` and `share`** path segments need to stay in the blocklist — verify they don't get re-added
5. **YouTube `@popular-pays`** in popularpays fixture is the site's own YT, should be blocklisted

### E2E Fixture Correctness: Exact Handle+Platform Ground Truth

Every E2E test MUST assert exact handles per platform. Use this as the canonical source of truth.

#### clickanalytic_fitness.html (15 IG, 0 TT, 0 YT, 0 X)
```
Instagram: @_paigecraig, @ashleyterk, @dorian_kohlanta, @fitbyclem, @fitclaire,
           @hbgoodie, @jujufitcats, @juliepujols, @karoline.ro, @majormouvement,
           @marinlle, @ockeydockey, @sissymua, @tiboinshape, @yasmynswitzer
```

#### theinfluenceroom_uk.html (19 IG, 14 TT, 1 YT, 2 X, 3 naked)
```
Instagram: @aimee_fuller, @amarakanu, @bencarter1, @charlexzfitness, @cjchallenger,
           @densfitness__, @donnanobleyoga, @Ellespibey_fit, @emilymouu,
           @georgeonsports, @jadecarolanfitness, @jadejonestkd, @little.niks,
           @selfacceptancewithjess, @sophieanneyas.pt, @suzionice, @thehartesisters,
           @theinfluenceroomofficial, @zairatary_roller
TikTok:    @ben1carter, @Charlexzfitness, @CJChallenger, @densfitness__,
           @Ellespibey, @emilymouu, @george_eghator, @jadecarolanfitness,
           @jaybefit, @selfacceptancewithjess, @Sophieanneyas, @suzionice,
           @thehartesisters, @zairatary_roller
YouTube:   @littleniks
Twitter:   @Aimee_fuller, @influence_room
naked:     @aimeefullersnow, @diaryofjess, @donnanoble65
```

#### gymfluencers_uk_fitness.html (0 IG, 4 TT, 3 YT, 0 X, 6 naked)
```
TikTok:    @alex.beattie, @bblisacross, @courtneyblackfitness, @victorianiamh
YouTube:   @adammaxted2262, @ESGfitness, @mac_griffiths
naked:     @adammaxted, @Courtney, @Lucy, @Michael, @Sean, @The
```

#### seekahost_uk_fitness.html (6 IG, 0 TT, 4 YT, 1 X, 14 naked)
```
Instagram: @givemestrengthapp, @shreddy, @wearetala, @welcometobabyhood,
           @womens_aid, @womenshealthuk
YouTube:   @MattDoesFitness, @thebodycoach1, @TheJameshaskell, @tvtomdaley
Twitter:   @atSeekaHost
naked:     @aliceliveing, @Aliceliveing_, @chessieking, @davinamccall,
           @glouiseatkinson, @gracebeverley, @jameshaskell, @lucy_meck,
           @lucymeck1, @MissGAtkinson, @thebodycoach, @ThisisDavina,
           @tomdaley, @TomDaley1994
```

#### seekahost_male_influencers.md (0 IG, 0 TT, 0 YT, 22 X)
```
Twitter:   @atSeekaHost, @ConHome, @GoodwoodRRC, @I17SbkoWBq, @Janine_Moore71,
           @Jeremy_Hunt, @Motor1com, @NicolaSturgeon, @nigelharniman, @paul_steele,
           @Popjustice, @rcO8FUipoL, @richardbranson, @RishiSunak, @Shmee150,
           @siightsofficial, @theatonphoto, @thebodycoach, @UKLabour,
           @virginhotels, @virginhotelsnyc, @wtf1official
```

#### popularpays.md (15 IG, 0 TT, 11 YT, 0 X, 1 naked)
```
Instagram: @allenswan, @andyanneville, @cgarciafitness, @chrisruden,
           @curveswithmoves, @dancefitlashawn, @ebenezersamuel23, @emmakirkyo,
           @fitlivinglifestyle, @itsjudinesaintg, @jonelleyoga, @kanoagreene,
           @omniyogagirl, @yoga_girl, @yogathletica
YouTube:   @AnnabelleHayes, @bartkwan, @DanaLinnBailey, @DiabeticMuscleandFitness,
           @KylaBeland, @LoveSweatFitness, @nikkiblackketter, @OmarIsuf,
           @popular-pays, @popularpays9201, @yogawithadriene
naked:     @popular
```

> ⚠️ `@popular-pays` and `@popularpays9201` are the **site's own YouTube accounts** — should be added to the blocklist.

#### modash_uk_food.html and feedspot_fitness_ig.html
These fixtures have 85 and 237 handles respectively — too many to list inline.
Run the profiler script to dump exact handles:
```bash
PYTHONPATH="." python -c "
from services.extraction.RegexHandleExtractor import extract_handles_from_html
from pathlib import Path
html = Path('tests/fixtures/FIXTURE_NAME.html').read_text(errors='replace')
for r in sorted(extract_handles_from_html(html), key=lambda x: (x.platform or 'zz', x.handle.lower())):
    print(f'{r.platform or \"naked\":<12} @{r.handle}')
"
```
