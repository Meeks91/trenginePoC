"""
E2E Regex Tests: Multi-Platform, Multi-Site, 100% Extraction Target
====================================================================
Pure regex tests (no LLM, no network) — runs extract_handles_from_html()
against HTML fixtures from real influencer listicle sites.

Tests cover ALL platforms:
  - Instagram  (gymfluencers, feedspot, izea)
  - TikTok     (gymfluencers, embedded)
  - YouTube    (gymfluencers, feedspot, channel IDs)
  - Twitter/X  (cross-platform mentions)

Each test asserts 100% extraction — every handle in the fixture must be found.

Run with:
    PYTHONPATH="." python3 -m pytest tests/integration/test_regex_e2e_multi_site.py -v
"""

from services.extraction.RegexHandleExtractor import (
    extract_handles_from_html,
    extract_youtube_channel_ids,
    extract_handles_from_url,
)


# ══════════════════════════════════════════════════════════════════════
# Fixture 1: Multi-Platform Fitness Page (IG + TT + YT + X)
# Simulates a complex listicle with handles across ALL platforms
# ══════════════════════════════════════════════════════════════════════

FITNESS_MULTI_PLATFORM_HTML = """
<article class="influencer-list">
  <h1>Top 15 Fitness Influencers to Follow in 2026</h1>

  <!-- Instagram handles via <a href> -->
  <div class="card">
    <h3>Kayla Itsines</h3>
    <p>Creator of BBG workout program</p>
    <a href="https://www.instagram.com/kayla_itsines/">Instagram</a>
    <a href="https://www.tiktok.com/@kayla_itsines">TikTok</a>
    <a href="https://x.com/kaaborz">X/Twitter</a>
  </div>

  <div class="card">
    <h3>Joe Wicks</h3>
    <p>The Body Coach</p>
    <a href="https://www.instagram.com/thebodycoach">Instagram</a>
    <a href="https://www.youtube.com/@TheBodyCoachTV">YouTube</a>
    <a href="https://twitter.com/thebodycoach">Twitter</a>
  </div>

  <div class="card">
    <h3>Whitney Simmons</h3>
    <a href="https://instagr.am/whitneyysimmons">Instagram</a>
    <a href="https://www.tiktok.com/@whitneyysimmons">TikTok</a>
  </div>

  <!-- Instagram embed pattern -->
  <blockquote class="instagram-media">
    <p>A post shared by Chloe Ting (@chloe_t)</p>
  </blockquote>

  <!-- YouTube via /c/ and /user/ patterns -->
  <div class="card">
    <h3>Blogilates</h3>
    <a href="https://www.youtube.com/c/blogilates">YouTube</a>
    <a href="https://www.instagram.com/blogilates">Instagram</a>
  </div>

  <div class="card">
    <h3>AthleanX</h3>
    <a href="https://www.youtube.com/user/JDCav24">YouTube</a>
    <a href="https://x.com/ataborz">X</a>
  </div>

  <!-- YouTube channel ID (for resolution) -->
  <div class="card">
    <h3>Tati Westbrook</h3>
    <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">YouTube</a>
  </div>

  <!-- Naked @mention in text -->
  <p>Also check out @pamela_rf on Instagram for home workouts!</p>

  <!-- Multiple platforms in one line -->
  <div class="card">
    <h3>Natacha Océane</h3>
    <a href="https://www.instagram.com/natacha.oceane">IG</a>
    <a href="https://www.tiktok.com/@natacha.oceane">TT</a>
    <a href="https://www.youtube.com/@natachaoceane">YT</a>
    <a href="https://x.com/natachaoceane">X</a>
  </div>

  <!-- Tricky: handles with dots, underscores, and trailing slashes -->
  <div class="card">
    <h3>Jeff Nippard</h3>
    <a href="https://www.instagram.com/jeffnippard/">Instagram</a>
    <a href="https://www.youtube.com/@JeffNippard/">YouTube</a>
  </div>

  <!-- Post URL that should NOT be extracted -->
  <a href="https://www.instagram.com/p/CydR62MqhqM/">View post</a>
  <a href="https://www.instagram.com/reel/ABC123/">View reel</a>
  <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">Watch video</a>

  <!-- Site navigation that should NOT be extracted -->
  <a href="https://twitter.com/home">Home</a>
  <a href="https://www.instagram.com/explore/">Explore</a>
  <a href="https://www.youtube.com/feed">Feed</a>
</article>
"""

