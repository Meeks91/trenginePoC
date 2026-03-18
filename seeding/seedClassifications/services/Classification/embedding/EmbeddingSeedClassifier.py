

from __future__ import annotations

import json
import math
from pathlib import Path

from services.Classification.embedding.models import Centroid, Embedder
from services.Classification.models import (
    ClassificationMethod,
    ClassificationResult,
)


DEFAULT_THRESHOLD = 0.70


class EmbeddingSeedClassifier:
    """Cosine similarity classifier against positive/negative centroids."""

    def __init__(
        self,
        centroids: list[Centroid],
        embedder: Embedder,
        threshold: float,
    ) -> None:
        self._centroids = centroids
        self._embedder = embedder
        self._threshold = threshold

    # ── API ──

    def classify(self, text: str) -> ClassificationResult | None:
        """Classify text by embedding similarity to centroids."""
        vec = self._embedder.embed(text)

        best_gap = -2.0
        best_pos_sim = 0.0
        best_centroid: Centroid | None = None

        for centroid in self._centroids:
            pos_sim = _cosine_similarity(vec, centroid.positive_embedding)
            neg_sim = _cosine_similarity(vec, centroid.negative_embedding)
            gap = pos_sim - neg_sim

            if gap > best_gap:
                best_gap = gap
                best_pos_sim = pos_sim
                best_centroid = centroid

        if best_centroid is None or best_pos_sim < self._threshold:
            return None

        return ClassificationResult(
            category=best_centroid.category,
            sub=best_centroid.sub,
            confidence=best_pos_sim,
            method=ClassificationMethod.EMBEDDING,
        )

    # ── Factory ──

    @classmethod
    def from_centroids_json(
        cls,
        path: Path,
        embedder: Embedder,
        threshold: float,
    ) -> "EmbeddingSeedClassifier":
        """Load centroids.json, embed all slugs, compute mean vectors."""
        with open(path, encoding="utf-8") as f:
            raw: list[dict] = json.load(f)

        centroids: list[Centroid] = []
        for entry in raw:
            pos_vecs = embedder.embed_batch(entry["positive"])
            neg_vecs = embedder.embed_batch(entry["negative"])

            centroids.append(Centroid(
                sub=entry["sub"],
                category=entry["category"],
                positive_embedding=_mean_vector(pos_vecs),
                negative_embedding=_mean_vector(neg_vecs),
            ))

        return cls(
            centroids=centroids,
            embedder=embedder,
            threshold=threshold,
        )


# ── Internal ──


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


def _mean_vector(vectors: list[list[float]]) -> list[float]:
    """Compute element-wise mean of a list of vectors."""
    dim = len(vectors[0])
    count = len(vectors)
    return [sum(v[i] for v in vectors) / count for i in range(dim)]
