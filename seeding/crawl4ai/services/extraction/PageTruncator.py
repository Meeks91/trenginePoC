"""
PageTruncator — Extract the relevant listicle section from a page.

When a long page is sent to the LLM, most of it is navigation, ads,
related posts, and other noise. This module finds the section that
contains the influencer list and returns only that.

Strategy:
  1. Find all markdown headings (## or ###)
  2. Filter headings that look like person names (capitalized, 1-5 words)
  3. Extract from first person-heading to last person-heading + trailing content
  4. Fall back to full text if no person headings found

Typical savings: 50-70% token reduction on long listicle pages.
"""

from __future__ import annotations

import re

# Headings that are section titles, not person names
_SECTION_TITLE_RE = re.compile(
    r'(?:top\s*\d+|best\s*\d+|influencer|creator|blogger|vlogger|'
    r'food|travel|fitness|beauty|fashion|lifestyle|'
    r'instagram|tiktok|youtube|london|uk|us|'
    r'follow|subscribe|check out|related|also|more|'
    r'conclusion|summary|faq|about|contact|source|'
    r'comment|share|newsletter|cookie|privacy|'
    r'table of contents|how to|what is|why)',
    re.IGNORECASE,
)

# Markdown links: [text](url)
_MD_LINK_RE = re.compile(r'\[([^\]]*)\]\([^)]*\)')

# Trailing parenthetical context: "Name (@handle on YouTube)" → "Name"
_TRAILING_PAREN_RE = re.compile(r'\s*\(.*?\)\s*$')

# Markdown headings: ## or ### (skip # — usually page titles)
_HEADING_RE = re.compile(r'^(#{2,4})\s+(.+?)$', re.MULTILINE)

# Max output length (chars) — safety cap
_MAX_TRUNCATED_CHARS = 12_000


def _clean_heading_for_classification(heading: str) -> str:
    """Strip markdown links and parenthetical context from a heading.

    This prevents inline platform links like
    ``## Joe Wicks ([@handle on YouTube](url))``
    from being misclassified as section titles due to 'YouTube' matching
    the section-title regex.
    """
    # Strip markdown link syntax: [text](url) → text
    cleaned = _MD_LINK_RE.sub(r'\1', heading)
    # Strip trailing parenthetical (handle/platform context)
    cleaned = _TRAILING_PAREN_RE.sub('', cleaned).strip()
    return cleaned


def truncate_for_llm(markdown: str) -> str:
    """Extract the influencer-list section from a markdown page.

    Returns a shorter version of the markdown containing only the
    section between person-name headings. Falls back to the original
    text (capped at _MAX_TRUNCATED_CHARS) if no person headings found.
    """
    if not markdown or len(markdown) < 500:
        return markdown  # Too short to bother truncating

    # Find all person-name headings
    person_headings: list[tuple[int, int, str]] = []  # (start, end, text)
    for match in _HEADING_RE.finditer(markdown):
        heading_text = match.group(2).strip()
        # Strip numbering: "1. Martha Stewart" → "Martha Stewart"
        heading_text = re.sub(r'^\d+[.)\-]\s*', '', heading_text).strip()

        # Clean heading before classification — strip links and parens
        # so inline platform references don't trigger section-title filter
        heading_clean = _clean_heading_for_classification(heading_text)

        if _SECTION_TITLE_RE.search(heading_clean):
            continue  # Section title, not a person

        words = heading_clean.split()
        if len(words) < 1 or len(words) > 5:
            continue
        # At least one word should be capitalized
        if not any(w[0].isupper() for w in words if w):
            continue

        person_headings.append((match.start(), match.end(), heading_text))

    if len(person_headings) < 2:
        # Not enough person headings — return full text (capped)
        return markdown[:_MAX_TRUNCATED_CHARS]

    # Extract from first person heading to end of last person heading's section
    first_start = person_headings[0][0]
    last_start = person_headings[-1][0]

    # Find the next non-person heading after the last person heading.
    # This captures the full profile content for the last person.
    section_end = len(markdown)
    for later_match in _HEADING_RE.finditer(markdown, last_start + 1):
        later_text = later_match.group(2).strip()
        later_clean = _clean_heading_for_classification(
            re.sub(r'^\d+[.)\-]\s*', '', later_text).strip()
        )
        # Stop at the first heading that is NOT a person heading
        is_person = (
            not _SECTION_TITLE_RE.search(later_clean)
            and 1 <= len(later_clean.split()) <= 5
            and any(w[0].isupper() for w in later_clean.split() if w)
        )
        if not is_person:
            section_end = later_match.start()
            break

    truncated = markdown[first_start:section_end]

    # Safety cap
    if len(truncated) > _MAX_TRUNCATED_CHARS:
        truncated = truncated[:_MAX_TRUNCATED_CHARS]

    return truncated
