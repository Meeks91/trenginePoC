"""Bootstrap script: run E2E pipeline once, dump golden fixtures.

Usage:
    cd seeding/crawl4ai
    PYTHONPATH="." python tests/integration/_bootstrap_e2e_golden.py

Outputs golden files to tests/fixtures/e2e_golden/
"""
import asyncio
import http.server
import json
import re
import tempfile
import threading
from pathlib import Path
from unittest.mock import patch, MagicMock

from config.schema import Influencer, Platform
from services.enrichment.CategoryProvenanceTagger import CategoryProvenanceTagger
from config.seed_schema import (
    SeedJob, SubCategory, Region, RegionCode, Difficulty,
)
from base_pipeline import BasePipelineRunner, GatherResult, JobOutcome
from services.audit.AuditService import AuditLog
from services.crawling.CrawlService import CrawlService
from services.extraction.HandleExtractionService import HandleExtractionService


FIXTURE_HTML = Path(__file__).resolve().parent.parent / "fixtures" / "gymfluencers_uk_fitness.html"
GOLDEN_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "e2e_golden"


def _normalize_ports(records: list[dict]) -> list[dict]:
    """Replace localhost:PORT with localhost:0 so random ports don't break diffs."""
    out = []
    for r in records:
        r2 = dict(r)
        if "source_urls" in r2:
            r2["source_urls"] = [
                re.sub(r"127\.0\.0\.1:\d+", "127.0.0.1:0", u)
                for u in r2["source_urls"]
            ]
        out.append(r2)
    return out


def _build_mock_influencers() -> list[Influencer]:
    return [
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "thebodycoach"}),
        Influencer(name="Alex Beattie", handles={
            Platform.Instagram: "alex.beattie",
            Platform.TikTok: "alex.beattie",
        }),
        Influencer(name="Lucy Davis", handles={}),
        Influencer(name="Courtney Black", handles={
            Platform.Instagram: "courtneyblackfitness",
            Platform.TikTok: "courtneyblackfitness",
        }),
        Influencer(name="Michael Griffiths", handles={
            Platform.YouTube: "mac_griffiths",
        }),
        Influencer(name="Emma Storey-Gordon", handles={
            Platform.Instagram: "esgfitness",
            Platform.YouTube: "esgfitness",
        }),
        Influencer(name="Lisa Cross", handles={
            Platform.TikTok: "bblisacross",
        }),
        Influencer(name="Adam Maxted", handles={
            Platform.YouTube: "adammaxted2262",
        }),
        Influencer(name="Victoria Niamh", handles={
            Platform.TikTok: "victorianiamh",
        }),
        Influencer(name="Sean Casey", handles={}),
    ]


MOCK_INFLUENCERS = _build_mock_influencers()


class _FixtureHandler(http.server.SimpleHTTPRequestHandler):
    fixture_content: bytes = b""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.fixture_content)))
        self.end_headers()
        self.wfile.write(self.fixture_content)
    def log_message(self, format, *args):
        pass


class _E2EPipelineRunner(BasePipelineRunner):
    def __init__(self, local_url, audit, **kwargs):
        super().__init__(name_resolution=False, **kwargs)
        self._local_url = local_url
        self._audit = audit

    async def _search_and_extract_influencers(self, jobs):
        job = jobs[0]
        crawl_svc = CrawlService(self._audit)
        pages = await crawl_svc.crawl_urls([
            (self._local_url, "site:gymfluencers.agency fitness influencers UK"),
        ])
        self._stats.record_crawl(pages, dropped=crawl_svc.dropped_count, retries=crawl_svc.retry_count)
        page = pages[0]

        handle_svc = HandleExtractionService(self._audit)

        async def mock_llm_extract(pages, platform, category_key, sub_name, region, year, sample_n=None):
            from config import OUTPUT_TOKENS_PER_INFLUENCER
            if not pages:
                return {}, 0, 0
            return {pages[0].url: list(MOCK_INFLUENCERS)}, 3800, len(MOCK_INFLUENCERS) * OUTPUT_TOKENS_PER_INFLUENCER

        with (
            patch("services.extraction.HandleExtractionService.needs_llm", return_value=True),
            patch("services.extraction.LLMExtractionService.LLMExtractionService.extract", side_effect=mock_llm_extract),
        ):
            extract_result = await handle_svc.extract_all_handles(
                pages, platform=job.platform.value, category_key=job.category_key,
                sub_name=job.sub.sub_name, region=job.region.label, year="2026",
                direct_handles=[], sample_n=None,
            )
        self._stats.record_extraction(extract_result)

        from services.enrichment.NameToHandleService import NameToHandleService
        enrich_svc = NameToHandleService(self._audit, delay_seconds=0)
        mock_ddgs = MagicMock()
        mock_ddgs.text.return_value = []
        enrich_svc._ddgs = mock_ddgs
        unique = enrich_svc.resolve_cross_account_handles(extract_result.all_merged, platform=job.platform)
        self._stats.record_enrichment(
            unique_count=len(unique),
            handles_filled=sum(1 for inf in unique if inf.handles),
            retries=enrich_svc.retries, failures=enrich_svc.failures,
        )

        CategoryProvenanceTagger.tag_from_job(
            influencers=unique,
            category_key=job.category_key,
            sub_name=job.sub.sub_name,
        )
        return GatherResult(
            influencers=unique,
            name_tracker=extract_result.name_tracker,
            job_outcomes=[JobOutcome(job=job, search_results=None, errored=None)],
        )

    async def _on_config_search_finished(self, job, search_results):
        pass

    def _report_mode(self):
        return "e2e-test"


