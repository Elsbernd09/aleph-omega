"""
Tests for Mathlib strengthening completion report.
"""

from pathlib import Path

from src.rigor.mathlib_strengthening_completion_report import (
    MathlibStrengtheningArtifact,
    MathlibStrengtheningCompletionReport,
    MathlibStrengtheningCompletionReportBuilder,
)


def test_mathlib_strengthening_completion_report_builds():
    report = MathlibStrengtheningCompletionReportBuilder().build()

    assert isinstance(report, MathlibStrengtheningCompletionReport)
    assert report.artifact_count() >= 10
    assert len(report.mathlib_checked_artifacts()) >= 4
    assert len(report.experimental_artifacts()) >= 1
    assert "MathlibStrengtheningCompletionReport" in report.describe()


def test_mathlib_strengthening_artifact_describe():
    report = MathlibStrengtheningCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, MathlibStrengtheningArtifact)
    assert "MathlibStrengtheningArtifact" in artifact.describe()


def test_mathlib_strengthening_markdown_contains_core_claims():
    report = MathlibStrengtheningCompletionReportBuilder().build()
    markdown = MathlibStrengtheningCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Mathlib Strengthening Completion Report" in markdown
    assert "quotient category prototype" in markdown
    assert "representative-independent quotient composition" in markdown
    assert "concrete three-system preservation chain" in markdown
    assert "PhD-Level" in markdown


def test_mathlib_strengthening_write_markdown(tmp_path):
    report = MathlibStrengtheningCompletionReportBuilder().build()
    output_path = tmp_path / "mathlib_strengthening_completion_report.md"

    written = MathlibStrengtheningCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Strengthening Completion Report" in written.read_text()
