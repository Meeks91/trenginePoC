"""Tests for KeywordSeedClassifier."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from services.Classification.keyword.KeywordSeedClassifier import (
    KeywordSeedClassifier,
    _normalize,
)
from services.Classification.models import (
    ClassificationMethod,
    ClassificationResult,
    Language,
)


# ── Fixtures ──

VALID_KEYWORD_MAP: dict[str, tuple[str, str]] = {
    "calisthenics": ("FITNESS", "Calisthenics"),
    "street workout": ("FITNESS", "Calisthenics"),
    "powerlifting": ("FITNESS", "Powerlifting / Strength"),
    "deadlift": ("FITNESS", "Powerlifting / Strength"),
    "yoga flow": ("FITNESS", "Yoga / Mobility"),
}


def _write_keywords_json(
    tmp_dir: Path,
    data: dict[str, dict[str, list[str]]],
) -> Path:
    """Write a keywords/{locale}.json file and return config_dir."""
    kw_dir = tmp_dir / "keywords"
    kw_dir.mkdir(parents=True, exist_ok=True)
    path = kw_dir / "en.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return tmp_dir


# ── Tests: _normalize ──


class TestNormalize:
    def test_lowercase(self) -> None:
        assert _normalize("AI-Tools") == "ai tools"

    def test_hyphens_become_spaces(self) -> None:
        assert _normalize("high-protein-recipe") == "high protein recipe"

    def test_underscores_become_spaces(self) -> None:
        assert _normalize("meal_prep_sunday") == "meal prep sunday"

    def test_hashtag_stripped(self) -> None:
        assert _normalize("#crossfit") == "crossfit"

    def test_combined(self) -> None:
        assert _normalize("#AI-Tools_Review") == "ai tools review"

    def test_already_normalized(self) -> None:
        assert _normalize("calisthenics") == "calisthenics"

    def test_empty_string(self) -> None:
        assert _normalize("") == ""


# ── Tests: classify ──


class TestClassify:
    def test_exact_keyword_match(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("I love calisthenics training")
        assert result == ClassificationResult(
            category="FITNESS",
            sub="Calisthenics",
            confidence=1.0,
            method=ClassificationMethod.KEYWORD,
        )

    def test_case_insensitive(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("POWERLIFTING is my life")
        assert result is not None
        assert result.sub == "Powerlifting / Strength"

    def test_no_match_returns_none(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("cooking recipes for dinner")
        assert result is None

    def test_hyphenated_input_matches_space_keyword(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("my street-workout journey continues")
        assert result is not None
        assert result.sub == "Calisthenics"

    def test_natural_language_matches(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("my street workout journey continues")
        assert result is not None
        assert result.sub == "Calisthenics"

    def test_hashtag_matches(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("Love #calisthenics training")
        assert result is not None
        assert result.sub == "Calisthenics"

    def test_underscore_matches(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("my yoga_flow practice")
        assert result is not None
        assert result.sub == "Yoga / Mobility"

    def test_confidence_always_one(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("yoga-flow for beginners")
        assert result is not None
        assert result.confidence == 1.0

    def test_method_is_keyword(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("deadlift PR today")
        assert result is not None
        assert result.method == ClassificationMethod.KEYWORD

    def test_empty_text_returns_none(self) -> None:
        clf = KeywordSeedClassifier(VALID_KEYWORD_MAP)
        result = clf.classify("")
        assert result is None


# ── Tests: from_locale factory ──


class TestFromLocale:
    def test_loads_valid_config(self) -> None:
        data = {
            "FITNESS": {
                "Calisthenics": ["calisthenics", "bodyweight-exercise"],
                "Yoga / Mobility": ["yoga-flow"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            clf = KeywordSeedClassifier.from_locale(config_dir, Language.EN)
            result = clf.classify("calisthenics workout")
            assert result is not None
            assert result.category == "FITNESS"
            assert result.sub == "Calisthenics"

    def test_from_locale_normalizes_keywords(self) -> None:
        data = {
            "AI": {
                "AI Tools": ["AI-Tools", "Best-AI-Apps"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            clf = KeywordSeedClassifier.from_locale(config_dir, Language.EN)
            result = clf.classify("I review AI tools for creators")
            assert result is not None
            assert result.category == "AI"
            assert result.sub == "AI Tools"

    def test_exact_overlap_raises(self) -> None:
        data = {
            "FITNESS": {
                "Calisthenics": ["overlap-keyword"],
                "Powerlifting / Strength": ["overlap-keyword"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            with pytest.raises(ValueError, match="Keyword overlap"):
                KeywordSeedClassifier.from_locale(config_dir, Language.EN)

    def test_case_variant_overlap_raises(self) -> None:
        data = {
            "FITNESS": {
                "Calisthenics": ["CrossFit"],
                "Powerlifting / Strength": ["crossfit"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            with pytest.raises(ValueError, match="Keyword overlap"):
                KeywordSeedClassifier.from_locale(config_dir, Language.EN)

    def test_hyphen_space_variant_overlap_raises(self) -> None:
        data = {
            "FITNESS": {
                "Calisthenics": ["street-workout"],
                "Yoga / Mobility": ["street workout"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            with pytest.raises(ValueError, match="Keyword overlap"):
                KeywordSeedClassifier.from_locale(config_dir, Language.EN)

    def test_cross_category_overlap_raises(self) -> None:
        data = {
            "FITNESS": {
                "Calisthenics": ["shared-term"],
            },
            "BEAUTY": {
                "Skincare Routines": ["shared-term"],
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = _write_keywords_json(Path(tmp), data)
            with pytest.raises(ValueError, match="Keyword overlap"):
                KeywordSeedClassifier.from_locale(config_dir, Language.EN)
