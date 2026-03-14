"""SearchCache — Disk-backed cache for DDG search results.

Stores DDG query responses as JSON files keyed by query hash.
Avoids redundant DDG calls across jobs and across pipeline re-runs.

Cache location: results/search_cache/{hash}.json
TTL: Configurable (default 24 hours).
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any


class SearchCache:
    """Disk-backed DDG result cache with TTL.

    Usage:
        cache = SearchCache(cache_dir=Path("results/search_cache"))
        results = cache.get("site:modash.io Yoga influencers 2026")
        if results is None:
            results = ddgs.text(query, ...)
            cache.put("site:modash.io Yoga influencers 2026", results)
    """

    def __init__(
        self,
        cache_dir: Path,
        ttl_seconds: int = 86400,  # 24 hours
    ) -> None:
        self._cache_dir = cache_dir
        self._ttl = ttl_seconds
        self._hits = 0
        self._misses = 0
        os.makedirs(cache_dir, exist_ok=True)

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def misses(self) -> int:
        return self._misses

    def get(self, query: str) -> list[dict[str, Any]] | None:
        """Look up cached results for a query. Returns None on miss."""
        path = self._path_for(query)
        if not path.exists():
            self._misses += 1
            return None

        try:
            with open(path) as f:
                entry = json.load(f)
        except (json.JSONDecodeError, OSError):
            self._misses += 1
            return None

        # Check TTL
        if time.time() - entry.get("ts", 0) > self._ttl:
            self._misses += 1
            return None

        self._hits += 1
        results: list[dict[str, Any]] = entry.get("results", [])
        return results

    def put(self, query: str, results: list[dict[str, Any]]) -> None:
        """Store results for a query."""
        path = self._path_for(query)
        entry = {
            "query": query,
            "ts": time.time(),
            "results": results,
        }
        with open(path, "w") as f:
            json.dump(entry, f, ensure_ascii=False)

    def _path_for(self, query: str) -> Path:
        """Deterministic file path for a query."""
        h = hashlib.sha256(query.encode()).hexdigest()[:16]
        return self._cache_dir / f"{h}.json"

    def clear(self) -> int:
        """Remove all cached entries. Returns count removed."""
        count = 0
        for p in self._cache_dir.glob("*.json"):
            p.unlink()
            count += 1
        self._hits = 0
        self._misses = 0
        return count
