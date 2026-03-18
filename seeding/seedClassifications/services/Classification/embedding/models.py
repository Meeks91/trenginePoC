"""Data models for the embedding classifier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Embedder(Protocol):
    """Protocol for embedding text to vector."""
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...


@dataclass(frozen=True)
class Centroid:
    """Pre-computed mean embedding for one subcategory."""
    sub: str
    category: str
    positive_embedding: list[float]
    negative_embedding: list[float]
