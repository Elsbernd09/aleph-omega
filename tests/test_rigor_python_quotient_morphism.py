"""
Tests for Python-side quotient morphisms.
"""

from src.rigor.bridge import identity_bridge
from src.rigor.finite_institution import FiniteInstitutionBuilder
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.institution_morphism import InstitutionMorphismBuilder
from src.rigor.interpretation import constant_interpretation
from src.rigor.python_quotient_morphism import (
    PythonQuotientMorphism,
    PythonQuotientMorphismBuilder,
)
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def make_institution():
    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    return FiniteInstitutionBuilder().from_universe_and_interpretations(
        name="Test Institution",
        universe=universe,
        interpretations=(interpretation,),
    )


def test_quotient_of_identity_builds():
    institution = make_institution()
    bridge = identity_bridge(institution.universe)

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=bridge,
    )

    quotient = PythonQuotientMorphismBuilder().quotient_of(morphism)

    assert isinstance(quotient, PythonQuotientMorphism)
    assert quotient.source_name() == institution.name
    assert quotient.target_name() == institution.name
    assert "PythonQuotientMorphism" in quotient.describe()


def test_equivalent_identity_quotients_match():
    institution = make_institution()
    bridge = identity_bridge(institution.universe)
    builder = PythonQuotientMorphismBuilder()

    first = builder.identity(institution=institution, bridge=bridge)
    second = builder.identity(institution=institution, bridge=bridge)

    assert first.equivalent_to(second)


def test_signature_contains_translation_and_pairing():
    institution = make_institution()
    bridge = identity_bridge(institution.universe)
    builder = PythonQuotientMorphismBuilder()

    quotient = builder.identity(institution=institution, bridge=bridge)

    assert "translation=" in quotient.equivalence_signature
    assert "pairing=" in quotient.equivalence_signature


def test_identity_quotient_composition_succeeds():
    institution = make_institution()
    bridge = identity_bridge(institution.universe)
    builder = PythonQuotientMorphismBuilder()

    first = builder.identity(institution=institution, bridge=bridge)
    second = builder.identity(institution=institution, bridge=bridge)

    composite = builder.compose(first, second)

    assert composite is not None
    assert isinstance(composite, PythonQuotientMorphism)
    assert composite.source_name() == institution.name
    assert composite.target_name() == institution.name
