"""
Tests for Lean packaging completion report generation.
"""

from pathlib import Path

from src.rigor.lean_packaging_completion_report import (
    LeanPackagingArtifact,
    LeanPackagingCompletionReport,
    LeanPackagingCompletionReportBuilder,
)


def test_lean_packaging_completion_report_builds():
    report = LeanPackagingCompletionReportBuilder().build()

    assert isinstance(report, LeanPackagingCompletionReport)
    assert report.artifact_count() >= 8
    assert len(report.completed_artifacts()) >= 8
    assert len(report.ci_artifacts()) >= 1
    assert "LeanPackagingCompletionReport" in report.describe()


def test_lean_packaging_artifact_describe():
    report = LeanPackagingCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, LeanPackagingArtifact)
    assert "LeanPackagingArtifact" in artifact.describe()


def test_lean_packaging_completion_markdown_contains_core_claims():
    report = LeanPackagingCompletionReportBuilder().build()
    markdown = LeanPackagingCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Lean Packaging Completion Report" in markdown
    assert "Lake project scaffold" in markdown
    assert "Unified formal stack checker" in markdown
    assert "GitHub Actions formal CI" in markdown
    assert "not a Mathlib Category instance" in markdown


def test_lean_packaging_completion_write_markdown(tmp_path):
    report = LeanPackagingCompletionReportBuilder().build()
    output_path = tmp_path / "lean_packaging_completion_report.md"

    written = LeanPackagingCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Lean Packaging Completion Report" in written.read_text()
