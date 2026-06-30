"""
Lean sketch generator for Project ℵω.

This module converts FormalizationTarget objects into Lean-style proof
skeletons.

The generated text is intentionally conservative. It uses comments and sorry
placeholders for nontrivial proof obligations. The goal is to create an
inspectable formalization plan, not to falsely claim completed proofs.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from src.cognitive_morphism.formalization_target import (
    FormalTargetKind,
    FormalizationTarget,
)


class LeanSketchStatus(str, Enum):
    """
    Status of a generated Lean sketch.
    """

    GENERATED = "generated"
    NEEDS_DEFINITIONS = "needs_definitions"
    NEEDS_ASSUMPTIONS = "needs_assumptions"
    NEEDS_HUMAN_REVIEW = "needs_human_review"
    NOT_RECOMMENDED = "not_recommended"


@dataclass(frozen=True)
class LeanSketch:
    """
    Lean-style formalization sketch.
    """

    target: FormalizationTarget
    code: str
    status: LeanSketchStatus
    imports: List[str]
    definitions_needed: List[str]
    assumptions_needed: List[str]
    sorry_count: int
    explanation: str
    metadata: Optional[Dict[str, str]] = None

    def line_count(self) -> int:
        """
        Counts lines in the generated sketch.
        """

        return len(self.code.splitlines())

    def is_machine_checked_claim(self) -> bool:
        """
        Returns False because these sketches are not completed proofs.
        """

        return False

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"LeanSketch\n"
            f"Statement: {self.target.statement.name}\n"
            f"Status: {self.status.value}\n"
            f"Imports: {', '.join(self.imports) or 'none'}\n"
            f"Definitions needed: {', '.join(self.definitions_needed) or 'none'}\n"
            f"Assumptions needed: {', '.join(self.assumptions_needed) or 'none'}\n"
            f"Sorry count: {self.sorry_count}\n"
            f"Line count: {self.line_count()}\n"
            f"Machine-checked claim: {self.is_machine_checked_claim()}\n"
            f"Explanation: {self.explanation}\n"
            f"\nGenerated Lean-style sketch:\n{self.code}"
        )


class LeanSketchGenerator:
    """
    Generates Lean-style sketches from formalization targets.
    """

    def generate(self, target: FormalizationTarget) -> LeanSketch:
        """
        Generates one Lean-style sketch.
        """

        imports = target.required_imports
        definitions_needed = target.required_definitions
        assumptions_needed = target.required_assumptions

        code_lines: List[str] = []
        code_lines.extend(self._import_lines(imports))
        code_lines.append("")
        code_lines.extend(self._header_comment(target))
        code_lines.append("")
        code_lines.extend(self._definition_placeholders(definitions_needed))
        code_lines.append("")
        code_lines.extend(self._assumption_placeholders(assumptions_needed))
        code_lines.append("")
        code_lines.extend(self._target_code(target))

        code = "\n".join(code_lines).rstrip() + "\n"
        sorry_count = code.count("sorry")

        status = self._status(target)
        explanation = self._explanation(target, status, sorry_count)

        return LeanSketch(
            target=target,
            code=code,
            status=status,
            imports=imports,
            definitions_needed=definitions_needed,
            assumptions_needed=assumptions_needed,
            sorry_count=sorry_count,
            explanation=explanation,
            metadata={
                "target_kind": target.target_kind.value,
                "difficulty": target.difficulty.value,
                "readiness": target.readiness.value,
            },
        )

    def generate_many(self, targets: List[FormalizationTarget]) -> List[LeanSketch]:
        """
        Generates sketches for many targets.
        """

        return [self.generate(target) for target in targets]

    @staticmethod
    def _import_lines(imports: List[str]) -> List[str]:
        """
        Builds import lines.
        """

        if not imports:
            return ["import Mathlib"]

        return [f"import {item}" for item in imports]

    @staticmethod
    def _header_comment(target: FormalizationTarget) -> List[str]:
        """
        Builds explanatory header comments.
        """

        return [
            "/-",
            "Project ℵω Lean-style sketch",
            "",
            f"Source statement: {target.statement.name}",
            f"Target kind: {target.target_kind.value}",
            f"Difficulty: {target.difficulty.value}",
            f"Readiness: {target.readiness.value}",
            "",
            "This file is a formalization sketch, not a completed proof.",
            "Any theorem containing `sorry` is unfinished and should not be",
            "presented as machine-checked mathematics.",
            "-/",
        ]

    @staticmethod
    def _definition_placeholders(definitions_needed: List[str]) -> List[str]:
        """
        Builds placeholder definitions.
        """

        if not definitions_needed:
            return [
                "/- No custom definitions were inferred as immediately necessary. -/",
            ]

        lines = [
            "/-",
            "Required definition placeholders.",
            "These must be replaced with mathematically precise definitions.",
            "-/",
        ]

        for definition in definitions_needed:
            lines.append(f"structure {definition} where")
            lines.append("  carrier : Type")
            lines.append("  -- TODO: replace this placeholder with real fields")
            lines.append("")

        return lines

    @staticmethod
    def _assumption_placeholders(assumptions_needed: List[str]) -> List[str]:
        """
        Builds assumption comments.
        """

        if not assumptions_needed:
            return [
                "/- No extra assumptions were inferred. -/",
            ]

        lines = [
            "/-",
            "Required assumptions inferred from the source statement.",
            "These are comments for now because many are informal universe-level assumptions.",
            "-/",
        ]

        for assumption in assumptions_needed:
            lines.append(f"-- assumption: {assumption}")

        return lines

    def _target_code(self, target: FormalizationTarget) -> List[str]:
        """
        Builds target Lean-style code.
        """

        if target.target_kind == FormalTargetKind.DEFINITION:
            return self._definition_code(target)

        if target.target_kind == FormalTargetKind.AXIOM:
            return self._axiom_code(target)

        if target.target_kind in {
            FormalTargetKind.THEOREM,
            FormalTargetKind.LEMMA,
            FormalTargetKind.EXAMPLE,
        }:
            return self._theorem_code(target)

        if target.target_kind == FormalTargetKind.STRUCTURE:
            return self._structure_code(target)

        return self._commentary_sketch_code(target)

    @staticmethod
    def _definition_code(target: FormalizationTarget) -> List[str]:
        """
        Builds definition sketch.
        """

        name = target.theorem_name or "generated_definition"

        return [
            "/- Definition sketch -/",
            f"def {name} : Prop :=",
            "  -- TODO: replace this placeholder proposition with the intended definition",
            "  True",
        ]

    @staticmethod
    def _axiom_code(target: FormalizationTarget) -> List[str]:
        """
        Builds axiom sketch.
        """

        name = target.theorem_name or "generated_axiom"

        return [
            "/- Axiom sketch.",
            "Using axioms should be done carefully and documented explicitly.",
            "-/",
            f"axiom {name} : Prop",
        ]

    @staticmethod
    def _theorem_code(target: FormalizationTarget) -> List[str]:
        """
        Builds theorem or lemma sketch.
        """

        keyword = "lemma" if target.target_kind == FormalTargetKind.LEMMA else "theorem"
        name = target.theorem_name or "generated_theorem"

        return [
            f"/- {keyword.capitalize()} sketch -/",
            f"{keyword} {name} : Prop := by",
            "  -- TODO: replace `Prop` with the real formal goal.",
            f"  -- Informal goal: {target.informal_goal}",
            f"  -- Symbolic sketch: {target.formal_goal_sketch}",
            "  sorry",
        ]

    @staticmethod
    def _structure_code(target: FormalizationTarget) -> List[str]:
        """
        Builds structure sketch.
        """

        name = target.theorem_name or "GeneratedStructure"

        return [
            "/- Structure sketch -/",
            f"structure {name} where",
            "  carrier : Type",
            "  -- TODO: add mathematically meaningful fields",
        ]

    @staticmethod
    def _commentary_sketch_code(target: FormalizationTarget) -> List[str]:
        """
        Builds commentary sketch for concepts not ready as Lean theorems.
        """

        name = target.theorem_name or "generated_commentary"

        return [
            "/-",
            "Commentary sketch.",
            "",
            "This statement is not currently recommended as a direct Lean theorem.",
            "It likely needs custom semantics, definitions, or human review first.",
            "",
            f"Name: {name}",
            f"Informal goal: {target.informal_goal}",
            f"Symbolic sketch: {target.formal_goal_sketch}",
            f"Proof strategy notes: {target.proof_strategy_notes}",
            f"Risk notes: {target.risk_notes}",
            "-/",
            "",
            f"-- placeholder marker for {name}",
            f"def {name}_needs_formal_semantics : Prop :=",
            "  True",
        ]

    @staticmethod
    def _status(target: FormalizationTarget) -> LeanSketchStatus:
        """
        Chooses sketch status.
        """

        if not target.is_ready_for_lean_sketch():
            return LeanSketchStatus.NEEDS_HUMAN_REVIEW

        if target.required_definitions:
            return LeanSketchStatus.NEEDS_DEFINITIONS

        if target.required_assumptions:
            return LeanSketchStatus.NEEDS_ASSUMPTIONS

        return LeanSketchStatus.GENERATED

    @staticmethod
    def _explanation(
        target: FormalizationTarget,
        status: LeanSketchStatus,
        sorry_count: int,
    ) -> str:
        """
        Builds explanation.
        """

        return (
            f"A Lean-style sketch was generated for '{target.statement.name}' "
            f"with status '{status.value}'. The sketch contains {sorry_count} "
            f"`sorry` placeholder(s). It should be treated as a roadmap for "
            f"formalization, not as a completed proof."
        )


if __name__ == "__main__":
    from src.cognitive_morphism.formalization_target import FormalizationTargetBuilder
    from src.cognitive_morphism.formalizer import InformalFormalizer
    from src.cognitive_morphism.intuition import starter_intuitions

    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()

    drafts = formalizer.formalize_many(starter_intuitions())
    targets = builder.build_many([draft.statement for draft in drafts])
    sketches = generator.generate_many(targets)

    for sketch in sketches:
        print(sketch.describe())
        print("-" * 100)
