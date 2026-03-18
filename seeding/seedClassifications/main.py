"""
Seed Classification PoC — entry point.

Wires dependencies and runs classification against sample texts.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from services.Classification.embedding.EmbeddingSeedClassifier import (
    EmbeddingSeedClassifier,
)
from services.Classification.embedding.GeminiEmbedder import GeminiEmbedder
from services.Classification.keyword.KeywordSeedClassifier import (
    KeywordSeedClassifier,
)
from services.Classification.models import Language
from services.Classification.SeedClassificationService import (
    SeedClassificationService,
)


CONFIG_DIR = Path(__file__).parent / "config"


def build_service(language: Language) -> SeedClassificationService:
    """Wire all dependencies and return the classification service."""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    keyword = KeywordSeedClassifier.from_locale(CONFIG_DIR, language)
    embedder = GeminiEmbedder(api_key)
    embedding = EmbeddingSeedClassifier.from_centroids_json(
        CONFIG_DIR / "centroids.json",
        embedder,
    )

    return SeedClassificationService(keyword=keyword, embedding=embedding)


SAMPLE_TEXTS = [
    "calisthenics muscle up tutorial for beginners",
    "powerlifting meet prep 600lb deadlift",
    "yoga flow for tight hips and lower back",
    "random tech review of the new iPhone",
    "evidence-based training volume for hypertrophy",
    "women who lift breaking stereotypes in the gym",
    "sharing my fitness journey and daily workouts",
]


def main() -> None:
    """Run classification on sample texts."""
    language = Language.EN
    service = build_service(language)

    print(f"\n{'='*60}")
    print(f"  Seed Classification PoC — language={language.value}")
    print(f"{'='*60}\n")

    for text in SAMPLE_TEXTS:
        result = service.classify(text)
        if result is None:
            print(f"  ❌ UNCLASSIFIED: {text!r}")
        else:
            label = f"[{result.method.value.upper()}]"
            print(
                f"  ✅ {label:11s} {result.category}/{result.sub} "
                f"({result.confidence:.2f}): {text!r}"
            )

    print()


if __name__ == "__main__":
    main()
