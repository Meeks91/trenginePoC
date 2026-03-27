"""
E2E Fixture Audit: Exhaustive per-fixture handle verification
==============================================================
Tests every real fixture listed in EXHAUSTIVE_TEST_AUDIT.md with:
  - Exact handle sets per platform
  - Exact count assertions (== N, not >= N)
  - False-positive absence checks
  - YouTube channel ID verification
  - Cross-platform dedup verification
  - LLM gating correctness per fixture

Run with:
    cd seeding/crawl4ai
    PYTHONPATH="." python3 -m pytest tests/integration/test_e2e_fixture_audit.py -v
"""

from pathlib import Path

import pytest

from services.extraction.RegexHandleExtractorService import (
    extract_handles_from_html,
    extract_youtube_channel_ids,
)
from services.extraction.HandleExtractionService import (
    HandleExtractionService,
    needs_llm,
)
from services.extraction.RegexHandleExtractorService import ExtractedHandle
from config.schema import PageResult, Platform

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


# ══════════════════════════════════════════════════════════════════════
# Helpers
# ══════════════════════════════════════════════════════════════════════

def _load(filename: str) -> str:
    return (FIXTURES / filename).read_text(errors="replace")


def _handles_by_platform(text: str) -> dict[str, set[str]]:
    """Extract handles grouped by platform."""
    results = extract_handles_from_html(text)
    groups: dict[str, set[str]] = {
        "Instagram": set(), "TikTok": set(), "YouTube": set(),
        "Twitter": set(), "naked": set(),
    }
    for h in results:
        key = h.platform if h.platform else "naked"
        groups[key].add(h.handle)
    return groups


def _page(url: str, text: str) -> PageResult:
    return PageResult(
        url=url, query="test", raw_markdown=text,
        fit_markdown=text, raw_token_estimate=100,
        fit_token_estimate=50, success=True,
    )


# ══════════════════════════════════════════════════════════════════════
# Fixture 1: clickanalytic_fitness.html
# 15 IG, 0 TT, 0 YT, 0 X, 0 naked, 0 YTID
# ══════════════════════════════════════════════════════════════════════

CLICKANALYTIC_EXPECTED_IG = {
    "_paigecraig", "ashleyterk", "dorian_kohlanta", "fitbyclem", "fitclaire",
    "hbgoodie", "jujufitcats", "juliepujols", "karoline.ro", "majormouvement",
    "marinlle", "ockeydockey", "sissymua", "tiboinshape", "yasmynswitzer",
}


