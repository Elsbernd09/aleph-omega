"""
Tests for satisfaction-based semantic preservation.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
)
from src.rigor.interpretation import constant_interpretation
from src.rigor.preservation import (
    BridgePreservationReport,
    PreservationResultStatus,
    SatisfactionPreservationAnalyzer,
    SatisfactionPreservationResult,
)
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def test_identity_bridge_preserves_satisfied_classical_statement():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = identity_bridge(universe)

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert isinstance(report, BridgePreservationReport)
    assert report.preserved_count() == 1
    assert report.distortion_count() == 0
    assert report.all_satisfied_sources_preserved()


def test_source_not_satisfied_means_preservation_not_required():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    bridge = identity_bridge(universe)

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    result = report.results[0]

    assert result.status == PreservationResultStatus.SOURCE_NOT_SATISFIED
    assert not result.is_distorted()
    assert report.distortion_count() == 0


def test_undefined_translation_distorts_satisfied_source():
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

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    result = report.results[0]

    assert isinstance(result, SatisfactionPreservationResult)
    assert result.status == PreservationResultStatus.UNDEFINED_TRANSLATION
    assert result.is_distorted()
    assert report.has_satisfaction_distortion()


def test_target_not_satisfied_distorts_satisfied_source():
    source_statement = FiniteStatement.from_features(
        name="source_true_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    target_statement = FiniteStatement.from_features(
        name="target_false_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = FiniteLogicalUniverse.build(
        name="Source Universe",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[source_statement],
    )

    target = FiniteLogicalUniverse.build(
        name="Target Universe",
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

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=source_interpretation,
        target_interpretation=target_interpretation,
    )

    result = report.results[0]

    assert result.status == PreservationResultStatus.TARGET_NOT_SATISFIED
    assert result.is_distorted()
    assert report.distortion_count() == 1


def test_collapse_bridge_can_preserve_satisfaction_if_target_is_satisfied():
    source = classical_finite_universe()
    target = classical_finite_universe()
    truth_space = classical_truth_space()

    bridge = collapse_bridge(
        name="Classical Collapse",
        source=source,
        target=target,
    )

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=target,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=source_interpretation,
        target_interpretation=target_interpretation,
    )

    assert report.distortion_count() == 1


def test_preservation_report_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge = identity_bridge(universe)

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert "BridgePreservationReport" in report.describe()
    assert "SatisfactionPreservationResult" in report.results[0].describe()
