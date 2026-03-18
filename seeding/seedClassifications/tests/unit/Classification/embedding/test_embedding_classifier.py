"""Tests for EmbeddingSeedClassifier."""

from __future__ import annotations

import math

import pytest

from services.Classification.embedding.EmbeddingSeedClassifier import (
    EmbeddingSeedClassifier,
    _cosine_similarity,
    _mean_vector,
)
from services.Classification.embedding.models import Centroid
from services.Classification.models import (
    ClassificationMethod,
    ClassificationResult,
)


# ── Mock Embedder ──


class FakeEmbedder:
    """Returns pre-configured vectors for known texts."""

    def __init__(self, mapping: dict[str, list[float]]) -> None:
        self._mapping = mapping

    def embed(self, text: str) -> list[float]:
        return self._mapping[text]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._mapping[t] for t in texts]


# ── Test Vectors ──

# Simple 3D vectors for deterministic testing.
CALISTHENICS_POS = [1.0, 0.0, 0.0]
CALISTHENICS_NEG = [0.0, 1.0, 0.0]
POWERLIFTING_POS = [0.0, 1.0, 0.0]
POWERLIFTING_NEG = [1.0, 0.0, 0.0]

CENTROIDS = [
    Centroid(
        sub="Calisthenics",
        category="FITNESS",
        positive_embedding=CALISTHENICS_POS,
        negative_embedding=CALISTHENICS_NEG,
    ),
    Centroid(
        sub="Powerlifting / Strength",
        category="FITNESS",
        positive_embedding=POWERLIFTING_POS,
        negative_embedding=POWERLIFTING_NEG,
    ),
]


# ── Tests: cosine_similarity ──


class TestCosineSimilarity:
    def test_identical_vectors(self) -> None:
        assert _cosine_similarity([1, 0, 0], [1, 0, 0]) == pytest.approx(1.0)

    def test_orthogonal_vectors(self) -> None:
        assert _cosine_similarity([1, 0, 0], [0, 1, 0]) == pytest.approx(0.0)

    def test_opposite_vectors(self) -> None:
        assert _cosine_similarity([1, 0], [-1, 0]) == pytest.approx(-1.0)

    def test_zero_vector_returns_zero(self) -> None:
        assert _cosine_similarity([0, 0], [1, 0]) == pytest.approx(0.0)

    def test_arbitrary_vectors(self) -> None:
        a = [1.0, 2.0, 3.0]
        b = [4.0, 5.0, 6.0]
        dot = 1 * 4 + 2 * 5 + 3 * 6  # 32
        norm_a = math.sqrt(14)
        norm_b = math.sqrt(77)
        expected = dot / (norm_a * norm_b)
        assert _cosine_similarity(a, b) == pytest.approx(expected)


# ── Tests: mean_vector ──


class TestMeanVector:
    def test_single_vector(self) -> None:
        assert _mean_vector([[1.0, 2.0, 3.0]]) == [1.0, 2.0, 3.0]

    def test_two_vectors(self) -> None:
        result = _mean_vector([[1.0, 0.0], [0.0, 1.0]])
        assert result == pytest.approx([0.5, 0.5])

    def test_three_vectors(self) -> None:
        result = _mean_vector([[3.0, 6.0], [0.0, 0.0], [0.0, 3.0]])
        assert result == pytest.approx([1.0, 3.0])


# ── Tests: classify ──


class TestClassify:
    def test_selects_best_centroid_by_gap(self) -> None:
        """Text vector [1,0,0] → Calisthenics (gap=1) over Powerlifting (gap=-1)."""
        embedder = FakeEmbedder({"calisthenics text": [1.0, 0.0, 0.0]})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=0.5,
        )
        result = clf.classify("calisthenics text")

        assert result == ClassificationResult(
            category="FITNESS",
            sub="Calisthenics",
            confidence=pytest.approx(1.0),
            method=ClassificationMethod.EMBEDDING,
        )

    def test_selects_powerlifting_for_matching_vector(self) -> None:
        """Text vector [0,1,0] → Powerlifting (gap=1) over Calisthenics (gap=-1)."""
        embedder = FakeEmbedder({"powerlifting text": [0.0, 1.0, 0.0]})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=0.5,
        )
        result = clf.classify("powerlifting text")

        assert result == ClassificationResult(
            category="FITNESS",
            sub="Powerlifting / Strength",
            confidence=pytest.approx(1.0),
            method=ClassificationMethod.EMBEDDING,
        )

    def test_below_threshold_returns_none(self) -> None:
        """Text at [0,0,1] has 0 cosine to both positives — below threshold."""
        embedder = FakeEmbedder({"unrelated text": [0.0, 0.0, 1.0]})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=0.5,
        )
        result = clf.classify("unrelated text")

        assert result is None

    def test_confidence_equals_positive_cosine(self) -> None:
        vec = [0.8, 0.2, 0.0]
        embedder = FakeEmbedder({"mixed text": vec})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=0.0,
        )
        result = clf.classify("mixed text")

        expected_cos = _cosine_similarity(vec, CALISTHENICS_POS)
        assert result is not None
        assert result.confidence == pytest.approx(expected_cos)

    def test_method_is_embedding(self) -> None:
        embedder = FakeEmbedder({"test": [1.0, 0.0, 0.0]})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=0.5,
        )
        result = clf.classify("test")

        assert result is not None
        assert result.method == ClassificationMethod.EMBEDDING

    def test_empty_centroids_returns_none(self) -> None:
        embedder = FakeEmbedder({"test": [1.0, 0.0, 0.0]})
        clf = EmbeddingSeedClassifier(
            centroids=[],
            embedder=embedder,
            threshold=0.5,
        )
        result = clf.classify("test")

        assert result is None

    def test_threshold_boundary_at_exactly_threshold(self) -> None:
        """At exactly the threshold, should still classify (>= not >)."""
        embedder = FakeEmbedder({"test": [1.0, 0.0, 0.0]})
        clf = EmbeddingSeedClassifier(
            centroids=CENTROIDS,
            embedder=embedder,
            threshold=1.0,
        )
        result = clf.classify("test")

        assert result is not None
        assert result.sub == "Calisthenics"
