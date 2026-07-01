"""
Tests for semantic transport along finite bridges.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)
from src.rigor.interpretation import constant_interpretation, explicit_interpretation
from src.rigor.semantic_transport import (
    SemanticTransportReport,
    SemanticTransporter,
    TransportConflict,
    TransportStatus,
)
from src.rigor.semantics import (
    FiniteTruthValue,
    classical_truth_space,
    modal_truth_space,
)


def test_identity_transport_success():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = identity_bridge(universe)

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    assert isinstance(report, SemanticTransportReport)
    assert report.status == TransportStatus.SUCCESS
    assert report.is_successful()
    assert report.transported_count == 1
    assert report.undefined_count == 0
    assert not report.has_conflicts()
    assert report.transported_interpretation.is_total()


def test_empty_transport_when_source_has_no_assignments():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = explicit_interpretation(
        universe=universe,
        truth_space=truth_space,
        assignments={},
    )

    bridge = identity_bridge(universe)

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    assert report.status == TransportStatus.EMPTY
    assert report.transported_count == 0
    assert report.undefined_count == 0


def test_partial_transport_when_bridge_undefined():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
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

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    assert report.status == TransportStatus.PARTIAL
    assert report.transported_count == 0
    assert report.undefined_count == 1


def test_collapse_transport_success():
    source = modal_finite_universe()
    target = classical_finite_universe()

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=modal_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=source_interpretation,
        target_truth_space=classical_truth_space(),
    )

    assert report.status == TransportStatus.SUCCESS
    assert report.transported_count == 1
    assert not report.has_conflicts()


def test_transport_conflict_detected():
    source_statement_1 = FiniteStatement.from_features(
        name="source_one",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source_statement_2 = FiniteStatement.from_features(
        name="source_two",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    target_statement = FiniteStatement.from_features(
        name="target",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = FiniteLogicalUniverse.build(
        name="Conflict Source",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[source_statement_1, source_statement_2],
    )

    target = FiniteLogicalUniverse.build(
        name="Conflict Target",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[target_statement],
    )

    bridge = FiniteBridge(
        name="Conflict Bridge",
        source=source,
        target=target,
        mapping={
            source_statement_1: target_statement,
            source_statement_2: target_statement,
        },
    )

    source_interpretation = explicit_interpretation(
        universe=source,
        truth_space=classical_truth_space(),
        assignments={
            "source_one": FiniteTruthValue.TRUE,
            "source_two": FiniteTruthValue.FALSE,
        },
    )

    report = SemanticTransporter().transport(
        bridge=bridge,
        source_interpretation=source_interpretation,
        target_truth_space=classical_truth_space(),
    )

    assert report.status == TransportStatus.CONFLICT
    assert report.has_conflicts()
    assert len(report.conflicts) == 1
    assert isinstance(report.conflicts[0], TransportConflict)
    assert "TransportConflict" in report.conflicts[0].describe()


def test_transport_report_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = SemanticTransporter().transport(
        bridge=identity_bridge(universe),
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    assert "SemanticTransportReport" in report.describe()
    assert "Transported count" in report.describe()
