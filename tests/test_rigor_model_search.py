"""
Tests for finite model search.
"""

from src.rigor.finite_universe import SemanticFeature
from src.rigor.model_search import (
    FiniteModelGenerator,
    GeneratedBridgeCase,
    GeneratedUniverseCase,
    ModelSearchReport,
)


def test_feature_subset_generation():
    generator = FiniteModelGenerator()

    subsets = generator.feature_subsets(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_size=2,
    )

    assert len(subsets) == 3
    assert frozenset([SemanticFeature.CLASSICAL_TRUTH]) in subsets
    assert frozenset([SemanticFeature.MODAL_NECESSITY]) in subsets


def test_generate_universe_cases():
    generator = FiniteModelGenerator()

    cases = generator.generate_universe_cases(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=1,
    )

    assert len(cases) == 2
    assert all(isinstance(case, GeneratedUniverseCase) for case in cases)
    assert all(case.statement_count == 1 for case in cases)
    assert "GeneratedUniverseCase" in cases[0].describe()


def test_generate_bridge_cases():
    generator = FiniteModelGenerator()

    universe_cases = generator.generate_universe_cases(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=1,
    )

    bridge_cases = generator.generate_bridge_cases(universe_cases)

    assert len(bridge_cases) == 4
    assert all(isinstance(case, GeneratedBridgeCase) for case in bridge_cases)
    assert "GeneratedBridgeCase" in bridge_cases[0].describe()


def test_bridge_distortion_model_search_report():
    report = FiniteModelGenerator().run_bridge_distortion_search(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ],
        max_feature_set_size=2,
    )

    assert isinstance(report, ModelSearchReport)
    assert report.universe_count() > 0
    assert report.bridge_case_count() > 0
    assert report.theorem_survived_search()
    assert len(report.counterexamples()) == 0
    assert len(report.nonvacuous_instances()) > 0
    assert "ModelSearchReport" in report.describe()


def test_search_contains_vacuous_and_nonvacuous_instances():
    report = FiniteModelGenerator().run_bridge_distortion_search(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=2,
    )

    assert len(report.vacuous_instances()) > 0
    assert len(report.nonvacuous_instances()) > 0
    assert report.theorem_survived_search()
