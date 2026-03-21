"""
LLMExtractionService — LLM extraction via litellm (Gemini 2.0 Flash).
Supports real-time and sampling modes.

Uses the fit_markdown from CrawlService directly — no re-crawl.
"""

from __future__ import annotations

import asyncio
import logging
import os
import random

import litellm

from services.audit.AuditService import AuditLog
from config import GEMINI_API_KEY, LLM_PROVIDER, RAW_DIR, LLM_DELAY_SECONDS, OUTPUT_TOKENS_PER_INFLUENCER
from config.schema import PageResult, Influencer
from services.extraction.LLMResponseParser import LLMResponseParser

logger = logging.getLogger(__name__)

# Pydantic schema for structured LLM output binding.
from config.seed_schema import SeedResults


# ── Extraction Prompt ────────────────────────────────────────────────
# Single source of truth for the LLM system prompt.
# Techniques applied:
#   1. Role assignment — expert extraction specialist
#   2. Few-shot example — concrete input→output pair
#   3. Chain-of-thought — scan section by section
#   4. Exhaustiveness emphasis — never skip a name
#   5. Schema descriptions handle field-level hints (see seed_schema.py)

EXTRACTION_PROMPT = """You are an expert data-extraction specialist. Your task \
is to extract EVERY influencer / content creator mentioned on a webpage about \
{sub_name} ({platform}) creators.

Context:
  Platform: {platform}
  Category: {category_key} > {sub_name}
  Region: {region}
  Year: {year}

Process:
  1. Scan the page section by section, heading by heading.
  2. For EACH person mentioned, record their display name exactly as written.
  3. Only extract a handle if it is for {platform}. Ignore handles for other \
platforms entirely — treat them as if no handle exists.
  4. Extract the bare username only — never display text, link labels, or \
descriptions. Leave handle_platform as empty string.
  5. If no {platform} handle is visible, set handle to empty string — but \
STILL include the person.

Critical rules:
  - Extract EVERY person. It is far better to include someone with an empty \
handle than to skip them entirely.
  - A page listing 10 people should produce 10 results, not 3.
  - Never invent or guess handles. Only extract what is explicitly on the page.
  - Only take handles that are for {platform}. Discard handles for other platforms.
  - Do NOT extract brand names, company names, app names, or product names.
  - Do NOT extract country names, news organisations, or generic phrases.
  - Return the COMPLETE list — do not truncate or summarise.

Example (target platform = {platform}):

  INPUT (markdown):
  ## Top Fitness Creators to Watch in 2026
  **Joe Wicks** has transformed home workouts with his Body Coach brand.
  Rising star **Courtney Black** (@courtneyblack on {platform}) focuses on HIIT.
  **Emma Storey-Gordon** (@esg_fitness on TikTok) brings an evidence-based approach.
  Also featured: Peloton, Nike Training Club, and MyFitnessPal.

  OUTPUT:
  - name: "Joe Wicks", handle: "", handle_platform: ""
  - name: "Courtney Black", handle: "courtneyblack", handle_platform: ""
  - name: "Emma Storey-Gordon", handle: "", handle_platform: ""
    (her TikTok handle is ignored — not {platform})

  NOT extracted: Peloton, Nike Training Club, MyFitnessPal (brands, not people)
"""


