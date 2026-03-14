"""
Unit Tests: Ignore Handle Categories
======================================
Verifies all ignore list categories block their entries from extraction.
"""

import pytest

from services.extraction.RegexHandleExtractor import (
    _IGNORE_PATH_SEGMENTS,
    _IGNORE_CSS_ATRULES,
    _IGNORE_JS_FRAMEWORKS,
    _IGNORE_PLACEHOLDERS,
    _IGNORE_PLATFORM_NAMES,
    _IGNORE_AGGREGATORS,
    _IGNORE_BRANDS_MEDIA,
    _IGNORE_BRANDS_SPORTS,
    _IGNORE_BRANDS_TECH,
    _IGNORE_BRANDS_AI,
    _IGNORE_BRANDS_FASHION,
    _IGNORE_BRANDS_FOOD,
    _IGNORE_BRANDS_ENTERTAINMENT,
    _IGNORE_BRANDS_TRAVEL,
    _IGNORE_BRANDS_AUTO,
    _IGNORE_BRANDS_RETAIL,
    _IGNORE_GENERIC,
    _IGNORE_HANDLES,
    _is_valid_handle,
)


# ══════════════════════════════════════════════════════════════════════
# All categories should be subsets of the combined _IGNORE_HANDLES
# ══════════════════════════════════════════════════════════════════════

ALL_CATEGORIES = {
    "path_segments": _IGNORE_PATH_SEGMENTS,
    "css_atrules": _IGNORE_CSS_ATRULES,
    "js_frameworks": _IGNORE_JS_FRAMEWORKS,
    "placeholders": _IGNORE_PLACEHOLDERS,
    "platform_names": _IGNORE_PLATFORM_NAMES,
    "aggregators": _IGNORE_AGGREGATORS,
    "brands_media": _IGNORE_BRANDS_MEDIA,
    "brands_sports": _IGNORE_BRANDS_SPORTS,
    "brands_tech": _IGNORE_BRANDS_TECH,
    "brands_ai": _IGNORE_BRANDS_AI,
    "brands_fashion": _IGNORE_BRANDS_FASHION,
    "brands_food": _IGNORE_BRANDS_FOOD,
    "brands_entertainment": _IGNORE_BRANDS_ENTERTAINMENT,
    "brands_travel": _IGNORE_BRANDS_TRAVEL,
    "brands_auto": _IGNORE_BRANDS_AUTO,
    "brands_retail": _IGNORE_BRANDS_RETAIL,
    "generic": _IGNORE_GENERIC,
}


class TestIgnoreCategoryCompleteness:
    """Every category set is included in the combined _IGNORE_HANDLES."""

    @pytest.mark.parametrize("category_name", sorted(ALL_CATEGORIES.keys()))
    def test_category_is_subset_of_combined(self, category_name):
        category = ALL_CATEGORIES[category_name]
        missing = category - _IGNORE_HANDLES
        assert not missing, (
            f"Category '{category_name}' has entries not in _IGNORE_HANDLES: {missing}"
        )


class TestIgnoreCategoriesBlockHandles:
    """Every entry in every category should fail _is_valid_handle."""

    @pytest.mark.parametrize("category_name", sorted(ALL_CATEGORIES.keys()))
    def test_all_entries_blocked(self, category_name):
        category = ALL_CATEGORIES[category_name]
        for entry in sorted(category):
            assert not _is_valid_handle(entry), (
                f"'{entry}' in category '{category_name}' should be blocked "
                f"by _is_valid_handle but it passed"
            )


class TestIgnoreCategoriesNotEmpty:
    """Every category should have at least one entry."""

    @pytest.mark.parametrize("category_name", sorted(ALL_CATEGORIES.keys()))
    def test_category_not_empty(self, category_name):
        assert len(ALL_CATEGORIES[category_name]) > 0, (
            f"Category '{category_name}' is empty"
        )


class TestAIBrandsSpecific:
    """AI brand names must all be blocked."""

    AI_BRANDS = [
        "chatgpt", "midjourney", "metaai", "anthropic", "claude",
        "gemini", "stablediffusion", "dalle", "perplexity",
        "huggingface", "openai", "copilot",
    ]

    @pytest.mark.parametrize("brand", AI_BRANDS)
    def test_ai_brand_blocked(self, brand):
        # Check it's in the category set
        assert brand in _IGNORE_BRANDS_AI or brand in _IGNORE_BRANDS_TECH, (
            f"AI brand '{brand}' not in _IGNORE_BRANDS_AI or _IGNORE_BRANDS_TECH"
        )
        # Check it fails validation
        assert not _is_valid_handle(brand), (
            f"AI brand '{brand}' should be blocked by _is_valid_handle"
        )


class TestValidHandlesStillPass:
    """Known valid influencer handles should not be blocked."""

    VALID_HANDLES = [
        "kayla_itsines", "jeffnippard", "thebodycoach",
        "foodgod", "andrewyng", "lexfridman",
    ]

    @pytest.mark.parametrize("handle", VALID_HANDLES)
    def test_valid_handle_passes(self, handle):
        assert _is_valid_handle(handle), (
            f"Valid handle '{handle}' was incorrectly blocked"
        )
