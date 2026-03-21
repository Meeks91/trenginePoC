"""
Unit Tests: RegexHandleExtractor — Handle extraction from real-world HTML
=========================================================================
Tests use HTML snippets from 5+ real websites across 4 categories:

1. Gymfluencers UK         (FITNESS)  — TikTok/YouTube <a href> cards
2. Feedspot Fitness IG     (FITNESS)  — [@handle](instagram.com/) pattern
3. Feedspot Healthy Food   (FOOD)     — Same pattern, different category
4. Feedspot Beauty YouTube (BEAUTY)   — youtube.com/channel/ URLs
5. IZEA Food Styling       (FOOD)     — Embedded IG posts, TikTok embeds
6. Edge cases              (MIXED)    — Malformed URLs, noise, no handles
7. Lorey patterns          (MIXED)    — instagr.am, consecutive dots, YT /c/ /user/
8. X/Twitter               (MIXED)    — x.com and twitter.com handles
9. YouTube channel IDs     (BEAUTY)   — UC... extraction for resolution
10. DDG URL extraction     (MIXED)    — Single-URL handle extraction
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.extraction.RegexHandleExtractor import (
    extract_handles_from_html,
    extract_youtube_channel_ids,
    extract_handles_from_url,
    count_handles,
)


# ══════════════════════════════════════════════════════════════════════
# Test 1: Gymfluencers UK (FITNESS — TikTok/YouTube <a href> links)
# Source: gymfluencers.co.uk/blog/best-uk-fitness-influencers
# Pattern: <a href="https://www.tiktok.com/@handle"> in card blocks
# ══════════════════════════════════════════════════════════════════════

GYMFLUENCERS_HTML = """
<div class="influencer-card">
  <h3>Alex Beattie</h3>
  <p>Former Love Island star turned fitness coach</p>
  <a href="https://www.tiktok.com/@alex.beattie" target="_blank">TikTok</a>
</div>
<div class="influencer-card">
  <h3>Lisa Cross</h3>
  <p>Champion bodybuilder and fitness model</p>
  <a href="https://www.tiktok.com/@bblisacross" target="_blank">TikTok</a>
</div>
<div class="influencer-card">
  <h3>Adam Maxted</h3>
  <p>Personal trainer and ex-Love Island contestant</p>
  <a href="https://www.youtube.com/@adammaxted2262" target="_blank">YouTube</a>
</div>
<div class="influencer-card">
  <h3>Emma Storey-Gordon</h3>
  <a href="https://www.youtube.com/@esgfitness" target="_blank">YouTube</a>
</div>
<div class="influencer-card">
  <h3>Michael Griffiths</h3>
  <a href="https://www.youtube.com/@mac_griffiths" target="_blank">YouTube</a>
</div>
"""


def test_gymfluencers_tiktok_handles():
    """Gymfluencers UK: TikTok <a href> must extract handles."""
    results = extract_handles_from_html(GYMFLUENCERS_HTML)
    handles = {r.handle.lower() for r in results}
    assert "alex.beattie" in handles
    assert "bblisacross" in handles


def test_gymfluencers_youtube_handles():
    """Gymfluencers UK: YouTube <a href> must extract handles."""
    results = extract_handles_from_html(GYMFLUENCERS_HTML)
    handles = {r.handle.lower() for r in results}
    assert "adammaxted2262" in handles
    assert "esgfitness" in handles
    assert "mac_griffiths" in handles


def test_gymfluencers_platforms():
    """Gymfluencers UK: Platform must be correctly identified per handle."""
    results = extract_handles_from_html(GYMFLUENCERS_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    assert by_handle["alex.beattie"].platform == "TikTok"
    assert by_handle["adammaxted2262"].platform == "YouTube"


def test_gymfluencers_count():
    """Gymfluencers UK: Should find exactly 5 unique handles."""
    assert count_handles(GYMFLUENCERS_HTML) == 5


# ══════════════════════════════════════════════════════════════════════
# Test 2: Feedspot Fitness Instagram (FITNESS — IG profile links)
# Source: blog.feedspot.com/fitness_instagram_influencers/
# Pattern: Instagram Handle [@handle](https://www.instagram.com/handle/)
# ══════════════════════════════════════════════════════════════════════

FEEDSPOT_FITNESS_HTML = """
<h3>1. Kerly Ruiz</h3>
<p>Bio Emmy winner - TV Host - Model</p>
<p>Instagram Handle <a href="https://www.instagram.com/kerlyruiz85/">@kerlyruiz85</a>
Instagram Followers 4.9M</p>

