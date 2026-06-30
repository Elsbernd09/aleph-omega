"""
Cognitive morphism model for Project ℵω.

A cognitive morphism represents the transformation from an informal human
mathematical intuition into a symbolic statement.

This is not a claim about neuroscience or cognitive science. It is a structured
model for tracking what is preserved, lost, or distorted when informal math
becomes formal symbolic math.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.cognitive_morphism.intuition import IntuitionObject
from src.toy_topoi.statements import Statement


class CognitiveMorphismKind(str, Enum):
    """
    Type of transformation from intuition to symbolic statement.
    """

    DIRECT_SYMBOLIZATION = "direct_symbolization"
    ANALOGICAL_FORMALIZATION = "analogical_formalization"
    STRUCTURAL_EXTRACTION = "structural_extraction"
    LOGICAL_COMPRESSION = "logical_compression"
    CONTEXTUAL_ENCODING = "contextual_encoding"
    MODAL_ENCODING = "modal_encoding"
    CONTRADICTION_ENCODING = "contradiction_encoding"
    CONSTRUCTIVE_ENCODING = "constructive_encoding"
    GENERATED_TRANSLATION = "generated_translation"


class CognitiveMorphismStatus(str, Enum):
    """
    Status of the intuition-to-statement transformation.
    """

    CLEAN = "clean"
    PARTIAL = "partial"
    DRIFTED = "drifted"
    OVERFORMALIZED = "overformalized"
    UNDERFORMALIZED = "underformalized"
    AMBIGUOUS = "ambiguous"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"


@dataclass(frozen=True)
class CognitivePreservation:
    """
    Records preservation and loss during cognitive formalization.
    """

    preserved_properties: List[str] = field(default_factory=list)
    lost_properties: List[str] = field(default_factory=list)
    added_formal_properties: List[str] = field(default_factory=list)
    preserved_metaphors: List[str] = field(default_factory=list)
    lost_metaphors: List[str] = field(default_factory=list)

    def property_preservation_score(self) -> float:
        """
        Scores preservation of desired intuition properties.
        """

        total = len(set(self.preserved_properties + self.lost_properties))

        if total == 0:
            return 10.0

        score = 10.0 * len(set(self.preserved_properties)) / total
        return round(max(0.0, min(10.0, score)), 2)

    def metaphor_preservation_score(self) -> float:
        """
        Scores preservation of guiding metaphors.
        """

        total = len(set(self.preserved_metaphors + self.lost_metaphors))

        if total == 0:
            return 10.0

        score = 10.0 * len(set(self.preserved_metaphors)) / total
        return round(max(0.0, min(10.0, score)), 2)

    def added_structure_count(self) -> int:
        """
        Counts added formal properties.
        """

        return len(set(self.added_formal_properties))

    def describe(self) -> str:
        """
        Returns a readable preservation report.
        """

        return (
            f"CognitivePreservation\n"
            f"Preserved properties: {', '.join(self.preserved_properties) or 'none'}\n"
            f"Lost properties: {', '.join(self.lost_properties) or 'none'}\n"
            f"Added formal properties: {', '.join(self.added_formal_properties) or 'none'}\n"
            f"Preserved metaphors: {', '.join(self.preserved_metaphors) or 'none'}\n"
            f"Lost metaphors: {', '.join(self.lost_metaphors) or 'none'}\n"
            f"Property preservation score: {self.property_preservation_score()}\n"
            f"Metaphor preservation score: {self.metaphor_preservation_score()}"
        )


@dataclass(frozen=True)
class CognitiveMorphism:
    """
    Transformation from an intuition object to a symbolic statement.
    """

    name: str
    source_intuition: IntuitionObject
    target_statement: Statement
    kind: CognitiveMorphismKind
    preservation: CognitivePreservation
    status: CognitiveMorphismStatus
    confidence: float
    meaning_drift_score: float
    notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def normalized_confidence(self) -> float:
        """
        Returns confidence clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.confidence)), 2)

    def normalized_meaning_drift(self) -> float:
        """
        Returns meaning drift clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.meaning_drift_score)), 2)

    def formalization_quality_score(self) -> float:
        """
        Scores the quality of the intuition-to-statement formalization.
        """

        score = 0.0
        score += self.normalized_confidence() * 0.35
        score += self.preservation.property_preservation_score() * 0.30
        score += self.preservation.metaphor_preservation_score() * 0.15
        score += (10.0 - self.normalized_meaning_drift()) * 0.20

        if self.status == CognitiveMorphismStatus.CLEAN:
            score += 0.5

        if self.status in {
            CognitiveMorphismStatus.DRIFTED,
            CognitiveMorphismStatus.OVERFORMALIZED,
            CognitiveMorphismStatus.UNDERFORMALIZED,
            CognitiveMorphismStatus.REQUIRES_HUMAN_REVIEW,
        }:
            score -= 1.0

        return round(max(0.0, min(10.0, score)), 2)

    def requires_review(self) -> bool:
        """
        Returns whether a human should review the formalization.
        """

        return (
            self.status == CognitiveMorphismStatus.REQUIRES_HUMAN_REVIEW
            or self.normalized_confidence() < 6.0
            or self.normalized_meaning_drift() > 5.5
            or self.formalization_quality_score() < 5.5
        )

    def summary_row(self) -> Dict[str, object]:
        """
        Returns compact table data.
        """

        return {
            "morphism": self.name,
            "intuition": self.source_intuition.name,
            "statement": self.target_statement.name,
            "kind": self.kind.value,
            "status": self.status.value,
            "confidence": self.normalized_confidence(),
            "meaning_drift": self.normalized_meaning_drift(),
            "quality": self.formalization_quality_score(),
            "requires_review": self.requires_review(),
        }

    def describe(self) -> str:
        """
        Returns a readable cognitive morphism report.
        """

        return (
            f"CognitiveMorphism: {self.name}\n"
            f"Source intuition: {self.source_intuition.name}\n"
            f"Target statement: {self.target_statement.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Status: {self.status.value}\n"
            f"Confidence: {self.normalized_confidence()}\n"
            f"Meaning drift score: {self.normalized_meaning_drift()}\n"
            f"Formalization quality score: {self.formalization_quality_score()}\n"
            f"Requires review: {self.requires_review()}\n"
            f"{self.preservation.describe()}\n"
            f"Notes: {self.notes or 'none'}"
        )


def example_cognitive_morphism(
    intuition: IntuitionObject,
    statement: Statement,
) -> CognitiveMorphism:
    """
    Builds a starter cognitive morphism between one intuition and one statement.
    """

    desired = set(intuition.desired_properties)
    statement_symbols = {symbol.lower() for symbol in statement.required_symbols}
    statement_text = statement.raw_text.lower() + " " + statement.symbolic_form.lower()

    preserved_properties = []
    lost_properties = []

    for prop in desired:
        prop_words = prop.replace("_", " ").split()
        if any(word in statement_text or word in statement_symbols for word in prop_words):
            preserved_properties.append(prop)
        else:
            lost_properties.append(prop)

    preserved_metaphors = []
    lost_metaphors = []

    for metaphor in intuition.guiding_metaphors:
        metaphor_words = metaphor.lower().split()
        if any(word in statement_text for word in metaphor_words):
            preserved_metaphors.append(metaphor)
        else:
            lost_metaphors.append(metaphor)

    preservation = CognitivePreservation(
        preserved_properties=sorted(preserved_properties),
        lost_properties=sorted(lost_properties),
        added_formal_properties=sorted(set(statement.required_symbols).difference(intuition.candidate_symbols)),
        preserved_metaphors=sorted(preserved_metaphors),
        lost_metaphors=sorted(lost_metaphors),
    )

    drift = 10.0 - (
        preservation.property_preservation_score() * 0.65
        + preservation.metaphor_preservation_score() * 0.35
    )

    confidence = (
        intuition.formalization_readiness_score() * 0.45
        + preservation.property_preservation_score() * 0.35
        + statement.structural_complexity() * 0.20
    )

    if preservation.property_preservation_score() >= 7.0 and drift <= 4.0:
        status = CognitiveMorphismStatus.CLEAN
    elif preservation.property_preservation_score() >= 5.0:
        status = CognitiveMorphismStatus.PARTIAL
    else:
        status = CognitiveMorphismStatus.REQUIRES_HUMAN_REVIEW

    return CognitiveMorphism(
        name=f"{intuition.name} → {statement.name}",
        source_intuition=intuition,
        target_statement=statement,
        kind=CognitiveMorphismKind.STRUCTURAL_EXTRACTION,
        preservation=preservation,
        status=status,
        confidence=confidence,
        meaning_drift_score=drift,
        notes=(
            "Automatically generated starter morphism. "
            "This is a heuristic comparison between intuition content and statement structure."
        ),
    )


if __name__ == "__main__":
    from src.cognitive_morphism.intuition import starter_intuitions
    from src.toy_topoi.statements import starter_statements

    intuitions = starter_intuitions()
    statements = starter_statements()

    for intuition in intuitions:
        for statement in statements:
            if intuition.name.split()[0].lower() in statement.name.lower():
                morphism = example_cognitive_morphism(intuition, statement)
                print(morphism.describe())
                print("-" * 80)
