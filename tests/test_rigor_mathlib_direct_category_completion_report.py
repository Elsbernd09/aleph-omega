"""
Tests for Mathlib direct category completion report.
"""

from pathlib import Path

from src.rigor.mathlib_direct_category_completion_report import (
    MathlibDirectCategoryArtifact,
    MathlibDirectCategoryCompletionReport,
    MathlibDirectCategoryCompletionReportBuilder,
)


def test_mathlib_direct_category_completion_report_builds():
    report = MathlibDirectCategoryCompletionReportBuilder().build()

    assert isinstance(report, MathlibDirectCategoryCompletionReport)
    assert report.artifact_count() >= 8
    assert len(report.completed_artifacts()) >= 4
    assert len(report.mathlib_checked_artifacts()) >= 4
    assert "MathlibDirectCategoryCompletionReport" in report.describe()


def test_mathlib_direct_category_artifact_describe():
    report = MathlibDirectCategoryCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, MathlibDirectCategoryArtifact)
    assert "MathlibDirectCategoryArtifact" in artifact.describe()


def test_mathlib_direct_category_markdown_contains_claims():
    report = MathlibDirectCategoryCompletionReportBuilder().build()
    markdown = MathlibDirectCategoryCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Mathlib Direct Category Completion Report" in markdown
    assert "formalSystemCategory" in markdown
    assert "real Category instance" in markdown
    assert "not yet the quotient category" in markdown
    assert "PhD-Level Upgrade" in markdown


def test_mathlib_direct_category_write_markdown(tmp_path):
    report = MathlibDirectCategoryCompletionReportBuilder().build()
    output_path = tmp_path / "mathlib_direct_category_completion_report.md"

    written = MathlibDirectCategoryCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Direct Category Completion Report" in written.read_text()
