"""
Generated diamond diagram data model for Project Aleph-Omega.

This module defines a finite diamond semantic diagram:

        B
      /   \
A           D
      \   /
        C

with two paths A -> B -> D and A -> C -> D.

The design prepares the project for nontrivial quotient path equivalence:
the two paths are distinct composites but agree pointwise on source models and
sentences.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from src.rigor.lean_finite_system_exporter import ExportedFiniteSystem
from src.rigor.lean_morphism_exporter import ExportedFiniteMorphism


@dataclass(frozen=True)
class GeneratedDiamondDiagram:
    """
    A generated finite semantic diamond diagram.
    """

    name: str
    source: ExportedFiniteSystem
    upper: ExportedFiniteSystem
    lower: ExportedFiniteSystem
    target: ExportedFiniteSystem
    source_to_upper: ExportedFiniteMorphism
    source_to_lower: ExportedFiniteMorphism
    upper_to_target: ExportedFiniteMorphism
    lower_to_target: ExportedFiniteMorphism
    description: str

    def validate(self) -> None:
        """
        Validates that the diamond is well-formed and preservation-safe.
        """

        self.source.validate()
        self.upper.validate()
        self.lower.validate()
        self.target.validate()

        for morphism in self.morphisms():
            morphism.validate()

        if self.source_to_upper.source.name != self.source.name:
            raise ValueError("source_to_upper has wrong source.")
        if self.source_to_upper.target.name != self.upper.name:
            raise ValueError("source_to_upper has wrong target.")

        if self.source_to_lower.source.name != self.source.name:
            raise ValueError("source_to_lower has wrong source.")
        if self.source_to_lower.target.name != self.lower.name:
            raise ValueError("source_to_lower has wrong target.")

        if self.upper_to_target.source.name != self.upper.name:
            raise ValueError("upper_to_target has wrong source.")
        if self.upper_to_target.target.name != self.target.name:
            raise ValueError("upper_to_target has wrong target.")

        if self.lower_to_target.source.name != self.lower.name:
            raise ValueError("lower_to_target has wrong source.")
        if self.lower_to_target.target.name != self.target.name:
            raise ValueError("lower_to_target has wrong target.")

        if not self.paths_agree_on_models():
            raise ValueError("Diamond paths do not agree on model maps.")

        if not self.paths_agree_on_sentences():
            raise ValueError("Diamond paths do not agree on sentence translations.")

    def systems(self) -> Tuple[ExportedFiniteSystem, ...]:
        return (self.source, self.upper, self.lower, self.target)

    def morphisms(self) -> Tuple[ExportedFiniteMorphism, ...]:
        return (
            self.source_to_upper,
            self.source_to_lower,
            self.upper_to_target,
            self.lower_to_target,
        )

    def upper_path_model_map(self, model: str) -> str:
        intermediate = self.source_to_upper.model_map[model]
        return self.upper_to_target.model_map[intermediate]

    def lower_path_model_map(self, model: str) -> str:
        intermediate = self.source_to_lower.model_map[model]
        return self.lower_to_target.model_map[intermediate]

    def upper_path_sentence_map(self, sentence: str) -> str:
        intermediate = self.source_to_upper.sentence_map[sentence]
        return self.upper_to_target.sentence_map[intermediate]

    def lower_path_sentence_map(self, sentence: str) -> str:
        intermediate = self.source_to_lower.sentence_map[sentence]
        return self.lower_to_target.sentence_map[intermediate]

    def paths_agree_on_models(self) -> bool:
        return all(
            self.upper_path_model_map(model) == self.lower_path_model_map(model)
            for model in self.source.models
        )

    def paths_agree_on_sentences(self) -> bool:
        return all(
            self.upper_path_sentence_map(sentence) == self.lower_path_sentence_map(sentence)
            for sentence in self.source.sentences
        )

    def describe(self) -> str:
        return (
            f"GeneratedDiamondDiagram\n"
            f"Name: {self.name}\n"
            f"Systems: {len(self.systems())}\n"
            f"Morphisms: {len(self.morphisms())}\n"
            f"Paths agree on models: {self.paths_agree_on_models()}\n"
            f"Paths agree on sentences: {self.paths_agree_on_sentences()}"
        )


def diamond_system(
    name: str,
    model0: str,
    model1: str,
    sentence0: str,
    sentence1: str,
) -> ExportedFiniteSystem:
    """
    Builds a two-point diamond system.
    """

    return ExportedFiniteSystem(
        name=name,
        models=(model0, model1),
        sentences=(sentence0, sentence1),
        satisfying_pairs=((model0, sentence0), (model1, sentence1)),
    )


def build_standard_diamond_diagram() -> GeneratedDiamondDiagram:
    """
    Builds the standard finite diamond diagram.

    The two paths from A to D agree pointwise:

    A -> B -> D
    A -> C -> D
    """

    source = diamond_system("DiamondSystemA", "a0", "a1", "pa", "qa")
    upper = diamond_system("DiamondSystemB", "b0", "b1", "pb", "qb")
    lower = diamond_system("DiamondSystemC", "c0", "c1", "pc", "qc")
    target = diamond_system("DiamondSystemD", "d0", "d1", "pd", "qd")

    source_to_upper = ExportedFiniteMorphism(
        name="DiamondMorphismAB",
        source=source,
        target=upper,
        model_map={"a0": "b0", "a1": "b1"},
        sentence_map={"pa": "pb", "qa": "qb"},
    )

    source_to_lower = ExportedFiniteMorphism(
        name="DiamondMorphismAC",
        source=source,
        target=lower,
        model_map={"a0": "c0", "a1": "c1"},
        sentence_map={"pa": "pc", "qa": "qc"},
    )

    upper_to_target = ExportedFiniteMorphism(
        name="DiamondMorphismBD",
        source=upper,
        target=target,
        model_map={"b0": "d0", "b1": "d1"},
        sentence_map={"pb": "pd", "qb": "qd"},
    )

    lower_to_target = ExportedFiniteMorphism(
        name="DiamondMorphismCD",
        source=lower,
        target=target,
        model_map={"c0": "d0", "c1": "d1"},
        sentence_map={"pc": "pd", "qc": "qd"},
    )

    return GeneratedDiamondDiagram(
        name="StandardGeneratedDiamond",
        source=source,
        upper=upper,
        lower=lower,
        target=target,
        source_to_upper=source_to_upper,
        source_to_lower=source_to_lower,
        upper_to_target=upper_to_target,
        lower_to_target=lower_to_target,
        description="A finite diamond diagram whose two source-to-target paths agree pointwise.",
    )


class GeneratedDiamondDiagramDocumenter:
    """
    Writes documentation for the generated diamond diagram model.
    """

    def to_markdown(self, diagram: GeneratedDiamondDiagram) -> str:
        diagram.validate()

        lines = [
            "# Generated Diamond Diagram Data Model",
            "",
            "## Purpose",
            "",
            "Phase 35C defines the Python data model for a generated finite diamond diagram.",
            "",
            "The diamond has two distinct paths from a source system to a target system.",
            "",
            "```text",
            "        B",
            "      /   \\",
            "A           D",
            "      \\   /",
            "        C",
            "```",
            "",
            "## Summary",
            "",
            f"- Diagram name: {diagram.name}",
            f"- Systems: {len(diagram.systems())}",
            f"- Morphisms: {len(diagram.morphisms())}",
            f"- Paths agree on models: {diagram.paths_agree_on_models()}",
            f"- Paths agree on sentences: {diagram.paths_agree_on_sentences()}",
            "",
            "## Systems",
            "",
        ]

        for system in diagram.systems():
            lines.append(f"- {system.name}")

        lines.extend(
            [
                "",
                "## Morphisms",
                "",
            ]
        )

        for morphism in diagram.morphisms():
            lines.append(f"- {morphism.name}: {morphism.source.name} -> {morphism.target.name}")

        lines.extend(
            [
                "",
                "## Path Agreement",
                "",
                "The upper path A -> B -> D and lower path A -> C -> D agree pointwise on:",
                "",
                "- source models,",
                "- source sentences.",
                "",
                "This prepares the Lean/Mathlib theorem that the two paths are equal as quotient morphisms.",
                "",
                "## Strongest Claim",
                "",
                "> Project Aleph-Omega now has a Python data model for a generated finite diamond diagram whose two distinct paths agree pointwise on models and sentence translations.",
                "",
                "## Boundary",
                "",
                "This phase defines the Python diamond data model only.",
                "",
                "The next phase should export this diamond into Mathlib and prove quotient path equivalence.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        diagram: GeneratedDiamondDiagram,
        path: str = "docs/generated_diamond_diagram_model.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(diagram))
        return output_path


if __name__ == "__main__":
    diagram = build_standard_diamond_diagram()
    diagram.validate()

    output_path = GeneratedDiamondDiagramDocumenter().write_markdown(diagram)

    print(diagram.describe())
    print(f"Wrote generated diamond diagram model docs to {output_path}")
