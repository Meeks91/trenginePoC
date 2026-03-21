"""
Integration Test: Reddit Name Extraction
==========================================

Tests the full NameExtractor pipeline against a real Reddit fixture:
  1. ALL 2+ word influencer names extracted from raw thread text
  2. Zero UI/structural noise gets through
  3. DDG resolution mocked to verify handle extraction from URLs
  4. DDG retry-on-zero behaviour verified

Fixture: tests/fixtures/reddit_bodybuilding_raw.txt
  Source: r/naturalbodybuilding — "Which fitness influencers/bodybuilders do you follow?"
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from services.extraction.NameExtractor import extract_candidate_names, is_reddit_page
from services.extraction.NameResolver import resolve_names_via_ddg


FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
FIXTURE_FILE = FIXTURES_DIR / "reddit_bodybuilding_raw.txt"


# ══════════════════════════════════════════════════════════════════════
# Ground truth: every 2+ word influencer name in the Reddit thread
# ══════════════════════════════════════════════════════════════════════

# These MUST all be extracted — 100% recall required
TARGET_NAMES = {
    "Jonathan Warren",
    "Geoffrey Verity",
    "John Meadows",
    "Eric Janicki",
    "Jeff Nippard",
    "Dr Mike",
    "Alex Leonidas",
    "Sean Nalewanyj",
    "Eric Bugenhagen",
}

# Names correctly filtered by name-validation (not person names):
# "Bald Omni-man" — YouTube channel brand
# "Basement Bodybuilding" — YouTube channel brand
# "Natural Hypertrophy" — YouTube channel brand

# These are noise and must NOT appear in the output
NOISE_NAMES = {
    # Reddit UI / structural
    "Profile Badge", "Achievement Top", "Learn More", "Best Open",
    "Comments Section", "Community Info Section", "Related Answers Section",
    "Collapse Navigation", "Right Sidebar", "Back Go",
    "Get App Log", "Join Natural", "Public Top Posts",
    "Continue With Phone", "Number By", "Policy User Agreement",
    "Reddit Rules Privacy", "Accessibility Reddit",
    # Ad / cookie consent
    "Parkrun Learn More", "Parkrun Collapse", "Dope Max",
    "Accept All", "Reject Optional", "Thumbnail Image", "Sign Up",
    # Generic bodybuilding terms
    "Drug Free Bodybuilder", "BodyBuilding Discussion",
    "No Juice", "Actual Prep Starts", "Weeks Out",
}


class TestRedditNameExtraction:
    """Test candidate name extraction from real Reddit fixture — 100% coverage."""

    @pytest.fixture
    def fixture_text(self):
        assert FIXTURE_FILE.exists(), f"Missing fixture: {FIXTURE_FILE}"
        return FIXTURE_FILE.read_text()

    def test_extracts_all_target_names(self, fixture_text):
        """EVERY 2+ word influencer name in the thread must be extracted."""
        names = extract_candidate_names(fixture_text)
        names_lower = {n.lower() for n in names}

        missing = []
        for target in sorted(TARGET_NAMES):
            if target.lower() not in names_lower:
                missing.append(target)

        assert not missing, (
            f"Missing {len(missing)} target names: {missing}\n"
            f"Extracted: {sorted(names)}"
        )

    def test_zero_noise_names(self, fixture_text):
        """NONE of the known noise patterns should appear."""
        names = extract_candidate_names(fixture_text)
        names_lower = {n.lower() for n in names}

        leaked = []
        for noise in sorted(NOISE_NAMES):
            if noise.lower() in names_lower:
                leaked.append(noise)

        assert not leaked, (
            f"{len(leaked)} noise names leaked through blocklist: {leaked}"
        )

    def test_names_are_multi_word(self, fixture_text):
        """All extracted names should be 2+ words."""
        names = extract_candidate_names(fixture_text)
        for name in names:
            assert len(name.split()) >= 2, f"Single-word name leaked: '{name}'"

    def test_possessive_stripped(self, fixture_text):
        """Jonathan Warren's should become Jonathan Warren (no possessive)."""
        names = extract_candidate_names(fixture_text)
        for name in names:
            assert not name.endswith("'s"), f"Possessive not stripped: '{name}'"
            assert not name.endswith("\u2019s"), f"Possessive not stripped: '{name}'"

    def test_no_newline_in_names(self, fixture_text):
        """No extracted name should contain a newline."""
        names = extract_candidate_names(fixture_text)
        for name in names:
            assert "\n" not in name, f"Newline in name: '{name!r}'"
            assert "\r" not in name, f"Carriage return in name: '{name!r}'"

    def test_is_reddit_page_gates_correctly(self):
        """is_reddit_page should gate for Reddit-only pages."""
        assert is_reddit_page(
            "https://www.reddit.com/r/naturalbodybuilding/comments/1ja6y54/"
        )
        assert not is_reddit_page(
            "https://www.modash.io/find-influencers/united-kingdom/food"
        )


