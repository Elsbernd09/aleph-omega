"""
Tests for associativity of finite bridge composition.
"""

from src.rigor.associativity import (
    AssociativityAnalyzer,
    AssociativityCheck,
    AssociativityReport,
    AssociativityStatus,
)
from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.category import FiniteUniverseCategory, starter_finite_universe_category
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)


def test_associativity_holds_for_three_identity_bridges():
    universe = classical_finite_universe()

    first = identity_bridge(universe)
    second = identity_bridge(universe)
    third = identity_bridge(universe)

    check = AssociativityAnalyzer().check_triple(first, second, third)

    assert isinstance(check, AssociativityCheck)
    assert check.status == AssociativityStatus.HOLDS
    assert check.holds()
    assert check.left_associated is not None
    assert check.right_associated is not None


def test_associativity_holds_for_identity_collapse_identity():
    source = modal_finite_universe()
    target = classical_finite_universe()

    first = identity_bridge(source)

    second = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    third = identity_bridge(target)

    check = AssociativityAnalyzer().check_triple(first, second, third)

    assert check.status == AssociativityStatus.HOLDS
    assert check.holds()


def test_noncomposable_triple_is_not_composable():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    first = identity_bridge(classical)
    second = identity_bridge(modal)
    third = identity_bridge(classical)

    check = AssociativityAnalyzer().check_triple(first, second, third)

    assert check.status == AssociativityStatus.NOT_COMPOSABLE
    assert not check.holds()


def test_associativity_report_for_starter_category():
    category = starter_finite_universe_category()

    report = AssociativityAnalyzer().check_category(category)

    assert isinstance(report, AssociativityReport)
    assert report.check_count() == category.morphism_count() ** 3
    assert report.composable_count() >= 1
    assert report.failure_count() == 0
    assert report.holds()


def test_associativity_for_custom_chain():
    statement_a = FiniteStatement.from_features(
        name="a",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    statement_b = FiniteStatement.from_features(
        name="b",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    statement_c = FiniteStatement.from_features(
        name="c",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    statement_d = FiniteStatement.from_features(
        name="d",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    universe_a = FiniteLogicalUniverse.build(
        name="A",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_a],
    )

    universe_b = FiniteLogicalUniverse.build(
        name="B",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_b],
    )

    universe_c = FiniteLogicalUniverse.build(
        name="C",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_c],
    )

    universe_d = FiniteLogicalUniverse.build(
        name="D",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_d],
    )

    first = FiniteBridge(
        name="f",
        source=universe_a,
        target=universe_b,
        mapping={statement_a: statement_b},
    )

    second = FiniteBridge(
        name="g",
        source=universe_b,
        target=universe_c,
        mapping={statement_b: statement_c},
    )

    third = FiniteBridge(
        name="h",
        source=universe_c,
        target=universe_d,
        mapping={statement_c: statement_d},
    )

    category = FiniteUniverseCategory.build(
        name="Custom Chain Category",
        objects=(universe_a, universe_b, universe_c, universe_d),
        morphisms=(first, second, third),
    )

    report = AssociativityAnalyzer().check_category(category)

    composable_checks = report.composable_checks()

    assert len(composable_checks) >= 1
    assert report.failure_count() == 0
    assert report.holds()


def test_associativity_report_describe():
    category = starter_finite_universe_category()
    report = AssociativityAnalyzer().check_category(category)

    assert "AssociativityReport" in report.describe()

    first_composable = report.composable_checks()[0]
    assert "AssociativityCheck" in first_composable.describe()


def test_associativity_status_values():
    assert AssociativityStatus.HOLDS.value == "holds"
    assert AssociativityStatus.NOT_COMPOSABLE.value == "not_composable"
    assert AssociativityStatus.FAILS.value == "fails"
