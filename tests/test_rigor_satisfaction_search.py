"""
Tests for satisfaction preservation stress search.
"""

from src.rigor.bridge_case_generator import BridgeCaseKind
from src.rigor.finite_universe import SemanticFeature
from src.rigor.model_search import FiniteModelGenerator
from src.rigor.satisfaction_search import (
    InterpretationCase,
    InterpretationGenerator,
    SatisfactionSearchCase,
    SatisfactionSearchReport,
    SatisfactionSearchRunner,
)


def test_interpretation_generator():
    universe = FiniteModelGenerator().generate_universe_cases(
        features=[SemanticFeature.CLASSICAL_TRUTH],
        max_feature_set_size=1,
    )[0].universe

    cases = InterpretationGenerator().generate_classical_interpretations(universe)

    assert len(cases) == 2
    assert all(isinstance(case, InterpretationCase) for case in cases)
    assert any(case.true_count == 1 for case in cases)
    assert any(case.false_count == 1 for case in cases)
    assert "InterpretationCase" in cases[0].describe()


def test_satisfaction_search_report_exists():
    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    assert isinstance(report, SatisfactionSearchReport)
    assert report.case_count() > 0
    assert "SatisfactionSearchReport" in report.describe()


def test_satisfaction_search_cases_exist():
    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    case = report.cases[0]

    assert isinstance(case, SatisfactionSearchCase)
    assert "SatisfactionSearchCase" in case.describe()


def test_search_contains_preserving_and_distortion_cases():
    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=2,
    )

    assert len(report.preserving_cases()) > 0
    assert len(report.distortion_cases()) > 0
    assert report.preservation_rate() > 0
    assert report.distortion_rate() > 0


def test_search_contains_bridge_kinds():
    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=2,
    )

    assert len(report.cases_by_kind(BridgeCaseKind.IDENTITY)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.COLLAPSE)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.EMPTY_PARTIAL)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.SAME_FEATURE)) > 0


def test_identity_cases_include_preservation():
    report = SatisfactionSearchRunner().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    identity_cases = report.cases_by_kind(BridgeCaseKind.IDENTITY)

    assert len(identity_cases) > 0
    assert any(case.preserves_satisfaction() for case in identity_cases)


def test_empty_partial_cases_can_distort():
    report = SatisfactionSearchRunner().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    empty_cases = report.cases_by_kind(BridgeCaseKind.EMPTY_PARTIAL)

    assert len(empty_cases) > 0
    assert any(case.has_distortion() for case in empty_cases)
