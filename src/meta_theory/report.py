"""
Intelligence report generator for Project ℵω.

This module turns global system metrics into a readable research report.

The report is designed for project introspection: what is strong, what is weak,
what needs human review, and what the next research actions should be.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.meta_theory.metrics import (
    MetricScore,
    ResearchRiskLevel,
    SystemHealthGrade,
    SystemMetricBundle,
)


class ReportPriority(str, Enum):
    """
    Priority level for intelligence report recommendations.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


@dataclass(frozen=True)
class ReportFinding:
    """
    One finding in the intelligence report.
    """

    title: str
    priority: ReportPriority
    explanation: str
    recommended_action: str
    metadata: Optional[Dict[str, str]] = None

    def describe(self) -> str:
        """
        Returns a readable finding.
        """

        return (
            f"Finding: {self.title}\n"
            f"Priority: {self.priority.value}\n"
            f"Explanation: {self.explanation}\n"
            f"Recommended action: {self.recommended_action}"
        )


@dataclass(frozen=True)
class IntelligenceReport:
    """
    Top-level intelligence report for Project ℵω.
    """

    title: str
    metric_bundle: SystemMetricBundle
    executive_summary: str
    strongest_layers: List[MetricScore] = field(default_factory=list)
    weakest_layers: List[MetricScore] = field(default_factory=list)
    findings: List[ReportFinding] = field(default_factory=list)
    next_actions: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, str]] = None

    def finding_count(self) -> int:
        """
        Counts findings.
        """

        return len(self.findings)

    def urgent_finding_count(self) -> int:
        """
        Counts urgent findings.
        """

        return sum(1 for finding in self.findings if finding.priority == ReportPriority.URGENT)

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        strongest_text = "\n".join(
            f"- {metric.name}: {metric.normalized_value()} ({metric.grade.value})"
            for metric in self.strongest_layers
        ) or "- none"

        weakest_text = "\n".join(
            f"- {metric.name}: {metric.normalized_value()} ({metric.grade.value})"
            for metric in self.weakest_layers
        ) or "- none"

        findings_text = "\n\n".join(
            finding.describe() for finding in self.findings
        ) or "No findings."

        actions_text = "\n".join(
            f"- {action}" for action in self.next_actions
        ) or "- none"

        limitations_text = "\n".join(
            f"- {limitation}" for limitation in self.limitations
        ) or "- none"

        return (
            f"{self.title}\n"
            f"{'=' * len(self.title)}\n\n"
            f"Executive Summary\n"
            f"-----------------\n"
            f"{self.executive_summary}\n\n"
            f"Overall Metrics\n"
            f"---------------\n"
            f"{self.metric_bundle.describe()}\n\n"
            f"Strongest Layers\n"
            f"----------------\n"
            f"{strongest_text}\n\n"
            f"Weakest Layers\n"
            f"--------------\n"
            f"{weakest_text}\n\n"
            f"Findings\n"
            f"--------\n"
            f"{findings_text}\n\n"
            f"Recommended Next Actions\n"
            f"------------------------\n"
            f"{actions_text}\n\n"
            f"Limitations\n"
            f"-----------\n"
            f"{limitations_text}"
        )


