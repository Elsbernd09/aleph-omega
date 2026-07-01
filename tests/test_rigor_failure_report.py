"""
Tests for failure laboratory report generation.
"""

from pathlib import Path

from src.rigor.failure_report import FailureLabReport, FailureLabReportBuilder
from src.rigor.finite_universe import SemanticFeature


def small_report():
    return FailureLabReportBuilder().build(
        features=(SemanticFeature.CLASSICAL_TRUTH,),
        max_feature_set_size=1,
    )


def test_failure_lab_report_exists():
    report = small_report()

    assert isinstance(report, FailureLabReport)
    assert report.failure_count() > 0
    assert "FailureLabReport" in report.describe()


def test_failure_lab_counts_by_kind():
    report = small_report()

    counts = report.counts_by_kind()

    assert isinstance(counts, dict)
    assert sum(counts.values()) == report.failure_count()


def test_failure_lab_sample_failures():
    report = small_report()

    samples = report.sample_failures(limit=3)

    assert len(samples) > 0
    assert len(samples) <= 3


def test_failure_lab_markdown_contains_sections():
    report = small_report()
    markdown = FailureLabReportBuilder().to_markdown(report)

    assert "# Failure Laboratory Report" in markdown
    assert "Counts by Failure Kind" in markdown
    assert "Sample Extracted Failures" in markdown
    assert "Correct Research Claim" in markdown


def test_failure_lab_write_markdown(tmp_path):
    report = small_report()
    output_path = tmp_path / "failure_lab_report.md"

    written = FailureLabReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Failure Laboratory Report" in written.read_text()
