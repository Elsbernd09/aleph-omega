"""
Tests for rigorous finite bridges in Project ℵω.
"""

from src.rigor.bridge import (
    BridgeTotality,
    FiniteBridge,
    PreservationStatus,
    collapse_bridge,
    identity_bridge,
)
from src.rigor.finite_universe import (
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
    paraconsistent_finite_universe,
)


def test_identity_bridge_is_total_and_preserves():
    universe = classical_finite_universe()
    bridge = identity_bridge(universe)

    assert bridge.is_total()
    assert bridge.totality() == BridgeTotality.TOTAL
    assert bridge.distortion_count() == 0
    assert bridge.preservation_count() == universe.statement_count()
    assert not bridge.has_feature_mismatch()


def test_partial_bridge_is_partial():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = FiniteBridge(
        name="Empty Bridge",
        source=source,
        target=target,
        mapping={},
    )

    assert not bridge.is_total()
    assert bridge.totality() == BridgeTotality.PARTIAL
    assert bridge.distortion_count() == source.statement_count()


def test_collapse_bridge_from_modal_to_classical_has_distortion():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    assert bridge.is_total()
    assert bridge.has_feature_mismatch()
    assert bridge.distortion_count() >= 1

    absent = bridge.source_features_absent_from_target()
    assert SemanticFeature.MODAL_NECESSITY in absent
    assert SemanticFeature.MODAL_POSSIBILITY in absent


def test_statements_using_absent_features():
    source = paraconsistent_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Paraconsistent to Classical Collapse",
        source=source,
        target=target,
    )

    statements = bridge.statements_using_absent_features()

    assert len(statements) == 1
    assert statements[0].requires(SemanticFeature.CONTRADICTION_TOLERANCE)


def test_bridge_translation_status():
    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    translation = bridge.translations()[0]

    assert translation.is_defined()
    assert translation.is_distorted()
    assert translation.preservation_status() == PreservationStatus.DISTORTED
    assert "BridgeTranslation" in translation.describe()


def test_custom_preserved_bridge_when_features_supported():
    statement = FiniteStatement.from_features(
        name="classical_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = classical_finite_universe()
    target = classical_finite_universe()

    bridge = FiniteBridge(
        name="Custom Classical Bridge",
        source=source,
        target=target,
        mapping={next(iter(source.statements)): statement},
    )

    assert bridge.is_total()
    assert bridge.distortion_count() == 0
    assert bridge.preservation_count() == 1
    assert "Custom Classical Bridge" in bridge.describe()
