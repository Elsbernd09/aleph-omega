"""
Tests for the finite Bridge Distortion Theorem.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
    paraconsistent_finite_universe,
)
from src.rigor.theorem import (
    BridgeDistortionTheorem,
    TheoremCheck,
    TheoremConclusion,
    TheoremHypothesis,
    TheoremStatus,
)


def test_theorem_statement_exists():
    theorem = BridgeDistortionTheorem()
    statement = theorem.theorem_statement()

    assert "Finite Bridge Distortion Theorem" in statement
    assert "total" in statement
    assert "distorted translation" in statement


def test_identity_bridge_is_vacuously_true():
    classical = classical_finite_universe()
    bridge = identity_bridge(classical)

    check = BridgeDistortionTheorem().check(bridge)

    assert isinstance(check, TheoremCheck)
    assert check.status == TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE
    assert check.implication_holds()
    assert not check.is_nonvacuous_verification()


def test_modal_to_classical_nonvacuous_verification():
    modal = modal_finite_universe()
    classical = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=modal,
        target=classical,
    )

    check = BridgeDistortionTheorem().check(bridge)

    assert check.status == TheoremStatus.VERIFIED_FOR_INSTANCE
    assert check.hypothesis.holds()
    assert check.conclusion.holds()
    assert check.implication_holds()
    assert check.is_nonvacuous_verification()


def test_paraconsistent_to_classical_nonvacuous_verification():
    source = paraconsistent_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Paraconsistent to Classical Collapse",
        source=source,
        target=target,
    )

    check = BridgeDistortionTheorem().check(bridge)

    assert check.status == TheoremStatus.VERIFIED_FOR_INSTANCE
    assert check.is_nonvacuous_verification()
    assert check.report.has_distortion()


def test_partial_bridge_is_vacuous_for_theorem():
    modal = modal_finite_universe()
    classical = classical_finite_universe()

    bridge = FiniteBridge(
        name="Partial Bridge",
        source=modal,
        target=classical,
        mapping={},
    )

    check = BridgeDistortionTheorem().check(bridge)

    assert not bridge.is_total()
    assert check.status == TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE
    assert check.implication_holds()


def test_theorem_hypothesis_and_conclusion_descriptions():
    hypothesis = TheoremHypothesis(
        bridge_is_total=True,
        feature_mismatch_exists=True,
        statement_uses_absent_feature=True,
    )

    conclusion = TheoremConclusion(
        distortion_witness_exists=True,
    )

    assert hypothesis.holds()
    assert conclusion.holds()
    assert "All hypotheses hold: True" in hypothesis.describe()
    assert "Distortion witness exists: True" in conclusion.describe()


def test_custom_resource_sensitive_theorem_instance():
    statement = FiniteStatement.from_features(
        name="resource_sensitive_statement",
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.RESOURCE_SENSITIVITY,
        ],
    )

    source = FiniteLogicalUniverse.build(
        name="Resource Sensitive Universe",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.RESOURCE_SENSITIVITY,
        ],
        statements=[statement],
    )

    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Resource Sensitive to Classical Collapse",
        source=source,
        target=target,
    )

    check = BridgeDistortionTheorem().check(bridge)

    assert check.status == TheoremStatus.VERIFIED_FOR_INSTANCE
    assert check.is_nonvacuous_verification()
    assert check.report.witness_count() == 1


def test_check_many():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    bridges = (
        identity_bridge(classical),
        collapse_bridge(
            name="Modal to Classical Collapse",
            source=modal,
            target=classical,
        ),
    )

    checks = BridgeDistortionTheorem().check_many(bridges)

    assert len(checks) == 2
    assert checks[0].implication_holds()
    assert checks[1].implication_holds()