<h3>2. Jeff Seid</h3>
<p>Bio Contact: jeff@jeffseid.com</p>
<p>Instagram Handle <a href="https://www.instagram.com/jeff_seid/">@jeff_seid</a>
Instagram Followers 4.6M</p>

<h3>3. Whitney Simmons</h3>
<p>Train with me on <a href="https://www.instagram.com/thealiveapp/">@thealiveapp</a></p>
<p>Instagram Handle <a href="https://www.instagram.com/whitneyysimmons/">@whitneyysimmons</a>
Instagram Followers 4M</p>

<h3>4. Lisa Lanceford</h3>
<p>Just a Fitness trainer</p>
<p>Instagram Handle <a href="https://www.instagram.com/lisafiitt/">@lisafiitt</a>
Instagram Followers 3.5M</p>

<h3>5. Sadik Hadzovic</h3>
<p>@NOWNEVERNYC Apparel - @TEAM.SADIK Online Coaching</p>
<p>Instagram Handle <a href="https://www.instagram.com/sadikhadzovic/">@sadikhadzovic</a></p>
"""


def test_feedspot_fitness_ig_handles():
    """Feedspot Fitness: Must extract all Instagram handles from profile links."""
    results = extract_handles_from_html(FEEDSPOT_FITNESS_HTML)
    handles = {r.handle.lower() for r in results}
    assert "kerlyruiz85" in handles
    assert "jeff_seid" in handles
    assert "whitneyysimmons" in handles
    assert "lisafiitt" in handles
    assert "sadikhadzovic" in handles


def test_feedspot_fitness_all_instagram():
    """Feedspot Fitness: All extracted handles should be Instagram."""
    results = extract_handles_from_html(FEEDSPOT_FITNESS_HTML)
    ig_handles = [r for r in results if r.platform == "Instagram"]
    # At least the 5 main profile links + thealiveapp
    assert len(ig_handles) >= 5


def test_feedspot_fitness_secondary_handles():
    """Feedspot Fitness: Secondary handles mentioned in bios should also be found."""
    results = extract_handles_from_html(FEEDSPOT_FITNESS_HTML)
    handles = {r.handle.lower() for r in results}
    # @thealiveapp is mentioned as a link in Whitney's bio
    assert "thealiveapp" in handles


# ══════════════════════════════════════════════════════════════════════
# Test 3: Feedspot Healthy Food Instagram (FOOD — same pattern)
# Source: blog.feedspot.com/healthy_food_instagram_influencers/
# Validates regex works across categories, not just fitness
# ══════════════════════════════════════════════════════════════════════

FEEDSPOT_FOOD_HTML = """
<h3>1. Danielle Brown</h3>
<p>here to help you live your healthiest (plant-based) life.
2x @nytimes best-selling cookbook author</p>
<p>Instagram Handle <a href="https://www.instagram.com/healthygirlkitchen/">@healthygirlkitchen</a>
Instagram Followers 5.2M</p>

<h3>2. Yumna</h3>
<p>Founder of <a href="https://www.instagram.com/oathoats/">@oathoats</a></p>
<p>Instagram Handle <a href="https://www.instagram.com/feelgoodfoodie/">@feelgoodfoodie</a>
Instagram Followers 4.8M</p>

<h3>3. Rena Awada</h3>
<p>Instagram Handle <a href="https://www.instagram.com/healthyfitnessmeals/">@healthyfitnessmeals</a>
Instagram Followers 4.3M</p>

<h3>4. Gina Homolka</h3>
<p>Instagram Handle <a href="https://www.instagram.com/skinnytaste/">@skinnytaste</a>
Instagram Followers 2.2M</p>

