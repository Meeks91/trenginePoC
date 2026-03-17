"""KnownNameIndex — Fast lookup: 'is this name already resolved?'

Maps normalized influencer names to their known handles.
Used by NameMentionTracker to skip NR for names that already
have handles from extraction.

Normalization strips spaces/underscores/dots/@ so 'Jeff Nippard'
matches 'jeffnippard' (handle-as-name).
"""

from __future__ import annotations

from config.schema import Influencer


class KnownNameIndex:
    """Maps normalized influencer names to their known handles.

    Accepts a list of already-merged Influencer objects and builds
    an internal dict of normalized_name → set[handle].  The has_handles
    query answers: 'does this name (or a handle variant of it) already
    exist in our extracted data WITH at least one social handle?'
    """

    __slots__ = ("_name_to_handles",)

    # ── API ──

    def __init__(self, influencers: list[Influencer]) -> None:
        self._name_to_handles: dict[str, set[str]] = {}
        for inf in influencers:
            key = self._normalize(inf.name)
            if key and inf.handles:
                handles = {h.lower() for h in inf.handles.values()}
                self._name_to_handles.setdefault(key, set()).update(handles)

    def has_handles(self, name: str) -> bool:
        """Return True if name (after normalization) maps to known handles."""
        return bool(self._name_to_handles.get(self._normalize(name)))

    # ── Internal ──

    @staticmethod
    def _normalize(name: str) -> str:
        """Strip spaces, underscores, dots, @ for fuzzy name matching."""
        return (
            name.strip()
            .lower()
            .replace(" ", "")
            .replace("_", "")
            .replace(".", "")
            .replace("@", "")
        )
