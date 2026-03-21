"""
Unit Tests: LLMExtractionService
================================
Tests LLM extraction with mocked litellm.acompletion.
Verifies: token usage extraction, sampling, rate limiting, error handling.
"""

import asyncio
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock


from services.extraction.LLMExtractionService import LLMExtractionService
from services.audit.AuditService import AuditLog
from config.schema import PageResult


def _make_page(url="https://example.com/page", fit_markdown="## Top Influencers\n- Kayla Itsines @kayla_itsines\n- Joe Wicks"):
    """Create a mock PageResult."""
    return PageResult(
        url=url,
        query="fitness influencers",
        raw_markdown="<html>..." + fit_markdown,
        fit_markdown=fit_markdown,
        raw_token_estimate=len(fit_markdown) * 2 // 4,
        fit_token_estimate=len(fit_markdown) // 4,
        success=True,
    )


def _make_litellm_response(influencers_json: str, prompt_tokens=100, completion_tokens=50):
    """Create a mock litellm response object."""
    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens

    message = MagicMock()
    message.content = influencers_json

    choice = MagicMock()
    choice.message = message

    response = MagicMock()
    response.choices = [choice]
    response.usage = usage
    return response


def _raw_dir(tmp):
    """Create and return a raw/ dir inside the temp directory."""
    d = Path(tmp) / "raw"
    os.makedirs(d, exist_ok=True)
    return d


def test_extract_uses_actual_token_counts():
    """LLMExtractionService should return actual token counts from litellm response."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        page = _make_page()
        response_json = json.dumps({
            "influencers": [
                {"name": "Kayla Itsines", "handle": "@kayla_itsines"},
                {"name": "Joe Wicks", "handle": "@thebodycoach"},
            ]
        })
        mock_response = _make_litellm_response(response_json, prompt_tokens=500, completion_tokens=120)

        with (
            patch("services.extraction.LLMExtractionService.litellm") as mock_litellm,
            patch("services.extraction.LLMExtractionService.RAW_DIR", _raw_dir(tmp)),
        ):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)

            url_to_inf, in_tok, out_tok = asyncio.run(svc.extract(
                pages=[page],
                platform="Instagram",
                category_key="FITNESS",
                sub_name="Fitness",
                region="United States",
                year="2026",
            ))

        assert page.url in url_to_inf
        assert len(url_to_inf[page.url]) == 2
        assert url_to_inf[page.url][0].name == "Kayla Itsines"
        # Token counts should come from API response, not estimates
        assert in_tok == 500, f"Expected 500 input tokens from API, got {in_tok}"
        assert out_tok == 120, f"Expected 120 output tokens from API, got {out_tok}"


def test_extract_fallback_token_estimate():
    """When litellm response has no usage stats, should fall back to estimates."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        page = _make_page()
        response_json = json.dumps({
            "influencers": [
                {"name": "Jane Smith", "handle": "@test"},
            ]
        })
        # Create response WITHOUT usage stats
        mock_response = _make_litellm_response(response_json)
        mock_response.usage = None

        with (
            patch("services.extraction.LLMExtractionService.litellm") as mock_litellm,
            patch("services.extraction.LLMExtractionService.RAW_DIR", _raw_dir(tmp)),
        ):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)

            url_to_inf, in_tok, out_tok = asyncio.run(svc.extract(
                pages=[page],
                platform="Instagram",
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
            ))

        assert len(url_to_inf[page.url]) == 1
        # Fallback: input = fit_token_estimate, output = n_influencers * OUTPUT_TOKENS_PER_INFLUENCER
        assert in_tok == page.fit_token_estimate
        from config import OUTPUT_TOKENS_PER_INFLUENCER
        assert out_tok == 1 * OUTPUT_TOKENS_PER_INFLUENCER


