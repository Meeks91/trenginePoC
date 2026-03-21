"""
Unit Tests: Enrichment (patterns + dedup + handle search)
===========================================================
Tests all 3 platforms: Instagram, TikTok, YouTube.
Includes mocked DDGS for _search_handle().
"""

import tempfile
from pathlib import Path
from unittest.mock import patch


from services.enrichment.patterns import extract_handle_from_url, extract_handle_from_text
from services.enrichment.NameToHandleService import NameToHandleService
from services.enrichment.InfluencerMerger import InfluencerMerger
from config.schema import Influencer, Platform
from services.audit.AuditService import AuditLog


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


# ── _search_handle() with mocked DDGS ──

def test_search_handle_from_url():
    """_search_handle should extract handle from DDG result URLs."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://www.instagram.com/kayla_itsines/",
                "title": "Kayla Itsines - Instagram",
                "body": "Fitness trainer",
            }
        ]

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            handle = svc._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

        assert handle == "@kayla_itsines"


def test_search_handle_from_text():
    """_search_handle should fall back to @handle in title/body text."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://somesite.com/article",
                "title": "Follow @joe_wicks for workouts",
                "body": "Joe Wicks fitness",
            }
        ]

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            handle = svc._search_handle("Joe Wicks", Platform.Instagram, "instagram.com")

        assert handle == "@joe_wicks"


def test_search_handle_no_results():
    """_search_handle should return None when DDG returns no useful results."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://somesite.com/random",
                "title": "Unrelated page",
                "body": "No handles here",
            }
        ]

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            handle = svc._search_handle("Unknown Person", Platform.Instagram, "instagram.com")

        assert handle is None


def test_search_handle_rejects_junk():
    """_search_handle should reject junk platform paths like /explore."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://www.instagram.com/explore",
                "title": "Instagram Explore",
                "body": "Discover content",
            }
        ]

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            handle = svc._search_handle("Someone", Platform.Instagram, "instagram.com")

        assert handle is None


def test_search_handle_tiktok():
    """_search_handle should work for TikTok URLs."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://www.tiktok.com/@charlidamelio",
                "title": "Charli D'Amelio TikTok",
                "body": "",
            }
        ]

        with patch.object(svc._ddgs, "text", return_value=mock_results):
            handle = svc._search_handle("Charli D'Amelio", Platform.TikTok, "tiktok.com")

        assert handle == "@charlidamelio"


def test_resolve_handles_full():
    """Full resolve_cross_account_handles() — backfills cross-platform handles via mocked DDG."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        influencers = [
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
            Influencer(name="Joe Wicks", handles={Platform.TikTok: "thebodycoach"},
                       source_urls={"a.com", "b.com"}),  # Cross-platform: needs IG
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),  # Already has target
            Influencer(name="Sarah Thompson", handles={}),  # Name-only — deferred to tracker
        ]

        def mock_text(query, **kwargs):
            if "Joe Wicks" in query:
                return [{"href": "https://www.instagram.com/thebodycoach/", "title": "Joe Wicks", "body": ""}]
            return [{"href": "https://somesite.com/random", "title": "No match", "body": ""}]

        with patch.object(svc._ddgs, "text", side_effect=mock_text):
            result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram)

        # 4 original + 1 new IG entry for Joe = 5
        assert len(result) == 5, f"Expected 5, got {len(result)}"

        # Joe Wicks should have new IG entry added alongside original TT
        joe_entries = [r for r in result if r.name == "Joe Wicks"]
        assert len(joe_entries) == 2, "Joe should have TT original + IG new"
        ig_joe = next(r for r in joe_entries if Platform.Instagram in r.handles)
        assert ig_joe.handles[Platform.Instagram] == "thebodycoach"

        # Name-only entries are NOT touched by resolve_cross_account_handles
        name_only = next(r for r in result if not r.handles)
        assert name_only.name == "Sarah Thompson", "Name-only should keep its name"


