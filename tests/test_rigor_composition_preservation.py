"""
Tests for preservation under bridge composition.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.composition_preservation import (
    CompositionPreservationAnalyzer,
    CompositionPreservationCheck,
    CompositionPreservationStatus,
)
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)
from src.rigor.interpretation import constant_interpretation
from src.rigor.semantics import FiniteTruthValue, classical_truth_space, modal_truth_space


def test_identity_composition_preserves_satisfaction():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    check = CompositionPreservationAnalyzer().check(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert isinstance(check, CompositionPreservationCheck)
    assert check.status == CompositionPreservationStatus.PRESERVED_THROUGH_COMPOSITION
    assert check.is_successful()
    assert check.composite is not None
    assert check.composite_check is not None
    assert check.composite_check.preserves_satisfaction()


def test_not_composable_bridges():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    first = identity_bridge(classical)
    second = identity_bridge(modal)

    classical_interpretation = constant_interpretation(
        universe=classical,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    modal_interpretation = constant_interpretation(
        universe=modal,
        truth_space=modal_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    check = CompositionPreservationAnalyzer().check(
        first=first,
        second=second,
        source_interpretation=classical_interpretation,
        middle_interpretation=classical_interpretation,
        target_interpretation=modal_interpretation,
    )

    assert check.status == CompositionPreservationStatus.NOT_COMPOSABLE
    assert not check.is_successful()
    assert check.composite is None


def test_first_leg_fails_preservation():
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

    first = FiniteBridge(
        name="A to B",
        source=universe_a,
        target=universe_b,
        mapping={statement_a: statement_b},
    )
    second = FiniteBridge(
        name="B to C",
        source=universe_b,
        target=universe_c,
        mapping={statement_b: statement_c},
    )

    interpretation_a = constant_interpretation(
        universe=universe_a,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )
    interpretation_b_false = constant_interpretation(
        universe=universe_b,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.FALSE,
    )
    interpretation_c = constant_interpretation(
        universe=universe_c,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    check = CompositionPreservationAnalyzer().check(
        first=first,
        second=second,
        source_interpretation=interpretation_a,
        middle_interpretation=interpretation_b_false,
        target_interpretation=interpretation_c,
    )

    assert check.status == CompositionPreservationStatus.FIRST_LEG_FAILS
    assert not check.is_successful()


def test_second_leg_fails_preservation():
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

    first = FiniteBridge(
        name="A to B",
        source=universe_a,
        target=universe_b,
        mapping={statement_a: statement_b},
    )
    second = FiniteBridge(
        name="B to C",
        source=universe_b,
        target=universe_c,
        mapping={statement_b: statement_c},
    )

    interpretation_a = constant_interpretation(
        universe=universe_a,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )
    interpretation_b = constant_interpretation(
        universe=universe_b,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )
    interpretation_c_false = constant_interpretation(
        universe=universe_c,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.FALSE,
    )

    check = CompositionPreservationAnalyzer().check(
        first=first,
        second=second,
        source_interpretation=interpretation_a,
        middle_interpretation=interpretation_b,
        target_interpretation=interpretation_c_false,
    )

    assert check.status == CompositionPreservationStatus.SECOND_LEG_FAILS
    assert not check.is_successful()


def test_composition_preservation_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    check = CompositionPreservationAnalyzer().check(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert "CompositionPreservationCheck" in check.describe()
    assert "Successful: True" in check.describe()
