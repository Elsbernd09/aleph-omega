"""
Generated semantic lab completion report for Project Aleph-Omega.

This module summarizes the generated finite semantic lab track.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class GeneratedSemanticLabArtifact:
    """
    One artifact from the generated semantic lab track.
    """

    name: str
    path: str
    contribution: str
    verification: str
    limitation: str

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Verification: {self.verification}"
        )


@dataclass(frozen=True)
class GeneratedSemanticLabCompletionReport:
    """
    Completion report for the generated finite semantic lab.
    """

    title: str
    artifacts: Tuple[GeneratedSemanticLabArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def generated_artifacts(self) -> Tuple[GeneratedSemanticLabArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "generated" in artifact.name.lower()
            or "generated" in artifact.contribution.lower()
        )

    def semantic_lab_artifacts(self) -> Tuple[GeneratedSemanticLabArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "semantic lab" in artifact.name.lower()
            or "semantic lab" in artifact.contribution.lower()
        )

    def verified_artifacts(self) -> Tuple[GeneratedSemanticLabArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "Mathlib" in artifact.verification
            or "Lake" in artifact.verification
            or "formal-stack" in artifact.verification
            or "pytest" in artifact.verification
        )

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Generated artifacts: {len(self.generated_artifacts())}\n"
            f"Semantic lab artifacts: {len(self.semantic_lab_artifacts())}\n"
            f"Verified artifacts: {len(self.verified_artifacts())}"
        )


class GeneratedSemanticLabCompletionReportBuilder:
    """
    Builds the generated semantic lab completion report.
    """

    def build(self) -> GeneratedSemanticLabCompletionReport:
        artifacts = (
            GeneratedSemanticLabArtifact(
                name="Generated semantic lab blueprint",
                path="docs/generated_semantic_lab_blueprint.md",
                contribution="Plans the finite semantic lab: multiple systems, morphisms, quotient wrappers, and composition chains.",
                verification="pytest documentation tests",
                limitation="Planning artifact only.",
            ),
            GeneratedSemanticLabArtifact(
                name="Generated semantic lab data model",
                path="src/rigor/generated_semantic_lab_model.py",
                contribution="Defines Python data structures for finite semantic lab systems, morphisms, and composable chains.",
                verification="pytest",
                limitation="Data model only; export handled separately.",
            ),
            GeneratedSemanticLabArtifact(
                name="Generated semantic lab model documentation",
                path="docs/generated_semantic_lab_model.md",
                contribution="Documents the standard generated semantic lab with two-, three-, and four-system chains.",
                verification="pytest documentation tests",
                limitation="Documentation only.",
            ),
            GeneratedSemanticLabArtifact(
                name="Semantic lab Mathlib exporter",
                path="src/rigor/semantic_lab_mathlib_exporter.py",
                contribution="Exports the standard semantic lab into the experimental Mathlib quotient-category track.",
                verification="pytest plus Mathlib Lake build",
                limitation="Exports the standard lab only.",
            ),
            GeneratedSemanticLabArtifact(
                name="Generated SemanticLab Lean artifact",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean",
                contribution="Generated Mathlib file containing four finite systems, three morphisms, quotient wrappers, and two quotient-composition theorems.",
                verification="Mathlib Lake build",
                limitation="Finite prototype-level semantic lab.",
            ),
            GeneratedSemanticLabArtifact(
                name="Semantic lab exporter documentation",
                path="docs/semantic_lab_mathlib_exporter.md",
                contribution="Documents the generated SemanticLab.lean artifact and its main quotient-composition theorems.",
                verification="pytest documentation tests",
                limitation="Documentation only.",
            ),
            GeneratedSemanticLabArtifact(
                name="Generated Mathlib checker integration",
                path="scripts/check_generated_mathlib_exports.sh",
                contribution="Regenerates the semantic lab Mathlib artifact and imports it into the generated Mathlib index.",
                verification="Mathlib Lake build",
                limitation="Depends on local Lean, Lake, elan, and Python setup.",
            ),
            GeneratedSemanticLabArtifact(
                name="Generated Mathlib index",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean",
                contribution="Imports the generated semantic lab alongside earlier generated Mathlib artifacts.",
                verification="Mathlib Lake build and formal-stack gate",
                limitation="Static generated index.",
            ),
            GeneratedSemanticLabArtifact(
                name="Formal-stack semantic lab verification",
                path="scripts/check_formal_stack.sh",
                contribution="Verifies the generated semantic lab through the generated Mathlib checker in the formal-stack gate.",
                verification="formal-stack verification",
                limitation="Network may be required if Mathlib dependencies are not cached.",
            ),
        )

        return GeneratedSemanticLabCompletionReport(
            title="Project Aleph-Omega Generated Semantic Lab Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: GeneratedSemanticLabCompletionReport) -> str:
        lines = [
            "# Project Aleph-Omega Generated Semantic Lab Completion Report",
            "",
            "## Purpose",
            "",
            "This report summarizes Phase 34 so far: the generated finite semantic lab.",
            "",
            "The project now has a Python-defined semantic lab and a generated Mathlib artifact containing multiple systems, morphisms, quotient wrappers, and quotient-composition theorems.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {report.artifact_count()}",
            f"- Generated artifacts: {len(report.generated_artifacts())}",
            f"- Semantic lab artifacts: {len(report.semantic_lab_artifacts())}",
            f"- Verified artifacts: {len(report.verified_artifacts())}",
            "",
            "## Artifacts",
            "",
        ]

        for index, artifact in enumerate(report.artifacts, start=1):
            lines.extend(
                [
                    f"### {index}. {artifact.name}",
                    "",
                    f"- Path: `{artifact.path}`",
                    f"- Verification: {artifact.verification}",
                    "",
                    f"Contribution: {artifact.contribution}",
                    "",
                    f"Limitation: {artifact.limitation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Current Claim",
                "",
                "> Project Aleph-Omega now has a generated finite semantic lab: Python defines multiple finite systems, preservation morphisms, and composable chains, then exports them into a generated Mathlib artifact with quotient wrappers and quotient-category composition theorems.",
                "",
                "## Why This Matters",
                "",
                "The generated pipeline has moved beyond a single tiny example.",
                "",
                "It now produces a small finite semantic laboratory that can be regenerated, inspected, imported into the Mathlib track, and verified.",
                "",
                "This turns the project into a reproducible experimental environment for finite semantic-preservation diagrams.",
                "",
                "## Boundary",
                "",
                "This remains finite and prototype-level.",
                "",
                "The semantic lab is not yet a general theorem generator for arbitrary finite diagrams, arbitrary institution morphisms, or non-finite systems.",
                "",
                "## Next Serious Step",
                "",
                "The next phase should add a semantic lab artifact index that lists each generated system, morphism, quotient wrapper, and composition theorem in the lab.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: GeneratedSemanticLabCompletionReport,
        path: str = "docs/generated_semantic_lab_completion_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = GeneratedSemanticLabCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote generated semantic lab completion report to {output_path}")