def test_enrich_cross_platform_handle():
    """Cross-platform handles should be KEPT as-is, with a new target-platform
    entry added alongside them — NOT overwritten."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        influencers = [
            Influencer(name="Adam Maxted", handles={Platform.YouTube: "adammaxted2262"}),
            Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),  # Already correct
        ]

        def mock_text(query, **kwargs):
            if "Adam Maxted" in query:
                return [{"href": "https://www.instagram.com/adammaxted/", "title": "Adam Maxted IG", "body": ""}]
            return [{"href": "https://somesite.com/random", "title": "No match", "body": ""}]

        with patch.object(svc._ddgs, "text", side_effect=mock_text):
            result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, min_sources=0)

        # Adam should now have TWO entries: YouTube (original) + Instagram (new)
        adam_entries = [r for r in result if r.name == "Adam Maxted"]
        assert len(adam_entries) == 2, (
            f"Expected 2 entries for Adam (YT + IG), got {len(adam_entries)}: "
            f"{[e.handles for e in adam_entries]}"
        )

        # Original YouTube entry untouched
        yt_adam = next((r for r in adam_entries if Platform.YouTube in r.handles), None)
        assert yt_adam is not None, "Original YouTube entry was lost"
        assert yt_adam.handles[Platform.YouTube] == "adammaxted2262", "YouTube handle was modified"

        # New Instagram entry added
        ig_adam = next((r for r in adam_entries if Platform.Instagram in r.handles), None)
        assert ig_adam is not None, "Instagram entry was not added"
        assert ig_adam.handles[Platform.Instagram] == "adammaxted", (
            f"Expected adammaxted, got {ig_adam.handles}"
        )

        # Kayla should remain unchanged (already correct platform)
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
    # All three platforms should be merged into ONE entry
    assert len(result) == 1, (
        f"Expected 1 merged entry, got {len(result)}: "
        f"{[r.handles for r in result]}"
    )
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
    assert len(result) == 1, (
        f"Expected 1 entry (deduped), got {len(result)}"
    )


def test_enrich_keeps_cross_platform_adds_target():
    """Full resolve_cross_account_handles flow: TikTok entry in → TikTok + Instagram out."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        influencers = [
            Influencer(name="Tom Hardy", handles={Platform.TikTok: "@testperson"}),
        ]

        def mock_text(query, **kwargs):
            if "Tom Hardy" in query:
                return [{"href": "https://www.instagram.com/testperson_ig/",
                         "title": "Test Person IG", "body": ""}]
            return []

        with patch.object(svc._ddgs, "text", side_effect=mock_text):
            result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, min_sources=0)

        assert len(result) == 2, (
            f"Expected 2 (TT kept + IG added), got {len(result)}: "
            f"{[r.handles for r in result]}"
        )

        tt = next(r for r in result if Platform.TikTok in r.handles)
        assert tt.handles[Platform.TikTok] == "@testperson", "TikTok handle was modified"

        ig = next(r for r in result if Platform.Instagram in r.handles)
        assert ig.handles[Platform.Instagram] == "testperson_ig", (
            f"Expected testperson_ig, got {ig.handles}"
        )


