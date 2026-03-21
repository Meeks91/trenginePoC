"""
test_base_search_loop — _search_all_configs threshold + kill switch.

Verifies:
- Configs exceeding failure threshold produce ErroredConfig outcomes
- Consecutive failures trigger kill switch
- Successful search resets consecutive counter
- Killed configs get ErroredConfig with reason
- _on_config_search_finished only called for successful configs
"""

import asyncio


from config.schema import Platform
from config.seed_schema import (
    SeedJob, SubCategory, Region, RegionCode, Difficulty,
)
from config.settings import DDG_KILL_AFTER_N
from base_pipeline import BasePipelineRunner
from services.search.SearchService import SearchResults


# ── Fixtures ──

def _make_job(sub_name: str = "Test") -> SeedJob:
    sub = SubCategory(
        sub_name=sub_name, is_top_level=True, search_prompt="test",
        alt_search_terms=[], known_sources=[], platform_notes="",
        region_notes="", difficulty=Difficulty.EASY, strict_slugs=[],
    )
    region = Region(code=RegionCode.US, language="en", label="US")
    return SeedJob(
        category_key="TEST", sub=sub,
        platform=Platform.Instagram, region=region,
    )


def _success_results() -> SearchResults:
    return SearchResults(
        url_query_pairs=[("http://a.com", "q")],
        direct_handles=[],
        failure_count=0, queries_attempted=5,
    )


def _failing_results(failures: int = 4, attempted: int = 5) -> SearchResults:
    return SearchResults(
        url_query_pairs=[],
        direct_handles=[],
        failure_count=failures, queries_attempted=attempted,
    )


class StubSearchRunner(BasePipelineRunner):
    """Concrete stub that allows injecting search results per-config."""

    def __init__(self, search_results_sequence: list[SearchResults], **kwargs):
        super().__init__(**kwargs)
        self._search_sequence = list(search_results_sequence)
        self._search_index = 0
        self.configs_finished: list[str] = []

    async def _search_and_extract_influencers(self, jobs):
        raise NotImplementedError("Not used — test calls _search_all_configs directly")

    async def _on_config_search_finished(self, job, search_results):
        self.configs_finished.append(
            f"{job.category_key}/{job.sub.sub_name}"
        )

    def _search_one_config(self, job, config_key, index, total):
        result = self._search_sequence[self._search_index]
        self._search_index += 1
        return result


class TestSearchAllConfigsThreshold:

    def test_successful_search_no_error(self):
        runner = StubSearchRunner(
            search_results_sequence=[_success_results()],
            name_resolution=False,
        )
        outcomes = asyncio.run(runner._search_all_configs([_make_job()]))
        assert len(outcomes) == 1
        assert outcomes[0].errored is None
        assert len(runner.configs_finished) == 1

    def test_failing_search_produces_errored_config(self):
        runner = StubSearchRunner(
            search_results_sequence=[_failing_results()],
            name_resolution=False,
        )
        outcomes = asyncio.run(runner._search_all_configs([_make_job()]))
        assert len(outcomes) == 1
        assert outcomes[0].errored is not None
        assert outcomes[0].errored.failure_count == 4
        assert len(runner.configs_finished) == 0

    def test_success_resets_consecutive_counter(self):
        """Fail, then succeed, then fail — should NOT trigger kill switch."""
        runner = StubSearchRunner(
            search_results_sequence=[
                _failing_results(),
                _success_results(),
                _failing_results(),
            ],
            name_resolution=False,
        )
        jobs = [_make_job(f"Sub{i}") for i in range(3)]
        outcomes = asyncio.run(runner._search_all_configs(jobs))

        errored = [o for o in outcomes if o.errored]
        success = [o for o in outcomes if not o.errored]
        assert len(errored) == 2
        assert len(success) == 1
        assert len(runner.configs_finished) == 1

    def test_kill_switch_triggers_after_n_consecutive(self):
        n = DDG_KILL_AFTER_N
        total_jobs = n + 2
        runner = StubSearchRunner(
            search_results_sequence=[_failing_results()] * n,
            name_resolution=False,
        )
        jobs = [_make_job(f"Sub{i}") for i in range(total_jobs)]
        outcomes = asyncio.run(runner._search_all_configs(jobs))

        assert len(outcomes) == total_jobs
        errored = [o for o in outcomes if o.errored]
        assert len(errored) == total_jobs

        killed_configs = [o for o in outcomes if o.search_results is None]
        assert len(killed_configs) == total_jobs - n
        for o in killed_configs:
            assert "DDG killed" in o.errored.reason

    def test_on_config_search_finished_not_called_for_errors(self):
        runner = StubSearchRunner(
            search_results_sequence=[_failing_results()],
            name_resolution=False,
        )
        asyncio.run(runner._search_all_configs([_make_job()]))
        assert len(runner.configs_finished) == 0

    def test_below_min_queries_not_errored(self):
        """Fewer than DDG_FAILURE_MIN_QUERIES → never error regardless of rate."""
        sr = SearchResults(
            url_query_pairs=[], direct_handles=[],
            failure_count=2, queries_attempted=2,
        )
        runner = StubSearchRunner(
            search_results_sequence=[sr],
            name_resolution=False,
        )
        outcomes = asyncio.run(runner._search_all_configs([_make_job()]))
        assert outcomes[0].errored is None
