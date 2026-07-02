"""
Tests for theorem-backed semantic lab report.
"""

from pathlib import Path

from src.rigor.theorem_backed_semantic_lab_report import (
    TheoremBackedSemanticLabArtifact,
    TheoremBackedSemanticLabReport,
    TheoremBackedSemanticLabReportBuilder,
)


def test_theorem_backed_semantic_lab_report_builds():
    report = TheoremBackedSemanticLabReportBuilder().build()

    assert isinstance(report, TheoremBackedSemanticLabReport)
    assert report.artifact_count() >= 9
    assert len(report.theorem_artifacts()) >= 4
    assert len(report.nontrivial_proof_artifacts()) >= 5
    assert len(report.generated_artifacts()) >= 3
    assert "TheoremBackedSemanticLabReport" in report.describe()


def test_theorem_backed_semantic_lab_artifact_describe():
    report = TheoremBackedSemanticLabReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, TheoremBackedSemanticLabArtifact)
    assert "TheoremBackedSemanticLabArtifact" in artifact.describe()


def test_theorem_backed_semantic_lab_markdown_contains_core_claims():
    report = TheoremBackedSemanticLabReportBuilder().build()
    markdown = TheoremBackedSemanticLabReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Theorem-Backed Semantic Lab Report" in markdown
    assert "Quotient.sound" in markdown
    assert "PreservationEquivalent" in markdown
    assert "pointwise translation equality" in markdown
    assert "Honest Boundary" in markdown


def test_theorem_backed_semantic_lab_write_markdown(tmp_path):
    report = TheoremBackedSemanticLabReportBuilder().build()
    output_path = tmp_path / "theorem_backed_semantic_lab_report.md"

    written = TheoremBackedSemanticLabReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Theorem-Backed Semantic Lab Report" in written.read_text()
