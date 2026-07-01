"""
Tests for finite institution-like systems.
"""

from src.rigor.finite_institution import (
    FiniteInstitution,
    FiniteInstitutionBuilder,
    FiniteModel,
    FiniteSignature,
    SatisfactionJudgement,
)
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.interpretation import constant_interpretation
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def make_institution():
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

    return FiniteInstitutionBuilder().from_universe_and_interpretations(
        name="Test Institution",
        universe=universe,
        interpretations=(true_interpretation, false_interpretation),
    )


def test_finite_signature_builds():
    signature = FiniteSignature.build(
        name="Test Signature",
        symbols=("P", "Q"),
    )

    assert signature.symbol_count() == 2
    assert "FiniteSignature" in signature.describe()


def test_finite_institution_builds():
    institution = make_institution()

    assert isinstance(institution, FiniteInstitution)
    assert institution.model_count() == 2
    assert institution.sentence_count() > 0
    assert "FiniteInstitution" in institution.describe()


def test_finite_models_build():
    institution = make_institution()

    model = institution.models[0]

    assert isinstance(model, FiniteModel)
    assert model.signature == institution.signature
    assert "FiniteModel" in model.describe()


def test_satisfaction_judgements_exist():
    institution = make_institution()

    judgements = institution.satisfaction_judgements()

    assert len(judgements) == institution.model_count() * institution.sentence_count()
    assert all(isinstance(judgement, SatisfactionJudgement) for judgement in judgements)
    assert any(judgement.satisfied for judgement in judgements)
    assert any(not judgement.satisfied for judgement in judgements)


def test_satisfied_judgement_count():
    institution = make_institution()

    assert institution.satisfied_judgement_count() > 0
    assert institution.satisfied_judgement_count() < len(institution.satisfaction_judgements())


def test_judgement_describe():
    institution = make_institution()
    judgement = institution.satisfaction_judgements()[0]

    assert "SatisfactionJudgement" in judgement.describe()
