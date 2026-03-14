"""
Regression tests for PageTruncator — LLM input truncation.

Tests ensure:
  1. Person-name sections are preserved (no data loss)
  2. Non-person content (nav, ads, footer) is trimmed
  3. Fallback to full text when no person headings found
  4. Short pages pass through unchanged
  5. Real-world listicle patterns work correctly
"""

from services.extraction.PageTruncator import truncate_for_llm


# ══════════════════════════════════════════════════════════════════════
# Basic behavior
# ══════════════════════════════════════════════════════════════════════

def test_short_page_unchanged():
    """Pages under 500 chars should pass through unchanged."""
    short = "## Jeff Nippard\n@jeffnippard on Instagram"
    assert truncate_for_llm(short) == short


def test_empty_page():
    assert truncate_for_llm("") == ""


def test_none_returns_none():
    assert truncate_for_llm(None) is None


# ══════════════════════════════════════════════════════════════════════
# Person heading extraction
# ══════════════════════════════════════════════════════════════════════

_LISTICLE_PAGE = """
# Top 10 Fitness Influencers 2026

This page has ads and navigation above.

Some navigation links and cookie banners here. Lorem ipsum dolor sit amet,
consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation
ullamco laboris nisi ut aliquip ex ea commodo consequat.

More filler text that the LLM doesn't need to see. This is the kind of
content that wastes tokens — navigation bars, disclaimers, etc.

## Jeff Nippard

Follow Jeff on Instagram: @jeffnippard
Known for science-based training content.

## Kayla Itsines

Follow Kayla on Instagram: @kayla_itsines
Creator of the BBG workout program.

## Joe Wicks

Follow Joe on Instagram: @thebodycoach
Known for 15-minute meals and PE sessions.

## Related Articles

More fitness content below...

## Newsletter

Subscribe to our newsletter for updates.
"""


def test_extracts_person_section():
    """Should extract from first person heading to last, dropping nav and footer."""
    result = truncate_for_llm(_LISTICLE_PAGE)

    # Person headings and their content preserved
    assert "## Jeff Nippard" in result
    assert "@jeffnippard" in result
    assert "## Kayla Itsines" in result
    assert "@kayla_itsines" in result
    assert "## Joe Wicks" in result
    assert "@thebodycoach" in result


def test_trims_preamble():
    """Navigation/preamble before first person heading should be trimmed."""
    result = truncate_for_llm(_LISTICLE_PAGE)
    assert "cookie banners" not in result
    assert "Lorem ipsum" not in result


def test_trims_footer():
    """Footer content after person section should be trimmed."""
    result = truncate_for_llm(_LISTICLE_PAGE)
    assert "Newsletter" not in result
    assert "Subscribe" not in result


def test_output_shorter_than_input():
    """Truncated output should be shorter than full page."""
    result = truncate_for_llm(_LISTICLE_PAGE)
    assert len(result) < len(_LISTICLE_PAGE)


# ══════════════════════════════════════════════════════════════════════
# Fallback behavior
# ══════════════════════════════════════════════════════════════════════

_NO_HEADINGS_PAGE = """
This is a long page with no markdown headings at all. It just has paragraphs
of text mentioning influencers like Jeff Nippard and Kayla Itsines scattered
throughout. There's no structure to extract from.
""" + "More content here. " * 200  # Make it long enough


def test_no_person_headings_returns_capped_text():
    """When no person headings found, return full text capped at max chars."""
    result = truncate_for_llm(_NO_HEADINGS_PAGE)
    assert len(result) <= 8000
    assert "Jeff Nippard" in result  # Content preserved


_SECTION_HEADINGS_ONLY = """
This is a page with only section-title headings, no person names.
""" + "Filler content. " * 100 + """
## Top 10 Fitness Influencers

Some intro text about fitness influencers.

## Best Instagram Accounts

More text about Instagram.

## Conclusion

Thanks for reading!
"""


def test_section_titles_not_treated_as_people():
    """Section titles like 'Top 10 Fitness Influencers' shouldn't be treated as person names."""
    result = truncate_for_llm(_SECTION_HEADINGS_ONLY)
    # Should fall back to capped text since no person headings
    assert len(result) <= 8000


# ══════════════════════════════════════════════════════════════════════
# Numbered listicle patterns
# ══════════════════════════════════════════════════════════════════════

_NUMBERED_LISTICLE = """
Lots of preamble here. Lots of preamble here. Lots of preamble here.
Lots of preamble here. Lots of preamble here. Lots of preamble here.
Lots of preamble here. Lots of preamble here. Lots of preamble here.
Lots of preamble here. Lots of preamble here. Lots of preamble here.
Lots of preamble here. Lots of preamble here. Lots of preamble here.
Lots of preamble here. Lots of preamble here. Lots of preamble here.

## 1. Martha Stewart

The queen of lifestyle content.

## 2. Gordon Ramsay

Celebrity chef and restaurateur.

## 3. Jamie Oliver

Food activist and cookbook author.

## Disclaimer

This is not financial advice.
"""


def test_numbered_headings_extracted():
    """Person names with leading numbers should still be detected."""
    result = truncate_for_llm(_NUMBERED_LISTICLE)
    assert "Martha Stewart" in result
    assert "Gordon Ramsay" in result
    assert "Jamie Oliver" in result


def test_numbered_preamble_trimmed():
    """Preamble before numbered person headings should be trimmed."""
    result = truncate_for_llm(_NUMBERED_LISTICLE)
    # Most of the preamble repetitions should be gone
    assert result.count("Lots of preamble") <= 1


# ══════════════════════════════════════════════════════════════════════
# Edge cases
# ══════════════════════════════════════════════════════════════════════

_SINGLE_PERSON = """
Lots of filler text here. More filler here. This page is about one person only.
Lots of filler text here. More filler here. This page is about one person only.
Lots of filler text here. More filler here. This page is about one person only.
Lots of filler text here. More filler here. This page is about one person only.
Lots of filler text here. More filler here. This page is about one person only.

## Alex Leonidas

The only influencer mentioned on this page.

## Related Content

More stuff here.
"""


def test_single_person_heading_fallback():
    """With only 1 person heading, should fallback to capped full text."""
    result = truncate_for_llm(_SINGLE_PERSON)
    assert "Alex Leonidas" in result


def test_max_char_cap():
    """Output should never exceed _MAX_TRUNCATED_CHARS."""
    huge_page = "## Person One\n" + "x" * 20000 + "\n## Person Two\n"
    result = truncate_for_llm(huge_page)
    assert len(result) <= 8000
