"""
Formalization planner for Project ℵω.

This module turns formalization targets, Lean-style sketches, and proof
obligation reports into an ordered action plan.

The purpose is to make theorem-prover work manageable: what must be defined,
what must be assumed, what must be proven, and what needs human review.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.cognitive_morphism.formalization_target import FormalizationTarget
from src.cognitive_morphism.lean_sketch import LeanSketch
from src.cognitive_morphism.proof_obligation import (
    ObligationKind,
    ObligationSeverity,
    ProofObligation,
    ProofObligationReport,
)


class PlanStepKind(str, Enum):
    """
    Type of formalization plan step.
    """

    DEFINE_OBJECT = "define_object"
    STATE_ASSUMPTION = "state_assumption"
    ENCODE_SEMANTICS = "encode_semantics"
    REPLACE_SORRY = "replace_sorry"
    SIMPLIFY_STATEMENT = "simplify_statement"
    HUMAN_REVIEW = "human_review"
    VERIFY_WITH_LEAN = "verify_with_lean"


class PlanPriority(str, Enum):
    """
    Priority level for a plan step.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class PlanReadinessGrade(str, Enum):
    """
    Overall readiness grade for a formalization plan.
    """

    READY_FOR_SKETCHING = "ready_for_sketching"
    NEEDS_FOUNDATIONS = "needs_foundations"
    NEEDS_SEMANTIC_ENCODING = "needs_semantic_encoding"
    BLOCKED_BY_PROOFS = "blocked_by_proofs"
    NEEDS_HUMAN_REDESIGN = "needs_human_redesign"


