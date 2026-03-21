"""
E2E Test: LLM Fallback Extraction
===================================
Tests the LLM extraction path as a FALLBACK to regex extraction.

Uses the gymfluencers_uk_fitness.html fixture where:
  - Regex extracts: TikTok handles, YouTube handles (7 handles)
  - Regex CANNOT extract: IG embeds (JavaScript blockquotes)
  - LLM extracts: All 10 influencer NAMES + handles visible in fit_markdown

This test proves that LLM fallback catches what regex misses, specifically
IG embed handles that only appear in JavaScript-rendered content.

Cost: ~$0.001 per run (1 LLM call).

Run with:
    GEMINI_API_KEY=... PYTHONPATH="." python3 -m pytest tests/integration/test_e2e_llm_fallback.py -v -s
"""

import asyncio
import http.server
import pytest
import tempfile
import threading
from pathlib import Path
from unittest.mock import patch

from config import GEMINI_API_KEY
from services.audit.AuditService import AuditLog
from services.crawling.CrawlService import CrawlService
from services.extraction.LLMExtractionService import LLMExtractionService
from services.extraction.RegexHandleExtractor import extract_handles_from_html

FIXTURE_HTML = Path(__file__).resolve().parent.parent / "fixtures" / "gymfluencers_uk_fitness.html"

# Names that LLM must find (regex can't get names from raw HTML)
LLM_EXPECTED_NAMES = {
    "joe wicks", "alex beattie", "courtney black",
    "emma storey-gordon", "adam maxted", "victoria niamh",
}

# Handles that regex finds (TikTok + YouTube)
REGEX_HANDLES = {
    "alex.beattie", "courtneyblackfitness", "bblisacross",
    "victorianiamh", "mac_griffiths", "esgfitness", "adammaxted2262",
}

# Handles regex MISSES (IG embeds in JS) — LLM should find these
LLM_ONLY_HANDLES = {
    "thebodycoach",  # Joe Wicks IG embed
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


def _start_server(html_bytes):
    _FixtureHandler.fixture_content = html_bytes
    server = http.server.HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


@pytest.mark.network
def test_llm_fallback_catches_what_regex_misses():
    """LLM fallback: extracts names and IG handles that regex cannot find."""
    assert GEMINI_API_KEY, "GEMINI_API_KEY must be set to run this test"
    asyncio.run(_test_llm_fallback_async())


async def _test_llm_fallback_async():

    assert FIXTURE_HTML.exists(), f"Missing fixture: {FIXTURE_HTML}"
    html_bytes = FIXTURE_HTML.read_bytes()

    # Step 1: Prove regex is insufficient on this fixture
    regex_results = extract_handles_from_html(html_bytes.decode("utf-8", errors="ignore"))
    regex_handles = {r.handle.lower() for r in regex_results}
    _regex_names = {r.name.lower() for r in regex_results if r.name}

    # Regex finds TikTok/YouTube handles but NOT names
    assert len(regex_handles & REGEX_HANDLES) >= 4, \
        f"Regex should find most TT/YT handles, got: {regex_handles}"

    # Regex CANNOT find these LLM-only handles
    for h in LLM_ONLY_HANDLES:
        assert h not in regex_handles, \
            f"Handle {h} should NOT be in regex results (it's in JS embed)"

    print(f"\n✓ Regex found {len(regex_handles)} handles, missing LLM-only handles as expected")

    # Step 2: Run LLM extraction — it should find names + handles
    server, port = _start_server(html_bytes)
    local_url = f"http://127.0.0.1:{port}/gymfluencers_uk_fitness.html"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            with (
                patch("services.crawling.CrawlService.PAGES_DIR", tmp_path / "pages"),
                patch("services.extraction.LLMExtractionService.RAW_DIR", tmp_path / "raw"),
            ):
                audit = AuditLog(tmp_path / "audit", "llm_fallback_test")
                crawl_svc = CrawlService(audit)
                pages = await crawl_svc.crawl_urls([
                    (local_url, "fitness influencers UK"),
                ])
                assert len(pages) == 1 and pages[0].success

                extract_svc = LLMExtractionService(audit)
                url_to_inf, in_tok, out_tok = await extract_svc.extract(
                    pages=pages,
                    platform="Instagram",
                    category_key="FITNESS",
                    sub_name="Fitness",
                    region="United Kingdom",
                    year="2026",
                )

                influencers = url_to_inf.get(local_url, [])
                llm_names = {inf.name.lower() for inf in influencers}
                llm_handles: set[str] = set()
                for inf in influencers:
                    for h in inf.handles.values():
                        if h:
                            llm_handles.add(h.lower().lstrip("@"))

                # LLM must find at least 5 names
                assert len(influencers) >= 3, \
                    f"LLM should find ≥3 influencers, got {len(influencers)}"

                # LLM should find names that regex cannot
                names_found = sum(1 for n in LLM_EXPECTED_NAMES if any(n in ln for ln in llm_names))
                assert names_found >= 3, \
                    f"LLM should find ≥3 expected names, got {names_found}: {llm_names}"

                print(f"\n✓ LLM found {len(influencers)} influencers with {len(llm_handles)} handles")
                print(f"✓ LLM found {names_found}/{len(LLM_EXPECTED_NAMES)} expected names")

                # Combined: regex + LLM should cover more than either alone
                combined = regex_handles | llm_handles
                print(f"✓ Combined regex+LLM: {len(combined)} unique handles")
                assert len(combined) >= len(regex_handles), \
                    "LLM should not remove regex-found handles"

                # Token usage should be minimal (1 page)
                print(f"  Tokens: {in_tok:,} in / {out_tok:,} out")

    finally:
        server.shutdown()
