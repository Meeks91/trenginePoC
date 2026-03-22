"""
test_name_cleaner — Full rule coverage for NameCleaner.

Tests every cleanup rule: markdown strip, number prefix, URL decode,
country/brand/news rejection, LinkedIn slug rejection, valid names pass.
"""


from services.extraction.NameCleanerService import NameCleanerService


class TestCleanName:
    """NameCleaner.clean_name() tests."""

    # ── Markdown stripping ──

    def test_strips_bold_markdown(self):
        assert NameCleanerService.clean_name("**Amanda Cerny**") == "Amanda Cerny"

    def test_strips_markdown_link(self):
        assert NameCleanerService.clean_name("[Andrej Karpathy](https://example.com)") == "Andrej Karpathy"

    def test_strips_bold_inside_link(self):
        assert NameCleanerService.clean_name("[**Joe Wicks**](https://youtube.com/@joewicks)") == "Joe Wicks"

    # ── Number prefix stripping ──

    def test_strips_dot_prefix(self):
        assert NameCleanerService.clean_name("1. Martha Stewart") == "Martha Stewart"

    def test_strips_paren_prefix(self):
        assert NameCleanerService.clean_name("23) Jane Fonda") == "Jane Fonda"

    def test_strips_dash_prefix(self):
        assert NameCleanerService.clean_name("5- Gordon Ramsay") == "Gordon Ramsay"

    # ── URL-encoded strings ──

    def test_rejects_url_encoded_garbled(self):
        assert NameCleanerService.clean_name("%D7%A6%D7%99%D7%A4") is None

    def test_decodes_url_encoded_valid(self):
        result = NameCleanerService.clean_name("Ren%C3%A9e Zellweger")
        assert result == "Renée Zellweger"

    # ── Non-person rejection: brands ──

    def test_rejects_brand_canva(self):
        assert NameCleanerService.clean_name("Canva") is None

    def test_rejects_brand_capcut(self):
        assert NameCleanerService.clean_name("CapCut") is None

    def test_rejects_brand_peloton(self):
        assert NameCleanerService.clean_name("Peloton") is None

    def test_rejects_brand_nike_training_club(self):
        assert NameCleanerService.clean_name("Nike Training Club") is None

    def test_rejects_brand_myfitnesspal(self):
        assert NameCleanerService.clean_name("MyFitnessPal") is None

    # ── Non-person rejection: countries ──

    def test_rejects_country_bangladesh(self):
        assert NameCleanerService.clean_name("Bangladesh") is None

    def test_rejects_country_united_states(self):
        assert NameCleanerService.clean_name("United States") is None

    def test_rejects_country_south_korea(self):
        assert NameCleanerService.clean_name("South Korea") is None

    # ── Non-person rejection: news orgs ──

    def test_rejects_news_org_forbes(self):
        assert NameCleanerService.clean_name("Forbes") is None

    def test_rejects_news_org_techcrunch(self):
        assert NameCleanerService.clean_name("TechCrunch") is None

    def test_rejects_news_org_bbc(self):
        assert NameCleanerService.clean_name("BBC") is None

    # ── Non-person rejection: generic phrases ──

    def test_rejects_generic_content_creator(self):
        assert NameCleanerService.clean_name("Content Creator") is None

    # ── Valid names pass through ──

    def test_valid_name_passes(self):
        assert NameCleanerService.clean_name("Joe Wicks") == "Joe Wicks"

    def test_valid_name_with_hyphen(self):
        assert NameCleanerService.clean_name("Emma Storey-Gordon") == "Emma Storey-Gordon"

    def test_valid_name_with_spaces(self):
        assert NameCleanerService.clean_name("  Kayla Itsines  ") == "Kayla Itsines"

    # ── Edge cases ──

    def test_empty_string_returns_none(self):
        assert NameCleanerService.clean_name("") is None

    def test_whitespace_only_returns_none(self):
        assert NameCleanerService.clean_name("   ") is None

    def test_none_input_raises_or_returns_none(self):
        assert NameCleanerService.clean_name(None) is None


class TestIsValidHandle:
    """NameCleaner.is_valid_handle() tests."""

    def test_valid_handle(self):
        assert NameCleanerService.is_valid_handle("courtneyblack") is True

    def test_valid_handle_with_underscore(self):
        assert NameCleanerService.is_valid_handle("kayla_itsines") is True

    def test_rejects_linkedin_slug(self):
        assert NameCleanerService.is_valid_handle("fei-fei-li-4541247") is False

    def test_rejects_path_with_slash(self):
        assert NameCleanerService.is_valid_handle("user/profile") is False

    def test_rejects_empty(self):
        assert NameCleanerService.is_valid_handle("") is False


