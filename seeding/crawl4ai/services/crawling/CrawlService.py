"""
CrawlService — Crawl URLs with Crawl4AI, apply content filtering, save markdown.
No LLM calls.

Supports BFS link-following: after crawling initial URLs, extract same-domain
internal links from the markdown and crawl them too (depth-limited).
"""

from __future__ import annotations

import os
import re
from urllib.parse import urlparse, urljoin

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig

from services.audit.AuditService import AuditLog
from config import (
    PAGES_DIR, EXCLUDED_TAGS, WORD_COUNT_THRESHOLD, CRAWL_CONCURRENCY,
)
from config.settings import BFS_MAX_DEPTH, BFS_MAX_PAGES, CRAWL_MAX_RETRIES
from config.schema import PageResult, count_handles_in_html
from services.crawling.filters import create_markdown_generator


# Link patterns in markdown output: [text](url)
_MD_LINK = re.compile(r'\[([^\]]*)\]\((https?://[^\)]+)\)')

# Keywords that suggest a link leads to another influencer listicle page
_LISTICLE_KEYWORDS = re.compile(
    r'(?:influencer|creator|blogger|vlogger|youtuber|instagrammer|'
    r'top\s+\d+|best\s+\d+|list|roundup|follow|account)',
    re.IGNORECASE,
)


