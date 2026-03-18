"""
SeedClassificationService — public orchestrator.

Classifies text by trying each classifier in priority order.
"""

from __future__ import annotations

from services.Classification.models import ClassificationResult, SeedClassifier


class SeedClassificationService:
    """Priority-ordered classification: first match wins."""

    def __init__(self, classifiers: list[SeedClassifier]) -> None:
        self._classifiers = classifiers

    # API:

    def classify(self, text: str) -> ClassificationResult | None:
        """Classify text using the first classifier that returns a result."""
        for classifier in self._classifiers:
            result = classifier.classify(text)
            if result is not None:
                return result
        return None