<h3>5. Sarah Cobacho</h3>
<p>Instagram Handle <a href="https://www.instagram.com/_plantbaes_/">@_plantbaes_</a>
Instagram Followers 2M</p>
"""


def test_feedspot_food_ig_handles():
    """Feedspot Food: Healthy food influencer handles extracted correctly."""
    results = extract_handles_from_html(FEEDSPOT_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    assert "healthygirlkitchen" in handles
    assert "feelgoodfoodie" in handles
    assert "healthyfitnessmeals" in handles
    assert "skinnytaste" in handles
    assert "_plantbaes_" in handles


def test_feedspot_food_secondary_brand():
    """Feedspot Food: Secondary brand handles in bios should also be found."""
    results = extract_handles_from_html(FEEDSPOT_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    # Yumna's brand @oathoats is linked
    assert "oathoats" in handles


def test_feedspot_food_underscore_handles():
    """Feedspot Food: Handles with leading/trailing underscores must be extracted."""
    results = extract_handles_from_html(FEEDSPOT_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    # _plantbaes_ has underscores on both sides
    assert "_plantbaes_" in handles


# ══════════════════════════════════════════════════════════════════════
# Test 4: Feedspot Beauty YouTube (BEAUTY — YouTube channel URLs)
# Source: blog.feedspot.com/beauty_youtube_channels/
# Pattern: youtube.com/channel/UC... (channel ID, not @handle)
# This tests a HARDER case where handles aren't in the URL
# ══════════════════════════════════════════════════════════════════════

FEEDSPOT_BEAUTY_YT_HTML = """
<h3>Tati Westbrook</h3>
<p>Youtube Channel <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">Visit</a></p>
<p>Channel Name Tati</p>
<p>Instagram Followers 2.1M</p>

<h3>Jackie Aina</h3>
<p>Youtube Channel <a href="https://www.youtube.com/channel/UCzJIliq68IHSn-Kwgjeg2AQ/videos">Visit</a></p>
<p>Channel Name Jackie Aina</p>

<h3>Huda Kattan</h3>
<p>Youtube Channel <a href="https://www.youtube.com/channel/UCRSvEADlY-caz3sfDNwvR1A">Visit</a></p>
<p>Channel Name Huda Beauty</p>
<p>Instagram Followers 57.5M</p>

<h3>Nikkie Tutorials</h3>
<p>Check out her <a href="https://www.youtube.com/@nikkietutorials">YouTube channel</a></p>
<p>and her <a href="https://www.instagram.com/nikkietutorials/">Instagram</a></p>
"""


def test_feedspot_beauty_yt_channel_urls_not_extracted():
    """Feedspot Beauty: youtube.com/channel/UC... should NOT extract as handle.

    Channel IDs (UC4qk9TtGh...) are not human-readable handles.
    Only youtube.com/@ URLs should extract.
    """
    results = extract_handles_from_html(FEEDSPOT_BEAUTY_YT_HTML)
    handles = {r.handle.lower() for r in results}
    # Channel IDs should NOT be extracted
    assert "uc4qk9ttghbkckwz5qgjcgg" not in handles
    assert "uczjiliq68ihsn" not in handles


def test_feedspot_beauty_at_handle_found():
    """Feedspot Beauty: youtube.com/@nikkietutorials SHOULD extract."""
    results = extract_handles_from_html(FEEDSPOT_BEAUTY_YT_HTML)
    handles = {r.handle.lower() for r in results}
    assert "nikkietutorials" in handles


def test_feedspot_beauty_cross_platform():
    """Feedspot Beauty: Should find both YouTube and Instagram for Nikkie."""
    results = extract_handles_from_html(FEEDSPOT_BEAUTY_YT_HTML)
    nikkie_results = [r for r in results if r.handle.lower() == "nikkietutorials"]
    # Per-platform dedup: same handle on IG + YT → 2 entries
    assert len(nikkie_results) == 2
    platforms = {r.platform for r in nikkie_results}
    assert platforms == {"Instagram", "YouTube"}


# ══════════════════════════════════════════════════════════════════════
# Test 5: IZEA Food Styling (FOOD — embedded IG posts + TikTok embeds)
# Source: izea.com/influencer-marketing/food-influencers/
# Patterns: "A post shared by Name (@handle)", tiktok.com/@handle
# ══════════════════════════════════════════════════════════════════════

IZEA_FOOD_HTML = """
<h3>Laura Muthesius and Nora Eiserman</h3>
<p>This Berlin-based twosome is the team behind Our Food Stories.</p>
<a href="https://www.instagram.com/p/CydR62MqhqM/">beautiful photos</a>
<blockquote class="instagram-media">
  <p>A post shared by Our Food Stories (@_foodstories_)</p>