# Expected handles from the fitness fixture
FITNESS_EXPECTED_IG = {
    "kayla_itsines", "thebodycoach", "whitneyysimmons", "chloe_t",
    "blogilates", "natacha.oceane", "jeffnippard",
}
FITNESS_EXPECTED_TT = {"kayla_itsines", "whitneyysimmons", "natacha.oceane"}
FITNESS_EXPECTED_YT = {
    "thebodycoachtv", "blogilates", "jdcav24", "natachaoceane", "jeffnippard",
}
FITNESS_EXPECTED_X = {"kaaborz", "thebodycoach", "ataborz", "natachaoceane"}
FITNESS_EXPECTED_YT_CHANNEL_IDS = {"UC4qk9TtGhBKCkoWz5qGJcGg"}
FITNESS_EXPECTED_NAKED = {"pamela_rf"}

# Handles that should NOT be extracted
FITNESS_INVALID = {"p", "reel", "explore", "feed", "home", "watch", "cydr62mqhqqm"}


def test_fitness_instagram_100_percent():
    """Fitness multi-platform: ALL Instagram handles extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    ig = {r.handle.lower() for r in results if r.platform == "Instagram"}
    for expected in FITNESS_EXPECTED_IG:
        assert expected in ig, f"Missing IG handle: {expected}"


def test_fitness_tiktok_100_percent():
    """Fitness multi-platform: ALL TikTok handles extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    tt = {r.handle.lower() for r in results if r.platform == "TikTok"}
    for expected in FITNESS_EXPECTED_TT:
        assert expected in tt, f"Missing TT handle: {expected}"


def test_fitness_youtube_100_percent():
    """Fitness multi-platform: ALL YouTube handles extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    yt = {r.handle.lower() for r in results if r.platform == "YouTube"}
    for expected in FITNESS_EXPECTED_YT:
        assert expected in yt, f"Missing YT handle: {expected}"


def test_fitness_twitter_100_percent():
    """Fitness multi-platform: ALL Twitter/X handles extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    tw = {r.handle.lower() for r in results if r.platform == "Twitter"}
    for expected in FITNESS_EXPECTED_X:
        assert expected in tw, f"Missing X handle: {expected}"


def test_fitness_yt_channel_ids():
    """Fitness: YouTube channel IDs extracted for resolution."""
    ids = extract_youtube_channel_ids(FITNESS_MULTI_PLATFORM_HTML)
    for expected in FITNESS_EXPECTED_YT_CHANNEL_IDS:
        assert expected in ids, f"Missing YT channel ID: {expected}"


def test_fitness_naked_handles():
    """Fitness: Naked @handles in text extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    for expected in FITNESS_EXPECTED_NAKED:
        assert expected in all_handles, f"Missing naked handle: {expected}"


def test_fitness_no_false_positives():
    """Fitness: Post URLs, navigation, and path segments NOT extracted."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    for invalid in FITNESS_INVALID:
        assert invalid not in all_handles, f"False positive extracted: {invalid}"


