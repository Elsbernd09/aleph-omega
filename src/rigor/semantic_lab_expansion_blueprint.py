"""
Semantic lab expansion blueprint for Project Aleph-Omega.

This module plans the expansion of the generated finite semantic lab beyond
one chain family into multiple named finite semantic diagram families.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class SemanticLabExpansionRequirement:
    """
    One requirement for expanding the generated semantic lab.
    """

    name: str
    purpose: str
    diagram_target: str
    verification_target: str
    limitation: str

    def describe(self) -> str:
        return (
            f"SemanticLabExpansionRequirement\n"
            f"Name: {self.name}\n"
            f"Diagram target: {self.diagram_target}\n"
            f"Verification: {self.verification_target}"
        )


@dataclass(frozen=True)
class SemanticLabExpansionBlueprint:
    """
    Blueprint for expanding the generated semantic lab.
    """

    title: str
    requirements: Tuple[SemanticLabExpansionRequirement, ...]

    def requirement_count(self) -> int:
        return len(self.requirements)

    def diagram_requirements(self) -> Tuple[SemanticLabExpansionRequirement, ...]:
        return tuple(
            requirement
            for requirement in self.requirements
            if "diagram" in requirement.diagram_target.lower()
            or "diagram" in requirement.purpose.lower()
        )

    def quotient_requirements(self) -> Tuple[SemanticLabExpansionRequirement, ...]:
        return tuple(
            requirement
            for requirement in self.requirements
            if "quotient" in requirement.diagram_target.lower()
            or "quotient" in requirement.purpose.lower()
        )

    def verified_requirements(self) -> Tuple[SemanticLabExpansionRequirement, ...]:
        return tuple(
            requirement
            for requirement in self.requirements
            if "Mathlib" in requirement.verification_target
            or "Lake" in requirement.verification_target
            or "formal-stack" in requirement.verification_target
            or "pytest" in requirement.verification_target
        )

    def describe(self) -> str:
        return (
            f"SemanticLabExpansionBlueprint\n"
            f"Title: {self.title}\n"
            f"Requirements: {self.requirement_count()}\n"
            f"Diagram requirements: {len(self.diagram_requirements())}\n"
            f"Quotient requirements: {len(self.quotient_requirements())}\n"
            f"Verified requirements: {len(self.verified_requirements())}"
        )


class SemanticLabExpansionBlueprintBuilder:
    """
    Builds the semantic lab expansion blueprint.
    """

    def build(self) -> SemanticLabExpansionBlueprint:
        requirements = (
            SemanticLabExpansionRequirement(
                name="Parallel translation diagram",
                purpose="Generate two different preservation morphisms from one source system to two target systems.",
                diagram_target="Generated parallel semantic diagram",
                verification_target="pytest and Mathlib Lake build",
                limitation="Initial version should use finite two-point systems only.",
            ),
            SemanticLabExpansionRequirement(
                name="Diamond diagram",
                purpose="Generate a finite diamond diagram with two paths from a source to a final target.",
                diagram_target="Generated diamond quotient diagram",
                verification_target="pytest and Mathlib Lake build",
                limitation="First diamond should prove a small definitional equality only.",
            ),
            SemanticLabExpansionRequirement(
                name="Commutativity theorem",
                purpose="Prove that two generated quotient-category paths produce the same quotient morphism.",
                diagram_target="Generated quotient commutativity theorem",
                verification_target="Mathlib Lake build and formal-stack gate",
                limitation="First theorem may rely on definitional equality rather than deep equivalence reasoning.",
            ),
            SemanticLabExpansionRequirement(
                name="Failure contrast example",
                purpose="Generate a finite map that fails preservation and document why it cannot be exported as a PreservationMorphism.",
                diagram_target="Generated semantic failure report",
                verification_target="pytest",
                limitation="Failure examples are documented in Python first, not Lean theorem failures.",
            ),
            SemanticLabExpansionRequirement(
                name="Diagram metadata index",
                purpose="Give reviewers a map of all expanded semantic lab diagrams.",
                diagram_target="Generated diagram index documentation",
                verification_target="pytest documentation tests",
                limitation="Static index at first.",
            ),
            SemanticLabExpansionRequirement(
                name="Regeneration script integration",
                purpose="Make expanded diagrams reproducible through the generated Mathlib checker.",
                diagram_target="Generated semantic lab expansion checker integration",
                verification_target="formal-stack gate",
                limitation="Depends on local Lean, Lake, elan, and Python setup.",
            ),
            SemanticLabExpansionRequirement(
                name="Boundary and non-claim documentation",
                purpose="Prevent overclaiming and keep the expansion clearly finite/prototype-level.",
                diagram_target="Generated semantic lab expansion documentation",
                verification_target="pytest documentation tests",
                limitation="Documentation does not replace general theorem proving.",
            ),
            SemanticLabExpansionRequirement(
                name="Reviewer-facing summary",
                purpose="Explain why expanded diagrams are stronger than a single chain.",
                diagram_target="Generated semantic lab expansion report",
                verification_target="pytest documentation tests",
                limitation="Report only.",
            ),
        )

        return SemanticLabExpansionBlueprint(
            title="Project Aleph-Omega Semantic Lab Expansion Blueprint",
            requirements=requirements,
        )

    def to_markdown(self, blueprint: SemanticLabExpansionBlueprint) -> str:
        lines = [
            "# Project Aleph-Omega Semantic Lab Expansion Blueprint",
            "",
            "## Purpose",
            "",
            "This document begins Phase 35: expansion of the generated finite semantic lab.",
            "",
            "Phase 34 created one generated semantic lab chain family.",
            "",
            "Phase 35 expands the lab toward multiple named finite semantic diagram families, including parallel diagrams, diamond diagrams, quotient commutativity theorems, and failure contrasts.",
            "",
            "## Summary",
            "",
            f"- Requirements indexed: {blueprint.requirement_count()}",
            f"- Diagram requirements: {len(blueprint.diagram_requirements())}",
            f"- Quotient requirements: {len(blueprint.quotient_requirements())}",
            f"- Verified requirements: {len(blueprint.verified_requirements())}",
            "",
            "## Requirements",
            "",
        ]

        for index, requirement in enumerate(blueprint.requirements, start=1):
            lines.extend(
                [
                    f"### {index}. {requirement.name}",
                    "",
                    f"- Purpose: {requirement.purpose}",
                    f"- Diagram target: `{requirement.diagram_target}`",
                    f"- Verification target: {requirement.verification_target}",
                    f"- Limitation: {requirement.limitation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## First Implementation Target",
                "",
                "The first implementation target should add a generated diamond diagram data model.",
                "",
                "The diamond should contain:",
                "",
                "- one source system,",
                "- two intermediate systems,",
                "- one target system,",
                "- two distinct paths from source to target,",
                "- a generated quotient-category commutativity theorem.",
                "",
                "## Strongest Claim After This Phase",
                "",
                "> Project Aleph-Omega now has a precise plan for expanding its generated finite semantic lab beyond chains into multiple named finite semantic diagram families.",
                "",
                "## Non-Claim",
                "",
                "This phase does not yet generate the expanded diagrams.",
                "",
                "The next phase should define the expanded semantic lab data model.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        blueprint: SemanticLabExpansionBlueprint,
        path: str = "docs/semantic_lab_expansion_blueprint.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(blueprint))
        return output_path


if __name__ == "__main__":
    builder = SemanticLabExpansionBlueprintBuilder()
    blueprint = builder.build()
    output_path = builder.write_markdown(blueprint)

    print(blueprint.describe())
    print(f"Wrote semantic lab expansion blueprint to {output_path}")