async def main():
    html_bytes = FIXTURE_HTML.read_bytes()
    _FixtureHandler.fixture_content = html_bytes
    server = http.server.HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    local_url = f"http://127.0.0.1:{port}/gymfluencers_uk_fitness.html"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            with (
                patch("services.crawling.CrawlService.PAGES_DIR", tmp_path / "pages"),
                patch("services.extraction.LLMExtractionService.RAW_DIR", tmp_path / "raw"),
                patch("services.reporting.ResultAssembler.REPORTS_DIR", tmp_path / "reports"),
                patch("services.reporting.ResultAssembler.RESULTS_DIR", tmp_path / "results"),
                patch("base_pipeline.RESULTS_DIR", tmp_path / "results"),
                patch("base_pipeline.REPORTS_DIR", tmp_path / "reports"),
                patch("base_pipeline.AUDIT_DIR", tmp_path / "audit"),
            ):
                audit = AuditLog(tmp_path / "audit", "e2e_html_test")
                job = SeedJob(
                    platform=Platform.Instagram,
                    region=Region(code=RegionCode.UK, language="en", label="United Kingdom"),
                    category_key="FITNESS",
                    sub=SubCategory(
                        sub_name="Fitness", is_top_level=True,
                        search_prompt="fitness influencers", alt_search_terms=[],
                        known_sources=["gymfluencers.agency"], platform_notes="",
                        region_notes="", difficulty=Difficulty.EASY, strict_slugs=[],
                    ),
                )

                runner = _E2EPipelineRunner(local_url=local_url, audit=audit)
                seeds = await runner.run([job])

                # Save golden fixtures
                GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

                # Find run directory
                results_dir = tmp_path / "results"
                run_dirs = [d for d in results_dir.iterdir() if d.is_dir()]
                assert len(run_dirs) == 1, f"Expected 1 run dir, got {len(run_dirs)}"
                run_dir = run_dirs[0]

                # seeds.json — normalize random ports for stable diffs
                seeds_data = json.loads((run_dir / "seeds.json").read_text())
                seeds_data = _normalize_ports(seeds_data)
                (GOLDEN_DIR / "seeds.json").write_text(
                    json.dumps(seeds_data, indent=2, ensure_ascii=False)
                )
                print(f"  Saved seeds.json ({len(seeds_data)} records)")

                # unresolved_names.json
                unresolved_data = json.loads((run_dir / "unresolved_names.json").read_text())
                unresolved_data = _normalize_ports(unresolved_data)
                (GOLDEN_DIR / "unresolved_names.json").write_text(
                    json.dumps(unresolved_data, indent=2, ensure_ascii=False)
                )
                print(f"  Saved unresolved_names.json ({len(unresolved_data)} records)")

                # output.json — build from seeds (the pipeline_output equivalent)
                output_data = [s.to_dict() if hasattr(s, 'to_dict') else {"name": s.name} for s in seeds]
                output_data = _normalize_ports(output_data)
                (GOLDEN_DIR / "output.json").write_text(
                    json.dumps(output_data, indent=2, ensure_ascii=False)
                )
                print(f"  Saved output.json ({len(output_data)} records)")

                # report — strip timestamps for stable comparison
                report_text = (run_dir / "report.md").read_text()
                stable = re.sub(r"\d{4}-\d{2}-\d{2}[T_]\d{2}[:\d]*\S*", "<TIMESTAMP>", report_text)
                stable = re.sub(r"Generated: .*", "Generated: <TIMESTAMP>", stable)
                (GOLDEN_DIR / "report.md").write_text(stable)
                print(f"  Saved report.md ({len(stable)} chars)")

                # validation results
                vr = runner.validation_results
                vr_data = {}
                for key, result in vr.items():
                    if result:
                        vr_data[key] = {
                            "pass_rate": result.pass_rate,
                            "found": sorted(result.found),
                            "missing": sorted(result.missing),
                            "expected": sorted(result.expected),
                        }
                (GOLDEN_DIR / "validation_results.json").write_text(
                    json.dumps(vr_data, indent=2, ensure_ascii=False)
                )
                print(f"  Saved validation_results.json")

                print(f"\n  Golden fixtures saved to: {GOLDEN_DIR}")

    finally:
        server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
