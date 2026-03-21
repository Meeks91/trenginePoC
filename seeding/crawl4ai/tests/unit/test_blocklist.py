"""
Unit Tests: Shared Blocklist
==============================
Tests for blocklist wiring, constant integrity, and end-to-end blocking
at both injection sites: RegexHandleExtractor and InfluencerMerger.filter_blocked().

The blocklist is defined once in RegexHandleExtractor and must be used
consistently at both sites.
"""

from config.schema import Influencer, Platform
from services.extraction.RegexHandleExtractor import (
    _IGNORE_HANDLES,
    _IGNORE_SUBSTRINGS,
    _IGNORE_PREFIXES,
    _is_valid_handle,
    extract_handles_from_html,
)
from services.influencerMerging.InfluencerMergerService import InfluencerMergerService as InfluencerMerger
from unittest.mock import MagicMock


# ══════════════════════════════════════════════════════════════════════
# Wiring: Both sites use the same blocklist
# ══════════════════════════════════════════════════════════════════════

def test_regex_extractor_uses_shared_blocklist():
    """Every handle in _IGNORE_HANDLES must be rejected by _is_valid_handle."""
    for handle in list(_IGNORE_HANDLES)[:20]:
        assert not _is_valid_handle(handle), f"{handle} should be blocked by regex extractor"


def test_merger_uses_shared_blocklist():
    """Every handle in _IGNORE_HANDLES must be blocked by filter_blocked."""
    for handle in list(_IGNORE_HANDLES)[:20]:
        influencer = Influencer(name="X", handles={Platform.Instagram: handle})
        result = InfluencerMerger.filter_blocked([influencer])
        assert len(result) == 0, f"{handle} should be blocked by merger"


def test_both_sites_use_same_is_blocked_handle():
    """InfluencerMerger imports is_blocked_handle from RegexHandleExtractor."""
    from services.influencerMerging import InfluencerMergerService as merger_mod
    from services.extraction import RegexHandleExtractor as regex_mod
    assert merger_mod.is_blocked_handle is regex_mod.is_blocked_handle


# ══════════════════════════════════════════════════════════════════════
# Constant integrity: one big test against the combined _IGNORE_HANDLES
# ══════════════════════════════════════════════════════════════════════

def test_ignore_handles_total_count():
    """Combined blocklist has exactly 587 entries."""
    assert len(_IGNORE_HANDLES) == 587, \
        f"Expected 587 entries in _IGNORE_HANDLES, got {len(_IGNORE_HANDLES)}"


def test_ignore_substrings_contains_profanity():
    """_IGNORE_SUBSTRINGS must contain core profanity terms."""
    for term in ("uncensored", "fuck", "shit", "sex", "porn", "fart", "booty"):
        assert term in _IGNORE_SUBSTRINGS, f"Missing profanity term: {term}"
    assert len(_IGNORE_SUBSTRINGS) == 41, \
        f"Expected 41 substring entries, got {len(_IGNORE_SUBSTRINGS)}"


def test_ignore_prefixes_exact():
    assert _IGNORE_PREFIXES == ("utm_", "ig_", "ref=", "img_", "case-study-")


def test_ignore_handles_contains_known_brands():
    """Spot-check: key entries must be present."""
    expected_present = {
        "foxnews", "cnn", "bbc", "nike", "adidas", "google", "apple",
        "microsoft", "amazon", "netflix", "disney", "spotify",
        "5newsuk", "nbcnews",
    }
    for entry in expected_present:
        assert entry in _IGNORE_HANDLES, f"Missing expected entry: {entry}"


def test_ignore_handles_contains_path_segments():
    """Spot-check: path segments must be present."""
    expected_present = {
        "login", "signup", "search", "feed", "embed",
    }
    for entry in expected_present:
        assert entry in _IGNORE_HANDLES, f"Missing expected path segment: {entry}"


def test_ignore_handles_contains_influencer_hero():
    """influencer-hero must be in aggregator blocklist."""
    assert "influencer-hero" in _IGNORE_HANDLES
    assert "influencerhero" in _IGNORE_HANDLES


# ══════════════════════════════════════════════════════════════════════
# Smoke: Regex extraction site
# ══════════════════════════════════════════════════════════════════════

