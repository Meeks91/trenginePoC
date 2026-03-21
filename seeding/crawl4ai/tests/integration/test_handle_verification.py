"""
Integration Test: Handle HTTP Verification
=============================================
Verifies that extracted handles resolve to real profiles by hitting
the platform URL and checking for HTTP 200.

Marked @pytest.mark.network — requires internet, skipped in CI.
Uses a subset of high-confidence handles from fixture ground truth.

Run with:
    PYTHONPATH="." python3 -m pytest tests/integration/test_handle_verification.py -v -m network
"""

from pathlib import Path

import pytest

# Try to import httpx — skip all tests if not available
httpx = pytest.importorskip("httpx")

from services.extraction.RegexHandleExtractorService import (
    extract_handles_from_html,
)

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


# ══════════════════════════════════════════════════════════════════════
# Profile URL builders
# ══════════════════════════════════════════════════════════════════════

_PLATFORM_URL_MAP = {
    "Instagram": "https://www.instagram.com/{handle}/",
    "TikTok": "https://www.tiktok.com/@{handle}",
    "YouTube": "https://www.youtube.com/@{handle}",
    # Twitter/X is too aggressive with bot detection — skip
}


def _build_url(handle: str, platform: str) -> str | None:
    """Build a profile URL for a handle on a given platform."""
    template = _PLATFORM_URL_MAP.get(platform)
    if not template:
        return None
    return template.format(handle=handle)


# ══════════════════════════════════════════════════════════════════════
# Ground truth handles to verify (known-good from fixture auditing)
# ══════════════════════════════════════════════════════════════════════

# These are high-confidence handles that appear in URL-based extraction
# from real fixture files — they should all resolve to real profiles.
VERIFIED_HANDLES = [
    # From gymfluencers_uk_fitness.html
    ("alex.beattie", "TikTok"),
    ("esgfitness", "YouTube"),
    # From feedspot_fitness_ig.html
    ("kayla_itsines", "Instagram"),
    ("jeff_seid", "Instagram"),
    ("whitneyysimmons", "Instagram"),
    # From theinfluenceroom_uk.html
    ("emilymouu", "Instagram"),
    ("emilymouu", "TikTok"),
    # From modash_uk_food.html
    ("lungisalwaysbaking", "Instagram"),
    ("sophiehlbrown", "Instagram"),
    # From clickanalytic_fitness.html
    ("tiboinshape", "Instagram"),
]


# ══════════════════════════════════════════════════════════════════════
# Network verification tests
# ══════════════════════════════════════════════════════════════════════

@pytest.mark.network
class TestHandleHTTPVerification:
    """Verify extracted handles resolve to real profiles (HTTP 200).

    These tests hit actual social media platforms so they:
      - Require internet access
      - Are rate-limited (1 request per test, with pauses)
      - May flake if platforms are down or URLs change
      - Are skipped by default (-m 'not network')
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """Create a shared httpx client."""
        self.client = httpx.Client(
            follow_redirects=True,
            timeout=15.0,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
        )
        yield
        self.client.close()

    @pytest.mark.parametrize("handle,platform", VERIFIED_HANDLES)
    def test_handle_resolves(self, handle: str, platform: str):
        """Handle should resolve to HTTP 200 on its platform."""
        url = _build_url(handle, platform)
        if url is None:
            pytest.skip(f"No URL template for platform: {platform}")

        resp = self.client.get(url)

        # Accept 200 or 3xx (some platforms redirect)
        assert resp.status_code < 400, (
            f"{handle} on {platform} returned {resp.status_code}\n"
            f"  URL: {url}\n"
            f"  Final URL: {resp.url}"
        )


@pytest.mark.network
class TestExtractedHandlesFromFixture:
    """Extract handles from a real fixture, then verify top N via HTTP.

    This is the full pipeline test: fixture → regex → HTTP verify.
    """

    def test_modash_top_handles_resolve(self):
        """Top 5 IG handles from modash_uk_food.html should resolve."""
        html = (FIXTURES_DIR / "modash_uk_food.html").read_text(errors="replace")
        results = extract_handles_from_html(html)
        ig_handles = [
            r.handle for r in results
            if r.platform == "Instagram"
        ][:5]

        assert len(ig_handles) >= 3, (
            f"Expected ≥3 IG handles from modash, got {len(ig_handles)}"
        )

        with httpx.Client(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TrendPuppy/1.0)"},
        ) as client:
            resolved = 0
            for handle in ig_handles:
                url = f"https://www.instagram.com/{handle}/"
                try:
                    resp = client.get(url)
                    if resp.status_code < 400:
                        resolved += 1
                except Exception:
                    pass  # Network errors don't fail the test

            # At least 60% of top handles should resolve
            assert resolved >= len(ig_handles) * 0.6, (
                f"Only {resolved}/{len(ig_handles)} IG handles resolved from modash"
            )

    def test_gymfluencers_tt_handles_resolve(self):
        """TikTok handles from gymfluencers fixture should resolve."""
        html = (FIXTURES_DIR / "gymfluencers_uk_fitness.html").read_text(
            errors="replace"
        )
        results = extract_handles_from_html(html)
        tt_handles = [
            r.handle for r in results
            if r.platform == "TikTok"
        ]

        assert len(tt_handles) >= 2, (
            f"Expected ≥2 TT handles from gymfluencers, got {len(tt_handles)}"
        )

        with httpx.Client(
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; TrendPuppy/1.0)"},
        ) as client:
            resolved = 0
            for handle in tt_handles[:3]:
                url = f"https://www.tiktok.com/@{handle}"
                try:
                    resp = client.get(url)
                    if resp.status_code < 400:
                        resolved += 1
                except Exception:
                    pass

            assert resolved >= 1, (
                f"0/{len(tt_handles[:3])} TT handles resolved from gymfluencers"
            )
