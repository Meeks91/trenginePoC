"""Tests for SearchCache — disk-backed DDG result cache."""

import json
import time
from pathlib import Path

import pytest

from services.search.SearchCache import SearchCache


class TestSearchCache:
    """Tests for SearchCache hit/miss/TTL/clear behavior."""

    @pytest.fixture
    def cache_dir(self, tmp_path: Path) -> Path:
        """Provide a clean temp directory for cache."""
        return tmp_path / "search_cache"

    @pytest.fixture
    def cache(self, cache_dir: Path) -> SearchCache:
        """Provide a fresh SearchCache instance."""
        return SearchCache(cache_dir=cache_dir, ttl_seconds=3600)

    def test_miss_returns_none(self, cache: SearchCache):
        """Cache miss returns None."""
        assert cache.get("unknown query") is None

    def test_put_then_get(self, cache: SearchCache):
        """Put results, then get them back."""
        results = [{"href": "https://example.com", "title": "Example"}]
        cache.put("test query", results)
        cached = cache.get("test query")
        assert cached == results

    def test_hit_counter(self, cache: SearchCache):
        """Hits and misses are counted."""
        cache.put("q1", [{"href": "a"}])

        cache.get("q1")       # hit
        cache.get("q1")       # hit
        cache.get("missing")  # miss

        assert cache.hits == 2
        assert cache.misses == 1

    def test_miss_counter(self, cache: SearchCache):
        """Misses are counted for non-existent queries."""
        cache.get("nope")
        cache.get("nope2")
        assert cache.misses == 2
        assert cache.hits == 0

    def test_ttl_expired(self, cache_dir: Path):
        """Expired entries return None."""
        cache = SearchCache(cache_dir=cache_dir, ttl_seconds=1)
        cache.put("q", [{"href": "old"}])

        # Manually backdate the timestamp
        path = cache._path_for("q")
        with open(path) as f:
            entry = json.load(f)
        entry["ts"] = time.time() - 10  # 10 seconds ago
        with open(path, "w") as f:
            json.dump(entry, f)

        assert cache.get("q") is None  # expired

    def test_different_queries_different_cache(self, cache: SearchCache):
        """Different queries have independent caches."""
        cache.put("query A", [{"href": "a"}])
        cache.put("query B", [{"href": "b"}])

        assert cache.get("query A") == [{"href": "a"}]
        assert cache.get("query B") == [{"href": "b"}]

    def test_clear(self, cache: SearchCache):
        """Clear removes all entries and resets counters."""
        cache.put("q1", [{"href": "a"}])
        cache.put("q2", [{"href": "b"}])
        cache.get("q1")  # hit

        removed = cache.clear()
        assert removed == 2
        assert cache.get("q1") is None
        assert cache.hits == 0
        assert cache.misses == 1  # the miss from get after clear

    def test_corrupted_json_returns_miss(self, cache: SearchCache):
        """Corrupted cache files return None (miss) without crashing."""
        cache.put("q", [{"href": "ok"}])
        path = cache._path_for("q")
        with open(path, "w") as f:
            f.write("NOT JSON{{{")

        assert cache.get("q") is None

    def test_empty_results_cached(self, cache: SearchCache):
        """Empty result lists are cached (DDG returned 0 results)."""
        cache.put("empty query", [])
        assert cache.get("empty query") == []

    def test_creates_directory(self, tmp_path: Path):
        """Cache creates its directory if it doesn't exist."""
        new_dir = tmp_path / "new" / "nested" / "cache"
        cache = SearchCache(cache_dir=new_dir)
        assert new_dir.exists()
        cache.put("q", [{"href": "x"}])
        assert cache.get("q") == [{"href": "x"}]
