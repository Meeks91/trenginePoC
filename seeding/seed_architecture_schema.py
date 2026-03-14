"""
Seed Architecture — Schema Sketch
==================================
Dataclass-based config layer for the Firecrawl seed pipeline.
Loads category JSON, handles query building, credit tiering, and job generation.

This is a SCHEMA SKETCH — not all data populated, but all types and methods defined.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────
# Firecrawl Output Schema (Pydantic — required by Firecrawl)
# ──────────────────────────────────────────────

class Influencer(BaseModel):
    name: str = Field(description="Creator display name")
    handle: str = Field(description="Platform handle (e.g. @username)")

class SeedResults(BaseModel):
    influencers: list[Influencer] = Field(description="Discovered influencer list")


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class Difficulty(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @property
    def max_credits(self) -> int:
        return {
            Difficulty.EASY: 30,
            Difficulty.MEDIUM: 40,
            Difficulty.HARD: 50,
        }[self]

    @property
    def model(self) -> str:
        return "spark-1-mini"


class Platform(str, Enum):
    IG = "Instagram"
    YT = "YouTube"
    TK = "TikTok"


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
        )

    @property
    def all_query_terms(self) -> list[str]:
        """searchPrompt + altSearchTerms combined."""
        return [self.search_prompt] + self.alt_search_terms

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
# Seed Job — one Firecrawl agent call
# ──────────────────────────────────────────────

@dataclass
class SeedJob:
    """Represents a single Firecrawl /agent call."""

    platform: Platform
    region: Region
    category_key: str
    sub: SubCategory
    year: str = "2025"

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

    @property
    def agent_config(self) -> dict:
        """Ready-to-send config for app.agent(**config)."""
        return {
            "prompt": self.prompt,
            "urls": self.sub.known_sources,
            "schema": SeedResults,
            "model": self.sub.difficulty.model,
            "maxCredits": self.sub.difficulty.max_credits,
        }


# ──────────────────────────────────────────────
# Seed Job Result — output of one Firecrawl call
# ──────────────────────────────────────────────

@dataclass
class SeedJobResult:
    """Result of executing a SeedJob. Contains both the job spec and the results."""

    # Job spec (copied from SeedJob for self-contained output)
    category_key: str
    sub_name: str
    platform: str
    region: str
    difficulty: str
    model: str
    credits_used: int
    prompt: str
    urls_sent: list[str]

    # Results
    influencers: list[dict]   # [{name, handle}, ...]
    count: int
    timestamp: str
    meets_threshold: bool     # count >= 10

    @classmethod
    def from_job(cls, job: SeedJob, raw_result: SeedResults,
                 credits_used: int, timestamp: str) -> SeedJobResult:
        influencers = [{"name": i.name, "handle": i.handle}
                       for i in raw_result.influencers]
        return cls(
            category_key=job.category_key,
            sub_name=job.sub.sub_name,
            platform=job.platform.value,
            region=job.region.search_label,
            difficulty=job.sub.difficulty.value,
            model=job.sub.difficulty.model,
            credits_used=credits_used,
            prompt=job.prompt,
            urls_sent=job.sub.known_sources,
            influencers=influencers,
            count=len(influencers),
            timestamp=timestamp,
            meets_threshold=len(influencers) >= 10,
        )

    def to_json(self) -> dict:
        """Serializable dict for JSON output."""
        from dataclasses import asdict
        return asdict(self)

    @staticmethod
    def to_md_report(results: list[SeedJobResult]) -> str:
        """Generate a full MD report from a list of results."""
        lines = ["# Seed Crawl Results Report\n"]

        # Summary table
        passed = sum(1 for r in results if r.meets_threshold)
        total_influencers = sum(r.count for r in results)
        total_credits = sum(r.credits_used for r in results)
        lines.append(f"**{len(results)} jobs** | **{passed}/{len(results)} passed threshold** "
                      f"| **{total_influencers} influencers** | **{total_credits} credits used**\n")

        lines.append("| # | Category | Sub | Platform | Region | Diff | Count | Pass? | Credits |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(results, 1):
            icon = "✅" if r.meets_threshold else "❌"
            lines.append(f"| {i} | {r.category_key} | {r.sub_name} | {r.platform} | "
                          f"{r.region} | {r.difficulty} | {r.count} | {icon} | {r.credits_used} |")

        # Per-job detail
        lines.append("\n---\n")
        for r in results:
            lines.append(f"## {r.category_key} / {r.sub_name} ({r.platform} × {r.region})\n")
            lines.append(f"- **Difficulty:** {r.difficulty} | **Credits:** {r.credits_used}")
            lines.append(f"- **Threshold:** {'✅ PASS' if r.meets_threshold else '❌ FAIL'} ({r.count}/10)")
            lines.append(f"- **Timestamp:** {r.timestamp}\n")
            if r.influencers:
                lines.append("| Name | Handle |")
                lines.append("|---|---|")
                for inf in r.influencers:
                    lines.append(f"| {inf['name']} | {inf['handle']} |")
            lines.append("")

        return "\n".join(lines)


# ──────────────────────────────────────────────
# Job Generator
# ──────────────────────────────────────────────

def generate_seed_jobs(
    categories: dict[str, Category] | list[Category],
    platforms: list[Platform] | None = None,
    regions: list[Region] | None = None,
    year: str = "2025",
) -> list[SeedJob]:
    """
    Generate all seed jobs from config.
    72 subs × 3 platforms × 2 regions = 432 jobs.
    """
    platforms = platforms or list(Platform)
    regions = regions or list(REGIONS.values())

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
        platforms=[Platform.IG],
        regions=[REGIONS[RegionCode.US]],
    )
    print(f"Test jobs (IG × US only): {len(test_jobs)}")

    # Peek at first job
    job = test_jobs[0]
    print(f"\n--- Sample Job ---")
    print(f"Category: {job.category_key}")
    print(f"Sub: {job.sub.sub_name}")
    print(f"Difficulty: {job.sub.difficulty.value} → {job.sub.difficulty.max_credits} credits")
    print(f"Model: {job.sub.difficulty.model}")
    print(f"\nPrompt:\n{job.prompt}")
    print(f"\nURLs: {job.sub.known_sources[:3]}...")

    # Full matrix
    all_jobs = generate_seed_jobs(categories)
    print(f"\nFull job matrix: {len(all_jobs)} calls")
    print(f"  Easy:   {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.EASY)}")
    print(f"  Medium: {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.MEDIUM)}")
    print(f"  Hard:   {sum(1 for j in all_jobs if j.sub.difficulty == Difficulty.HARD)}")
