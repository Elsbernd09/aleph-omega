"""
Generated semantic lab artifact index for Project Aleph-Omega.

This module indexes the systems, morphisms, quotient wrappers, and composition
theorems in the generated finite semantic lab.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class GeneratedSemanticLabIndexedArtifact:
    """
    One indexed semantic lab artifact.
    """

    name: str
    artifact_kind: str
    lean_name: str
    location: str
    role: str
    verification: str

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabIndexedArtifact\n"
            f"Name: {self.name}\n"
            f"Kind: {self.artifact_kind}\n"
            f"Lean name: {self.lean_name}"
        )


@dataclass(frozen=True)
class GeneratedSemanticLabArtifactIndex:
    """
    Index of generated semantic lab artifacts.
    """

    title: str
    artifacts: Tuple[GeneratedSemanticLabIndexedArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def system_artifacts(self) -> Tuple[GeneratedSemanticLabIndexedArtifact, ...]:
        return tuple(
            artifact for artifact in self.artifacts
            if "system" in artifact.artifact_kind.lower()
        )

    def morphism_artifacts(self) -> Tuple[GeneratedSemanticLabIndexedArtifact, ...]:
        return tuple(
            artifact for artifact in self.artifacts
            if "morphism" in artifact.artifact_kind.lower()
        )

    def quotient_artifacts(self) -> Tuple[GeneratedSemanticLabIndexedArtifact, ...]:
        return tuple(
            artifact for artifact in self.artifacts
            if "quotient" in artifact.artifact_kind.lower()
            or "quotient" in artifact.role.lower()
        )

    def theorem_artifacts(self) -> Tuple[GeneratedSemanticLabIndexedArtifact, ...]:
        return tuple(
            artifact for artifact in self.artifacts
            if "theorem" in artifact.artifact_kind.lower()
        )

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabArtifactIndex\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Systems: {len(self.system_artifacts())}\n"
            f"Morphisms: {len(self.morphism_artifacts())}\n"
            f"Quotient artifacts: {len(self.quotient_artifacts())}\n"
            f"Theorems: {len(self.theorem_artifacts())}"
        )


class GeneratedSemanticLabArtifactIndexBuilder:
    """
    Builds the generated semantic lab artifact index.
    """

    def build(self) -> GeneratedSemanticLabArtifactIndex:
        location = "formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean"

        artifacts = (
            GeneratedSemanticLabIndexedArtifact(
                name="Lab System A",
                artifact_kind="finite system",
                lean_name="LabSystemASystem",
                location=location,
                role="First object in the generated semantic lab.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab System B",
                artifact_kind="finite system",
                lean_name="LabSystemBSystem",
                location=location,
                role="Second object in the generated semantic lab.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab System C",
                artifact_kind="finite system",
                lean_name="LabSystemCSystem",
                location=location,
                role="Third object in the generated semantic lab.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab System D",
                artifact_kind="finite system",
                lean_name="LabSystemDSystem",
                location=location,
                role="Fourth object in the generated semantic lab.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab Morphism AB",
                artifact_kind="preservation morphism",
                lean_name="LabMorphismABMorphism",
                location=location,
                role="Generated satisfaction-preserving morphism from A to B.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab Morphism BC",
                artifact_kind="preservation morphism",
                lean_name="LabMorphismBCMorphism",
                location=location,
                role="Generated satisfaction-preserving morphism from B to C.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Lab Morphism CD",
                artifact_kind="preservation morphism",
                lean_name="LabMorphismCDMorphism",
                location=location,
                role="Generated satisfaction-preserving morphism from C to D.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Quotient Lab Morphism AB",
                artifact_kind="quotient morphism",
                lean_name="qLabMorphismAB",
                location=location,
                role="Quotient class of the generated A-to-B morphism.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Quotient Lab Morphism BC",
                artifact_kind="quotient morphism",
                lean_name="qLabMorphismBC",
                location=location,
                role="Quotient class of the generated B-to-C morphism.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Quotient Lab Morphism CD",
                artifact_kind="quotient morphism",
                lean_name="qLabMorphismCD",
                location=location,
                role="Quotient class of the generated C-to-D morphism.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Composition ABC",
                artifact_kind="quotient composition theorem",
                lean_name="q_category_lab_composition_abc",
                location=location,
                role="Generated theorem proving quotient-category composition along A -> B -> C.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Composition BCD",
                artifact_kind="quotient composition theorem",
                lean_name="q_category_lab_composition_bcd",
                location=location,
                role="Generated theorem proving quotient-category composition along B -> C -> D.",
                verification="Mathlib Lake build",
            ),
            GeneratedSemanticLabIndexedArtifact(
                name="Semantic Lab Lean File",
                artifact_kind="generated Mathlib file",
                lean_name="AlephOmegaMathlib.Generated.SemanticLab",
                location=location,
                role="Generated Mathlib file containing the full finite semantic lab.",
                verification="Generated Mathlib checker and formal-stack gate",
            ),
        )

        return GeneratedSemanticLabArtifactIndex(
            title="Project Aleph-Omega Generated Semantic Lab Artifact Index",
            artifacts=artifacts,
        )

    def to_markdown(self, index: GeneratedSemanticLabArtifactIndex) -> str:
        lines = [
            "# Project Aleph-Omega Generated Semantic Lab Artifact Index",
            "",
            "## Purpose",
            "",
            "This document indexes the generated finite semantic lab artifacts.",
            "",
            "It identifies each generated system, preservation morphism, quotient wrapper, and quotient-composition theorem in the semantic lab.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {index.artifact_count()}",
            f"- Systems: {len(index.system_artifacts())}",
            f"- Morphisms: {len(index.morphism_artifacts())}",
            f"- Quotient artifacts: {len(index.quotient_artifacts())}",
            f"- Theorems: {len(index.theorem_artifacts())}",
            "",
            "## Artifact Table",
            "",
            "| Name | Kind | Lean name | Location | Role | Verification |",
            "|---|---|---|---|---|---|",
        ]

        for artifact in index.artifacts:
            lines.append(
                f"| {artifact.name} | {artifact.artifact_kind} | `{artifact.lean_name}` | `{artifact.location}` | {artifact.role} | {artifact.verification} |"
            )

        lines.extend(
            [
                "",
                "## Strongest Current Claim",
                "",
                "> Project Aleph-Omega now has a reviewer-facing index of the generated finite semantic lab, including four generated systems, three generated preservation morphisms, quotient morphism classes, and two generated quotient-category composition theorems.",
                "",
                "## Boundary",
                "",
                "This is a static index for the current generated semantic lab.",
                "",
                "It is not yet an automatic parser over arbitrary generated Lean files.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        index: GeneratedSemanticLabArtifactIndex,
        path: str = "docs/generated_semantic_lab_artifact_index.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(index))
        return output_path


if __name__ == "__main__":
    builder = GeneratedSemanticLabArtifactIndexBuilder()
    index = builder.build()
    output_path = builder.write_markdown(index)

    print(index.describe())
    print(f"Wrote generated semantic lab artifact index to {output_path}")
