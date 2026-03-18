"""
SeedClassificationService — public orchestrator.

Classifies text by trying keyword match first, then embedding fallback.
"""

from __future__ import annotations

from services.Classification.embedding.EmbeddingSeedClassifier import (
    EmbeddingSeedClassifier,
)
from services.Classification.keyword.KeywordSeedClassifier import (
    KeywordSeedClassifier,
)
from services.Classification.models import ClassificationResult


class SeedClassificationService:
    """Keyword-first → embedding fallback classification."""

    def __init__(
        self,
        keyword: KeywordSeedClassifier,
        embedding: EmbeddingSeedClassifier,
    ) -> None:
        self._keyword = keyword
        self._embedding = embedding

    # ── API ──

    def classify(self, text: str) -> ClassificationResult | None:
        """Classify text: keyword match (instant) or embedding fallback."""
        return self._keyword.classify(text) or self._embedding.classify(text)
