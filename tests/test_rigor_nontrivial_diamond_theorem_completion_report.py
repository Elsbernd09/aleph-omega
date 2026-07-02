"""
Tests for non-rfl diamond theorem completion report.
"""

from pathlib import Path

from src.rigor.nontrivial_diamond_theorem_completion_report import (
    NontrivialDiamondTheoremArtifact,
    NontrivialDiamondTheoremCompletionReport,
    NontrivialDiamondTheoremCompletionReportBuilder,
)


def test_nontrivial_diamond_theorem_completion_report_builds():
    report = NontrivialDiamondTheoremCompletionReportBuilder().build()

    assert isinstance(report, NontrivialDiamondTheoremCompletionReport)
    assert report.artifact_count() >= 10
    assert len(report.theorem_artifacts()) >= 6
    assert len(report.non_rfl_artifacts()) >= 5
    assert len(report.generated_artifacts()) >= 3
    assert "NontrivialDiamondTheoremCompletionReport" in report.describe()


def test_nontrivial_diamond_theorem_artifact_describe():
    report = NontrivialDiamondTheoremCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, NontrivialDiamondTheoremArtifact)
    assert "NontrivialDiamondTheoremArtifact" in artifact.describe()


def test_nontrivial_diamond_theorem_markdown_contains_core_claims():
    report = NontrivialDiamondTheoremCompletionReportBuilder().build()
    markdown = NontrivialDiamondTheoremCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Non-rfl Diamond Theorem Completion Report" in markdown
    assert "Quotient.sound" in markdown
    assert "PreservationEquivalent" in markdown
    assert "pointwise translation equality" in markdown
    assert "Boundary" in markdown


def test_nontrivial_diamond_theorem_completion_write_markdown(tmp_path):
    report = NontrivialDiamondTheoremCompletionReportBuilder().build()
    output_path = tmp_path / "nontrivial_diamond_theorem_completion_report.md"

    written = NontrivialDiamondTheoremCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Non-rfl Diamond Theorem Completion Report" in written.read_text()
