"""
Unit Tests: Report Presentation Layer
========================================
Verifies PipelineReporter output format:
  - Seed table shows handles + categories, NOT name
  - Name mentions section shows NameMentionRecord with frequency
"""

from pathlib import Path
from unittest.mock import patch
from config.schema import PipelineStats, SeedInfluencer, NameMentionRecord


def _empty_stats() -> PipelineStats:
    return PipelineStats()


def _generate_report(**kwargs) -> str:
    """Generate report to temp dir and return content."""
    from services.reporting.PipelineReporter import PipelineReporter
    reporter = PipelineReporter()
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        path = reporter.generate(
            run_dir=Path(tmpdir),
            stats=kwargs.get("stats", _empty_stats()),
            validation_results=kwargs.get("validation_results", {}),
            model="test",
            mode="test",
            **{k: v for k, v in kwargs.items()
               if k not in ("stats", "validation_results")},
        )
        return path.read_text()


# ── Seed Table ──────────────────────────────────────────────────────────────

def test_report_seed_table_excludes_name():
    """Seed table header should NOT contain Name column."""
    seeds = [SeedInfluencer(name="Andrew Ng", ig_handle="andrewyng", categories=["AI"])]
    report = _generate_report(global_seeds=seeds)
    assert "| Name |" not in report


def test_report_seed_table_has_handle_columns():
    """Seed table must have IG/TK/YT handle columns."""
    seeds = [SeedInfluencer(name="Test", ig_handle="test_ig", categories=["AI"])]
    report = _generate_report(global_seeds=seeds)
    assert "| IG Handle |" in report
    assert "| TK Handle |" in report
    assert "| YT Handle |" in report


def test_report_seed_table_shows_handle_values():
    """Handle values appear in the seed table rows."""
    seeds = [SeedInfluencer(name="X", ig_handle="creator1", yt_handle="creator1yt", categories=["AI"])]
    report = _generate_report(global_seeds=seeds)
    assert "creator1" in report
    assert "creator1yt" in report


# ── Name Mentions ───────────────────────────────────────────────────────────

def test_report_includes_name_mentions_section():
    """Name mentions section with frequency from NameMentionRecord."""
    mentions = [
        NameMentionRecord(canonical="Andrew Ng", mention_count=4, source_types=["LLM"]),
    ]
    report = _generate_report(name_mentions=mentions)
    assert "Andrew Ng" in report
    assert "4" in report
    assert "Name Mentions" in report


def test_report_no_name_mentions_when_empty():
    """Empty name mentions → section omitted."""
    report = _generate_report(name_mentions=[])
    assert "Name Mentions" not in report
