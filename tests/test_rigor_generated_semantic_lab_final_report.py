"""
Tests for generated semantic lab final report.
"""

from pathlib import Path

from src.rigor.generated_semantic_lab_final_report import (
    GeneratedSemanticLabFinalArtifact,
    GeneratedSemanticLabFinalReport,
    GeneratedSemanticLabFinalReportBuilder,
)


def test_generated_semantic_lab_final_report_builds():
    report = GeneratedSemanticLabFinalReportBuilder().build()

    assert isinstance(report, GeneratedSemanticLabFinalReport)
    assert report.artifact_count() >= 10
    assert len(report.semantic_lab_artifacts()) >= 7
    assert len(report.generated_artifacts()) >= 8
    assert len(report.mathlib_artifacts()) >= 3
    assert len(report.verified_artifacts()) >= 8
    assert "GeneratedSemanticLabFinalReport" in report.describe()


def test_generated_semantic_lab_final_artifact_describe():
    report = GeneratedSemanticLabFinalReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, GeneratedSemanticLabFinalArtifact)
    assert "GeneratedSemanticLabFinalArtifact" in artifact.describe()


def test_generated_semantic_lab_final_markdown_contains_core_claims():
    report = GeneratedSemanticLabFinalReportBuilder().build()
    markdown = GeneratedSemanticLabFinalReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Generated Semantic Lab Final Report" in markdown
    assert "generated finite semantic lab" in markdown
    assert "quotient-category composition theorems" in markdown
    assert "four systems, three morphisms" in markdown
    assert "Boundary" in markdown


def test_generated_semantic_lab_final_report_write_markdown(tmp_path):
    report = GeneratedSemanticLabFinalReportBuilder().build()
    output_path = tmp_path / "generated_semantic_lab_final_report.md"

    written = GeneratedSemanticLabFinalReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Semantic Lab Final Report" in written.read_text()
