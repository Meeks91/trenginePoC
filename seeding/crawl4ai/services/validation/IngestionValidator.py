"""
IngestionValidator
====================
Validates pipeline results against a reference list of expected
"canary" influencers — known creators per sub/region that should appear.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config.schema import Influencer


CANARY_FILE = Path(__file__).resolve().parent.parent.parent / "config" / "canary_influencers.json"


@dataclass
class ValidationResult:
    """Result of canary validation for one sub."""
    expected: list[str]
    found: list[str]
    missing: list[str]
    pass_rate: float  # 0.0 – 1.0


class IngestionValidator:
    """Validates extraction results against canary influencer list."""

    def __init__(self, canary_path: Path = CANARY_FILE):
        self._canaries: dict = {}
        if canary_path.exists():
            with open(canary_path) as f:
                self._canaries = json.load(f)

    def validate(
        self,
        influencers: list[Influencer],
        category_key: str,
        sub_name: str,
        region: str,
    ) -> ValidationResult | None:
        """
        Check if known canary influencers were found in results.

        Returns:
            ValidationResult if canaries exist for this sub, else None.
        """
        # Look up canaries for this category/sub/region
        canary_list = (
            self._canaries
            .get(category_key, {})
            .get(sub_name, {})
            .get(region, [])
        )

        if not canary_list:
            return None

        # Build lookup set from found influencers (name + handle)
        found_names = set()
        for inf in influencers:
            found_names.add(inf.name.lower().strip())
            for handle_val in inf.handles.values():
                if handle_val:
                    found_names.add(handle_val.lower().strip().lstrip("@"))

        # Check each canary
        expected = [c["name"] if isinstance(c, dict) else c for c in canary_list]
        found = []
        missing = []

        for name in expected:
            name_lower = name.lower().strip()
            if name_lower in found_names:
                found.append(name)
            else:
                # Also check partial match (e.g. "Kayla" in "Kayla Itsines")
                if any(name_lower in fn for fn in found_names):
                    found.append(name)
                else:
                    missing.append(name)

        pass_rate = len(found) / len(expected) if expected else 1.0

        return ValidationResult(
            expected=expected,
            found=found,
            missing=missing,
            pass_rate=pass_rate,
        )
