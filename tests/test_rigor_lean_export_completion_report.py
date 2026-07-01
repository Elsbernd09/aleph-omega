"""
Tests for Python-to-Lean export completion report.
"""

from pathlib import Path

from src.rigor.lean_export_completion_report import (
    LeanExportArtifact,
    LeanExportCompletionReport,
    LeanExportCompletionReportBuilder,
)


def test_lean_export_completion_report_builds():
    report = LeanExportCompletionReportBuilder().build()

    assert isinstance(report, LeanExportCompletionReport)
    assert report.artifact_count() >= 8
    assert len(report.lean_verified_artifacts()) >= 4
    assert len(report.exporter_artifacts()) >= 2
    assert "LeanExportCompletionReport" in report.describe()


def test_lean_export_artifact_describe():
    report = LeanExportCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, LeanExportArtifact)
    assert "LeanExportArtifact" in artifact.describe()


def test_lean_export_completion_markdown_contains_core_claims():
    report = LeanExportCompletionReportBuilder().build()
    markdown = LeanExportCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Python-to-Lean Export Completion Report" in markdown
    assert "Python-to-Lean export pipeline" in markdown
    assert "finite satisfaction-preserving morphisms" in markdown
    assert "formal-stack gate" in markdown
    assert "Boundary" in markdown


def test_lean_export_completion_write_markdown(tmp_path):
    report = LeanExportCompletionReportBuilder().build()
    output_path = tmp_path / "lean_export_completion_report.md"

    written = LeanExportCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Python-to-Lean Export Completion Report" in written.read_text()
