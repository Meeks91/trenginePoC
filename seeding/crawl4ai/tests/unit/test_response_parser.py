"""
Unit Tests: LLMResponseParser
============================
Verifies LLM JSON response parsing into Influencer[].
Includes handle validation tests (invalid handles cleared, not rejected).
"""


from config.schema import Platform
from services.extraction.LLMResponseParser import LLMResponseParser


def test_parse_standard_response():
    """Standard response: {"influencers": [...]}."""
    json_str = '{"influencers": [{"name": "Kayla Itsines", "handle": "@kayla_itsines"}, {"name": "Joe Wicks", "handle": ""}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 2
    assert result[0].name == "Kayla Itsines"
    assert result[0].handles.get(Platform.Instagram) == "kayla_itsines"  # @ prefix stripped
    assert result[1].name == "Joe Wicks"
    assert not result[1].handles  # empty handle → empty handles dict


def test_parse_chunked_response():
    """Chunked response: [{"influencers": [...]}, {"influencers": [...]}]."""
    json_str = '[{"influencers": [{"name": "Alex Beattie", "handle": "@a_handle"}]}, {"influencers": [{"name": "Ben Carter", "handle": "@b_handle"}]}]'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 2
    assert result[0].name == "Alex Beattie"
    assert result[1].name == "Ben Carter"


def test_parse_direct_list():
    """Direct list: [{"name": "...", "handle": "..."}, ...]."""
    json_str = '[{"name": "Alex Yale", "handle": "@x_user"}, {"name": "Mark Jensen", "handle": "@y_user"}]'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 2


def test_parse_invalid_json():
    """Should return empty list on invalid JSON."""
    result = LLMResponseParser.parse("not json at all")
    assert result == []


def test_parse_empty_names_skipped():
    """Influencers with empty names should be skipped."""
    json_str = '{"influencers": [{"name": "", "handle": "@ghost"}, {"name": "Anna Thompson", "handle": "@real"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Anna Thompson"


def test_parse_error_responses_ignored():
    """Error responses in chunked list should be ignored."""
    json_str = '[{"error": true, "content": "rate limit"}, {"influencers": [{"name": "James Knox", "handle": "@ok_handle"}]}]'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "James Knox"


def test_parse_strips_whitespace():
    """Names and handles should be stripped of whitespace."""
    json_str = '{"influencers": [{"name": "  Sarah Green  ", "handle": "  @padded  "}]}'
    result = LLMResponseParser.parse(json_str)
    assert result[0].name == "Sarah Green"
    assert result[0].handles.get(Platform.Instagram) == "padded"  # @ stripped + whitespace stripped


def test_parse_handle_platform_propagated():
    """handle_platform from LLM output should be propagated to handles dict."""
    json_str = '{"influencers": [{"name": "Adam Maxted", "handle": "adammaxted2262", "handle_platform": "YouTube"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Adam Maxted"
    assert Platform.YouTube in result[0].handles
    assert result[0].handles[Platform.YouTube] == "adammaxted2262"


def test_parse_handle_platform_defaults_empty():
    """handle_platform defaults to Instagram when not provided by LLM."""
    json_str = '{"influencers": [{"name": "Kayla Itsines", "handle": "@kayla_itsines"}]}'
    result = LLMResponseParser.parse(json_str)
    # Without handle_platform, default mapping uses Instagram
    assert Platform.Instagram in result[0].handles
    assert result[0].handles[Platform.Instagram] == "kayla_itsines"


# ══════════════════════════════════════════════════════════════════════
# Handle Validation in LLMResponseParser
# ══════════════════════════════════════════════════════════════════════

def test_parse_invalid_handle_cleared():
    """LLM returns a blocklisted handle → handle cleared, influencer kept."""
    json_str = '{"influencers": [{"name": "Emma Clark", "handle": "explore"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Emma Clark"
    assert not result[0].handles  # Invalid handle cleared → empty dict


def test_parse_css_atrule_handle_cleared():
    """LLM returns CSS at-rule as handle → cleared."""
    json_str = '{"influencers": [{"name": "Tom Bradley", "handle": "@context"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert not result[0].handles


def test_parse_numeric_handle_cleared():
    """LLM returns pure numeric handle (post ID) → cleared."""
    json_str = '{"influencers": [{"name": "Jack Porter", "handle": "1234567890"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert not result[0].handles


def test_parse_short_handle_cleared():
    """LLM returns single character handle → cleared."""
    json_str = '{"influencers": [{"name": "Lisa Short", "handle": "x"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert not result[0].handles


def test_parse_valid_handle_kept():
    """Valid handle passes through validation."""
    json_str = '{"influencers": [{"name": "Kayla Itsines", "handle": "kayla_itsines"}]}'
    result = LLMResponseParser.parse(json_str)
    assert result[0].handles.get(Platform.Instagram) == "kayla_itsines"


def test_parse_consecutive_dots_cleared():
    """Handle with consecutive dots → cleared (lorey rule)."""
    json_str = '{"influencers": [{"name": "Dorothy Mills", "handle": "bad..handle"}]}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert not result[0].handles


def test_parse_at_prefix_stripped():
    """@ prefix in LLM-returned handle should be stripped."""
    json_str = '{"influencers": [{"name": "Anna Thompson", "handle": "@real_handle"}]}'
    result = LLMResponseParser.parse(json_str)
    assert result[0].handles.get(Platform.Instagram) == "real_handle"


# ══════════════════════════════════════════════════════════════════════
# Blocklist on LLM-extracted names (item 1c)
# ══════════════════════════════════════════════════════════════════════

def test_parse_blocks_ai_company_names():
    """AI company names (ChatGPT, Midjourney) should be filtered from LLM output."""
    json_str = '{"influencers": [' \
        '{"name": "ChatGPT", "handle": "chatopenai", "handle_platform": "YouTube"},' \
        '{"name": "Midjourney", "handle": "midjourneyartwork", "handle_platform": "Instagram"},' \
        '{"name": "Sam Wilson", "handle": "real_person"}' \
    ']}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Sam Wilson"


def test_parse_blocks_spaced_company_names():
    """Multi-word company names like 'Meta AI' should be blocked (spaces removed for matching)."""
    json_str = '{"influencers": [' \
        '{"name": "Meta AI", "handle": "metademolab"},' \
        '{"name": "Inworld AI", "handle": "inworldai"},' \
        '{"name": "Kayla Itsines", "handle": "kayla_itsines"}' \
    ']}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Kayla Itsines"


def test_parse_blocks_brand_names():
    """Well-known brand names should be filtered from LLM output."""
    json_str = '{"influencers": [' \
        '{"name": "Nike", "handle": "nike"},' \
        '{"name": "Gymshark", "handle": "gymshark"},' \
        '{"name": "Jeff Nippard", "handle": "jeffnippard"}' \
    ']}'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Jeff Nippard"


# ══════════════════════════════════════════════════════════════════════
# Markdown fence stripping
# ══════════════════════════════════════════════════════════════════════

def test_parse_markdown_fenced_json():
    """LLM responses wrapped in ```json ... ``` should be parsed correctly."""
    json_str = '```json\n{"influencers": [{"name": "Kayla Itsines", "handle": "kayla_itsines"}]}\n```'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Kayla Itsines"


def test_parse_markdown_fenced_plain():
    """LLM responses wrapped in ``` ... ``` (no language) should also work."""
    json_str = '```\n{"influencers": [{"name": "Joe Wicks", "handle": "thebodycoach"}]}\n```'
    result = LLMResponseParser.parse(json_str)
    assert len(result) == 1
    assert result[0].name == "Joe Wicks"