def test_skip_cross_platform_lookup():
    """skip_cross_platform=True skips DDG for cross-platform handles but still enriches name-only."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        influencers = [
            Influencer(name="Mike Chen", handles={Platform.TikTok: "@tiktoker"}),
            Influencer(name="Laura Smith", handles={}),
        ]

        def mock_text(query, **kwargs):
            if "Laura Smith" in query:
                return [{"href": "https://www.instagram.com/nameonly/", "title": "", "body": ""}]
            if "Mike Chen" in query:
                return [{"href": "https://www.instagram.com/tiktoker_ig/", "title": "", "body": ""}]
            return []

        with patch.object(svc._ddgs, "text", side_effect=mock_text) as mock_ddgs:
            result = svc.resolve_cross_account_handles(influencers, platform=Platform.Instagram, skip_cross_platform=True)

        # "Has TikTok" should NOT have been looked up — kept as-is
        tt = next(r for r in result if r.name == "Mike Chen")
        assert Platform.TikTok in tt.handles
        assert tt.handles[Platform.TikTok] == "@tiktoker"
        # No new IG entry added for them
        assert sum(1 for r in result if r.name == "Mike Chen") == 1

        # Name-only entries are NOT resolved via resolve_cross_account_handles (deferred to tracker)
        name_only = next(r for r in result if r.name == "Laura Smith")
        assert not name_only.handles, "Name-only entries should NOT be enriched by resolve_cross_account_handles"

        # DDG should NOT have been called (skip_cross_platform=True)
        assert mock_ddgs.call_count == 0


def test_resolve_handles_frequency_cap():
    """Only top N by source frequency get DDG'd, entries below min_sources skipped."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        # Create 4 cross-platform entries with varying source_urls counts
        influencers = [
            Influencer(name="Anna Brown", handles={Platform.TikTok: "low"},
                       source_urls={"a.com"}),  # 1 source — below threshold
            Influencer(name="David Clark", handles={Platform.TikTok: "medium"},
                       source_urls={"a.com", "b.com"}),  # 2 sources
            Influencer(name="Emily Wright", handles={Platform.TikTok: "highfreq"},
                       source_urls={"a.com", "b.com", "c.com", "d.com"}),  # 4 sources
            Influencer(name="James Parker", handles={Platform.TikTok: "alsohigh"},
                       source_urls={"a.com", "b.com", "c.com"}),  # 3 sources
        ]

        ddg_calls = []
        def mock_text(query, **kwargs):
            ddg_calls.append(query)
            return [{"href": "https://www.instagram.com/found/", "title": "", "body": ""}]

        with patch.object(svc._ddgs, "text", side_effect=mock_text):
            # max_lookups=2 and min_sources=2
            svc.resolve_cross_account_handles(
                influencers, platform=Platform.Instagram,
                max_lookups=2, min_sources=2,
            )

        # Should have queried only top 2 by frequency: "High Freq" (4) and "Also High" (3)
        assert len(ddg_calls) == 2, f"Expected 2 DDG calls, got {len(ddg_calls)}: {ddg_calls}"
        assert any("Emily Wright" in q for q in ddg_calls), "Emily Wright should have been DDG'd"
        assert any("James Parker" in q for q in ddg_calls), "James Parker should have been DDG'd"
        # "Anna Brown" (1 source) should NOT have been DDG'd
        assert not any("Anna Brown" in q for q in ddg_calls), "Anna Brown should NOT be DDG'd"
        # "David Clark" (2 sources) qualifies but was capped out
        assert not any("David Clark" in q for q in ddg_calls), "David Clark was capped (only top 2 by frequency)"

# ── _needs_resolution() — per-platform logic ──

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




# ── Engine rotation kwargs ──

def test_search_handle_forwards_backend_and_region():
    """_search_handle should pass backend= and region= to DDGS.text()."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = NameToHandleService(audit, delay_seconds=0)

        mock_results = [
            {
                "href": "https://www.instagram.com/kayla_itsines/",
                "title": "Kayla Itsines",
                "body": "",
            }
        ]

        with (
            patch.object(svc._ddgs, "text", return_value=mock_results) as mock_text,
            patch("services.enrichment.NameToHandleService.SEARCH_BACKEND", "duckduckgo,brave"),
            patch("services.enrichment.NameToHandleService.SEARCH_REGION", "de-de"),
        ):
            svc._search_handle("Kayla Itsines", Platform.Instagram, "instagram.com")

        _, kwargs = mock_text.call_args
        assert kwargs["backend"] == "duckduckgo,brave"
        assert kwargs["region"] == "de-de"