class CrawlService:
    """Fetch pages and produce fit_markdown. Supports BFS link-following."""

    def __init__(self, audit: AuditLog):
        self._audit = audit
        os.makedirs(PAGES_DIR, exist_ok=True)
        self._dropped_count: int = 0
        self._retry_count: int = 0

    async def crawl_urls(self, url_query_pairs: list[tuple[str, str]]) -> list[PageResult]:
        """Crawl all URLs with automatic retry via crawl4ai dispatcher.

        Uses SemaphoreDispatcher + RateLimiter for exponential backoff on
        429/503 responses. Detects and logs URLs silently dropped by arun_many.
        """
        if not url_query_pairs:
            return []

        urls = [u for u, _ in url_query_pairs]
        query_map = {u: q for u, q in url_query_pairs}

        config = CrawlerRunConfig(
            markdown_generator=create_markdown_generator(),
            excluded_tags=EXCLUDED_TAGS,
            word_count_threshold=WORD_COUNT_THRESHOLD,
            # NOTE: exclude_external_links must be False — social media handles
            # live in external links (instagram.com, tiktok.com, youtube.com).
            # Setting this to True strips them from the markdown entirely.
            exclude_external_links=False,
            remove_overlay_elements=True,
            wait_until="domcontentloaded",  # Read DOM before JS hydration (SSR pages have content in initial HTML)
            page_timeout=30000,         # 30s timeout for page load
        )

        # Wire up crawl4ai's built-in retry + rate limiting
        # Use importlib to bypass pytest's import rewriting — the project dir
        # 'crawl4ai' shadows the pip package during test collection.
        import importlib
        _dispatcher = importlib.import_module("crawl4ai.async_dispatcher")
        SemaphoreDispatcher = _dispatcher.SemaphoreDispatcher
        RateLimiter = _dispatcher.RateLimiter
        # Use importlib to bypass pytest's import rewriting — the project dir
        # 'crawl4ai' shadows the pip package during test collection.
        import importlib
        _dispatcher = importlib.import_module("crawl4ai.async_dispatcher")
        SemaphoreDispatcher = _dispatcher.SemaphoreDispatcher
        RateLimiter = _dispatcher.RateLimiter

        rate_limiter = RateLimiter(
            base_delay=(1.0, 3.0),
            max_delay=60.0,
            max_retries=CRAWL_MAX_RETRIES,
            rate_limit_codes=[429, 503],
        )
        dispatcher = SemaphoreDispatcher(
            semaphore_count=CRAWL_CONCURRENCY,
            rate_limiter=rate_limiter,
        )

        results: list[PageResult] = []
        total_retries = 0

        print(f"\n  --- Crawling {len(urls)} URLs (max_concurrent={CRAWL_CONCURRENCY}, max_retries={CRAWL_MAX_RETRIES}) ---")

        async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
            crawl_results = await crawler.arun_many(
                urls=urls,
                config=config,
                dispatcher=dispatcher,
            )

            # Track which URLs got results
            result_urls: set[str] = set()

            for result in crawl_results:
                url = result.url
                result_urls.add(url)
                query = query_map.get(url, "")

                # Track retries from dispatcher (if available)
                if hasattr(result, 'retry_count'):
                    total_retries += result.retry_count

                if not result.success:
                    error_msg = str(result.error_message) if hasattr(result, 'error_message') else "unknown"
                    print(f"    FAIL {url}: {error_msg}")
                    self._audit.log_page_failed(url, error_msg)
                    results.append(PageResult(
                        url=url, query=query,
                        raw_markdown="", fit_markdown="",
                        raw_token_estimate=0, fit_token_estimate=0,
                        success=False, error=error_msg,
                    ))
                    continue

                raw = result.markdown.raw_markdown or ""
                fit = result.markdown.fit_markdown or ""

                raw_tokens = len(raw) // 4
                fit_tokens = len(fit) // 4
                reduction = (1 - len(fit) / max(1, len(raw))) * 100

                md_path = self._save_markdown(url, fit)

                self._audit.log_page_success(url, raw_tokens, fit_tokens)
                print(f"    OK {url}  ({raw_tokens:,} -> {fit_tokens:,} tokens, -{reduction:.0f}%)")

                source_handles = count_handles_in_html(raw)

                results.append(PageResult(
                    url=url, query=query,
                    raw_markdown=raw, fit_markdown=fit,
                    raw_token_estimate=raw_tokens, fit_token_estimate=fit_tokens,
                    success=True, md_path=md_path,
                    handles_in_source=source_handles,
                ))

        # Detect and log dropped URLs (submitted but no result returned)
        dropped_urls = set(urls) - result_urls
        for dropped_url in dropped_urls:
            self._audit.log_page_failed(dropped_url, "dropped_by_crawler")
            print(f"    DROP {dropped_url}: silently dropped by arun_many")

        successes = sum(1 for r in results if r.success)
        failures = sum(1 for r in results if not r.success)
        dropped = len(dropped_urls)
        print(f"\n  Crawled {successes}/{len(urls)} pages ({failures} failed, {dropped} dropped, {total_retries} retries)")

        # Store counts for pipeline stats
        self._dropped_count = dropped
        self._retry_count = total_retries

        return results

    @property
    def dropped_count(self) -> int:
        return self._dropped_count

    @property
    def retry_count(self) -> int:
        return self._retry_count

    async def crawl_urls_bfs(
        self,
        url_query_pairs: list[tuple[str, str]],
        max_depth: int | None = None,
        max_extra_pages: int | None = None,
    ) -> list[PageResult]:
        """Crawl URLs with BFS link-following.

        After initial crawl, extract internal links from crawled markdown and
        crawl them too, up to max_depth levels deep and max_extra_pages total.

        Args:
            url_query_pairs: Initial (url, query) pairs from search.
            max_depth: How many levels deep to follow links (default: BFS_MAX_DEPTH).
            max_extra_pages: Max additional pages from link-following (default: BFS_MAX_PAGES).

        Returns:
            All PageResults from initial + BFS crawls combined.
        """
        if max_depth is None:
            max_depth = BFS_MAX_DEPTH
        if max_extra_pages is None:
            max_extra_pages = BFS_MAX_PAGES

        # Initial crawl
        all_results = await self.crawl_urls(url_query_pairs)

        if max_depth <= 0 or max_extra_pages <= 0:
            return all_results

        # Track all crawled URLs to avoid re-crawling
        crawled_urls: set[str] = {r.url for r in all_results}
        # Track which domains we started on (only follow same-domain links)
        seed_domains: set[str] = set()
        for url, _ in url_query_pairs:
            seed_domains.add(urlparse(url).netloc.lower())

        extra_crawled = 0

        for depth in range(max_depth):
            # Extract links from successful pages at this depth
            links_to_crawl: list[tuple[str, str]] = []

            for result in all_results:
                if not result.success or not result.raw_markdown:
                    continue
                discovered = self._extract_internal_links(
                    result.raw_markdown, result.url, seed_domains, crawled_urls,
                )
                for link_url in discovered:
                    if extra_crawled + len(links_to_crawl) >= max_extra_pages:
                        break
                    links_to_crawl.append((link_url, f"bfs_depth_{depth + 1}"))
                    crawled_urls.add(link_url)

            if not links_to_crawl:
                break

            print(f"\n  --- BFS Depth {depth + 1}: {len(links_to_crawl)} internal links ---")
            bfs_results = await self.crawl_urls(links_to_crawl)
            all_results.extend(bfs_results)
            extra_crawled += len(bfs_results)

            if extra_crawled >= max_extra_pages:
                break

        if extra_crawled > 0:
            print(f"\n  BFS: crawled {extra_crawled} extra pages from link-following")
        return all_results

    @staticmethod
    def _extract_internal_links(
        markdown: str,
        source_url: str,
        allowed_domains: set[str],
        already_crawled: set[str],
    ) -> list[str]:
        """Extract same-domain links from markdown that look like listicle pages.

        Only follows links:
        - On the same domain as the source page
        - That contain listicle-related keywords in the link text
        - That haven't been crawled already
        """
        source_domain = urlparse(source_url).netloc.lower()
        found: list[str] = []

        for match in _MD_LINK.finditer(markdown):
            text = match.group(1)
            url = match.group(2)

            # Must be same domain
            link_domain = urlparse(url).netloc.lower()
            if link_domain not in allowed_domains and link_domain != source_domain:
                continue

            # Must look like a listicle page (keyword in link text or URL)
            if not (_LISTICLE_KEYWORDS.search(text) or _LISTICLE_KEYWORDS.search(url)):
                continue

            # Not already crawled
            if url in already_crawled:
                continue

            found.append(url)

        return found

    @staticmethod
    def _save_markdown(url: str, markdown: str) -> str:
        """Save markdown to disk, return relative path."""
        domain = urlparse(url).netloc.replace(".", "_")
        path_slug = urlparse(url).path.replace("/", "_")[:50]
        filename = f"{domain}{path_slug}.md"
        filepath = PAGES_DIR / filename

        with open(filepath, "w") as f:
            f.write(markdown)

        return str(filepath.relative_to(PAGES_DIR.parent.parent))
