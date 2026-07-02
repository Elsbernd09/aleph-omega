"""
Tests for generated quotient export completion report.
"""

from pathlib import Path

from src.rigor.generated_quotient_export_completion_report import (
    GeneratedQuotientExportArtifact,
    GeneratedQuotientExportCompletionReport,
    GeneratedQuotientExportCompletionReportBuilder,
)


def test_generated_quotient_export_completion_report_builds():
    report = GeneratedQuotientExportCompletionReportBuilder().build()

    assert isinstance(report, GeneratedQuotientExportCompletionReport)
    assert report.artifact_count() >= 8
    assert len(report.generated_artifacts()) >= 5
    assert len(report.quotient_artifacts()) >= 5
    assert len(report.verified_artifacts()) >= 5
    assert "GeneratedQuotientExportCompletionReport" in report.describe()


def test_generated_quotient_export_artifact_describe():
    report = GeneratedQuotientExportCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, GeneratedQuotientExportArtifact)
    assert "GeneratedQuotientExportArtifact" in artifact.describe()


def test_generated_quotient_export_completion_markdown_contains_core_claims():
    report = GeneratedQuotientExportCompletionReportBuilder().build()
    markdown = GeneratedQuotientExportCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Generated Quotient Export Completion Report" in markdown
    assert "Python-generated Mathlib quotient export path" in markdown
    assert "finite quotient-category composition theorem" in markdown
    assert "formal-stack gate" in markdown
    assert "Boundary" in markdown


def test_generated_quotient_export_completion_write_markdown(tmp_path):
    report = GeneratedQuotientExportCompletionReportBuilder().build()
    output_path = tmp_path / "generated_quotient_export_completion_report.md"

    written = GeneratedQuotientExportCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Quotient Export Completion Report" in written.read_text()
