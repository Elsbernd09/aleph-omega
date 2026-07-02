"""
Tests for generated Mathlib export completion report.
"""

from pathlib import Path

from src.rigor.mathlib_export_completion_report import (
    MathlibExportArtifact,
    MathlibExportCompletionReport,
    MathlibExportCompletionReportBuilder,
)


def test_mathlib_export_completion_report_builds():
    report = MathlibExportCompletionReportBuilder().build()

    assert isinstance(report, MathlibExportCompletionReport)
    assert report.artifact_count() >= 9
    assert len(report.generated_artifacts()) >= 4
    assert len(report.mathlib_verified_artifacts()) >= 5
    assert len(report.exporter_artifacts()) >= 2
    assert "MathlibExportCompletionReport" in report.describe()


def test_mathlib_export_artifact_describe():
    report = MathlibExportCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, MathlibExportArtifact)
    assert "MathlibExportArtifact" in artifact.describe()


def test_mathlib_export_completion_markdown_contains_core_claims():
    report = MathlibExportCompletionReportBuilder().build()
    markdown = MathlibExportCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Generated Mathlib Export Completion Report" in markdown
    assert "Python-to-Mathlib export pipeline" in markdown
    assert "experimental Mathlib category-theory track" in markdown
    assert "formal-stack gate" in markdown
    assert "Boundary" in markdown


def test_mathlib_export_completion_write_markdown(tmp_path):
    report = MathlibExportCompletionReportBuilder().build()
    output_path = tmp_path / "mathlib_export_completion_report.md"

    written = MathlibExportCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Mathlib Export Completion Report" in written.read_text()