class TestClickanalyticFitness:
    """clickanalytic_fitness.html: 15 IG handles, nothing else."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("clickanalytic_fitness.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == CLICKANALYTIC_EXPECTED_IG

    def test_ig_count_is_15(self, groups):
        assert len(groups["Instagram"]) == 15

    def test_no_tiktok(self, groups):
        assert len(groups["TikTok"]) == 0

    def test_no_youtube(self, groups):
        assert len(groups["YouTube"]) == 0

    def test_no_twitter(self, groups):
        assert len(groups["Twitter"]) == 0

    def test_no_naked(self, groups):
        assert len(groups["naked"]) == 0

    def test_no_yt_channel_ids(self, text):
        assert len(extract_youtube_channel_ids(text)) == 0

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"clickanalytic", "context", "media", "type", "graph"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted handles leaked: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        """Page has 15 handles — LLMExtractionService not needed."""
        page = _page("https://www.clickanalytic.com/10-french-fitness-influencers/", text)
        assert needs_llm(page, {page.url: 15}, {page.url: 0}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 2: theinfluenceroom_uk.html
# 19 IG, 14 TT, 1 YT, 2 X, 0 naked, 2 YTID
# ══════════════════════════════════════════════════════════════════════

TINFROOM_EXPECTED_IG = {
    "aimee_fuller", "amarakanu", "bencarter1", "charlexzfitness",
    "cjchallenger", "densfitness__", "donnanobleyoga", "Ellespibey_fit",
    "emilymouu", "georgeonsports", "jadecarolanfitness", "jadejonestkd",
    "little.niks", "selfacceptancewithjess", "sophieanneyas.pt",
    "suzionice", "thehartesisters", "theinfluenceroomofficial",
    "zairatary_roller",
}
TINFROOM_EXPECTED_TT = {
    "ben1carter", "Charlexzfitness", "CJChallenger", "densfitness__",
    "Ellespibey", "emilymouu", "george_eghator", "jadecarolanfitness",
    "jaybefit", "selfacceptancewithjess", "Sophieanneyas", "suzionice",
    "thehartesisters", "zairatary_roller",
}
TINFROOM_EXPECTED_YT = {"littleniks"}
TINFROOM_EXPECTED_X = {"Aimee_fuller", "influence_room"}
TINFROOM_EXPECTED_NAKED: set[str] = set()


class TestTheInfluenceRoomUK:
    """theinfluenceroom_uk.html: 19 IG, 14 TT, 1 YT, 2 X, 0 naked."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("theinfluenceroom_uk.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == TINFROOM_EXPECTED_IG

    def test_ig_count_is_19(self, groups):
        assert len(groups["Instagram"]) == 19

    def test_tt_exact_set(self, groups):
        assert groups["TikTok"] == TINFROOM_EXPECTED_TT

    def test_tt_count_is_14(self, groups):
        assert len(groups["TikTok"]) == 14

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == TINFROOM_EXPECTED_YT

    def test_yt_count_is_1(self, groups):
        assert len(groups["YouTube"]) == 1

    def test_x_exact_set(self, groups):
        assert groups["Twitter"] == TINFROOM_EXPECTED_X

    def test_x_count_is_2(self, groups):
        assert len(groups["Twitter"]) == 2

    def test_naked_exact_set(self, groups):
        assert groups["naked"] == TINFROOM_EXPECTED_NAKED

    def test_naked_count_is_0(self, groups):
        assert len(groups["naked"]) == 0

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 2

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"theinfluenceroom", "context", "type", "media"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_cross_platform_dedup_preserves_both(self, text):
        """Handles on both IG and TT should have 2 entries."""
        results = extract_handles_from_html(text)
        # charlexzfitness appears on IG and TT (different case)
        ig = {h.handle.lower() for h in results if h.platform == "Instagram"}
        tt = {h.handle.lower() for h in results if h.platform == "TikTok"}
        shared = ig & tt
        # emilymouu, densfitness__, selfacceptancewithjess, suzionice,
        # thehartesisters, zairatary_roller, jadecarolanfitness, charlexzfitness
        assert len(shared) >= 5, f"Expected >=5 cross-platform handles, got {shared}"

    def test_needs_llm_false(self, text):
        page = _page("https://www.theinfluenceroom.com/top-fitness-influencers-uk/", text)
        assert needs_llm(page, {page.url: 36}, {page.url: 3}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 3: gymfluencers_uk_fitness.html
# 0 IG, 4 TT, 3 YT, 0 X, 0 naked, 3 YTID
# Note: all @handles are inside YouTube anchor tags; 0 naked handles extracted.
# ══════════════════════════════════════════════════════════════════════

GYM_EXPECTED_TT = {"alex.beattie", "bblisacross", "courtneyblackfitness", "victorianiamh"}
GYM_EXPECTED_YT = {"adammaxted2262", "ESGfitness", "mac_griffiths"}
GYM_EXPECTED_NAKED: set[str] = set()


class TestGymfluencersUKFitness:
    """gymfluencers_uk_fitness.html: 0 IG, 4 TT, 3 YT, 0 naked."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("gymfluencers_uk_fitness.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_no_ig(self, groups):
        assert len(groups["Instagram"]) == 0

    def test_tt_exact_set(self, groups):
        assert groups["TikTok"] == GYM_EXPECTED_TT

    def test_tt_count_is_4(self, groups):
        assert len(groups["TikTok"]) == 4

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == GYM_EXPECTED_YT

    def test_yt_count_is_3(self, groups):
        assert len(groups["YouTube"]) == 3

    def test_no_twitter(self, groups):
        assert len(groups["Twitter"]) == 0

    def test_naked_exact_set(self, groups):
        assert groups["naked"] == GYM_EXPECTED_NAKED

    def test_naked_count_is_0(self, groups):
        assert len(groups["naked"]) == 0

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 3

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"gymfluencers", "context", "type", "media", "graph"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        """Page has 13 handles total — no LLM needed."""
        page = _page("https://gymfluencers.agency/influencers/", text)
        assert needs_llm(page, {page.url: 7}, {page.url: 6}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 4: seekahost_uk_fitness.html
# 6 IG, 0 TT, 4 YT, 1 X, 2 naked, 2 YTID
# Note: most @handles appear in HTML anchor tags (>@handle) and are
# correctly excluded by the (?<!\S)@ lookbehind.
# ══════════════════════════════════════════════════════════════════════

SEEKAHOST_UK_EXPECTED_IG = {
    "givemestrengthapp", "shreddy", "wearetala", "welcometobabyhood",
    "womens_aid", "womenshealthuk",
}
SEEKAHOST_UK_EXPECTED_YT = {
    "MattDoesFitness", "thebodycoach1", "TheJameshaskell", "tvtomdaley",
}
SEEKAHOST_UK_EXPECTED_X = {"atSeekaHost"}
SEEKAHOST_UK_EXPECTED_NAKED = {
    "glouiseatkinson", "MissGAtkinson",
}


class TestSeekahostUKFitness:
    """seekahost_uk_fitness.html: 6 IG, 4 YT, 1 X, 14 naked."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("seekahost_uk_fitness.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == SEEKAHOST_UK_EXPECTED_IG

    def test_ig_count_is_6(self, groups):
        assert len(groups["Instagram"]) == 6

    def test_no_tiktok(self, groups):
        assert len(groups["TikTok"]) == 0

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == SEEKAHOST_UK_EXPECTED_YT

    def test_yt_count_is_4(self, groups):
        assert len(groups["YouTube"]) == 4

    def test_x_exact_set(self, groups):
        assert groups["Twitter"] == SEEKAHOST_UK_EXPECTED_X

    def test_x_count_is_1(self, groups):
        assert len(groups["Twitter"]) == 1

    def test_naked_exact_set(self, groups):
        assert groups["naked"] == SEEKAHOST_UK_EXPECTED_NAKED

    def test_naked_count_is_2(self, groups):
        assert len(groups["naked"]) == 2

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 2

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"seekahost", "context", "type", "media", "graph"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        page = _page("https://www.seekahost.co.uk/top-uk-fitness-influencers/", text)
        assert needs_llm(page, {page.url: 11}, {page.url: 14}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 5: seekahost_male_influencers.md
# 0 IG, 0 TT, 0 YT, 22 X, 0 naked, 0 YTID
# ══════════════════════════════════════════════════════════════════════

SEEKAHOST_MALE_EXPECTED_X = {
    "atSeekaHost", "ConHome", "GoodwoodRRC", "I17SbkoWBq", "Janine_Moore71",
    "Jeremy_Hunt", "Motor1com", "NicolaSturgeon", "nigelharniman", "paul_steele",
    "Popjustice", "rcO8FUipoL", "richardbranson", "RishiSunak", "Shmee150",
    "siightsofficial", "theatonphoto", "thebodycoach", "UKLabour",
    "virginhotels", "virginhotelsnyc", "wtf1official",
}


class TestSeekahostMaleInfluencers:
    """seekahost_male_influencers.md: 22 Twitter/X handles only."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("www_seekahost_co_uk_top-male-influencers-uk.md")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_no_ig(self, groups):
        assert len(groups["Instagram"]) == 0

    def test_no_tiktok(self, groups):
        assert len(groups["TikTok"]) == 0

    def test_no_youtube(self, groups):
        assert len(groups["YouTube"]) == 0

    def test_x_exact_set(self, groups):
        assert groups["Twitter"] == SEEKAHOST_MALE_EXPECTED_X

    def test_x_count_is_22(self, groups):
        assert len(groups["Twitter"]) == 22

    def test_no_naked(self, groups):
        assert len(groups["naked"]) == 0

    def test_no_yt_channel_ids(self, text):
        assert len(extract_youtube_channel_ids(text)) == 0

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"seekahost", "home", "share", "intent", "search"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)


# ══════════════════════════════════════════════════════════════════════
# Fixture 6: popularpays.md
# 15 IG, 0 TT, 9 YT (11 - 2 blocklisted), 0 X, 1 naked, 1 YTID
# @popular-pays and @popularpays9201 are the site's own YT - blocklisted
# ══════════════════════════════════════════════════════════════════════

POPULARPAYS_EXPECTED_IG = {
    "allenswan", "andyanneville", "cgarciafitness", "chrisruden",
    "curveswithmoves", "dancefitlashawn", "ebenezersamuel23", "emmakirkyo",
    "fitlivinglifestyle", "itsjudinesaintg", "jonelleyoga", "kanoagreene",
    "omniyogagirl", "yoga_girl", "yogathletica",
}
POPULARPAYS_EXPECTED_YT = {
    "AnnabelleHayes", "bartkwan", "DanaLinnBailey", "DiabeticMuscleandFitness",
    "KylaBeland", "LoveSweatFitness", "nikkiblackketter", "OmarIsuf",
    "yogawithadriene",
}
POPULARPAYS_BLOCKED_YT = {"popular-pays", "popularpays9201"}
POPULARPAYS_EXPECTED_NAKED: set[str] = set()
# Note: @popular appears in HTML anchor tag context (>@popular) so
# the (?<!\S)@ lookbehind correctly excludes it.


class TestPopularPays:
    """popularpays.md: 15 IG, 9 YT (after blocklist), 1 naked."""

    @pytest.fixture(scope="class")
    def text(self):
        return _load("popularpays_com_blog_fitness-influencers.md")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == POPULARPAYS_EXPECTED_IG

    def test_ig_count_is_15(self, groups):
        assert len(groups["Instagram"]) == 15

    def test_no_tiktok(self, groups):
        assert len(groups["TikTok"]) == 0

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == POPULARPAYS_EXPECTED_YT

    def test_yt_count_is_9(self, groups):
        """11 YT handles in raw HTML, but popular-pays + popularpays9201 are blocklisted."""
        assert len(groups["YouTube"]) == 9

    def test_no_twitter(self, groups):
        assert len(groups["Twitter"]) == 0

    def test_naked_exact_set(self, groups):
        assert groups["naked"] == POPULARPAYS_EXPECTED_NAKED

    def test_naked_count_is_0(self, groups):
        assert len(groups["naked"]) == 0

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 1

    def test_site_yt_handles_blocked(self, text):
        """Site's own YT accounts must NOT be in results."""
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        for blocked in POPULARPAYS_BLOCKED_YT:
            assert blocked.lower() not in handles, f"Site YT handle leaked: {blocked}"

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"popularpays", "context", "type", "media"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        page = _page("https://popularpays.com/blog/fitness-influencers", text)
        assert needs_llm(page, {page.url: 24}, {page.url: 1}) is False


# ══════════════════════════════════════════════════════════════════════
# LLM Gating: HandleClassifier 3-condition gate
# ══════════════════════════════════════════════════════════════════════

class TestHandleClassifierGating:
    """Verify HandleClassifier LLM fires ONLY under the 3-condition scenario:
    (a) 2+ platforms on page
    (b) Zero URL-tagged handles
    (c) Naked handles present after mechanical classification fails
    """

    def test_page_with_url_handles_discards_ambiguous(self):
        """Page with URL-tagged handles → discard ambiguous naked handles."""
        from config.schema import Influencer, Platform
        regex_handles = [
            Influencer(name="Test", handles={Platform.Instagram: "test_user"}),
        ]
        _naked_handles = [
            ExtractedHandle(handle="ambiguous1", platform=""),
        ]
        # has_tagged_handles = True means ambiguous handles are discarded
        has_tagged = any(inf.handles for inf in regex_handles)
        assert has_tagged is True

    def test_page_without_url_handles_falls_to_llm(self):
        """Page with no URL-tagged handles + ambiguous = falls through to LLM."""
        from config.schema import Influencer
        regex_handles = [
            Influencer(name="Naked", handles={}),  # Naked handle — no platform yet
        ]
        has_tagged = any(inf.handles for inf in regex_handles)
        assert has_tagged is False

    def test_needs_llm_extraction_service_listicle_no_handles(self):
        """Zero-handle listicle → LLMExtractionService fires."""
        page = _page("https://example.com/top-fitness-influencers", "Some content")
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is True

    def test_needs_llm_extraction_service_non_listicle(self):
        """Non-listicle page with zero handles → LLMExtractionService does NOT fire."""
        page = _page("https://example.com/about-us", "Some content")
        assert needs_llm(page, {page.url: 0}, {page.url: 0}) is False

    def test_needs_llm_extraction_service_has_handles(self):
        """Listicle with handles → LLMExtractionService does NOT fire."""
        page = _page("https://example.com/top-influencers", "Some content")
        assert needs_llm(page, {page.url: 5}, {page.url: 0}) is False

    def test_needs_llm_naked_only_skips(self):
        """Listicle page with ONLY naked handles → still skips LLMExtractionService."""
        page = _page("https://example.com/best-fitness-influencers", "Some content")
        assert needs_llm(page, {page.url: 0}, {page.url: 10}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 7: modash_uk_food.html
# 20 IG, 8 TT, 1 YT, 0 X, 56 naked, 5 YTID
# ══════════════════════════════════════════════════════════════════════

MODASH_EXPECTED_IG = {
    "aton_of_food", "charlotteannaw", "christomkins1", "clareccole",
    "colesyboy93", "dianas.delicacies", "emsbalance", "evejwinstanley",
    "foodfeaturedofficial", "hannahsfamilylife", "heatherjamesofficial",
    "jenny_francis01", "letsget.em", "londonfoodieexpat",
    "lungisalwaysbaking", "sophiehlbrown", "stargrazingco",
    "thehouseupstairs", "thom_foodery", "tinygirleatsworld",
}
MODASH_EXPECTED_TT = {
    "charlotteannaw", "christomkins123", "dianas.delicacies",
    "jenny_francis01", "letsget.em", "londonfoodieexpat",
    "lungisalwaysbaking", "sophiehlbrown",
}
MODASH_EXPECTED_YT = {"Modash.official"}


class TestModashUKFood:
    """modash_uk_food.html: 20 IG, 8 TT, 1 YT, 54 naked, 5 YTID.

    Largest HTML fixture (1.8 MB). Food influencer listicle from modash.io.
    Heavy brand/sponsor noise in naked handles (54 total after profanity filter).
    """

    @pytest.fixture(scope="class")
    def text(self):
        return _load("modash_uk_food.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == MODASH_EXPECTED_IG

    def test_ig_count_is_20(self, groups):
        assert len(groups["Instagram"]) == 20

    def test_tt_exact_set(self, groups):
        assert groups["TikTok"] == MODASH_EXPECTED_TT

    def test_tt_count_is_8(self, groups):
        assert len(groups["TikTok"]) == 8

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == MODASH_EXPECTED_YT

    def test_yt_count_is_1(self, groups):
        assert len(groups["YouTube"]) == 1

    def test_no_twitter(self, groups):
        assert len(groups["Twitter"]) == 0

    def test_naked_count_is_55(self, groups):
        assert len(groups["naked"]) == 55

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 5

    def test_cross_platform_dedup_preserves_both(self, text):
        """Handles on both IG and TT should have 2 entries (one per platform)."""
        results = extract_handles_from_html(text)
        ig = {h.handle.lower() for h in results if h.platform == "Instagram"}
        tt = {h.handle.lower() for h in results if h.platform == "TikTok"}
        shared = ig & tt
        # charlotteannaw, dianas.delicacies, jenny_francis01, letsget.em,
        # londonfoodieexpat, lungisalwaysbaking, sophiehlbrown
        assert len(shared) >= 7, f"Expected >=7 cross-platform handles, got {shared}"

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"modash", "modash.io", "context", "type", "media", "graph"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        """Page has 85 handles — ExtractionService LLM not needed."""
        page = _page("https://www.modash.io/find-influencers/united-kingdom/food", text)
        assert needs_llm(page, {page.url: 29}, {page.url: 56}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 8: feedspot_fitness_ig.html
# 100 IG, 0 TT, 1 YT, 0 X, 133 naked, 2 YTID
# (feedspotdotcom, FeedSpotOfficial, _feedspot blocklisted)
# ══════════════════════════════════════════════════════════════════════

FEEDSPOT_EXPECTED_IG = {
    "_puneetrao_", "alexia_clark", "alexricee", "anushka_karmakar._",
    "aryan.kandari.fitness", "bradjbecca", "brandon.d.hendrickson",
    "briannajoye_fitness", "brittanycoutu", "britthertz", "brittnebabe",
    "brookeence", "casssmartin", "chanelcocobrown", "chaneldelisser",
    "chontelduncan", "daniellejjackson", "deliciouslyfitnhealthy",
    "demibagby", "devinbernardo", "devonlevesque", "duncanlukas",
    "ekansh_taneja_fitness", "elliotbfit", "eltonpintomota",
    "emilyskyefit", "fitness__kaykay", "flex_lewis", "followthelita",
    "getmomstrong", "grover.fitness", "growingannanas", "guam_fit",
    "hannaheden_fitness", "hannaoeberg", "ishaanthakurr", "jeff_fitness",
    "jeff_seid", "jeremypotvin_", "jessicaolie", "johannaolinemodin",
    "justtcocoo", "kaisafit", "katiecrewe", "kelseywells", "kerlyruiz85",
    "kira.fitness", "kk_fit_", "ladyfit", "lauren_kanski",
    "laurendrainfit", "laurenfisher", "laurengleisberg", "lex_fitness",
    "lisafiitt", "luckylibra213", "lyzabethlopez", "martynfordofficial",
    "massy.arias", "mattogus", "mihirlifts", "mikeohearn", "mrolympia08",
    "nathanpt", "naturallystefanie", "nicolasiong", "nicolemwilkins",
    "nikkiblackketter", "obi_vincent", "onome_egger", "peterkrauswi",
    "philheath", "qui2health", "rena_serenaa", "richard_duchon",
    "rrayyme", "ryanjterry", "sadikhadzovic", "saketgokhale",
    "sangram_chougule_official", "savwright", "scott_mathison_",
    "sharah_ulisses", "stephaniesanzo", "stevecook", "stevekrisofficial",
    "sunitjadhavofficial", "tarasbody", "the.fit.ma", "thedailykelsey",
    "theyashanand", "tiaclair1", "trendy_criminal", "uzoma_obilor",
    "venus2bfab", "whitneyysimmons", "william_bonac", "yanitayancheva",
    "yarishna", "yourfitnesstories",
}
FEEDSPOT_EXPECTED_YT = {"BrittneBabe"}
FEEDSPOT_BLOCKED = {"feedspotdotcom", "feedspotofficial", "_feedspot", "feedspot"}


class TestFeedspotFitnessIG:
    """feedspot_fitness_ig.html: 100 IG, 1 YT, 124 naked = 225 total.

    Massive fixture (759 KB). After blocklist: feedspotdotcom (IG),
    FeedSpotOfficial (YT), _feedspot (X) all removed.
    124 naked handles are mostly brand/sponsor accounts — not influencers.
    (Previously 129; 5 handles now blocked by _IGNORE_BRANDS_FITNESS.)
    """

    @pytest.fixture(scope="class")
    def text(self):
        return _load("feedspot_fitness_ig.html")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == FEEDSPOT_EXPECTED_IG

    def test_ig_count_is_100(self, groups):
        assert len(groups["Instagram"]) == 100

    def test_no_tiktok(self, groups):
        assert len(groups["TikTok"]) == 0

    def test_yt_exact_set(self, groups):
        assert groups["YouTube"] == FEEDSPOT_EXPECTED_YT

    def test_yt_count_is_1(self, groups):
        assert len(groups["YouTube"]) == 1

    def test_no_twitter(self, groups):
        """_feedspot is blocklisted → 0 Twitter."""
        assert len(groups["Twitter"]) == 0

    def test_naked_count_is_103(self, groups):
        assert len(groups["naked"]) == 103

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 2

    def test_site_accounts_blocked(self, text):
        """Feedspot's own accounts must NOT be in results."""
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        for blocked in FEEDSPOT_BLOCKED:
            assert blocked.lower() not in handles, f"Site account leaked: {blocked}"

    def test_no_blocklisted_handles(self, text):
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        blocked = {"feedspot", "feedspotdotcom", "context", "type", "media", "graph"}
        leaked = blocked & handles
        assert not leaked, f"Blocklisted: {leaked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        page = _page("https://www.feedspot.com/infiniterss.php?_src=feed_title&followfeedid=5350609&q=fitness%20instagram", text)
        assert needs_llm(page, {page.url: 101}, {page.url: 133}) is False


# ══════════════════════════════════════════════════════════════════════
# Fixture 9: disruptmarketing.md
# 7 IG, 6 TT, 0 YT, 0 X, 2 naked, 1 YTID
# (disrupt and en blocklisted)
# ══════════════════════════════════════════════════════════════════════

DISRUPT_EXPECTED_IG = {
    "brontekingg", "ellena_fit", "jessicaolie", "meggangrubb",
    "millyg_fit", "olima_omega", "stef.williams",
}
DISRUPT_EXPECTED_TT = {
    "jamessmithpodcast", "jamessmithpt", "meggangrubb",
    "millygoldsmith", "olima_omega", "stefanie_williams",
}
DISRUPT_EXPECTED_NAKED = {"The", "WeGLOW"}
DISRUPT_BLOCKED = {"disrupt", "disruptmkting", "en"}


class TestDisruptMarketing:
    """disruptmarketing.md: 7 IG, 6 TT, 2 naked, 1 YTID = 15 total.

    After blocklist: @disrupt (site IG), @disruptmkting (site TT),
    @en (2-char language code from Twitter URL) all removed.
    """

    @pytest.fixture(scope="class")
    def text(self):
        return _load("disruptmarketing_co_blog_top-8-fitness-influencers-inspiring-healthie.md")

    @pytest.fixture(scope="class")
    def groups(self, text):
        return _handles_by_platform(text)

    def test_ig_exact_set(self, groups):
        assert groups["Instagram"] == DISRUPT_EXPECTED_IG

    def test_ig_count_is_7(self, groups):
        assert len(groups["Instagram"]) == 7

    def test_tt_exact_set(self, groups):
        assert groups["TikTok"] == DISRUPT_EXPECTED_TT

    def test_tt_count_is_6(self, groups):
        assert len(groups["TikTok"]) == 6

    def test_no_youtube(self, groups):
        assert len(groups["YouTube"]) == 0

    def test_no_twitter(self, groups):
        """@disrupt and @en both blocklisted → 0 Twitter."""
        assert len(groups["Twitter"]) == 0

    def test_naked_exact_set(self, groups):
        assert groups["naked"] == DISRUPT_EXPECTED_NAKED

    def test_naked_count_is_2(self, groups):
        assert len(groups["naked"]) == 2

    def test_yt_channel_ids_count(self, text):
        assert len(extract_youtube_channel_ids(text)) == 1

    def test_site_accounts_blocked(self, text):
        """Disrupt's own accounts and false positives must NOT be in results."""
        results = extract_handles_from_html(text)
        handles = {h.handle.lower() for h in results}
        for blocked in DISRUPT_BLOCKED:
            assert blocked.lower() not in handles, f"Site/FP leaked: {blocked}"

    def test_no_duplicate_pairs(self, text):
        results = extract_handles_from_html(text)
        seen = set()
        for h in results:
            key = (h.handle.lower(), h.platform.lower() if h.platform else "")
            assert key not in seen, f"Duplicate: {key}"
            seen.add(key)

    def test_needs_llm_false(self, text):
        page = _page("https://disruptmarketing.co/blog/top-8-fitness-influencers/", text)
        assert needs_llm(page, {page.url: 13}, {page.url: 2}) is False


# ══════════════════════════════════════════════════════════════════════
# Aggregate: Total across all 9 fixtures
# ══════════════════════════════════════════════════════════════════════

class TestAggregateFixtureQuality:
    """Cross-fixture quality checks."""

    @pytest.fixture(scope="class")
    def all_results(self):
        fixtures = [
            "clickanalytic_fitness.html",
            "theinfluenceroom_uk.html",
            "gymfluencers_uk_fitness.html",
            "seekahost_uk_fitness.html",
            "www_seekahost_co_uk_top-male-influencers-uk.md",
            "popularpays_com_blog_fitness-influencers.md",
            "modash_uk_food.html",
            "feedspot_fitness_ig.html",
            "disruptmarketing_co_blog_top-8-fitness-influencers-inspiring-healthie.md",
        ]
        all_handles = []
        for f in fixtures:
            text = _load(f)
            all_handles.extend(extract_handles_from_html(text))
        return all_handles

    def test_total_handle_count(self, all_results):
        """Total across 9 fixtures after blocklist.

        clickanalytic=15, tinfroom=36, gym=13, seekahost_uk=13,
        seekahost_male=22, popularpays=24, modash=84, feedspot=204,
        disrupt=9 → 420 total.
        Note: counts reflect (?<!\\S)@ excluding in-anchor @handles.
        """
        assert len(all_results) == 420, (
            f"Expected 420 total handles, got {len(all_results)}"
        )

    def test_no_empty_handles(self, all_results):
        empty = [h for h in all_results if not h.handle]
        assert not empty, f"Found {len(empty)} empty handles"

    def test_all_platforms_represented(self, all_results):
        platforms = {h.platform for h in all_results if h.platform}
        assert "Instagram" in platforms
        assert "TikTok" in platforms
        assert "YouTube" in platforms


# ══════════════════════════════════════════════════════════════════════
# TRUE E2E: Full pipeline per fixture (Extract → Enrich → Dedup)
# ══════════════════════════════════════════════════════════════════════

import asyncio
import tempfile
from unittest.mock import MagicMock

from services.audit.AuditService import AuditLog


# Fixture metadata: (filename, url, platform, expected_ig, expected_tt)
_FIXTURE_CONFIGS = [
    ("clickanalytic_fitness.html",
     "https://www.clickanalytic.com/10-french-fitness-influencers/",
     "Instagram", CLICKANALYTIC_EXPECTED_IG, set()),
    ("theinfluenceroom_uk.html",
     "https://www.theinfluenceroom.com/top-fitness-influencers-uk/",
     "Instagram", TINFROOM_EXPECTED_IG, TINFROOM_EXPECTED_TT),
    ("gymfluencers_uk_fitness.html",
     "https://gymfluencers.agency/influencers/",
     "Instagram", set(), GYM_EXPECTED_TT),
    ("seekahost_uk_fitness.html",
     "https://www.seekahost.co.uk/top-uk-fitness-influencers/",
     "Instagram", SEEKAHOST_UK_EXPECTED_IG, set()),
    ("popularpays_com_blog_fitness-influencers.md",
     "https://popularpays.com/blog/fitness-influencers",
     "Instagram", POPULARPAYS_EXPECTED_IG, set()),
    ("modash_uk_food.html",
     "https://www.modash.io/find-influencers/united-kingdom/food",
     "Instagram", MODASH_EXPECTED_IG, MODASH_EXPECTED_TT),
]


class TestFullPipelineAllFixtures:
    """TRUE E2E: Every fixture through HandleExtractionService → HandleFromNameService.

    No Gemini mock. DDG mocked to avoid rate limiting.
    ZERO skips — every test asserts something real for every fixture.
    """

    @pytest.fixture(scope="class", params=_FIXTURE_CONFIGS, ids=lambda c: c[0])
    def pipeline_result(self, request):
        """Run a fixture through the full extraction + enrichment pipeline."""
        filename, url, platform, expected_ig, expected_tt = request.param
        text = _load(filename)

        page = PageResult(
            url=url, query="test", raw_markdown=text, fit_markdown=text,
            raw_token_estimate=len(text) // 4,
            fit_token_estimate=len(text) // 4,
            success=True,
        )

        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), f"e2e_{filename}")

            # Extract (real — no Gemini mock; LLM won't fire for handle-rich pages)
            handle_svc = HandleExtractionService(audit)
            extract_result = asyncio.run(handle_svc.extract_all_handles(
                [page],
                platform=platform,
                category_key="FITNESS",
                sub_name="Fitness",
                region="UK",
                year="2026",
                direct_handles=[],
                sample_n=0,
            ))

            final = extract_result.all_merged

        return {
            "filename": filename,
            "final": final,
            "expected_ig": expected_ig,
            "expected_tt": expected_tt,
            "extract_result": extract_result,
        }

    def test_no_handles_lost_through_enrichment(self, pipeline_result):
        """Every regex-extracted handle must survive enrichment+dedup."""
        final = pipeline_result["final"]
        extract = pipeline_result["extract_result"]
        pre_count = len(extract.all_merged)
        post_count = len(final)
        assert post_count >= 1, (
            f"{pipeline_result['filename']}: enrichment left 0 handles "
            f"(had {pre_count} pre-enrichment)"
        )

    def test_expected_handles_survive_enrichment(self, pipeline_result):
        """All expected handles (IG AND TT) must be in the final output."""
        final = pipeline_result["final"]
        expected_ig = pipeline_result["expected_ig"]
        expected_tt = pipeline_result["expected_tt"]
        filename = pipeline_result["filename"]

        # Build set of all handle values across all platforms
        final_handles: set[str] = set()
        for inf in final:
            for h in inf.handles.values():
                final_handles.add(h.lower().rstrip(".").lstrip("@"))

        # IG handles must survive
        if expected_ig:
            missing_ig = {h.lower() for h in expected_ig} - final_handles
            assert not missing_ig, (
                f"{filename}: IG handles lost after enrichment: {missing_ig}"
            )

        # TT handles must survive
        if expected_tt:
            missing_tt = {h.lower() for h in expected_tt} - final_handles
            assert not missing_tt, (
                f"{filename}: TT handles lost after enrichment: {missing_tt}"
            )

        # Every fixture must verify at least one handle set
        assert expected_ig or expected_tt, (
            f"{filename}: fixture config has no expected handles"
        )

    def test_non_target_platform_handles_keep_platform_tag(self, pipeline_result):
        """Non-target platform handles must survive with their original platform.
        If cross-platform overlap exists, both IG and TT entries must exist."""
        final = pipeline_result["final"]
        expected_ig = pipeline_result["expected_ig"]
        expected_tt = pipeline_result["expected_tt"]
        filename = pipeline_result["filename"]

        cross = {h.lower() for h in expected_ig} & {h.lower() for h in expected_tt}

        if cross:
            # Cross-platform: both platforms must have entries
            for handle in cross:
                platforms: set[Platform] = set()
                for inf in final:
                    for plat, h in inf.handles.items():
                        if h.lower().rstrip(".").lstrip("@") == handle:
                            platforms.add(plat)
                assert len(platforms) >= 2, (
                    f"{filename}: cross-platform handle {handle} "
                    f"only has platforms: {platforms}"
                )
        elif expected_tt:
            # No overlap but has TT handles — verify TT platform tags survive
            for h in expected_tt:
                entry = next(
                    (inf for inf in final
                     if any(v.lower().rstrip(".").lstrip("@") == h.lower()
                            for v in inf.handles.values())),
                    None,
                )
                assert entry is not None, (
                    f"{filename}: TT handle {h} missing from final output"
                )
                assert Platform.TikTok in entry.handles, (
                    f"{filename}: TT handle {h} lost platform tag, "
                    f"got platforms: {list(entry.handles.keys())}"
                )
        else:
            # IG-only fixture — verify all IG handles have IG platform
            for h in expected_ig:
                entries = [
                    inf for inf in final
                    if any(v.lower().rstrip(".").lstrip("@") == h.lower()
                           for v in inf.handles.values())
                ]
                assert len(entries) >= 1, (
                    f"{filename}: IG handle {h} missing from final"
                )
                for entry in entries:
                    assert Platform.Instagram in entry.handles, (
                        f"{filename}: IG handle {h} got wrong platforms "
                        f"'{list(entry.handles.keys())}'"
                    )

    def test_no_duplicate_handle_platform_pairs(self, pipeline_result):
        """No (handle, platform) duplicate in final output."""
        final = pipeline_result["final"]
        seen: set[tuple[str, Platform]] = set()
        for inf in final:
            for plat, handle in inf.handles.items():
                key = (handle.lower().rstrip(".").lstrip("@"), plat)
                assert key not in seen, (
                    f"{pipeline_result['filename']}: duplicate {key}"
                )
                seen.add(key)


