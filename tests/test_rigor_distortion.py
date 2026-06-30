"""
Tests for rigorous bridge distortion analysis in Project ℵω.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.distortion import (
    BridgeDistortionReport,
    DistortionAnalyzer,
    DistortionKind,
    DistortionWitness,
)
from src.rigor.finite_universe import (
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
    paraconsistent_finite_universe,
)


def test_identity_bridge_has_no_distortion():
    universe = classical_finite_universe()
    bridge = identity_bridge(universe)

    report = DistortionAnalyzer().analyze_bridge(bridge)

    assert isinstance(report, BridgeDistortionReport)
    assert not report.has_distortion()
    assert report.witness_count() == 0
    assert report.preserved_count() == universe.statement_count()
    assert report.theorem_verified_for_bridge()


def test_modal_to_classical_has_feature_loss():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    report = DistortionAnalyzer().analyze_bridge(bridge)

    assert report.theorem_hypothesis_holds()
    assert report.theorem_conclusion_holds()
    assert report.theorem_verified_for_bridge()
    assert report.witness_count() >= 1
    assert len(report.feature_loss_witnesses()) >= 1


def test_paraconsistent_to_classical_witnesses_contradiction_loss():
    source = paraconsistent_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Paraconsistent to Classical Collapse",
        source=source,
        target=target,
    )

    report = DistortionAnalyzer().analyze_bridge(bridge)

    witnesses = report.feature_loss_witnesses()

    assert len(witnesses) == 1
    assert SemanticFeature.CONTRADICTION_TOLERANCE in witnesses[0].missing_features
    assert witnesses[0].kind == DistortionKind.FEATURE_LOSS


def test_undefined_translation_is_distortion():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = FiniteBridge(
        name="Empty Modal to Classical Bridge",
        source=source,
        target=target,
        mapping={},
    )

    report = DistortionAnalyzer().analyze_bridge(bridge)

    assert not bridge.is_total()
    assert report.has_distortion()
    assert len(report.undefined_witnesses()) == source.statement_count()
    assert report.theorem_verified_for_bridge()


def test_preserved_translation_witness_kind():
    source = classical_finite_universe()
    target = classical_finite_universe()
    bridge = identity_bridge(source)

    report = DistortionAnalyzer().analyze_bridge(bridge)
    witness = report.witnesses[0]

    assert isinstance(witness, DistortionWitness)
    assert witness.kind == DistortionKind.PRESERVED
    assert not witness.is_real_witness()
    assert witness.missing_feature_count() == 0


def test_custom_feature_loss_statement():
    statement = FiniteStatement.from_features(
        name="resource_statement",
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.RESOURCE_SENSITIVITY,
        ],
    )

    source = source = classical_finite_universe()
    richer_source = source.__class__.build(
        name="Resource Source Universe",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.RESOURCE_SENSITIVITY,
        ],
        statements=[statement],
    )

    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Resource to Classical Collapse",
        source=richer_source,
        target=target,
    )

    report = DistortionAnalyzer().analyze_bridge(bridge)

    assert report.theorem_hypothesis_holds()
    assert report.has_distortion()
    assert SemanticFeature.RESOURCE_SENSITIVITY in report.witnesses[0].missing_features
    assert "BridgeDistortionReport" in report.describe()
