"""
Tests for Bridge Distortion Theorem stress search.
"""

from src.rigor.bridge_case_generator import BridgeCaseKind
from src.rigor.bridge_distortion_search import (
    BridgeDistortionSearchCase,
    BridgeDistortionSearchReport,
    BridgeDistortionSearchRunner,
)
from src.rigor.finite_universe import SemanticFeature


def small_report():
    return BridgeDistortionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=2,
    )


def test_bridge_distortion_search_report_exists():
    report = small_report()

    assert isinstance(report, BridgeDistortionSearchReport)
    assert report.case_count() > 0
    assert "BridgeDistortionSearchReport" in report.describe()


def test_bridge_distortion_search_cases_exist():
    report = small_report()

    case = report.cases[0]

    assert isinstance(case, BridgeDistortionSearchCase)
    assert "BridgeDistortionSearchCase" in case.describe()


def test_bridge_distortion_theorem_survives_generated_search():
    report = small_report()

    assert report.theorem_survived_search()
    assert len(report.counterexamples()) == 0


def test_search_contains_nonvacuous_and_vacuous_instances():
    report = small_report()

    assert len(report.nonvacuous_instances()) > 0
    assert len(report.vacuous_instances()) > 0


def test_search_contains_all_bridge_case_kinds():
    report = small_report()

    assert len(report.cases_by_kind(BridgeCaseKind.IDENTITY)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.COLLAPSE)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.EMPTY_PARTIAL)) > 0
    assert len(report.cases_by_kind(BridgeCaseKind.SAME_FEATURE)) > 0


def test_larger_search_survives():
    report = BridgeDistortionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ),
        max_feature_set_size=2,
    )

    assert report.case_count() > small_report().case_count()
    assert report.theorem_survived_search()
    assert len(report.counterexamples()) == 0
