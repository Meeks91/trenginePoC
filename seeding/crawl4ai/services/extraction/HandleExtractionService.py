"""
HandleExtractionService — Orchestrates all handle extraction steps.

Delegates to:
  - RegexHandleExtractor (deterministic regex)
  - HandleClassifier (naked @handle classification via LLM)
  - YouTubeChannelResolver (channel ID → @handle)
  - LLMExtractionService (LLM extraction — conditional)
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.extraction.NameMentionTracker import NameMentionTracker, NameMention

from config.schema import Influencer, PageResult, Platform
from services.audit.AuditService import AuditLog
from services.extraction.NameCleaner import NameCleaner
from services.extraction.RegexHandleExtractor import (
    extract_handles_from_html,
    extract_youtube_channel_ids,
    assign_names_from_headings,
    ExtractedHandle,
)

logger = logging.getLogger(__name__)

# Map platform strings from ExtractedHandle to Platform enum
_PLATFORM_MAP: dict[str, Platform] = {
    "Instagram": Platform.Instagram,
    "TikTok": Platform.TikTok,
    "YouTube": Platform.YouTube,
}

def _to_handles(handle: str, platform_str: str) -> dict[Platform, str]:
    """Convert a handle + platform string into a handles dict."""
    if not handle:
        return {}
    plat = _PLATFORM_MAP.get(platform_str)
    if plat:
        return {plat: handle}
    return {}  # Unknown/naked — classified later


# ══════════════════════════════════════════════════════════════════════
# Result dataclass
# ══════════════════════════════════════════════════════════════════════

@dataclass
class HandleExtractionResult:
    """Combined output from all extraction sub-phases."""
    regex_handles: list[Influencer] = field(default_factory=list)
    llm_handles: dict[str, list[Influencer]] = field(default_factory=dict)
    all_merged: list[Influencer] = field(default_factory=list)
    llm_input_tokens: int = 0
    llm_output_tokens: int = 0
    llm_pages_used: int = 0
    llm_pages_skipped: int = 0
    name_candidates_found: int = 0
    name_resolved_handles: int = 0
    name_mentions: list[NameMention] = field(default_factory=list)
    name_tracker: NameMentionTracker | None = None


# ══════════════════════════════════════════════════════════════════════
# LLM gating logic
# ══════════════════════════════════════════════════════════════════════

_LISTICLE_KW = re.compile(
    r'(?:influencer|creator|blogger|vlogger|youtuber|instagrammer|'
    r'top.?\d+|best.?\d+|list|roundup|follow)',
    re.IGNORECASE,
)

# Platform classification is in its own module
from services.extraction.PlatformClassifier import (
    classify_by_context as _classify_by_context,
)


def needs_llm(
    page: PageResult,
    page_url_handle_counts: dict[str, int],
    page_naked_handle_counts: dict[str, int],
) -> bool:
    """Determine if a page needs LLM extraction (LLMExtractionService).

    Rules:
      1. Naked @handles do NOT trigger this — they are classified
         mechanically via classify_by_context(), with HandleClassifier
         LLM fallback only when 2+ platforms are ambiguous AND all
         handles remain untagged.
      2. Listicle page (keyword in URL) with zero regex handles — LLM
         extracts handles that regex couldn't reach (JS-rendered, etc.).
    """
    if not page.success or not page.fit_markdown.strip():
        return False
    url_handles = page_url_handle_counts.get(page.url, 0)
    naked_count = page_naked_handle_counts.get(page.url, 0)
    total_handles = url_handles + naked_count
    # Only fire for zero-handle listicle pages
    if total_handles == 0 and _LISTICLE_KW.search(page.url):
        return True
    return False


# ══════════════════════════════════════════════════════════════════════
# Service class
# ══════════════════════════════════════════════════════════════════════

class HandleExtractionService:
    """Orchestrates handle extraction: Regex → Classify → YouTube → LLM gating.

    Composes existing leaf services; the pipeline runner calls this
    instead of doing all extraction steps inline.
    """

    def __init__(self, audit: AuditLog):
        self._audit = audit

    async def extract_all_handles(
        self,
        pages: list[PageResult],
        *,
        platform: str,
        category_key: str,
        sub_name: str,
        region: str,
        year: str,
        direct_handles: list[ExtractedHandle],
        sample_n: int | None = None,
    ) -> HandleExtractionResult:
        """Run all extraction phases and return merged handles.

        Args:
            pages: Crawled pages from CrawlService.
            platform: Target platform (e.g. "Instagram").
            category_key: Category identifier for LLM context.
            sub_name: Sub-category name for LLM context.
            region: Region label for LLM context.
            year: Current year for LLM context.
            direct_handles: Handles extracted from DDG URLs.
            sample_n: If set, sample N pages for LLM extraction.

        Returns:
            HandleExtractionResult with all handles merged.
        """
        result = HandleExtractionResult()

        # ── Regex Handle Extraction ──
        regex_handles, naked_handles, yt_channel_ids, \
            page_url_handle_counts, page_naked_handle_counts = \
            self._regex_extract(pages)
        result.regex_handles = regex_handles

        logger.info("  Regex found %d handles (%d naked @mentions)",
                    len(regex_handles), len(naked_handles))
        if yt_channel_ids:
            logger.info("  Found %d YouTube channel IDs to resolve", len(yt_channel_ids))

        # ── Classify naked @handles (mechanical → LLM fallback) ──
        if naked_handles:
            self._classify_naked_handles(naked_handles, regex_handles, pages)

        # ── YouTube Channel ID Resolution ──
        if yt_channel_ids:
            yt_resolved = await self._resolve_youtube_channels(yt_channel_ids)
            for _cid, handle in yt_resolved.items():
                regex_handles.append(Influencer(
                    name=handle,
                    handles={Platform.YouTube: handle},
                ))

        # ── Name Mention Tracking (all pages, no gate) ──
        from services.extraction.NameExtractor import (
            extract_candidate_names_with_counts, is_reddit_page,
        )
        from services.extraction.NameMentionTracker import NameMentionTracker
        from config.schema import SourceType

        tracker = NameMentionTracker()
        for page in [p for p in pages if p.success and p.raw_markdown]:
            counts = extract_candidate_names_with_counts(page.raw_markdown)
            source = SourceType.REDDIT if is_reddit_page(page.url) else SourceType.NON_REDDIT
            tracker.record_names_in_url(
                names_with_counts=counts,
                source_url=page.url,
                source_type=source,
                platform=platform,
                category=category_key,
                sub_name=sub_name or "",
                region=region,
            )

        # Feed regex-extracted names into the tracker
        for inf in regex_handles:
            if inf.name:
                page_url = next(iter(inf.source_urls)) if inf.source_urls else ""
                if page_url:
                    tracker.record_names_in_url(
                        names_with_counts={inf.name: 1},
                        source_url=page_url,
                        source_type=SourceType.REGEX,
                        platform=platform,
                        category=category_key,
                        sub_name=sub_name or "",
                        region=region,
                    )

        result.name_tracker = tracker

        # ── LLM Extraction (conditional) ──
        llm_pages = [p for p in pages if needs_llm(
            p, page_url_handle_counts, page_naked_handle_counts,
        )]
        skipped = sum(1 for p in pages if p.success) - len(llm_pages)
        result.llm_pages_used = len(llm_pages)
        result.llm_pages_skipped = skipped

        logger.info("  --- LLM Extraction ---")
        logger.info("  %d pages need LLM (skipped %d handle-rich pages)", len(llm_pages), skipped)

        from services.extraction.LLMExtractionService import LLMExtractionService
        extract_svc = LLMExtractionService(self._audit)
        url_to_influencers, extract_input_tokens, extract_output_tokens = \
            await extract_svc.extract(
                pages=llm_pages,
                platform=platform,
                category_key=category_key,
                sub_name=sub_name,
                region=region,
                year=year,
                sample_n=sample_n,
            )
        result.llm_handles = url_to_influencers
        result.llm_input_tokens = extract_input_tokens
        result.llm_output_tokens = extract_output_tokens

        # Stamp LLM-extracted influencers with their source URL
        for url, influencers_list in url_to_influencers.items():
            for inf in influencers_list:
                inf.source_urls = {url}
                inf.extraction_methods = {"llm"}

        # Feed LLM-extracted names into the tracker
        for url, influencers_list in url_to_influencers.items():
            for inf in influencers_list:
                if inf.name:
                    tracker.record_names_in_url(
                        names_with_counts={inf.name: 1},
                        source_url=url,
                        source_type=SourceType.LLM,
                        platform=platform,
                        category=category_key,
                        sub_name=sub_name or "",
                        region=region,
                    )

        # ── Merge: DDG direct handles + regex handles + LLM handles ──
        all_raw = self._merge_handles(
            direct_handles=direct_handles,
            regex_handles=regex_handles,
            llm_handles=url_to_influencers,
        )
        result.all_merged = all_raw

        return result

    # ── Internal helpers ──

    @staticmethod
    def _regex_extract(
        pages: list[PageResult],
    ) -> tuple[
        list[Influencer],
        list[ExtractedHandle],
        list[str],
        dict[str, int],
        dict[str, int],
    ]:
        """Regex handle extraction from crawled pages.

        Returns:
            (regex_handles, naked_handles, yt_channel_ids,
             page_url_handle_counts, page_naked_handle_counts)
        """
        logger.info("  --- Regex Handle Extraction ---")
        regex_handles: list[Influencer] = []
        naked_handles: list[ExtractedHandle] = []
        yt_channel_ids: list[str] = []
        page_url_handle_counts: dict[str, int] = {}
        page_naked_handle_counts: dict[str, int] = {}

        for page in pages:
            if not page.success or not page.raw_markdown:
                continue
            handles = extract_handles_from_html(page.raw_markdown)
            # Backfill names from nearby headings before creating Influencers
            assign_names_from_headings(handles, page.raw_markdown)
            url_handle_count = 0
            naked_count = 0
            for h in handles:
                cleaned_name = NameCleaner.clean_name(h.name) if h.name else None
                regex_handles.append(Influencer(
                    name=cleaned_name or h.handle,
                    handles=_to_handles(h.handle, h.platform),
                    source_urls={page.url},
                    extraction_methods={"regex"},
                ))
                if h.platform:
                    url_handle_count += 1
                else:
                    naked_handles.append(h)
                    naked_count += 1
            page_url_handle_counts[page.url] = url_handle_count
            page_naked_handle_counts[page.url] = naked_count
            yt_channel_ids.extend(extract_youtube_channel_ids(page.raw_markdown))

        return (
            regex_handles, naked_handles, yt_channel_ids,
            page_url_handle_counts, page_naked_handle_counts,
        )

    @staticmethod
    def _classify_naked_handles(
        naked_handles: list[ExtractedHandle],
        regex_handles: list[Influencer],
        pages: list[PageResult],
    ) -> None:
        """Classify naked @handles — mechanical first, LLM only as last resort.

        Classification priority:
          1. Local context (100 chars either side) — 1 platform → auto-assign
          2. Full page text — 1 platform → auto-assign
          3. 2+ platforms, 1 within 100 chars → assign the local one
          4. 0 platforms → leave unclassified (don't waste LLM)
          5. 2+ platforms, ambiguous:
             - Page already has URL-tagged handles → discard (brand mentions)
             - Page has zero URL-tagged handles → LLM fallback
        """
        logger.info("  --- Handle Classification ---")

        # Build page text lookup for context search
        page_texts: dict[str, str] = {}
        page_urls: dict[str, str] = {}
        for page in pages:
            if page.success and page.raw_markdown:
                page_texts[page.url] = page.raw_markdown
                page_urls[page.url] = page.url

        # Step 1: Mechanical classification
        still_ambiguous: list[ExtractedHandle] = []
        mechanical_count = 0

        for handle in naked_handles:
            # Find which page this handle came from
            source_text = ""
            source_url = ""
            for url, text in page_texts.items():
                if f"@{handle.handle}" in text or handle.handle in text:
                    source_text = text
                    source_url = url
                    break

            platform = HandleExtractionService.classify_by_context(
                handle, source_text, source_url,
            )

            if platform is None:
                still_ambiguous.append(handle)
            elif platform == "":
                pass  # 0 platforms found — leave unclassified
            else:
                handle.platform = platform
                mechanical_count += 1
                # Update the corresponding Influencer’s handles dict
                plat_enum = _PLATFORM_MAP.get(platform)
                if plat_enum:
                    for inf in regex_handles:
                        if (
                            not inf.handles
                            and inf.name.lower().lstrip("@") == handle.handle.lower()
                        ):
                            inf.handles[plat_enum] = handle.handle
                            break

        logger.info("  Mechanical: classified %d/%d handles", mechanical_count, len(naked_handles))

        # Step 2: HandleClassifier LLM fallback.
        # Fires ONLY when ALL THREE conditions are true:
        #   (a) 2+ platforms on page (implicit: classify_by_context returns
        #       None only when 2+ platforms detected → handle goes to still_ambiguous)
        #   (b) Zero URL-tagged handles on page (no URL-extracted handles with platforms)
        #   (c) Naked handles present (still_ambiguous is non-empty)
        # If page has URL-tagged handles → discard ambiguous naked handles
        # (they're likely brand mentions / sponsors, not worth LLM cost).
        has_tagged_handles = any(inf.handles for inf in regex_handles)

        if still_ambiguous and not has_tagged_handles:
            import asyncio
            from services.extraction.HandleClassifier import classify_handles
            logger.info("  LLM fallback: %d ambiguous handles (no URL-tagged handles on page)",
                        len(still_ambiguous))
            classified = asyncio.get_event_loop().run_until_complete(
                classify_handles(still_ambiguous)
            ) if not asyncio.get_event_loop().is_running() else still_ambiguous

            for ch in classified:
                if ch.platform:
                    plat_enum = _PLATFORM_MAP.get(ch.platform)
                    if plat_enum:
                        for inf in regex_handles:
                            if (
                                not inf.handles
                                and inf.name.lower().lstrip("@") == ch.handle.lower()
                            ):
                                inf.handles[plat_enum] = ch.handle
                                break
        elif still_ambiguous:
            logger.info("  Discarding %d ambiguous handles (page already has URL-tagged handles)",
                        len(still_ambiguous))
        else:
            logger.info("  No ambiguous handles — LLM skipped")

    @staticmethod
    def classify_by_context(
        handle: ExtractedHandle,
        page_text: str,
        page_url: str,
    ) -> str | None:
        """Delegate to PlatformClassifier.classify_by_context."""
        return _classify_by_context(handle, page_text, page_url)

    @staticmethod
    async def _resolve_youtube_channels(
        yt_channel_ids: list[str],
    ) -> dict[str, str]:
        """Resolve YouTube channel IDs to @handles."""
        from services.extraction.YouTubeChannelResolver import resolve_youtube_channels
        logger.info(f"\n  --- YouTube Channel Resolution ---")
        return await resolve_youtube_channels(list(set(yt_channel_ids)))

    @staticmethod
    def _merge_handles(
        *,
        direct_handles: list[ExtractedHandle],
        regex_handles: list[Influencer],
        llm_handles: dict[str, list[Influencer]],
    ) -> list[Influencer]:
        """Merge DDG direct handles + regex handles + LLM handles.

        Deduplicates on (handle.lower(), platform.lower()) — keeps first
        occurrence. Priority order: LLM > DDG direct > Regex.
        """
        seen: set[tuple[str, str]] = set()
        merged: list[Influencer] = []

        def _dedup_key(inf: Influencer) -> tuple[str, str]:
            if inf.handles:
                return next(
                    ((p.value.lower(), h.lower().rstrip("."))
                     for p, h in inf.handles.items()),
                    ("", ""),
                )
            return (inf.name.lower().lstrip("@").rstrip("."), "")

        def _add(inf: Influencer) -> None:
            key = _dedup_key(inf)
            if key not in seen:
                seen.add(key)
                merged.append(inf)
            else:
                # Union source_urls into the existing entry
                for existing in merged:
                    if _dedup_key(existing) == key:
                        existing.source_urls |= inf.source_urls
                        existing.extraction_methods |= inf.extraction_methods
                        break

        # LLM handles first (highest priority)
        for infs in llm_handles.values():
            for inf in infs:
                _add(inf)

        # DDG direct handles
        for dh in direct_handles:
            _add(Influencer(
                name=dh.name or dh.handle,
                handles=_to_handles(dh.handle, dh.platform),
                extraction_methods={"ddg_direct"},
            ))

        # Regex handles
        for inf in regex_handles:
            _add(inf)

        return merged
