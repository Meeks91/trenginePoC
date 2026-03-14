"""
Unit Tests: QueryBuilder
=========================
Verifies search query generation from seed config.

Formula per leaf:
  perms = 1 primary + len(altSearchTerms) alt + len(knownSources) site-targeted
"""

from config.seed_schema import Difficulty
from services.search.QueryBuilder import QueryBuilder, QueryType


def _build(*, sub_name="Fitness", platform="Instagram", region="US", year="2026",
           search_prompt="top fitness influencers", alt_search_terms=None,
           known_sources=None, difficulty=Difficulty.EASY, inurl_slugs=None):
    """Helper to construct QueryBuilder with defaults."""
    return QueryBuilder(
        sub_name=sub_name,
        platform=platform,
        region=region,
        year=year,
        search_prompt=search_prompt,
        alt_search_terms=alt_search_terms or [],
        known_sources=known_sources or [],
        difficulty=difficulty,
        inurl_slugs=inurl_slugs or [],
    )


# ── Existing tests (Easy mode — no inurl:) ──────────────────────────────────

def test_all_query_types_generated():
    """All 3 query types should be generated."""
    qb = _build(
        alt_search_terms=["best gym creators", "powerlifting accounts"],
        known_sources=["favikon.com", "modash.io"],
    )
    queries = qb.build_all()
    types = {q.query_type for q in queries}

    assert "site_targeted" in types, "Missing site_targeted queries"
    assert "primary_open" in types, "Missing primary_open queries"
    assert "alt_open" in types, "Missing alt_open queries"
    assert "discovery" not in types, "Discovery queries should be removed"
    assert len(queries) == 5


def test_year_in_all_queries():
    """Every query should include the year."""
    qb = _build(sub_name="Cooking", platform="TikTok", region="UK",
                search_prompt="best cooking creators",
                alt_search_terms=["recipe tiktok"], known_sources=["favikon.com"])
    for q in qb.build_all():
        assert "2026" in q.query, f"Year missing from query: {q.query}"


def test_site_targeted_uses_known_sources():
    """Site-targeted queries: 1 per source (primary search prompt only)."""
    qb = _build(
        search_prompt="fitness influencers",
        known_sources=["favikon.com", "modash.io"],
    )
    site_queries = [q for q in qb.build_all() if q.query_type == QueryType.SITE_TARGETED]
    assert len(site_queries) == 2
    assert any("site:favikon.com" in q.query for q in site_queries)
    assert any("site:modash.io" in q.query for q in site_queries)
    for q in site_queries:
        assert "fitness influencers" in q.query


def test_site_targeted_includes_platform():
    """Site-targeted queries should include platform name."""
    qb = _build(sub_name="Beauty", platform="TikTok", region="UK",
                search_prompt="top beauty influencers",
                known_sources=["modash.io"])
    site_queries = [q for q in qb.build_all() if q.query_type == QueryType.SITE_TARGETED]
    assert len(site_queries) == 1
    assert "TikTok" in site_queries[0].query


def test_all_alt_terms_used():
    """Every alt_search_term should generate a query."""
    alt_terms = ["gym creators", "powerlifting", "crossfit", "bodybuilding", "calisthenics"]
    qb = _build(search_prompt="fitness influencers", alt_search_terms=alt_terms)
    alt_queries = [q for q in qb.build_all() if q.query_type == QueryType.ALT_OPEN]
    assert len(alt_queries) == 5


def test_empty_sources():
    """Should work with no known sources."""
    qb = _build(search_prompt="fitness influencers", alt_search_terms=["gym"])
    queries = qb.build_all()
    site_queries = [q for q in queries if q.query_type == QueryType.SITE_TARGETED]
    assert len(site_queries) == 0
    assert len(queries) == 2


def test_query_count_formula():
    """Verify the formula: 1 primary + len(alt) + len(sources) = total."""
    qb = _build(sub_name="Test", search_prompt="test prompt",
                alt_search_terms=["a", "b", "c"],
                known_sources=["x.com", "y.com", "z.com", "w.com"])
    queries = qb.build_all()
    assert len(queries) == 8  # 1 + 3 + 4


