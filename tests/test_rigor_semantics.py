"""
Tests for finite truth-value semantics in the Project ℵω rigor track.
"""

from src.rigor.semantics import (
    FiniteTruthValue,
    FiniteTruthValueSpace,
    SemanticOperation,
    TruthValueInterpretation,
    classical_truth_space,
    many_valued_truth_space,
    modal_truth_space,
    paraconsistent_truth_space,
    standard_truth_spaces,
    truth_space_index,
)


def test_classical_truth_space():
    space = classical_truth_space()

    assert space.has_value(FiniteTruthValue.TRUE)
    assert space.has_value(FiniteTruthValue.FALSE)
    assert not space.has_value(FiniteTruthValue.BOTH)
    assert space.supports_operation(SemanticOperation.NEGATION)
    assert space.is_designated(FiniteTruthValue.TRUE)
    assert not space.is_designated(FiniteTruthValue.FALSE)
    assert space.value_count() == 2


def test_paraconsistent_truth_space_has_both():
    space = paraconsistent_truth_space()

    assert space.has_value(FiniteTruthValue.BOTH)
    assert space.has_value(FiniteTruthValue.NEITHER)
    assert space.is_designated(FiniteTruthValue.BOTH)
    assert space.value_count() == 4


def test_modal_truth_space_has_modal_operations():
    space = modal_truth_space()

    assert space.has_value(FiniteTruthValue.NECESSARY_TRUE)
    assert space.has_value(FiniteTruthValue.POSSIBLY_TRUE)
    assert space.supports_operation(SemanticOperation.MODAL_NECESSITY)
    assert space.supports_operation(SemanticOperation.MODAL_POSSIBILITY)
    assert space.operation_count() == 6


def test_truth_space_expressivity():
    classical = classical_truth_space()
    modal = modal_truth_space()

    assert not classical.is_at_least_as_expressive_as(modal)
    assert FiniteTruthValue.NECESSARY_TRUE in modal.values_absent_from(classical)
    assert SemanticOperation.MODAL_NECESSITY in modal.operations_absent_from(classical)


def test_many_valued_truth_space_has_unknown():
    space = many_valued_truth_space()

    assert space.has_value(FiniteTruthValue.UNKNOWN)
    assert not space.is_designated(FiniteTruthValue.UNKNOWN)
    assert "Many-Valued Truth Space" in space.describe()


def test_truth_value_interpretation():
    space = classical_truth_space()

    interpretation = TruthValueInterpretation(
        statement_name="test_statement",
        truth_value=FiniteTruthValue.TRUE,
        truth_space=space,
        explanation="A true classical statement.",
    )

    assert interpretation.is_valid_in_space()
    assert interpretation.is_designated()
    assert "TruthValueInterpretation" in interpretation.describe()


def test_invalid_truth_value_interpretation():
    space = classical_truth_space()

    interpretation = TruthValueInterpretation(
        statement_name="bad_statement",
        truth_value=FiniteTruthValue.BOTH,
        truth_space=space,
    )

    assert not interpretation.is_valid_in_space()
    assert not interpretation.is_designated()


def test_custom_truth_value_space():
    space = FiniteTruthValueSpace.build(
        name="Custom Space",
        values=[FiniteTruthValue.TRUE],
        operations=[SemanticOperation.NEGATION],
        designated_values=[FiniteTruthValue.TRUE],
    )

    assert space.value_count() == 1
    assert space.operation_count() == 1
    assert space.has_value(FiniteTruthValue.TRUE)


def test_standard_truth_spaces_and_index():
    spaces = standard_truth_spaces()
    index = truth_space_index()

    assert len(spaces) == 4
    assert "Classical Truth Space" in index
    assert "Modal Truth Space" in index
