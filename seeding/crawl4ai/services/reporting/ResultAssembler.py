"""
ResultAssembler — File I/O for pipeline run output.

All output from a single run is consolidated into a single directory:
  reports/<run_id>/
    report.md
    seeds.json
    errors.json          (only if non-empty)
    unresolved_names.json
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from config import RESULTS_DIR, SEARCH_DIR, REPORTS_DIR
from config.schema import (
    Influencer, NameMentionRecord, SourceResult,
    PageResult, SubResult, RegionResult, ErroredConfig,
)


class ResultAssembler:
    """Persists pipeline artifacts and assembles nested result structures."""

    # ── API ──

    def save_search_urls(
        self,
        job_key: str,
        url_query_pairs: list[tuple[str, str]],
    ) -> None:
        """Save discovered URLs for a job to JSON."""
        os.makedirs(SEARCH_DIR, exist_ok=True)
        safe_key = job_key.replace("/", "-").replace(" ", "_")
        with open(SEARCH_DIR / f"{safe_key}_urls.json", "w") as f:
            json.dump(
                [{"url": u, "query": q} for u, q in url_query_pairs],
                f, indent=2,
            )

    def build_source_results(
        self,
        pages: list[PageResult],
        url_to_influencers: dict[str, list[Influencer]],
    ) -> list[SourceResult]:
        """Build SourceResult list from pages + extraction map."""
        sources = []
        for page in pages:
            if not page.success:
                continue
            page_influencers = url_to_influencers.get(page.url, [])
            sources.append(SourceResult(
                url=page.url,
                query=page.query,
                md=page.md_path or "",
                influencers=page_influencers,
            ))
        return sources

    def save_run_report(
        self,
        run_dir: Path,
        seeds: list[Influencer],
        errored_configs: list[ErroredConfig],
        name_records: list[NameMentionRecord] | None = None,
        report_path: Path | None = None,
    ) -> Path:
        """Consolidate all outputs into a single run directory.

        Writes:
          - seeds.json
          - unresolved_names.json
          - errors.json (only if errored_configs is non-empty)
          - report.md (copied from reporter output, if provided)

        Returns: path to the run directory.
        """
        os.makedirs(run_dir, exist_ok=True)

        self._write_seeds(run_dir, seeds)
        self._write_unresolved_names(run_dir, name_records or [])
        self._write_errors(run_dir, errored_configs)
        self._copy_report(run_dir, report_path)

        print(f"  Run output saved: {run_dir}")
        return run_dir

    # ── Internal ──

    @staticmethod
    def generate_run_id(region_label: str) -> str:
        """Produce a human-readable run directory name.

        Format: YYYY-MM-DD_H.MMam/pm_{region}
        Example: 2026-03-15_1.48pm_US
        """
        now = datetime.now(ZoneInfo("Europe/London"))
        hour_12 = now.strftime("%-I")
        minute = now.strftime("%M")
        am_pm = now.strftime("%p").lower()
        return f"{now.strftime('%Y-%m-%d')}_{hour_12}.{minute}{am_pm}_{region_label}"

    @staticmethod
    def _write_seeds(run_dir: Path, seeds: list[Influencer]) -> None:
        with open(run_dir / "seeds.json", "w") as f:
            json.dump(
                [s.to_dict() for s in seeds],
                f, indent=2, ensure_ascii=False,
            )
        print(f"  Seeds saved: {run_dir / 'seeds.json'} ({len(seeds)} records)")

    @staticmethod
    def _write_unresolved_names(
        run_dir: Path,
        records: list[NameMentionRecord],
    ) -> None:
        unresolved = [r for r in records if not r.resolved_handle]
        with open(run_dir / "unresolved_names.json", "w") as f:
            json.dump(
                [r.to_dict() for r in unresolved],
                f, indent=2, ensure_ascii=False,
            )
        print(
            f"  Unresolved names saved: {run_dir / 'unresolved_names.json'} "
            f"({len(unresolved)} of {len(records)} names)"
        )

    @staticmethod
    def _write_errors(
        run_dir: Path,
        errored_configs: list[ErroredConfig],
    ) -> None:
        if not errored_configs:
            return
        with open(run_dir / "errors.json", "w") as f:
            json.dump(
                [ec.to_dict() for ec in errored_configs],
                f, indent=2, ensure_ascii=False,
            )

    @staticmethod
    def _copy_report(run_dir: Path, report_path: Path | None) -> None:
        if report_path is None or not report_path.exists():
            return
        dest = run_dir / "report.md"
        if not dest.exists() or not report_path.samefile(dest):
            import shutil
            shutil.copy2(report_path, dest)
