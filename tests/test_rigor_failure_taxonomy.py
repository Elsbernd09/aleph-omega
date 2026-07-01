"""
Tests for failure taxonomy.
"""

from src.rigor.bridge_case_generator import BridgeCaseGenerator
from src.rigor.failure_taxonomy import (
    FailureClassification,
    FailureClassifier,
    FailureKind,
)
from src.rigor.finite_universe import SemanticFeature
from src.rigor.model_search import FiniteModelGenerator
from src.rigor.satisfaction_search import SatisfactionSearchRunner


def small_universe_cases():
    return FiniteModelGenerator().generate_universe_cases(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=1,
    )


def test_failure_kind_values():
    assert FailureKind.NO_FAILURE.value == "no_failure"
    assert FailureKind.UNDEFINED_TRANSLATION.value == "undefined_translation"
    assert FailureKind.FEATURE_MISMATCH.value == "feature_mismatch"


def test_classify_identity_bridge_as_no_failure():
    universe = small_universe_cases()[0].universe
    bridge_case = BridgeCaseGenerator().identity_case(universe)

    classification = FailureClassifier().classify_bridge_case(bridge_case)

    assert isinstance(classification, FailureClassification)
    assert classification.kind == FailureKind.NO_FAILURE
    assert not classification.is_failure()
    assert "FailureClassification" in classification.describe()


def test_classify_empty_partial_bridge_failure():
    universe = small_universe_cases()[0].universe
    bridge_case = BridgeCaseGenerator().empty_partial_case(universe, universe)

    classification = FailureClassifier().classify_bridge_case(bridge_case)

    assert classification.kind == FailureKind.PARTIAL_BRIDGE_FAILURE
    assert classification.is_failure()


def test_classify_satisfaction_cases_contains_failures():
    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    classifications = FailureClassifier().classify_many_satisfaction_cases(report.cases)

    assert len(classifications) == report.case_count()
    assert any(item.is_failure() for item in classifications)
    assert any(item.kind == FailureKind.NO_FAILURE for item in classifications)


def test_classify_distortion_case_not_no_failure():
    report = SatisfactionSearchRunner().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    distortion_case = report.distortion_cases()[0]

    classification = FailureClassifier().classify_satisfaction_case(distortion_case)

    assert classification.is_failure()
    assert classification.kind != FailureKind.NO_FAILURE
