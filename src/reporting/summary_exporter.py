"""
System summary exporter for Project ℵω.

This module converts system-level outputs into ResearchArtifact objects that
can be used by the Markdown report generator.

The exporter summarizes what the system has built and where review is needed.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from src.meta_theory.metrics import ResearchRiskLevel, SystemMetricBundle
from src.meta_theory.report import IntelligenceReport
from src.reporting.artifact import (
    ArtifactKind,
    ArtifactRisk,
    ArtifactStatus,
    ResearchArtifact,
    ResearchArtifactCollection,
)


@dataclass(frozen=True)
class ExportSummary:
    """
    Summary of an export operation.
    """

    collection: ResearchArtifactCollection
    artifact_count: int
    review_required_count: int
    average_confidence: float
    metadata: Optional[Dict[str, str]] = None

    def describe(self) -> str:
        """
        Returns a readable export summary.
        """

        return (
            f"ExportSummary\n"
            f"Collection: {self.collection.title}\n"
            f"Artifact count: {self.artifact_count}\n"
            f"Review required count: {self.review_required_count}\n"
            f"Average confidence: {self.average_confidence}"
        )


class SystemSummaryExporter:
    """
    Converts Project ℵω system metrics and intelligence reports into artifacts.
    """

    def export(
        self,
        metric_bundle: SystemMetricBundle,
        intelligence_report: IntelligenceReport,
    ) -> ExportSummary:
        """
        Exports a research artifact collection.
        """

        artifacts = [
            self._overall_system_artifact(metric_bundle),
            self._layer_artifact(
                title="Axiom Engine Summary",
                source_layer="generative_axioms",
                kind=ArtifactKind.AXIOM,
                score=metric_bundle.axiom_engine_score.normalized_value(),
                summary=metric_bundle.axiom_engine_score.explanation,
            ),
            self._layer_artifact(
                title="Toy Universe Engine Summary",
                source_layer="toy_topoi",
                kind=ArtifactKind.UNIVERSE,
                score=metric_bundle.universe_engine_score.normalized_value(),
                summary=metric_bundle.universe_engine_score.explanation,
            ),
            self._layer_artifact(
                title="Bridge Translation Engine Summary",
                source_layer="bridges",
                kind=ArtifactKind.BRIDGE_TRANSLATION,
                score=metric_bundle.bridge_engine_score.normalized_value(),
                summary=metric_bundle.bridge_engine_score.explanation,
            ),
            self._layer_artifact(
                title="Cognitive Morphism Layer Summary",
                source_layer="cognitive_morphism",
                kind=ArtifactKind.COGNITIVE_MORPHISM,
                score=metric_bundle.cognitive_layer_score.normalized_value(),
                summary=metric_bundle.cognitive_layer_score.explanation,
            ),
            self._layer_artifact(
                title="Neural-Symbolic Formalization Summary",
                source_layer="cognitive_morphism",
                kind=ArtifactKind.FORMALIZATION_PLAN,
                score=metric_bundle.formalization_layer_score.normalized_value(),
                summary=metric_bundle.formalization_layer_score.explanation,
            ),
            self._intelligence_report_artifact(intelligence_report),
        ]

        collection = ResearchArtifactCollection(
            title="Project ℵω Unified Research Artifacts",
            artifacts=artifacts,
            summary=(
                "This collection summarizes the major layers of Project ℵω: "
                "axiom generation, toy universe simulation, bridge translation, "
                "cognitive formalization, neural-symbolic planning, and "
                "meta-theory intelligence reporting."
            ),
            metadata={
                "overall_score": str(metric_bundle.overall_score.normalized_value()),
                "research_risk": metric_bundle.research_risk.value,
            },
        )

        return ExportSummary(
            collection=collection,
            artifact_count=collection.artifact_count(),
            review_required_count=collection.review_required_count(),
            average_confidence=collection.average_confidence(),
            metadata={
                "source": "SystemSummaryExporter",
            },
        )

    @staticmethod
    def _overall_system_artifact(metric_bundle: SystemMetricBundle) -> ResearchArtifact:
        """
        Builds the overall system summary artifact.
        """

        risk = SystemSummaryExporter._artifact_risk_from_research_risk(
            metric_bundle.research_risk
        )

        status = (
            ArtifactStatus.REVIEW_REQUIRED
            if metric_bundle.review_required
            else ArtifactStatus.READY_FOR_REPORT
        )

        return ResearchArtifact(
            title="Overall Project ℵω System Summary",
            kind=ArtifactKind.SYSTEM_SUMMARY,
            status=status,
            risk=risk,
            summary=metric_bundle.summary,
            key_points=[
                f"Overall score: {metric_bundle.overall_score.normalized_value()}",
                f"Overall grade: {metric_bundle.overall_score.grade.value}",
                f"Research risk: {metric_bundle.research_risk.value}",
                f"Review required: {metric_bundle.review_required}",
            ],
            limitations=[
                "The score is heuristic.",
                "The system does not prove new mathematics by itself.",
                "Human review is required before making serious claims.",
            ],
            source_layer="meta_theory",
            confidence_score=metric_bundle.overall_score.normalized_value(),
        )

    @staticmethod
    def _layer_artifact(
        title: str,
        source_layer: str,
        kind: ArtifactKind,
        score: float,
        summary: str,
    ) -> ResearchArtifact:
        """
        Builds an artifact for a project layer.
        """

        if score >= 7.0:
            status = ArtifactStatus.READY_FOR_REPORT
            risk = ArtifactRisk.MEDIUM
        elif score >= 5.0:
            status = ArtifactStatus.EXPERIMENTAL
            risk = ArtifactRisk.MEDIUM
        else:
            status = ArtifactStatus.REVIEW_REQUIRED
            risk = ArtifactRisk.HIGH

        return ResearchArtifact(
            title=title,
            kind=kind,
            status=status,
            risk=risk,
            summary=summary,
            key_points=[
                f"Layer score: {score}",
                "This layer has executable code and tests.",
                "Interpretation should remain bounded by the project's limitations.",
            ],
            limitations=[
                "Layer score is heuristic.",
                "Executable experiments are not equivalent to mathematical proof.",
            ],
            source_layer=source_layer,
            confidence_score=score,
        )

    @staticmethod
    def _intelligence_report_artifact(
        intelligence_report: IntelligenceReport,
    ) -> ResearchArtifact:
        """
        Builds an artifact for the intelligence report.
        """

        confidence = intelligence_report.metric_bundle.overall_score.normalized_value()

        risk = SystemSummaryExporter._artifact_risk_from_research_risk(
            intelligence_report.metric_bundle.research_risk
        )

        status = (
            ArtifactStatus.REVIEW_REQUIRED
            if intelligence_report.metric_bundle.review_required
            else ArtifactStatus.READY_FOR_REPORT
        )

        return ResearchArtifact(
            title="Meta-Theory Intelligence Report",
            kind=ArtifactKind.META_THEORY_REPORT,
            status=status,
            risk=risk,
            summary=intelligence_report.executive_summary,
            key_points=[
                f"Findings: {intelligence_report.finding_count()}",
                f"Urgent findings: {intelligence_report.urgent_finding_count()}",
                f"Next actions: {len(intelligence_report.next_actions)}",
            ],
            limitations=intelligence_report.limitations,
            source_layer="meta_theory",
            confidence_score=confidence,
            metadata={
                "report_title": intelligence_report.title,
            },
        )

    @staticmethod
    def _artifact_risk_from_research_risk(
        research_risk: ResearchRiskLevel,
    ) -> ArtifactRisk:
        """
        Converts research risk to artifact risk.
        """

        if research_risk == ResearchRiskLevel.LOW:
            return ArtifactRisk.LOW

        if research_risk == ResearchRiskLevel.MEDIUM:
            return ArtifactRisk.MEDIUM

        if research_risk == ResearchRiskLevel.HIGH:
            return ArtifactRisk.HIGH

        return ArtifactRisk.EXTREME


if __name__ == "__main__":
    print("SystemSummaryExporter module loaded.")
