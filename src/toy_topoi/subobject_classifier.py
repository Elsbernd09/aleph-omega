"""
Toy subobject classifier for Project ℵω.

In full topos theory, a subobject classifier is a deep categorical structure.
This module does not implement the full mathematical theory.

Instead, it creates a simplified computational analogue:
a classifier that assigns toy truth/classification statuses to statements
inside formal universes.

The goal is to make internal truth classification visible and inspectable.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from .statements import ProofStatus, Statement
from .truth_values import TruthValue
from .universe import FormalUniverse


class ClassificationStatus(str, Enum):
    """
    High-level classification result for a statement inside a universe.
    """

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    UNKNOWN = "unknown"
    CONTRADICTORY = "contradictory"
    MODAL = "modal"
    REQUIRES_REVIEW = "requires_review"


@dataclass(frozen=True)
class SubobjectClassification:
    """
    Result of classifying a statement inside a universe.

    This is a toy analogue of asking how a statement/object is classified
    by the internal truth structure of a universe.
    """

    statement_name: str
    universe_name: str
    truth_value: TruthValue
    proof_status: ProofStatus
    classification_status: ClassificationStatus
    membership_score: float
    explanation: str
    metadata: Optional[Dict[str, str]] = None

    def as_dict(self) -> Dict[str, object]:
        """
        Converts the classification to a dictionary.
        """

        return {
            "statement_name": self.statement_name,
            "universe_name": self.universe_name,
            "truth_value": self.truth_value.value,
            "proof_status": self.proof_status.value,
            "classification_status": self.classification_status.value,
            "membership_score": self.membership_score,
            "explanation": self.explanation,
        }

    def describe(self) -> str:
        """
        Returns a readable classification report.
        """

        return (
            f"SubobjectClassification\n"
            f"Statement: {self.statement_name}\n"
            f"Universe: {self.universe_name}\n"
            f"Truth value: {self.truth_value.value}\n"
            f"Proof status: {self.proof_status.value}\n"
            f"Classification status: {self.classification_status.value}\n"
            f"Membership score: {self.membership_score}\n"
            f"Explanation: {self.explanation}"
        )


class ToySubobjectClassifier:
    """
    Classifies statement evaluations inside toy universes.

    The classifier is intentionally heuristic. It is not a full categorical
    subobject classifier. It is a computational instrument for experiments.
    """

    def classify(
        self,
        statement: Statement,
        universe: FormalUniverse,
        truth_value: TruthValue,
        proof_status: ProofStatus,
        universe_fit_score: float,
        ambiguity_score: float,
    ) -> SubobjectClassification:
        """
        Classifies a statement inside a universe using analysis scores.
        """

        classification_status = self._classification_status(
            universe=universe,
            truth_value=truth_value,
            proof_status=proof_status,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
        )

        membership_score = self._membership_score(
            truth_value=truth_value,
            proof_status=proof_status,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
            classification_status=classification_status,
        )

        explanation = self._explanation(
            statement=statement,
            universe=universe,
            truth_value=truth_value,
            proof_status=proof_status,
            classification_status=classification_status,
            membership_score=membership_score,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
        )

        return SubobjectClassification(
            statement_name=statement.name,
            universe_name=universe.name,
            truth_value=truth_value,
            proof_status=proof_status,
            classification_status=classification_status,
            membership_score=membership_score,
            explanation=explanation,
            metadata={
                "universe_fit_score": str(universe_fit_score),
                "ambiguity_score": str(ambiguity_score),
            },
        )

    @staticmethod
    def _classification_status(
        universe: FormalUniverse,
        truth_value: TruthValue,
        proof_status: ProofStatus,
        universe_fit_score: float,
        ambiguity_score: float,
    ) -> ClassificationStatus:
        """
        Determines a high-level classification status.
        """

        if ambiguity_score >= 6.5 or universe_fit_score <= 3.0:
            return ClassificationStatus.REQUIRES_REVIEW

        if truth_value == TruthValue.TRUE:
            if proof_status in {
                ProofStatus.ASSUMED,
                ProofStatus.DERIVED,
                ProofStatus.MACHINE_CHECKED,
                ProofStatus.UNTESTED,
                ProofStatus.UNKNOWN,
            }:
                return ClassificationStatus.ACCEPTED

        if truth_value == TruthValue.FALSE:
            return ClassificationStatus.REJECTED

        if truth_value == TruthValue.UNKNOWN:
            return ClassificationStatus.UNKNOWN

        if truth_value in {TruthValue.BOTH, TruthValue.NEITHER}:
            if universe.supports_contradiction():
                return ClassificationStatus.CONTRADICTORY
            return ClassificationStatus.REQUIRES_REVIEW

        if truth_value in {
            TruthValue.NECESSARY,
            TruthValue.POSSIBLE,
            TruthValue.IMPOSSIBLE,
            TruthValue.CONTINGENT,
        }:
            if universe.supports_modal_status():
                return ClassificationStatus.MODAL
            return ClassificationStatus.REQUIRES_REVIEW

        if proof_status == ProofStatus.HUMAN_REVIEW_REQUIRED:
            return ClassificationStatus.REQUIRES_REVIEW

        return ClassificationStatus.REQUIRES_REVIEW

    @staticmethod
    def _membership_score(
        truth_value: TruthValue,
        proof_status: ProofStatus,
        universe_fit_score: float,
        ambiguity_score: float,
        classification_status: ClassificationStatus,
    ) -> float:
        """
        Computes a toy membership score from 0 to 10.

        Higher means the statement fits more cleanly as an internally accepted
        object/subobject of the universe.
        """

        score = universe_fit_score
        score -= ambiguity_score * 0.35

        if truth_value == TruthValue.TRUE:
            score += 1.0

        if truth_value == TruthValue.FALSE:
            score -= 2.0

        if truth_value == TruthValue.UNKNOWN:
            score -= 0.75

        if truth_value == TruthValue.BOTH:
            score -= 0.25

        if proof_status == ProofStatus.MACHINE_CHECKED:
            score += 2.0

        if proof_status == ProofStatus.DERIVED:
            score += 1.25

        if proof_status == ProofStatus.ASSUMED:
            score += 0.5

        if proof_status == ProofStatus.HUMAN_REVIEW_REQUIRED:
            score -= 1.5

        if classification_status == ClassificationStatus.REQUIRES_REVIEW:
            score -= 1.0

        if classification_status == ClassificationStatus.ACCEPTED:
            score += 0.5

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _explanation(
        statement: Statement,
        universe: FormalUniverse,
        truth_value: TruthValue,
        proof_status: ProofStatus,
        classification_status: ClassificationStatus,
        membership_score: float,
        universe_fit_score: float,
        ambiguity_score: float,
    ) -> str:
        """
        Builds a human-readable explanation.
        """

        return (
            f"The statement '{statement.name}' was classified inside "
            f"'{universe.name}'. Its toy truth value is '{truth_value.value}' "
            f"and its proof status is '{proof_status.value}'. The classifier "
            f"assigned status '{classification_status.value}' with membership "
            f"score {membership_score}. Universe fit score was {universe_fit_score}; "
            f"ambiguity score was {ambiguity_score}. This is a simplified "
            f"subobject-classifier analogue, not a categorical proof."
        )


def classify_simulation_results(results) -> List[SubobjectClassification]:
    """
    Classifies a list of SimulationResult objects.

    The function is kept untyped on purpose to avoid circular imports with
    simulator.py.
    """

    classifier = ToySubobjectClassifier()
    classifications: List[SubobjectClassification] = []

    for result in results:
        classifications.append(
            classifier.classify(
                statement=result.statement,
                universe=result.universe,
                truth_value=result.evaluation.truth_value,
                proof_status=result.evaluation.proof_status,
                universe_fit_score=result.analysis.universe_fit_score,
                ambiguity_score=result.analysis.ambiguity_score,
            )
        )

    return classifications


if __name__ == "__main__":
    from .library import standard_universes
    from .simulator import ToyToposSimulator
    from .statements import starter_statements

    simulator = ToyToposSimulator(
        universes=standard_universes(),
        statements=starter_statements(),
    )

    results = simulator.evaluate_all()
    classifications = classify_simulation_results(results)

    for classification in classifications[:10]:
        print(classification.describe())
        print("-" * 80)
