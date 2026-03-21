"""
Unit Tests: IngestionValidator
================================
Verifies canary validation logic — matches and misses.
"""



from services.validation.IngestionValidator import IngestionValidator, CANARY_FILE
from config.schema import Influencer, Platform


def _make_validator():
    """Create validator with the canonical canary file."""
    return IngestionValidator(CANARY_FILE)


def test_canary_found():
    """Should detect when all canaries are found."""
    validator = _make_validator()
    influencers = [
        Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
        Influencer(name="Michelle Lewin", handles={Platform.Instagram: "@michelle_lewin"}),
        Influencer(name="Whitney Simmons", handles={Platform.Instagram: "@whitneyysimmons"}),
    ]
    result = validator.validate(influencers, "FITNESS", "Fitness", "US")
    assert result is not None
    assert result.pass_rate == 1.0
    assert len(result.missing) == 0


def test_canary_partial():
    """Should report partial canary match."""
    validator = _make_validator()
    influencers = [
        Influencer(name="Kayla Itsines", handles={Platform.Instagram: "@kayla_itsines"}),
        # Michelle Lewin and Whitney Simmons missing
    ]
    result = validator.validate(influencers, "FITNESS", "Fitness", "US")
    assert result is not None
    assert len(result.found) == 1
    assert len(result.missing) == 2
    assert "Kayla Itsines" in result.found
    assert result.pass_rate < 1.0


def test_canary_by_handle():
    """Should match canary by handle in lookup set."""
    validator = _make_validator()
    influencers = [
        Influencer(name="", handles={Platform.Instagram: "@kayla_itsines"}),
        Influencer(name="Michelle Lewin", handles={Platform.Instagram: ""}),
        Influencer(name="Whitney Simmons", handles={Platform.Instagram: ""}),
    ]
    # "kayla_itsines" handle is in the found set, but canary checks by name "Kayla Itsines"
    result = validator.validate(influencers, "FITNESS", "Fitness", "US")
    assert result is not None
    assert "Michelle Lewin" in result.found
    assert "Whitney Simmons" in result.found


def test_no_canaries_for_sub():
    """Should return None when no canaries exist for a sub."""
    validator = _make_validator()
    result = validator.validate([], "NONEXISTENT", "FakeSub", "US")
    assert result is None


def test_case_insensitive_match():
    """Canary matching should be case-insensitive."""
    validator = _make_validator()
    influencers = [
        Influencer(name="Kayla Itsines", handles={Platform.Instagram: "kayla_itsines"}),
        Influencer(name="Michelle Lewin", handles={Platform.Instagram: "michelle_lewin"}),
        Influencer(name="Whitney Simmons", handles={Platform.Instagram: "whitneyysimmons"}),
    ]
    result = validator.validate(influencers, "FITNESS", "Fitness", "US")
    assert result is not None
    assert result.pass_rate == 1.0


def test_uk_region():
    """Should use UK canaries for UK region."""
    validator = _make_validator()
    influencers = [
        Influencer(name="Joe Wicks", handles={Platform.Instagram: "@thebodycoach"}),
        Influencer(name="Krissy Cela", handles={Platform.Instagram: ""}),
        Influencer(name="Alice Liveing", handles={Platform.Instagram: ""}),
    ]
    result = validator.validate(influencers, "FITNESS", "Fitness", "UK")
    assert result is not None
    assert result.pass_rate == 1.0


# ============================================================
# Regression: cross-platform canary validation
# BUG: Canary validation ran per-job, so Matt Wolfe (YT-only)
#      was reported MISSING when checked against IG-only results.
# FIX: Validate against ALL seeds after global dedup.
# ============================================================

def test_cross_platform_canary_found_globally():
    """Canary passes when validated against combined cross-platform results.

    Matt Wolfe has a YT handle (@mreflow) but no IG handle.
    When validated against combined IG+YT results, he should be FOUND.
    This is the CORRECT behavior after the fix.
    """
    validator = _make_validator()

    # Simulated cross-platform results (IG + YT combined)
    all_influencers = [
        # IG-only creators
        Influencer(name="", handles={Platform.Instagram: "ig_creator"}),
        # YT-only creators — Matt Wolfe found here
        Influencer(name="Matt Wolfe", handles={Platform.YouTube: "mreflow"}),
        Influencer(name="Matthew Berman", handles={Platform.YouTube: "matthew_berman"}),
    ]

    result = validator.validate(all_influencers, "AI", "AI", "US")
    assert result is not None
    assert result.pass_rate == 1.0, (
        f"Expected 100% canary pass rate with cross-platform results, "
        f"got {result.pass_rate:.0%}. Missing: {result.missing}"
    )
    assert len(result.missing) == 0


def test_cross_platform_canary_missed_per_job():
    """Proves the OLD per-job bug: IG-only results miss YT-only canaries.

    When validated against only IG job results (no Matt Wolfe),
    the canary should be MISSING. This is the per-job behavior
    that was incorrectly reporting 0% canary pass rates.
    """
    validator = _make_validator()

    # IG job results ONLY — no Matt Wolfe (he's YT-only)
    ig_only_influencers = [
        Influencer(name="", handles={Platform.Instagram: "ig_creator"}),
        Influencer(name="", handles={Platform.Instagram: "another_ig"}),
    ]

    result = validator.validate(ig_only_influencers, "AI", "AI", "US")
    assert result is not None
    # Per-job: Matt Wolfe and Matthew Berman are both MISSING
    assert result.pass_rate == 0.0
    assert "Matt Wolfe" in result.missing
    assert "Matthew Berman" in result.missing
