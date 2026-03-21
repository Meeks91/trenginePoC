"""
Unit Tests: CrossPlatformHandleResolverService
===============================================
Tests the public resolve() API and key internal paths:
  - Empty input → no-op
  - Influencers with no handles → skipped
  - min_sources filters low-frequency influencers
  - max_lookups caps the queue
  - Missing platform found → new entry appended
  - Already has all platforms → nothing searched
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from config.schema import Influencer, Platform
from services.audit.AuditService import AuditLog
from services.handleResolution.CrossPlatformHandleResolverService import CrossPlatformHandleResolverService


# Fixtures:

def _mock_search_client(results: list[dict] | None = None) -> MagicMock:
    client = MagicMock()
    client.search_text.return_value = results if results is not None else []
    client.nr_query_template.return_value = "{name} Instagram YouTube TikTok"
    return client


def _gen_resolver(
    tmp: str,
    search_client: MagicMock | None = None,
    max_lookups: int = 10,
    min_sources: int = 0,
) -> CrossPlatformHandleResolverService:
    audit = AuditLog(Path(tmp), "test")
    return CrossPlatformHandleResolverService(
        audit,
        search_client=search_client or _mock_search_client(),
        max_lookups=max_lookups,
        min_sources=min_sources,
        delay_seconds=0,
    )


def _influencer_with_sources(
    name: str,
    handles: dict,
    source_count: int = 0,
) -> Influencer:
    inf = Influencer(name=name, handles=handles)
    inf.source_urls = [f"https://example.com/{i}" for i in range(source_count)]
    return inf

# Fixtures


class TestCrossPlatformHandleResolverService:

    def test_empty_input_returns_empty(self):
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            resolver = _gen_resolver(tmp)

            # When
            result = resolver.resolve([])

        # Then
        assert result == []

    def test_name_only_influencers_are_skipped(self):
        """Influencers with no handles at all are not searched."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            client = _mock_search_client()
            resolver = _gen_resolver(tmp, search_client=client)
            name_only = [Influencer(name="Joe Wicks", handles={})]

            # When
            result = resolver.resolve(name_only)

        # Then
        assert len(result) == 1
        client.search_text.assert_not_called()

    def test_influencer_with_all_platforms_skipped(self):
        """Influencers already having all platform handles are not searched."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            client = _mock_search_client()
            resolver = _gen_resolver(tmp, search_client=client)
            full = [Influencer(name="Kayla Itsines", handles={
                Platform.Instagram: "kayla_itsines",
                Platform.TikTok: "kayla_itsines",
                Platform.YouTube: "kayla_itsines",
            })]

            # When
            result = resolver.resolve(full)

        # Then
        assert len(result) == 1
        client.search_text.assert_not_called()

    def test_missing_platform_found_appends_new_entry(self):
        """When search finds a handle on a missing platform, a new entry is appended."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            results = [{"href": "https://www.tiktok.com/@kayla_itsines", "title": "", "body": ""}]
            client = _mock_search_client(results=results)
            resolver = _gen_resolver(tmp, search_client=client)
            influencers = [
                Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}),
            ]

            # When
            result = resolver.resolve(influencers)

        # Then: original IG entry + new TikTok entry (and possibly YouTube)
        assert len(result) > 1
        platforms = {list(inf.handles.keys())[0] for inf in result if inf.handles}
        assert Platform.Instagram in platforms
        assert Platform.TikTok in platforms

    def test_min_sources_filters_low_frequency_influencers(self):
        """Influencers with fewer sources than min_sources are skipped."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            client = _mock_search_client(results=[
                {"href": "https://www.tiktok.com/@test_handle", "title": "", "body": ""},
            ])
            resolver = _gen_resolver(tmp, search_client=client, min_sources=3)
            influencers = [
                _influencer_with_sources(
                    "Low Freq",
                    handles={Platform.Instagram: "low_freq"},
                    source_count=1,
                ),
            ]

            # When
            result = resolver.resolve(influencers)

        # Then: low_freq is below threshold, search not called
        assert len(result) == 1
        client.search_text.assert_not_called()

    def test_max_lookups_caps_queue(self):
        """max_lookups caps how many influencers are searched."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            client = _mock_search_client(results=[])
            resolver = _gen_resolver(tmp, search_client=client, max_lookups=2)

            influencers = [
                Influencer(name=f"Creator {i}", handles={Platform.Instagram: f"creator{i}"})
                for i in range(5)
            ]

            # When
            resolver.resolve(influencers)

        # max_lookups=2 → at most 2 influencers × their missing platforms searched
        # Each influencer missing TikTok + YouTube = 2 calls × 2 influencers = 4 max
        call_count = client.search_text.call_count
        assert call_count <= 4, f"Expected ≤4 search calls, got {call_count}"

    def test_search_returns_none_no_new_entry(self):
        """When search returns no useful result, no new entry is appended."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            client = _mock_search_client(results=[
                {"href": "https://example.com/random", "title": "Unrelated", "body": "No handles"},
            ])
            resolver = _gen_resolver(tmp, search_client=client)
            influencers = [
                Influencer(name="Unknown Creator", handles={Platform.Instagram: "unknown_creator"}),
            ]

            # When
            result = resolver.resolve(influencers)

        # Then: only the original entry, no new cross-platform entries
        resolved_with_tiktok = [inf for inf in result if Platform.TikTok in inf.handles]
        assert resolved_with_tiktok == []

    def test_resolve_returns_same_list_reference(self):
        """resolve() mutates and returns the same list that was passed in."""
        # Given
        with tempfile.TemporaryDirectory() as tmp:
            resolver = _gen_resolver(tmp)
            influencers: list[Influencer] = []

            # When
            result = resolver.resolve(influencers)

        # Then
        assert result is influencers

    def test_platform_missing_from_platform_domains_raises_value_error(self):
        """If _ALL_PLATFORMS contains a platform not in PLATFORM_DOMAINS, ValueError is raised."""
        import services.handleResolution.CrossPlatformHandleResolverService as svc_module

        fake_platform = MagicMock()
        fake_platform.value = "UnknownPlatform"

        original_all_platforms = svc_module._ALL_PLATFORMS
        svc_module._ALL_PLATFORMS = frozenset({fake_platform})

        try:
            with tempfile.TemporaryDirectory() as tmp:
                resolver = _gen_resolver(tmp)
                influencers = [
                    Influencer(name="Test Creator", handles={Platform.Instagram: "test_creator"}),
                ]

                with pytest.raises(ValueError, match="UnknownPlatform"):
                    resolver.resolve(influencers)
        finally:
            svc_module._ALL_PLATFORMS = original_all_platforms