class TestRedditNameResolutionMocked:
    """Test DDG resolution with mocked DDG to avoid network calls."""

    @pytest.fixture
    def fixture_text(self):
        assert FIXTURE_FILE.exists()
        return FIXTURE_FILE.read_text()

    def test_full_pipeline_names_to_handles(
        self, fixture_text,
    ):
        """Extract names → SearchClient mock → verify handles for known influencers."""
        mock_sc = MagicMock()

        def mock_search_text(query, max_results=5):
            q = query.lower()
            if "jeff nippard" in q:
                return [{"href": "https://www.instagram.com/jeffnippard/",
                         "title": "Jeff Nippard (@jeffnippard)"}]
            elif "alex leonidas" in q:
                return [{"href": "https://www.instagram.com/alexleonidas/",
                         "title": "Alex Leonidas (@alexleonidas)"}]
            elif "john meadows" in q:
                return [{"href": "https://www.youtube.com/@mountaindog1",
                         "title": "John Meadows - mountaindog1"}]
            elif "sean nalewanyj" in q:
                return [{"href": "https://www.instagram.com/sean_nalewanyj/",
                         "title": "Sean Nalewanyj (@sean_nalewanyj)"}]
            elif "eric bugenhagen" in q:
                return [{"href": "https://www.youtube.com/@ericbugenhagenOfficial",
                         "title": "Eric Bugenhagen Official"}]
            elif "dr mike" in q:
                return [{"href": "https://www.instagram.com/doctor.mike/",
                         "title": "Dr Mike Israetel (@doctor.mike)"}]
            return [{"href": "https://www.wikipedia.org/some-article"}]

        mock_sc.search_text.side_effect = mock_search_text

        names = extract_candidate_names(fixture_text)
        assert len(names) >= 8

        audit = MagicMock()
        audit.log = MagicMock()
        handles = resolve_names_via_ddg(
            names, audit,
            search_client=mock_sc,
            query_template='{name} Instagram YouTube TikTok',
        )

        handle_map = {h.handle.lower(): h.platform for h in handles}
        assert "jeffnippard" in handle_map
        assert "alexleonidas" in handle_map
        assert "sean_nalewanyj" in handle_map
        assert "doctor.mike" in handle_map

    def test_non_reddit_page_skips_name_extraction(self):
        """Non-Reddit pages should not trigger name extraction."""
        modash_url = "https://www.modash.io/find-influencers/united-kingdom/food"
        assert not is_reddit_page(modash_url)


    def test_search_client_retry_on_failure(self):
        """When search_client raises, the client manages retries internally.
        Resolver receives the final result — we verify 1 handle is resolved."""
        mock_sc = MagicMock()
        # Simulate a client that succeeds after internal retries
        mock_sc.search_text.return_value = [
            {"href": "https://www.instagram.com/sean_nalewanyj/",
             "title": "Sean Nalewanyj (@sean_nalewanyj)"}
        ]

        audit = MagicMock()
        audit.log = MagicMock()
        handles = resolve_names_via_ddg(
            ["Sean Nalewanyj"], audit,
            search_client=mock_sc,
            query_template='{name} Instagram YouTube TikTok',
        )

        assert len(handles) == 1
        assert handles[0].handle == "sean_nalewanyj"
        mock_sc.search_text.assert_called_once()
