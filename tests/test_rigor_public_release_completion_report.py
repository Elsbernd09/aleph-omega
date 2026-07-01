"""
Tests for public release completion report generation.
"""

from pathlib import Path

from src.rigor.public_release_completion_report import (
    PublicReleaseArtifact,
    PublicReleaseCompletionReport,
    PublicReleaseCompletionReportBuilder,
)


def test_public_release_completion_report_builds():
    report = PublicReleaseCompletionReportBuilder().build()

    assert isinstance(report, PublicReleaseCompletionReport)
    assert report.artifact_count() >= 10
    assert len(report.completed_artifacts()) >= 10
    assert "PublicReleaseCompletionReport" in report.describe()


def test_public_release_artifact_describe():
    report = PublicReleaseCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, PublicReleaseArtifact)
    assert "PublicReleaseArtifact" in artifact.describe()


def test_public_release_completion_markdown_contains_core_claims():
    report = PublicReleaseCompletionReportBuilder().build()
    markdown = PublicReleaseCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Public Release Completion Report" in markdown
    assert "Strongest Current Public Claim" in markdown
    assert "Public Boundary" in markdown
    assert "docs/verification_status.md" in markdown
    assert "./scripts/check_formal_stack.sh" in markdown


def test_public_release_completion_write_markdown(tmp_path):
    report = PublicReleaseCompletionReportBuilder().build()
    output_path = tmp_path / "public_release_completion_report.md"

    written = PublicReleaseCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Public Release Completion Report" in written.read_text()
