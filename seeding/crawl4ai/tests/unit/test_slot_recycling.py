"""
Unit tests for slot recycling:
  - NameToHandleService.resolve_with_recycling()
  - BasePipelineRunner._build_known_handles()
  - NameToHandleService._mention_to_record()
"""

from collections import deque
from unittest.mock import patch, MagicMock

import pytest

from config.schema import Influencer, Platform, NameMentionRecord
from services.extraction.NameMentionTracker import NameMention
from services.enrichment.NameToHandleService import NameToHandleService
from services.extraction.RegexHandleExtractor import ExtractedHandle


type GroupKey = tuple[str, str, str, str]


def _make_mention(
    canonical: str,
    mention_count: int,
    source_types: list[str] | None = None,
) -> NameMention:
    """Build a NameMention for testing."""
    return NameMention(
        canonical=canonical,
        variants=[canonical],
        mention_count=mention_count,
        was_searched=False,
        source_types=source_types or ["reddit"],
        source_urls={f"https://reddit.com/{canonical.lower().replace(' ', '_')}"},
        sub_names=["Gym"],
        platforms=["Instagram"],
        categories=["FITNESS"],
        regions=["US"],
    )


def _make_extracted(name: str, handle: str, platform: str = "Instagram") -> ExtractedHandle:
    """Build an ExtractedHandle for mock return values."""
    return ExtractedHandle(handle=handle, platform=platform, name=name)


class TestResolveWithRecycling:
    """resolve_with_recycling() — collision-aware per-group DDG resolution."""

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_new_handle_creates_influencer(self, mock_ddg: MagicMock) -> None:
        mock_ddg.return_value = [_make_extracted("Sean N", "seannal")]
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention("Sean N", 4),
            ]),
        }
        known: set[str] = set()

        resolved, records = svc.resolve_with_recycling(
            group_queues=queues,
            known_handles=known,
            platform=Platform.Instagram,
            sub_name="Gym",
            max_slots_per_group=5,
        )

        assert len(resolved) == 1
        assert resolved[0].name == "Sean N"
        assert "seannal" in known
        assert len(records) == 1
        assert records[0].resolved_handle == "seannal"

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_collision_recycles_slot(self, mock_ddg: MagicMock) -> None:
        """Known handle → skip, next candidate gets the slot."""
        mock_ddg.side_effect = [
            [_make_extracted("Jeff N", "jeffnippard")],  # collision
            [_make_extracted("Sean N", "seannal")],       # new
        ]
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention("Jeff N", 10),
                _make_mention("Sean N", 4),
            ]),
        }
        known: set[str] = {"jeffnippard"}

        resolved, records = svc.resolve_with_recycling(
            group_queues=queues,
            known_handles=known,
            platform=Platform.Instagram,
            sub_name="Gym",
            max_slots_per_group=5,
        )

        assert len(resolved) == 1
        assert resolved[0].name == "Sean N"
        assert len(records) == 2
        assert records[0].resolved_handle == "jeffnippard"
        assert records[1].resolved_handle == "seannal"

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_no_handle_found_consumes_slot(self, mock_ddg: MagicMock) -> None:
        mock_ddg.return_value = []
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention("Unknown Person", 5),
            ]),
        }
        known: set[str] = set()

        resolved, records = svc.resolve_with_recycling(
            group_queues=queues,
            known_handles=known,
            platform=Platform.Instagram,
            sub_name="Gym",
            max_slots_per_group=5,
        )

        assert len(resolved) == 0
        assert len(records) == 1
        assert records[0].was_searched is True
        assert records[0].resolved_handle == ""

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_max_slots_respected(self, mock_ddg: MagicMock) -> None:
        """Only fills max_slots_per_group, stops even if queue has more."""
        mock_ddg.side_effect = [
            [_make_extracted(f"Person {i}", f"handle{i}")]
            for i in range(5)
        ]
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention(f"Person {i}", 10 - i)
                for i in range(5)
            ]),
        }
        known: set[str] = set()

        resolved, _ = svc.resolve_with_recycling(
            group_queues=queues,
            known_handles=known,
            platform=Platform.Instagram,
            sub_name="Gym",
            max_slots_per_group=2,
        )

        assert len(resolved) == 2

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_known_handles_mutated_across_groups(self, mock_ddg: MagicMock) -> None:
        """Handle found in group 1 becomes known for group 2."""
        mock_ddg.side_effect = [
            [_make_extracted("Shared Person", "shared_handle")],
            [_make_extracted("Shared Person", "shared_handle")],  # collision in group 2
        ]
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention("Shared Person", 5),
            ]),
            ("Instagram", "FITNESS", "Yoga", "US"): deque([
                _make_mention("Shared Person", 5),
            ]),
        }
        known: set[str] = set()

        resolved, _ = svc.resolve_with_recycling(
            group_queues=queues,
            known_handles=known,
            platform=Platform.Instagram,
            sub_name="Gym",
            max_slots_per_group=5,
        )

        assert len(resolved) == 1

    @patch("services.extraction.NameResolver.resolve_names_via_ddg")
    def test_all_collisions_logs_error(self, mock_ddg: MagicMock) -> None:
        """When all candidates in a group are collisions, error is logged."""
        mock_ddg.return_value = [_make_extracted("Known", "known_handle")]
        audit = MagicMock()
        svc = NameToHandleService(audit)

        queues: dict[GroupKey, deque[NameMention]] = {
            ("Instagram", "FITNESS", "Gym", "US"): deque([
                _make_mention("Known", 5),
            ]),
        }
        known: set[str] = {"known_handle"}

        with patch("services.enrichment.NameToHandleService.logger") as mock_logger:
            svc.resolve_with_recycling(
                group_queues=queues,
                known_handles=known,
                platform=Platform.Instagram,
                sub_name="Gym",
                max_slots_per_group=5,
            )
            mock_logger.error.assert_called_once()