def test_extract_sampling():
    """With sample_n, only N pages should be sent to LLM."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        pages = [_make_page(url=f"https://example.com/page{i}") for i in range(5)]
        response_json = json.dumps({"influencers": [{"name": "Test", "handle": "@test"}]})
        mock_response = _make_litellm_response(response_json, prompt_tokens=100, completion_tokens=20)

        with (
            patch("services.extraction.LLMExtractionService.litellm") as mock_litellm,
            patch("services.extraction.LLMExtractionService.RAW_DIR", _raw_dir(tmp)),
            patch("services.extraction.LLMExtractionService.LLM_DELAY_SECONDS", 0),
        ):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)

            url_to_inf, _, _ = asyncio.run(svc.extract(
                pages=pages,
                platform="Instagram",
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
                sample_n=2,
            ))

        # Only 2 pages should have been extracted
        assert mock_litellm.acompletion.call_count == 2
        assert len(url_to_inf) == 2


def test_extract_skips_failed_pages():
    """Failed pages should not be sent to LLM."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        pages = [
            _make_page(url="https://example.com/good"),
            PageResult(
                url="https://example.com/bad", query="test",
                raw_markdown="", fit_markdown="",
                raw_token_estimate=0, fit_token_estimate=0,
                success=False, error="timeout",
            ),
        ]
        response_json = json.dumps({"influencers": [{"name": "Test", "handle": "@test"}]})
        mock_response = _make_litellm_response(response_json, prompt_tokens=100, completion_tokens=20)

        with (
            patch("services.extraction.LLMExtractionService.litellm") as mock_litellm,
            patch("services.extraction.LLMExtractionService.RAW_DIR", _raw_dir(tmp)),
        ):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)

            url_to_inf, _, _ = asyncio.run(svc.extract(
                pages=pages,
                platform="Instagram",
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
            ))

        assert mock_litellm.acompletion.call_count == 1
        assert "https://example.com/good" in url_to_inf
        assert "https://example.com/bad" not in url_to_inf


def test_extract_empty_response():
    """Empty LLM response should return empty list for that page."""
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        page = _make_page()
        mock_response = _make_litellm_response("", prompt_tokens=100, completion_tokens=0)
        mock_response.choices[0].message.content = ""

        with (
            patch("services.extraction.LLMExtractionService.litellm") as mock_litellm,
            patch("services.extraction.LLMExtractionService.RAW_DIR", _raw_dir(tmp)),
        ):
            mock_litellm.acompletion = AsyncMock(return_value=mock_response)

            url_to_inf, _, _ = asyncio.run(svc.extract(
                pages=[page],
                platform="Instagram",
                category_key="FITNESS",
                sub_name="Fitness",
                region="US",
                year="2026",
            ))

        assert url_to_inf[page.url] == []


def test_extract_no_eligible_pages_returns_tuple():
    """Regression: extract() with zero eligible pages must return ({}, 0, 0).

    Previously returned bare {} which caused 'not enough values to unpack'
    when callers destructured as (dict, int, int).
    """
    with tempfile.TemporaryDirectory() as tmp:
        audit = AuditLog(Path(tmp), "test")
        svc = LLMExtractionService(audit)

        # All pages are failures — none eligible
        pages = [
            PageResult(
                url="https://example.com/fail1", query="test",
                raw_markdown="", fit_markdown="",
                raw_token_estimate=0, fit_token_estimate=0,
                success=False, error="timeout",
            ),
            PageResult(
                url="https://example.com/fail2", query="test",
                raw_markdown="content", fit_markdown="   ",  # whitespace-only
                raw_token_estimate=100, fit_token_estimate=50,
                success=True,
            ),
        ]

        url_to_inf, in_tok, out_tok = asyncio.run(svc.extract(
            pages=pages,
            platform="Instagram",
            category_key="FITNESS",
            sub_name="Fitness",
            region="US",
            year="2026",
        ))

        assert url_to_inf == {}, "Expected empty dict for no eligible pages"
        assert in_tok == 0, f"Expected 0 input tokens, got {in_tok}"
        assert out_tok == 0, f"Expected 0 output tokens, got {out_tok}"


# ── Regression: Shared NameCleaner ──

def test_name_cleaner_shared_by_both_parsers():
    """LLMResponseParser and NameExtractor must both use NameCleanerService.

    Old code defined cleanup logic independently. Now both import
    NameCleanerService for consistent name cleaning.
    """
    import services.extraction.LLMResponseParser as parser_mod
    import services.extraction.NameExtractor as extractor_mod

    assert hasattr(parser_mod, 'NameCleanerService'), (
        "LLMResponseParser must import NameCleanerService"
    )
    assert hasattr(extractor_mod, 'NameCleanerService'), (
        "NameExtractor must import NameCleanerService"
    )
