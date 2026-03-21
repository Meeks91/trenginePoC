"""
LLMResponseParser
================
Parses raw LLM JSON output into Influencer[] with error handling.
Validates handles using the same rules as regex extraction.
"""

from __future__ import annotations

import json
import re
from typing import Any

from config.schema import Influencer, Platform
from services.extraction.RegexHandleExtractorService import _is_valid_handle
from services.extraction.NameCleanerService import NameCleaner


class LLMResponseParser:
    """Parse LLM extraction responses into structured Influencer lists."""

    # Map LLM output strings to Platform enum values
    _PLATFORM_MAP: dict[str, Platform] = {
        "instagram": Platform.Instagram,
        "tiktok": Platform.TikTok,
        "youtube": Platform.YouTube,
    }

    @staticmethod
    def parse(raw_json: str, source_url: str = "") -> list[Influencer]:
        """
        Parse LLM output JSON into a list of Influencer objects.

        Handles multiple response shapes:
          - {"influencers": [...]}
          - [{"influencers": [...]}, ...]
          - [{"name": "...", "handle": "..."}, ...]

        Validates handles using _is_valid_handle() to filter out
        path segments, CSS at-rules, and other garbage from LLM output.

        Returns:
            list of Influencer objects, empty on parse failure.
        """
        # Strip markdown fences: ```json\n{...}\n``` → {....}
        cleaned = raw_json.strip()
        if cleaned.startswith("```"):
            # Remove opening fence (```json or ```)
            cleaned = re.sub(r'^```\w*\n?', '', cleaned)
            # Remove closing fence
            cleaned = re.sub(r'\n?```\s*$', '', cleaned)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return []

        raw_items = LLMResponseParser._extract_items(parsed)

        influencers = []
        for item in raw_items:
            if not isinstance(item, dict):
                continue
            raw_name = str(item.get("name", "")).strip()
            name = NameCleaner.clean_name(raw_name)
            if not name:
                continue
            handle = str(item.get("handle", "")).strip().lstrip("@")
            handle_platform = str(item.get("handle_platform", "")).strip().lower()
            if handle and not (_is_valid_handle(handle) and NameCleaner.is_valid_handle(handle)):
                handle = ""

            # Build handles dict from LLM output
            handles: dict[Platform, str] = {}
            if handle:
                platform = LLMResponseParser._PLATFORM_MAP.get(handle_platform, Platform.Instagram)
                handles[platform] = handle

            influencers.append(Influencer(name=name, handles=handles))

        return influencers

    @staticmethod
    def _extract_items(parsed: Any) -> list[dict[str, Any]]:
        """Extract influencer dicts from various LLM response shapes."""
        # Shape: {"influencers": [...]}
        if isinstance(parsed, dict):
            if "influencers" in parsed:
                return list(parsed["influencers"])
            # Single influencer dict
            if "name" in parsed:
                return [parsed]
            return []

        # Shape: [{...}, {...}, ...] — could be list of influencers or list of responses
        if isinstance(parsed, list):
            all_items = []
            for item in parsed:
                if isinstance(item, dict):
                    if "influencers" in item:
                        # Chunked response: [{"influencers": [...]}, ...]
                        all_items.extend(item["influencers"])
                    elif "name" in item:
                        # Direct list of influencers
                        all_items.append(item)
            return all_items

        return []
