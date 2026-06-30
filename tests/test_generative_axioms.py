"""
Unit tests for the Project ℵω Generative Axiom Engine.

These tests verify that the first implementation can:
- represent axioms,
- load the starter axiom library,
- score axioms,
- generate candidate axioms,
- rank candidates.
"""

from src.generative_axioms.axiom import Axiom, AxiomDomain, AxiomStatus
from src.generative_axioms.evaluator import AxiomEvaluator, AxiomScore
from src.generative_axioms.generator import AxiomGenerator
from src.generative_axioms.library import foundational_axioms, find_axiom_by_name, get_axiom_names


def test_axiom_model_basic_methods():
    axiom = Axiom(
        name="Test Axiom",
        informal_statement="A test object has a test property.",
        symbolic_sketch="test_property(x)",
        domains=[AxiomDomain.GENERAL_FOUNDATIONS],
        symbols_used=["test_property", "x", "test_property"],
        compatible_universes=["classical"],
        dependencies=["test_dependency"],
        notes="Used only for testing.",
        status=AxiomStatus.HAND_DESIGNED,
    )

    assert axiom.name == "Test Axiom"
    assert axiom.symbol_count() == 2
    assert axiom.dependency_count() == 1
    assert axiom.universe_span() == 1
    assert "general_foundations" in axiom.domain_names()
    assert "Test Axiom" in axiom.short_label()
    assert "Informal statement" in axiom.describe()


def test_foundational_axiom_library_loads():
    axioms = foundational_axioms()

    assert len(axioms) >= 5
    assert all(isinstance(axiom, Axiom) for axiom in axioms)

    names = get_axiom_names()

    assert "Contextual Identity" in names
    assert "Truth Relativity" in names


def test_find_axiom_by_name():
    axiom = find_axiom_by_name("Contextual Identity")

    assert axiom.name == "Contextual Identity"
    assert AxiomDomain.IDENTITY in axiom.domains


def test_find_axiom_by_name_raises_for_missing_axiom():
    try:
        find_axiom_by_name("This Axiom Does Not Exist")
    except ValueError as error:
        assert "No axiom found" in str(error)
    else:
        raise AssertionError("Expected ValueError for missing axiom")


def test_axiom_evaluator_returns_scores():
    axioms = foundational_axioms()
    evaluator = AxiomEvaluator(reference_axioms=axioms)

    score = evaluator.evaluate(axioms[0])

    assert isinstance(score, AxiomScore)

    for value in score.as_dict().values():
        assert 0.0 <= value <= 10.0


def test_axiom_evaluator_ranks_axioms():
    axioms = foundational_axioms()
    evaluator = AxiomEvaluator(reference_axioms=axioms)

    ranked = evaluator.rank_axioms(axioms)

    assert len(ranked) == len(axioms)

    scores = [score.overall_interest for _, score in ranked]

    assert scores == sorted(scores, reverse=True)


def test_axiom_generator_creates_candidates():
    generator = AxiomGenerator()
    generated = generator.generate_all()

    assert len(generated) > 0
    assert all(isinstance(axiom, Axiom) for axiom in generated)
    assert any(axiom.status == AxiomStatus.GENERATED for axiom in generated)


def test_axiom_generator_mutates_seed_axioms():
    seed_axioms = foundational_axioms()
    generator = AxiomGenerator()

    generated = generator.generate_all(seed_axioms=seed_axioms)

    assert len(generated) > len(seed_axioms)
    assert any(axiom.status == AxiomStatus.MUTATED for axiom in generated)
