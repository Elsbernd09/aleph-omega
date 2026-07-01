"""
Tests for the finite satisfaction preservation theorem.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
)
from src.rigor.interpretation import constant_interpretation
from src.rigor.preservation_theorem import (
    PreservationTheoremStatus,
    SatisfactionPreservationTheorem,
    SatisfactionPreservationTheoremCheck,
)
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def test_theorem_statement_exists():
    theorem = SatisfactionPreservationTheorem()
    statement = theorem.theorem_statement()

    assert "Finite Satisfaction Preservation Theorem" in statement
    assert "preserves satisfaction" in statement
    assert "undefined or not satisfied" in statement


def test_identity_bridge_preserves_satisfaction_nonvacuously():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = identity_bridge(universe)

    check = SatisfactionPreservationTheorem().check(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert isinstance(check, SatisfactionPreservationTheoremCheck)
    assert check.status == PreservationTheoremStatus.PRESERVES_SATISFACTION
    assert check.has_satisfied_sources()
    assert check.is_nonvacuous_preservation()
    assert check.preserves_satisfaction()


def test_vacuous_preservation_when_no_source_satisfied():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    false_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    bridge = identity_bridge(universe)

    check = SatisfactionPreservationTheorem().check(
        bridge=bridge,
        source_interpretation=false_interpretation,
        target_interpretation=false_interpretation,
    )

    assert check.status == PreservationTheoremStatus.VACUOUSLY_PRESERVES_SATISFACTION
    assert not check.has_satisfied_sources()
    assert check.preserves_satisfaction()


def test_undefined_translation_fails_preservation():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    true_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = FiniteBridge(
        name="Empty Bridge",
        source=universe,
        target=universe,
        mapping={},
    )

    check = SatisfactionPreservationTheorem().check(
        bridge=bridge,
        source_interpretation=true_interpretation,
        target_interpretation=true_interpretation,
    )

    assert check.status == PreservationTheoremStatus.FAILS_SATISFACTION_PRESERVATION
    assert check.has_satisfied_sources()
    assert not check.preserves_satisfaction()
    assert check.distortion_count() == 1


def test_target_not_satisfied_fails_preservation():
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

    truth_space = classical_truth_space()

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=target,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    bridge = FiniteBridge(
        name="Truth to False Bridge",
        source=source,
        target=target,
        mapping={source_statement: target_statement},
    )

    check = SatisfactionPreservationTheorem().check(
        bridge=bridge,
        source_interpretation=source_interpretation,
        target_interpretation=target_interpretation,
    )

    assert check.status == PreservationTheoremStatus.FAILS_SATISFACTION_PRESERVATION
    assert check.has_satisfied_sources()
    assert check.distortion_count() == 1


def test_check_many():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    true_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    false_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    bridge = identity_bridge(universe)

    cases = (
        (bridge, true_interpretation, true_interpretation),
        (bridge, false_interpretation, false_interpretation),
    )

    checks = SatisfactionPreservationTheorem().check_many(cases)

    assert len(checks) == 2
    assert checks[0].status == PreservationTheoremStatus.PRESERVES_SATISFACTION
    assert checks[1].status == PreservationTheoremStatus.VACUOUSLY_PRESERVES_SATISFACTION
    assert "SatisfactionPreservationTheoremCheck" in checks[0].describe()
