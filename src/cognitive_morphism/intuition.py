"""
Intuition object model for Project ℵω.

This module represents informal mathematical intuitions before they are
translated into symbolic statements.

The purpose is to model the gap between human mathematical thought and
formal symbolic systems.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class IntuitionKind(str, Enum):
    """
    Broad type of human mathematical intuition.
    """

    ANALOGY = "analogy"
    VISUAL_GEOMETRIC = "visual_geometric"
    ALGEBRAIC_PATTERN = "algebraic_pattern"
    LOGICAL_PRINCIPLE = "logical_principle"
    PHYSICAL_METAPHOR = "physical_metaphor"
    CATEGORY_STRUCTURAL = "category_structural"
    CONTRADICTION_TOLERANCE = "contradiction_tolerance"
    MODAL_POSSIBILITY = "modal_possibility"
    CONSTRUCTIVE_EVIDENCE = "constructive_evidence"
    PRIME_STRUCTURE = "prime_structure"
    GENERATED_SPECULATION = "generated_speculation"


class ClarityLevel(str, Enum):
    """
    Human clarity level of an intuition.
    """

    VAGUE = "vague"
    PARTIAL = "partial"
    STRUCTURED = "structured"
    SYMBOL_READY = "symbol_ready"
    FORMALIZATION_READY = "formalization_ready"


class FormalizationRisk(str, Enum):
    """
    Risk that an intuition will lose meaning during formalization.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass(frozen=True)
class IntuitionObject:
    """
    Represents one informal mathematical intuition.

    Fields:
        name:
            Human-readable name.

        raw_intuition:
            The informal human idea.

        kind:
            Type of intuition.

        guiding_metaphors:
            Human analogies or metaphors used to understand the idea.

        candidate_symbols:
            Symbols that might represent the idea.

        implied_structures:
            Mathematical structures suggested by the intuition.

        desired_properties:
            Properties the formalization should preserve.

        clarity_level:
            How ready the intuition is for formalization.

        formalization_risk:
            Risk of losing meaning during formalization.

        notes:
            Human explanation.

        metadata:
            Optional extra information.
    """

    name: str
    raw_intuition: str
    kind: IntuitionKind
    guiding_metaphors: List[str] = field(default_factory=list)
    candidate_symbols: List[str] = field(default_factory=list)
    implied_structures: List[str] = field(default_factory=list)
    desired_properties: List[str] = field(default_factory=list)
    clarity_level: ClarityLevel = ClarityLevel.VAGUE
    formalization_risk: FormalizationRisk = FormalizationRisk.MEDIUM
    notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def metaphor_count(self) -> int:
        """
        Counts guiding metaphors.
        """

        return len(set(self.guiding_metaphors))

    def symbol_count(self) -> int:
        """
        Counts candidate symbols.
        """

        return len(set(self.candidate_symbols))

    def structure_count(self) -> int:
        """
        Counts implied structures.
        """

        return len(set(self.implied_structures))

    def property_count(self) -> int:
        """
        Counts desired properties.
        """

        return len(set(self.desired_properties))

    def conceptual_richness_score(self) -> float:
        """
        Computes a toy score for conceptual richness.

        Higher means the intuition contains more formalizable structure.
        """

        score = 0.0
        score += self.metaphor_count() * 0.8
        score += self.symbol_count() * 0.7
        score += self.structure_count() * 1.0
        score += self.property_count() * 0.9

        if self.kind in {
            IntuitionKind.CATEGORY_STRUCTURAL,
            IntuitionKind.LOGICAL_PRINCIPLE,
            IntuitionKind.CONSTRUCTIVE_EVIDENCE,
        }:
            score += 1.0

        return round(max(0.0, min(10.0, score)), 2)

    def clarity_score(self) -> float:
        """
        Converts clarity level into a score.
        """

        scores = {
            ClarityLevel.VAGUE: 2.0,
            ClarityLevel.PARTIAL: 4.0,
            ClarityLevel.STRUCTURED: 6.5,
            ClarityLevel.SYMBOL_READY: 8.0,
            ClarityLevel.FORMALIZATION_READY: 9.5,
        }

        return scores[self.clarity_level]

    def risk_score(self) -> float:
        """
        Converts formalization risk into a score.
        """

        scores = {
            FormalizationRisk.LOW: 2.0,
            FormalizationRisk.MEDIUM: 5.0,
            FormalizationRisk.HIGH: 7.5,
            FormalizationRisk.EXTREME: 9.5,
        }

        return scores[self.formalization_risk]

    def formalization_readiness_score(self) -> float:
        """
        Estimates how ready the intuition is to become a symbolic statement.
        """

        score = 0.0
        score += self.clarity_score() * 0.45
        score += self.conceptual_richness_score() * 0.35
        score += (10.0 - self.risk_score()) * 0.20

        return round(max(0.0, min(10.0, score)), 2)

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        return (
            f"IntuitionObject: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Raw intuition: {self.raw_intuition}\n"
            f"Guiding metaphors: {', '.join(self.guiding_metaphors) or 'none'}\n"
            f"Candidate symbols: {', '.join(self.candidate_symbols) or 'none'}\n"
            f"Implied structures: {', '.join(self.implied_structures) or 'none'}\n"
            f"Desired properties: {', '.join(self.desired_properties) or 'none'}\n"
            f"Clarity level: {self.clarity_level.value}\n"
            f"Formalization risk: {self.formalization_risk.value}\n"
            f"Conceptual richness score: {self.conceptual_richness_score()}\n"
            f"Formalization readiness score: {self.formalization_readiness_score()}\n"
            f"Notes: {self.notes or 'none'}"
        )


