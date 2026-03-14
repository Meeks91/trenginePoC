"""
Audit Trail
============
JSONL-based audit logger — records every decision in the pipeline.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


@dataclass
class AuditEntry:
    """A single auditable event."""
    phase: str             # "search", "crawl", "extract", "enrich"
    action: str            # "query", "url_accepted", "page_success", etc.
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    url: Optional[str] = None
    query: Optional[str] = None
    name: Optional[str] = None
    handle: Optional[str] = None
    reason: Optional[str] = None
    error: Optional[str] = None
    results: Optional[int] = None
    raw_tokens: Optional[int] = None
    fit_tokens: Optional[int] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    influencers_found: Optional[int] = None
    platform: Optional[str] = None
    attempt: Optional[int] = None

    def to_json(self) -> str:
        """Serialise to compact JSON, omitting None fields."""
        d = {k: v for k, v in asdict(self).items() if v is not None}
        return json.dumps(d, ensure_ascii=False)


class AuditLog:
    """Append-only JSONL audit log for a pipeline run."""

    def __init__(self, audit_dir: Path, job_key: str):
        os.makedirs(audit_dir, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        safe_key = job_key.replace("/", "-").replace(" ", "_")
        self._path = audit_dir / f"{ts}_{safe_key}.jsonl"
        self._entries: list[AuditEntry] = []

    @property
    def path(self) -> Path:
        return self._path

    @property
    def entries(self) -> list[AuditEntry]:
        return self._entries

    def log(self, phase: str, action: str, **kwargs: Any) -> None:
        """Record an audit event and append to JSONL file."""
        entry = AuditEntry(phase=phase, action=action, **kwargs)
        self._entries.append(entry)
        with open(self._path, "a") as f:
            f.write(entry.to_json() + "\n")

    def log_search_query(self, query: str, results: int) -> None:
        self.log("search", "query", query=query, results=results)

    def log_url_accepted(self, url: str) -> None:
        self.log("search", "url_accepted", url=url, reason="new")

    def log_url_rejected(self, url: str, reason: str) -> None:
        self.log("search", "url_rejected", url=url, reason=reason)

    def log_page_success(self, url: str, raw_tokens: int, fit_tokens: int) -> None:
        self.log("crawl", "page_success", url=url, raw_tokens=raw_tokens, fit_tokens=fit_tokens)

    def log_page_failed(self, url: str, error: str) -> None:
        self.log("crawl", "page_failed", url=url, error=error)

    def log_llm_call(self, url: str, input_tokens: int, output_tokens: int, influencers_found: int) -> None:
        self.log("extract", "llm_call", url=url, input_tokens=input_tokens,
                 output_tokens=output_tokens, influencers_found=influencers_found)

    def log_handle_found(self, name: str, handle: str) -> None:
        self.log("enrich", "handle_found", name=name, handle=handle)

    def log_dedup(self, name: str, reason: str) -> None:
        self.log("enrich", "dedup", name=name, reason=reason)