class LLMExtractionService:
    """Extract influencers from crawled pages using LLM.

    Takes the fit_markdown produced by CrawlService and sends
    it directly to the LLM with the extraction prompt. No re-crawling.
    """

    def __init__(self, audit: AuditLog):
        self._audit = audit
        os.makedirs(RAW_DIR, exist_ok=True)

    async def extract(
        self,
        pages: list[PageResult],
        platform: str,
        category_key: str,
        sub_name: str,
        region: str,
        year: str,
        sample_n: int | None = None,
    ) -> tuple[dict[str, list[Influencer]], int, int]:
        """Extract influencers from crawled pages.

        Args:
            pages: Crawled page results from CrawlService.
            platform, category_key, sub_name, region, year: Job context.
            sample_n: If set, only extract from N random pages.

        Returns:
            Tuple of (url_to_influencers, total_input_tokens, total_output_tokens).
        """
        eligible = [p for p in pages if p.success and p.fit_markdown.strip()]

        if sample_n is not None and sample_n < len(eligible):
            logger.info(f"\n  Sampling {sample_n}/{len(eligible)} pages for LLM extraction")
            eligible = random.sample(eligible, sample_n)

        if not eligible:
            logger.warning("No pages eligible for extraction")
            return {}, 0, 0

        logger.info(f"\n  --- LLM Extraction ({len(eligible)} pages) ---")

        prompt = EXTRACTION_PROMPT.format(
            platform=platform,
            category_key=category_key,
            sub_name=sub_name,
            region=region,
            year=year,
        )


        url_to_influencers: dict[str, list[Influencer]] = {}
        total_input_tokens = 0
        total_output_tokens = 0

        for i, page in enumerate(eligible, 1):
            logger.info(f"\n    [{i}/{len(eligible)}] {page.url}")

            try:
                influencers, in_tok, out_tok = await self._extract_page(page, prompt)
                url_to_influencers[page.url] = influencers
                total_input_tokens += in_tok
                total_output_tokens += out_tok

                self._audit.log_llm_call(
                    url=page.url,
                    input_tokens=in_tok,
                    output_tokens=out_tok,
                    influencers_found=len(influencers),
                )

                count = len(influencers)
                logger.info("      %d influencers extracted (%s in / %s out tokens)",
                            count, f"{in_tok:,}", f"{out_tok:,}")
                for inf in influencers[:5]:
                    handle_str = ", ".join(
                        f"{p.value}: {h}" for p, h in inf.handles.items()
                    ) if inf.handles else "no handle"
                    logger.info("        %s (%s)", inf.name, handle_str)
                if count > 5:
                    logger.info("        ... and %d more", count - 5)

            except Exception:
                logger.exception("LLM extraction failed for %s", page.url)
                url_to_influencers[page.url] = []

            if LLM_DELAY_SECONDS and i < len(eligible):
                await asyncio.sleep(LLM_DELAY_SECONDS)

        total = sum(len(v) for v in url_to_influencers.values())
        logger.info("  Extracted %d influencers from %d pages", total, len(url_to_influencers))
        logger.info("  Tokens: %s input, %s output", f"{total_input_tokens:,}", f"{total_output_tokens:,}")
        return url_to_influencers, total_input_tokens, total_output_tokens

    async def _extract_page(
        self,
        page: PageResult,
        prompt: str,
    ) -> tuple[list[Influencer], int, int]:
        """Send fit_markdown + prompt to LLM, parse response into Influencers.

        Returns:
            Tuple of (influencers, input_tokens, output_tokens).
        """

        # Truncate page to relevant listicle section (saves 50-70% tokens)
        from services.extraction.PageTruncator import truncate_for_llm
        page_content = truncate_for_llm(page.fit_markdown)

        # Build the message: system prompt has all instructions,
        # user message is just the page content with a clear delimiter.
        messages = [
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": (
                    f"---PAGE CONTENT---\n"
                    f"{page_content}"
                ),
            },
        ]

        # Call the LLM via litellm — Pydantic schema constrains output format.
        response = await litellm.acompletion(
            model=LLM_PROVIDER,
            messages=messages,
            api_key=GEMINI_API_KEY,
            response_format=SeedResults,
            temperature=0.1,
            thinking={"type": "disabled"},
        )

        # Extract actual token usage from API response (fallback to estimates)
        usage = getattr(response, 'usage', None)
        input_tokens = getattr(usage, 'prompt_tokens', None) or page.fit_token_estimate
        output_tokens = getattr(usage, 'completion_tokens', None)

        raw_content = response.choices[0].message.content
        if not raw_content:
            logger.warning("LLM returned empty response")
            return [], input_tokens, output_tokens or 0

        # Save raw response
        self._save_raw(page.url, raw_content)

        # Parse into Influencer objects
        influencers = LLMResponseParser.parse(raw_content, source_url=page.url)

        # Fallback output token estimate if API didn't provide usage
        if output_tokens is None:
            output_tokens = len(influencers) * OUTPUT_TOKENS_PER_INFLUENCER

        return influencers, input_tokens, output_tokens

    @staticmethod
    def _save_raw(url: str, content: str) -> None:
        """Save raw LLM JSON response to disk."""
        from urllib.parse import urlparse
        domain = urlparse(url).netloc.replace(".", "_")
        path_slug = urlparse(url).path.replace("/", "_")[:50]
        filename = f"{domain}{path_slug}.json"
        with open(RAW_DIR / filename, "w") as f:
            f.write(content)
