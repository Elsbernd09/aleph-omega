"""
Tests for Python-side morphism equivalence.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.finite_institution import FiniteInstitutionBuilder
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.institution_morphism import InstitutionMorphismBuilder
from src.rigor.interpretation import constant_interpretation
from src.rigor.python_morphism_equivalence import (
    PythonMorphismEquivalenceChecker,
    PythonMorphismEquivalenceReport,
    PythonMorphismEquivalenceStatus,
)
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def make_institution(name="Test Institution", value=FiniteTruthValue.TRUE):
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=value,
    )

    return FiniteInstitutionBuilder().from_universe_and_interpretations(
        name=name,
        universe=universe,
        interpretations=(interpretation,),
    )


def test_identity_morphisms_are_equivalent():
    institution = make_institution()
    bridge = identity_bridge(institution.universe)

    first = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=bridge,
    )

    second = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=bridge,
    )

    report = PythonMorphismEquivalenceChecker().check(first, second)

    assert isinstance(report, PythonMorphismEquivalenceReport)
    assert report.status == PythonMorphismEquivalenceStatus.EQUIVALENT
    assert report.equivalent()
    assert "PythonMorphismEquivalenceReport" in report.describe()


def test_different_translation_is_not_equivalent():
    institution = make_institution()

    identity = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    empty_bridge = FiniteBridge(
        name="Empty Bridge",
        source=institution.universe,
        target=institution.universe,
        mapping={},
    )

    empty = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=empty_bridge,
    )

    report = PythonMorphismEquivalenceChecker().check(identity, empty)

    assert not report.equivalent()
    assert report.status == PythonMorphismEquivalenceStatus.DIFFERENT_TRANSLATION


def test_different_source_is_not_equivalent():
    first_institution = make_institution("First")
    second_institution = make_institution("Second")

    first = InstitutionMorphismBuilder().identity_morphism(
        institution=first_institution,
        bridge=identity_bridge(first_institution.universe),
    )

    second = InstitutionMorphismBuilder().identity_morphism(
        institution=second_institution,
        bridge=identity_bridge(second_institution.universe),
    )

    report = PythonMorphismEquivalenceChecker().check(first, second)

    assert not report.equivalent()
    assert report.status == PythonMorphismEquivalenceStatus.DIFFERENT_SOURCE


def test_translation_signature_exists():
    institution = make_institution()

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    signature = PythonMorphismEquivalenceChecker().translation_signature(morphism)

    assert len(signature) == institution.sentence_count()
    assert isinstance(signature[0][0], str)
    assert isinstance(signature[0][1], str)


def test_model_pairing_signature_exists():
    institution = make_institution()

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    signature = PythonMorphismEquivalenceChecker().model_pairing_signature(morphism)

    assert len(signature) == institution.model_count()
    assert isinstance(signature[0][0], str)
    assert isinstance(signature[0][1], str)
