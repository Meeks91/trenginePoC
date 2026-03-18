"""Guard tests against the real en.json keyword config.

These tests load the production config and verify:
1. No keyword appears in more than one (category, sub) pair
2. Every keyword is fully lowercase (matches classifier's text.lower())
3. Every keyword in every sub actually matches its intended category
4. Sub names in en.json match sub names in centroids.json
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.Classification.keyword.KeywordSeedClassifier import (
    KeywordSeedClassifier,
)
from services.Classification.models import Language

CONFIG_DIR = Path(__file__).resolve().parents[4] / "config"
KEYWORDS_PATH = CONFIG_DIR / "keywords" / "en.json"
CENTROIDS_PATH = CONFIG_DIR / "centroids.json"


def _load_keywords() -> dict[str, dict[str, list[str]]]:
    with open(KEYWORDS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _load_centroids() -> list[dict]:
    with open(CENTROIDS_PATH, encoding="utf-8") as f:
        return json.load(f)


# ── No crossover ──


class TestNoCrossover:
    """Loading real config must not raise ValueError for duplicate keywords."""

    def test_real_config_loads_without_overlap(self) -> None:
        clf = KeywordSeedClassifier.from_locale(CONFIG_DIR, Language.EN)
        assert clf is not None

    def test_no_duplicate_keywords_across_all_subs(self) -> None:
        data = _load_keywords()
        seen: dict[str, tuple[str, str]] = {}
        duplicates: list[str] = []

        for category, subs in data.items():
            for sub, keywords in subs.items():
                for kw in keywords:
                    if kw in seen:
                        prev_cat, prev_sub = seen[kw]
                        duplicates.append(
                            f"{kw!r} in ({category}/{sub}) "
                            f"AND ({prev_cat}/{prev_sub})"
                        )
                    else:
                        seen[kw] = (category, sub)

        assert duplicates == [], (
            f"Duplicate keywords found:\n"
            + "\n".join(f"  {d}" for d in duplicates)
        )


# ── All lowercase ──


class TestAllLowercase:
    """Every keyword must be fully lowercase to match text.lower() in classifier."""

    def test_all_keywords_are_lowercase(self) -> None:
        data = _load_keywords()
        uppercase: list[str] = []

        for category, subs in data.items():
            for sub, keywords in subs.items():
                for kw in keywords:
                    if kw != kw.lower():
                        uppercase.append(f"{category}/{sub}: {kw!r}")

        assert uppercase == [], (
            f"Keywords with uppercase chars (won't match text.lower()):\n"
            + "\n".join(f"  {u}" for u in uppercase)
        )


# ── Every keyword matches its category ──


class TestKeywordMatchesByCategory:
    """Every keyword in en.json must correctly classify to its category/sub."""

    @pytest.fixture()
    def classifier(self) -> KeywordSeedClassifier:
        return KeywordSeedClassifier.from_locale(CONFIG_DIR, Language.EN)

    @pytest.fixture()
    def keywords_data(self) -> dict[str, dict[str, list[str]]]:
        return _load_keywords()

    @staticmethod
    def _keyword_ids(
        data: dict[str, dict[str, list[str]]],
    ) -> list[tuple[str, str, str]]:
        ids: list[tuple[str, str, str]] = []
        for category, subs in data.items():
            for sub, keywords in subs.items():
                for kw in keywords:
                    ids.append((category, sub, kw))
        return ids

    def test_all_keywords_classify_to_correct_category_and_sub(
        self,
        classifier: KeywordSeedClassifier,
        keywords_data: dict[str, dict[str, list[str]]],
    ) -> None:
        mismatches: list[str] = []

        for category, subs in keywords_data.items():
            for sub, keywords in subs.items():
                for kw in keywords:
                    result = classifier.classify(kw)
                    if result is None:
                        mismatches.append(
                            f"{kw!r} → None (expected {category}/{sub})"
                        )
                    elif result.category != category or result.sub != sub:
                        mismatches.append(
                            f"{kw!r} → {result.category}/{result.sub} "
                            f"(expected {category}/{sub})"
                        )

        assert mismatches == [], (
            f"Keywords classifying to wrong category/sub:\n"
            + "\n".join(f"  {m}" for m in mismatches)
        )


# ── Keyword subs match centroids subs ──


class TestKeywordsMatchCentroids:
    """Every sub in en.json must have a matching entry in centroids.json."""

    def test_keyword_subs_exist_in_centroids(self) -> None:
        kw_data = _load_keywords()
        centroids = _load_centroids()

        centroid_subs: set[tuple[str, str]] = {
            (c["category"], c["sub"]) for c in centroids
        }

        kw_subs: set[tuple[str, str]] = set()
        for category, subs in kw_data.items():
            for sub in subs:
                kw_subs.add((category, sub))

        missing_in_centroids = kw_subs - centroid_subs
        assert missing_in_centroids == set(), (
            f"Keyword subs not found in centroids.json:\n"
            + "\n".join(f"  {cat}/{sub}" for cat, sub in missing_in_centroids)
        )

    def test_centroid_subs_have_keywords(self) -> None:
        kw_data = _load_keywords()
        centroids = _load_centroids()

        kw_subs: set[tuple[str, str]] = set()
        for category, subs in kw_data.items():
            for sub in subs:
                kw_subs.add((category, sub))

        centroid_subs: set[tuple[str, str]] = {
            (c["category"], c["sub"]) for c in centroids
        }

        missing_keywords = centroid_subs - kw_subs
        assert missing_keywords == set(), (
            f"Centroid subs missing keyword entries in en.json:\n"
            + "\n".join(f"  {cat}/{sub}" for cat, sub in missing_keywords)
        )
