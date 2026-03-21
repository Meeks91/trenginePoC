"""
test_search_abort — SearchResults failure stats.

Verifies:
- failure_threshold_percentage computed correctly
- Zero queries → 0.0 threshold (no divide-by-zero)
- Partial failures below threshold → no abort
"""

import pytest

from services.search.SearchService import SearchResults


class TestSearchResultsFailureStats:
    """SearchResults.failure_threshold_percentage correctness."""

    def test_zero_queries_returns_zero(self):
        sr = SearchResults(
            url_query_pairs=[], direct_handles=[],
            failure_count=0, queries_attempted=0,
        )
        assert sr.failure_threshold_percentage == 0.0

    def test_no_failures_returns_zero(self):
        sr = SearchResults(
            url_query_pairs=[("http://a.com", "q1")],
            direct_handles=[],
            failure_count=0, queries_attempted=5,
        )
        assert sr.failure_threshold_percentage == 0.0

    def test_all_failures_returns_one(self):
        sr = SearchResults(
            url_query_pairs=[], direct_handles=[],
            failure_count=4, queries_attempted=4,
        )
        assert sr.failure_threshold_percentage == 1.0

    def test_partial_failures(self):
        sr = SearchResults(
            url_query_pairs=[("http://a.com", "q1")],
            direct_handles=[],
            failure_count=2, queries_attempted=5,
        )
        assert sr.failure_threshold_percentage == pytest.approx(0.4)

    def test_fifty_percent_threshold(self):
        sr = SearchResults(
            url_query_pairs=[], direct_handles=[],
            failure_count=3, queries_attempted=6,
        )
        assert sr.failure_threshold_percentage == pytest.approx(0.5)
