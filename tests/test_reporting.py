"""
Unit tests for Project ℵω reporting layer.

These tests verify that Phase 9 can:
- represent research artifacts,
- collect artifacts,
- generate Markdown reports,
- export system summaries,
- run the reporting pipeline.
"""

from src.meta_theory.metrics import (
    MetricScore,
    ResearchRiskLevel,
    SystemHealthGrade,
    SystemMetricBundle,
)
from src.meta_theory.report import IntelligenceReportGenerator
from src.reporting.artifact import (
    ArtifactKind,
    ArtifactRisk,
    ArtifactStatus,
    ResearchArtifact,
    ResearchArtifactCollection,
    demo_artifact_collection,
)
from src.reporting.markdown_generator import MarkdownReport, MarkdownReportGenerator
from src.reporting.summary_exporter import ExportSummary, SystemSummaryExporter


def demo_metric_bundle() -> SystemMetricBundle:
    axiom = MetricScore(
        name="Axiom Engine Score",
        value=7.5,
        grade=SystemHealthGrade.STRONG,
        explanation="Demo axiom score.",
    )

    universe = MetricScore(
        name="Universe Engine Score",
        value=7.0,
        grade=SystemHealthGrade.STRONG,
        explanation="Demo universe score.",
    )

    bridge = MetricScore(
        name="Bridge Engine Score",
        value=6.5,
        grade=SystemHealthGrade.DEVELOPING,
        explanation="Demo bridge score.",
    )

    cognitive = MetricScore(
        name="Cognitive Layer Score",
        value=7.2,
        grade=SystemHealthGrade.STRONG,
        explanation="Demo cognitive score.",
    )

    formalization = MetricScore(
        name="Formalization Layer Score",
        value=5.8,
        grade=SystemHealthGrade.DEVELOPING,
        explanation="Demo formalization score.",
    )

    overall = MetricScore(
        name="Overall System Intelligence Score",
        value=6.8,
        grade=SystemHealthGrade.DEVELOPING,
        explanation="Demo overall score.",
    )

    return SystemMetricBundle(
        axiom_engine_score=axiom,
        universe_engine_score=universe,
        bridge_engine_score=bridge,
        cognitive_layer_score=cognitive,
        formalization_layer_score=formalization,
        overall_score=overall,
        research_risk=ResearchRiskLevel.MEDIUM,
        review_required=True,
        summary="Demo system summary.",
    )


def test_research_artifact_model():
    artifact = ResearchArtifact(
        title="Test Artifact",
        kind=ArtifactKind.SYSTEM_SUMMARY,
        status=ArtifactStatus.EXPERIMENTAL,
        risk=ArtifactRisk.MEDIUM,
        summary="Testing artifact behavior.",
        key_points=["Point one", "Point two"],
        limitations=["Limitation one"],
        source_layer="tests",
        confidence_score=7.0,
    )

    assert artifact.normalized_confidence() == 7.0
    assert artifact.requires_review() is False
    assert "Test Artifact" in artifact.describe()
    assert "## Test Artifact" in artifact.markdown_section()


def test_research_artifact_requires_review_when_high_risk():
    artifact = ResearchArtifact(
        title="Risky Artifact",
        kind=ArtifactKind.LEAN_SKETCH,
        status=ArtifactStatus.EXPERIMENTAL,
        risk=ArtifactRisk.HIGH,
        summary="Risky artifact.",
        confidence_score=8.0,
    )

    assert artifact.requires_review() is True


def test_research_artifact_collection():
    collection = demo_artifact_collection()

    assert isinstance(collection, ResearchArtifactCollection)
    assert collection.artifact_count() == 1
    assert collection.average_confidence() == 7.0
    assert "system_summary" in collection.artifacts_by_kind()
    assert "# Demo Artifact Collection" in collection.markdown()
    assert "ResearchArtifactCollection" in collection.describe()


def test_markdown_report_generator():
    collection = demo_artifact_collection()
    generator = MarkdownReportGenerator()

    report = generator.generate(collection)

    assert isinstance(report, MarkdownReport)
    assert report.artifact_count == collection.artifact_count()
    assert report.review_required_count == collection.review_required_count()
    assert report.line_count() > 0
    assert report.word_count() > 0
    assert "# Project ℵω Research Report" in report.markdown
    assert "Limitations" in report.markdown
    assert "MarkdownReport" in report.describe()


def test_markdown_report_save(tmp_path):
    collection = demo_artifact_collection()
    generator = MarkdownReportGenerator()
    report = generator.generate(collection)

    output_path = tmp_path / "report.md"
    generator.save(report, str(output_path))

    assert output_path.exists()
    assert "Project ℵω" in output_path.read_text()


def test_system_summary_exporter():
    bundle = demo_metric_bundle()
    intelligence_report = IntelligenceReportGenerator().generate(bundle)

    exporter = SystemSummaryExporter()
    export_summary = exporter.export(
        metric_bundle=bundle,
        intelligence_report=intelligence_report,
    )

    assert isinstance(export_summary, ExportSummary)
    assert export_summary.artifact_count >= 7
    assert export_summary.collection.artifact_count() == export_summary.artifact_count
    assert export_summary.review_required_count >= 1
    assert export_summary.average_confidence >= 0.0
    assert "ExportSummary" in export_summary.describe()


def test_full_reporting_pipeline():
    bundle = demo_metric_bundle()
    intelligence_report = IntelligenceReportGenerator().generate(bundle)

    exporter = SystemSummaryExporter()
    export_summary = exporter.export(bundle, intelligence_report)

    markdown_generator = MarkdownReportGenerator()
    markdown_report = markdown_generator.generate(
        collection=export_summary.collection,
        title="Project ℵω Test Report",
    )

    assert markdown_report.artifact_count == export_summary.artifact_count
    assert markdown_report.review_required_count == export_summary.review_required_count
    assert "Project ℵω Test Report" in markdown_report.markdown
    assert "Human Review Queue" in markdown_report.markdown
    assert "Recommended Next Steps" in markdown_report.markdown
