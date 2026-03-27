"""
Unit Tests: HandleResolution (patterns + dedup)
===========================================================
Tests all 3 platforms: Instagram, TikTok, YouTube.
"""

from services.handleResolution.patterns import extract_handle_from_url, extract_handle_from_text
from services.influencerMerging.InfluencerMergerService import InfluencerMergerService as InfluencerMerger
from config.schema import Influencer, Platform


# ── Instagram ──

def test_ig_handle_from_url():
    assert extract_handle_from_url("https://instagram.com/kayla_itsines/", "Instagram") == "kayla_itsines"
    assert extract_handle_from_url("https://www.instagram.com/jeffnippard", "Instagram") == "jeffnippard"

def test_ig_junk_rejected():
    assert extract_handle_from_url("https://instagram.com/explore", "Instagram") is None
    assert extract_handle_from_url("https://instagram.com/reels", "Instagram") is None
    assert extract_handle_from_url("https://instagram.com/p/ABC123", "Instagram") is None


# ── TikTok ──

def test_tiktok_handle_from_url():
    assert extract_handle_from_url("https://tiktok.com/@charlidamelio", "TikTok") == "charlidamelio"
    assert extract_handle_from_url("https://www.tiktok.com/@khaby.lame/", "TikTok") == "khaby.lame"

def test_tiktok_junk_rejected():
    assert extract_handle_from_url("https://tiktok.com/@discover", "TikTok") is None
    assert extract_handle_from_url("https://tiktok.com/@foryou", "TikTok") is None


# ── YouTube ──

def test_youtube_handle_from_url():
    assert extract_handle_from_url("https://youtube.com/@MrBeast", "YouTube") == "mrbeast"
    assert extract_handle_from_url("https://youtube.com/c/PewDiePie", "YouTube") == "pewdiepie"
    assert extract_handle_from_url("https://www.youtube.com/@mkbhd/", "YouTube") == "mkbhd"

def test_youtube_junk_rejected():
    assert extract_handle_from_url("https://youtube.com/@watch", "YouTube") is None
    assert extract_handle_from_url("https://youtube.com/@shorts", "YouTube") is None


# ── Cross-platform ──

def test_non_matching_url():
    assert extract_handle_from_url("https://google.com", "Instagram") is None
    assert extract_handle_from_url("https://twitter.com/user", "TikTok") is None

def test_unknown_platform():
    assert extract_handle_from_url("https://example.com/user", "Snapchat") is None


# ── @handle from text ──

def test_handle_from_text():
    assert extract_handle_from_text("Follow @kayla_itsines for workouts") == "kayla_itsines"
    assert extract_handle_from_text("no handles here") is None
    assert extract_handle_from_text("@ab") is None  # Too short


# ── Dedup ──

def test_dedup_by_handle():
    influencers = [
        Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
        Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),  # Duplicate
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "@joewicks"}),
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "@joewicks"}),  # Duplicate
    ]

    result = InfluencerMerger.merge(influencers)
    assert len(result) == 2
    names = {r.name for r in result}
    assert "Kayla Itsines" in names
    assert "Joe Wicks" in names


def test_dedup_by_name_fallback():
    influencers = [
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "joewicks"}),
        Influencer(name="joe wicks", handles={Platform.Instagram: "joewicks"}),  # Same handle, different case name
        Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
    ]

    result = InfluencerMerger.merge(influencers)
    assert len(result) == 2