def test_fitness_embed_carries_name():
    """Fitness: IG embed extracts name along with handle."""
    results = extract_handles_from_html(FITNESS_MULTI_PLATFORM_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    assert by_handle["chloe_t"].name == "Chloe Ting"


# ══════════════════════════════════════════════════════════════════════
# Fixture 2: Food Influencer Page (IG embeds + TikTok)
# Tests Instagram embed + TikTok extraction in food category
# ══════════════════════════════════════════════════════════════════════

FOOD_PLATFORM_HTML = """
<div class="food-influencers">
  <h1>Best Food Influencers 2026</h1>

  <div class="influencer">
    <h3>Jamie Oliver</h3>
    <a href="https://www.instagram.com/jamieoliver">Instagram</a>
    <a href="https://www.youtube.com/@JamieOliver">YouTube</a>
    <a href="https://x.com/jamieoliver">X</a>
  </div>

  <blockquote class="instagram-media">
    <p>A post shared by Gordon Ramsay (@gordongram)</p>
  </blockquote>
  <a href="https://www.tiktok.com/@gordonramsayofficial">TikTok</a>

  <div class="influencer">
    <h3>Tabitha Brown</h3>
    <a href="https://www.instagram.com/iamtabithabrown">Instagram</a>
    <a href="https://www.tiktok.com/@iamtabithabrown">TikTok</a>
    <a href="https://twitter.com/iamtabithabrown">Twitter</a>
  </div>

  <!-- YouTube channel + custom URL -->
  <div class="influencer">
    <h3>Binging with Babish</h3>
    <a href="https://www.youtube.com/c/baborz">YouTube</a>
    <a href="https://www.instagram.com/baborz">Instagram</a>
  </div>

  <div class="influencer">
    <h3>Salt Bae</h3>
    <a href="https://www.instagram.com/nuaborz_saltbae">IG</a>
    <a href="https://www.tiktok.com/@nuaborz_saltbae">TT</a>
  </div>

  <!-- Should NOT extract -->
  <a href="https://www.instagram.com/p/Cxf8v0Gth5p/">View embed</a>
  <a href="https://www.instagram.com/stories/jamieoliver/">Stories</a>
</div>
"""

FOOD_EXPECTED_IG = {"jamieoliver", "gordongram", "iamtabithabrown", "baborz", "nuaborz_saltbae"}
FOOD_EXPECTED_TT = {"gordonramsayofficial", "iamtabithabrown", "nuaborz_saltbae"}
FOOD_EXPECTED_YT = {"jamieoliver", "baborz"}
FOOD_EXPECTED_X = {"jamieoliver", "iamtabithabrown"}


def test_food_instagram_100_percent():
    """Food: ALL Instagram handles extracted."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    ig = {r.handle.lower() for r in results if r.platform == "Instagram"}
    for expected in FOOD_EXPECTED_IG:
        assert expected in ig, f"Missing IG handle: {expected}"


def test_food_tiktok_100_percent():
    """Food: ALL TikTok handles extracted."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    tt = {r.handle.lower() for r in results if r.platform == "TikTok"}
    for expected in FOOD_EXPECTED_TT:
        assert expected in tt, f"Missing TT handle: {expected}"


def test_food_youtube_100_percent():
    """Food: ALL YouTube handles extracted."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    yt = {r.handle.lower() for r in results if r.platform == "YouTube"}
    for expected in FOOD_EXPECTED_YT:
        assert expected in yt, f"Missing YT handle: {expected}"


def test_food_twitter_100_percent():
    """Food: ALL Twitter/X handles extracted."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    tw = {r.handle.lower() for r in results if r.platform == "Twitter"}
    for expected in FOOD_EXPECTED_X:
        assert expected in tw, f"Missing X handle: {expected}"


def test_food_embed_name():
    """Food: IG embed extracts Gordon Ramsay name."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    assert by_handle["gordongram"].name == "Gordon Ramsay"


def test_food_no_false_positives():
    """Food: Post/story URLs NOT extracted."""
    results = extract_handles_from_html(FOOD_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    assert "p" not in all_handles
    assert "stories" not in all_handles


# ══════════════════════════════════════════════════════════════════════
# Fixture 3: Beauty/Skincare (YouTube heavy + IG)
# Tests YouTube /c/, /user/, /@, channel IDs
# ══════════════════════════════════════════════════════════════════════

BEAUTY_PLATFORM_HTML = """
<section class="beauty-channels">
  <h1>Top Beauty YouTubers 2026</h1>

  <div class="creator">
    <h3>James Charles</h3>
    <a href="https://www.youtube.com/@jamescharles">YouTube</a>
    <a href="https://www.instagram.com/jamescharles">Instagram</a>
    <a href="https://www.tiktok.com/@jamescharles">TikTok</a>
  </div>

  <div class="creator">
    <h3>NikkieTutorials</h3>
    <a href="https://www.youtube.com/@NikkieTutorials">YouTube</a>
    <a href="https://www.instagram.com/nikkietutorials">Instagram</a>
    <a href="https://x.com/NikkieTutorials">X</a>
  </div>

  <div class="creator">
    <h3>Hyram</h3>
    <a href="https://www.youtube.com/c/Hyram">YouTube</a>
    <a href="https://www.tiktok.com/@hyram">TikTok</a>
  </div>

  <div class="creator">
    <h3>Robert Welsh</h3>
    <a href="https://www.youtube.com/user/RobertWelshMUA">YouTube</a>
    <a href="https://www.instagram.com/robertwelshofficial">Instagram</a>
  </div>

  <!-- Channel IDs for resolution -->
  <div class="creator">
    <h3>Tati</h3>
    <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">YouTube</a>
  </div>
  <div class="creator">
    <h3>Jackie Aina</h3>
    <a href="https://www.youtube.com/channel/UCzJIliq68IHSn-Kwgjeg2AQ">YouTube</a>
  </div>
</section>
"""

BEAUTY_EXPECTED_YT = {"jamescharles", "nikkietutorials", "hyram", "robertwelshmua"}
BEAUTY_EXPECTED_IG = {"jamescharles", "nikkietutorials", "robertwelshofficial"}
BEAUTY_EXPECTED_TT = {"jamescharles", "hyram"}
BEAUTY_EXPECTED_X = {"nikkietutorials"}
BEAUTY_EXPECTED_CHANNEL_IDS = {"UC4qk9TtGhBKCkoWz5qGJcGg", "UCzJIliq68IHSn-Kwgjeg2AQ"}


def test_beauty_youtube_100_percent():
    """Beauty: ALL YouTube handles extracted (/@, /c/, /user/)."""
    results = extract_handles_from_html(BEAUTY_PLATFORM_HTML)
    yt = {r.handle.lower() for r in results if r.platform == "YouTube"}
    for expected in BEAUTY_EXPECTED_YT:
        assert expected in yt, f"Missing YT handle: {expected}"


def test_beauty_instagram_100_percent():
    """Beauty: ALL Instagram handles extracted."""
    results = extract_handles_from_html(BEAUTY_PLATFORM_HTML)
    ig = {r.handle.lower() for r in results if r.platform == "Instagram"}
    for expected in BEAUTY_EXPECTED_IG:
        assert expected in ig, f"Missing IG handle: {expected}"


def test_beauty_tiktok_100_percent():
    """Beauty: ALL TikTok handles extracted."""
    results = extract_handles_from_html(BEAUTY_PLATFORM_HTML)
    tt = {r.handle.lower() for r in results if r.platform == "TikTok"}
    for expected in BEAUTY_EXPECTED_TT:
        assert expected in tt, f"Missing TT handle: {expected}"


def test_beauty_twitter_100_percent():
    """Beauty: ALL Twitter/X handles extracted."""
    results = extract_handles_from_html(BEAUTY_PLATFORM_HTML)
    tw = {r.handle.lower() for r in results if r.platform == "Twitter"}
    for expected in BEAUTY_EXPECTED_X:
        assert expected in tw, f"Missing X handle: {expected}"


def test_beauty_channel_ids():
    """Beauty: YouTube channel IDs extracted for resolution."""
    ids = extract_youtube_channel_ids(BEAUTY_PLATFORM_HTML)
    for expected in BEAUTY_EXPECTED_CHANNEL_IDS:
        assert expected in ids, f"Missing channel ID: {expected}"


def test_beauty_channel_ids_not_in_handles():
    """Beauty: Channel IDs NOT in normal handle results."""
    results = extract_handles_from_html(BEAUTY_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    assert "uc4qk9ttghbkckwz5qgjcgg" not in all_handles
    assert "uczjiliq68ihsn" not in all_handles


# ══════════════════════════════════════════════════════════════════════
# Fixture 4: Health & Wellness (instagr.am + tricky patterns)
# Tests edge cases: instagr.am, dot handles, underscores
# ══════════════════════════════════════════════════════════════════════

HEALTH_PLATFORM_HTML = """
<div class="health-influencers">
  <h1>Health & Wellness Creators</h1>

  <div class="creator">
    <h3>Dr. Mike</h3>
    <a href="https://instagr.am/doctor.mike">Instagram</a>
    <a href="https://www.youtube.com/@DoctorMike">YouTube</a>
    <a href="https://x.com/RealDoctorMike">X</a>
  </div>

  <div class="creator">
    <h3>Yoga With Adriene</h3>
    <a href="https://www.instagram.com/adrienelouise">Instagram</a>
    <a href="https://www.youtube.com/user/yogawithadaborz">YouTube</a>
    <a href="https://www.tiktok.com/@yogawithadaborz">TikTok</a>
  </div>

  <div class="creator">
    <h3>Dr. Sandra Lee</h3>
    <p>Also known as @drpimplepopper</p>
    <a href="https://www.instagram.com/drpimplepopper">Instagram</a>
    <a href="https://www.youtube.com/@DrPimplePopper">YouTube</a>
    <a href="https://www.tiktok.com/@dermdoctor">TikTok</a>
  </div>

  <blockquote class="instagram-media">
    <p>A post shared by Massy Arias (@mankofit)</p>
  </blockquote>

  <div class="creator">
    <h3>Cassey Ho</h3>
    <a href="https://www.instagram.com/_cassey_ho_">Instagram</a>
    <a href="https://twitter.com/blogilates">Twitter</a>
  </div>

  <!-- Tricky: consecutive dots should NOT match -->
  <a href="https://www.instagram.com/fake..account">Invalid</a>
  <!-- Tricky: pure numeric should NOT match -->
  <a href="https://www.instagram.com/1234567890">Not an account</a>
</div>
"""

HEALTH_EXPECTED_IG = {"doctor.mike", "adrienelouise", "drpimplepopper", "mankofit", "_cassey_ho_"}
HEALTH_EXPECTED_YT = {"doctormike", "yogawithadaborz", "drpimplepopper"}
HEALTH_EXPECTED_TT = {"yogawithadaborz", "dermdoctor"}
HEALTH_EXPECTED_X = {"realdoctormike", "blogilates"}


def test_health_instagram_100_percent():
    """Health: ALL Instagram handles including instagr.am and embedded."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    ig = {r.handle.lower() for r in results if r.platform == "Instagram"}
    for expected in HEALTH_EXPECTED_IG:
        assert expected in ig, f"Missing IG handle: {expected}"


def test_health_youtube_100_percent():
    """Health: ALL YouTube handles (/@, /user/)."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    yt = {r.handle.lower() for r in results if r.platform == "YouTube"}
    for expected in HEALTH_EXPECTED_YT:
        assert expected in yt, f"Missing YT handle: {expected}"


def test_health_tiktok_100_percent():
    """Health: ALL TikTok handles extracted."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    tt = {r.handle.lower() for r in results if r.platform == "TikTok"}
    for expected in HEALTH_EXPECTED_TT:
        assert expected in tt, f"Missing TT handle: {expected}"


def test_health_twitter_100_percent():
    """Health: ALL Twitter/X handles extracted."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    tw = {r.handle.lower() for r in results if r.platform == "Twitter"}
    for expected in HEALTH_EXPECTED_X:
        assert expected in tw, f"Missing X handle: {expected}"


def test_health_instagr_am_works():
    """Health: instagr.am short URL correctly identified as Instagram."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    assert "doctor.mike" in by_handle
    assert by_handle["doctor.mike"].platform == "Instagram"


def test_health_consecutive_dots_rejected():
    """Health: Handle with consecutive dots NOT extracted."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    assert "fake..account" not in all_handles


def test_health_numeric_rejected():
    """Health: Pure numeric 'handle' NOT extracted."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    all_handles = {r.handle.lower() for r in results}
    assert "1234567890" not in all_handles


def test_health_embed_name():
    """Health: IG embed extracts Massy Arias name."""
    results = extract_handles_from_html(HEALTH_PLATFORM_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    assert by_handle["mankofit"].name == "Massy Arias"


# ══════════════════════════════════════════════════════════════════════
# Fixture 5: DDG Dorking URL Extraction (all platforms)
# Tests extract_handles_from_url for each platform
# ══════════════════════════════════════════════════════════════════════

DDG_TEST_URLS = [
    ("https://www.instagram.com/kayla_itsines", "kayla_itsines", "Instagram"),
    ("https://instagr.am/fitnessguru", "fitnessguru", "Instagram"),
    ("https://www.tiktok.com/@charlidamelio", "charlidamelio", "TikTok"),
    ("https://www.youtube.com/@MrBeast", "MrBeast", "YouTube"),
    ("https://www.youtube.com/c/PewDiePie", "PewDiePie", "YouTube"),
    ("https://www.youtube.com/user/JDCav24", "JDCav24", "YouTube"),
    ("https://x.com/elonmusk", "elonmusk", "Twitter"),
    ("https://twitter.com/karllorey", "karllorey", "Twitter"),
]

DDG_JUNK_URLS = [
    "https://www.instagram.com/p/CydR62MqhqM/",
    "https://www.instagram.com/reel/ABC123/",
    "https://www.instagram.com/explore/",
    "https://twitter.com/home",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.healthline.com/best-workouts",
]


def test_ddg_all_platform_urls():
    """DDG: Every platform URL correctly extracted."""
    for url, expected_handle, expected_platform in DDG_TEST_URLS:
        result = extract_handles_from_url(url)
        assert result is not None, f"No extraction for {url}"
        assert result.handle.lower() == expected_handle.lower(), \
            f"Wrong handle for {url}: got {result.handle}, expected {expected_handle}"
        assert result.platform == expected_platform, \
            f"Wrong platform for {url}: got {result.platform}, expected {expected_platform}"


def test_ddg_junk_urls_return_none():
    """DDG: Post/navigation/non-platform URLs return None."""
    for url in DDG_JUNK_URLS:
        result = extract_handles_from_url(url)
        assert result is None, f"False positive for junk URL: {url} → {result}"


# ══════════════════════════════════════════════════════════════════════
# Aggregate: Total extraction across ALL fixtures
# Proves regex alone achieves 100% on structured listicle pages
# ══════════════════════════════════════════════════════════════════════

def test_aggregate_total_handles():
    """Aggregate: combined extraction across all 4 fixtures meets minimum."""
    combined = (
        FITNESS_MULTI_PLATFORM_HTML +
        FOOD_PLATFORM_HTML +
        BEAUTY_PLATFORM_HTML +
        HEALTH_PLATFORM_HTML
    )
    results = extract_handles_from_html(combined)
    all_handles = {r.handle.lower() for r in results}

    # Total unique handles expected: fitness ~18 + food ~8 + beauty ~8 + health ~10 = ~44
    # After dedup across fixtures (shared handles like blogilates, jamescharles): ~35+
    assert len(all_handles) == 35, \
        f"Expected 35 unique handles, got {len(all_handles)}: {sorted(all_handles)}"


def test_aggregate_all_platforms_represented():
    """Aggregate: at least 3 handles per platform across all fixtures."""
    combined = (
        FITNESS_MULTI_PLATFORM_HTML +
        FOOD_PLATFORM_HTML +
        BEAUTY_PLATFORM_HTML +
        HEALTH_PLATFORM_HTML
    )
    results = extract_handles_from_html(combined)
    platforms = {}
    for r in results:
        p = r.platform or "unknown"
        platforms[p] = platforms.get(p, 0) + 1

    assert platforms.get("Instagram", 0) == 21, f"IG: {platforms.get('Instagram', 0)}"
    assert platforms.get("TikTok", 0) == 10, f"TT: {platforms.get('TikTok', 0)}"
    assert platforms.get("YouTube", 0) == 14, f"YT: {platforms.get('YouTube', 0)}"
    assert platforms.get("Twitter", 0) == 9, f"X: {platforms.get('Twitter', 0)}"
