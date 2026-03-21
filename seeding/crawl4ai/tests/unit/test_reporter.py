"""
Unit Tests: PipelineReporter
Verifies markdown report generation with stats and canary results.
"""

import tempfile
from pathlib import Path

from config.schema import PipelineStats, Influencer, Platform
from services.validation.IngestionValidator import ValidationResult


def test_generates_report_file():
    """Reporter should create a markdown file with correct metrics."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    stats = PipelineStats(
        urls_discovered=20,
        pages_crawled=18,
        pages_failed=2,
        pages_extracted=15,
        influencers_raw=45,
        influencers_deduped=30,
        handles_filled=25,
        total_input_tokens=50000,
        total_output_tokens=3000,
    )

    from config import LLM_PROVIDER
    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model=LLM_PROVIDER,
            mode="sampled",
        )

        assert path.exists()
        content = path.read_text()
        assert "20" in content
        assert "30" in content
        assert "25/30" in content
        assert "sampled" in content


def test_includes_canary_results():
    """Report should include canary validation table when results present."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    stats = PipelineStats(influencers_deduped=10, handles_filled=8)
    vr = ValidationResult(
        expected=["Kayla Itsines", "Joe Wicks"],
        found=["Kayla Itsines"],
        missing=["Joe Wicks"],
        pass_rate=0.5,
    )

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={"FITNESS_Fitness_IG_US": vr},
            model="test",
            mode="test",
        )

        content = path.read_text()
        assert "Canary Validation" in content
        assert "Kayla Itsines" in content
        assert "MISSING" in content


def test_reliability_section_shows_failures():
    """Report should include Reliability section when there are retries or failures."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    stats = PipelineStats(
        urls_discovered=20,
        pages_crawled=18,
        pages_failed=3,
        influencers_deduped=10,
        search_retries=5,
        search_failures=2,
        enrich_retries=3,
        enrich_failures=1,
    )

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
        )

        content = path.read_text()
        assert "Reliability" in content, "Reliability section missing from report"
        assert "DDG search retries | 5" in content
        assert "DDG search failures | 2" in content
        assert "DDG enrich retries | 3" in content
        assert "DDG enrich failures | 1" in content
        assert "Crawl failures | 3" in content


def test_reliability_hidden_when_clean():
    """Report should NOT include Reliability section when no failures occurred."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    stats = PipelineStats(
        urls_discovered=20,
        pages_crawled=20,
        pages_failed=0,
        influencers_deduped=10,
    )

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
        )

        content = path.read_text()
        assert "Reliability" not in content, (
            "Reliability section should be hidden when no failures occurred"
        )


def test_influencer_roster_renders():
    """Report should include a grouped influencer roster with handles, platforms, and alt_handles."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    influencers = [
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "@thebodycoach"}),
        Influencer(name="Adam Maxted", handles={Platform.Instagram: "@adammaxted"}),
        Influencer(name="Adam Maxted", handles={Platform.YouTube: "@adammaxted2262"}),
        Influencer(name="Victoria Niamh", handles={Platform.TikTok: "@victorianiamh"}),
        Influencer(name="Lucy Davis", handles={Platform.YouTube: "@lucydavis"}),
    ]

    stats = PipelineStats(influencers_deduped=5, handles_filled=5)
    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
            influencers=influencers,
        )

        content = path.read_text()
        assert "Influencers Found" in content, "Roster section missing"
        assert "unique people" in content, "Grouped count line missing"
        assert "IG Handle" in content, "IG column header missing"
        assert "TK Handle" in content, "TK column header missing"
        assert "YT Handle" in content, "YT column header missing"
        assert "Joe Wicks" in content
        assert "Adam Maxted" in content
        assert "Victoria Niamh" in content
        assert "Lucy Davis" in content
        assert "thebodycoach" in content
        assert "adammaxted" in content
        assert "adammaxted2262" in content
        assert "victorianiamh" in content
        assert "lucydavis" in content
        adam_line = [line for line in content.split("\n") if "Adam Maxted" in line][0]
        assert "adammaxted" in adam_line
        assert "adammaxted2262" in adam_line


def test_single_url_mode_report():
    """Single-URL mode should produce a grouped report with influencer roster, no job breakdown."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    influencers = [
        Influencer(name="Maria Garcia", handles={Platform.Instagram: "@creator_a"}),
        Influencer(name="John Rivera", handles={Platform.TikTok: "@creator_b"}),
    ]

    stats = PipelineStats(
        pages_crawled=1,
        influencers_raw=2,
        influencers_deduped=2,
        handles_filled=2,
    )

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="single-url",
            influencers=influencers,
        )

        assert path.exists(), "Report file not created"
        content = path.read_text()
        assert "Pipeline Report" in content
        assert "single-url" in content
        assert "Influencers Found" in content
        assert "unique people" in content
        assert "IG Handle" in content
        assert "TK Handle" in content
        assert "Maria Garcia" in content
        assert "creator_a" in content
        assert "John Rivera" in content
        assert "creator_b" in content
        assert "Breakdown by Job" not in content


def test_errored_configs_section_renders():
    """Report should include Errored Configs table when errored configs present."""
    from services.reporting.PipelineReporter import PipelineReporter
    from config.schema import ErroredConfig
    reporter = PipelineReporter()

    stats = PipelineStats(influencers_deduped=5, configs_aborted=2)
    errored = [
        ErroredConfig(
            config_key="FITNESS/HIIT/Instagram/US",
            category="FITNESS", sub_name="HIIT",
            platform="Instagram", region="US",
            failure_count=4, queries_attempted=5,
            failure_threshold_percentage=0.8,
            reason="DDG failure rate 80% >= threshold 50%",
        ),
        ErroredConfig(
            config_key="AI/AI/TikTok/US",
            category="AI", sub_name="AI",
            platform="TikTok", region="US",
            failure_count=3, queries_attempted=3,
            failure_threshold_percentage=1.0,
            reason="DDG killed after 3 consecutive config failures",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
            errored_configs=errored,
            total_configs=10,
        )

        content = path.read_text()
        assert "Errored Configs" in content
        assert "FITNESS/HIIT/Instagram/US" in content
        assert "AI/AI/TikTok/US" in content
        assert "80%" in content
        assert "2 config(s)" in content


def test_config_summary_line_renders():
    """Report should show 'X succeeded, Y failed (Z total)' summary line."""
    from services.reporting.PipelineReporter import PipelineReporter
    from config.schema import ErroredConfig
    reporter = PipelineReporter()

    stats = PipelineStats(influencers_deduped=5)
    errored = [
        ErroredConfig(
            config_key="TEST/Sub/IG/US",
            category="TEST", sub_name="Sub",
            platform="Instagram", region="US",
            failure_count=3, queries_attempted=5,
            failure_threshold_percentage=0.6,
            reason="test",
        ),
    ]

    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
            errored_configs=errored,
            total_configs=5,
        )

        content = path.read_text()
        assert "4 succeeded, 1 failed (5 total)" in content


def test_config_summary_hidden_without_total():
    """Config summary not shown when total_configs is 0."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()

    stats = PipelineStats(influencers_deduped=5)
    with tempfile.TemporaryDirectory() as tmp:
        path = reporter.generate(
            run_dir=Path(tmp),
            stats=stats,
            validation_results={},
            model="test",
            mode="test",
        )

        content = path.read_text()
        assert "succeeded" not in content
        assert "total)" not in content
