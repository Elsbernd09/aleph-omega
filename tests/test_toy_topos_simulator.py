"""
Unit tests for the Project ℵω toy topos simulator layer.

These tests verify that Phase 4 can:
- represent internal statements,
- represent topos-inspired objects and morphisms,
- analyze statements inside universes,
- simulate statements across universes,
- classify results with the toy subobject classifier.
"""

from src.toy_topoi.internal_language import InternalLanguageAnalyzer
from src.toy_topoi.library import classical_universe, paraconsistent_universe, standard_universes
from src.toy_topoi.simulator import SimulationResult, StatementProfile, ToyToposSimulator
from src.toy_topoi.statements import (
    ProofStatus,
    Statement,
    StatementEvaluation,
    StatementKind,
    starter_statements,
)
from src.toy_topoi.subobject_classifier import (
    ClassificationStatus,
    ToySubobjectClassifier,
    classify_simulation_results,
)
from src.toy_topoi.topos_objects import (
    MorphismKind,
    ToposDiagram,
    ToposMorphism,
    ToposObject,
    ToposObjectKind,
    starter_topos_diagram,
)
from src.toy_topoi.truth_values import TruthValue


def test_statement_model_complexity_and_description():
    statement = Statement(
        name="Test Statement",
        raw_text="For every x, property P holds.",
        symbolic_form="forall x, P(x)",
        kind=StatementKind.PROPOSITION,
        free_variables=["x", "P", "x"],
        required_symbols=["forall", "property", "forall"],
        dependencies=["test_axiom"],
        notes="Testing statement model.",
    )

    assert statement.variable_count() == 2
    assert statement.symbol_count() == 2
    assert statement.dependency_count() == 1
    assert statement.structural_complexity() > 0
    assert "Test Statement" in statement.describe()


def test_statement_evaluation_description():
    evaluation = StatementEvaluation(
        statement_name="Test Statement",
        universe_name="Test Universe",
        truth_value=TruthValue.TRUE,
        proof_status=ProofStatus.UNTESTED,
        explanation="Test explanation.",
    )

    assert evaluation.truth_value == TruthValue.TRUE
    assert evaluation.proof_status == ProofStatus.UNTESTED
    assert "Test Statement" in evaluation.describe()


def test_starter_statements_load():
    statements = starter_statements()

    assert len(statements) >= 5
    assert all(isinstance(statement, Statement) for statement in statements)


def test_topos_object_model():
    obj = ToposObject(
        name="TruthObject",
        kind=ToposObjectKind.TRUTH_OBJECT,
        internal_symbols=["true", "false", "true"],
        properties=["classifies", "internal_truth"],
        universe_name="Test Universe",
    )

    assert obj.symbol_count() == 2
    assert obj.property_count() == 2
    assert obj.structural_weight() > 0
    assert "TruthObject" in obj.describe()


def test_topos_morphism_scores():
    morphism = ToposMorphism(
        name="truth_assignment",
        source="Statement",
        target="TruthObject",
        kind=MorphismKind.TRUTH_ASSIGNMENT,
        mapping_rule="assign statement to truth value",
        preserved_structure=["statement_identity", "truth_value"],
        lost_structure=["ambiguity"],
    )

    assert morphism.preservation_score() > 0
    assert morphism.distortion_score() >= 0
    assert "truth_assignment" in morphism.describe()


def test_topos_diagram_validation():
    diagram = starter_topos_diagram()

    assert isinstance(diagram, ToposDiagram)
    assert diagram.object_count() >= 3
    assert diagram.morphism_count() >= 2
    assert diagram.validate_references()
    assert diagram.average_preservation_score() > 0
    assert "Starter Internal Truth Diagram" in diagram.describe()


def test_internal_language_analyzer_returns_analysis():
    analyzer = InternalLanguageAnalyzer()
    statement = starter_statements()[0]
    universe = classical_universe()

    analysis = analyzer.analyze(statement, universe)

    assert analysis.statement_name == statement.name
    assert analysis.universe_name == universe.name
    assert 0.0 <= analysis.universe_fit_score <= 10.0
    assert 0.0 <= analysis.ambiguity_score <= 10.0
    assert 0.0 <= analysis.formalization_readiness <= 10.0
    assert isinstance(analysis.recommended_truth_value, TruthValue)
    assert isinstance(analysis.recommended_proof_status, ProofStatus)


def test_internal_language_analysis_to_evaluation():
    analyzer = InternalLanguageAnalyzer()
    statement = starter_statements()[0]
    universe = classical_universe()

    evaluation = analyzer.evaluate(statement, universe)

    assert isinstance(evaluation, StatementEvaluation)
    assert evaluation.statement_name == statement.name
    assert evaluation.universe_name == universe.name


def test_toy_topos_simulator_evaluates_one_pair():
    simulator = ToyToposSimulator(
        universes=[classical_universe()],
        statements=[starter_statements()[0]],
    )

    result = simulator.evaluate_statement_in_universe(
        statement=starter_statements()[0],
        universe=classical_universe(),
    )

    assert isinstance(result, SimulationResult)
    assert result.statement.name == starter_statements()[0].name
    assert result.universe.name == classical_universe().name
    assert "truth_value" in result.summary_row()


def test_toy_topos_simulator_profiles():
    simulator = ToyToposSimulator(
        universes=standard_universes(),
        statements=starter_statements(),
    )

    profiles = simulator.statement_profiles()

    assert len(profiles) == len(starter_statements())
    assert all(isinstance(profile, StatementProfile) for profile in profiles)
    assert all(profile.best_fit() is not None for profile in profiles)
    assert all(profile.worst_fit() is not None for profile in profiles)


def test_toy_topos_simulator_evaluate_all():
    universes = standard_universes()
    statements = starter_statements()

    simulator = ToyToposSimulator(
        universes=universes,
        statements=statements,
    )

    results = simulator.evaluate_all()

    assert len(results) == len(universes) * len(statements)
    assert all(isinstance(result, SimulationResult) for result in results)


def test_subobject_classifier_classifies_result():
    classifier = ToySubobjectClassifier()
    statement = starter_statements()[0]
    universe = classical_universe()

    classification = classifier.classify(
        statement=statement,
        universe=universe,
        truth_value=TruthValue.TRUE,
        proof_status=ProofStatus.UNTESTED,
        universe_fit_score=8.0,
        ambiguity_score=1.0,
    )

    assert classification.classification_status in set(ClassificationStatus)
    assert 0.0 <= classification.membership_score <= 10.0
    assert classification.statement_name == statement.name


def test_classify_simulation_results():
    simulator = ToyToposSimulator(
        universes=[classical_universe(), paraconsistent_universe()],
        statements=starter_statements()[:2],
    )

    results = simulator.evaluate_all()
    classifications = classify_simulation_results(results)

    assert len(classifications) == len(results)
    assert all(0.0 <= item.membership_score <= 10.0 for item in classifications)
