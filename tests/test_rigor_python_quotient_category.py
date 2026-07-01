"""
Tests for Python-side quotient category layer.
"""

from src.rigor.finite_institution import FiniteInstitutionBuilder
from src.rigor.finite_universe import classical_finite_universe
from src.rigor.interpretation import constant_interpretation
from src.rigor.python_quotient_category import (
    PythonQuotientCategory,
    PythonQuotientCategoryLawReport,
    PythonQuotientCategoryLawStatus,
)
from src.rigor.python_quotient_morphism import PythonQuotientMorphism
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


def make_category():
    institution = make_institution()

    return PythonQuotientCategory(
        name="Test Python Quotient Category",
        objects=(institution,),
    )


def test_python_quotient_category_builds():
    category = make_category()

    assert category.object_count() == 1
    assert "PythonQuotientCategory" in category.describe()


def test_identity_builds():
    category = make_category()
    institution = category.objects[0]

    identity = category.identity(institution)

    assert isinstance(identity, PythonQuotientMorphism)
    assert identity.source_name() == institution.name
    assert identity.target_name() == institution.name


def test_left_identity_holds_for_identity():
    category = make_category()
    institution = category.objects[0]
    identity = category.identity(institution)

    report = category.check_left_identity(identity)

    assert isinstance(report, PythonQuotientCategoryLawReport)
    assert report.status == PythonQuotientCategoryLawStatus.HOLDS
    assert report.holds()


def test_right_identity_holds_for_identity():
    category = make_category()
    institution = category.objects[0]
    identity = category.identity(institution)

    report = category.check_right_identity(identity)

    assert isinstance(report, PythonQuotientCategoryLawReport)
    assert report.status == PythonQuotientCategoryLawStatus.HOLDS
    assert report.holds()


def test_associativity_holds_for_identity():
    category = make_category()
    institution = category.objects[0]

    first = category.identity(institution)
    second = category.identity(institution)
    third = category.identity(institution)

    report = category.check_associativity(first, second, third)

    assert isinstance(report, PythonQuotientCategoryLawReport)
    assert report.status == PythonQuotientCategoryLawStatus.HOLDS
    assert report.holds()
