"""
Tests for Lean/Python correspondence completion report.
"""

from pathlib import Path

from src.rigor.correspondence_completion_report import (
    CorrespondenceCompletionClaim,
    CorrespondenceCompletionReport,
    CorrespondenceCompletionReportBuilder,
)


def test_correspondence_completion_report_builds():
    report = CorrespondenceCompletionReportBuilder().build()

    assert isinstance(report, CorrespondenceCompletionReport)
    assert report.claim_count() >= 10
    assert len(report.completed_correspondences()) >= 7
    assert "CorrespondenceCompletionReport" in report.describe()


def test_correspondence_completion_claim_describe():
    report = CorrespondenceCompletionReportBuilder().build()
    claim = report.claims[0]

    assert isinstance(claim, CorrespondenceCompletionClaim)
    assert "CorrespondenceCompletionClaim" in claim.describe()


def test_correspondence_completion_markdown_contains_key_claims():
    report = CorrespondenceCompletionReportBuilder().build()
    markdown = CorrespondenceCompletionReportBuilder().to_markdown(report)

    assert "# Lean/Python Correspondence Completion Report" in markdown
    assert "AlephOmegaQuotientCategory" in markdown
    assert "PythonQuotientCategory" in markdown
    assert "Strongest Current Claim" in markdown
    assert "not fully machine-verified" in markdown


def test_correspondence_completion_write_markdown(tmp_path):
    report = CorrespondenceCompletionReportBuilder().build()
    output_path = tmp_path / "correspondence_completion_report.md"

    written = CorrespondenceCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Lean/Python Correspondence Completion Report" in written.read_text()
