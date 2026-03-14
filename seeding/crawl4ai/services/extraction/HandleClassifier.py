"""
HandleClassifier — Classify naked @handles by platform via LLM.

When regex extraction finds @handles with no platform URL context (naked
mentions like "@fitguru" in plain text), this service batches them into
a single cheap LLM call to determine which platform each belongs to.

Cost: ~$0.001 per batch (one LLM call for all handles in a job).
"""

from __future__ import annotations

import json
import logging
import litellm

from config import GEMINI_API_KEY, LLM_PROVIDER
from services.extraction.RegexHandleExtractor import ExtractedHandle

logger = logging.getLogger(__name__)


CLASSIFY_PROMPT = """You are classifying social media handles by platform.

For each handle below, determine which platform it most likely belongs to.
Choose ONLY from: Instagram, TikTok, YouTube, or "unknown" if you can't tell.

Context clues:
  - Instagram handles are typically personal names, brands, or lifestyle accounts
  - TikTok handles often have underscores and creative names
  - YouTube handles tend to include "vlog", "tv", channel-style names
  - If the handle could belong to multiple platforms, choose the most likely one

Handles to classify:
{handles_list}

Respond with ONLY a JSON array like:
[{{"handle": "fitguru", "platform": "Instagram"}}, ...]

Do NOT include handles you are unsure about — set platform to "unknown" for those.
"""


async def classify_handles(handles: list[ExtractedHandle]) -> list[ExtractedHandle]:
    """Classify unknown-platform handles via a single LLM call.

    Args:
        handles: ExtractedHandle objects with platform="" (unknown).

    Returns:
        The same handles with platform updated where the LLM was confident.
    """
    if not handles:
        return handles

    if not GEMINI_API_KEY:
        logger.warning("  SKIP: No API key for handle classification")
        return handles

    # Build handle list for prompt
    handle_names = [h.handle for h in handles]
    handles_text = "\n".join(f"  - @{h}" for h in handle_names)

    prompt = CLASSIFY_PROMPT.format(handles_list=handles_text)

    try:
        response = await litellm.acompletion(
            model=LLM_PROVIDER,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=500,
        )

        raw = response.choices[0].message.content.strip()

        # Extract JSON from response
        # Handle markdown code blocks
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        classifications = json.loads(raw)

        # Build lookup
        platform_map = {}
        for item in classifications:
            h = item.get("handle", "").lower()
            p = item.get("platform", "unknown")
            if p in ("Instagram", "TikTok", "YouTube"):
                platform_map[h] = p

        # Update handles
        classified = 0
        for handle in handles:
            new_platform = platform_map.get(handle.handle.lower())
            if new_platform:
                handle.platform = new_platform
                classified += 1

        logger.info("  LLM classified %d/%d naked handles", classified, len(handles))
        return handles

    except Exception:
        logger.exception("Handle classification failed")
        return handles  # Return unmodified on failure
