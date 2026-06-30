"""
Formalization gap analyzer for Project ℵω.

This module measures the gap between an informal mathematical intuition and
the symbolic statement produced from it.

The goal is to make formalization loss visible: what gets preserved, what gets
lost, what gets added, and where human review is needed.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from src.cognitive_morphism.formalizer import FormalizationDraft
from src.cognitive_morphism.morphism import CognitiveMorphism


class GapSeverity(str, Enum):
    """
    Severity of the intuition-to-formalization gap.
    """

    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    SEVERE = "severe"
    CRITICAL = "critical"


@dataclass(frozen=True)
class FormalizationGapReport:
    """
    Structured report on the gap between intuition and formalization.
    """

    intuition_name: str
    statement_name: str
    lost_property_count: int
    lost_metaphor_count: int
    added_structure_count: int
    property_preservation_score: float
    metaphor_preservation_score: float
    confidence: float
    meaning_drift_score: float
    formalization_quality_score: float
    review_urgency_score: float
    gap_index: float
    severity: GapSeverity
    explanation: str
    metadata: Optional[Dict[str, str]] = None

    def as_dict(self) -> Dict[str, object]:
        """
        Converts the report into dictionary form.
        """

        return {
            "intuition_name": self.intuition_name,
            "statement_name": self.statement_name,
            "lost_property_count": self.lost_property_count,
            "lost_metaphor_count": self.lost_metaphor_count,
            "added_structure_count": self.added_structure_count,
            "property_preservation_score": self.property_preservation_score,
            "metaphor_preservation_score": self.metaphor_preservation_score,
            "confidence": self.confidence,
            "meaning_drift_score": self.meaning_drift_score,
            "formalization_quality_score": self.formalization_quality_score,
            "review_urgency_score": self.review_urgency_score,
            "gap_index": self.gap_index,
            "severity": self.severity.value,
            "explanation": self.explanation,
        }

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"FormalizationGapReport\n"
            f"Intuition: {self.intuition_name}\n"
            f"Statement: {self.statement_name}\n"
            f"Lost property count: {self.lost_property_count}\n"
            f"Lost metaphor count: {self.lost_metaphor_count}\n"
            f"Added structure count: {self.added_structure_count}\n"
            f"Property preservation score: {self.property_preservation_score}\n"
            f"Metaphor preservation score: {self.metaphor_preservation_score}\n"
            f"Confidence: {self.confidence}\n"
            f"Meaning drift score: {self.meaning_drift_score}\n"
            f"Formalization quality score: {self.formalization_quality_score}\n"
            f"Review urgency score: {self.review_urgency_score}\n"
            f"Gap index: {self.gap_index}\n"
            f"Severity: {self.severity.value}\n"
            f"Explanation: {self.explanation}"
        )


class FormalizationGapAnalyzer:
    """
    Analyzes formalization gaps from cognitive morphisms or drafts.
    """

    def analyze_morphism(self, morphism: CognitiveMorphism) -> FormalizationGapReport:
        """
        Analyzes one cognitive morphism.
        """

        preservation = morphism.preservation

        lost_property_count = len(set(preservation.lost_properties))
        lost_metaphor_count = len(set(preservation.lost_metaphors))
        added_structure_count = preservation.added_structure_count()

        property_score = preservation.property_preservation_score()
        metaphor_score = preservation.metaphor_preservation_score()
        confidence = morphism.normalized_confidence()
        drift = morphism.normalized_meaning_drift()
        quality = morphism.formalization_quality_score()

        review_urgency = self._review_urgency_score(
            lost_property_count=lost_property_count,
            lost_metaphor_count=lost_metaphor_count,
            added_structure_count=added_structure_count,
            confidence=confidence,
            drift=drift,
            quality=quality,
            requires_review=morphism.requires_review(),
        )

        gap_index = self._gap_index(
            property_preservation_score=property_score,
            metaphor_preservation_score=metaphor_score,
            confidence=confidence,
            meaning_drift_score=drift,
            formalization_quality_score=quality,
            review_urgency_score=review_urgency,
        )

        severity = self._severity(gap_index)

        explanation = self._explanation(
            morphism=morphism,
            gap_index=gap_index,
            severity=severity,
            lost_property_count=lost_property_count,
            lost_metaphor_count=lost_metaphor_count,
            added_structure_count=added_structure_count,
        )

        return FormalizationGapReport(
            intuition_name=morphism.source_intuition.name,
            statement_name=morphism.target_statement.name,
            lost_property_count=lost_property_count,
            lost_metaphor_count=lost_metaphor_count,
            added_structure_count=added_structure_count,
            property_preservation_score=property_score,
            metaphor_preservation_score=metaphor_score,
            confidence=confidence,
            meaning_drift_score=drift,
            formalization_quality_score=quality,
            review_urgency_score=review_urgency,
            gap_index=gap_index,
            severity=severity,
            explanation=explanation,
            metadata={
                "morphism_status": morphism.status.value,
                "morphism_kind": morphism.kind.value,
                "requires_review": str(morphism.requires_review()),
            },
        )

    def analyze_draft(self, draft: FormalizationDraft) -> FormalizationGapReport:
        """
        Analyzes one formalization draft.
        """

        return self.analyze_morphism(draft.morphism)

    def analyze_many(self, drafts: List[FormalizationDraft]) -> List[FormalizationGapReport]:
        """
        Analyzes many formalization drafts.
        """

        return [self.analyze_draft(draft) for draft in drafts]

    @staticmethod
    def _review_urgency_score(
        lost_property_count: int,
        lost_metaphor_count: int,
        added_structure_count: int,
        confidence: float,
        drift: float,
        quality: float,
        requires_review: bool,
    ) -> float:
        """
        Computes how urgently a formalization needs human review.
        """

        score = 0.0
        score += lost_property_count * 1.4
        score += lost_metaphor_count * 0.7
        score += min(added_structure_count * 0.35, 1.5)
        score += max(0.0, 7.0 - confidence) * 0.55
        score += drift * 0.45
        score += max(0.0, 7.0 - quality) * 0.50

        if requires_review:
            score += 1.0

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _gap_index(
        property_preservation_score: float,
        metaphor_preservation_score: float,
        confidence: float,
        meaning_drift_score: float,
        formalization_quality_score: float,
        review_urgency_score: float,
    ) -> float:
        """
        Computes the overall formalization gap index from 0 to 10.
        """

        property_loss = 10.0 - property_preservation_score
        metaphor_loss = 10.0 - metaphor_preservation_score
        confidence_loss = 10.0 - confidence
        quality_loss = 10.0 - formalization_quality_score

        score = 0.0
        score += property_loss * 0.24
        score += metaphor_loss * 0.10
        score += confidence_loss * 0.16
        score += meaning_drift_score * 0.22
        score += quality_loss * 0.18
        score += review_urgency_score * 0.10

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _severity(gap_index: float) -> GapSeverity:
        """
        Converts gap index into severity.
        """

        if gap_index <= 1.0:
            return GapSeverity.MINIMAL

        if gap_index <= 2.25:
            return GapSeverity.LOW

        if gap_index <= 4.0:
            return GapSeverity.MODERATE

        if gap_index <= 5.75:
            return GapSeverity.HIGH

        if gap_index <= 7.5:
            return GapSeverity.SEVERE

        return GapSeverity.CRITICAL

    @staticmethod
    def _explanation(
        morphism: CognitiveMorphism,
        gap_index: float,
        severity: GapSeverity,
        lost_property_count: int,
        lost_metaphor_count: int,
        added_structure_count: int,
    ) -> str:
        """
        Builds a human-readable explanation.
        """

        return (
            f"The formalization from intuition '{morphism.source_intuition.name}' "
            f"to statement '{morphism.target_statement.name}' received gap index "
            f"{gap_index} with severity '{severity.value}'. It lost "
            f"{lost_property_count} desired properties and {lost_metaphor_count} "
            f"guiding metaphors, while adding {added_structure_count} formal "
            f"structures. The cognitive morphism quality score is "
            f"{morphism.formalization_quality_score()} and review requirement is "
            f"{morphism.requires_review()}. This is a heuristic gap analysis, "
            f"not a proof of formal correctness."
        )


def rank_gap_reports_by_severity(
    reports: List[FormalizationGapReport],
) -> List[FormalizationGapReport]:
    """
    Ranks reports from largest gap to smallest gap.
    """

    return sorted(reports, key=lambda report: report.gap_index, reverse=True)


def rank_gap_reports_by_quality(
    reports: List[FormalizationGapReport],
) -> List[FormalizationGapReport]:
    """
    Ranks reports from smallest gap to largest gap.
    """

    return sorted(reports, key=lambda report: report.gap_index)


if __name__ == "__main__":
    from src.cognitive_morphism.formalizer import InformalFormalizer
    from src.cognitive_morphism.intuition import starter_intuitions

    formalizer = InformalFormalizer()
    analyzer = FormalizationGapAnalyzer()

    drafts = formalizer.formalize_many(starter_intuitions())
    reports = analyzer.analyze_many(drafts)

    for report in rank_gap_reports_by_severity(reports):
        print(report.describe())
        print("-" * 100)
