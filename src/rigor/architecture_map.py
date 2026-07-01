"""
Architecture map generator for Project Aleph-Omega.

This module creates a structured map of the rigor-track architecture.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ArchitectureLayer:
    """
    One architecture layer in the project.
    """

    name: str
    purpose: str
    files: Tuple[str, ...]
    outputs: Tuple[str, ...]

    def file_count(self) -> int:
        """
        Counts files in the layer.
        """

        return len(self.files)

    def output_count(self) -> int:
        """
        Counts outputs in the layer.
        """

        return len(self.outputs)

    def describe(self) -> str:
        """
        Returns a readable layer description.
        """

        return (
            f"ArchitectureLayer\n"
            f"Name: {self.name}\n"
            f"Files: {self.file_count()}\n"
            f"Outputs: {self.output_count()}\n"
            f"Purpose: {self.purpose}"
        )


@dataclass(frozen=True)
class ArchitectureMap:
    """
    Full architecture map.
    """

    layers: Tuple[ArchitectureLayer, ...]

    def layer_count(self) -> int:
        """
        Counts architecture layers.
        """

        return len(self.layers)

    def total_file_count(self) -> int:
        """
        Counts all mapped files.
        """

        return sum(layer.file_count() for layer in self.layers)

    def layer_names(self) -> Tuple[str, ...]:
        """
        Returns layer names.
        """

        return tuple(layer.name for layer in self.layers)

    def describe(self) -> str:
        """
        Returns a readable architecture summary.
        """

        return (
            f"ArchitectureMap\n"
            f"Layers: {self.layer_count()}\n"
            f"Mapped files: {self.total_file_count()}"
        )


class ArchitectureMapBuilder:
    """
    Builds architecture maps for Project Aleph-Omega.
    """

    def build(self) -> ArchitectureMap:
        """
        Builds the standard architecture map.
        """

        layers = (
            ArchitectureLayer(
                name="Finite Universe Layer",
                purpose="Defines finite logical universes, statements, and semantic features.",
                files=(
                    "src/rigor/finite_universe.py",
                    "tests/test_rigor_finite_universe.py",
                ),
                outputs=(
                    "finite statements",
                    "finite logical universes",
                    "semantic feature sets",
                ),
            ),
            ArchitectureLayer(
                name="Bridge and Distortion Layer",
                purpose="Defines finite bridges and detects structural distortion.",
                files=(
                    "src/rigor/bridge.py",
                    "src/rigor/distortion.py",
                    "src/rigor/theorem.py",
                    "tests/test_rigor_bridge.py",
                    "tests/test_rigor_distortion.py",
                    "tests/test_rigor_theorem.py",
                ),
                outputs=(
                    "finite bridges",
                    "distortion reports",
                    "bridge distortion theorem checks",
                ),
            ),
            ArchitectureLayer(
                name="Satisfaction Semantics Layer",
                purpose="Defines truth-value spaces, interpretations, satisfaction, and preservation.",
                files=(
                    "src/rigor/semantics.py",
                    "src/rigor/interpretation.py",
                    "src/rigor/satisfaction.py",
                    "src/rigor/preservation.py",
                    "src/rigor/preservation_theorem.py",
                    "tests/test_rigor_semantics.py",
                    "tests/test_rigor_interpretation.py",
                    "tests/test_rigor_satisfaction.py",
                    "tests/test_rigor_preservation.py",
                    "tests/test_rigor_preservation_theorem.py",
                ),
                outputs=(
                    "truth-value spaces",
                    "universe interpretations",
                    "satisfaction reports",
                    "preservation theorem checks",
                ),
            ),
            ArchitectureLayer(
                name="Category and Composition Layer",
                purpose="Defines bridge composition, identity laws, associativity, and category-like structure.",
                files=(
                    "src/rigor/composition.py",
                    "src/rigor/category.py",
                    "src/rigor/identity_laws.py",
                    "src/rigor/associativity.py",
                    "tests/test_rigor_composition.py",
                    "tests/test_rigor_category.py",
                    "tests/test_rigor_identity_laws.py",
                    "tests/test_rigor_associativity.py",
                ),
                outputs=(
                    "composed bridges",
                    "identity law reports",
                    "associativity reports",
                    "finite universe categories",
                ),
            ),
            ArchitectureLayer(
                name="Functorial Semantics Layer",
                purpose="Connects composition with semantic transport and preservation under composition.",
                files=(
                    "src/rigor/semantic_transport.py",
                    "src/rigor/composition_preservation.py",
                    "src/rigor/composition_preservation_theorem.py",
                    "src/rigor/distortion_accumulation.py",
                    "src/rigor/functorial_examples.py",
                    "tests/test_rigor_semantic_transport.py",
                    "tests/test_rigor_composition_preservation.py",
                    "tests/test_rigor_composition_preservation_theorem.py",
                    "tests/test_rigor_distortion_accumulation.py",
                    "tests/test_rigor_functorial_examples.py",
                ),
                outputs=(
                    "semantic transport reports",
                    "composition preservation checks",
                    "distortion accumulation reports",
                    "functorial examples",
                ),
            ),
            ArchitectureLayer(
                name="Finite Model Search Layer",
                purpose="Generates finite structures and stress-tests theorem-like claims.",
                files=(
                    "src/rigor/model_search.py",
                    "src/rigor/bridge_case_generator.py",
                    "src/rigor/bridge_distortion_search.py",
                    "src/rigor/satisfaction_search.py",
                    "src/rigor/search_report.py",
                    "tests/test_rigor_model_search.py",
                    "tests/test_rigor_bridge_case_generator.py",
                    "tests/test_rigor_bridge_distortion_search.py",
                    "tests/test_rigor_satisfaction_search.py",
                    "tests/test_rigor_search_report.py",
                ),
                outputs=(
                    "generated universes",
                    "generated bridges",
                    "search reports",
                    "model-search markdown report",
                ),
            ),
            ArchitectureLayer(
                name="Failure Laboratory Layer",
                purpose="Extracts, classifies, and reports generated semantic failure cases.",
                files=(
                    "src/rigor/failure_taxonomy.py",
                    "src/rigor/failure_extractor.py",
                    "src/rigor/failure_report.py",
                    "src/rigor/theorem_boundary.py",
                    "tests/test_rigor_failure_taxonomy.py",
                    "tests/test_rigor_failure_extractor.py",
                    "tests/test_rigor_failure_report.py",
                    "tests/test_rigor_theorem_boundary.py",
                ),
                outputs=(
                    "failure classifications",
                    "extracted failure cases",
                    "failure lab report",
                    "theorem boundary analysis",
                ),
            ),
            ArchitectureLayer(
                name="Verification Interface Layer",
                purpose="Records claims, audits theorem-like statements, and tracks proof obligations.",
                files=(
                    "src/rigor/claim_registry.py",
                    "src/rigor/theorem_audit.py",
                    "src/rigor/proof_obligations.py",
                    "src/rigor/verification_report.py",
                    "tests/test_rigor_claim_registry.py",
                    "tests/test_rigor_theorem_audit.py",
                    "tests/test_rigor_proof_obligations.py",
                    "tests/test_rigor_verification_report.py",
                ),
                outputs=(
                    "formal claim registry",
                    "theorem audit report",
                    "proof obligation report",
                    "verification report",
                ),
            ),
            ArchitectureLayer(
                name="Research Artifact Layer",
                purpose="Exports human-readable research artifacts from the project.",
                files=(
                    "src/rigor/research_abstract.py",
                    "src/rigor/theorem_inventory.py",
                    "src/rigor/architecture_map.py",
                    "tests/test_rigor_research_abstract.py",
                    "tests/test_rigor_theorem_inventory.py",
                    "tests/test_rigor_architecture_map.py",
                ),
                outputs=(
                    "research abstract",
                    "theorem inventory",
                    "architecture map",
                ),
            ),
        )

        return ArchitectureMap(layers=layers)

    def to_markdown(self, architecture_map: ArchitectureMap) -> str:
        """
        Converts the architecture map to markdown.
        """

        lines = [
            "# Architecture Map",
            "",
            "## Purpose",
            "",
            "This document maps the major rigor-track layers of Project Aleph-Omega.",
            "",
            "It shows how the project moves from finite logical objects to theorem checks, model search, failure analysis, verification records, and exportable research artifacts.",
            "",
            "## Summary",
            "",
            f"- Architecture layers: {architecture_map.layer_count()}",
            f"- Mapped files: {architecture_map.total_file_count()}",
            "",
            "## Layers",
            "",
        ]

        for index, layer in enumerate(architecture_map.layers, start=1):
            lines.extend(
                [
                    f"### {index}. {layer.name}",
                    "",
                    f"Purpose: {layer.purpose}",
                    "",
                    "Files:",
                    "",
                ]
            )

            for file_name in layer.files:
                lines.append(f"- {file_name}")

            lines.extend(
                [
                    "",
                    "Outputs:",
                    "",
                ]
            )

            for output in layer.outputs:
                lines.append(f"- {output}")

            lines.append("")

        lines.extend(
            [
                "## Architecture Interpretation",
                "",
                "The architecture is intentionally layered.",
                "",
                "The lower layers define finite mathematical objects.",
                "",
                "The middle layers define theorem-like checks, composition, preservation, and generated search.",
                "",
                "The upper layers classify failure, audit claims, track proof obligations, and export research artifacts.",
                "",
                "This structure makes the project easier to review and harder to overstate.",
                "",
                "## Correct Research Framing",
                "",
                "The architecture map describes the implemented finite research system.",
                "",
                "It does not imply that the project proves universal results about all mathematical foundations.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        architecture_map: ArchitectureMap,
        path: str = "docs/architecture_map.md",
    ) -> Path:
        """
        Writes the architecture map to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(architecture_map))
        return output_path


if __name__ == "__main__":
    builder = ArchitectureMapBuilder()
    architecture_map = builder.build()
    output_path = builder.write_markdown(architecture_map)

    print(architecture_map.describe())
    print(f"Wrote architecture map to {output_path}")
