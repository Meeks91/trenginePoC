"""
scrape_ig_bios.py — One-off script to extract Instagram bios via crawl4ai.

Opens a VISIBLE browser so you can log in, then crawls each profile page
and extracts the bio text from the authenticated, JS-rendered DOM.

Usage:
    source ../.venv/bin/activate
    python scripts/scrape_ig_bios.py
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

# ── Handles to scrape ──

HANDLES: list[str] = [
    "oneractive",
    "pilates949",
    "missy._.fit",
    "mussbefitt",
    "kelechnekoff",
    "kristinadedwards_",
    "amandatress",
    "canesfootball",
    "sincerelyjules",
    "duvallco",
    "readysetflow",
    "celestpereirapt",
    "jcmartinezfit",
    "ishimwenaomie5_",
    "the.littlebeast",
]

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "results"
DELAY_BETWEEN_REQUESTS = 4.0  # IG rate-limits aggressively

# ── JS to extract bio from rendered DOM ──

# Instagram renders the bio in the header section.  The bio lives inside the
# profile header, typically in a <span> inside a div with the class containing
# "-webkit-line-clamp" or inside the section after follower counts.
# This JS tries multiple selectors and returns the first hit.
EXTRACT_BIO_JS = """
(() => {
    // Strategy 1: IG's React data includes __additionalData or __next_data
    // with the user object.  Look for the biography in the page's JSON data.
    const scripts = document.querySelectorAll('script[type="application/json"]');
    for (const script of scripts) {
        try {
            const text = script.textContent;
            // Look for biography field near the username
            const bioMatch = text.match(/"biography":"((?:[^"\\\\]|\\\\.)*)"/);
            if (bioMatch) {
                const bio = bioMatch[1]
                    .replace(/\\\\n/g, '\\n')
                    .replace(/\\\\u([0-9a-fA-F]{4})/g, (m, g) => String.fromCharCode(parseInt(g, 16)));
                // Verify this isn't a placeholder by checking if username also appears nearby
                const handleMatch = text.match(/"username":"((?:[^"\\\\]|\\\\.)*)"/);
                if (handleMatch) {
                    return JSON.stringify({
                        bio: bio,
                        username: handleMatch[1],
                        source: 'json_script'
                    });
                }
            }
        } catch(e) { continue; }
    }

    // Strategy 2: look for the bio in the rendered profile header section
    // IG profile layout: header > section with display name, bio, link
    const headerSection = document.querySelector('header section');
    if (headerSection) {
        // Bio is usually in a span inside the section, after the stats row
        const spans = headerSection.querySelectorAll('span');
        const candidates = [];
        for (const span of spans) {
            const text = span.textContent.trim();
            // Skip follower counts, "posts", "followers", "following", buttons
            if (/^[\\d,.]+[KkMm]?$/.test(text)) continue;
            if (/^(posts?|followers?|following|edit profile|share profile|message|follow)$/i.test(text)) continue;
            if (text.length > 10 && text.length < 500) {
                candidates.push(text);
            }
        }
        if (candidates.length > 0) {
            return JSON.stringify({
                bio: candidates[0],
                source: 'header_span'
            });
        }
    }

    // Strategy 3: meta description with actual bio content
    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
        const content = metaDesc.getAttribute('content') || '';
        // IG meta: "N Followers, N Following, N Posts - BIO TEXT from Name (@handle)"
        const match = content.match(/Posts\\s*[-–—]\\s*(.+?)\\s*from\\s+/i);
        if (match) {
            return JSON.stringify({
                bio: match[1].trim(),
                source: 'meta_description'
            });
        }
    }

    return JSON.stringify({bio: null, source: 'none'});
})()
"""


# ── Main crawl logic ──

async def scrape_bios() -> dict[str, dict[str, str | None]]:
    """Open visible browser, let user log in, then crawl all IG profiles."""
    results: dict[str, dict[str, str | None]] = {}

    browser_config = BrowserConfig(
        headless=False,
        viewport_width=1920,
        viewport_height=1080,
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    )

    # Login config — just load the page, no bio extraction
    login_config = CrawlerRunConfig(
        session_id="ig_session",
        page_timeout=120000,
        wait_until="domcontentloaded",
    )

    # Profile crawl config — execute JS to extract bio
    profile_config = CrawlerRunConfig(
        page_timeout=60000,
        remove_overlay_elements=True,
        wait_until="domcontentloaded",
        delay_before_return_html=5.0,  # Wait for React to render bio
        js_code=EXTRACT_BIO_JS,
        session_id="ig_session",
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Step 1: Login
        print("\n🔑  Browser opening — you have 60 seconds to log in.")
        print("    Log in via the browser window, then sit tight.\n")

        await crawler.arun(
            url="https://www.instagram.com/accounts/login/",
            config=login_config,
        )
        print("    ⏳  Waiting 60s for login...")
        await asyncio.sleep(60)
        print("    ✅  Continuing with authenticated session.\n")

        # Step 2: Crawl each profile
        for i, handle in enumerate(HANDLES, start=1):
            url = f"https://www.instagram.com/{handle}/"
            print(f"  [{i:2d}/{len(HANDLES)}]  {url}  ...", end="  ", flush=True)

            try:
                result = await crawler.arun(url=url, config=profile_config)
            except Exception as exc:
                print(f"❌  error: {exc}")
                results[handle] = {"handle": f"@{handle}", "bio": None, "error": str(exc)}
                if i < len(HANDLES):
                    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
                continue

            if not result.success:
                error_msg = getattr(result, "error_message", "unknown")
                print(f"❌  failed: {error_msg}")
                results[handle] = {"handle": f"@{handle}", "bio": None, "error": str(error_msg)}
                if i < len(HANDLES):
                    await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
                continue

            # The JS execution result is in result.js_result or
            # we need to check result.extracted_content
            bio: str | None = None
            source = "none"

            # Try to get JS execution result
            js_result = getattr(result, "js_execution_result", None)
            if not js_result:
                js_result = getattr(result, "extracted_content", None)

            if js_result and isinstance(js_result, str):
                try:
                    data = json.loads(js_result)
                    bio = data.get("bio")
                    source = data.get("source", "js")
                    # If json_script source, verify the username matches
                    if source == "json_script":
                        found_username = data.get("username", "")
                        if found_username and found_username != handle:
                            # Wrong profile's data, skip
                            bio = None
                            source = "none"
                except (json.JSONDecodeError, TypeError):
                    pass

            # Fallback: scan the HTML for biography field near the handle
            if not bio and result.html:
                import re
                # Find all biography fields and their nearby usernames
                bio_pattern = re.compile(
                    r'"username"\s*:\s*"' + re.escape(handle) + r'"'
                    r'.*?"biography"\s*:\s*"((?:[^"\\]|\\.)*)"',
                    re.DOTALL,
                )
                match = bio_pattern.search(result.html)
                if not match:
                    # Try reverse order
                    bio_pattern2 = re.compile(
                        r'"biography"\s*:\s*"((?:[^"\\]|\\.)*)"'
                        r'.*?"username"\s*:\s*"' + re.escape(handle) + r'"',
                        re.DOTALL,
                    )
                    match = bio_pattern2.search(result.html)
                if match:
                    bio = match.group(1).strip()
                    bio = bio.encode().decode("unicode_escape", errors="replace")
                    source = "html_regex"

            if bio:
                display = bio[:80] + "..." if len(bio) > 80 else bio
                print(f"✅  ({source}) {display}")
            else:
                print("⚠️   no bio found")

            results[handle] = {"handle": f"@{handle}", "bio": bio}

            # Rate limit between requests
            if i < len(HANDLES):
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)

    return results


async def main() -> None:
    print(f"\n{'='*60}")
    print(f"  Instagram Bio Scraper — {len(HANDLES)} profiles")
    print("  Mode: visible browser + manual login")
    print(f"{'='*60}")

    results = await scrape_bios()

    # Save output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H.%M")
    output_path = OUTPUT_DIR / f"ig_bios_{timestamp}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    found = sum(1 for r in results.values() if r.get("bio"))
    missing = len(results) - found

    print(f"\n{'='*60}")
    print(f"  Done: {found} bios found, {missing} missing")
    print(f"  Output: {output_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
