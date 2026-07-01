"""
Tests for identity laws in finite universe categories.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.category import FiniteUniverseCategory, starter_finite_universe_category
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)
from src.rigor.identity_laws import (
    IdentityLawAnalyzer,
    IdentityLawCheck,
    IdentityLawReport,
    IdentityLawStatus,
)


def test_identity_laws_hold_for_identity_bridge():
    universe = classical_finite_universe()
    bridge = identity_bridge(universe)

    check = IdentityLawAnalyzer().check_bridge(bridge)

    assert isinstance(check, IdentityLawCheck)
    assert check.holds()
    assert check.left_identity_holds
    assert check.right_identity_holds
    assert check.status == IdentityLawStatus.HOLDS


def test_identity_laws_hold_for_collapse_bridge():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    check = IdentityLawAnalyzer().check_bridge(bridge)

    assert check.holds()
    assert check.status == IdentityLawStatus.HOLDS


def test_identity_laws_hold_for_starter_category():
    category = starter_finite_universe_category()

    report = IdentityLawAnalyzer().check_category(category)

    assert isinstance(report, IdentityLawReport)
    assert report.holds()
    assert report.failure_count() == 0
    assert report.success_count() == category.morphism_count()


def test_identity_law_report_describe():
    category = starter_finite_universe_category()
    report = IdentityLawAnalyzer().check_category(category)

    assert "IdentityLawReport" in report.describe()
    assert "Identity laws hold: True" in report.describe()

    for check in report.checks:
        assert "IdentityLawCheck" in check.describe()


def test_identity_laws_for_custom_bridge():
    source_statement = FiniteStatement.from_features(
        name="source_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    target_statement = FiniteStatement.from_features(
        name="target_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = FiniteLogicalUniverse.build(
        name="Source",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[source_statement],
    )

    target = FiniteLogicalUniverse.build(
        name="Target",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[target_statement],
    )

    bridge = FiniteBridge(
        name="Custom Bridge",
        source=source,
        target=target,
        mapping={source_statement: target_statement},
    )

    category = FiniteUniverseCategory.build(
        name="Custom Category",
        objects=(source, target),
        morphisms=(
            identity_bridge(source),
            identity_bridge(target),
            bridge,
        ),
    )

    report = IdentityLawAnalyzer().check_category(category)

    assert report.holds()
    assert report.failure_count() == 0


def test_identity_law_status_values():
    assert IdentityLawStatus.HOLDS.value == "holds"
    assert IdentityLawStatus.FAILS_LEFT_IDENTITY.value == "fails_left_identity"
    assert IdentityLawStatus.FAILS_RIGHT_IDENTITY.value == "fails_right_identity"
    assert IdentityLawStatus.FAILS_BOTH.value == "fails_both"