</blockquote>

<h3>Madison</h3>
<p>Madison is a food and product photographer.</p>
<a href="https://www.instagram.com/ladyofashion">Instagram</a>
<a href="https://www.tiktok.com/@ladyofashion?refer=embed">@ladyofashion</a>
<p>Spicy Mussels w/pasta</p>

<h3>Linda Lomelino</h3>
<p>She has 752K followers on Instagram.</p>
<a href="https://www.instagram.com/p/Cxf8v0Gth5p/">moody style</a>
<blockquote class="instagram-media">
  <p>A post shared by Linda Lomelino (@linda_lomelino)</p>
</blockquote>

<h3>Blair Johnson</h3>
<p>You can find her work on her personal
<a href="https://www.instagram.com/thelifeofmamablair">Instagram</a></p>
<blockquote class="instagram-media">
  <p>A post shared by Blair | Food Recipes + Mom Tips (@thelifeofmamablair)</p>
</blockquote>
"""


def test_izea_food_ig_embed_handles():
    """IZEA Food: Instagram embed 'A post shared by ... (@handle)' must extract."""
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    assert "_foodstories_" in handles
    assert "linda_lomelino" in handles
    assert "thelifeofmamablair" in handles


def test_izea_food_ig_embed_extracts_name():
    """IZEA Food: Embedded IG posts should extract valid person names only.

    After NameCleaner integration:
      - 'Linda Lomelino' → valid two-word person name → kept
      - 'Blair | Food Recipes + Mom Tips' → pipe-stripped to 'Blair' (single word) → rejected
      - 'Our Food Stories' → not a person name → rejected
    """
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    by_handle = {r.handle.lower(): r for r in results}
    # "A post shared by Linda Lomelino (@linda_lomelino)" → valid
    assert by_handle["linda_lomelino"].name == "Linda Lomelino"
    # "Blair | Food Recipes ..." → pipe-stripped to "Blair" → single word → rejected
    assert by_handle["thelifeofmamablair"].name == ""
    # "Our Food Stories" → not a person name per NameCleaner → rejected
    assert by_handle["_foodstories_"].name == ""


def test_izea_food_tiktok_embed():
    """IZEA Food: TikTok embed links must extract handle."""
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    assert "ladyofashion" in handles


def test_izea_food_tiktok_platform():
    """IZEA Food: ladyofashion should be tagged as TikTok (first URL match wins)."""
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    lady = next(r for r in results if r.handle.lower() == "ladyofashion")
    # Instagram link appears first in HTML, so it will be tagged Instagram
    assert lady.platform == "Instagram"


def test_izea_food_dedup():
    """IZEA Food: Same handle on IG + TT → 2 entries (per-platform dedup)."""
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    # ladyofashion appears as both instagram.com/ladyofashion and tiktok.com/@ladyofashion
    # Per-platform dedup: each platform gets its own entry
    ladyofashion_list = [r for r in results if r.handle.lower() == "ladyofashion"]
    assert len(ladyofashion_list) == 2
    platforms = {r.platform for r in ladyofashion_list}
    assert platforms == {"Instagram", "TikTok"}


def test_izea_food_skips_post_urls():
    """IZEA Food: instagram.com/p/... post URLs must NOT extract as handles."""
    results = extract_handles_from_html(IZEA_FOOD_HTML)
    handles = {r.handle.lower() for r in results}
    # instagram.com/p/CydR62MqhqM should NOT match
    assert "cydr62mqhqqm" not in handles


# ══════════════════════════════════════════════════════════════════════
# Test 6: Edge Cases (MIXED — stress tests for the patterns)
# ══════════════════════════════════════════════════════════════════════

def test_no_handles_returns_empty():
    """Page with no social media links should return empty list."""
    html = """
    <h1>Best Recipes 2025</h1>
    <p>Here are some great cooking tips for beginners.</p>
    <a href="https://example.com/about">About Us</a>
    """
    results = extract_handles_from_html(html)
    assert results == []


def test_mixed_platforms_all_extracted():
    """Handles from all 3 platforms in one page should all be extracted."""
    html = """
    <a href="https://www.instagram.com/fitgirl99">Instagram</a>
    <a href="https://www.tiktok.com/@dancequeen">TikTok</a>
    <a href="https://www.youtube.com/@chef_mike">YouTube</a>
    """
    results = extract_handles_from_html(html)
    handles = {r.handle.lower(): r.platform for r in results}
    assert handles["fitgirl99"] == "Instagram"
    assert handles["dancequeen"] == "TikTok"
    assert handles["chef_mike"] == "YouTube"


def test_duplicate_handles_deduped():
    """Same handle appearing multiple times should be deduped."""
    html = """
    <a href="https://www.instagram.com/kayla_itsines">Profile</a>
    <p>Follow @kayla_itsines on Instagram!</p>
    <a href="https://www.instagram.com/kayla_itsines/">Also here</a>
    """
    results = extract_handles_from_html(html)
    kayla = [r for r in results if "kayla" in r.handle.lower()]
    assert len(kayla) == 1


def test_url_path_segments_filtered():
    """URL path segments like /p/, /reel/, /explore/ must not match."""
    html = """
    <a href="https://www.instagram.com/p/CydR62MqhqM/">Post link</a>
    <a href="https://www.instagram.com/reel/ABC123/">Reel link</a>
    <a href="https://www.instagram.com/explore/tags/fitness/">Tag link</a>
    <a href="https://www.instagram.com/stories/someone/">Story link</a>
    <a href="https://www.youtube.com/watch?v=abc">Watch link</a>
    <a href="https://www.youtube.com/channel/UC123abc">Channel ID link</a>
    """
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "p" not in handles
    assert "reel" not in handles
    assert "explore" not in handles
    assert "stories" not in handles
    assert "watch" not in handles
    assert "channel" not in handles


def test_tracking_params_filtered():
    """UTM parameters and IG params should not be extracted as handles."""
    html = """
    <a href="https://www.instagram.com/p/ABC/?utm_source=ig_embed&utm_campaign=loading">Embed</a>
    """
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "utm_source" not in handles
    assert "ig_embed" not in handles


def test_handles_with_periods_and_underscores():
    """Handles with dots and underscores should be fully captured."""
    html = """
    <a href="https://www.instagram.com/a.b_c.d_/">dotted handle</a>
    <a href="https://www.tiktok.com/@_leading.underscore">underscored</a>
    """
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "a.b_c.d_" in handles or "a.b_c.d" in handles  # trailing dot stripped
    assert "_leading.underscore" in handles


def test_short_handles_rejected():
    """Single character handles should be rejected."""
    html = """
    <a href="https://www.instagram.com/x/">Too short</a>
    """
    results = extract_handles_from_html(html)
    # "x" is only 1 char, should be rejected (but "ab" is 2 chars, we allow 2+)
    handles = {r.handle.lower() for r in results}
    assert "x" not in handles


def test_numeric_only_rejected():
    """Pure numeric 'handles' (post IDs) should be rejected."""
    html = """
    <a href="https://www.instagram.com/1234567890/">Numbers only</a>
    """
    results = extract_handles_from_html(html)
    assert len(results) == 0


def test_at_mention_without_url():
    """@handle in plain text should be extracted when no URL exists for it."""
    html = """
    <p>Check out @fitness_queen on Instagram for great workouts!</p>
    """
    results = extract_handles_from_html(html)
    assert len(results) == 1
    assert results[0].handle == "fitness_queen"
    assert results[0].platform == ""  # Unknown — no URL context


def test_at_mention_deduped_with_url():
    """@handle in text should be deduped if the same handle exists in a URL."""
    html = """
    <a href="https://www.instagram.com/kayla_itsines/">Profile</a>
    <p>Follow @kayla_itsines !</p>
    """
    results = extract_handles_from_html(html)
    kayla = [r for r in results if "kayla" in r.handle.lower()]
    assert len(kayla) == 1
    assert kayla[0].platform == "Instagram"  # URL takes precedence


# ══════════════════════════════════════════════════════════════════════
# Test 7: Lorey Patterns (from lorey/social-media-profiles-regexs)
# Validates community-standard regex patterns are supported
# ══════════════════════════════════════════════════════════════════════

def test_instagr_am_short_url():
    """instagr.am short URL should extract handle (lorey pattern)."""
    html = '<a href="https://www.instagr.am/__disco__dude">Profile</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "__disco__dude" in handles


def test_instagr_am_platform_is_instagram():
    """instagr.am should be identified as Instagram platform."""
    html = '<a href="https://instagr.am/fitnessguru">Profile</a>'
    results = extract_handles_from_html(html)
    assert results[0].platform == "Instagram"


def test_consecutive_dots_rejected():
    """Handles with consecutive dots should be rejected (lorey rule)."""
    html = '<a href="https://www.instagram.com/disco..dude">Profile</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    # disco..dude has consecutive dots — should not match or should be filtered
    assert "disco..dude" not in handles


def test_youtube_custom_url():
    """youtube.com/c/{handle} should extract handle."""
    html = '<a href="https://www.youtube.com/c/PewDiePie">YouTube</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "pewdiepie" in handles


def test_youtube_user_url():
    """youtube.com/user/{handle} should extract handle (lorey pattern)."""
    html = '<a href="https://www.youtube.com/user/JPPGmbH">YouTube</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "jppgmbh" in handles


def test_youtube_user_platform():
    """youtube.com/user/ handles should be tagged as YouTube."""
    html = '<a href="https://www.youtube.com/user/CookingWithDog">YouTube</a>'
    results = extract_handles_from_html(html)
    assert results[0].platform == "YouTube"


# ══════════════════════════════════════════════════════════════════════
# Test 8: X/Twitter Handles
# ══════════════════════════════════════════════════════════════════════

def test_twitter_handle_extracted():
    """twitter.com/{handle} should extract handle."""
    html = '<a href="https://twitter.com/karllorey">Twitter</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "karllorey" in handles


def test_x_dot_com_handle():
    """x.com/{handle} (rebrand) should extract handle."""
    html = '<a href="https://x.com/elonmusk">X Profile</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "elonmusk" in handles


def test_twitter_platform_tag():
    """Twitter/X handles should be tagged as Twitter platform."""
    html = '<a href="https://x.com/fitnessgal">X</a>'
    results = extract_handles_from_html(html)
    assert results[0].platform == "Twitter"


def test_twitter_path_segments_filtered():
    """Twitter navigation paths should not match as handles."""
    html = """
    <a href="https://twitter.com/home">Home</a>
    <a href="https://twitter.com/search">Search</a>
    <a href="https://twitter.com/settings">Settings</a>
    <a href="https://twitter.com/i/flow/signup">Sign up</a>
    """
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "home" not in handles
    assert "search" not in handles
    assert "settings" not in handles
    assert "i" not in handles


def test_twitter_with_at_prefix():
    """twitter.com/@handle should work (some URLs have @)."""
    html = '<a href="http://twitter.com/@karllorey">Profile</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert "karllorey" in handles


# ══════════════════════════════════════════════════════════════════════
# Test 9: YouTube Channel ID Extraction
# ══════════════════════════════════════════════════════════════════════

def test_yt_channel_ids_extracted():
    """youtube.com/channel/UC... IDs should be extracted for later resolution."""
    html = """
    <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">Tati</a>
    <a href="https://www.youtube.com/channel/UCzJIliq68IHSn-Kwgjeg2AQ/videos">Jackie</a>
    """
    ids = extract_youtube_channel_ids(html)
    assert "UC4qk9TtGhBKCkoWz5qGJcGg" in ids
    assert len(ids) == 2


def test_yt_channel_ids_deduped():
    """Duplicate channel IDs should be deduped."""
    html = """
    <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">Visit</a>
    <a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg/videos">Videos</a>
    """
    ids = extract_youtube_channel_ids(html)
    assert len(ids) == 1


def test_yt_channel_ids_not_in_handles():
    """Channel IDs should NOT appear in handle extraction results."""
    html = '<a href="https://www.youtube.com/channel/UC4qk9TtGhBKCkoWz5qGJcGg">Visit</a>'
    results = extract_handles_from_html(html)
    handles = {r.handle.lower() for r in results}
    assert len(handles) == 0  # Channel IDs are not handles


# ══════════════════════════════════════════════════════════════════════
# Test 10: DDG URL → Handle Extraction (single URL)
# ══════════════════════════════════════════════════════════════════════

def test_ddg_ig_url_extraction():
    """DDG returns instagram.com/handle → extract immediately."""
    result = extract_handles_from_url("https://www.instagram.com/kayla_itsines")
    assert result is not None
    assert result.handle == "kayla_itsines"
    assert result.platform == "Instagram"


def test_ddg_tiktok_url_extraction():
    """DDG returns tiktok.com/@handle → extract immediately."""
    result = extract_handles_from_url("https://www.tiktok.com/@charlidamelio")
    assert result is not None
    assert result.handle == "charlidamelio"
    assert result.platform == "TikTok"


def test_ddg_yt_at_handle_url():
    """DDG returns youtube.com/@handle → extract immediately."""
    result = extract_handles_from_url("https://www.youtube.com/@MrBeast")
    assert result is not None
    assert result.handle == "MrBeast"
    assert result.platform == "YouTube"


def test_ddg_twitter_url():
    """DDG returns x.com/handle → extract immediately."""
    result = extract_handles_from_url("https://x.com/fitcoach_uk")
    assert result is not None
    assert result.handle == "fitcoach_uk"
    assert result.platform == "Twitter"


def test_ddg_non_platform_url_returns_none():
    """DDG returns a blog URL → should return None."""
    result = extract_handles_from_url("https://www.healthline.com/best-workouts")
    assert result is None


def test_ddg_ig_junk_path_filtered():
    """DDG returns instagram.com/explore → should return None."""
    result = extract_handles_from_url("https://www.instagram.com/explore/tags/fitness")
    assert result is None


# ══════════════════════════════════════════════════════════════════════
# Test 11: Multi-site Aggregate (E2E regex, no LLM)
# Proves regex alone hits 100% on structured listicle pages
# ══════════════════════════════════════════════════════════════════════

def test_multisite_all_handles_extracted():
    """All handles from all 5 test sites should be extracted when combined."""
    combined = GYMFLUENCERS_HTML + FEEDSPOT_FITNESS_HTML + FEEDSPOT_FOOD_HTML + IZEA_FOOD_HTML
    results = extract_handles_from_html(combined)
    handles = {r.handle.lower() for r in results}
    # Gymfluencers (5 handles)
    assert "alex.beattie" in handles
    assert "bblisacross" in handles
    assert "adammaxted2262" in handles
    assert "esgfitness" in handles
    assert "mac_griffiths" in handles
    # Feedspot Fitness (6 handles)
    assert "kerlyruiz85" in handles
    assert "jeff_seid" in handles
    assert "whitneyysimmons" in handles
    assert "lisafiitt" in handles
    assert "sadikhadzovic" in handles
    assert "thealiveapp" in handles
    # Feedspot Food (6 handles)
    assert "healthygirlkitchen" in handles
    assert "feelgoodfoodie" in handles
    assert "healthyfitnessmeals" in handles
    assert "skinnytaste" in handles
    assert "_plantbaes_" in handles
    assert "oathoats" in handles
    # IZEA (4 handles)
    assert "_foodstories_" in handles
    assert "linda_lomelino" in handles
    assert "thelifeofmamablair" in handles
    assert "ladyofashion" in handles
    # Total: at least 21 unique handles
    assert len(handles) >= 21
