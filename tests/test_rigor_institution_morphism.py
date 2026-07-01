"""
Tests for finite institution morphisms.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.finite_institution import FiniteInstitutionBuilder
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.institution_morphism import (
    FiniteInstitutionMorphism,
    InstitutionMorphismBuilder,
    InstitutionMorphismReport,
    ModelPairing,
    MorphismConditionStatus,
    SatisfactionConditionWitness,
)
from src.rigor.interpretation import constant_interpretation
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def make_institution(value=FiniteTruthValue.TRUE):
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=value,
    )

    return FiniteInstitutionBuilder().from_universe_and_interpretations(
        name="Test Institution",
        universe=universe,
        interpretations=(interpretation,),
    )


def test_identity_institution_morphism_preserves_satisfaction():
    institution = make_institution(FiniteTruthValue.TRUE)
    bridge = identity_bridge(institution.universe)

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=bridge,
    )

    assert isinstance(morphism, FiniteInstitutionMorphism)
    assert morphism.preserves_satisfaction()
    assert "FiniteInstitutionMorphism" in morphism.describe()


def test_satisfaction_condition_report_exists():
    institution = make_institution(FiniteTruthValue.TRUE)
    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    report = morphism.check_satisfaction_condition()

    assert isinstance(report, InstitutionMorphismReport)
    assert report.witness_count() > 0
    assert report.condition_holds()
    assert "InstitutionMorphismReport" in report.describe()


def test_model_pairing_describe():
    institution = make_institution(FiniteTruthValue.TRUE)
    model = institution.models[0]

    pairing = ModelPairing(source_model=model, target_model=model)

    assert "ModelPairing" in pairing.describe()


def test_witness_describe():
    institution = make_institution(FiniteTruthValue.TRUE)
    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    witness = morphism.check_satisfaction_condition().witnesses[0]

    assert isinstance(witness, SatisfactionConditionWitness)
    assert "SatisfactionConditionWitness" in witness.describe()


def test_empty_bridge_fails_when_source_true():
    source = make_institution(FiniteTruthValue.TRUE)
    target = make_institution(FiniteTruthValue.TRUE)

    empty_bridge = FiniteBridge(
        name="Empty Institution Bridge",
        source=source.universe,
        target=target.universe,
        mapping={},
    )

    morphism = InstitutionMorphismBuilder().paired_morphism(
        name="Empty Morphism",
        source=source,
        target=target,
        bridge=empty_bridge,
    )

    report = morphism.check_satisfaction_condition()

    assert not report.condition_holds()
    assert len(report.failure_witnesses()) > 0
    assert report.failure_witnesses()[0].status == MorphismConditionStatus.UNDEFINED_TRANSLATION


def test_target_false_fails_when_source_true():
    source = make_institution(FiniteTruthValue.TRUE)
    target = make_institution(FiniteTruthValue.FALSE)

    bridge = identity_bridge(source.universe)

    morphism = InstitutionMorphismBuilder().paired_morphism(
        name="Target False Morphism",
        source=source,
        target=target,
        bridge=bridge,
    )

    report = morphism.check_satisfaction_condition()

    assert not report.condition_holds()
    assert len(report.failure_witnesses()) > 0
