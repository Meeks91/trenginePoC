"""
Seed Architecture — Schema
===========================
Dataclass-based config layer for the seeding pipeline.
Loads category JSON, handles query building, and job generation.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field

from config.settings import CURRENT_YEAR


# ──────────────────────────────────────────────
# LLM Extraction Output Schema (Pydantic)
# ──────────────────────────────────────────────

class LLMInfluencer(BaseModel):
    """Pydantic schema for structured LLM output — distinct from config.schema.Influencer."""
    name: str = Field(description="The influencer's display name exactly as it appears on the page")
    handle: str = Field(description="Social media username without the @ symbol. Extract from URLs like instagram.com/X or tiktok.com/@X. Empty string if not visible on the page.")
    handle_platform: str = Field(default="", description="Always empty string. All extracted handles must be for the target platform.")

class SeedResults(BaseModel):
    influencers: list[LLMInfluencer] = Field(description="Discovered influencer list")


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


from config.schema import Platform

# Convenience aliases (used throughout seed_schema)
IG, YT, TK = Platform.Instagram, Platform.YouTube, Platform.TikTok


class RegionCode(str, Enum):
    US = "US"
    UK = "UK"
    # Future: FR, BR, ES


# ──────────────────────────────────────────────
# Region
# ──────────────────────────────────────────────

@dataclass(frozen=True)
class Region:
    code: RegionCode
    language: str
    label: str  # "United States", "United Kingdom"

    @property
    def search_label(self) -> str:
        """Label used in search queries — 'US' or 'UK'."""
        return self.code.value


REGIONS: dict[RegionCode, Region] = {
    RegionCode.US: Region(code=RegionCode.US, language="en", label="United States"),
    RegionCode.UK: Region(code=RegionCode.UK, language="en", label="United Kingdom"),
}


# ──────────────────────────────────────────────
# Subcategory
# ──────────────────────────────────────────────

@dataclass
class SubCategory:
    """One of the 72 sub-groupings. Loaded from JSON."""

    sub_name: str
    is_top_level: bool
    search_prompt: str          # Niche language only — no {platform}/{region}/{year}
    alt_search_terms: list[str]
    known_sources: list[str]
    platform_notes: str
    region_notes: str
    difficulty: Difficulty
    strict_slugs: list[str]     # Required for Medium/Hard — explicit inurl: slugs

    @classmethod
    def from_dict(cls, d: dict) -> SubCategory:
        return cls(
            sub_name=d["subName"],
            is_top_level=d["isTopLevel"],
            search_prompt=d["searchPrompt"],
            alt_search_terms=d["altSearchTerms"],
            known_sources=d["knownSources"],
            platform_notes=d["platformNotes"],
            region_notes=d["regionNotes"],
            difficulty=Difficulty(d["difficulty"]),
            strict_slugs=d.get("strictSlugs", []),
        )

    @property
    def all_query_terms(self) -> list[str]:
        """searchPrompt + altSearchTerms combined."""
        return [self.search_prompt] + self.alt_search_terms

    @property
    def resolved_strict_slugs(self) -> list[str]:
        """Return explicit strict_slugs for inurl: filtering.

        Raises ValueError if difficulty is Medium/Hard and strict_slugs is empty.
        Easy difficulty returns whatever is defined (may be empty).
        """
        if self.difficulty != Difficulty.EASY and not self.strict_slugs:
            raise ValueError(
                f"SubCategory '{self.sub_name}' has difficulty={self.difficulty.value} "
                f"but no strictSlugs defined. Medium/Hard subcats must define strictSlugs."
            )
        return self.strict_slugs

    def build_query_hints(self, platform: Platform, region: Region, year: str) -> str:
        """Build quoted query list with platform/region/year injected."""
        return ", ".join(
            f'"{q} {platform.value} {region.search_label} {year}"'
            for q in self.all_query_terms
        )


# ──────────────────────────────────────────────
# Category
# ──────────────────────────────────────────────

@dataclass
class Category:
    """One of the 12 top-level categories. Contains subs."""

    category_key: str           # e.g. "FITNESS", "REACTORS"
    top_level_sub: SubCategory  # The isTopLevel=true sub
    subcategories: list[SubCategory]

    @classmethod
    def from_dict(cls, d: dict) -> Category:
        subs = [SubCategory.from_dict(s) for s in d["subs"]]
        top = next(s for s in subs if s.is_top_level)
        children = [s for s in subs if not s.is_top_level]
        return cls(
            category_key=d["category"],
            top_level_sub=top,
            subcategories=children,
        )

    @property
    def all_subs(self) -> list[SubCategory]:
        """Top-level + all children."""
        return [self.top_level_sub] + self.subcategories

    @property
    def aggregate_sources(self) -> set[str]:
        """Union of all knownSources across all subs — computed, not stored."""
        sources: set[str] = set()
        for sub in self.all_subs:
            sources.update(sub.known_sources)
        return sources


# ──────────────────────────────────────────────
# Seed Job — one pipeline job
# ──────────────────────────────────────────────

@dataclass
class SeedJob:
    """One pipeline job = 1 subcategory x 1 platform x 1 region."""

    platform: Platform
    region: Region
    category_key: str
    sub: SubCategory
    year: str = field(default_factory=lambda: CURRENT_YEAR)

    @property
    def prompt(self) -> str:
        query_hints = self.sub.build_query_hints(self.platform, self.region, self.year)
        return (
            f"Find the top {self.platform.value} influencers based in the "
            f"{self.region.search_label} who create content about "
            f"{self.sub.search_prompt}.\n\n"
            f"These search queries return good results for this niche: "
            f"{query_hints}\n\n"
            f"Extract every influencer name and their {self.platform.value} "
            f"handle from the sources you find. Return as many as possible."
        )

    @staticmethod
    def build_sub_to_category(
        jobs: list[SeedJob],
    ) -> dict[str, str]:
        """Build sub_name → category_key mapping from a list of jobs."""
        return {job.sub.sub_name: job.category_key for job in jobs}






# ──────────────────────────────────────────────
# Job Generator
# ──────────────────────────────────────────────

def generate_seed_jobs(
    categories: dict[str, Category] | list[Category],
    platforms: list[Platform] | None = None,
    regions: list[Region] | None = None,
    year: str | None = None,
) -> list[SeedJob]:
    """
    Generate all seed jobs from config.
    72 subs × 3 platforms × N regions = N jobs.
    """
    platforms = platforms or list(Platform)
    regions = regions or list(REGIONS.values())
    year = year or CURRENT_YEAR

    cat_list = categories.values() if isinstance(categories, dict) else categories

    jobs: list[SeedJob] = []
    for category in cat_list:
        for sub in category.all_subs:
            for platform in platforms:
                for region in regions:
                    jobs.append(SeedJob(
                        platform=platform,
                        region=region,
                        category_key=category.category_key,
                        sub=sub,
                        year=year,
                    ))
    return jobs


# ──────────────────────────────────────────────
# Config Loader
# ──────────────────────────────────────────────

def load_categories(path: str | None = None) -> dict[str, Category]:
    """Load all_categories.json → dict of Category dataclasses keyed by category_key."""
    import json
    if path is None:
        path = str(Path(__file__).resolve().parent / "categories" / "all_categories.json")
    with open(path) as f:
        data = json.load(f)
    return {d["category"]: Category.from_dict(d) for d in data}


# ──────────────────────────────────────────────
# Usage sketch
# ──────────────────────────────────────────────

if __name__ == "__main__":
    categories = load_categories()

    # Print stats
    total_subs = sum(len(c.all_subs) for c in categories.values())
    print(f"Loaded {len(categories)} categories, {total_subs} subs")

    # Generate jobs for a single test
    test_jobs = generate_seed_jobs(
        categories=categories,
        platforms=[IG],
        regions=[REGIONS[RegionCode.US]],
    )
    print(f"Test jobs (IG × US only): {len(test_jobs)}")

    # Peek at first job
    job = test_jobs[0]
    print(f"\n--- Sample Job ---")
    print(f"Category: {job.category_key}")
    print(f"Sub: {job.sub.sub_name}")
    print(f"Difficulty: {job.sub.difficulty.value}")
    print(f"\nPrompt:\n{job.prompt}")
    print(f"\nURLs: {job.sub.known_sources[:3]}...")

    # Full matrix
    all_jobs = generate_seed_jobs(categories)
    print(f"\nFull job matrix: {len(all_jobs)} calls")
    print(f"  Easy:   {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.EASY)}")
    print(f"  Medium: {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.MEDIUM)}")
    print(f"  Hard:   {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.HARD)}")
