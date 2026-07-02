"""
Generated finite semantic lab data model for Project Aleph-Omega.

This module defines Python data structures for finite semantic lab diagrams:
systems, morphisms, and chains that can later be exported into Lean/Mathlib.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from src.rigor.lean_finite_system_exporter import ExportedFiniteSystem
from src.rigor.lean_morphism_exporter import ExportedFiniteMorphism


@dataclass(frozen=True)
class GeneratedSemanticLabChain:
    """
    A named finite chain of generated morphisms.
    """

    name: str
    systems: Tuple[ExportedFiniteSystem, ...]
    morphisms: Tuple[ExportedFiniteMorphism, ...]
    description: str

    def validate(self) -> None:
        """
        Validates that the chain is composable.
        """

        if len(self.systems) < 2:
            raise ValueError("A semantic lab chain must contain at least two systems.")

        if len(self.morphisms) != len(self.systems) - 1:
            raise ValueError("A chain with n systems must contain n - 1 morphisms.")

        for index, morphism in enumerate(self.morphisms):
            morphism.validate()

            expected_source = self.systems[index]
            expected_target = self.systems[index + 1]

            if morphism.source.name != expected_source.name:
                raise ValueError(
                    f"Morphism {morphism.name} has wrong source at position {index}."
                )

            if morphism.target.name != expected_target.name:
                raise ValueError(
                    f"Morphism {morphism.name} has wrong target at position {index}."
                )

    def system_count(self) -> int:
        return len(self.systems)

    def morphism_count(self) -> int:
        return len(self.morphisms)

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabChain\n"
            f"Name: {self.name}\n"
            f"Systems: {self.system_count()}\n"
            f"Morphisms: {self.morphism_count()}"
        )


@dataclass(frozen=True)
class GeneratedSemanticLab:
    """
    A generated finite semantic laboratory.
    """

    name: str
    chains: Tuple[GeneratedSemanticLabChain, ...]

    def validate(self) -> None:
        """
        Validates all chains in the lab.
        """

        if not self.name:
            raise ValueError("Semantic lab name cannot be empty.")

        if not self.chains:
            raise ValueError("Semantic lab must contain at least one chain.")

        for chain in self.chains:
            chain.validate()

    def chain_count(self) -> int:
        return len(self.chains)

    def systems(self) -> Tuple[ExportedFiniteSystem, ...]:
        """
        Returns unique systems by name.
        """

        seen = set()
        unique = []

        for chain in self.chains:
            for system in chain.systems:
                if system.name not in seen:
                    seen.add(system.name)
                    unique.append(system)

        return tuple(unique)

    def morphisms(self) -> Tuple[ExportedFiniteMorphism, ...]:
        """
        Returns unique morphisms by name.
        """

        seen = set()
        unique = []

        for chain in self.chains:
            for morphism in chain.morphisms:
                if morphism.name not in seen:
                    seen.add(morphism.name)
                    unique.append(morphism)

        return tuple(unique)

    def system_count(self) -> int:
        return len(self.systems())

    def morphism_count(self) -> int:
        return len(self.morphisms())

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLab\n"
            f"Name: {self.name}\n"
            f"Chains: {self.chain_count()}\n"
            f"Systems: {self.system_count()}\n"
            f"Morphisms: {self.morphism_count()}"
        )


def two_point_system(name: str, model_a: str, model_b: str, sentence_a: str, sentence_b: str) -> ExportedFiniteSystem:
    """
    Builds a deterministic two-point finite system.
    """

    return ExportedFiniteSystem(
        name=name,
        models=(model_a, model_b),
        sentences=(sentence_a, sentence_b),
        satisfying_pairs=((model_a, sentence_a), (model_b, sentence_b)),
    )


def two_point_morphism(
    name: str,
    source: ExportedFiniteSystem,
    target: ExportedFiniteSystem,
    model_map: Dict[str, str],
    sentence_map: Dict[str, str],
) -> ExportedFiniteMorphism:
    """
    Builds a deterministic total finite preservation morphism.
    """

    return ExportedFiniteMorphism(
        name=name,
        source=source,
        target=target,
        model_map=model_map,
        sentence_map=sentence_map,
    )


def build_standard_semantic_lab() -> GeneratedSemanticLab:
    """
    Builds the standard finite semantic lab.

    The lab contains:
    - a two-system example,
    - a three-system chain,
    - a four-system extended chain.
    """

    system_a = two_point_system("LabSystemA", "a0", "a1", "pa", "qa")
    system_b = two_point_system("LabSystemB", "b0", "b1", "pb", "qb")
    system_c = two_point_system("LabSystemC", "c0", "c1", "pc", "qc")
    system_d = two_point_system("LabSystemD", "d0", "d1", "pd", "qd")

    morphism_ab = two_point_morphism(
        name="LabMorphismAB",
        source=system_a,
        target=system_b,
        model_map={"a0": "b0", "a1": "b1"},
        sentence_map={"pa": "pb", "qa": "qb"},
    )

    morphism_bc = two_point_morphism(
        name="LabMorphismBC",
        source=system_b,
        target=system_c,
        model_map={"b0": "c0", "b1": "c1"},
        sentence_map={"pb": "pc", "qb": "qc"},
    )

    morphism_cd = two_point_morphism(
        name="LabMorphismCD",
        source=system_c,
        target=system_d,
        model_map={"c0": "d0", "c1": "d1"},
        sentence_map={"pc": "pd", "qc": "qd"},
    )

    two_system_chain = GeneratedSemanticLabChain(
        name="TwoSystemChain",
        systems=(system_a, system_b),
        morphisms=(morphism_ab,),
        description="A generated two-system preservation example.",
    )

    three_system_chain = GeneratedSemanticLabChain(
        name="ThreeSystemChain",
        systems=(system_a, system_b, system_c),
        morphisms=(morphism_ab, morphism_bc),
        description="A generated three-system preservation chain.",
    )

    four_system_chain = GeneratedSemanticLabChain(
        name="FourSystemChain",
        systems=(system_a, system_b, system_c, system_d),
        morphisms=(morphism_ab, morphism_bc, morphism_cd),
        description="A generated four-system extended preservation chain.",
    )

    return GeneratedSemanticLab(
        name="StandardGeneratedSemanticLab",
        chains=(two_system_chain, three_system_chain, four_system_chain),
    )


class GeneratedSemanticLabModelDocumenter:
    """
    Writes documentation for the generated semantic lab model.
    """

    def to_markdown(self, lab: GeneratedSemanticLab) -> str:
        lab.validate()

        lines = [
            "# Generated Semantic Lab Data Model",
            "",
            "## Purpose",
            "",
            "Phase 34B defines the Python data model for a generated finite semantic lab.",
            "",
            "The lab contains finite systems, preservation morphisms, and composable chains.",
            "",
            "## Summary",
            "",
            f"- Lab name: {lab.name}",
            f"- Chains: {lab.chain_count()}",
            f"- Unique systems: {lab.system_count()}",
            f"- Unique morphisms: {lab.morphism_count()}",
            "",
            "## Chains",
            "",
        ]

        for chain in lab.chains:
            lines.extend(
                [
                    f"### {chain.name}",
                    "",
                    f"- Systems: {chain.system_count()}",
                    f"- Morphisms: {chain.morphism_count()}",
                    f"- Description: {chain.description}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Claim",
                "",
                "> Project Aleph-Omega now has a Python data model for a generated finite semantic lab containing multiple finite systems, preservation morphisms, and composable chains.",
                "",
                "## Boundary",
                "",
                "This phase defines the data model only.",
                "",
                "The next phase should export this lab into generated Lean/Mathlib artifacts.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        lab: GeneratedSemanticLab,
        path: str = "docs/generated_semantic_lab_model.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(lab))
        return output_path


if __name__ == "__main__":
    lab = build_standard_semantic_lab()
    lab.validate()

    output_path = GeneratedSemanticLabModelDocumenter().write_markdown(lab)

    print(lab.describe())
    print(f"Wrote generated semantic lab model docs to {output_path}")
