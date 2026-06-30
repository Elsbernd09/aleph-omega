"""
System metrics model for Project ℵω.

This module defines top-level metrics for evaluating the whole architecture:
axioms, toy universes, bridge translations, cognitive morphisms, and
formalization plans.

The metrics are heuristic research diagnostics. They are not mathematical
proofs, admissions claims, or claims of solving open problems.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class SystemHealthGrade(str, Enum):
    """
    High-level health grade for part of the system.
    """

    EXCELLENT = "excellent"
    STRONG = "strong"
    DEVELOPING = "developing"
    WEAK = "weak"
    CRITICAL = "critical"


class ResearchRiskLevel(str, Enum):
    """
    Risk level for a research component.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass(frozen=True)
class MetricScore:
    """
    A named score with an explanation.
    """

    name: str
    value: float
    grade: SystemHealthGrade
    explanation: str
    metadata: Optional[Dict[str, str]] = None

    def normalized_value(self) -> float:
        """
        Returns score clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.value)), 2)

    def describe(self) -> str:
        """
        Returns a readable metric report.
        """

        return (
            f"MetricScore: {self.name}\n"
            f"Value: {self.normalized_value()}\n"
            f"Grade: {self.grade.value}\n"
            f"Explanation: {self.explanation}"
        )


@dataclass(frozen=True)
class SystemMetricBundle:
    """
    Top-level score bundle for the full project.
    """

    axiom_engine_score: MetricScore
    universe_engine_score: MetricScore
    bridge_engine_score: MetricScore
    cognitive_layer_score: MetricScore
    formalization_layer_score: MetricScore
    overall_score: MetricScore
    research_risk: ResearchRiskLevel
    review_required: bool
    summary: str
    metadata: Optional[Dict[str, str]] = None

    def score_dict(self) -> Dict[str, float]:
        """
        Returns compact numeric scores.
        """

        return {
            "axiom_engine_score": self.axiom_engine_score.normalized_value(),
            "universe_engine_score": self.universe_engine_score.normalized_value(),
            "bridge_engine_score": self.bridge_engine_score.normalized_value(),
            "cognitive_layer_score": self.cognitive_layer_score.normalized_value(),
            "formalization_layer_score": self.formalization_layer_score.normalized_value(),
            "overall_score": self.overall_score.normalized_value(),
        }

    def describe(self) -> str:
        """
        Returns a readable full score bundle.
        """

        return (
            f"SystemMetricBundle\n"
            f"Research risk: {self.research_risk.value}\n"
            f"Review required: {self.review_required}\n"
            f"Summary: {self.summary}\n\n"
            f"{self.axiom_engine_score.describe()}\n\n"
            f"{self.universe_engine_score.describe()}\n\n"
            f"{self.bridge_engine_score.describe()}\n\n"
            f"{self.cognitive_layer_score.describe()}\n\n"
            f"{self.formalization_layer_score.describe()}\n\n"
            f"{self.overall_score.describe()}"
        )


def grade_from_score(score: float) -> SystemHealthGrade:
    """
    Converts a 0-10 score into a system health grade.
    """

    if score >= 8.5:
        return SystemHealthGrade.EXCELLENT

    if score >= 7.0:
        return SystemHealthGrade.STRONG

    if score >= 5.0:
        return SystemHealthGrade.DEVELOPING

    if score >= 3.0:
        return SystemHealthGrade.WEAK

    return SystemHealthGrade.CRITICAL


def risk_from_review_pressure(
    human_review_items: int,
    severe_distortion_items: int,
    blocking_formalization_items: int,
) -> ResearchRiskLevel:
    """
    Converts review pressure into a research risk level.
    """

    pressure = 0
    pressure += human_review_items
    pressure += severe_distortion_items * 2
    pressure += blocking_formalization_items * 2

    if pressure >= 10:
        return ResearchRiskLevel.EXTREME

    if pressure >= 6:
        return ResearchRiskLevel.HIGH

    if pressure >= 3:
        return ResearchRiskLevel.MEDIUM

    return ResearchRiskLevel.LOW


def weighted_overall_score(
    axiom_score: float,
    universe_score: float,
    bridge_score: float,
    cognitive_score: float,
    formalization_score: float,
) -> float:
    """
    Computes weighted overall project score.
    """

    score = 0.0
    score += axiom_score * 0.18
    score += universe_score * 0.22
    score += bridge_score * 0.20
    score += cognitive_score * 0.18
    score += formalization_score * 0.22

    return round(max(0.0, min(10.0, score)), 2)


if __name__ == "__main__":
    demo = MetricScore(
        name="Demo Metric",
        value=7.6,
        grade=grade_from_score(7.6),
        explanation="Example metric for checking the metrics module.",
    )

    print(demo.describe())
