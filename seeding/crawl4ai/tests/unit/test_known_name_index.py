"""Tests for KnownNameIndex — NR pre-filtering lookup."""

from config.schema import Influencer, Platform
from services.extraction.KnownNameIndex import KnownNameIndex


class TestKnownNameIndex:

    def test_exact_name_match(self) -> None:
        """'Jeff Nippard' with IG handle → has_handles('Jeff Nippard') is True."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
        ])
        assert index.has_handles("Jeff Nippard") is True

    def test_handle_as_name_match(self) -> None:
        """'jeffnippard' normalizes to same key as 'Jeff Nippard' → True."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
        ])
        assert index.has_handles("jeffnippard") is True

    def test_no_handles_returns_false(self) -> None:
        """Name-only influencer (no handles) → has_handles returns False."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={}),
        ])
        assert index.has_handles("Jeff Nippard") is False

    def test_unknown_name_returns_false(self) -> None:
        """Name not in index → False."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
        ])
        assert index.has_handles("Mike Israetel") is False

    def test_case_insensitive(self) -> None:
        """Lookup is case-insensitive."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
        ])
        assert index.has_handles("jeff nippard") is True
        assert index.has_handles("JEFF NIPPARD") is True

    def test_dots_and_underscores_stripped(self) -> None:
        """Dots and underscores stripped: 'jeff.nippard' matches 'Jeff Nippard'."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
        ])
        assert index.has_handles("jeff.nippard") is True
        assert index.has_handles("jeff_nippard") is True

    def test_empty_list(self) -> None:
        """Empty influencer list → all lookups False."""
        index = KnownNameIndex([])
        assert index.has_handles("Jeff Nippard") is False

    def test_multiple_influencers(self) -> None:
        """Multiple influencers all queryable."""
        index = KnownNameIndex([
            Influencer(name="Jeff Nippard", handles={Platform.Instagram: "jeffnippard"}),
            Influencer(name="Mike Israetel", handles={Platform.YouTube: "rpstrength"}),
        ])
        assert index.has_handles("Jeff Nippard") is True
        assert index.has_handles("Mike Israetel") is True
        assert index.has_handles("Unknown Person") is False
