"""
ResultAssembler — File I/O and result assembly for the pipeline.

Extracts file-writing responsibilities from PipelineRunner:
  - save_search_urls()      — search results JSON
  - save_pipeline_output()  — final output JSON
  - build_source_results()  — SourceResult list from pages
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from config import RESULTS_DIR, SEARCH_DIR, REPORTS_DIR
from config.schema import (
    Influencer, NameMentionRecord, SeedInfluencer, SourceResult,
    PageResult, SubResult, RegionResult, ErroredConfig,
)


class ResultAssembler:
    """Persists pipeline artifacts and assembles nested result structures."""

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

    def save_pipeline_output(
        self,
        output: list[RegionResult],
    ) -> Path:
        """Save final pipeline output JSON. Returns the output path."""
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_dicts = [r.to_dict() for r in output]
        output_path = RESULTS_DIR / "pipeline_output.json"
        with open(output_path, "w") as f:
            json.dump(output_dicts, f, indent=2, ensure_ascii=False)
        print(f"\n  Output saved: {output_path}")
        return output_path

    def save_global_seeds(
        self,
        seeds: list[SeedInfluencer],
    ) -> Path:
        """Save global deduped seed list as JSON. DB-ready format."""
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_path = RESULTS_DIR / "global_seeds.json"
        with open(output_path, "w") as f:
            json.dump(
                [s.to_dict() for s in seeds],
                f, indent=2, ensure_ascii=False,
            )
        print(f"  Global seeds saved: {output_path} ({len(seeds)} records)")
        return output_path

    def save_unresolved_names(
        self,
        records: list[NameMentionRecord],
    ) -> Path:
        """Save names found but not resolved to handles as JSON sidecar.

        Filters to records where DDG did not find a handle
        (``resolved_handle == ""``).  Includes mention counts, source URLs,
        and whether a search was attempted — useful for manual follow-up.

        Returns:
            Path to the saved ``unresolved_names.json`` file.
        """
        unresolved = [r for r in records if not r.resolved_handle]
        os.makedirs(RESULTS_DIR, exist_ok=True)
        output_path = RESULTS_DIR / "unresolved_names.json"
        with open(output_path, "w") as f:
            json.dump(
                [r.to_dict() for r in unresolved],
                f, indent=2, ensure_ascii=False,
            )
        print(
            f"  Unresolved names saved: {output_path} "
            f"({len(unresolved)} of {len(records)} names)"
        )
        return output_path

    def save_report_directory(
        self,
        seeds: list[SeedInfluencer],
        errored_configs: list[ErroredConfig],
        name_records: list[NameMentionRecord] | None = None,
        pipeline_output: list | None = None,
        report_path: Path | None = None,
    ) -> Path:
        """Consolidate all key outputs into a single report directory.

        Writes:
          - global_seeds.json
          - unresolved_names.json (unresolved subset of name_records)
          - errored_configs.json (only if non-empty)
          - pipeline_output.json (only if provided)
          - report_*.md (copy from reporter path, if provided)

        Returns: path to the report directory.
        """
        report_dir = REPORTS_DIR
        os.makedirs(report_dir, exist_ok=True)

        with open(report_dir / "global_seeds.json", "w") as f:
            json.dump(
                [s.to_dict() for s in seeds],
                f, indent=2, ensure_ascii=False,
            )

        unresolved = [r for r in (name_records or []) if not r.resolved_handle]
        with open(report_dir / "unresolved_names.json", "w") as f:
            json.dump(
                [r.to_dict() for r in unresolved],
                f, indent=2, ensure_ascii=False,
            )

        if errored_configs:
            with open(report_dir / "errored_configs.json", "w") as f:
                json.dump(
                    [ec.to_dict() for ec in errored_configs],
                    f, indent=2, ensure_ascii=False,
                )

        if pipeline_output is not None:
            with open(report_dir / "pipeline_output.json", "w") as f:
                json.dump(pipeline_output, f, indent=2, ensure_ascii=False)

        if report_path and report_path.exists():
            dest = report_dir / report_path.name
            if not dest.exists() or not report_path.samefile(dest):
                import shutil
                shutil.copy2(report_path, dest)

        print(f"  Report directory saved: {report_dir}")
        return report_dir
