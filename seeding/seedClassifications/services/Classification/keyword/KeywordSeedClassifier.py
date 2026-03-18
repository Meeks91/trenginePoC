"""
KeywordSeedClassifier — deterministic reverse-lookup classification.

Loads locale-keyed keyword sets from JSON config.
Each keyword maps to exactly one (category, sub) pair — no overlap allowed.
Keywords and input text are normalized (lowercase, hyphens/underscores → spaces,
hashtags stripped) so that "AI-tools", "ai tools", and "#aitools" all match.
"""

from __future__ import annotations

import json
from pathlib import Path

from services.Classification.models import (
    ClassificationMethod,
    ClassificationResult,
    Language,
)


def _normalize(text: str) -> str:
    """Lowercase, replace hyphens/underscores with spaces, strip hashtags."""
    return text.lower().replace("-", " ").replace("_", " ").replace("#", "")


class KeywordSeedClassifier:
    """Reverse-lookup: keyword → (category, sub). No overlap allowed."""

    def __init__(self, keyword_map: dict[str, tuple[str, str]]) -> None:
        self._map = keyword_map

    # ── API ──

    def classify(self, text: str) -> ClassificationResult | None:
        """Return classification if any keyword is found in text."""
        normalized = _normalize(text)
        for keyword, (category, sub) in self._map.items():
            if keyword in normalized:
                return ClassificationResult(
                    category=category,
                    sub=sub,
                    confidence=1.0,
                    method=ClassificationMethod.KEYWORD,
                )
        return None

    # ── Factory ──

    @classmethod
    def from_locale(
        cls,
        config_dir: Path,
        language: Language,
    ) -> "KeywordSeedClassifier":
        """Load keyword sets from config/keywords/{locale}.json.

        Normalizes all keywords at load time.
        Raises ValueError on duplicate keywords after normalization.
        """
        path = config_dir / "keywords" / f"{language.value}.json"
        with open(path, encoding="utf-8") as f:
            raw: dict[str, dict[str, list[str]]] = json.load(f)

        keyword_map: dict[str, tuple[str, str]] = {}
        for category, subs in raw.items():
            for sub_name, keywords in subs.items():
                for keyword in keywords:
                    normalized = _normalize(keyword)
                    existing = keyword_map.get(normalized)
                    if existing is not None:
                        raise ValueError(
                            f"Keyword overlap: {keyword!r} normalizes to "
                            f"{normalized!r}, which already maps to "
                            f"{existing} (new: ({category!r}, {sub_name!r}))"
                        )
                    keyword_map[normalized] = (category, sub_name)

        return cls(keyword_map)
