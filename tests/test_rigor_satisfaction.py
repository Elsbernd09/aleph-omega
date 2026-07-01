"""
Tests for the finite satisfaction relation in the Project ℵω rigor track.
"""

from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
)
from src.rigor.interpretation import constant_interpretation, explicit_interpretation
from src.rigor.satisfaction import (
    SatisfactionChecker,
    SatisfactionReport,
    SatisfactionResult,
    SatisfactionStatus,
)
from src.rigor.semantics import (
    FiniteTruthValue,
    classical_truth_space,
)


def test_classical_true_statement_is_satisfied():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = SatisfactionChecker().check_interpretation(interpretation)

    assert isinstance(report, SatisfactionReport)
    assert report.satisfied_count() == 1
    assert report.failed_count() == 0
    assert report.all_satisfied()


def test_classical_false_statement_not_designated():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    report = SatisfactionChecker().check_interpretation(interpretation)
    result = report.results[0]

    assert result.status == SatisfactionStatus.NOT_DESIGNATED
    assert not result.is_satisfied()
    assert report.failed_count() == 1


def test_invalid_truth_value_fails_satisfaction():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.BOTH,
    )

    report = SatisfactionChecker().check_interpretation(interpretation)
    result = report.results[0]

    assert result.status == SatisfactionStatus.INVALID_INTERPRETATION
    assert not result.is_satisfied()


def test_uninterpreted_statement_fails_satisfaction():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = explicit_interpretation(
        universe=universe,
        truth_space=truth_space,
        assignments={},
    )

    report = SatisfactionChecker().check_interpretation(interpretation)
    result = report.results[0]

    assert result.status == SatisfactionStatus.UNINTERPRETED
    assert not result.is_satisfied()


def test_feature_inadmissible_statement_fails_satisfaction():
    statement = FiniteStatement.from_features(
        name="modal_statement_inside_classical_universe",
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
    )

    universe = FiniteLogicalUniverse.build(
        name="Bad Classical Universe",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement],
    )

    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = SatisfactionChecker().check_interpretation(interpretation)
    result = report.results[0]

    assert isinstance(result, SatisfactionResult)
    assert result.status == SatisfactionStatus.FEATURE_INADMISSIBLE
    assert result.has_feature_failure()
    assert SemanticFeature.MODAL_NECESSITY in result.missing_features


def test_satisfaction_result_describe():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    report = SatisfactionChecker().check_interpretation(interpretation)
    result = report.results[0]

    assert "SatisfactionResult" in result.describe()
    assert "SatisfactionReport" in report.describe()