def test_execution_order():
    """Queries should be: primary first, then alt, then site-targeted."""
    qb = _build(search_prompt="fitness influencers",
                alt_search_terms=["alt1"], known_sources=["source.com"])
    types = [q.query_type for q in qb.build_all()]
    assert types == ["primary_open", "alt_open", "site_targeted"]


def test_realistic_fitness_count():
    """Realistic FITNESS sub: 3 alt terms, 10 sources = 14 queries per leaf."""
    qb = _build(
        alt_search_terms=[
            "favorite fitness creators",
            "top fitness accounts",
            "most popular fitness influencers",
        ],
        known_sources=[f"source{i}.com" for i in range(10)],
    )
    queries = qb.build_all()
    assert len(queries) == 14


# ── Strict mode (inurl: DDG operator) ────────────────────────────────────────

def test_strict_inurl_ddg_operator_single_slug():
    """Medium + single slug → inurl: in all 3 query types."""
    qb = _build(sub_name="AI", search_prompt="top AI influencers",
                alt_search_terms=["ai creators"],
                known_sources=["favikon.com"],
                difficulty=Difficulty.MEDIUM, inurl_slugs=["ai"])
    for q in qb.build_all():
        assert "inurl:ai" in q.query, f"Missing inurl:ai in: {q.query}"


def test_strict_inurl_ddg_operator_or_clause():
    """Medium + multiple slugs → inurl:x OR inurl:y in all queries."""
    qb = _build(sub_name="Protein / Macros", search_prompt="top protein influencers",
                alt_search_terms=["macro tracking"],
                known_sources=["favikon.com"],
                difficulty=Difficulty.MEDIUM, inurl_slugs=["protein", "macros"])
    for q in qb.build_all():
        assert "inurl:protein OR inurl:macros" in q.query, \
            f"Missing OR clause in: {q.query}"


def test_easy_no_inurl_ddg_operator():
    """Easy → no inurl: in any query, even if slugs are provided."""
    qb = _build(search_prompt="fitness influencers",
                alt_search_terms=["gym"],
                known_sources=["modash.io"],
                difficulty=Difficulty.EASY, inurl_slugs=["fitness"])
    for q in qb.build_all():
        assert "inurl:" not in q.query, f"Unexpected inurl: in: {q.query}"


def test_hard_inurl_ddg_operator():
    """Hard difficulty also activates inurl:."""
    qb = _build(sub_name="AI Coding / Dev Tools",
                search_prompt="top AI coding influencers",
                known_sources=["favikon.com"],
                difficulty=Difficulty.HARD, inurl_slugs=["ai", "coding", "dev", "tools"])
    for q in qb.build_all():
        assert "inurl:" in q.query


def test_site_targeted_inurl_position():
    """In site-targeted queries, inurl: appears after site:{source}."""
    qb = _build(sub_name="AI", search_prompt="top AI influencers",
                known_sources=["favikon.com"],
                difficulty=Difficulty.MEDIUM, inurl_slugs=["ai"])
    site_q = [q for q in qb.build_all() if q.query_type == QueryType.SITE_TARGETED][0]
    # site: should come before inurl:
    assert site_q.query.index("site:") < site_q.query.index("inurl:")


def test_all_three_query_types_fire_in_strict():
    """Strict mode does NOT skip any query type — all 3 always fire."""
    qb = _build(search_prompt="test", alt_search_terms=["alt"],
                known_sources=["x.com"],
                difficulty=Difficulty.HARD, inurl_slugs=["test"])
    types = {q.query_type for q in qb.build_all()}
    assert types == {"primary_open", "alt_open", "site_targeted"}


def test_empty_inurl_slugs_no_clause():
    """Empty slugs → no inurl: even for non-Easy."""
    qb = _build(difficulty=Difficulty.MEDIUM, inurl_slugs=[],
                known_sources=["x.com"], alt_search_terms=["alt"])
    for q in qb.build_all():
        assert "inurl:" not in q.query