@dataclass(frozen=True)
class FormalizationPlanStep:
    """
    One ordered step in a formalization plan.
    """

    order: int
    kind: PlanStepKind
    priority: PlanPriority
    title: str
    description: str
    related_obligation_name: Optional[str] = None
    estimated_difficulty: float = 0.0
    suggested_output: str = ""
    metadata: Optional[Dict[str, str]] = None

    def difficulty_score(self) -> float:
        """
        Returns difficulty clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.estimated_difficulty)), 2)

    def describe(self) -> str:
        """
        Returns a readable plan step.
        """

        return (
            f"Step {self.order}: {self.title}\n"
            f"Kind: {self.kind.value}\n"
            f"Priority: {self.priority.value}\n"
            f"Difficulty: {self.difficulty_score()}\n"
            f"Related obligation: {self.related_obligation_name or 'none'}\n"
            f"Description: {self.description}\n"
            f"Suggested output: {self.suggested_output or 'none'}"
        )


@dataclass(frozen=True)
class FormalizationPlan:
    """
    Ordered formalization plan for one statement.
    """

    target: FormalizationTarget
    sketch: LeanSketch
    obligation_report: ProofObligationReport
    steps: List[FormalizationPlanStep] = field(default_factory=list)
    readiness_grade: PlanReadinessGrade = PlanReadinessGrade.NEEDS_FOUNDATIONS
    next_action: str = ""
    explanation: str = ""
    metadata: Optional[Dict[str, str]] = None

    def step_count(self) -> int:
        """
        Counts plan steps.
        """

        return len(self.steps)

    def urgent_step_count(self) -> int:
        """
        Counts urgent steps.
        """

        return sum(1 for step in self.steps if step.priority == PlanPriority.URGENT)

    def average_step_difficulty(self) -> float:
        """
        Computes average step difficulty.
        """

        if not self.steps:
            return 0.0

        total = sum(step.difficulty_score() for step in self.steps)
        return round(total / len(self.steps), 2)

    def plan_burden_score(self) -> float:
        """
        Computes total plan burden from 0 to 10.
        """

        score = 0.0
        score += min(self.step_count() * 0.45, 3.0)
        score += min(self.urgent_step_count() * 1.2, 3.0)
        score += self.average_step_difficulty() * 0.35
        score += self.obligation_report.obligation_index() * 0.25

        return round(max(0.0, min(10.0, score)), 2)

    def describe(self) -> str:
        """
        Returns a readable formalization plan.
        """

        steps_text = "\n\n".join(step.describe() for step in self.steps) or "No steps."

        return (
            f"FormalizationPlan\n"
            f"Statement: {self.target.statement.name}\n"
            f"Readiness grade: {self.readiness_grade.value}\n"
            f"Step count: {self.step_count()}\n"
            f"Urgent steps: {self.urgent_step_count()}\n"
            f"Average step difficulty: {self.average_step_difficulty()}\n"
            f"Plan burden score: {self.plan_burden_score()}\n"
            f"Next action: {self.next_action or 'none'}\n"
            f"Explanation: {self.explanation or 'none'}\n"
            f"\nPlan steps:\n{steps_text}"
        )


class FormalizationPlanner:
    """
    Builds ordered formalization plans from sketches and obligations.
    """

    def plan(
        self,
        target: FormalizationTarget,
        sketch: LeanSketch,
        obligation_report: ProofObligationReport,
    ) -> FormalizationPlan:
        """
        Builds a formalization plan.
        """

        steps = self._steps_from_obligations(obligation_report.obligations)
        steps.extend(self._final_verification_steps(sketch))

        ordered_steps = [
            FormalizationPlanStep(
                order=index + 1,
                kind=step.kind,
                priority=step.priority,
                title=step.title,
                description=step.description,
                related_obligation_name=step.related_obligation_name,
                estimated_difficulty=step.estimated_difficulty,
                suggested_output=step.suggested_output,
                metadata=step.metadata,
            )
            for index, step in enumerate(steps)
        ]

        readiness_grade = self._readiness_grade(obligation_report)
        next_action = self._next_action(ordered_steps, readiness_grade)
        explanation = self._explanation(target, readiness_grade, ordered_steps)

        return FormalizationPlan(
            target=target,
            sketch=sketch,
            obligation_report=obligation_report,
            steps=ordered_steps,
            readiness_grade=readiness_grade,
            next_action=next_action,
            explanation=explanation,
            metadata={
                "obligation_index": str(obligation_report.obligation_index()),
                "sketch_status": sketch.status.value,
            },
        )

    def plan_many(
        self,
        targets: List[FormalizationTarget],
        sketches: List[LeanSketch],
        obligation_reports: List[ProofObligationReport],
    ) -> List[FormalizationPlan]:
        """
        Builds plans for aligned target/sketch/report lists.
        """

        return [
            self.plan(target, sketch, report)
            for target, sketch, report in zip(targets, sketches, obligation_reports)
        ]

    def _steps_from_obligations(
        self,
        obligations: List[ProofObligation],
    ) -> List[FormalizationPlanStep]:
        """
        Converts obligations into ordered plan steps.
        """

        steps: List[FormalizationPlanStep] = []

        for obligation in obligations:
            steps.append(self._step_from_obligation(obligation))

        return sorted(
            steps,
            key=lambda step: (
                self._priority_rank(step.priority),
                self._kind_rank(step.kind),
                -step.difficulty_score(),
            ),
        )

    @staticmethod
    def _step_from_obligation(obligation: ProofObligation) -> FormalizationPlanStep:
        """
        Converts one obligation into one plan step.
        """

        priority = FormalizationPlanner._priority_from_severity(obligation.severity)

        if obligation.kind == ObligationKind.MISSING_DEFINITION:
            return FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.DEFINE_OBJECT,
                priority=priority,
                title=obligation.name,
                description=obligation.description,
                related_obligation_name=obligation.name,
                estimated_difficulty=obligation.severity_score(),
                suggested_output="A precise Lean definition replacing the placeholder.",
            )

        if obligation.kind == ObligationKind.MISSING_ASSUMPTION:
            return FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.STATE_ASSUMPTION,
                priority=priority,
                title=obligation.name,
                description=obligation.description,
                related_obligation_name=obligation.name,
                estimated_difficulty=obligation.severity_score(),
                suggested_output="An explicit theorem hypothesis, axiom, or documented assumption.",
            )

        if obligation.kind == ObligationKind.SEMANTIC_ENCODING:
            return FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.ENCODE_SEMANTICS,
                priority=priority,
                title=obligation.name,
                description=obligation.description,
                related_obligation_name=obligation.name,
                estimated_difficulty=obligation.severity_score(),
                suggested_output="A custom semantic structure with truth conditions and rules.",
            )

        if obligation.kind == ObligationKind.SORRY_PLACEHOLDER:
            return FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.REPLACE_SORRY,
                priority=priority,
                title=obligation.name,
                description=obligation.description,
                related_obligation_name=obligation.name,
                estimated_difficulty=obligation.severity_score(),
                suggested_output="A completed Lean proof term or tactic proof.",
            )

        if obligation.kind == ObligationKind.HUMAN_REVIEW:
            return FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.HUMAN_REVIEW,
                priority=priority,
                title=obligation.name,
                description=obligation.description,
                related_obligation_name=obligation.name,
                estimated_difficulty=obligation.severity_score(),
                suggested_output="A revised mathematical statement and formalization strategy.",
            )

        return FormalizationPlanStep(
            order=0,
            kind=PlanStepKind.SIMPLIFY_STATEMENT,
            priority=priority,
            title=obligation.name,
            description=obligation.description,
            related_obligation_name=obligation.name,
            estimated_difficulty=obligation.severity_score(),
            suggested_output="A simpler statement with fewer undefined concepts.",
        )

    @staticmethod
    def _final_verification_steps(sketch: LeanSketch) -> List[FormalizationPlanStep]:
        """
        Adds final verification steps.
        """

        return [
            FormalizationPlanStep(
                order=0,
                kind=PlanStepKind.VERIFY_WITH_LEAN,
                priority=PlanPriority.MEDIUM,
                title="Run Lean verification",
                description=(
                    "After definitions, assumptions, semantic encodings, and proof "
                    "placeholders are resolved, run Lean to check the file."
                ),
                estimated_difficulty=4.0,
                suggested_output="A Lean file with no errors and no unjustified sorry placeholders.",
                metadata={
                    "current_sorry_count": str(sketch.sorry_count),
                },
            )
        ]

    @staticmethod
    def _priority_from_severity(severity: ObligationSeverity) -> PlanPriority:
        """
        Converts obligation severity into plan priority.
        """

        if severity == ObligationSeverity.CRITICAL:
            return PlanPriority.URGENT

        if severity == ObligationSeverity.HIGH:
            return PlanPriority.HIGH

        if severity == ObligationSeverity.MEDIUM:
            return PlanPriority.MEDIUM

        return PlanPriority.LOW

    @staticmethod
    def _priority_rank(priority: PlanPriority) -> int:
        """
        Sort rank for priority.
        """

        ranks = {
            PlanPriority.URGENT: 0,
            PlanPriority.HIGH: 1,
            PlanPriority.MEDIUM: 2,
            PlanPriority.LOW: 3,
        }

        return ranks[priority]

    @staticmethod
    def _kind_rank(kind: PlanStepKind) -> int:
        """
        Sort rank for step kind.
        """

        ranks = {
            PlanStepKind.HUMAN_REVIEW: 0,
            PlanStepKind.ENCODE_SEMANTICS: 1,
            PlanStepKind.DEFINE_OBJECT: 2,
            PlanStepKind.STATE_ASSUMPTION: 3,
            PlanStepKind.REPLACE_SORRY: 4,
            PlanStepKind.SIMPLIFY_STATEMENT: 5,
            PlanStepKind.VERIFY_WITH_LEAN: 6,
        }

        return ranks[kind]

    @staticmethod
    def _readiness_grade(report: ProofObligationReport) -> PlanReadinessGrade:
        """
        Computes overall readiness grade.
        """

        kinds = {obligation.kind for obligation in report.obligations}

        if ObligationKind.HUMAN_REVIEW in kinds and report.blocking_count() >= 2:
            return PlanReadinessGrade.NEEDS_HUMAN_REDESIGN

        if ObligationKind.SEMANTIC_ENCODING in kinds:
            return PlanReadinessGrade.NEEDS_SEMANTIC_ENCODING

        if ObligationKind.SORRY_PLACEHOLDER in kinds:
            return PlanReadinessGrade.BLOCKED_BY_PROOFS

        if ObligationKind.MISSING_DEFINITION in kinds or ObligationKind.MISSING_ASSUMPTION in kinds:
            return PlanReadinessGrade.NEEDS_FOUNDATIONS

        return PlanReadinessGrade.READY_FOR_SKETCHING

    @staticmethod
    def _next_action(
        steps: List[FormalizationPlanStep],
        readiness_grade: PlanReadinessGrade,
    ) -> str:
        """
        Chooses the next recommended action.
        """

        if not steps:
            return "No immediate action required."

        first = steps[0]

        if readiness_grade == PlanReadinessGrade.NEEDS_HUMAN_REDESIGN:
            return "Start with human review and redesign the statement before coding."

        return f"Begin with: {first.title}."

    @staticmethod
    def _explanation(
        target: FormalizationTarget,
        readiness_grade: PlanReadinessGrade,
        steps: List[FormalizationPlanStep],
    ) -> str:
        """
        Builds explanation.
        """

        return (
            f"The formalization plan for '{target.statement.name}' has readiness "
            f"grade '{readiness_grade.value}' and {len(steps)} ordered step(s). "
            f"The plan should be treated as a roadmap for future Lean work, not "
            f"as evidence that the theorem has been proven."
        )


def rank_plans_by_burden(plans: List[FormalizationPlan]) -> List[FormalizationPlan]:
    """
    Ranks plans from hardest/highest burden to easiest.
    """

    return sorted(plans, key=lambda plan: plan.plan_burden_score(), reverse=True)


def rank_plans_by_readiness(plans: List[FormalizationPlan]) -> List[FormalizationPlan]:
    """
    Ranks plans from easiest/lowest burden to hardest.
    """

    return sorted(plans, key=lambda plan: plan.plan_burden_score())


if __name__ == "__main__":
    from src.cognitive_morphism.formalization_target import FormalizationTargetBuilder
    from src.cognitive_morphism.formalizer import InformalFormalizer
    from src.cognitive_morphism.intuition import starter_intuitions
    from src.cognitive_morphism.lean_sketch import LeanSketchGenerator
    from src.cognitive_morphism.proof_obligation import ProofObligationAnalyzer

    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    sketch_generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    drafts = formalizer.formalize_many(starter_intuitions())
    targets = builder.build_many([draft.statement for draft in drafts])
    sketches = sketch_generator.generate_many(targets)
    reports = obligation_analyzer.analyze_many(sketches)
    plans = planner.plan_many(targets, sketches, reports)

    for plan in rank_plans_by_burden(plans):
        print(plan.describe())
        print("-" * 100)