class IntelligenceReportGenerator:
    """
    Generates intelligence reports from system metric bundles.
    """

    def generate(self, bundle: SystemMetricBundle) -> IntelligenceReport:
        """
        Generates one intelligence report.
        """

        layer_scores = [
            bundle.axiom_engine_score,
            bundle.universe_engine_score,
            bundle.bridge_engine_score,
            bundle.cognitive_layer_score,
            bundle.formalization_layer_score,
        ]

        strongest_layers = sorted(
            layer_scores,
            key=lambda metric: metric.normalized_value(),
            reverse=True,
        )[:2]

        weakest_layers = sorted(
            layer_scores,
            key=lambda metric: metric.normalized_value(),
        )[:2]

        findings = self._findings(bundle, weakest_layers)
        next_actions = self._next_actions(bundle, weakest_layers, findings)
        limitations = self._limitations()

        executive_summary = self._executive_summary(bundle)

        return IntelligenceReport(
            title="Project ℵω Intelligence Report",
            metric_bundle=bundle,
            executive_summary=executive_summary,
            strongest_layers=strongest_layers,
            weakest_layers=weakest_layers,
            findings=findings,
            next_actions=next_actions,
            limitations=limitations,
            metadata={
                "overall_grade": bundle.overall_score.grade.value,
                "research_risk": bundle.research_risk.value,
            },
        )

    @staticmethod
    def _executive_summary(bundle: SystemMetricBundle) -> str:
        """
        Builds the executive summary.
        """

        return (
            f"Project ℵω currently has an overall system score of "
            f"{bundle.overall_score.normalized_value()} with grade "
            f"'{bundle.overall_score.grade.value}'. The research risk level is "
            f"'{bundle.research_risk.value}'. The system has working layers for "
            f"axiom generation, toy universe simulation, bridge translation, "
            f"cognitive formalization, and Lean-style formalization planning. "
            f"The current result is a structured computational research framework, "
            f"not a proof of new mathematics."
        )

    @staticmethod
    def _findings(
        bundle: SystemMetricBundle,
        weakest_layers: List[MetricScore],
    ) -> List[ReportFinding]:
        """
        Builds report findings.
        """

        findings: List[ReportFinding] = []

        if bundle.research_risk in {ResearchRiskLevel.HIGH, ResearchRiskLevel.EXTREME}:
            findings.append(
                ReportFinding(
                    title="High research review pressure",
                    priority=ReportPriority.URGENT,
                    explanation=(
                        "The system detected significant review pressure from "
                        "ambiguity, translation distortion, or blocked formalization plans."
                    ),
                    recommended_action=(
                        "Prioritize human review of the highest-burden formalization "
                        "plans and the most distorted bridge translations."
                    ),
                )
            )

        elif bundle.research_risk == ResearchRiskLevel.MEDIUM:
            findings.append(
                ReportFinding(
                    title="Moderate research review pressure",
                    priority=ReportPriority.HIGH,
                    explanation=(
                        "Some system components require human review before they can be "
                        "treated as mathematically serious."
                    ),
                    recommended_action=(
                        "Review the weakest layer scores and resolve the largest proof "
                        "obligations before adding more complexity."
                    ),
                )
            )

        for metric in weakest_layers:
            if metric.grade in {
                SystemHealthGrade.WEAK,
                SystemHealthGrade.CRITICAL,
                SystemHealthGrade.DEVELOPING,
            }:
                findings.append(
                    ReportFinding(
                        title=f"Weak layer detected: {metric.name}",
                        priority=ReportPriority.HIGH,
                        explanation=(
                            f"{metric.name} received score {metric.normalized_value()} "
                            f"with grade '{metric.grade.value}'. {metric.explanation}"
                        ),
                        recommended_action=(
                            "Inspect this layer's experiment output and add stronger "
                            "tests, clearer definitions, or better scoring logic."
                        ),
                    )
                )

        if bundle.formalization_layer_score.grade in {
            SystemHealthGrade.WEAK,
            SystemHealthGrade.CRITICAL,
            SystemHealthGrade.DEVELOPING,
        }:
            findings.append(
                ReportFinding(
                    title="Formalization layer needs strengthening",
                    priority=ReportPriority.HIGH,
                    explanation=(
                        "The formalization layer is the bridge from computational "
                        "experiments to theorem-prover credibility. Weakness here "
                        "limits the seriousness of the project."
                    ),
                    recommended_action=(
                        "Choose one small statement, define its terms precisely, and "
                        "work toward a real Lean file with no unresolved proof claims."
                    ),
                )
            )

        if not findings:
            findings.append(
                ReportFinding(
                    title="System architecture is structurally stable",
                    priority=ReportPriority.MEDIUM,
                    explanation=(
                        "No critical weakness was detected by the heuristic report generator."
                    ),
                    recommended_action=(
                        "Continue by adding richer experiments and improving mathematical "
                        "precision layer by layer."
                    ),
                )
            )

        return findings

    @staticmethod
    def _next_actions(
        bundle: SystemMetricBundle,
        weakest_layers: List[MetricScore],
        findings: List[ReportFinding],
    ) -> List[str]:
        """
        Builds next action list.
        """

        actions: List[str] = []

        if bundle.review_required:
            actions.append(
                "Review all high-priority findings before adding new abstract machinery."
            )

        for metric in weakest_layers:
            actions.append(
                f"Improve {metric.name} by inspecting its experiment output and adding clearer definitions or stronger tests."
            )

        if any("Formalization" in finding.title for finding in findings):
            actions.append(
                "Select one small theorem candidate and convert it into a minimal Lean file with explicit definitions."
            )

        actions.append(
            "Create a global experiment that runs all phases and writes a single project report."
        )

        actions.append(
            "Keep all claims honest: describe the system as a computational framework, not a solved mathematical theory."
        )

        return actions

    @staticmethod
    def _limitations() -> List[str]:
        """
        Lists report limitations.
        """

        return [
            "Metrics are heuristic and should not be interpreted as mathematical proof.",
            "Toy universes are simplified models, not full topoi or complete formal systems.",
            "Bridge translations are diagnostics, not categorical equivalences.",
            "Lean-style sketches containing `sorry` are unfinished and not machine-checked proofs.",
            "Human mathematical review is required before presenting any result as serious formal mathematics.",
        ]


if __name__ == "__main__":
    print("IntelligenceReportGenerator module loaded.")
