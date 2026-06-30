"""
Tests for finite logical universes in the Project ℵω rigor track.
"""

from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    intuitionistic_finite_universe,
    modal_finite_universe,
    paraconsistent_finite_universe,
    standard_rigor_universes,
)


def test_finite_statement_features():
    statement = FiniteStatement.from_features(
        name="test_statement",
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        informal_reading="A test statement.",
    )

    assert statement.requires(SemanticFeature.CLASSICAL_TRUTH)
    assert statement.requires(SemanticFeature.MODAL_NECESSITY)
    assert not statement.requires(SemanticFeature.CONTRADICTION_TOLERANCE)
    assert statement.feature_count() == 2
    assert "test_statement" in statement.describe()


def test_classical_universe_supports_classical_truth():
    universe = classical_finite_universe()

    assert universe.supports(SemanticFeature.CLASSICAL_TRUTH)
    assert not universe.supports(SemanticFeature.CONTRADICTION_TOLERANCE)
    assert universe.feature_count() == 1
    assert universe.statement_count() == 1
    assert len(universe.admissible_statements()) == 1


def test_paraconsistent_is_more_expressive_than_classical():
    classical = classical_finite_universe()
    paraconsistent = paraconsistent_finite_universe()

    assert paraconsistent.is_at_least_as_expressive_as(classical)
    assert not classical.is_at_least_as_expressive_as(paraconsistent)

    absent = paraconsistent.features_absent_from(classical)
    assert SemanticFeature.CONTRADICTION_TOLERANCE in absent


def test_modal_statement_missing_feature_in_classical_universe():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    statement = next(
        item for item in modal.statements
        if item.name == "necessary_truth_statement"
    )

    missing = classical.missing_features_for(statement)

    assert SemanticFeature.MODAL_NECESSITY in missing
    assert not classical.supports_all_required_features(statement)


def test_intuitionistic_statement_requires_constructive_witness():
    universe = intuitionistic_finite_universe()

    statement = next(iter(universe.statements))

    assert statement.requires(SemanticFeature.CONSTRUCTIVE_WITNESS)
    assert universe.supports_all_required_features(statement)
    assert len(universe.inadmissible_statements()) == 0


def test_custom_universe_admissibility():
    statement = FiniteStatement.from_features(
        name="resource_sensitive_statement",
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.RESOURCE_SENSITIVITY,
        ],
    )

    weak_universe = FiniteLogicalUniverse.build(
        name="Weak Universe",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement],
    )

    assert len(weak_universe.admissible_statements()) == 0
    assert len(weak_universe.inadmissible_statements()) == 1
    assert SemanticFeature.RESOURCE_SENSITIVITY in weak_universe.missing_features_for(statement)


def test_standard_rigor_universes():
    universes = standard_rigor_universes()

    assert len(universes) == 4
    names = {universe.name for universe in universes}

    assert "Finite Classical Universe" in names
    assert "Finite Paraconsistent Universe" in names
    assert "Finite Modal Universe" in names
    assert "Finite Intuitionistic Universe" in names