class TestBlocklistAdditions:
    """Regression tests for blocklist additions (2026-03-17)."""

    # ── Generic job titles ──

    def test_rejects_personal_trainer(self):
        assert NameCleanerService.clean_name("Personal Trainer") is None

    def test_rejects_fitness_model(self):
        assert NameCleanerService.clean_name("Fitness Model") is None

    def test_rejects_yoga_teacher(self):
        assert NameCleanerService.clean_name("Yoga Teacher") is None

    def test_rejects_brand_ambassador(self):
        assert NameCleanerService.clean_name("Brand Ambassador") is None

    # ── Min-length check (≤3 chars rejected) ──

    def test_rejects_short_name_the(self):
        assert NameCleanerService.clean_name("The") is None

    def test_accepts_four_char_name(self):
        assert NameCleanerService.clean_name("Emi Wong") == "Emi Wong"


class TestNerValidation:
    """NER validation gate — rejects non-PERSON entities that bypass blocklists."""

    # ── Noise that previously slipped through ──

    def test_rejects_non_person_media_post(self):
        assert NameCleanerService.clean_name("Media Post") is None

    def test_rejects_non_person_world_record(self):
        assert NameCleanerService.clean_name("World Record") is None

    def test_rejects_non_person_fat_loss(self):
        assert NameCleanerService.clean_name("Fat Loss") is None

    def test_rejects_non_person_state_university(self):
        assert NameCleanerService.clean_name("State University") is None

    def test_rejects_non_person_questions_thread(self):
        assert NameCleanerService.clean_name("Questions Thread") is None

    # ── Real person names still pass ──

    def test_accepts_real_person_jeff_nippard(self):
        assert NameCleanerService.clean_name("Jeff Nippard") == "Jeff Nippard"

    def test_accepts_real_person_stefi_cohen(self):
        assert NameCleanerService.clean_name("Stefi Cohen") == "Stefi Cohen"

    def test_accepts_real_person_kayla_itsines(self):
        assert NameCleanerService.clean_name("Kayla Itsines") == "Kayla Itsines"

    # ── Title prefix stripping ──

    def test_accepts_title_prefix_dr_mike(self):
        assert NameCleanerService.clean_name("Dr Mike") == "Dr Mike"

    def test_accepts_title_prefix_coach_greg(self):
        assert NameCleanerService.clean_name("Coach Greg") == "Coach Greg"

    def test_accepts_title_prefix_prof_andrews(self):
        assert NameCleanerService.clean_name("Prof Andrews") == "Prof Andrews"

    def test_accepts_title_prefix_sir_chris(self):
        assert NameCleanerService.clean_name("Sir Chris") == "Sir Chris"

    def test_accepts_title_prefix_dame_jessica(self):
        assert NameCleanerService.clean_name("Dame Jessica") == "Dame Jessica"

    def test_accepts_title_prefix_rev_samuel(self):
        assert NameCleanerService.clean_name("Rev Samuel") == "Rev Samuel"

    # ── Possessive suffix stripping ──

    def test_accepts_possessive_curly_apostrophe(self):
        assert NameCleanerService.clean_name("Sophie\u2019s Kitchen") == "Sophie\u2019s Kitchen"

    def test_accepts_possessive_straight_apostrophe(self):
        assert NameCleanerService.clean_name("Sophie's Kitchen") == "Sophie's Kitchen"

    # ── Non-person first words rejected ──

    def test_rejects_non_person_first_word_dirty(self):
        assert NameCleanerService.clean_name("Dirty Harry") is None

    def test_rejects_non_person_first_word_niche(self):
        assert NameCleanerService.clean_name("Niche The") is None


class TestGameBlocklist:
    """Regression tests for _GAME_BLOCKLIST additions."""

    # ── Specific seeds.json offenders ──

    def test_rejects_the_sims(self):
        assert NameCleanerService.clean_name("The Sims") is None

    def test_rejects_far_cry(self):
        assert NameCleanerService.clean_name("Far Cry") is None

    def test_rejects_indie_game(self):
        assert NameCleanerService.clean_name("Indie Game") is None

    def test_rejects_garry_mod(self):
        assert NameCleanerService.clean_name("Garry Mod") is None

    def test_rejects_marine_electrical(self):
        # "Marine Electrical" is an occupation phrase blocked via _GENERIC_BLOCKLIST.
        assert NameCleanerService.clean_name("Marine Electrical") is None

    # ── Franchise names ──

    def test_rejects_dark_souls(self):
        assert NameCleanerService.clean_name("Dark Souls") is None

    def test_rejects_final_fantasy(self):
        assert NameCleanerService.clean_name("Final Fantasy") is None

    def test_rejects_grand_theft(self):
        assert NameCleanerService.clean_name("Grand Theft") is None

    def test_rejects_star_wars(self):
        assert NameCleanerService.clean_name("Star Wars") is None

    def test_rejects_call_duty(self):
        assert NameCleanerService.clean_name("Call Duty") is None

    # ── Real gaming creator names must still pass ──

    def test_accepts_jesse_cox(self):
        assert NameCleanerService.clean_name("Jesse Cox") == "Jesse Cox"

    def test_accepts_jim_sterling(self):
        assert NameCleanerService.clean_name("Jim Sterling") == "Jim Sterling"

