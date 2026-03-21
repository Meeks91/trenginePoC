"""
Unit Tests: CrawlService — HTML→Markdown handle preservation
=============================================================
Verifies that social media handles in raw HTML survive into
fit_markdown after Crawl4AI's markdown conversion + PruningContentFilter.

This test catches config issues like exclude_external_links=True
stripping social media URLs from the markdown.
"""

import asyncio
import functools
import http.server
import sys
import threading
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.crawling.CrawlService import CrawlService
from services.audit.AuditService import AuditLog


FIXTURE_HTML = Path(__file__).resolve().parent.parent / "fixtures" / "gymfluencers_uk_fitness.html"

# Ground truth: handles that exist in the raw HTML fixture.
# Grouped by platform as they appear in the source markup.
HANDLES_IN_HTML = {
    "TikTok": ["alex.beattie", "bblisacross", "courtneyblackfitness", "victorianiamh"],
    "YouTube": ["esgfitness", "adammaxted2262", "mac_griffiths"],
}

ALL_HANDLES = [h for handles in HANDLES_IN_HTML.values() for h in handles]


def test_handles_survive_in_fit_markdown():
    """Handles in raw HTML MUST survive into fit_markdown after CrawlService processing.

    This catches config mistakes like exclude_external_links=True
    which strips social media URLs from the markdown entirely.
    """
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(FIXTURE_HTML.parent),
    )
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/{FIXTURE_HTML.name}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test_crawl")
            svc = CrawlService(audit)
            pages = asyncio.run(svc.crawl_urls([(url, "test")]))

        assert len(pages) == 1
        page = pages[0]
        assert page.success

        fit_lower = page.fit_markdown.lower()

        missing = []
        for handle in ALL_HANDLES:
            if handle.lower() not in fit_lower:
                missing.append(handle)

        assert not missing, (
            f"Handles missing from fit_markdown — likely stripped by "
            f"exclude_external_links or markdown conversion:\n"
            f"  Missing: {missing}\n"
            f"  All expected: {ALL_HANDLES}"
        )
    finally:
        srv.shutdown()


def test_handles_survive_per_platform():
    """Each platform's handles should be extractable from fit_markdown.

    Verifies handles grouped by platform so failures pinpoint
    which platform's links are being stripped.
    """
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(FIXTURE_HTML.parent),
    )
    srv = http.server.HTTPServer(("127.0.0.1", 0), handler)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/{FIXTURE_HTML.name}"

    try:
        with tempfile.TemporaryDirectory() as tmp:
            audit = AuditLog(Path(tmp), "test_crawl")
            svc = CrawlService(audit)
            pages = asyncio.run(svc.crawl_urls([(url, "test")]))

        page = pages[0]
        fit_lower = page.fit_markdown.lower()

        for platform, handles in HANDLES_IN_HTML.items():
            missing = [h for h in handles if h.lower() not in fit_lower]
            assert not missing, (
                f"{platform} handles missing from fit_markdown: {missing}"
            )
    finally:
        srv.shutdown()


# ── Regression: _dropped_count / _retry_count init ──

def test_crawl_service_counters_initialised():
    """REGRESSION: dropped_count and retry_count must be accessible before crawl_urls().

    Old code used getattr(self, '_dropped_count', 0) because the attributes
    were only set inside crawl_urls(). Now they're initialised in __init__.
    """
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = CrawlService(audit)

        assert svc.dropped_count == 0, "dropped_count must be 0 before any crawl"
        assert svc.retry_count == 0, "retry_count must be 0 before any crawl"
