"""
Tests for generated quotient category completion report.
"""

from pathlib import Path

from src.rigor.generated_quotient_category_completion_report import (
    GeneratedQuotientCategoryArtifact,
    GeneratedQuotientCategoryCompletionReport,
    GeneratedQuotientCategoryCompletionReportBuilder,
)


def test_generated_quotient_category_completion_report_builds():
    report = GeneratedQuotientCategoryCompletionReportBuilder().build()

    assert isinstance(report, GeneratedQuotientCategoryCompletionReport)
    assert report.artifact_count() >= 9
    assert len(report.quotient_artifacts()) >= 6
    assert len(report.generated_artifacts()) >= 6
    assert len(report.verified_artifacts()) >= 5
    assert "GeneratedQuotientCategoryCompletionReport" in report.describe()


def test_generated_quotient_category_artifact_describe():
    report = GeneratedQuotientCategoryCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, GeneratedQuotientCategoryArtifact)
    assert "GeneratedQuotientCategoryArtifact" in artifact.describe()


def test_generated_quotient_category_completion_markdown_contains_core_claims():
    report = GeneratedQuotientCategoryCompletionReportBuilder().build()
    markdown = GeneratedQuotientCategoryCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Generated Quotient Category Completion Report" in markdown
    assert "generated quotient-category pipeline" in markdown
    assert "quotient morphism classes" in markdown
    assert "formal-stack gate" in markdown
    assert "Boundary" in markdown


def test_generated_quotient_category_completion_write_markdown(tmp_path):
    report = GeneratedQuotientCategoryCompletionReportBuilder().build()
    output_path = tmp_path / "generated_quotient_category_completion_report.md"

    written = GeneratedQuotientCategoryCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Quotient Category Completion Report" in written.read_text()
