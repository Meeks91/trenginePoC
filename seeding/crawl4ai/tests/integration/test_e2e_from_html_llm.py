"""
Integration Test: E2E From HTML — Real LLM
============================================
Same pipeline as test_e2e_from_html.py but with REAL LLM calls.
Uses soft assertions for LLM non-determinism.

Mock boundaries:
  1. HTML source: served from localhost (deterministic).
  2. LLM extraction: REAL Gemini API call.
  3. DDG cross-platform lookup: MOCKED (tested separately in cross-platform tests).

Requires GEMINI_API_KEY to be set. Warns if missing.

Run with:
    PYTHONPATH="." pytest tests/integration/test_e2e_from_html_llm.py -v -s
"""

import asyncio
import http.server
import logging
import tempfile
import threading
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from config import GEMINI_API_KEY, LLM_PROVIDER
from config.schema import PipelineStats, JobBreakdown, Platform
from services.audit.AuditService import AuditLog
from services.crawling.CrawlService import CrawlService
from services.extraction.LLMExtractionService import LLMExtractionService
from services.handleResolution.HandleFromNameService import HandleFromNameService
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService
from services.validation.IngestionValidator import IngestionValidator
from services.reporting.PipelineReporter import PipelineReporter

logger = logging.getLogger(__name__)


FIXTURE_HTML = Path(__file__).resolve().parent.parent / "fixtures" / "gymfluencers_uk_fitness.html"

EXPECTED_NAMES = {
    "joe wicks",
    "alex beattie",
    "lucy davis",
    "courtney black",
    "michael griffiths",
    "emma storey-gordon",
    "lisa cross",
    "adam maxted",
    "victoria niamh",
    "sean casey",
}

HANDLES_IN_HTML: dict[str, dict[str, str]] = {
    "alex beattie":       {"TikTok": "alex.beattie"},
    "lisa cross":         {"TikTok": "bblisacross"},
    "courtney black":     {"TikTok": "courtneyblackfitness"},
    "victoria niamh":     {"TikTok": "victorianiamh"},
    "emma storey-gordon": {"YouTube": "esgfitness"},
    "adam maxted":        {"YouTube": "adammaxted2262"},
    "michael griffiths":  {"YouTube": "mac_griffiths"},
}

ALL_EXPECTED_HANDLES = {
    h for handles in HANDLES_IN_HTML.values() for h in handles.values()
}


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


def _start_server(html_bytes: bytes) -> tuple[http.server.HTTPServer, int]:
    _FixtureHandler.fixture_content = html_bytes
    server = http.server.HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


