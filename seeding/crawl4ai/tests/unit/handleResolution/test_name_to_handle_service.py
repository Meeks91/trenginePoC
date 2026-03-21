"""
Unit Tests: HandleResolution (patterns + dedup + handle search)
===========================================================
Tests all 3 platforms: Instagram, TikTok, YouTube.
Includes mocked SearchClient for _search_handle() (now on CrossPlatformHandleResolverService).
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock


from services.handleResolution.patterns import extract_handle_from_url, extract_handle_from_text
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService
from services.influencerMerging.InfluencerMergerService import InfluencerMergerService as InfluencerMerger
from config.schema import Influencer, Platform
from services.audit.AuditService import AuditLog


# Fixtures:

def _mock_search_client(results: list[dict] | None = None) -> MagicMock:
    """Create a SearchClient mock that returns fixed search_text results."""
    client = MagicMock()
    client.search_text.return_value = results if results is not None else []
    client.nr_query_template.return_value = '{name} Instagram YouTube TikTok'
    return client


def _make_resolver(tmp: str, search_client: MagicMock | None = None) -> CrossPlatformHandleResolverService:
    audit = AuditLog(Path(tmp), "test")
    return CrossPlatformHandleResolverService(
        audit,
        search_client=search_client or _mock_search_client(),
        delay_seconds=0,
    )

# Fixtures


# ── Instagram ──

def test_ig_handle_from_url():
    assert extract_handle_from_url("https://instagram.com/kayla_itsines/", "Instagram") == "@kayla_itsines"
    assert extract_handle_from_url("https://www.instagram.com/jeffnippard", "Instagram") == "@jeffnippard"

def test_ig_junk_rejected():
    assert extract_handle_from_url("https://instagram.com/explore", "Instagram") is None
    assert extract_handle_from_url("https://instagram.com/reels", "Instagram") is None
    assert extract_handle_from_url("https://instagram.com/p/ABC123", "Instagram") is None


# ── TikTok ──

def test_tiktok_handle_from_url():
    assert extract_handle_from_url("https://tiktok.com/@charlidamelio", "TikTok") == "@charlidamelio"
    assert extract_handle_from_url("https://www.tiktok.com/@khaby.lame/", "TikTok") == "@khaby.lame"

def test_tiktok_junk_rejected():
    assert extract_handle_from_url("https://tiktok.com/@discover", "TikTok") is None
    assert extract_handle_from_url("https://tiktok.com/@foryou", "TikTok") is None


# ── YouTube ──

def test_youtube_handle_from_url():
    assert extract_handle_from_url("https://youtube.com/@MrBeast", "YouTube") == "@mrbeast"
    assert extract_handle_from_url("https://youtube.com/c/PewDiePie", "YouTube") == "@pewdiepie"
    assert extract_handle_from_url("https://www.youtube.com/@mkbhd/", "YouTube") == "@mkbhd"

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
    assert extract_handle_from_text("Follow @kayla_itsines for workouts") == "@kayla_itsines"
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


# ── _search_handle() with mocked SearchClient ──

def test_search_handle_from_url():
    """_search_handle extracts handle from search client result URLs."""
    with tempfile.TemporaryDirectory() as tmp:
        mock_results = [
            {
                "href": "https://www.instagram.com/kayla_itsines/",
                "title": "Kayla Itsines - Instagram",
                "body": "Fitness trainer",
            }
        ]
        resolver = _make_resolver(tmp, _mock_search_client(results=mock_results))

        handle = resolver._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

    assert handle == "@kayla_itsines"


def test_search_handle_from_text():
    """_search_handle falls back to @handle in title/body text."""
    with tempfile.TemporaryDirectory() as tmp:
        mock_results = [
            {
                "href": "https://somesite.com/article",
                "title": "Follow @joe_wicks for workouts",
                "body": "Joe Wicks fitness",
            }
        ]
        resolver = _make_resolver(tmp, _mock_search_client(results=mock_results))

        handle = resolver._search_handle("Joe Wicks", Platform.Instagram, "instagram.com")

    assert handle == "@joe_wicks"


def test_search_handle_no_results():
    """_search_handle returns None when search returns no useful results."""
    with tempfile.TemporaryDirectory() as tmp:
        mock_results = [
            {
                "href": "https://somesite.com/random",
                "title": "Unrelated page",
                "body": "No handles here",
            }
        ]
        resolver = _make_resolver(tmp, _mock_search_client(results=mock_results))

        handle = resolver._search_handle("Unknown Person", Platform.Instagram, "instagram.com")

    assert handle is None


def test_search_handle_rejects_junk():
    """_search_handle rejects junk platform paths like /explore."""
    with tempfile.TemporaryDirectory() as tmp:
        mock_results = [
            {
                "href": "https://www.instagram.com/explore",
                "title": "Instagram Explore",
                "body": "Discover content",
            }
        ]
        resolver = _make_resolver(tmp, _mock_search_client(results=mock_results))

        handle = resolver._search_handle("Someone", Platform.Instagram, "instagram.com")

    assert handle is None


def test_search_handle_tiktok():
    """_search_handle works for TikTok URLs."""
    with tempfile.TemporaryDirectory() as tmp:
        mock_results = [
            {
                "href": "https://www.tiktok.com/@charlidamelio",
                "title": "Charli D'Amelio TikTok",
                "body": "",
            }
        ]
        resolver = _make_resolver(tmp, _mock_search_client(results=mock_results))

        handle = resolver._search_handle("Charli D'Amelio", Platform.TikTok, "tiktok.com")

    assert handle == "@charlidamelio"



def test_search_handle_calls_search_client():
    """_search_handle delegates to search_client.search_text, not DDGS."""
    with tempfile.TemporaryDirectory() as tmp:
        client = _mock_search_client(results=[
            {"href": "https://www.instagram.com/kayla_itsines/", "title": "Kayla Itsines", "body": ""},
        ])
        resolver = _make_resolver(tmp, client)

        resolver._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

        client.search_text.assert_called_once()
        call_args = client.search_text.call_args
        query = call_args.args[0] if call_args.args else call_args.kwargs.get("query", "")
        assert "Kayla Itsines" in query
        assert "instagram.com" in query
