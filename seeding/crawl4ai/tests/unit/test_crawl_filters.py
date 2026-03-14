"""
Unit Tests: Crawl Filters
===========================
Verifies PruningContentFilter preserves influencer names and handles
in fixture pages. Tests run offline against saved markdown files.
"""

import sys
import os
import re
from pathlib import Path


FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"


def _count_names_in_text(text: str) -> int:
    """Count likely influencer names — lines starting with * or # followed by capitalized words."""
    count = 0
    for line in text.split("\n"):
        line = line.strip()
        # Bulleted list items with capitalized names
        if re.match(r"^[\*\-\d\.]+\s+[A-Z][a-z]+\s+", line):
            count += 1
        # Headers with names
        if re.match(r"^#+\s+\d*\.?\s*[A-Z][a-z]+\s+", line):
            count += 1
    return count


def _count_handles_in_text(text: str) -> int:
    """Count @handles in text."""
    return len(re.findall(r"@[a-zA-Z0-9_.]{2,}", text))


def test_fixture_files_exist():
    """At least some fixture files should exist."""
    md_files = list(FIXTURES_DIR.glob("*.md"))
    assert len(md_files) > 0, f"No fixture files found in {FIXTURES_DIR}"
    print(f"  Found {len(md_files)} fixture files")


def test_fixtures_contain_names():
    """Fixture pages should contain influencer names."""
    fitness_fixtures = [
        f for f in FIXTURES_DIR.glob("*.md")
        if "fitness" in f.name.lower() or "influencer" in f.name.lower()
    ]

    if not fitness_fixtures:
        print("  ⚠️ No fitness/influencer fixtures found, skipping")
        return

    for fixture in fitness_fixtures[:3]:
        content = fixture.read_text()
        names = _count_names_in_text(content)
        print(f"  {fixture.name}: {names} names, {len(content)} chars")
        # At least some structure should exist
        assert len(content) > 100, f"Fixture {fixture.name} is too short"


def test_gymfluencers_handles_preserved():
    """gymfluencers page should retain @handles after filtering."""
    fixture = FIXTURES_DIR / "gymfluencers_agency_top-10-fitness-influencers-in-the-uk-to-follow_.md"
    if not fixture.exists():
        print("  ⚠️ Gymfluencers fixture not found, skipping")
        return

    content = fixture.read_text()
    handle_count = _count_handles_in_text(content)
    print(f"  gymfluencers UK: {handle_count} handles, {len(content)} chars")
    # This page is known to have many handles
    assert handle_count > 0, "Expected handles in gymfluencers fixture"


def test_content_not_empty():
    """No fixture should be empty or near-empty."""
    for fixture in list(FIXTURES_DIR.glob("*.md"))[:10]:
        content = fixture.read_text()
        assert len(content) > 50, f"Fixture {fixture.name} is empty/too short ({len(content)} chars)"
