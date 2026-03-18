"""
PipelineReporter — Generates human-readable pipeline report as markdown.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from config import INPUT_COST_PER_1M, OUTPUT_COST_PER_1M
from config.schema import (
    PipelineStats, JobBreakdown, Influencer,
    NameMentionRecord, Platform, ErroredConfig,
)
from services.enrichment.InfluencerMerger import InfluencerMerger
from services.validation.IngestionValidator import ValidationResult


class PipelineReporter:
    """Generates pipeline_report.md after a run."""

    def __init__(self) -> None:
        self.last_report_path: Path | None = None

    def generate(
        self,
        run_dir: Path,
        stats: PipelineStats,
        validation_results: dict[str, ValidationResult | None],
        model: str,
        mode: str,
        target_platform: str = "Instagram",
        job_results: list[JobBreakdown] | None = None,
        influencers: list[Influencer] | None = None,
        global_seeds: list[Influencer] | None = None,
        name_mentions: list[NameMentionRecord] | None = None,
        warnings: list[str] | None = None,
        errored_configs: list[ErroredConfig] | None = None,
        total_configs: int = 0,
    ) -> Path:
        """Generate a human-readable report. Returns path to the report file."""
        os.makedirs(run_dir, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        report_path = run_dir / "report.md"

        handle_fill_rate = (
            f"{stats.handles_filled}/{stats.influencers_deduped}"
            if stats.influencers_deduped > 0 else "N/A"
        )

        input_cost = stats.total_input_tokens * INPUT_COST_PER_1M / 1_000_000
        output_cost = stats.total_output_tokens * OUTPUT_COST_PER_1M / 1_000_000
        total_cost = input_cost + output_cost

        lines = [
            f"# Pipeline Report — {ts}",
            "",
            "## Summary",
            "| Metric | Value |",
            "|--------|-------|",
            f"| URLs discovered | {stats.urls_discovered} |",
            f"| Pages crawled | {stats.pages_crawled} ({stats.pages_failed} failed, {stats.pages_dropped} dropped) |",
            f"| Pages extracted (LLM) | {stats.pages_extracted} |",
            f"| Influencers found (raw) | {stats.influencers_raw} |",
            f"| Unique (after dedup) | {stats.influencers_deduped} |",
            f"| Handle fill rate | {handle_fill_rate} |",
            f"| **Handle retrieval** | **{stats.handles_retrieved}/{stats.handles_in_source}** |",
            f"| Estimated LLM cost | ${total_cost:.4f} |",
        ]

        # Yield metric in summary (always shown, informational)
        if stats.pages_crawled > 0:
            yield_ratio = stats.regex_handles_total / stats.pages_crawled
            lines.append(f"| Regex yield | {yield_ratio:.1f} handles/page |")
        if stats.configs_aborted > 0:
            lines.append(f"| **Configs aborted** | **{stats.configs_aborted}** |")
        if total_configs > 0:
            failed = len(errored_configs) if errored_configs else 0
            succeeded = total_configs - failed
            lines.append(f"| **Configs** | **{succeeded} succeeded, {failed} failed ({total_configs} total)** |")
        lines.append("")

        # ── Warnings ──
        if warnings:
            lines.extend([
                "## ⚠️ Warnings",
                "",
            ])
            for w in warnings:
                lines.append(f"- {w}")
            lines.append("")

        # ── Per-Job Breakdown ──
        if job_results:
            lines.extend([
                "## Breakdown by Job",
                "| Region | Platform | Category | Sub | Influencers | Handles | Pages |",
                "|--------|----------|----------|-----|-------------|---------|-------|",
            ])
            for job in sorted(job_results, key=lambda j: (j.region, j.platform, j.category, j.sub)):
                lines.append(
                    f"| {job.region} | {job.platform} | {job.category} | {job.sub} "
                    f"| {job.influencers_found} | {job.handles_filled} | {job.pages_crawled} |"
                )
            lines.append("")

        # ── Full Influencer Roster (grouped by identity) ──
        if influencers:
            grouped = InfluencerMerger.merge(influencers)
            grouped.sort(key=lambda inf: len(inf.source_urls), reverse=True)
            lines.extend([
                "## Influencers Found",
                f"**{len(grouped)} unique people** (grouped from {len(influencers)} raw entries)",
                "",
                "| # | Name | IG Handle | TK Handle | YT Handle | Cites |",
                "|---|------|-----------|-----------|-----------|-------|",
            ])
            for i, inf in enumerate(grouped, 1):
                ig = inf.handles.get(Platform.Instagram, "—")
                tk = inf.handles.get(Platform.TikTok, "—")
                yt = inf.handles.get(Platform.YouTube, "—")
                cites = len(inf.source_urls)
                lines.append(f"| {i} | {inf.name} | {ig} | {tk} | {yt} | {cites} |")
            lines.append("")

        # ── Global Seed DB (Deduped across configs) ──
        if global_seeds:
            lines.extend([
                "## Global Seed DB (Deduped)",
                f"**{len(global_seeds)} unique seeds** across all configs",
                "",
                "| # | IG Handle | TK Handle | YT Handle | Categories |",
                "|---|-----------|-----------|-----------|------------|",
            ])
            for i, seed in enumerate(sorted(global_seeds, key=lambda s: s.name.lower()), 1):
                ig = seed.ig_handle or "—"
                tk = seed.tk_handle or "—"
                yt = seed.yt_handle or "—"
                cats = ", ".join(sorted(seed.categories_found_in)) if seed.categories_found_in else "—"
                lines.append(f"| {i} | {ig} | {tk} | {yt} | {cats} |")
            lines.append("")

        # ── Canary Validation ──
        valid_results = {k: v for k, v in validation_results.items() if v is not None}
        if valid_results:
            lines.extend([
                "## Canary Validation",
                "| Sub | Canary | Found? |",
                "|-----|--------|--------|",
            ])
            total_expected = 0
            total_found = 0
            for sub_key, vr in valid_results.items():
                total_expected += len(vr.expected)
                total_found += len(vr.found)
                for name in vr.found:
                    lines.append(f"| {sub_key} | {name} | YES |")
                for name in vr.missing:
                    lines.append(f"| {sub_key} | {name} | MISSING |")

            overall_rate = total_found / total_expected if total_expected else 0
            lines.extend([
                f"| **Overall** | **{total_found}/{total_expected}** | **{overall_rate:.0%}** |",
                "",
            ])

        # ── Name Mentions ──
        if name_mentions:
            lines.extend([
                "## Name Mentions",
                f"**{len(name_mentions)} names** tracked across all pages",
                "",
                "| # | Name | Mentions | Source | URLs | Resolved? | Handle |",
                "|---|------|----------|--------|------|-----------|--------|",
            ])
            for i, nm in enumerate(sorted(name_mentions, key=lambda x: x.mention_count, reverse=True), 1):
                source = ", ".join(nm.source_types) if nm.source_types else "—"
                url_count = len(nm.source_urls) if nm.source_urls else 0
                if nm.was_searched and nm.resolved_handle:
                    resolved = f"✅ @{nm.resolved_handle} ({nm.resolved_platform})"
                elif nm.was_searched:
                    resolved = "✅ (no match)"
                else:
                    resolved = "❌"
                lines.append(f"| {i} | {nm.canonical} | {nm.mention_count} | {source} | {url_count} | {resolved} |")
            lines.append("")

        # ── Token Usage ──
        lines.extend([
            "## Token Usage",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total input tokens | ~{stats.total_input_tokens:,} |",
            f"| Total output tokens | ~{stats.total_output_tokens:,} |",
            f"| Model | {model} |",
            f"| Mode | {mode} |",
            "",
        ])

        # ── Reliability (only shown if there were issues) ──
        total_retries = stats.search_retries + stats.enrich_retries + stats.llm_retries + stats.crawl_retries
        total_failures = stats.search_failures + stats.enrich_failures + stats.llm_failures + stats.pages_failed + stats.pages_dropped
        if total_retries > 0 or total_failures > 0:
            lines.extend([
                "## Reliability",
                "| Metric | Value |",
                "|--------|-------|",
            ])
            if stats.search_retries or stats.search_failures:
                lines.append(f"| DDG search retries | {stats.search_retries} |")
                lines.append(f"| DDG search failures | {stats.search_failures} |")
            if stats.enrich_retries or stats.enrich_failures:
                lines.append(f"| DDG enrich retries | {stats.enrich_retries} |")
                lines.append(f"| DDG enrich failures | {stats.enrich_failures} |")
            if stats.llm_retries or stats.llm_failures:
                lines.append(f"| LLM retries | {stats.llm_retries} |")
                lines.append(f"| LLM failures | {stats.llm_failures} |")
            if stats.pages_failed or stats.pages_dropped or stats.crawl_retries:
                lines.append(f"| Crawl failures | {stats.pages_failed} |")
                lines.append(f"| Crawl dropped | {stats.pages_dropped} |")
                lines.append(f"| Crawl retries | {stats.crawl_retries} |")
            lines.append("")

        # ── Errored Configs ──
        if errored_configs:
            lines.extend([
                "## ❌ Errored Configs",
                f"**{len(errored_configs)} config(s)** failed due to DDG search errors",
                "",
                "| # | Config | Failures | Attempted | Rate | Reason |",
                "|---|--------|----------|-----------|------|--------|",
            ])
            for i, ec in enumerate(errored_configs, 1):
                lines.append(
                    f"| {i} | {ec.config_key} | {ec.failure_count} "
                    f"| {ec.queries_attempted} "
                    f"| {ec.failure_threshold_percentage:.0%} | {ec.reason} |"
                )
            lines.append("")

        report_content = "\n".join(lines)

        with open(report_path, "w") as f:
            f.write(report_content)

        self.last_report_path = report_path
        print(f"\n  Report saved: {report_path}")
        return report_path
