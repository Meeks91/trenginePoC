"""
Unit Tests: Enrichment (patterns + dedup + handle search)
===========================================================
Tests all 3 platforms: Instagram, TikTok, YouTube.
Includes mocked SearchClient for _search_handle().
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch


from services.enrichment.patterns import extract_handle_from_url, extract_handle_from_text
from services.enrichment.NameToHandleService import NameToHandleService
from services.enrichment.InfluencerMerger import InfluencerMerger
from config.schema import Influencer, Platform
from services.audit.AuditService import AuditLog


# Fixtures:

def _mock_search_client(results: list[dict] | None = None) -> MagicMock:
    """Create a SearchClient mock that returns fixed search_text results."""
    client = MagicMock()
    client.search_text.return_value = results if results is not None else []
    client.nr_query_template.return_value = '{name} Instagram YouTube TikTok'
    return client


def _make_svc(tmp: str, search_client: MagicMock | None = None) -> NameToHandleService:
    audit = AuditLog(Path(tmp), "test")
    return NameToHandleService(
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
        svc = _make_svc(tmp, _mock_search_client(results=mock_results))

        handle = svc._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

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
        svc = _make_svc(tmp, _mock_search_client(results=mock_results))

        handle = svc._search_handle("Joe Wicks", Platform.Instagram, "instagram.com")

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
        svc = _make_svc(tmp, _mock_search_client(results=mock_results))

        handle = svc._search_handle("Unknown Person", Platform.Instagram, "instagram.com")

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
        svc = _make_svc(tmp, _mock_search_client(results=mock_results))

        handle = svc._search_handle("Someone", Platform.Instagram, "instagram.com")

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
        svc = _make_svc(tmp, _mock_search_client(results=mock_results))

        handle = svc._search_handle("Charli D'Amelio", Platform.TikTok, "tiktok.com")

    assert handle == "@charlidamelio"


def test_resolve_handles_full():
    """Full resolve_cross_account_handles() — backfills cross-platform handles via mocked client."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")

        def side_effect(query, **kwargs):
            if "Joe Wicks" in query:
                return [{"href": "https://www.instagram.com/thebodycoach/", "title": "Joe Wicks", "body": ""}]
            return [{"href": "https://somesite.com/random", "title": "No match", "body": ""}]

        client = _mock_search_client()
        client.search_text.side_effect = side_effect
        svc = NameToHandleService(audit, search_client=client, delay_seconds=0)

        influencers = [
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
            Influencer(name="Joe Wicks", handles={Platform.TikTok: "thebodycoach"},
                       source_urls={"a.com", "b.com"}),
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
            Influencer(name="Sarah Thompson", handles={}),
        ]

        result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram)

    assert len(result) == 5, f"Expected 5, got {len(result)}"

    joe_entries = [r for r in result if r.name == "Joe Wicks"]
    assert len(joe_entries) == 2, "Joe should have TT original + IG new"
    ig_joe = next(r for r in joe_entries if Platform.Instagram in r.handles)
    assert ig_joe.handles[Platform.Instagram] == "thebodycoach"

    name_only = next(r for r in result if not r.handles)
    assert name_only.name == "Sarah Thompson"


def test_enrich_cross_platform_handle():
    """Cross-platform handles kept; new target-platform entry added alongside."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")

        def side_effect(query, **kwargs):
            if "Adam Maxted" in query:
                return [{"href": "https://www.instagram.com/adammaxted/", "title": "Adam Maxted IG", "body": ""}]
            return [{"href": "https://somesite.com/random", "title": "No match", "body": ""}]

        client = _mock_search_client()
        client.search_text.side_effect = side_effect
        svc = NameToHandleService(audit, search_client=client, delay_seconds=0)

        influencers = [
            Influencer(name="Adam Maxted", handles={Platform.YouTube: "adammaxted2262"}),
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
        ]

        result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, min_sources=0)

    adam_entries = [r for r in result if r.name == "Adam Maxted"]
    assert len(adam_entries) == 2, f"Expected 2 entries for Adam (YT + IG), got {len(adam_entries)}"

    yt_adam = next((r for r in adam_entries if Platform.YouTube in r.handles), None)
    assert yt_adam is not None, "Original YouTube entry was lost"
    assert yt_adam.handles[Platform.YouTube] == "adammaxted2262"

    ig_adam = next((r for r in adam_entries if Platform.Instagram in r.handles), None)
    assert ig_adam is not None, "Instagram entry was not added"
    assert ig_adam.handles[Platform.Instagram] == "adammaxted"

    kayla = next(r for r in result if r.name == "Kayla Itsines")
    assert kayla.handles[Platform.Instagram] == "@kayla_itsines"


def test_dedup_same_handle_different_platforms():
    """Same handle on different platforms must all survive merge."""
    influencers = [
        Influencer(name="Maria Garcia", handles={Platform.Instagram: "@creator_a"}),
        Influencer(name="Maria Garcia", handles={Platform.TikTok: "@creator_a"}),
        Influencer(name="Maria Garcia", handles={Platform.YouTube: "@creator_a"}),
    ]

    result = InfluencerMerger.merge(influencers)
    assert len(result) == 1, f"Expected 1 merged entry, got {len(result)}"
    assert Platform.Instagram in result[0].handles
    assert Platform.TikTok in result[0].handles
    assert Platform.YouTube in result[0].handles


def test_dedup_same_handle_same_platform_collapses():
    """Same handle on same platform must collapse to 1."""
    influencers = [
        Influencer(name="Maria Garcia", handles={Platform.Instagram: "@creator_a"}),
        Influencer(name="Maria Garcia", handles={Platform.Instagram: "@creator_a"}),
    ]

    result = InfluencerMerger.merge(influencers)
    assert len(result) == 1


def test_enrich_keeps_cross_platform_adds_target():
    """Full flow: TikTok entry in → TikTok + Instagram out."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")

        def side_effect(query, **kwargs):
            if "Tom Hardy" in query:
                return [{"href": "https://www.instagram.com/testperson_ig/", "title": "Test Person IG", "body": ""}]
            return []

        client = _mock_search_client()
        client.search_text.side_effect = side_effect
        svc = NameToHandleService(audit, search_client=client, delay_seconds=0)

        influencers = [
            Influencer(name="Tom Hardy", handles={Platform.TikTok: "@testperson"}),
        ]

        result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, min_sources=0)

    assert len(result) == 2

    tt = next(r for r in result if Platform.TikTok in r.handles)
    assert tt.handles[Platform.TikTok] == "@testperson"

    ig = next(r for r in result if Platform.Instagram in r.handles)
    assert ig.handles[Platform.Instagram] == "testperson_ig"


