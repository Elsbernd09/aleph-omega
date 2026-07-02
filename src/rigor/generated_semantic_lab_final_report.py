"""
Generated semantic lab final completion report for Project Aleph-Omega.

This module closes Phase 34 by summarizing the generated finite semantic lab.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class GeneratedSemanticLabFinalArtifact:
    """
    One final artifact from the generated semantic lab track.
    """

    name: str
    path: str
    contribution: str
    verification: str
    limitation: str

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabFinalArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Verification: {self.verification}"
        )


@dataclass(frozen=True)
class GeneratedSemanticLabFinalReport:
    """
    Final completion report for the generated finite semantic lab.
    """

    title: str
    artifacts: Tuple[GeneratedSemanticLabFinalArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def semantic_lab_artifacts(self) -> Tuple[GeneratedSemanticLabFinalArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "semantic lab" in artifact.name.lower()
            or "semantic lab" in artifact.contribution.lower()
        )

    def generated_artifacts(self) -> Tuple[GeneratedSemanticLabFinalArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "generated" in artifact.name.lower()
            or "generated" in artifact.contribution.lower()
        )

    def mathlib_artifacts(self) -> Tuple[GeneratedSemanticLabFinalArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "Mathlib" in artifact.path
            or "Mathlib" in artifact.verification
            or "Mathlib" in artifact.contribution
        )

    def verified_artifacts(self) -> Tuple[GeneratedSemanticLabFinalArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "pytest" in artifact.verification
            or "Mathlib" in artifact.verification
            or "Lake" in artifact.verification
            or "formal-stack" in artifact.verification
        )

    def describe(self) -> str:
        return (
            f"GeneratedSemanticLabFinalReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Semantic lab artifacts: {len(self.semantic_lab_artifacts())}\n"
            f"Generated artifacts: {len(self.generated_artifacts())}\n"
            f"Mathlib artifacts: {len(self.mathlib_artifacts())}\n"
            f"Verified artifacts: {len(self.verified_artifacts())}"
        )


class GeneratedSemanticLabFinalReportBuilder:
    """
    Builds the final generated semantic lab report.
    """

    def build(self) -> GeneratedSemanticLabFinalReport:
        artifacts = (
            GeneratedSemanticLabFinalArtifact(
                name="Generated semantic lab blueprint",
                path="docs/generated_semantic_lab_blueprint.md",
                contribution="Defines the plan for a generated finite semantic laboratory.",
                verification="pytest documentation tests",
                limitation="Planning artifact only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated semantic lab data model",
                path="src/rigor/generated_semantic_lab_model.py",
                contribution="Defines Python data structures for finite systems, preservation morphisms, and composable semantic chains.",
                verification="pytest",
                limitation="Finite deterministic lab model only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated semantic lab model documentation",
                path="docs/generated_semantic_lab_model.md",
                contribution="Documents the standard semantic lab containing two-, three-, and four-system chains.",
                verification="pytest documentation tests",
                limitation="Documentation only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Semantic lab Mathlib exporter",
                path="src/rigor/semantic_lab_mathlib_exporter.py",
                contribution="Exports the standard generated semantic lab into the experimental Mathlib quotient-category track.",
                verification="pytest plus Mathlib Lake build when dependencies are available",
                limitation="Exports the standard lab only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated SemanticLab Lean file",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean",
                contribution="Generated Mathlib artifact with four systems, three morphisms, quotient wrappers, and two quotient-category composition theorems.",
                verification="Mathlib Lake build when dependencies are available",
                limitation="Finite prototype-level semantic lab.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Semantic lab exporter documentation",
                path="docs/semantic_lab_mathlib_exporter.md",
                contribution="Documents SemanticLab.lean and its generated quotient-category composition theorems.",
                verification="pytest documentation tests",
                limitation="Documentation only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated semantic lab completion report",
                path="docs/generated_semantic_lab_completion_report.md",
                contribution="Summarizes the generated semantic lab build path and its verification boundaries.",
                verification="pytest documentation tests",
                limitation="Report only.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated semantic lab artifact index",
                path="docs/generated_semantic_lab_artifact_index.md",
                contribution="Indexes systems, morphisms, quotient wrappers, and composition theorems inside the generated semantic lab.",
                verification="pytest documentation tests",
                limitation="Static index of current lab artifacts.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Generated Mathlib checker integration",
                path="scripts/check_generated_mathlib_exports.sh",
                contribution="Regenerates the semantic lab and checks the generated Mathlib library through Lake.",
                verification="Mathlib Lake build when dependencies are available",
                limitation="Network may be required if Mathlib dependencies are not cached.",
            ),
            GeneratedSemanticLabFinalArtifact(
                name="Formal-stack integration",
                path="scripts/check_formal_stack.sh",
                contribution="Runs generated Mathlib export verification inside the official formal-stack gate.",
                verification="formal-stack verification",
                limitation="Depends on local Python, Lean, Lake, elan, and sometimes GitHub access.",
            ),
        )

        return GeneratedSemanticLabFinalReport(
            title="Project Aleph-Omega Generated Semantic Lab Final Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: GeneratedSemanticLabFinalReport) -> str:
        lines = [
            "# Project Aleph-Omega Generated Semantic Lab Final Report",
            "",
            "## Purpose",
            "",
            "This report closes Phase 34: the generated finite semantic lab.",
            "",
            "The project now has a Python-defined semantic laboratory that exports into the experimental Mathlib quotient-category track.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {report.artifact_count()}",
            f"- Semantic lab artifacts: {len(report.semantic_lab_artifacts())}",
            f"- Generated artifacts: {len(report.generated_artifacts())}",
            f"- Mathlib artifacts: {len(report.mathlib_artifacts())}",
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
                "> Project Aleph-Omega now contains a generated finite semantic lab: Python defines multiple finite systems, preservation morphisms, and composable chains, then exports them into the experimental Mathlib quotient-category track with quotient wrappers and quotient-category composition theorems.",
                "",
                "## Why This Matters",
                "",
                "This phase moves the project beyond a single generated example.",
                "",
                "The project now has a small generated semantic laboratory: four systems, three morphisms, quotient morphism classes, and two quotient-category composition theorems.",
                "",
                "This makes the generated pipeline easier to review, regenerate, and extend.",
                "",
                "## Boundary",
                "",
                "This remains finite and prototype-level.",
                "",
                "It is not a general theorem generator for arbitrary semantic diagrams, arbitrary institution morphisms, or non-finite systems.",
                "",
                "Mathlib verification may require working internet access if dependencies are not already cached.",
                "",
                "## Next Serious Step",
                "",
                "The next phase should add semantic lab expansion: multiple named finite diagrams beyond a single chain family.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: GeneratedSemanticLabFinalReport,
        path: str = "docs/generated_semantic_lab_final_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = GeneratedSemanticLabFinalReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote generated semantic lab final report to {output_path}")
