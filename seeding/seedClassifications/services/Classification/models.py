"""
Data models and enums for the Seed Classification Service.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class Language(str, Enum):
    """Locale for keyword config selection."""
    EN = "en"


class ClassificationMethod(str, Enum):
    """How the classification was determined."""
    KEYWORD = "keyword"
    EMBEDDING = "embedding"


@dataclass(frozen=True)
class ClassificationResult:
    """Output of a classification attempt."""
    category: str
    sub: str
    confidence: float
    method: ClassificationMethod


class SeedClassifier(Protocol):
    """Abstraction for any classification strategy."""
    def classify(self, text: str) -> ClassificationResult | None: ...

