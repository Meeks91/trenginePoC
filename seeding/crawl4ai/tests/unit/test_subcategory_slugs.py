"""
Unit Tests: SubCategory.resolved_strict_slugs
================================================
Tests the explicit strictSlugs config used for the inurl: DDG operator.

Verifies:
  - Easy difficulty returns whatever slugs are defined (may be empty)
  - Medium/Hard without strict_slugs raises ValueError
  - Medium/Hard with strict_slugs returns them
  - Config validation: all Medium/Hard subcats in all_categories.json have strictSlugs
"""

import pytest

from config.seed_schema import SubCategory, Difficulty


def _sub(
    sub_name: str,
    difficulty: Difficulty = Difficulty.MEDIUM,
    strict_slugs: list[str] | None = None,
) -> SubCategory:
    """Helper to build a minimal SubCategory for slug testing."""
    return SubCategory(
        sub_name=sub_name,
        is_top_level=False,
        search_prompt="test",
        alt_search_terms=[],
        known_sources=[],
        platform_notes="",
        region_notes="",
        difficulty=difficulty,
        strict_slugs=strict_slugs or [],
    )


# ── Easy difficulty ──────────────────────────────────────────────────────────

def test_easy_returns_empty_list_when_no_slugs():
    """Easy difficulty with no slugs → returns []."""
    sub = _sub("AI", difficulty=Difficulty.EASY)
    assert sub.resolved_strict_slugs == []


def test_easy_returns_slugs_when_defined():
    """Easy with strictSlugs defined → returns them (slugs are now enforced)."""
    sub = _sub("AI", difficulty=Difficulty.EASY, strict_slugs=["ai"])
    assert sub.resolved_strict_slugs == ["ai"]


# ── Medium/Hard without strict_slugs ────────────────────────────────────────

def test_medium_without_strict_slugs_raises():
    """Medium difficulty with no strictSlugs → ValueError."""
    sub = _sub("AI Creative Tools", difficulty=Difficulty.MEDIUM)
    with pytest.raises(ValueError, match="strictSlugs"):
        sub.resolved_strict_slugs


def test_hard_without_strict_slugs_raises():
    """Hard difficulty with no strictSlugs → ValueError."""
    sub = _sub("AI Coding / Dev Tools", difficulty=Difficulty.HARD)
    with pytest.raises(ValueError, match="strictSlugs"):
        sub.resolved_strict_slugs


# ── Medium/Hard with strict_slugs ───────────────────────────────────────────

def test_medium_with_strict_slugs_returns_them():
    """Medium with strictSlugs → returns the exact list."""
    slugs = ["ai-art", "midjourney", "creative"]
    sub = _sub("AI Creative Tools", difficulty=Difficulty.MEDIUM, strict_slugs=slugs)
    assert sub.resolved_strict_slugs == slugs


def test_hard_with_strict_slugs_returns_them():
    """Hard with strictSlugs → returns the exact list."""
    slugs = ["ai-coding", "llm", "developer"]
    sub = _sub("AI Coding / Dev Tools", difficulty=Difficulty.HARD, strict_slugs=slugs)
    assert sub.resolved_strict_slugs == slugs


def test_strict_slugs_not_modified():
    """resolved_strict_slugs returns the exact list, no transformation."""
    slugs = ["ai-automation", "ai-workflow", "agent", "agents"]
    sub = _sub("AI Automation / Agents", difficulty=Difficulty.MEDIUM, strict_slugs=slugs)
    assert sub.resolved_strict_slugs is sub.strict_slugs


# ── Config validation ────────────────────────────────────────────────────────

def test_all_medium_hard_subcats_have_strict_slugs():
    """Every non-Easy sub in all_categories.json must have non-empty strictSlugs."""
    from config.seed_schema import load_categories
    categories = load_categories()
    for cat in categories.values():
        for sub in cat.all_subs:
            if sub.difficulty != Difficulty.EASY:
                assert sub.strict_slugs, (
                    f"{cat.category_key}/{sub.sub_name} ({sub.difficulty.value}) "
                    f"has no strictSlugs defined"
                )
                # Should not raise
                slugs = sub.resolved_strict_slugs
                assert len(slugs) > 0
