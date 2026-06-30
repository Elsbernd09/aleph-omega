"""
Internal statement model for Project ℵω toy topoi.

This module defines statements that can live inside toy formal universes.

A statement is not treated as true or false in isolation. It is interpreted
inside a universe with a particular truth-value space, logic family,
consistency policy, and inference behavior.

These models are simplified and educational. They are not full formal logic,
not full type theory, and not complete topos-theoretic internal languages.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from .truth_values import TruthValue


class StatementKind(str, Enum):
    """
    Broad kind of mathematical statement.
    """

    PROPOSITION = "proposition"
    DEFINITION = "definition"
    AXIOMATIC_ASSUMPTION = "axiomatic_assumption"
    THEOREM_CANDIDATE = "theorem_candidate"
    LEMMA_CANDIDATE = "lemma_candidate"
    CONTRADICTION = "contradiction"
    MODAL_CLAIM = "modal_claim"
    FUZZY_CLAIM = "fuzzy_claim"
    TRANSPORTED_STATEMENT = "transported_statement"
    PRIME_GEOMETRY_CLAIM = "prime_geometry_claim"
    COGNITIVE_SKETCH = "cognitive_sketch"


class ProofStatus(str, Enum):
    """
    Proof or formalization status of a statement.
    """

    UNTESTED = "untested"
    ASSUMED = "assumed"
    DERIVED = "derived"
    REFUTED = "refuted"
    CONTRADICTORY = "contradictory"
    UNKNOWN = "unknown"
    PARTIALLY_FORMALIZED = "partially_formalized"
    FORMALIZED_WITH_SORRY = "formalized_with_sorry"
    MACHINE_CHECKED = "machine_checked"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


@dataclass(frozen=True)
class Statement:
    """
    A mathematical statement inside a toy formal universe.

    Fields:
        name:
            Human-readable name.

        raw_text:
            Informal or semi-formal natural-language statement.

        symbolic_form:
            Structured symbolic sketch.

        kind:
            Broad statement type.

        free_variables:
            Variables not bound by quantifiers.

        required_symbols:
            Logical or mathematical symbols needed to interpret the statement.

        origin_universe:
            Name of the universe where the statement was created.

        dependencies:
            Other statements, axioms, definitions, or rules required.

        notes:
            Human-readable explanation.

        metadata:
            Optional extra data.
    """

    name: str
    raw_text: str
    symbolic_form: str
    kind: StatementKind = StatementKind.PROPOSITION
    free_variables: List[str] = field(default_factory=list)
    required_symbols: List[str] = field(default_factory=list)
    origin_universe: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def variable_count(self) -> int:
        """
        Counts unique free variables.
        """

        return len(set(self.free_variables))

    def symbol_count(self) -> int:
        """
        Counts unique required symbols.
        """

        return len(set(self.required_symbols))

    def dependency_count(self) -> int:
        """
        Counts unique dependencies.
        """

        return len(set(self.dependencies))

    def structural_complexity(self) -> float:
        """
        Computes a simple heuristic structural complexity score.

        This is not a theorem-proving metric. It is a lightweight way to
        estimate how much structure a statement carries.
        """

        score = 0.0
        score += self.variable_count() * 0.8
        score += self.symbol_count() * 0.7
        score += self.dependency_count() * 0.6
        score += min(len(self.symbolic_form.split()) * 0.15, 2.0)

        return round(min(score, 10.0), 2)

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        return (
            f"Statement: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Raw text: {self.raw_text}\n"
            f"Symbolic form: {self.symbolic_form}\n"
            f"Free variables: {', '.join(self.free_variables) or 'none'}\n"
            f"Required symbols: {', '.join(self.required_symbols) or 'none'}\n"
            f"Origin universe: {self.origin_universe or 'not specified'}\n"
            f"Dependencies: {', '.join(self.dependencies) or 'none'}\n"
            f"Structural complexity: {self.structural_complexity()}\n"
            f"Notes: {self.notes or 'none'}"
        )


@dataclass(frozen=True)
class StatementEvaluation:
    """
    Evaluation result for a statement inside a universe.

    Fields:
        statement_name:
            Name of the evaluated statement.

        universe_name:
            Universe where evaluation happened.

        truth_value:
            Toy truth value assigned by the universe.

        proof_status:
            Proof or formalization status.

        explanation:
            Human-readable explanation of the evaluation.

        required_human_review:
            Whether the result should be manually reviewed.

        metadata:
            Optional additional notes.
    """

    statement_name: str
    universe_name: str
    truth_value: TruthValue
    proof_status: ProofStatus
    explanation: str
    required_human_review: bool = True
    metadata: Optional[Dict[str, str]] = None

    def describe(self) -> str:
        """
        Returns a readable evaluation report.
        """

        return (
            f"Statement evaluation\n"
            f"Statement: {self.statement_name}\n"
            f"Universe: {self.universe_name}\n"
            f"Truth value: {self.truth_value.value}\n"
            f"Proof status: {self.proof_status.value}\n"
            f"Human review required: {self.required_human_review}\n"
            f"Explanation: {self.explanation}"
        )


def starter_statements() -> List[Statement]:
    """
    Returns starter internal statements for Phase 4 experiments.
    """

    return [
        Statement(
            name="Excluded Middle Statement",
            raw_text="For every proposition P, either P is true or not P is true.",
            symbolic_form="forall P, P or not(P)",
            kind=StatementKind.PROPOSITION,
            free_variables=["P"],
            required_symbols=["forall", "or", "not", "truth"],
            origin_universe="Classical Set-Theoretic Neighborhood",
            dependencies=["law_of_excluded_middle"],
            notes=(
                "This statement is classically natural but becomes proof-sensitive "
                "in intuitionistic settings."
            ),
        ),
        Statement(
            name="Local Contradiction Statement",
            raw_text="A statement P may be both true and false without making every statement derivable.",
            symbolic_form="both(P) does_not_imply arbitrary(Q)",
            kind=StatementKind.CONTRADICTION,
            free_variables=["P", "Q"],
            required_symbols=["both", "not", "implies", "arbitrary"],
            origin_universe="Paraconsistent Contradiction-Tolerant Universe",
            dependencies=["local_contradiction_containment"],
            notes=(
                "This statement is designed for paraconsistent experiments and "
                "should be unstable in strict classical transport."
            ),
        ),
        Statement(
            name="Constructive Existence Statement",
            raw_text="An object satisfying property P exists only when a witness can be constructed.",
            symbolic_form="exists x, P(x) requires witness(x)",
            kind=StatementKind.THEOREM_CANDIDATE,
            free_variables=["P"],
            required_symbols=["exists", "property", "requires", "witness"],
            origin_universe="Intuitionistic Constructive Universe",
            dependencies=["witness_requirement"],
            notes=(
                "This statement models constructive existence and proof evidence."
            ),
        ),
        Statement(
            name="Modal Possibility Statement",
            raw_text="A statement may be possible without being necessary.",
            symbolic_form="possible(P) and not(necessary(P))",
            kind=StatementKind.MODAL_CLAIM,
            free_variables=["P"],
            required_symbols=["possible", "necessary", "not", "and"],
            origin_universe="Modal Possibility Universe",
            dependencies=["modal_status"],
            notes=(
                "This statement tests whether a universe can preserve modal information."
            ),
        ),
        Statement(
            name="Contextual Identity Statement",
            raw_text="Two objects may be identical inside one interpretation context but not inside another.",
            symbolic_form="identity(x, y, C1) and not identity(x, y, C2)",
            kind=StatementKind.PROPOSITION,
            free_variables=["x", "y", "C1", "C2"],
            required_symbols=["identity", "context", "and", "not"],
            origin_universe="Many-Valued Indeterminate Universe",
            dependencies=["contextual_identity"],
            notes=(
                "This statement supports experiments on context-sensitive identity."
            ),
        ),
    ]


if __name__ == "__main__":
    for statement in starter_statements():
        print(statement.describe())
        print("-" * 80)
