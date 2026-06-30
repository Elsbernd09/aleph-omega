"""
Proof obligation model for Project ℵω.

This module identifies what remains unfinished in a Lean-style sketch.

A proof obligation is not a completed proof. It is a structured record of
what must be defined, assumed, justified, or reviewed before a formalization
can be considered serious.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.cognitive_morphism.lean_sketch import LeanSketch, LeanSketchStatus


class ObligationKind(str, Enum):
    """
    Type of proof/formalization obligation.
    """

    MISSING_DEFINITION = "missing_definition"
    MISSING_ASSUMPTION = "missing_assumption"
    UNPROVED_GOAL = "unproved_goal"
    SORRY_PLACEHOLDER = "sorry_placeholder"
    SEMANTIC_ENCODING = "semantic_encoding"
    TYPE_CHECKING_RISK = "type_checking_risk"
    HUMAN_REVIEW = "human_review"


class ObligationSeverity(str, Enum):
    """
    Severity of a proof obligation.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ObligationStatus(str, Enum):
    """
    Current status of a proof obligation.
    """

    OPEN = "open"
    PARTIALLY_ADDRESSED = "partially_addressed"
    BLOCKED = "blocked"
    RESOLVED = "resolved"


@dataclass(frozen=True)
class ProofObligation:
    """
    One required task before a sketch can become a serious formalization.
    """

    name: str
    kind: ObligationKind
    severity: ObligationSeverity
    status: ObligationStatus = ObligationStatus.OPEN
    description: str = ""
    suggested_resolution: str = ""
    related_statement_name: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def severity_score(self) -> float:
        """
        Converts severity into a numeric score.
        """

        scores = {
            ObligationSeverity.LOW: 2.0,
            ObligationSeverity.MEDIUM: 5.0,
            ObligationSeverity.HIGH: 7.5,
            ObligationSeverity.CRITICAL: 9.5,
        }

        return scores[self.severity]

    def is_blocking(self) -> bool:
        """
        Returns whether this obligation blocks serious formalization.
        """

        return (
            self.status != ObligationStatus.RESOLVED
            and self.severity in {
                ObligationSeverity.HIGH,
                ObligationSeverity.CRITICAL,
            }
        )

    def describe(self) -> str:
        """
        Returns a readable obligation report.
        """

        return (
            f"ProofObligation: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Severity: {self.severity.value}\n"
            f"Status: {self.status.value}\n"
            f"Blocking: {self.is_blocking()}\n"
            f"Related statement: {self.related_statement_name or 'none'}\n"
            f"Description: {self.description or 'none'}\n"
            f"Suggested resolution: {self.suggested_resolution or 'none'}"
        )


@dataclass(frozen=True)
class ProofObligationReport:
    """
    Collection of proof obligations for one Lean sketch.
    """

    sketch: LeanSketch
    obligations: List[ProofObligation] = field(default_factory=list)
    explanation: str = ""
    metadata: Optional[Dict[str, str]] = None

    def obligation_count(self) -> int:
        """
        Counts obligations.
        """

        return len(self.obligations)

    def blocking_count(self) -> int:
        """
        Counts blocking obligations.
        """

        return sum(1 for obligation in self.obligations if obligation.is_blocking())

    def average_severity_score(self) -> float:
        """
        Computes average severity score.
        """

        if not self.obligations:
            return 0.0

        total = sum(obligation.severity_score() for obligation in self.obligations)
        return round(total / len(self.obligations), 2)

    def unresolved_obligations(self) -> List[ProofObligation]:
        """
        Returns unresolved obligations.
        """

        return [
            obligation for obligation in self.obligations
            if obligation.status != ObligationStatus.RESOLVED
        ]

    def formalization_blocked(self) -> bool:
        """
        Returns whether the sketch is blocked by high-severity obligations.
        """

        return self.blocking_count() > 0

    def obligation_index(self) -> float:
        """
        Computes an overall proof-obligation index from 0 to 10.
        """

        score = 0.0
        score += min(self.obligation_count() * 0.7, 3.0)
        score += min(self.blocking_count() * 1.4, 4.0)
        score += self.average_severity_score() * 0.30
        score += min(self.sketch.sorry_count * 0.8, 2.0)

        return round(max(0.0, min(10.0, score)), 2)

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        obligations_text = "\n".join(
            obligation.describe() for obligation in self.obligations
        ) or "No obligations detected."

        return (
            f"ProofObligationReport\n"
            f"Statement: {self.sketch.target.statement.name}\n"
            f"Obligation count: {self.obligation_count()}\n"
            f"Blocking count: {self.blocking_count()}\n"
            f"Average severity score: {self.average_severity_score()}\n"
            f"Obligation index: {self.obligation_index()}\n"
            f"Formalization blocked: {self.formalization_blocked()}\n"
            f"Explanation: {self.explanation or 'none'}\n"
            f"\nObligations:\n{obligations_text}"
        )


