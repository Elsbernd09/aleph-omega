"""
Global research evaluator for Project ℵω.

This module evaluates the full Project ℵω architecture across multiple layers:
- generative axioms,
- toy logical universes,
- bridge translations,
- cognitive morphisms,
- neural-symbolic formalization plans.

The evaluator is heuristic. It is designed to summarize research-system
behavior, not to prove mathematical correctness.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from src.bridges.distortion import DistortionReport
from src.cognitive_morphism.formalization_planner import FormalizationPlan
from src.cognitive_morphism.gap_analyzer import FormalizationGapReport
from src.generative_axioms.evaluator import AxiomScore
from src.meta_theory.metrics import (
    MetricScore,
    ResearchRiskLevel,
    SystemMetricBundle,
    grade_from_score,
    risk_from_review_pressure,
    weighted_overall_score,
)
from src.toy_topoi.comparator import UniverseComparison
from src.toy_topoi.simulator import SimulationResult


@dataclass(frozen=True)
class GlobalEvaluationInputs:
    """
    Inputs used by the global research evaluator.
    """

    axiom_scores: List[AxiomScore]
    universe_comparisons: List[UniverseComparison]
    simulation_results: List[SimulationResult]
    distortion_reports: List[DistortionReport]
    gap_reports: List[FormalizationGapReport]
    formalization_plans: List[FormalizationPlan]
    metadata: Optional[Dict[str, str]] = None

    def total_items(self) -> int:
        """
        Counts all input records.
        """

        return (
            len(self.axiom_scores)
            + len(self.universe_comparisons)
            + len(self.simulation_results)
            + len(self.distortion_reports)
            + len(self.gap_reports)
            + len(self.formalization_plans)
        )


class GlobalResearchEvaluator:
    """
    Evaluates the full Project ℵω system.
    """

    def evaluate(self, inputs: GlobalEvaluationInputs) -> SystemMetricBundle:
        """
        Produces a top-level system metric bundle.
        """

        axiom_score = self._axiom_engine_metric(inputs.axiom_scores)
        universe_score = self._universe_engine_metric(
            inputs.universe_comparisons,
            inputs.simulation_results,
        )
        bridge_score = self._bridge_engine_metric(inputs.distortion_reports)
        cognitive_score = self._cognitive_layer_metric(inputs.gap_reports)
        formalization_score = self._formalization_layer_metric(inputs.formalization_plans)

        overall_value = weighted_overall_score(
            axiom_score=axiom_score.normalized_value(),
            universe_score=universe_score.normalized_value(),
            bridge_score=bridge_score.normalized_value(),
            cognitive_score=cognitive_score.normalized_value(),
            formalization_score=formalization_score.normalized_value(),
        )

        human_review_items = self._human_review_items(inputs)
        severe_distortion_items = self._severe_distortion_items(inputs.distortion_reports)
        blocking_formalization_items = self._blocking_formalization_items(inputs.formalization_plans)

        research_risk = risk_from_review_pressure(
            human_review_items=human_review_items,
            severe_distortion_items=severe_distortion_items,
            blocking_formalization_items=blocking_formalization_items,
        )

        review_required = research_risk in {
            ResearchRiskLevel.MEDIUM,
            ResearchRiskLevel.HIGH,
            ResearchRiskLevel.EXTREME,
        }

        overall_score = MetricScore(
            name="Overall System Intelligence Score",
            value=overall_value,
            grade=grade_from_score(overall_value),
            explanation=(
                "Weighted score combining axiom generation, universe simulation, "
                "bridge translation, cognitive formalization, and proof-planning "
                "layers. This is a heuristic system-readiness score."
            ),
        )

        summary = self._summary(
            overall_score=overall_score,
            research_risk=research_risk,
            human_review_items=human_review_items,
            severe_distortion_items=severe_distortion_items,
            blocking_formalization_items=blocking_formalization_items,
            total_items=inputs.total_items(),
        )

        return SystemMetricBundle(
            axiom_engine_score=axiom_score,
            universe_engine_score=universe_score,
            bridge_engine_score=bridge_score,
            cognitive_layer_score=cognitive_score,
            formalization_layer_score=formalization_score,
            overall_score=overall_score,
            research_risk=research_risk,
            review_required=review_required,
            summary=summary,
            metadata={
                "total_items": str(inputs.total_items()),
                "human_review_items": str(human_review_items),
                "severe_distortion_items": str(severe_distortion_items),
                "blocking_formalization_items": str(blocking_formalization_items),
            },
        )

    @staticmethod
    def _axiom_engine_metric(axiom_scores: List[AxiomScore]) -> MetricScore:
        """
        Evaluates the generative axiom layer.
        """

        if not axiom_scores:
            value = 0.0
            explanation = "No axiom scores were provided."
        else:
            average_interest = sum(score.overall_interest for score in axiom_scores) / len(axiom_scores)
            average_stability = sum(score.stability for score in axiom_scores) / len(axiom_scores)
            average_expressivity = sum(score.expressivity for score in axiom_scores) / len(axiom_scores)

            value = (
                average_interest * 0.40
                + average_stability * 0.30
                + average_expressivity * 0.30
            )

            explanation = (
                f"Evaluated {len(axiom_scores)} axiom scores using average interest, "
                "stability, and expressivity."
            )

        value = round(max(0.0, min(10.0, value)), 2)

        return MetricScore(
            name="Axiom Engine Score",
            value=value,
            grade=grade_from_score(value),
            explanation=explanation,
        )

    @staticmethod
    def _universe_engine_metric(
        universe_comparisons: List[UniverseComparison],
        simulation_results: List[SimulationResult],
    ) -> MetricScore:
        """
        Evaluates the toy universe and simulator layer.
        """

        if not universe_comparisons and not simulation_results:
            value = 0.0
            explanation = "No universe comparisons or simulation results were provided."
        else:
            comparison_component = 0.0
            simulation_component = 0.0

            if universe_comparisons:
                comparison_component = (
                    sum(comparison.compatibility_score for comparison in universe_comparisons)
                    / len(universe_comparisons)
                )

            if simulation_results:
                simulation_component = (
                    sum(result.analysis.universe_fit_score for result in simulation_results)
                    / len(simulation_results)
                )

            if universe_comparisons and simulation_results:
                value = comparison_component * 0.45 + simulation_component * 0.55
            elif universe_comparisons:
                value = comparison_component
            else:
                value = simulation_component

            explanation = (
                f"Evaluated {len(universe_comparisons)} universe comparisons and "
                f"{len(simulation_results)} statement-universe simulation results."
            )

        value = round(max(0.0, min(10.0, value)), 2)

        return MetricScore(
            name="Universe Engine Score",
            value=value,
            grade=grade_from_score(value),
            explanation=explanation,
        )

    @staticmethod
    def _bridge_engine_metric(distortion_reports: List[DistortionReport]) -> MetricScore:
        """
        Evaluates the bridge translation layer.
        """

        if not distortion_reports:
            value = 0.0
            explanation = "No bridge distortion reports were provided."
        else:
            average_distortion = (
                sum(report.overall_distortion_index for report in distortion_reports)
                / len(distortion_reports)
            )

            value = 10.0 - average_distortion

            explanation = (
                f"Evaluated {len(distortion_reports)} bridge distortion reports. "
                "Lower translation distortion increases the bridge score."
            )

        value = round(max(0.0, min(10.0, value)), 2)

        return MetricScore(
            name="Bridge Engine Score",
            value=value,
            grade=grade_from_score(value),
            explanation=explanation,
        )

    @staticmethod
    def _cognitive_layer_metric(gap_reports: List[FormalizationGapReport]) -> MetricScore:
        """
        Evaluates the cognitive morphism layer.
        """

        if not gap_reports:
            value = 0.0
            explanation = "No formalization gap reports were provided."
        else:
            average_quality = (
                sum(report.formalization_quality_score for report in gap_reports)
                / len(gap_reports)
            )
            average_gap = sum(report.gap_index for report in gap_reports) / len(gap_reports)

            value = average_quality * 0.65 + (10.0 - average_gap) * 0.35

            explanation = (
                f"Evaluated {len(gap_reports)} formalization gap reports using "
                "formalization quality and gap severity."
            )

        value = round(max(0.0, min(10.0, value)), 2)

        return MetricScore(
            name="Cognitive Layer Score",
            value=value,
            grade=grade_from_score(value),
            explanation=explanation,
        )

    @staticmethod
    def _formalization_layer_metric(plans: List[FormalizationPlan]) -> MetricScore:
        """
        Evaluates the neural-symbolic formalization layer.
        """

        if not plans:
            value = 0.0
            explanation = "No formalization plans were provided."
        else:
            average_burden = sum(plan.plan_burden_score() for plan in plans) / len(plans)
            average_steps = sum(plan.step_count() for plan in plans) / len(plans)

            value = 10.0 - average_burden
            value += min(average_steps * 0.05, 0.5)

            explanation = (
                f"Evaluated {len(plans)} formalization plans. Lower proof burden "
                "and clearer step structure improve the score."
            )

        value = round(max(0.0, min(10.0, value)), 2)

        return MetricScore(
            name="Formalization Layer Score",
            value=value,
            grade=grade_from_score(value),
            explanation=explanation,
        )

    @staticmethod
    def _human_review_items(inputs: GlobalEvaluationInputs) -> int:
        """
        Counts items requiring human review.
        """

        count = 0

        count += sum(1 for report in inputs.gap_reports if report.review_urgency_score >= 6.0)
        count += sum(1 for plan in inputs.formalization_plans if plan.urgent_step_count() > 0)
        count += sum(1 for result in inputs.simulation_results if result.analysis.ambiguity_score >= 6.0)

        return count

    @staticmethod
    def _severe_distortion_items(reports: List[DistortionReport]) -> int:
        """
        Counts severe bridge distortions.
        """

        return sum(1 for report in reports if report.overall_distortion_index >= 6.0)

    @staticmethod
    def _blocking_formalization_items(plans: List[FormalizationPlan]) -> int:
        """
        Counts plans blocked by serious proof obligations.
        """

        return sum(1 for plan in plans if plan.obligation_report.formalization_blocked())

    @staticmethod
    def _summary(
        overall_score: MetricScore,
        research_risk: ResearchRiskLevel,
        human_review_items: int,
        severe_distortion_items: int,
        blocking_formalization_items: int,
        total_items: int,
    ) -> str:
        """
        Builds global summary.
        """

        return (
            f"Project ℵω evaluated {total_items} total research artifacts. "
            f"The overall system score is {overall_score.normalized_value()} "
            f"with grade '{overall_score.grade.value}'. Research risk is "
            f"'{research_risk.value}'. The evaluator detected {human_review_items} "
            f"human-review pressure item(s), {severe_distortion_items} severe "
            f"translation distortion item(s), and {blocking_formalization_items} "
            f"blocking formalization item(s). These results summarize system "
            f"structure and readiness, not mathematical proof completion."
        )


if __name__ == "__main__":
    print("GlobalResearchEvaluator module loaded.")
