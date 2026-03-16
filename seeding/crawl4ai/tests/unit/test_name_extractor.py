"""
Unit tests for NameExtractor — regex-based candidate name extraction.
"""

import pytest
from services.extraction.NameExtractor import extract_candidate_names, is_reddit_page


# ══════════════════════════════════════════════════════════════════════
# extract_candidate_names
# ══════════════════════════════════════════════════════════════════════

class TestExtractCandidateNames:
    """Test the regex name extraction logic."""

    def test_two_word_names(self):
        text = "I really like Alex Leonidas and Jeff Nippard for form tips."
        names = extract_candidate_names(text)
        assert "Alex Leonidas" in names
        assert "Jeff Nippard" in names

    def test_three_word_names_rejected(self):
        """Three-word sequences should NOT be matched — regex requires exactly 2."""
        text = "Check out Bald Omni Man for bodybuilding content."
        names = extract_candidate_names(text)
        assert "Bald Omni Man" not in names
        assert "Bald Omni" in names

    def test_single_words_skipped(self):
        """Single capitalized words should NOT be extracted as names."""
        text = "I watch Nippard and sometimes AthleanX"
        names = extract_candidate_names(text)
        assert "Nippard" not in names
        assert "AthleanX" not in names

    def test_blocklist_filtered(self):
        """Common phrases in the blocklist should be skipped."""
        text = "In New York and the United States there are many influencers."
        names = extract_candidate_names(text)
        blocklisted = {"New York", "United States"}
        for name in names:
            assert name not in blocklisted, f"Blocklisted name leaked: {name}"

    def test_dedup_case_insensitive(self):
        """Same name appearing multiple times should be deduplicated."""
        text = (
            "He thinks Jeff Nippard is great. I agree that Jeff Nippard has the best tips."
        )
        names = extract_candidate_names(text)
        jeff_count = sum(1 for n in names if "jeff nippard" in n.lower())
        assert jeff_count == 1, f"Expected 1 Jeff Nippard, got {jeff_count}"

    def test_max_cap_respected(self):
        """Should cap at max_names."""
        # Generate text with many capitalized name pairs
        text = " ".join(f"Person{i} Name{i}" for i in range(30))
        names = extract_candidate_names(text, max_names=5)
        assert len(names) <= 5

    def test_hyphenated_names(self):
        """Names with hyphens should be captured."""
        text = "Bald Omni-Man is one of the best creators."
        names = extract_candidate_names(text)
        matching = [n for n in names if "Omni" in n and "Man" in n]
        assert len(matching) >= 1, f"Expected hyphenated name, got {names}"

    def test_apostrophe_names(self):
        """Names with apostrophes should be captured."""
        text = "What about Ryan O'Brien and his form videos?"
        names = extract_candidate_names(text)
        matching = [n for n in names if "Brien" in n]
        assert len(matching) >= 1, f"Expected apostrophe name, got {names}"

    def test_empty_text(self):
        assert extract_candidate_names("") == []
        assert extract_candidate_names(None) == []

    def test_no_capitalized_sequences(self):
        """Text with no capitalized sequences returns empty."""
        text = "i like watching fitness content on youtube and reddit"
        assert extract_candidate_names(text) == []

    def test_short_names_skipped(self):
        """Names shorter than 4 characters should be skipped."""
        text = "By Mr X and also Dr Y"
        names = extract_candidate_names(text)
        short = [n for n in names if len(n) < 4]
        assert not short, f"Short names leaked: {short}"


# ══════════════════════════════════════════════════════════════════════
# is_reddit_page
# ══════════════════════════════════════════════════════════════════════

class TestIsRedditPage:

    def test_reddit_url_detected(self):
        assert is_reddit_page("https://www.reddit.com/r/naturalbodybuilding/comments/1ja6y54/") is True

    def test_old_reddit_detected(self):
        assert is_reddit_page("https://old.reddit.com/r/fitness/") is True

    def test_non_reddit_skipped(self):
        assert is_reddit_page("https://www.modash.io/find-influencers/") is False

    def test_empty_url(self):
        assert is_reddit_page("") is False

    def test_reddit_search_detected(self):
        assert is_reddit_page("https://www.reddit.com/search/?q=Jeff+Nippard") is True

