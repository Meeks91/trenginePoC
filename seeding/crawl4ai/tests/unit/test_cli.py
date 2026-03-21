"""
Unit Tests: CLI Functions
============================
Verifies parse_job_key(), build_jobs(), and CURRENT_YEAR dynamic default.
"""



from cli import parse_job_key, build_jobs
from config.seed_schema import load_categories, SeedJob, Platform, RegionCode, REGIONS, generate_seed_jobs
from config.settings import CURRENT_YEAR
from datetime import datetime


# ── parse_job_key ──

def test_parse_valid_key():
    cat, sub, plat, region = parse_job_key("FITNESS/Fitness/Instagram/US")
    assert cat == "FITNESS"
    assert sub == "Fitness"
    assert plat == "Instagram"
    assert region == "US"


def test_parse_key_with_spaces():
    cat, sub, plat, region = parse_job_key("FOOD_AND_COOKING/Quick Recipes/TikTok/UK")
    assert sub == "Quick Recipes"


def test_parse_key_too_few_parts():
    try:
        parse_job_key("FITNESS/Fitness/Instagram")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be CATEGORY/Sub/Platform/Region" in str(e)


def test_parse_key_too_many_parts():
    try:
        parse_job_key("FITNESS/Fitness/Instagram/US/extra")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "must be CATEGORY/Sub/Platform/Region" in str(e)


# ── build_jobs ──

def test_build_all_jobs():
    categories = load_categories()
    jobs = build_jobs(categories)
    # 72 subs × 3 platforms × 2 regions = 432
    total_subs = sum(len(c.all_subs) for c in categories.values())
    expected = total_subs * len(Platform) * len(RegionCode)
    assert len(jobs) == expected, f"Expected {expected} jobs, got {len(jobs)}"


def test_build_jobs_category_filter():
    categories = load_categories()
    jobs = build_jobs(categories, category_filter="FITNESS")
    # All jobs should be FITNESS
    for job in jobs:
        assert job.category_key == "FITNESS"
    assert len(jobs) > 0


def test_build_jobs_single_key():
    categories = load_categories()
    jobs = build_jobs(categories, job_key="FITNESS/Fitness/Instagram/US")
    assert len(jobs) == 1
    assert jobs[0].platform == Platform.Instagram
    assert jobs[0].region.code == RegionCode.US


def test_build_jobs_nonexistent_key():
    categories = load_categories()
    jobs = build_jobs(categories, job_key="NONEXISTENT/Fake/Instagram/US")
    assert len(jobs) == 0


# ── CURRENT_YEAR dynamic ──

def test_current_year_is_dynamic():
    """CURRENT_YEAR should match the actual current year."""
    assert CURRENT_YEAR == str(datetime.now().year), (
        f"CURRENT_YEAR is '{CURRENT_YEAR}' but actual year is {datetime.now().year}"
    )


def test_seed_job_default_year():
    """SeedJob should default to CURRENT_YEAR, not a hardcoded value."""
    categories = load_categories()
    fitness = categories["FITNESS"]
    job = SeedJob(
        platform=Platform.Instagram,
        region=REGIONS[RegionCode.US],
        category_key="FITNESS",
        sub=fitness.top_level_sub,
        # No year specified — should use CURRENT_YEAR
    )
    assert job.year == CURRENT_YEAR, (
        f"SeedJob default year is '{job.year}' but CURRENT_YEAR is '{CURRENT_YEAR}'"
    )


def test_generate_seed_jobs_default_year():
    """generate_seed_jobs should default to CURRENT_YEAR."""
    categories = load_categories()
    jobs = generate_seed_jobs(
        categories=categories,
        platforms=[Platform.Instagram],
        regions=[REGIONS[RegionCode.US]],
        # No year specified
    )
    assert len(jobs) > 0
    for job in jobs:
        assert job.year == CURRENT_YEAR


# ── SearchClientType wiring ──

def test_default_search_client_is_open(tmp_path):
    """Default search_client_type should be OPEN (DDG)."""
    from base_pipeline import SearchClientType
    from pipeline import PerJobPipelineRunner
    from services.search.OpenSearchClient import OpenSearchClient
    from services.audit.AuditService import AuditLog

    runner = PerJobPipelineRunner()
    assert runner._search_client_type == SearchClientType.OPEN

    audit = AuditLog(tmp_path, "test")
    client = runner._build_search_client(audit)
    assert isinstance(client, OpenSearchClient)


def test_strict_search_client_type_builds_strict(tmp_path, monkeypatch):
    """search_client_type=STRICT should build StrictSearchClient."""
    monkeypatch.setenv("SERPER_API_KEY", "test-key-123")
    from base_pipeline import SearchClientType
    from pipeline import PerJobPipelineRunner
    from services.search.StrictSearchClient import StrictSearchClient
    from services.audit.AuditService import AuditLog

    runner = PerJobPipelineRunner(search_client_type=SearchClientType.STRICT)
    assert runner._search_client_type == SearchClientType.STRICT

    audit = AuditLog(tmp_path, "test")
    client = runner._build_search_client(audit)
    assert isinstance(client, StrictSearchClient)


def test_open_search_client_type_builds_open(tmp_path):
    """search_client_type=OPEN should build OpenSearchClient."""
    from base_pipeline import SearchClientType
    from pipeline import PerJobPipelineRunner
    from services.search.OpenSearchClient import OpenSearchClient
    from services.audit.AuditService import AuditLog

    runner = PerJobPipelineRunner(search_client_type=SearchClientType.OPEN)
    audit = AuditLog(tmp_path, "test")
    client = runner._build_search_client(audit)
    assert isinstance(client, OpenSearchClient)


# ── Regression: Phase pipeline accumulators init in __init__ ──

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


# ── Regression: SeedJob.build_sub_to_category centralised helper ──

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

