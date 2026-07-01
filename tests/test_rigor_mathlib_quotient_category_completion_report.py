"""
Tests for Mathlib quotient category completion report.
"""

from pathlib import Path

from src.rigor.mathlib_quotient_category_completion_report import (
    MathlibQuotientCategoryArtifact,
    MathlibQuotientCategoryCompletionReport,
    MathlibQuotientCategoryCompletionReportBuilder,
)


def test_mathlib_quotient_category_completion_report_builds():
    report = MathlibQuotientCategoryCompletionReportBuilder().build()

    assert isinstance(report, MathlibQuotientCategoryCompletionReport)
    assert report.artifact_count() >= 10
    assert len(report.completed_artifacts()) >= 10
    assert len(report.mathlib_artifacts()) >= 7
    assert "MathlibQuotientCategoryCompletionReport" in report.describe()


def test_mathlib_quotient_category_artifact_describe():
    report = MathlibQuotientCategoryCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, MathlibQuotientCategoryArtifact)
    assert "MathlibQuotientCategoryArtifact" in artifact.describe()


def test_mathlib_quotient_category_markdown_contains_core_claims():
    report = MathlibQuotientCategoryCompletionReportBuilder().build()
    markdown = MathlibQuotientCategoryCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Mathlib Quotient Category Completion Report" in markdown
    assert "quotientFormalSystemCategory" in markdown
    assert "representative-independent composition" in markdown
    assert "real Mathlib `Category` instance" in markdown
    assert "experimental prototype" in markdown


def test_mathlib_quotient_category_write_markdown(tmp_path):
    report = MathlibQuotientCategoryCompletionReportBuilder().build()
    output_path = tmp_path / "mathlib_quotient_category_completion_report.md"

    written = MathlibQuotientCategoryCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Quotient Category Completion Report" in written.read_text()
