"""
Tests for statement interpretation functions in the Project ℵω rigor track.
"""

from src.rigor.finite_universe import (
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)
from src.rigor.interpretation import (
    InterpretationStatus,
    StatementInterpretationResult,
    UniverseInterpretation,
    constant_interpretation,
    explicit_interpretation,
)
from src.rigor.semantics import (
    FiniteTruthValue,
    classical_truth_space,
    modal_truth_space,
)


def test_constant_interpretation_is_valid_for_classical_true():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    assert interpretation.is_total()
    assert interpretation.is_valid_interpretation()
    assert interpretation.validity_count() == universe.statement_count()
    assert interpretation.designated_count() == universe.statement_count()
    assert "UniverseInterpretation" in interpretation.describe()


def test_invalid_truth_value_in_classical_space():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.BOTH,
    )

    result = interpretation.results()[0]

    assert not interpretation.is_valid_interpretation()
    assert result.status == InterpretationStatus.INVALID_TRUTH_VALUE
    assert not result.is_valid()


def test_explicit_interpretation_by_statement_name():
    universe = modal_finite_universe()
    truth_space = modal_truth_space()

    interpretation = explicit_interpretation(
        universe=universe,
        truth_space=truth_space,
        assignments={
            "necessary_truth_statement": FiniteTruthValue.NECESSARY_TRUE,
            "possible_truth_statement": FiniteTruthValue.POSSIBLY_TRUE,
        },
    )

    assert interpretation.is_total()
    assert interpretation.is_valid_interpretation()
    assert interpretation.validity_count() == 2
    assert interpretation.designated_count() == 1


def test_uninterpreted_statement_result():
    universe = modal_finite_universe()
    truth_space = modal_truth_space()

    interpretation = explicit_interpretation(
        universe=universe,
        truth_space=truth_space,
        assignments={
            "necessary_truth_statement": FiniteTruthValue.NECESSARY_TRUE,
        },
    )

    assert not interpretation.is_total()
    assert not interpretation.is_valid_interpretation()

    results = interpretation.results()
    statuses = {result.status for result in results}

    assert InterpretationStatus.UNINTERPRETED in statuses


def test_statement_interpretation_result_designated():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    result = interpretation.results()[0]

    assert isinstance(result, StatementInterpretationResult)
    assert result.is_valid()
    assert result.is_designated()
    assert "StatementInterpretationResult" in result.describe()


def test_custom_universe_interpretation():
    statement = FiniteStatement.from_features(
        name="custom_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    universe = classical_finite_universe().__class__.build(
        name="Custom Universe",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement],
    )

    truth_space = classical_truth_space()

    interpretation = UniverseInterpretation(
        universe=universe,
        truth_space=truth_space,
        assignment={statement: FiniteTruthValue.FALSE},
    )

    assert interpretation.is_total()
    assert interpretation.is_valid_interpretation()
    assert interpretation.validity_count() == 1
    assert interpretation.designated_count() == 0
