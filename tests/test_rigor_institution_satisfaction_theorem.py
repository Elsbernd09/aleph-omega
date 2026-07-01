"""
Tests for finite institution satisfaction theorem.
"""

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.finite_institution import FiniteInstitutionBuilder
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.institution_morphism import InstitutionMorphismBuilder
from src.rigor.institution_satisfaction_theorem import (
    InstitutionSatisfactionTheorem,
    InstitutionSatisfactionTheoremCheck,
    InstitutionTheoremStatus,
)
from src.rigor.interpretation import constant_interpretation
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


def make_institution(value):
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


def test_theorem_statement_exists():
    statement = InstitutionSatisfactionTheorem().theorem_statement()

    assert "Finite Institution Satisfaction Theorem" in statement
    assert "preserves finite satisfaction" in statement


def test_identity_morphism_verifies_theorem():
    institution = make_institution(FiniteTruthValue.TRUE)

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    check = InstitutionSatisfactionTheorem().check(morphism)

    assert isinstance(check, InstitutionSatisfactionTheoremCheck)
    assert check.status == InstitutionTheoremStatus.VERIFIED_FOR_INSTANCE
    assert check.hypothesis_holds()
    assert check.conclusion_holds()
    assert check.is_nonvacuous_verification()


def test_false_source_is_vacuous():
    institution = make_institution(FiniteTruthValue.FALSE)

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    check = InstitutionSatisfactionTheorem().check(morphism)

    assert check.status == InstitutionTheoremStatus.VACUOUS_FOR_INSTANCE
    assert check.hypothesis_holds()
    assert check.conclusion_holds()
    assert not check.has_source_satisfied_witness()


def test_empty_bridge_fails_theorem_instance():
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

    check = InstitutionSatisfactionTheorem().check(morphism)

    assert check.status == InstitutionTheoremStatus.FAILED_FOR_INSTANCE
    assert not check.hypothesis_holds()
    assert not check.conclusion_holds()


def test_target_false_fails_theorem_instance():
    source = make_institution(FiniteTruthValue.TRUE)
    target = make_institution(FiniteTruthValue.FALSE)

    morphism = InstitutionMorphismBuilder().paired_morphism(
        name="Target False Morphism",
        source=source,
        target=target,
        bridge=identity_bridge(source.universe),
    )

    check = InstitutionSatisfactionTheorem().check(morphism)

    assert check.status == InstitutionTheoremStatus.FAILED_FOR_INSTANCE
    assert not check.hypothesis_holds()


def test_theorem_check_describe():
    institution = make_institution(FiniteTruthValue.TRUE)

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(institution.universe),
    )

    check = InstitutionSatisfactionTheorem().check(morphism)

    assert "InstitutionSatisfactionTheoremCheck" in check.describe()
    assert "Nonvacuous verification: True" in check.describe()
