"""
Tests for the formal claim registry.
"""

import pytest

from src.rigor.claim_registry import (
    ClaimRegistry,
    ClaimScope,
    FormalClaim,
    VerificationLevel,
    standard_claim_registry,
)


def test_standard_claim_registry_exists():
    registry = standard_claim_registry()

    assert isinstance(registry, ClaimRegistry)
    assert registry.claim_count() >= 5
    assert "ClaimRegistry" in registry.describe()


def test_claim_lookup_by_identifier():
    registry = standard_claim_registry()

    claim = registry.by_identifier("claim.composition_preservation.finite")

    assert isinstance(claim, FormalClaim)
    assert claim.title == "Finite Composition Preservation"
    assert claim.scope == ClaimScope.FINITE_MODEL


def test_claim_lookup_missing_identifier_raises():
    registry = standard_claim_registry()

    with pytest.raises(KeyError):
        registry.by_identifier("missing.claim")


def test_strongly_verified_claims_exist():
    registry = standard_claim_registry()

    strong_claims = registry.strongly_verified_claims()

    assert len(strong_claims) > 0
    assert all(claim.is_strongly_verified() for claim in strong_claims)


def test_conjectural_claims_exist():
    registry = standard_claim_registry()

    conjectural_claims = registry.conjectural_claims()

    assert len(conjectural_claims) > 0
    assert all(claim.is_conjectural() for claim in conjectural_claims)


def test_by_scope_and_verification_level():
    registry = standard_claim_registry()

    finite_claims = registry.by_scope(ClaimScope.FINITE_MODEL)
    stress_tested_claims = registry.by_verification_level(VerificationLevel.STRESS_TESTED)

    assert len(finite_claims) > 0
    assert len(stress_tested_claims) > 0


def test_formal_claim_describe():
    claim = standard_claim_registry().by_identifier("claim.general_foundations")

    description = claim.describe()

    assert "FormalClaim" in description
    assert "Conjectural: True" in description