class ProofObligationAnalyzer:
    """
    Extracts proof obligations from LeanSketch objects.
    """

    def analyze(self, sketch: LeanSketch) -> ProofObligationReport:
        """
        Produces a proof-obligation report for one sketch.
        """

        obligations: List[ProofObligation] = []

        obligations.extend(self._definition_obligations(sketch))
        obligations.extend(self._assumption_obligations(sketch))
        obligations.extend(self._sorry_obligations(sketch))
        obligations.extend(self._semantic_obligations(sketch))
        obligations.extend(self._review_obligations(sketch))

        explanation = self._explanation(sketch, obligations)

        return ProofObligationReport(
            sketch=sketch,
            obligations=obligations,
            explanation=explanation,
            metadata={
                "sketch_status": sketch.status.value,
                "sorry_count": str(sketch.sorry_count),
            },
        )

    def analyze_many(self, sketches: List[LeanSketch]) -> List[ProofObligationReport]:
        """
        Produces reports for many sketches.
        """

        return [self.analyze(sketch) for sketch in sketches]

    @staticmethod
    def _definition_obligations(sketch: LeanSketch) -> List[ProofObligation]:
        """
        Creates obligations for missing definitions.
        """

        obligations = []

        for definition in sketch.definitions_needed:
            obligations.append(
                ProofObligation(
                    name=f"Define {definition}",
                    kind=ObligationKind.MISSING_DEFINITION,
                    severity=ObligationSeverity.HIGH,
                    description=(
                        f"The sketch references '{definition}', but it is only "
                        "represented by a placeholder structure."
                    ),
                    suggested_resolution=(
                        f"Replace the placeholder for '{definition}' with a precise "
                        "Lean definition and supporting lemmas."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        return obligations

    @staticmethod
    def _assumption_obligations(sketch: LeanSketch) -> List[ProofObligation]:
        """
        Creates obligations for assumptions.
        """

        obligations = []

        for assumption in sketch.assumptions_needed:
            obligations.append(
                ProofObligation(
                    name=f"Justify assumption: {assumption}",
                    kind=ObligationKind.MISSING_ASSUMPTION,
                    severity=ObligationSeverity.MEDIUM,
                    description=(
                        f"The statement depends on the assumption '{assumption}'."
                    ),
                    suggested_resolution=(
                        "Either prove this assumption from earlier definitions, "
                        "state it explicitly as a hypothesis, or document why it "
                        "is accepted as an axiom."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        return obligations

    @staticmethod
    def _sorry_obligations(sketch: LeanSketch) -> List[ProofObligation]:
        """
        Creates obligations for sorry placeholders.
        """

        obligations = []

        for index in range(sketch.sorry_count):
            obligations.append(
                ProofObligation(
                    name=f"Resolve sorry placeholder {index + 1}",
                    kind=ObligationKind.SORRY_PLACEHOLDER,
                    severity=ObligationSeverity.CRITICAL,
                    description=(
                        "The generated Lean-style sketch contains an unfinished "
                        "`sorry` placeholder."
                    ),
                    suggested_resolution=(
                        "Replace `sorry` with a valid Lean proof term or tactic proof."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        return obligations

    @staticmethod
    def _semantic_obligations(sketch: LeanSketch) -> List[ProofObligation]:
        """
        Creates obligations for semantic encoding risks.
        """

        risk_notes = sketch.target.risk_notes.lower()
        obligations = []

        if "paraconsistent" in risk_notes:
            obligations.append(
                ProofObligation(
                    name="Encode paraconsistent semantics",
                    kind=ObligationKind.SEMANTIC_ENCODING,
                    severity=ObligationSeverity.CRITICAL,
                    description=(
                        "Ordinary Lean logic is classical/constructive depending on "
                        "configuration, but paraconsistent truth requires explicit encoding."
                    ),
                    suggested_resolution=(
                        "Define a custom truth-value structure and inference rules "
                        "before stating paraconsistent claims."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        if "modal semantics" in risk_notes:
            obligations.append(
                ProofObligation(
                    name="Encode modal semantics",
                    kind=ObligationKind.SEMANTIC_ENCODING,
                    severity=ObligationSeverity.HIGH,
                    description=(
                        "Modal operators such as possible and necessary require "
                        "explicit semantics."
                    ),
                    suggested_resolution=(
                        "Define possible worlds, accessibility relations, and modal "
                        "truth conditions before attempting the proof."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        if "context-dependence" in risk_notes:
            obligations.append(
                ProofObligation(
                    name="Define context dependence",
                    kind=ObligationKind.SEMANTIC_ENCODING,
                    severity=ObligationSeverity.HIGH,
                    description=(
                        "The statement depends on context-sensitive meaning."
                    ),
                    suggested_resolution=(
                        "Define an InterpretationContext type and specify how truth "
                        "or identity depends on context."
                    ),
                    related_statement_name=sketch.target.statement.name,
                )
            )

        return obligations

    @staticmethod
    def _review_obligations(sketch: LeanSketch) -> List[ProofObligation]:
        """
        Creates obligations when human review is required.
        """

        if sketch.status not in {
            LeanSketchStatus.NEEDS_HUMAN_REVIEW,
            LeanSketchStatus.NOT_RECOMMENDED,
        }:
            return []

        return [
            ProofObligation(
                name="Human review required",
                kind=ObligationKind.HUMAN_REVIEW,
                severity=ObligationSeverity.HIGH,
                description=(
                    "The sketch is not ready to be treated as a direct theorem."
                ),
                suggested_resolution=(
                    "Review the statement, definitions, assumptions, and semantics "
                    "before further formalization."
                ),
                related_statement_name=sketch.target.statement.name,
            )
        ]

    @staticmethod
    def _explanation(
        sketch: LeanSketch,
        obligations: List[ProofObligation],
    ) -> str:
        """
        Builds explanation for the report.
        """

        blocking = sum(1 for obligation in obligations if obligation.is_blocking())

        return (
            f"The Lean-style sketch for '{sketch.target.statement.name}' produced "
            f"{len(obligations)} proof obligation(s), including {blocking} blocking "
            f"obligation(s). These obligations must be resolved before the sketch "
            f"can be interpreted as serious formal mathematics."
        )


def rank_obligation_reports_by_burden(
    reports: List[ProofObligationReport],
) -> List[ProofObligationReport]:
    """
    Ranks reports from highest proof burden to lowest.
    """

    return sorted(reports, key=lambda report: report.obligation_index(), reverse=True)


def rank_obligation_reports_by_readiness(
    reports: List[ProofObligationReport],
) -> List[ProofObligationReport]:
    """
    Ranks reports from lowest proof burden to highest.
    """

    return sorted(reports, key=lambda report: report.obligation_index())


if __name__ == "__main__":
    from src.cognitive_morphism.formalization_target import FormalizationTargetBuilder
    from src.cognitive_morphism.formalizer import InformalFormalizer
    from src.cognitive_morphism.intuition import starter_intuitions
    from src.cognitive_morphism.lean_sketch import LeanSketchGenerator

    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    analyzer = ProofObligationAnalyzer()

    drafts = formalizer.formalize_many(starter_intuitions())
    targets = builder.build_many([draft.statement for draft in drafts])
    sketches = generator.generate_many(targets)
    reports = analyzer.analyze_many(sketches)

    for report in rank_obligation_reports_by_burden(reports):
        print(report.describe())
        print("-" * 100)
