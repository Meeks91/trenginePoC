"""
Unit Tests: AuditService
Verifies JSONL append-only audit logging for all pipeline phases.
"""

import json
import tempfile
from pathlib import Path


from services.audit.AuditService import AuditLog, AuditEntry


def test_creates_file_on_first_log():
    """AuditLog should create a JSONL file on first log call."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test_job")
        audit.log("search", "query", query="test query", results=5)

        assert audit.path.exists()
        parsed = json.loads(audit.path.read_text().strip())
        assert parsed["phase"] == "search"
        assert parsed["action"] == "query"
        assert parsed["results"] == 5


def test_appends_multiple_entries():
    """Multiple log calls append to the same JSONL file."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test_job")
        audit.log_url_accepted("https://example.com")
        audit.log_url_rejected("https://bing.com/ad", reason="ad_domain")
        audit.log_page_success("https://example.com", raw_tokens=1000, fit_tokens=600)

        lines = audit.path.read_text().strip().split("\n")
        assert len(lines) == 3
        assert len(audit.entries) == 3


def test_entry_omits_none_fields():
    """AuditEntry.to_json() should not include None-valued fields."""
    entry = AuditEntry(phase="search", action="query", query="test", results=3)
    d = json.loads(entry.to_json())
    assert "url" not in d
    assert "error" not in d
    assert d["query"] == "test"


def test_llm_call_captures_tokens():
    """LLM call audit should record token counts and influencer count."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test_job")
        audit.log_llm_call(
            url="https://example.com/page",
            input_tokens=5000,
            output_tokens=200,
            influencers_found=12,
        )

        parsed = json.loads(audit.path.read_text().strip())
        assert parsed["phase"] == "extract"
        assert parsed["input_tokens"] == 5000
        assert parsed["influencers_found"] == 12


def test_dedup_logging():
    """Dedup events should be logged with reason."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test_job")
        audit.log_dedup("Joe Wicks", reason="duplicate_handle")

        parsed = json.loads(audit.path.read_text().strip())
        assert parsed["phase"] == "enrich"
        assert parsed["action"] == "dedup"
        assert parsed["reason"] == "duplicate_handle"
