"""
Tests for StatsCollector
=========================
Unit tests for centralized pipeline metrics accumulation.
"""

from config.schema import PageResult
from services.reporting.StatsCollector import StatsCollector
from services.extraction.HandleExtractionService import HandleExtractionResult
from config.schema import Influencer, Platform


class TestRecordSearch:
    """Tests for StatsCollector.record_search()."""

    def test_accumulates_url_and_handle_counts(self):
        sc = StatsCollector()
        sc.record_search(url_count=10, direct_handle_count=3, retries=1, failures=0)
        assert sc.stats.urls_discovered == 13
        assert sc.stats.search_retries == 1
        assert sc.stats.search_failures == 0

    def test_accumulates_across_calls(self):
        sc = StatsCollector()
        sc.record_search(url_count=5, direct_handle_count=0, retries=0, failures=0)
        sc.record_search(url_count=3, direct_handle_count=2, retries=1, failures=1)
        assert sc.stats.urls_discovered == 10
        assert sc.stats.search_retries == 1
        assert sc.stats.search_failures == 1


class TestRecordCrawl:
    """Tests for StatsCollector.record_crawl()."""

    def _page(self, url, success=True):
        return PageResult(
            url=url, query="q", raw_markdown="", fit_markdown="",
            raw_token_estimate=0, fit_token_estimate=0, success=success,
        )

    def test_counts_successes_and_failures(self):
        sc = StatsCollector()
        pages = [
            self._page("https://a.com", success=True),
            self._page("https://b.com", success=True),
            self._page("https://c.com", success=False),
        ]
        sc.record_crawl(pages)
        assert sc.stats.pages_crawled == 2
        assert sc.stats.pages_failed == 1


class TestRecordExtraction:
    """Tests for StatsCollector.record_extraction()."""

    def test_records_from_extraction_result(self):
        sc = StatsCollector()
        result = HandleExtractionResult(
            regex_handles=[],
            llm_handles={
                "https://a.com": [Influencer(name="A")],
                "https://b.com": [],  # empty = not counted as extracted
            },
            all_merged=[Influencer(name="A"), Influencer(name="B")],
            llm_input_tokens=1000,
            llm_output_tokens=200,
        )
        sc.record_extraction(result)
        assert sc.stats.pages_extracted == 1  # only non-empty
        assert sc.stats.influencers_raw == 2
        assert sc.stats.total_input_tokens == 1000
        assert sc.stats.total_output_tokens == 200

    def test_tracks_regex_handles_total(self):
        sc = StatsCollector()
        result = HandleExtractionResult(
            regex_handles=[
                Influencer(name="A", handles={Platform.Instagram: "a_handle"}),
                Influencer(name="B", handles={Platform.TikTok: "b_handle"}),
                Influencer(name="C", handles={Platform.YouTube: "c_handle"}),
            ],
            llm_handles={},
            all_merged=[],
            llm_input_tokens=0,
            llm_output_tokens=0,
        )
        sc.record_extraction(result)
        assert sc.stats.regex_handles_total == 3

    def test_regex_handles_accumulates_across_calls(self):
        sc = StatsCollector()
        for count in [5, 3, 7]:
            result = HandleExtractionResult(
                regex_handles=[Influencer(name=f"I{i}") for i in range(count)],
                llm_handles={},
                all_merged=[],
                llm_input_tokens=0,
                llm_output_tokens=0,
            )
            sc.record_extraction(result)
        assert sc.stats.regex_handles_total == 15


class TestRecordEnrichment:
    """Tests for StatsCollector.record_enrichment()."""

    def test_records_enrichment_metrics(self):
        sc = StatsCollector()
        sc.record_enrichment(
            unique_count=8, handles_filled=6, retries=2, failures=1,
        )
        assert sc.stats.influencers_deduped == 8
        assert sc.stats.handles_filled == 6
        assert sc.stats.enrich_retries == 2
        assert sc.stats.enrich_failures == 1


class TestCheckYieldWarnings:
    """Tests for StatsCollector.check_yield_warnings()."""

    def test_no_warning_when_yield_is_healthy(self):
        sc = StatsCollector()
        sc.stats.pages_crawled = 100
        sc.stats.regex_handles_total = 1000  # 10.0 handles/page
        warnings = sc.check_yield_warnings()
        assert warnings == []

    def test_warning_when_yield_below_threshold(self):
        sc = StatsCollector()
        sc.stats.pages_crawled = 100
        sc.stats.regex_handles_total = 50  # 0.5 handles/page
        warnings = sc.check_yield_warnings()
        assert len(warnings) == 1
        assert "LOW YIELD" in warnings[0]
        assert "0.5" in warnings[0]

    def test_no_warning_at_exact_threshold(self):
        sc = StatsCollector()
        sc.stats.pages_crawled = 100
        sc.stats.regex_handles_total = 200  # 2.0 handles/page = threshold
        warnings = sc.check_yield_warnings()
        assert warnings == []

    def test_empty_when_zero_pages(self):
        sc = StatsCollector()
        sc.stats.pages_crawled = 0
        warnings = sc.check_yield_warnings()
        assert warnings == []


class TestInitialState:
    """Verify clean initial state."""

    def test_starts_at_zero(self):
        sc = StatsCollector()
        assert sc.stats.urls_discovered == 0
        assert sc.stats.pages_crawled == 0
        assert sc.stats.influencers_raw == 0
        assert sc.stats.regex_handles_total == 0
        assert sc.validation_results == {}
