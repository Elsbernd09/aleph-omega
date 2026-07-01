"""
Tests for manuscript completion report generation.
"""

from pathlib import Path

from src.rigor.manuscript_completion_report import (
    ManuscriptArtifact,
    ManuscriptCompletionReport,
    ManuscriptCompletionReportBuilder,
)


def test_manuscript_completion_report_builds():
    report = ManuscriptCompletionReportBuilder().build()

    assert isinstance(report, ManuscriptCompletionReport)
    assert report.artifact_count() >= 8
    assert len(report.completed_artifacts()) >= 8
    assert "ManuscriptCompletionReport" in report.describe()


def test_manuscript_artifact_describe():
    report = ManuscriptCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, ManuscriptArtifact)
    assert "ManuscriptArtifact" in artifact.describe()


def test_manuscript_completion_markdown_contains_public_framing():
    report = ManuscriptCompletionReportBuilder().build()
    markdown = ManuscriptCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Manuscript Completion Report" in markdown
    assert "Strongest Current Manuscript Claim" in markdown
    assert "Public Framing" in markdown
    assert "should not be framed" in markdown
    assert "Next Serious Milestones" in markdown


def test_manuscript_completion_write_markdown(tmp_path):
    report = ManuscriptCompletionReportBuilder().build()
    output_path = tmp_path / "manuscript_completion_report.md"

    written = ManuscriptCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Manuscript Completion Report" in written.read_text()
