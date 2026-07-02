"""
Tests for generated semantic lab completion report.
"""

from pathlib import Path

from src.rigor.generated_semantic_lab_completion_report import (
    GeneratedSemanticLabArtifact,
    GeneratedSemanticLabCompletionReport,
    GeneratedSemanticLabCompletionReportBuilder,
)


def test_generated_semantic_lab_completion_report_builds():
    report = GeneratedSemanticLabCompletionReportBuilder().build()

    assert isinstance(report, GeneratedSemanticLabCompletionReport)
    assert report.artifact_count() >= 9
    assert len(report.generated_artifacts()) >= 6
    assert len(report.semantic_lab_artifacts()) >= 6
    assert len(report.verified_artifacts()) >= 8
    assert "GeneratedSemanticLabCompletionReport" in report.describe()


def test_generated_semantic_lab_artifact_describe():
    report = GeneratedSemanticLabCompletionReportBuilder().build()
    artifact = report.artifacts[0]

    assert isinstance(artifact, GeneratedSemanticLabArtifact)
    assert "GeneratedSemanticLabArtifact" in artifact.describe()


def test_generated_semantic_lab_completion_markdown_contains_core_claims():
    report = GeneratedSemanticLabCompletionReportBuilder().build()
    markdown = GeneratedSemanticLabCompletionReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Generated Semantic Lab Completion Report" in markdown
    assert "generated finite semantic lab" in markdown
    assert "quotient-category composition theorems" in markdown
    assert "reproducible experimental environment" in markdown
    assert "Boundary" in markdown


def test_generated_semantic_lab_completion_write_markdown(tmp_path):
    report = GeneratedSemanticLabCompletionReportBuilder().build()
    output_path = tmp_path / "generated_semantic_lab_completion_report.md"

    written = GeneratedSemanticLabCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Semantic Lab Completion Report" in written.read_text()
