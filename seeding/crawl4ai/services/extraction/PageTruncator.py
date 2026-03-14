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

# Markdown headings: ## or ### (skip # — usually page titles)
_HEADING_RE = re.compile(r'^(#{2,4})\s+(.+?)$', re.MULTILINE)

# Max output length (chars) — safety cap
_MAX_TRUNCATED_CHARS = 8000


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

        if _SECTION_TITLE_RE.search(heading_text):
            continue  # Section title, not a person

        words = heading_text.split()
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

    # Find the end of the last person's section:
    # either the next heading after the last person heading, or end of text
    next_heading_after_last = _HEADING_RE.search(markdown, last_start + 1)
    if next_heading_after_last:
        # Include up to 500 chars after the last person heading for their content
        section_end = min(
            next_heading_after_last.start(),
            last_start + 500,
            len(markdown),
        )
    else:
        section_end = min(last_start + 500, len(markdown))

    truncated = markdown[first_start:section_end]

    # Safety cap
    if len(truncated) > _MAX_TRUNCATED_CHARS:
        truncated = truncated[:_MAX_TRUNCATED_CHARS]

    return truncated