def test_regex_blocks_news_handle():
    """HTML with @5newsuk link → not in extracted handles."""
    html = '<a href="https://youtube.com/@5newsuk">5NewsUK</a>'
    handles = extract_handles_from_html(html)
    assert not any(h.handle.lower() == "5newsuk" for h in handles), \
        "5newsuk should be blocked by regex extractor"


def test_regex_blocks_profanity_handles():
    """Profanity substring handles must be blocked."""
    test_cases = [
        ("fartman_1738", "fart"),
        ("bigbootyms2shiesty", "booty"),
        ("sexygirl23", "sex"),
        ("pornhub_official", "porn"),
    ]
    for handle, reason in test_cases:
        html = f'<a href="https://tiktok.com/@{handle}">{handle}</a>'
        handles = extract_handles_from_html(html)
        assert not any(h.handle.lower() == handle for h in handles), \
            f"{handle} should be blocked (contains '{reason}')"


def test_regex_blocks_case_study_prefix():
    """Handles starting with case-study- must be blocked."""
    html = '<a href="https://instagram.com/case-study-tcl">TCL</a>'
    handles = extract_handles_from_html(html)
    assert not any(h.handle.lower() == "case-study-tcl" for h in handles), \
        "case-study-tcl should be blocked by prefix filter"


def test_regex_blocks_uncensored_substring():
    """Substring filter: 'uncensored' anywhere in handle → blocked."""
    html = '<a href="https://youtube.com/@uncensoredpodcast">Pod</a>'
    handles = extract_handles_from_html(html)
    assert not any("uncensored" in h.handle.lower() for h in handles), \
        "uncensored substring should be blocked"


# ══════════════════════════════════════════════════════════════════════
# Smoke: Post-dedup merger site (filter_blocked)
# ══════════════════════════════════════════════════════════════════════

def test_merger_blocks_news_handle():
    """foxnews handle → filtered out by filter_blocked."""
    entries = [Influencer(name="Fox", handles={Platform.YouTube: "foxnews"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 0, "foxnews should be blocked by merger"


def test_merger_blocks_uncensored_substring():
    """Substring filter also works at merger level."""
    entries = [Influencer(name="Pod", handles={Platform.YouTube: "uncensoredpod"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 0


def test_merger_allows_non_blocked():
    """Non-blocked handle passes through."""
    entries = [Influencer(name="Matt Wolfe", handles={Platform.YouTube: "mattwolfe"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 1, "mattwolfe should NOT be blocked"


def test_merger_blocks_on_any_platform():
    """If ANY handle (ig/tk/yt) is blocked, the entry is removed."""
    entries = [
        Influencer(name="X", handles={
            Platform.Instagram: "foxnews",
            Platform.YouTube: "legit_handle",
        }, most_seen_category="AI"),
    ]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 0, "Entry with any blocked handle should be removed"


# ══════════════════════════════════════════════════════════════════════
# Handleless influencer filtering
# ══════════════════════════════════════════════════════════════════════

def test_handleless_influencer_filtered():
    """Name-only influencer (no handles) → excluded by filter_blocked."""
    entries = [Influencer(name="Evelina Khanoyan", handles={}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 0, f"Expected 0 results for handleless entry, got {len(result)}"


def test_influencer_with_handle_kept():
    """Influencer with at least one handle → kept."""
    entries = [Influencer(name="Andrew Ng", handles={Platform.Instagram: "andrewyng"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries)
    assert len(result) == 1
    assert result[0].ig_handle == "andrewyng"


def test_filter_blocked_calls_injected_handle_filter():
    """Verify filter_blocked() calls the injected handle_filter (DI wiring test)."""
    mock_filter = MagicMock(return_value=False)
    entries = [Influencer(name="X", handles={Platform.Instagram: "test_handle"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries, handle_filter=mock_filter)
    assert mock_filter.called, "handle_filter should have been called"
    assert len(result) == 1


def test_filter_blocked_injected_filter_can_block():
    """Injected filter returning True → entry is blocked."""
    def always_block(h: str) -> bool:
        return True
    entries = [Influencer(name="X", handles={Platform.Instagram: "anything"}, most_seen_category="AI")]
    result = InfluencerMerger.filter_blocked(entries, handle_filter=always_block)
    assert len(result) == 0