def starter_intuitions() -> List[IntuitionObject]:
    """
    Returns starter intuitions for Phase 6 experiments.
    """

    return [
        IntuitionObject(
            name="Contextual Identity Intuition",
            raw_intuition=(
                "Two mathematical objects may seem identical inside one context "
                "but become distinguishable when moved into another context."
            ),
            kind=IntuitionKind.CATEGORY_STRUCTURAL,
            guiding_metaphors=["identity depends on viewpoint", "objects under different lenses"],
            candidate_symbols=["identity", "context", "x", "y"],
            implied_structures=["contextual logic", "many-valued identity", "bridge translation"],
            desired_properties=["context_sensitivity", "truth_preservation"],
            clarity_level=ClarityLevel.STRUCTURED,
            formalization_risk=FormalizationRisk.MEDIUM,
            notes="Useful for testing context-sensitive identity across toy universes.",
        ),
        IntuitionObject(
            name="Contained Contradiction Intuition",
            raw_intuition=(
                "A contradiction can exist locally without destroying the entire "
                "logical universe."
            ),
            kind=IntuitionKind.CONTRADICTION_TOLERANCE,
            guiding_metaphors=["firewall for inconsistency", "local damage containment"],
            candidate_symbols=["both", "P", "Q", "not"],
            implied_structures=["paraconsistent logic", "local contradiction containment"],
            desired_properties=["contradiction_support", "non_explosion"],
            clarity_level=ClarityLevel.SYMBOL_READY,
            formalization_risk=FormalizationRisk.HIGH,
            notes="Important for paraconsistent-to-classical bridge experiments.",
        ),
        IntuitionObject(
            name="Constructive Witness Intuition",
            raw_intuition=(
                "To claim that something exists, the system should be able to "
                "construct or exhibit a witness."
            ),
            kind=IntuitionKind.CONSTRUCTIVE_EVIDENCE,
            guiding_metaphors=["existence as construction", "proof as object"],
            candidate_symbols=["exists", "witness", "x", "P"],
            implied_structures=["intuitionistic logic", "proof object", "constructive existence"],
            desired_properties=["constructive_evidence", "witness_preservation"],
            clarity_level=ClarityLevel.SYMBOL_READY,
            formalization_risk=FormalizationRisk.MEDIUM,
            notes="Useful for measuring constructive weakening under classical translation.",
        ),
        IntuitionObject(
            name="Modal Possibility Intuition",
            raw_intuition=(
                "A statement can be possible without being necessary, and this "
                "distinction should not be erased too early."
            ),
            kind=IntuitionKind.MODAL_POSSIBILITY,
            guiding_metaphors=["possible worlds", "logical horizon"],
            candidate_symbols=["possible", "necessary", "P"],
            implied_structures=["modal logic", "possible-world semantics"],
            desired_properties=["modal_support", "possibility_preservation"],
            clarity_level=ClarityLevel.STRUCTURED,
            formalization_risk=FormalizationRisk.HIGH,
            notes="Useful for modal-to-classical bridge distortion tests.",
        ),
    ]


if __name__ == "__main__":
    for intuition in starter_intuitions():
        print(intuition.describe())
        print("-" * 80)