def test_skip_cross_platform_lookup():
    """skip_cross_platform=True skips enrichment for cross-platform handles."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        client = _mock_search_client()
        svc = NameToHandleService(audit, search_client=client, delay_seconds=0)

        influencers = [
            Influencer(name="Mike Chen", handles={Platform.TikTok: "@tiktoker"}),
            Influencer(name="Laura Smith", handles={}),
        ]

        result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, skip_cross_platform=True)

    tt = next(r for r in result if r.name == "Mike Chen")
    assert Platform.TikTok in tt.handles
    assert tt.handles[Platform.TikTok] == "@tiktoker"
    assert sum(1 for r in result if r.name == "Mike Chen") == 1

    name_only = next(r for r in result if r.name == "Laura Smith")
    assert not name_only.handles

    client.search_text.assert_not_called()


def test_resolve_handles_frequency_cap():
    """Only top N by source frequency get searched, entries below min_sources skipped."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")

        search_calls: list[str] = []
        def side_effect(query, **kwargs):
            search_calls.append(query)
            return [{"href": "https://www.instagram.com/found/", "title": "", "body": ""}]

        client = _mock_search_client()
        client.search_text.side_effect = side_effect
        svc = NameToHandleService(audit, search_client=client, delay_seconds=0)

        influencers = [
            Influencer(name="Anna Brown", handles={Platform.TikTok: "low"},
                       source_urls={"a.com"}),
            Influencer(name="David Clark", handles={Platform.TikTok: "medium"},
                       source_urls={"a.com", "b.com"}),
            Influencer(name="Emily Wright", handles={Platform.TikTok: "highfreq"},
                       source_urls={"a.com", "b.com", "c.com", "d.com"}),
            Influencer(name="James Parker", handles={Platform.TikTok: "alsohigh"},
                       source_urls={"a.com", "b.com", "c.com"}),
        ]

        svc.resolve_cross_account_handles(
            influencers, platform=Platform.Instagram,
            max_lookups=2, min_sources=2,
        )

    assert len(search_calls) == 2, f"Expected 2 calls, got {len(search_calls)}: {search_calls}"
    assert any("Emily Wright" in q for q in search_calls)
    assert any("James Parker" in q for q in search_calls)
    assert not any("Anna Brown" in q for q in search_calls)
    assert not any("David Clark" in q for q in search_calls)


# ── _needs_resolution() ──

def test_needs_resolution_no_handle():
    """Influencer with no handle always needs enrichment."""
    inf = Influencer(name="Lisa Turner", handles={})
    assert NameToHandleService._needs_resolution(inf, Platform.Instagram) is True
    assert NameToHandleService._needs_resolution(inf, Platform.TikTok) is True
    assert NameToHandleService._needs_resolution(inf, Platform.YouTube) is True


def test_needs_resolution_correct_platform():
    """Influencer with handle matching target platform does NOT need enrichment."""
    inf = Influencer(name="Lisa Turner", handles={Platform.Instagram: "@test"})
    assert NameToHandleService._needs_resolution(inf, Platform.Instagram) is False


def test_needs_resolution_youtube_targeting_instagram():
    """YouTube handle when targeting Instagram → needs enrichment."""
    inf = Influencer(name="Lisa Turner", handles={Platform.YouTube: "adammaxted2262"})
    assert NameToHandleService._needs_resolution(inf, Platform.Instagram) is True


def test_needs_resolution_tiktok_targeting_instagram():
    """TikTok handle when targeting Instagram → needs enrichment."""
    inf = Influencer(name="Lisa Turner", handles={Platform.TikTok: "@victorianiamh"})
    assert NameToHandleService._needs_resolution(inf, Platform.Instagram) is True


def test_needs_resolution_instagram_targeting_tiktok():
    """Instagram handle when targeting TikTok → needs enrichment."""
    inf = Influencer(name="Lisa Turner", handles={Platform.Instagram: "@kayla_itsines"})
    assert NameToHandleService._needs_resolution(inf, Platform.TikTok) is True


# ── search_text is invoked (not _ddgs directly) ──

def test_search_handle_calls_search_client():
    """_search_handle delegates to search_client.search_text, not DDGS."""
    with tempfile.TemporaryDirectory() as tmp:
        client = _mock_search_client(results=[
            {"href": "https://www.instagram.com/kayla_itsines/", "title": "Kayla Itsines", "body": ""},
        ])
        svc = _make_svc(tmp, client)

        svc._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

        client.search_text.assert_called_once()
        call_args = client.search_text.call_args
        query = call_args.args[0] if call_args.args else call_args.kwargs.get("query", "")
        assert "Kayla Itsines" in query
        assert "instagram.com" in query
