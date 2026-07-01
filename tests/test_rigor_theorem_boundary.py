"""
Tests for theorem boundary analysis.
"""

from src.rigor.failure_extractor import FailureExtractor
from src.rigor.finite_universe import SemanticFeature
from src.rigor.satisfaction_search import SatisfactionSearchRunner
from src.rigor.theorem_boundary import (
    BoundaryAnalysisReport,
    BoundaryClassification,
    BoundaryStatus,
    TheoremBoundaryAnalyzer,
)


def test_boundary_status_values():
    assert BoundaryStatus.VERIFIED_PRESERVATION.value == "verified_preservation"
    assert BoundaryStatus.VACUOUS_PRESERVATION.value == "vacuous_preservation"
    assert BoundaryStatus.SEMANTIC_DISTORTION.value == "semantic_distortion"


def test_boundary_analyzer_report_exists():
    report = TheoremBoundaryAnalyzer().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    assert isinstance(report, BoundaryAnalysisReport)
    assert report.case_count() > 0
    assert "BoundaryAnalysisReport" in report.describe()


def test_boundary_report_contains_success_and_failure():
    report = TheoremBoundaryAnalyzer().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    assert report.success_count() > 0
    assert report.failure_count() > 0


def test_classify_one_case():
    satisfaction_report = SatisfactionSearchRunner().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    classification = TheoremBoundaryAnalyzer().classify_satisfaction_case(
        satisfaction_report.cases[0]
    )

    assert isinstance(classification, BoundaryClassification)
    assert classification.status in set(BoundaryStatus)
    assert "BoundaryClassification" in classification.describe()


def test_boundary_counts_by_status():
    report = TheoremBoundaryAnalyzer().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    counts = report.counts_by_status()

    assert isinstance(counts, dict)
    assert sum(counts.values()) == report.case_count()


def test_analyze_extracted_failures():
    extraction_report = FailureExtractor().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    boundary_report = TheoremBoundaryAnalyzer().analyze_extracted_failures(
        extraction_report.failures
    )

    assert isinstance(boundary_report, BoundaryAnalysisReport)
    assert boundary_report.case_count() == extraction_report.failure_count()
    assert boundary_report.failure_count() == extraction_report.failure_count()


def test_verified_and_vacuous_statuses_appear():
    report = TheoremBoundaryAnalyzer().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    assert len(report.by_status(BoundaryStatus.VERIFIED_PRESERVATION)) > 0
    assert len(report.by_status(BoundaryStatus.VACUOUS_PRESERVATION)) > 0
