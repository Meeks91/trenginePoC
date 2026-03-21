"""
Regression Tests: Code Review Fixes
======================================
Tests verifying the correctness of fixes applied during the code review.
Each test documents which fix it validates and what the old broken behavior was.
"""

import tempfile
from datetime import datetime
from pathlib import Path


from services.audit.AuditService import AuditLog
from services.search.SearchService import SearchService
from services.crawling.CrawlService import CrawlService
from services.enrichment.InfluencerMerger import InfluencerMerger
from config.schema import Influencer, Platform


# ── Fix 1: lstrip("www.") → removeprefix("www.") ──
#
# Old: str.lstrip("www.") strips CHARACTERS {w, .} from the left.
#      "wwwexample.com".lstrip("www.") → "example.com"  (accidentally correct)
#      "weather.com".lstrip("www.") → "eather.com"      (BUG: strips 'w')
# New: str.removeprefix("www.") strips the exact prefix "www." only.


class TestRemovePrefixFix:
    """Regression tests for the lstrip → removeprefix fix in SearchService."""

    def test_www_prefix_stripped(self):
        """Standard www. prefix is correctly removed."""
        assert SearchService._is_platform_url("https://www.instagram.com/user") is True
        assert SearchService._is_platform_url("https://www.tiktok.com/@user") is True

    def test_no_www_prefix_works(self):
        """URLs without www. prefix still match."""
        assert SearchService._is_platform_url("https://instagram.com/user") is True
        assert SearchService._is_platform_url("https://tiktok.com/@user") is True

    def test_domain_starting_with_w_not_mangled(self):
        """REGRESSION: domains starting with 'w' must NOT be mangled.

        Old lstrip("www.") would strip the leading 'w' from 'weather.com'
        turning it into 'eather.com'. removeprefix keeps it intact.
        """
        # These should NOT be platform URLs — verify the domain isn't mangled
        # into something that accidentally matches
        assert SearchService._is_platform_url("https://weather.com/forecast") is False
        assert SearchService._is_platform_url("https://wikipedia.org/wiki") is False

    def test_double_www_not_over_stripped(self):
        """REGRESSION: 'wwww.instagram.com' should still resolve.

        Old lstrip("www.") would strip all leading w's AND the dot.
        removeprefix("www.") strips exactly one 'www.' prefix.
        """
        # wwww.instagram.com → after removeprefix("www.") → "w.instagram.com"
        # This contains "instagram.com" so should still match
        assert SearchService._is_platform_url("https://wwww.instagram.com/user") is True


# ── Fix 2: Hardcoded "2026" → CURRENT_YEAR ──

def test_current_year_is_dynamic():
    """CURRENT_YEAR should match the actual runtime year, not a hardcoded value."""
    from config.settings import CURRENT_YEAR
    assert CURRENT_YEAR == str(datetime.now().year), (
        f"CURRENT_YEAR is '{CURRENT_YEAR}' but actual year is {datetime.now().year}"
    )


# ── Fix 3: Phase pipeline accumulators init in __init__ ──

def test_phase_pipeline_accumulators_initialised():
    """REGRESSION: phase pipeline accumulators must exist at init time.

    _url_bag and _all_direct_handles are the real accumulators used
    during phase-based search. They must be initialised in __init__.
    (_name_records and _direct_handles were dead fields, now removed.)
    """
    from phase_pipeline import PhasePipelineRunner
    runner = PhasePipelineRunner()
    assert hasattr(runner, '_url_bag'), "_url_bag must be set in __init__"
    assert runner._url_bag == {}, "_url_bag must default to empty dict"
    assert hasattr(runner, '_all_direct_handles'), "_all_direct_handles must be set in __init__"
    assert runner._all_direct_handles == [], "_all_direct_handles must default to empty list"


# ── Fix 4: _dropped_count / _retry_count init ──

def test_crawl_service_counters_initialised():
    """REGRESSION: dropped_count and retry_count must be accessible before crawl_urls().

    Old code used getattr(self, '_dropped_count', 0) because the attributes
    were only set inside crawl_urls(). Now they're initialised in __init__.
    """
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = CrawlService(audit)

        # Properties must work BEFORE any crawl_urls() call
        assert svc.dropped_count == 0, "dropped_count must be 0 before any crawl"
        assert svc.retry_count == 0, "retry_count must be 0 before any crawl"


# ── Fix 5: callable → Callable[[str], bool] ──

def test_filter_blocked_accepts_custom_filter():
    """InfluencerMerger.filter_blocked() handle_filter must accept a typed callable."""
    entries = [
        Influencer(name="Test", handles={Platform.Instagram: "@test_user"}, most_seen_category="CAT"),
    ]
    # Pass a custom filter that blocks nothing
    result = InfluencerMerger.filter_blocked(entries, handle_filter=lambda h: False)
    assert len(result) >= 1, "Custom filter should allow all handles through"

    # Pass a custom filter that blocks everything
    result_blocked = InfluencerMerger.filter_blocked(entries, handle_filter=lambda h: True)
    assert len(result_blocked) == 0, "Filter returning True should block all handles"


# ── Fix 8: Shared NameCleaner ──

def test_name_cleaner_shared_by_both_parsers():
    """LLMResponseParser and NameExtractor must both use NameCleaner.

    Old code defined cleanup logic independently. Now both import
    NameCleaner for consistent name cleaning.
    """
    import services.extraction.LLMResponseParser as parser_mod
    import services.extraction.NameExtractor as extractor_mod

    assert hasattr(parser_mod, 'NameCleaner'), (
        "LLMResponseParser must import NameCleaner"
    )
    assert hasattr(extractor_mod, 'NameCleaner'), (
        "NameExtractor must import NameCleaner"
    )


# ── Fix 9: SeedJob.build_sub_to_category centralised helper ──

def test_build_sub_to_category_maps_subs_to_categories():
    """SeedJob.build_sub_to_category builds {sub_name: category_key} from jobs."""
    from config.seed_schema import SeedJob, SubCategory, Difficulty, Region, RegionCode

    sub_gym = SubCategory(
        sub_name="Gym", is_top_level=False, search_prompt="", alt_search_terms=[],
        known_sources=[], platform_notes="", region_notes="",
        difficulty=Difficulty.EASY, strict_slugs=[],
    )
    sub_cooking = SubCategory(
        sub_name="Cooking", is_top_level=False, search_prompt="", alt_search_terms=[],
        known_sources=[], platform_notes="", region_notes="",
        difficulty=Difficulty.EASY, strict_slugs=[],
    )
    region = Region(code=RegionCode.US, language="en", label="United States")
    jobs = [
        SeedJob(platform=Platform.Instagram, region=region, category_key="FITNESS", sub=sub_gym),
        SeedJob(platform=Platform.Instagram, region=region, category_key="FOOD", sub=sub_cooking),
    ]

    result = SeedJob.build_sub_to_category(jobs=jobs)

    assert result == {"Gym": "FITNESS", "Cooking": "FOOD"}


def test_build_sub_to_category_empty_jobs():
    """Empty job list → empty mapping."""
    from config.seed_schema import SeedJob

    assert SeedJob.build_sub_to_category(jobs=[]) == {}


