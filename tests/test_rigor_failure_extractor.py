"""
Tests for failure extraction.
"""

from src.rigor.failure_extractor import (
    ExtractedFailureCase,
    FailureExtractionReport,
    FailureExtractor,
)
from src.rigor.failure_taxonomy import FailureKind
from src.rigor.finite_universe import SemanticFeature
from src.rigor.satisfaction_search import SatisfactionSearchRunner


def test_extract_from_cases_returns_report():
    satisfaction_report = SatisfactionSearchRunner().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    extraction_report = FailureExtractor().extract_from_cases(satisfaction_report.cases)

    assert isinstance(extraction_report, FailureExtractionReport)
    assert extraction_report.failure_count() > 0
    assert extraction_report.has_failures()
    assert "FailureExtractionReport" in extraction_report.describe()


def test_extracted_failure_case_exists():
    report = FailureExtractor().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    failure = report.failures[0]

    assert isinstance(failure, ExtractedFailureCase)
    assert failure.failure_kind() != FailureKind.NO_FAILURE
    assert failure.search_case.has_distortion()
    assert "ExtractedFailureCase" in failure.describe()


def test_counts_by_kind():
    report = FailureExtractor().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    counts = report.counts_by_kind()

    assert isinstance(counts, dict)
    assert sum(counts.values()) == report.failure_count()
    assert report.failure_count() > 0


def test_by_kind_filters_failures():
    report = FailureExtractor().run(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )

    undefined_failures = report.by_kind(FailureKind.UNDEFINED_TRANSLATION)

    assert isinstance(undefined_failures, tuple)
    assert len(undefined_failures) > 0
    assert all(failure.failure_kind() == FailureKind.UNDEFINED_TRANSLATION for failure in undefined_failures)


def test_run_with_two_features_finds_failures():
    report = FailureExtractor().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=2,
    )

    assert report.failure_count() > 0
    assert report.has_failures()
