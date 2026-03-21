"""
E2E integration test — Reddit name extraction (deterministic, localhost only).

Uses a trimmed HTML fixture from r/bodyweightfitness containing exactly 3
comments with known influencer names. crawl4ai produces fit_markdown from
the HTML; NameExtractor extracts candidate names.

DDG resolution (Phase 2) moved to scripts/test_nr_resolution.py — run manually.
"""

from __future__ import annotations

import asyncio
import http.server
import threading
from collections.abc import Generator
from pathlib import Path

import pytest

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

from services.extraction.NameExtractor import extract_candidate_names

# ── Fixture path ──

FIXTURE_HTML = (
    Path(__file__).parent.parent / "fixtures" / "reddit_bodyweightfitness.html"
)

# ── Ground truth from the trimmed HTML ──

# These 3 names MUST appear in the extracted names.
# The trimmed HTML keeps only the comments containing them.
TARGET_NAMES: set[str] = {
    "Jeff Nippard",
    "Sean Nalewanyj",
    "Chris Heria",
}

# Reddit UI noise that blocklists should filter out.
NOISE_NAMES: set[str] = {
    "Learn More",
    "Sign Up",
    "View More",
    "Read More",
    "Log In",
}

# Phase 2 (DDG resolution) moved to scripts/test_nr_resolution.py — run manually.


# ── Fixtures ──

class _FixtureHandler(http.server.SimpleHTTPRequestHandler):
    """Serve the trimmed HTML fixture on every GET."""

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(FIXTURE_HTML.read_bytes())

    def log_message(self, *args: object) -> None:  # suppress noise
        pass


@pytest.fixture(scope="module")
def fixture_server() -> Generator[str, None, None]:
    """Start a localhost HTTP server serving the fixture HTML."""
    server = http.server.HTTPServer(("127.0.0.1", 0), _FixtureHandler)
    port = server.server_address[1]
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    yield f"http://127.0.0.1:{port}/"
    server.shutdown()


@pytest.fixture(scope="module")
def fit_markdown(fixture_server: str) -> str:
    """Crawl the fixture server with crawl4ai, return fit_markdown."""

    async def _crawl() -> str:
        config = CrawlerRunConfig(
            wait_until="domcontentloaded",
            page_timeout=15_000,
        )
        async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
            result = await crawler.arun(url=fixture_server, config=config)
        assert result.success, f"crawl4ai failed: {getattr(result, 'error_message', '')}"
        md = result.markdown
        return getattr(md, "fit_markdown", None) or getattr(md, "raw_markdown", None) or str(md)

    return asyncio.run(_crawl())


@pytest.fixture(scope="module")
def extracted_names(fit_markdown: str) -> list[str]:
    """Extract candidate names from the fit_markdown."""
    return extract_candidate_names(fit_markdown)


# ══════════════════════════════════════════════════════════════════════
# Phase 1: Name Extraction (deterministic, no network beyond localhost)
# ══════════════════════════════════════════════════════════════════════


class TestRedditNameExtraction:
    """Verify NameExtractor finds target names from crawl4ai markdown."""

    def test_extracts_target_names(self, extracted_names: list[str]) -> None:
        names_lower = {n.lower() for n in extracted_names}
        for target in TARGET_NAMES:
            assert target.lower() in names_lower, (
                f"Expected '{target}' in extracted names, got: {extracted_names}"
            )

    def test_no_noise_names(self, extracted_names: list[str]) -> None:
        names_lower = {n.lower() for n in extracted_names}
        for noise in NOISE_NAMES:
            assert noise.lower() not in names_lower, (
                f"Noise name '{noise}' should have been filtered"
            )

    def test_all_names_are_multi_word(self, extracted_names: list[str]) -> None:
        for name in extracted_names:
            assert len(name.split()) >= 2, f"Single-word name leaked: '{name}'"
