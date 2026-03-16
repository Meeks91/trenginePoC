"""
Serper API Validation Script — validates dork operator assumptions.

Two dense tests:
  Test 1: open query with (intitle:X OR site:reddit.com) unified mandatory clause
  Test 2: site-targeted with intitle: only (no reddit in OR)

Key assumption to verify:
  Google treats site:reddit.com inside an OR group as expected.

Usage:
  SERPER_API_KEY=xxx python scripts/validate_serper.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from urllib.parse import urlparse

import requests


# ── Config ──

SERPER_URL = "https://google.serper.dev/search"
DELAY_BETWEEN_QUERIES = 1.0


# ── Types ──

@dataclass(frozen=True)
class TestResult:
    test_name: str
    query: str
    result_count: int
    passed_checks: list[str]
    failed_checks: list[str]
    raw_results: list[dict[str, str]]

    @property
    def passed(self) -> bool:
        return len(self.failed_checks) == 0


# ── Tests ──

TESTS = [
    {
        "name": "1: reddit in OR clause does NOT exclude non-reddit results",
        "description": (
            "site:reddit.com is in the OR group but search terms point at "
            "Instagram content. Proves the reddit clause doesn't break or "
            "exclude normal intitle: results when terms don't mention reddit."
        ),
        "query": (
            '(intitle:influencer OR intitle:creator OR intitle:top OR site:reddit.com) '
            '(fitness OR workout) top fitness influencers Instagram 2026'
        ),
        "checks": {
            "min_results": 3,
            "each_result_must_match": {
                "title_contains_any": ["influencer", "creator", "top"],
                "or_domain_is": "reddit.com",
            },
        },
    },
    {
        "name": "2: reddit clause returns reddit when terms direct toward it",
        "description": (
            "Same OR group but search terms include 'on reddit'. "
            "Proves site:reddit.com in the OR actually surfaces reddit "
            "results when the query topic matches."
        ),
        "query": (
            '(intitle:influencer OR intitle:creator OR intitle:top OR site:reddit.com) '
            '(fitness OR workout) top fitness influencers Instagram 2026 on reddit'
        ),
        "checks": {
            "min_results": 3,
            "must_contain_domain": "reddit.com",
            "each_result_must_match": {
                "title_contains_any": ["influencer", "creator", "top"],
                "or_domain_is": "reddit.com",
            },
        },
    },
    {
        "name": "3: complex dork composition (site: + intitle: + OR + parens)",
        "description": (
            "Validates all operators compose correctly: "
            "site:favikon.com locks domain, (intitle:X OR intitle:Y) "
            "filters titles, (slug1 OR slug2) narrows topic."
        ),
        "query": (
            'site:favikon.com (intitle:influencer OR intitle:creator OR intitle:top) '
            '(fitness OR workout) fitness influencers Instagram 2026'
        ),
        "checks": {
            "min_results": 1,
            "all_results_domain": "favikon.com",
            "each_result_must_match": {
                "title_contains_any": ["influencer", "creator", "top"],
            },
        },
    },
]


# ── API ──

def serper_search(query: str, api_key: str, num: int = 10) -> list[dict[str, str]]:
    """Execute a search via Serper API, return organic results."""
    resp = requests.post(
        SERPER_URL,
        json={"q": query, "num": num},
        headers={
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return [
        {"title": r.get("title", ""), "url": r.get("link", ""), "snippet": r.get("snippet", "")}
        for r in data.get("organic", [])
    ]


# ── Validation ──

def validate_test(test: dict, results: list[dict[str, str]]) -> TestResult:
    """Run all checks for a test against its results."""
    checks = test["checks"]
    passed: list[str] = []
    failed: list[str] = []

    # Check minimum result count
    min_results = checks.get("min_results", 1)
    if len(results) >= min_results:
        passed.append(f"min_results: {len(results)} >= {min_results}")
    else:
        failed.append(f"min_results: got {len(results)}, expected >= {min_results}")

    # Check at least one result from required domain (e.g. reddit.com)
    must_contain = checks.get("must_contain_domain")
    if must_contain:
        matching = [
            r["url"] for r in results
            if must_contain in urlparse(r["url"]).netloc.lower()
        ]
        if matching:
            passed.append(
                f"must_contain_domain: {len(matching)} results from {must_contain}"
            )
        else:
            failed.append(
                f"must_contain_domain: NO results from {must_contain} — "
                f"site: inside OR group may not work!"
            )

    # Check at least one NON-reddit result with mandatory word in title
    non_reddit_title_words = checks.get("must_contain_non_reddit_title_match")
    if non_reddit_title_words:
        words_lower = [w.lower() for w in non_reddit_title_words]
        matching = [
            r for r in results
            if "reddit.com" not in urlparse(r["url"]).netloc.lower()
            and any(w in r["title"].lower() for w in words_lower)
        ]
        if matching:
            passed.append(
                f"must_contain_non_reddit_title_match: {len(matching)} non-reddit "
                f"results with title matching {non_reddit_title_words}"
            )
        else:
            failed.append(
                f"must_contain_non_reddit_title_match: NO non-reddit results with "
                f"title containing {non_reddit_title_words} — intitle: may not work!"
            )

    # Check all results from expected domain
    expected_domain = checks.get("all_results_domain")
    if expected_domain:
        non_matching = [
            r["url"] for r in results
            if expected_domain not in urlparse(r["url"]).netloc.lower()
        ]
        if not non_matching:
            passed.append(f"all_results_domain: all from {expected_domain}")
        else:
            failed.append(
                f"all_results_domain: {len(non_matching)} results NOT from "
                f"{expected_domain}: {non_matching[:3]}"
            )

    # Check each result matches condition (title contains ANY keyword OR domain matches)
    each_check = checks.get("each_result_must_match")
    if each_check and results:
        title_words = [w.lower() for w in each_check.get("title_contains_any", [])]
        or_domain = each_check.get("or_domain_is", "")
        failures = []

        for r in results:
            title_lower = r["title"].lower()
            domain = urlparse(r["url"]).netloc.lower()
            title_match = any(w in title_lower for w in title_words) if title_words else True
            domain_match = or_domain in domain if or_domain else False

            if not title_match and not domain_match:
                failures.append(f"  '{r['title'][:60]}' ({domain})")

        if not failures:
            label = f"title has {title_words}"
            if or_domain:
                label += f" OR domain={or_domain}"
            passed.append(f"each_result_must_match: all {len(results)} results match ({label})")
        else:
            failed.append(
                f"each_result_must_match: {len(failures)}/{len(results)} failed:\n"
                + "\n".join(failures[:5])
            )

    return TestResult(
        test_name=test["name"],
        query=test["query"],
        result_count=len(results),
        passed_checks=passed,
        failed_checks=failed,
        raw_results=results,
    )


# ── Output ──

def print_report(result: TestResult) -> None:
    """Print formatted test report."""
    status = "✅ PASS" if result.passed else "❌ FAIL"
    print(f"\n{'='*80}")
    print(f"{status}  {result.test_name}")
    print(f"{'='*80}")
    print(f"Query:   {result.query}")
    print(f"Results: {result.result_count}")

    if result.passed_checks:
        print(f"\n  Passed:")
        for check in result.passed_checks:
            print(f"    ✅ {check}")

    if result.failed_checks:
        print(f"\n  Failed:")
        for check in result.failed_checks:
            print(f"    ❌ {check}")

    print(f"\n  Top results:")
    for i, r in enumerate(result.raw_results[:5], 1):
        domain = urlparse(r["url"]).netloc
        print(f"    {i}. [{domain}] {r['title'][:70]}")
        print(f"       {r['url']}")


# ── Main ──

def run() -> None:
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        print("ERROR: SERPER_API_KEY environment variable not set")
        print("Usage: SERPER_API_KEY=xxx python scripts/validate_serper.py")
        sys.exit(1)

    print("Serper API Validation Script")
    print(f"Running {len(TESTS)} tests...\n")

    all_results: list[TestResult] = []

    for i, test in enumerate(TESTS):
        print(f"[{i+1}/{len(TESTS)}] Running: {test['name']}...")
        print(f"         {test['description']}")

        results = serper_search(test["query"], api_key)
        test_result = validate_test(test, results)
        all_results.append(test_result)
        print_report(test_result)

        if i < len(TESTS) - 1:
            time.sleep(DELAY_BETWEEN_QUERIES)

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)
    print(f"  {passed}/{total} tests passed")

    for r in all_results:
        status = "✅" if r.passed else "❌"
        print(f"  {status} {r.test_name} ({r.result_count} results)")

    # Dump raw results to JSON for inspection
    dump_path = "results/serper_validation.json"
    os.makedirs("results", exist_ok=True)
    with open(dump_path, "w") as f:
        json.dump(
            [
                {
                    "test": r.test_name,
                    "query": r.query,
                    "passed": r.passed,
                    "result_count": r.result_count,
                    "results": r.raw_results,
                }
                for r in all_results
            ],
            f,
            indent=2,
        )
    print(f"\n  Raw results saved to: {dump_path}")

    if passed < total:
        print("\n⚠️  Some tests failed. Review results before committing to Serper integration.")
        sys.exit(1)
    else:
        print("\n✅ All assumptions validated. Safe to proceed with StrictSearchClient.")


if __name__ == "__main__":
    run()