@pytest.mark.asyncio
async def test_e2e_from_html_real_llm():
    """Full pipeline with REAL Gemini call — soft LLM assertions, hard pipeline assertions."""

    if not GEMINI_API_KEY:
        logger.warning(
            "GEMINI_API_KEY not set — skipping real-LLM integration test. "
            "Set the env var to run this test."
        )
        pytest.skip("GEMINI_API_KEY not set")

    assert FIXTURE_HTML.exists(), f"HTML fixture not found: {FIXTURE_HTML}"
    html_bytes = FIXTURE_HTML.read_bytes()
    print(f"Loaded HTML fixture: {len(html_bytes):,} bytes")

    server, port = _start_server(html_bytes)
    local_url = f"http://127.0.0.1:{port}/gymfluencers_uk_fitness.html"
    print(f"Serving fixture at {local_url}")

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            with (
                patch("services.crawling.CrawlService.PAGES_DIR", tmp_path / "pages"),
                patch("services.extraction.LLMExtractionService.RAW_DIR", tmp_path / "raw"),
            ):
                audit = AuditLog(tmp_path / "audit", "e2e_html_llm_test")

                # ── Crawl (REAL) ──
                print("\n--- Crawl + Filter ---")
                crawl_svc = CrawlService(audit)
                pages = await crawl_svc.crawl_urls([
                    (local_url, "site:gymfluencers.agency fitness influencers UK"),
                ])

                # HARD: crawl is deterministic
                assert len(pages) == 1, f"Expected 1 page, got {len(pages)}"
                page = pages[0]
                assert page.success, f"Crawl failed: {page.error}"
                assert len(page.raw_markdown) > 500
                assert len(page.fit_markdown) > 100
                assert page.fit_token_estimate < page.raw_token_estimate
                assert page.md_path is not None
                print(f"  raw: {page.raw_token_estimate:,} → fit: {page.fit_token_estimate:,} tokens")

                # ── Extract (REAL LLM) ──
                print("\n--- LLM Extraction (REAL) ---")
                extract_svc = LLMExtractionService(audit)
                url_to_inf, in_tok, out_tok = await extract_svc.extract(
                    pages=pages,
                    platform=Platform.Instagram,
                    category_key="FITNESS",
                    sub_name="Fitness",
                    region="United Kingdom",
                    year="2026",
                )

                influencers = url_to_inf.get(local_url, [])
                # SOFT: LLM is non-deterministic — at least 3 of 10
                assert len(influencers) >= 3, (
                    f"Expected at least 3 influencers, got {len(influencers)}"
                )
                print(f"  Extracted {len(influencers)} influencers")

                found_names = {inf.name.lower() for inf in influencers}
                missing_names = [n for n in EXPECTED_NAMES if not any(n in fn for fn in found_names)]
                extracted_count = len(EXPECTED_NAMES) - len(missing_names)
                assert extracted_count >= 3, (
                    f"LLM extracted only {extracted_count}/{len(EXPECTED_NAMES)} names "
                    f"(need >= 3): missing {missing_names}"
                )
                if missing_names:
                    print(f"  WARN: LLM missed {len(missing_names)} names: {missing_names}")
                print(f"  ✓ {extracted_count}/{len(EXPECTED_NAMES)} expected names extracted")

                # SOFT: handle verification (LLM may or may not include handles)
                handle_hits = 0
                for name_lower, platform_handles in HANDLES_IN_HTML.items():
                    inf = next((i for i in influencers if name_lower in i.name.lower()), None)
                    if not inf:
                        continue
                    for platform_str, expected_handle in platform_handles.items():
                        inf_handle_vals = [h.lower().lstrip("@").replace(" ", "") for h in inf.handles.values()]
                        exp = expected_handle.lower()
                        if any(exp in h or h in exp for h in inf_handle_vals):
                            handle_hits += 1
                if handle_hits == 0:
                    print(f"  WARN: LLM extracted 0/{len(ALL_EXPECTED_HANDLES)} expected handles")
                else:
                    print(f"  ✓ {handle_hits}/{len(ALL_EXPECTED_HANDLES)} handles matched")

                # ── Enrich + Dedup (DDG MOCKED) ──
                print("\n--- Enrich + Dedup (DDG mocked) ---")
                resolver = CrossPlatformHandleResolverService(
                    audit, search_client=MagicMock(), delay_seconds=0,
                )

                unique = resolver.resolve(influencers)

                # HARD: enrichment pipeline is deterministic — must not lose data
                assert len(unique) >= len(influencers), (
                    f"Enrichment lost influencers: {len(influencers)} in → {len(unique)} out"
                )
                print(f"  {len(unique)} unique influencers after dedup")

                # HARD: every LLM-extracted name must survive enrichment
                final_names = {inf.name.lower() for inf in unique}
                for fn in found_names:
                    assert any(fn in n for n in final_names), (
                        f"Name '{fn}' extracted by LLM but lost during enrichment/dedup"
                    )
                print("  ✓ All LLM-extracted names survived pipeline")

                # HARD: handles must not be lost through enrichment
                handles_filled = sum(1 for inf in unique if inf.handles)
                llm_handles = sum(1 for inf in influencers if inf.handles)
                assert handles_filled >= llm_handles, (
                    f"Enrichment lost handles: {llm_handles} in → {handles_filled} out"
                )

                # ── Canary Validation ──
                print("\n--- Canary Validation ---")
                validator = IngestionValidator()
                vr = validator.validate(unique, "FITNESS", "Fitness", "UK")
                if vr:
                    print(f"  Canary pass rate: {vr.pass_rate:.0%} "
                          f"({len(vr.found)}/{len(vr.expected)})")
                    if vr.missing:
                        print(f"  Missing canaries: {', '.join(vr.missing)}")

                # ── Report ──
                print("\n--- Report ---")
                reporter = PipelineReporter()
                stats = PipelineStats(
                    urls_discovered=1,
                    pages_crawled=1,
                    pages_failed=0,
                    pages_extracted=1,
                    influencers_raw=len(influencers),
                    influencers_deduped=len(unique),
                    handles_filled=handles_filled,
                    handles_in_source=len(ALL_EXPECTED_HANDLES),
                    handles_retrieved=handle_hits,
                    total_input_tokens=in_tok,
                    total_output_tokens=out_tok,
                )
                validation_results = {"FITNESS_Fitness_IG_UK": vr} if vr else {}
                job_results = [
                    JobBreakdown(
                        category="FITNESS",
                        sub="Fitness",
                        platform=Platform.Instagram,
                        region="UK",
                        influencers_found=len(unique),
                        handles_filled=handles_filled,
                        handles_in_source=len(ALL_EXPECTED_HANDLES),
                        handles_retrieved=handle_hits,
                        pages_crawled=1,
                    )
                ]
                report_path = reporter.generate(
                    run_dir=tmp_path / "reports" / "e2e_llm_run",
                    stats=stats,
                    validation_results=validation_results,
                    model=LLM_PROVIDER,
                    mode="e2e-llm-test",
                    job_results=job_results,
                    influencers=unique,
                )

                # HARD: report structure is deterministic
                assert report_path.exists(), "Report file not created"
                report_content = report_path.read_text()
                assert "Pipeline Report" in report_content
                assert "Token Usage" in report_content
                assert "Breakdown by Job" in report_content
                assert "Influencers Found" in report_content
                # HARD: every handle-bearing influencer must be in the report
                for inf in unique:
                    if inf.handles:
                        assert inf.name in report_content, (
                            f"Influencer '{inf.name}' missing from report"
                        )
                print(f"  ✓ Report verified: {report_path.name}")

                # ── Audit Trail ──
                assert len(audit.entries) > 0, "Audit trail is empty"
                phases = {e.phase for e in audit.entries}
                assert "crawl" in phases, "Audit missing crawl entries"
                assert "extract" in phases, "Audit missing extract entries"
                print(f"  Audit: {len(audit.entries)} entries across phases {phases}")

                print(f"\nE2E from-HTML LLM test PASSED ({extracted_count}/{len(EXPECTED_NAMES)} names)")

    finally:
        server.shutdown()


if __name__ == "__main__":
    asyncio.run(test_e2e_from_html_real_llm())
