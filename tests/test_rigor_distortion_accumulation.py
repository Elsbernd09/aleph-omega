"""
Tests for distortion accumulation across bridge composition.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.distortion_accumulation import (
    DistortionAccumulationAnalyzer,
    DistortionAccumulationReport,
    DistortionAccumulationStatus,
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


def make_chain():
    statement_a = FiniteStatement.from_features("a", [SemanticFeature.CLASSICAL_TRUTH])
    statement_b = FiniteStatement.from_features("b", [SemanticFeature.CLASSICAL_TRUTH])
    statement_c = FiniteStatement.from_features("c", [SemanticFeature.CLASSICAL_TRUTH])

    universe_a = FiniteLogicalUniverse.build(
        "A",
        [SemanticFeature.CLASSICAL_TRUTH],
        [statement_a],
    )
    universe_b = FiniteLogicalUniverse.build(
        "B",
        [SemanticFeature.CLASSICAL_TRUTH],
        [statement_b],
    )
    universe_c = FiniteLogicalUniverse.build(
        "C",
        [SemanticFeature.CLASSICAL_TRUTH],
        [statement_c],
    )

    first = FiniteBridge(
        "A to B",
        universe_a,
        universe_b,
        {statement_a: statement_b},
    )
    second = FiniteBridge(
        "B to C",
        universe_b,
        universe_c,
        {statement_b: statement_c},
    )

    return universe_a, universe_b, universe_c, first, second


def test_no_distortion_for_identity_chain():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = DistortionAccumulationAnalyzer().analyze(
        first=identity_bridge(universe),
        second=identity_bridge(universe),
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert isinstance(report, DistortionAccumulationReport)
    assert report.status == DistortionAccumulationStatus.NO_DISTORTION
    assert report.total_distortion_pressure() == 0
    assert not report.has_any_distortion()


def test_first_leg_distortion():
    universe_a, universe_b, universe_c, first, second = make_chain()

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
    interpretation_c_false = constant_interpretation(
        universe=universe_c,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.FALSE,
    )

    report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=interpretation_a,
        middle_interpretation=interpretation_b_false,
        target_interpretation=interpretation_c_false,
    )

    assert report.status in {
        DistortionAccumulationStatus.FIRST_LEG_DISTORTION,
        DistortionAccumulationStatus.MULTIPLE_DISTORTIONS,
    }
    assert report.first_distortion_count() == 1
    assert report.has_any_distortion()


def test_second_leg_distortion():
    universe_a, universe_b, universe_c, first, second = make_chain()

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

    report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=interpretation_a,
        middle_interpretation=interpretation_b,
        target_interpretation=interpretation_c_false,
    )

    assert report.status in {
        DistortionAccumulationStatus.SECOND_LEG_DISTORTION,
        DistortionAccumulationStatus.MULTIPLE_DISTORTIONS,
    }
    assert report.second_distortion_count() == 1
    assert report.composite_distortion_count() == 1


def test_not_composable_status():
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

    report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=classical_interpretation,
        middle_interpretation=classical_interpretation,
        target_interpretation=modal_interpretation,
    )

    assert report.status == DistortionAccumulationStatus.NOT_COMPOSABLE
    assert report.composite is None
    assert report.total_distortion_pressure() == 0


def test_distortion_accumulation_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = DistortionAccumulationAnalyzer().analyze(
        first=identity_bridge(universe),
        second=identity_bridge(universe),
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    assert "DistortionAccumulationReport" in report.describe()
    assert "Total distortion pressure" in report.describe()


def test_status_values():
    assert DistortionAccumulationStatus.NO_DISTORTION.value == "no_distortion"
    assert DistortionAccumulationStatus.MULTIPLE_DISTORTIONS.value == "multiple_distortions"
    assert DistortionAccumulationStatus.NOT_COMPOSABLE.value == "not_composable"
