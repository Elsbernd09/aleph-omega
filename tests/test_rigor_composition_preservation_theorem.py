"""
Tests for the finite composition preservation theorem.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.composition_preservation_theorem import (
    CompositionPreservationTheorem,
    CompositionPreservationTheoremCheck,
    CompositionPreservationTheoremStatus,
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


def test_theorem_statement_exists():
    theorem = CompositionPreservationTheorem()
    statement = theorem.theorem_statement()

    assert "Finite Composition Preservation Theorem" in statement
    assert "G ∘ F" in statement
    assert "preserves satisfaction" in statement


def test_identity_composition_theorem_verified():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert isinstance(check, CompositionPreservationTheoremCheck)
    assert check.status == CompositionPreservationTheoremStatus.VERIFIED_FOR_INSTANCE
    assert check.hypothesis_holds()
    assert check.conclusion_holds()
    assert check.implication_holds()
    assert check.is_nonvacuous_verification()


def test_noncomposable_theorem_status():
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

    check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=classical_interpretation,
        middle_interpretation=classical_interpretation,
        target_interpretation=modal_interpretation,
    )

    assert check.status == CompositionPreservationTheoremStatus.NOT_COMPOSABLE
    assert not check.hypothesis_holds()
    assert check.implication_holds()


def test_hypothesis_fails_when_first_leg_fails():
    statement_a = FiniteStatement.from_features("a", [SemanticFeature.CLASSICAL_TRUTH])
    statement_b = FiniteStatement.from_features("b", [SemanticFeature.CLASSICAL_TRUTH])
    statement_c = FiniteStatement.from_features("c", [SemanticFeature.CLASSICAL_TRUTH])

    universe_a = FiniteLogicalUniverse.build("A", [SemanticFeature.CLASSICAL_TRUTH], [statement_a])
    universe_b = FiniteLogicalUniverse.build("B", [SemanticFeature.CLASSICAL_TRUTH], [statement_b])
    universe_c = FiniteLogicalUniverse.build("C", [SemanticFeature.CLASSICAL_TRUTH], [statement_c])

    first = FiniteBridge("A to B", universe_a, universe_b, {statement_a: statement_b})
    second = FiniteBridge("B to C", universe_b, universe_c, {statement_b: statement_c})

    interpretation_a = constant_interpretation(universe_a, classical_truth_space(), FiniteTruthValue.TRUE)
    interpretation_b_false = constant_interpretation(universe_b, classical_truth_space(), FiniteTruthValue.FALSE)
    interpretation_c = constant_interpretation(universe_c, classical_truth_space(), FiniteTruthValue.TRUE)

    check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=interpretation_a,
        middle_interpretation=interpretation_b_false,
        target_interpretation=interpretation_c,
    )

    assert check.status == CompositionPreservationTheoremStatus.HYPOTHESIS_FAILS_FOR_INSTANCE
    assert not check.hypothesis_holds()
    assert check.implication_holds()


def test_theorem_check_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()
    interpretation = constant_interpretation(universe, truth_space, FiniteTruthValue.TRUE)

    check = CompositionPreservationTheorem().check(
        first=identity_bridge(universe),
        second=identity_bridge(universe),
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert "CompositionPreservationTheoremCheck" in check.describe()
    assert "Implication holds: True" in check.describe()
