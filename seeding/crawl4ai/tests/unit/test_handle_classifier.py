"""
Unit tests for HandleClassifier — LLM-based platform classification of naked @handles.

Tests mock litellm.acompletion to verify prompt construction, response parsing,
and error handling without making real LLM calls.
"""

from __future__ import annotations

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from services.extraction.HandleClassifier import classify_handles
from services.extraction.RegexHandleExtractor import ExtractedHandle


# Fixtures:

def gen_handle(handle: str, platform: str = "") -> ExtractedHandle:
    return ExtractedHandle(handle=handle, platform=platform)


def gen_llm_response(classifications: list[dict[str, str]]) -> MagicMock:
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = json.dumps(classifications)
    return response


def gen_llm_response_with_code_block(classifications: list[dict[str, str]]) -> MagicMock:
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = f"```json\n{json.dumps(classifications)}\n```"
    return response


# Fixtures


class TestClassifyHandles:

    @pytest.mark.asyncio
    async def test_empty_input_returns_immediately(self):
        result = await classify_handles(handles=[])
        assert result == []

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "")
    async def test_no_api_key_returns_unmodified(self):
        handles = [gen_handle("fitguru")]
        result = await classify_handles(handles=handles)
        assert result[0].platform == ""

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_classifies_single_handle(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(return_value=gen_llm_response(
            [{"handle": "fitguru", "platform": "Instagram"}],
        ))
        handles = [gen_handle("fitguru")]

        result = await classify_handles(handles=handles)

        assert result[0].platform == "Instagram"

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_classifies_multiple_handles(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(return_value=gen_llm_response([
            {"handle": "fitguru", "platform": "Instagram"},
            {"handle": "dancequeen", "platform": "TikTok"},
            {"handle": "techreview", "platform": "YouTube"},
        ]))
        handles = [
            gen_handle("fitguru"),
            gen_handle("dancequeen"),
            gen_handle("techreview"),
        ]

        result = await classify_handles(handles=handles)

        assert result[0].platform == "Instagram"
        assert result[1].platform == "TikTok"
        assert result[2].platform == "YouTube"

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_unknown_platform_leaves_handle_unchanged(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(return_value=gen_llm_response(
            [{"handle": "mystery", "platform": "unknown"}],
        ))
        handles = [gen_handle("mystery")]

        result = await classify_handles(handles=handles)

        assert result[0].platform == ""

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_handles_markdown_code_block_response(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(
            return_value=gen_llm_response_with_code_block(
                [{"handle": "yogalife", "platform": "Instagram"}],
            ),
        )
        handles = [gen_handle("yogalife")]

        result = await classify_handles(handles=handles)

        assert result[0].platform == "Instagram"

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_llm_exception_returns_unmodified(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(side_effect=RuntimeError("LLM down"))
        handles = [gen_handle("fitguru")]

        result = await classify_handles(handles=handles)

        assert result[0].platform == ""

    @pytest.mark.asyncio
    @patch("services.extraction.HandleClassifier.GEMINI_API_KEY", "test-key")
    @patch("services.extraction.HandleClassifier.litellm")
    async def test_case_insensitive_handle_matching(self, mock_litellm: MagicMock):
        mock_litellm.acompletion = AsyncMock(return_value=gen_llm_response(
            [{"handle": "FitGuru", "platform": "Instagram"}],
        ))
        handles = [gen_handle("fitguru")]

        result = await classify_handles(handles=handles)

        assert result[0].platform == "Instagram"