class TestMentionToRecord:
    """_mention_to_record() — converts NameMention to NameMentionRecord."""

    def test_basic_conversion(self) -> None:
        mention = _make_mention("Jeff Nippard", 10)
        record = NameToHandleService._mention_to_record(
            mention, searched=True, handle="jeffnippard", platform_str="Instagram",
        )
        assert record.canonical == "Jeff Nippard"
        assert record.mention_count == 10
        assert record.was_searched is True
        assert record.resolved_handle == "jeffnippard"
        assert record.resolved_platform == "Instagram"

    def test_no_handle_defaults(self) -> None:
        mention = _make_mention("Unknown", 3)
        record = NameToHandleService._mention_to_record(mention, searched=True)
        assert record.resolved_handle == ""
        assert record.resolved_platform == ""


class TestBuildKnownHandles:
    """_build_known_handles() — extracts lowercase handle set from gathered data."""

    def test_extracts_handles(self) -> None:
        from base_pipeline import BasePipelineRunner
        runner = MagicMock(spec=BasePipelineRunner)

        data: list[Influencer] = [
            Influencer(name="Jeff", handles={Platform.Instagram: "JeffNippard"}),
            Influencer(name="Sean", handles={Platform.YouTube: "SeanNal"}),
        ]
        result = BasePipelineRunner._build_known_handles(runner, data)
        assert result == {"jeffnippard", "seannal"}

    def test_skips_empty_handles(self) -> None:
        from base_pipeline import BasePipelineRunner
        runner = MagicMock(spec=BasePipelineRunner)

        data: list[Influencer] = [
            Influencer(name="No Handle", handles={}),
        ]
        result = BasePipelineRunner._build_known_handles(runner, data)
        assert result == set()

    def test_empty_list(self) -> None:
        from base_pipeline import BasePipelineRunner
        runner = MagicMock(spec=BasePipelineRunner)
        result = BasePipelineRunner._build_known_handles(runner, [])
        assert result == set()
