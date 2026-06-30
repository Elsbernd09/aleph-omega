"""
Formalization target model for Project ℵω.

This module represents the next step after an informal statement has been
created: deciding what kind of formal object it should become.

The goal is not to automatically prove theorems. The goal is to create a
clear, inspectable target for Lean-style or theorem-prover-style work.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.toy_topoi.statements import ProofStatus, Statement, StatementKind


class FormalTargetKind(str, Enum):
    """
    Type of formal object we want to produce.
    """

    DEFINITION = "definition"
    AXIOM = "axiom"
    THEOREM = "theorem"
    LEMMA = "lemma"
    STRUCTURE = "structure"
    INDUCTIVE_TYPE = "inductive_type"
    CLASS = "class"
    EXAMPLE = "example"
    COMMENTARY_SKETCH = "commentary_sketch"


class FormalizationDifficulty(str, Enum):
    """
    Estimated difficulty of formalizing a statement.
    """

    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"
    RESEARCH_LEVEL = "research_level"
    CURRENTLY_UNREALISTIC = "currently_unrealistic"


class FormalizationReadiness(str, Enum):
    """
    Whether the statement is ready for formalization.
    """

    READY = "ready"
    NEEDS_DEFINITIONS = "needs_definitions"
    NEEDS_ASSUMPTIONS = "needs_assumptions"
    NEEDS_SIMPLIFICATION = "needs_simplification"
    NEEDS_HUMAN_REVIEW = "needs_human_review"


@dataclass(frozen=True)
class FormalizationTarget:
    """
    A target formal object generated from a statement.

    This tells the system whether a statement should become a definition,
    theorem, axiom, lemma, structure, or proof sketch.
    """

    statement: Statement
    target_kind: FormalTargetKind
    difficulty: FormalizationDifficulty
    readiness: FormalizationReadiness
    required_definitions: List[str] = field(default_factory=list)
    required_assumptions: List[str] = field(default_factory=list)
    required_imports: List[str] = field(default_factory=list)
    theorem_name: Optional[str] = None
    informal_goal: str = ""
    formal_goal_sketch: str = ""
    proof_strategy_notes: str = ""
    risk_notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def required_definition_count(self) -> int:
        """
        Counts required definitions.
        """

        return len(set(self.required_definitions))

    def required_assumption_count(self) -> int:
        """
        Counts required assumptions.
        """

        return len(set(self.required_assumptions))

    def estimated_work_score(self) -> float:
        """
        Estimates formalization work required from 0 to 10.

        Higher means more work.
        """

        score = 0.0
        score += self.required_definition_count() * 0.9
        score += self.required_assumption_count() * 0.8

        difficulty_scores = {
            FormalizationDifficulty.EASY: 1.5,
            FormalizationDifficulty.MODERATE: 3.5,
            FormalizationDifficulty.HARD: 6.0,
            FormalizationDifficulty.RESEARCH_LEVEL: 8.0,
            FormalizationDifficulty.CURRENTLY_UNREALISTIC: 9.5,
        }

        readiness_penalties = {
            FormalizationReadiness.READY: 0.0,
            FormalizationReadiness.NEEDS_DEFINITIONS: 1.0,
            FormalizationReadiness.NEEDS_ASSUMPTIONS: 1.0,
            FormalizationReadiness.NEEDS_SIMPLIFICATION: 1.5,
            FormalizationReadiness.NEEDS_HUMAN_REVIEW: 2.0,
        }

        score += difficulty_scores[self.difficulty]
        score += readiness_penalties[self.readiness]

        return round(max(0.0, min(10.0, score)), 2)

    def is_ready_for_lean_sketch(self) -> bool:
        """
        Returns whether we can generate a Lean-style sketch.
        """

        return self.readiness in {
            FormalizationReadiness.READY,
            FormalizationReadiness.NEEDS_DEFINITIONS,
            FormalizationReadiness.NEEDS_ASSUMPTIONS,
        }

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"FormalizationTarget\n"
            f"Statement: {self.statement.name}\n"
            f"Target kind: {self.target_kind.value}\n"
            f"Difficulty: {self.difficulty.value}\n"
            f"Readiness: {self.readiness.value}\n"
            f"Theorem name: {self.theorem_name or 'not assigned'}\n"
            f"Required definitions: {', '.join(self.required_definitions) or 'none'}\n"
            f"Required assumptions: {', '.join(self.required_assumptions) or 'none'}\n"
            f"Required imports: {', '.join(self.required_imports) or 'none'}\n"
            f"Estimated work score: {self.estimated_work_score()}\n"
            f"Ready for Lean sketch: {self.is_ready_for_lean_sketch()}\n"
            f"Informal goal: {self.informal_goal or 'none'}\n"
            f"Formal goal sketch: {self.formal_goal_sketch or 'none'}\n"
            f"Proof strategy notes: {self.proof_strategy_notes or 'none'}\n"
            f"Risk notes: {self.risk_notes or 'none'}"
        )


class FormalizationTargetBuilder:
    """
    Builds FormalizationTarget objects from statements.
    """

    def build(self, statement: Statement) -> FormalizationTarget:
        """
        Builds a formalization target from one statement.
        """

        target_kind = self._target_kind(statement)
        difficulty = self._difficulty(statement)
        readiness = self._readiness(statement)
        required_definitions = self._required_definitions(statement)
        required_assumptions = self._required_assumptions(statement)
        required_imports = self._required_imports(statement)
        theorem_name = self._theorem_name(statement)

        return FormalizationTarget(
            statement=statement,
            target_kind=target_kind,
            difficulty=difficulty,
            readiness=readiness,
            required_definitions=required_definitions,
            required_assumptions=required_assumptions,
            required_imports=required_imports,
            theorem_name=theorem_name,
            informal_goal=statement.raw_text,
            formal_goal_sketch=statement.symbolic_form,
            proof_strategy_notes=self._proof_strategy_notes(statement),
            risk_notes=self._risk_notes(statement),
            metadata={
                "statement_kind": statement.kind.value,
                "proof_status": statement.metadata.get("proof_status", "unknown") if statement.metadata else "unknown",
            },
        )

    def build_many(self, statements: List[Statement]) -> List[FormalizationTarget]:
        """
        Builds targets for many statements.
        """

        return [self.build(statement) for statement in statements]

    @staticmethod
    def _target_kind(statement: Statement) -> FormalTargetKind:
        """
        Chooses formal target kind from statement kind.
        """

        if statement.kind == StatementKind.DEFINITION:
            return FormalTargetKind.DEFINITION

        if statement.kind == StatementKind.AXIOMATIC_ASSUMPTION:
            return FormalTargetKind.AXIOM

        if statement.kind == StatementKind.THEOREM_CANDIDATE:
            return FormalTargetKind.THEOREM

        if statement.kind == StatementKind.LEMMA_CANDIDATE:
            return FormalTargetKind.LEMMA

        if statement.kind in {
            StatementKind.CONTRADICTION,
            StatementKind.MODAL_CLAIM,
            StatementKind.FUZZY_CLAIM,
            StatementKind.COGNITIVE_SKETCH,
        }:
            return FormalTargetKind.COMMENTARY_SKETCH

        return FormalTargetKind.THEOREM

    @staticmethod
    def _difficulty(statement: Statement) -> FormalizationDifficulty:
        """
        Estimates formalization difficulty.
        """

        complexity = statement.structural_complexity()
        symbols = {symbol.lower() for symbol in statement.required_symbols}

        if "both" in symbols or "possible" in symbols or "necessary" in symbols:
            return FormalizationDifficulty.RESEARCH_LEVEL

        if "context" in symbols or "identity" in symbols:
            return FormalizationDifficulty.HARD

        if complexity <= 3.0:
            return FormalizationDifficulty.EASY

        if complexity <= 5.5:
            return FormalizationDifficulty.MODERATE

        if complexity <= 7.5:
            return FormalizationDifficulty.HARD

        return FormalizationDifficulty.RESEARCH_LEVEL

    @staticmethod
    def _readiness(statement: Statement) -> FormalizationReadiness:
        """
        Estimates readiness for formalization.
        """

        symbols = {symbol.lower() for symbol in statement.required_symbols}

        if not statement.symbolic_form:
            return FormalizationReadiness.NEEDS_SIMPLIFICATION

        if "both" in symbols or "possible" in symbols or "necessary" in symbols:
            return FormalizationReadiness.NEEDS_HUMAN_REVIEW

        if "witness" in symbols or "context" in symbols or "identity" in symbols:
            return FormalizationReadiness.NEEDS_DEFINITIONS

        if statement.dependencies:
            return FormalizationReadiness.NEEDS_ASSUMPTIONS

        return FormalizationReadiness.READY

    @staticmethod
    def _required_definitions(statement: Statement) -> List[str]:
        """
        Infers required definitions.
        """

        definitions = set()
        symbols = {symbol.lower() for symbol in statement.required_symbols}

        if "identity" in symbols:
            definitions.add("ContextualIdentity")

        if "context" in symbols:
            definitions.add("InterpretationContext")

        if "witness" in symbols:
            definitions.add("Witness")

        if "possible" in symbols or "necessary" in symbols:
            definitions.add("ModalStatus")

        if "both" in symbols:
            definitions.add("ParaconsistentTruth")

        return sorted(definitions)

    @staticmethod
    def _required_assumptions(statement: Statement) -> List[str]:
        """
        Infers assumptions needed for a target.
        """

        assumptions = set(statement.dependencies)

        if statement.origin_universe:
            assumptions.add(f"Working inside {statement.origin_universe}")

        return sorted(assumptions)

    @staticmethod
    def _required_imports(statement: Statement) -> List[str]:
        """
        Infers Lean-style imports.
        """

        imports = {"Mathlib"}

        symbols = {symbol.lower() for symbol in statement.required_symbols}

        if "exists" in symbols or "forall" in symbols:
            imports.add("Mathlib.Logic.Basic")

        if "identity" in symbols or "context" in symbols:
            imports.add("Mathlib.CategoryTheory.Category.Basic")

        return sorted(imports)

    @staticmethod
    def _theorem_name(statement: Statement) -> str:
        """
        Creates a Lean-safe theorem-style name.
        """

        cleaned = statement.name.lower()
        cleaned = cleaned.replace("formalized ", "")
        cleaned = cleaned.replace("translated ", "")
        cleaned = "".join(char if char.isalnum() else "_" for char in cleaned)
        cleaned = "_".join(part for part in cleaned.split("_") if part)

        if not cleaned:
            cleaned = "generated_statement"

        return cleaned

    @staticmethod
    def _proof_strategy_notes(statement: Statement) -> str:
        """
        Adds strategy notes.
        """

        if statement.kind == StatementKind.CONTRADICTION:
            return (
                "This statement should not be treated as a classical theorem. "
                "It needs a custom paraconsistent semantics or should remain a sketch."
            )

        if statement.kind == StatementKind.MODAL_CLAIM:
            return (
                "This statement needs modal semantics before a serious proof can be attempted."
            )

        if statement.kind == StatementKind.THEOREM_CANDIDATE:
            return (
                "Define the involved objects first, state assumptions explicitly, "
                "then attempt a proof or leave a sorry placeholder."
            )

        return (
            "Start by defining all nonstandard terms, then state the goal with "
            "explicit assumptions."
        )

    @staticmethod
    def _risk_notes(statement: Statement) -> str:
        """
        Adds risk notes.
        """

        symbols = {symbol.lower() for symbol in statement.required_symbols}

        risky = []

        if "both" in symbols:
            risky.append("paraconsistent truth is not native to ordinary classical Lean statements")

        if "possible" in symbols or "necessary" in symbols:
            risky.append("modal semantics need explicit encoding")

        if "context" in symbols:
            risky.append("context-dependence must be defined before use")

        if not risky:
            return "No major formalization risk detected beyond ordinary missing definitions."

        return "; ".join(risky) + "."


if __name__ == "__main__":
    from src.cognitive_morphism.formalizer import InformalFormalizer
    from src.cognitive_morphism.intuition import starter_intuitions

    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()

    drafts = formalizer.formalize_many(starter_intuitions())
    targets = builder.build_many([draft.statement for draft in drafts])

    for target in targets:
        print(target.describe())
        print("-" * 100)
