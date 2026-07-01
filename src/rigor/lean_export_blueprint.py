"""
Lean export blueprint for Project Aleph-Omega.

This module documents the technical plan for exporting finite Python semantic
systems into Lean definitions and theorem stubs.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LeanExportRequirement:
    """
    One requirement for exporting Python finite systems into Lean.
    """

    name: str
    python_source: str
    lean_target: str
    challenge: str
    planned_solution: str

    def describe(self) -> str:
        return (
            f"LeanExportRequirement\n"
            f"Name: {self.name}\n"
            f"Python source: {self.python_source}\n"
            f"Lean target: {self.lean_target}"
        )


@dataclass(frozen=True)
class LeanExportBlueprint:
    """
    Blueprint for Python-to-Lean finite model export.
    """

    title: str
    requirements: Tuple[LeanExportRequirement, ...]

    def requirement_count(self) -> int:
        return len(self.requirements)

    def describe(self) -> str:
        return (
            f"LeanExportBlueprint\n"
            f"Title: {self.title}\n"
            f"Requirements: {self.requirement_count()}"
        )


class LeanExportBlueprintBuilder:
    """
    Builds the Lean export blueprint.
    """

    def build(self) -> LeanExportBlueprint:
        requirements = (
            LeanExportRequirement(
                name="Finite model enumeration",
                python_source="FiniteInstitution.models",
                lean_target="inductive Model where ...",
                challenge="Python objects may have arbitrary names not valid as Lean constructors.",
                planned_solution="Normalize names into Lean-safe identifiers and preserve original names in comments.",
            ),
            LeanExportRequirement(
                name="Finite sentence enumeration",
                python_source="FiniteInstitution.sentences",
                lean_target="inductive Sentence where ...",
                challenge="Sentence names may contain symbols or whitespace.",
                planned_solution="Generate sanitized constructors such as s0, s1, s2 with comment metadata.",
            ),
            LeanExportRequirement(
                name="Satisfaction relation",
                python_source="FiniteModel.satisfies(sentence)",
                lean_target="Sat := fun m φ => match m, φ with ...",
                challenge="Need exhaustive finite match cases.",
                planned_solution="Emit True for satisfying pairs and False for all other cases.",
            ),
            LeanExportRequirement(
                name="Positive satisfaction proofs",
                python_source="pairs where model satisfies sentence",
                lean_target="theorem exported_model_satisfies_sentence : System.Sat m s := by trivial",
                challenge="Names must be unique and readable.",
                planned_solution="Generate deterministic theorem names from model and sentence indices.",
            ),
            LeanExportRequirement(
                name="Negative satisfaction proofs",
                python_source="pairs where model does not satisfy sentence",
                lean_target="theorem exported_model_not_satisfy_sentence : ¬ System.Sat m s := by intro h; cases h",
                challenge="False cases must reduce definitionally.",
                planned_solution="Use match-defined Sat so negative proofs reduce to False.",
            ),
            LeanExportRequirement(
                name="Bridge translation export",
                python_source="FiniteBridge.statement_mapping",
                lean_target="def exportedTranslate : Source.Sentence -> Target.Sentence",
                challenge="Partial bridges may not map every sentence.",
                planned_solution="First support total bridges; document partial bridge export as future work.",
            ),
            LeanExportRequirement(
                name="Model map export",
                python_source="ModelPairing.source_model -> target_model",
                lean_target="def exportedMapModel : Source.Model -> Target.Model",
                challenge="Model pairings must be total for Lean function export.",
                planned_solution="Require total finite pairings in the first exporter version.",
            ),
            LeanExportRequirement(
                name="Preservation morphism export",
                python_source="FiniteInstitutionMorphism",
                lean_target="def exportedMorphism : PreservationMorphism Source Target",
                challenge="Need a Lean proof that all satisfying source pairs map to satisfying target pairs.",
                planned_solution="Generate proof by exhaustive cases over finite source models and sentences.",
            ),
            LeanExportRequirement(
                name="Exporter validation",
                python_source="generated Lean file",
                lean_target="lean generated_file.lean",
                challenge="Export is only meaningful if Lean accepts the generated file.",
                planned_solution="Add script-level validation that runs Lean on generated artifacts.",
            ),
        )

        return LeanExportBlueprint(
            title="Project Aleph-Omega Python-to-Lean Export Blueprint",
            requirements=requirements,
        )

    def to_markdown(self, blueprint: LeanExportBlueprint) -> str:
        lines = [
            "# Project Aleph-Omega Python-to-Lean Export Blueprint",
            "",
            "## Purpose",
            "",
            "This document begins the Python-to-Lean finite model export track.",
            "",
            "The goal is to generate Lean finite systems automatically from Python finite semantic data.",
            "",
            "## Why This Matters",
            "",
            "Project Aleph-Omega already has Python finite semantic systems and hand-written Lean examples.",
            "",
            "The next serious upgrade is to connect them by generating Lean definitions from Python data.",
            "",
            "That turns the Python layer from a parallel analogue into a producer of machine-checkable Lean artifacts.",
            "",
            "## Summary",
            "",
            f"- Export requirements indexed: {blueprint.requirement_count()}",
            "",
            "## Requirements",
            "",
        ]

        for index, requirement in enumerate(blueprint.requirements, start=1):
            lines.extend(
                [
                    f"### {index}. {requirement.name}",
                    "",
                    f"- Python source: `{requirement.python_source}`",
                    f"- Lean target: `{requirement.lean_target}`",
                    f"- Challenge: {requirement.challenge}",
                    f"- Planned solution: {requirement.planned_solution}",
                    "",
                ]
            )

        lines.extend(
            [
                "## First Export Target",
                "",
                "The first exporter should generate a simple finite Lean system with:",
                "",
                "- an inductive model type,",
                "- an inductive sentence type,",
                "- a match-defined satisfaction relation,",
                "- positive satisfaction theorems,",
                "- negative satisfaction theorems.",
                "",
                "## Later Export Target",
                "",
                "The later exporter should generate:",
                "",
                "- translations,",
                "- model maps,",
                "- preservation morphisms,",
                "- exhaustive preservation proofs.",
                "",
                "## Strongest Claim After This Phase",
                "",
                "> Project Aleph-Omega now has a technical blueprint for exporting finite Python semantic systems into Lean finite formal systems.",
                "",
                "## Non-Claim",
                "",
                "This phase does not yet generate Lean code.",
                "",
                "The next phase should implement the first exporter.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        blueprint: LeanExportBlueprint,
        path: str = "docs/lean_export_blueprint.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(blueprint))
        return output_path


if __name__ == "__main__":
    builder = LeanExportBlueprintBuilder()
    blueprint = builder.build()
    output_path = builder.write_markdown(blueprint)

    print(blueprint.describe())
    print(f"Wrote Lean export blueprint to {output_path}")
