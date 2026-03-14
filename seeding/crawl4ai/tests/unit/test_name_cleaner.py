"""
test_name_cleaner — Full rule coverage for NameCleaner.

Tests every cleanup rule: markdown strip, number prefix, URL decode,
country/brand/news rejection, LinkedIn slug rejection, valid names pass.
"""

import pytest

from services.extraction.NameCleaner import NameCleaner


class TestCleanName:
    """NameCleaner.clean_name() tests."""

    # ── Markdown stripping ──

    def test_strips_bold_markdown(self):
        assert NameCleaner.clean_name("**Amanda Cerny**") == "Amanda Cerny"

    def test_strips_markdown_link(self):
        assert NameCleaner.clean_name("[Andrej Karpathy](https://example.com)") == "Andrej Karpathy"

    def test_strips_bold_inside_link(self):
        assert NameCleaner.clean_name("[**Joe Wicks**](https://youtube.com/@joewicks)") == "Joe Wicks"

    # ── Number prefix stripping ──

    def test_strips_dot_prefix(self):
        assert NameCleaner.clean_name("1. Martha Stewart") == "Martha Stewart"

    def test_strips_paren_prefix(self):
        assert NameCleaner.clean_name("23) Jane Fonda") == "Jane Fonda"

    def test_strips_dash_prefix(self):
        assert NameCleaner.clean_name("5- Gordon Ramsay") == "Gordon Ramsay"

    # ── URL-encoded strings ──

    def test_rejects_url_encoded_garbled(self):
        assert NameCleaner.clean_name("%D7%A6%D7%99%D7%A4") is None

    def test_decodes_url_encoded_valid(self):
        result = NameCleaner.clean_name("Ren%C3%A9e Zellweger")
        assert result == "Renée Zellweger"

    # ── Non-person rejection: brands ──

    def test_rejects_brand_canva(self):
        assert NameCleaner.clean_name("Canva") is None

    def test_rejects_brand_capcut(self):
        assert NameCleaner.clean_name("CapCut") is None

    def test_rejects_brand_peloton(self):
        assert NameCleaner.clean_name("Peloton") is None

    def test_rejects_brand_nike_training_club(self):
        assert NameCleaner.clean_name("Nike Training Club") is None

    def test_rejects_brand_myfitnesspal(self):
        assert NameCleaner.clean_name("MyFitnessPal") is None

    # ── Non-person rejection: countries ──

    def test_rejects_country_bangladesh(self):
        assert NameCleaner.clean_name("Bangladesh") is None

    def test_rejects_country_united_states(self):
        assert NameCleaner.clean_name("United States") is None

    def test_rejects_country_south_korea(self):
        assert NameCleaner.clean_name("South Korea") is None

    # ── Non-person rejection: news orgs ──

    def test_rejects_news_org_forbes(self):
        assert NameCleaner.clean_name("Forbes") is None

    def test_rejects_news_org_techcrunch(self):
        assert NameCleaner.clean_name("TechCrunch") is None

    def test_rejects_news_org_bbc(self):
        assert NameCleaner.clean_name("BBC") is None

    # ── Non-person rejection: generic phrases ──

    def test_rejects_generic_content_creator(self):
        assert NameCleaner.clean_name("Content Creator") is None

    # ── Valid names pass through ──

    def test_valid_name_passes(self):
        assert NameCleaner.clean_name("Joe Wicks") == "Joe Wicks"

    def test_valid_name_with_hyphen(self):
        assert NameCleaner.clean_name("Emma Storey-Gordon") == "Emma Storey-Gordon"

    def test_valid_name_with_spaces(self):
        assert NameCleaner.clean_name("  Kayla Itsines  ") == "Kayla Itsines"

    # ── Edge cases ──

    def test_empty_string_returns_none(self):
        assert NameCleaner.clean_name("") is None

    def test_whitespace_only_returns_none(self):
        assert NameCleaner.clean_name("   ") is None

    def test_none_input_raises_or_returns_none(self):
        assert NameCleaner.clean_name(None) is None  # type: ignore


class TestIsValidHandle:
    """NameCleaner.is_valid_handle() tests."""

    def test_valid_handle(self):
        assert NameCleaner.is_valid_handle("courtneyblack") is True

    def test_valid_handle_with_underscore(self):
        assert NameCleaner.is_valid_handle("kayla_itsines") is True

    def test_rejects_linkedin_slug(self):
        assert NameCleaner.is_valid_handle("fei-fei-li-4541247") is False

    def test_rejects_path_with_slash(self):
        assert NameCleaner.is_valid_handle("user/profile") is False

    def test_rejects_empty(self):
        assert NameCleaner.is_valid_handle("") is False
