"""
Non-rfl diamond theorem completion report for Project Aleph-Omega.

This module summarizes the generated diamond diagram theorem-backed upgrade.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class NontrivialDiamondTheoremArtifact:
    """
    One artifact from the non-rfl diamond theorem track.
    """

    name: str
    path: str
    contribution: str
    proof_character: str
    limitation: str

    def describe(self) -> str:
        return (
            f"NontrivialDiamondTheoremArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Proof character: {self.proof_character}"
        )


@dataclass(frozen=True)
class NontrivialDiamondTheoremCompletionReport:
    """
    Completion report for the non-rfl generated diamond theorem track.
    """

    title: str
    artifacts: Tuple[NontrivialDiamondTheoremArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def theorem_artifacts(self) -> Tuple[NontrivialDiamondTheoremArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "theorem" in artifact.name.lower()
            or "theorem" in artifact.contribution.lower()
        )

    def non_rfl_artifacts(self) -> Tuple[NontrivialDiamondTheoremArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "Quotient.sound" in artifact.proof_character
            or "pointwise" in artifact.proof_character.lower()
            or "not bare rfl" in artifact.proof_character.lower()
        )

    def generated_artifacts(self) -> Tuple[NontrivialDiamondTheoremArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "generated" in artifact.name.lower()
            or "generated" in artifact.contribution.lower()
        )

    def describe(self) -> str:
        return (
            f"NontrivialDiamondTheoremCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Theorem artifacts: {len(self.theorem_artifacts())}\n"
            f"Non-rfl artifacts: {len(self.non_rfl_artifacts())}\n"
            f"Generated artifacts: {len(self.generated_artifacts())}"
        )


class NontrivialDiamondTheoremCompletionReportBuilder:
    """
    Builds the non-rfl diamond theorem completion report.
    """

    def build(self) -> NontrivialDiamondTheoremCompletionReport:
        artifacts = (
            NontrivialDiamondTheoremArtifact(
                name="Nontrivial quotient path equivalence blueprint",
                path="docs/nontrivial_quotient_path_equivalence_blueprint.md",
                contribution="Defines the theorem plan for proving quotient path equality by pointwise equivalence.",
                proof_character="Blueprint for non-rfl theorem track.",
                limitation="Planning artifact only.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Generated diamond diagram data model",
                path="src/rigor/generated_diamond_diagram_model.py",
                contribution="Defines a finite diamond diagram with two distinct source-to-target paths that agree pointwise.",
                proof_character="Python-level path agreement validation.",
                limitation="Finite two-point systems.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Generated diamond diagram documentation",
                path="docs/generated_diamond_diagram_model.md",
                contribution="Documents the diamond diagram and its pointwise path agreement.",
                proof_character="Documentation of theorem setup.",
                limitation="Documentation only.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Diamond diagram Mathlib exporter",
                path="src/rigor/diamond_diagram_mathlib_exporter.py",
                contribution="Generates the diamond diagram Lean artifact with path-equivalence theorems.",
                proof_character="Generates pointwise equivalence and Quotient.sound proof structure.",
                limitation="Exports the standard diamond only.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Generated DiamondDiagram Lean file",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="Generated Mathlib artifact proving upper and lower diamond paths equal as quotient morphisms.",
                proof_character="Uses PreservationEquivalent and Quotient.sound; not bare rfl.",
                limitation="Finite generated diamond.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Translation equivalence theorem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="Proves upper and lower path sentence translations agree pointwise.",
                proof_character="Pointwise finite proof by cases.",
                limitation="Finite source sentence type.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Model-map equivalence theorem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="Proves upper and lower path model maps agree pointwise.",
                proof_character="Pointwise finite proof by cases.",
                limitation="Finite source model type.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="PreservationEquivalent theorem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="Combines pointwise translation and model-map equality into the quotient equivalence relation.",
                proof_character="Constructs PreservationEquivalent explicitly.",
                limitation="Depends on current quotient equivalence definition.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Quotient path equality theorem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="Proves qDiamondUpperPath equals qDiamondLowerPath.",
                proof_character="Uses Quotient.sound; not bare rfl.",
                limitation="Finite generated diamond.",
            ),
            NontrivialDiamondTheoremArtifact(
                name="Category-level diamond commutativity theorem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean",
                contribution="States diamond path equality using quotient-category arrow objects.",
                proof_character="Uses the quotient equality theorem.",
                limitation="Prototype quotient category theorem.",
            ),
        )

        return NontrivialDiamondTheoremCompletionReport(
            title="Project Aleph-Omega Non-rfl Diamond Theorem Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: NontrivialDiamondTheoremCompletionReport) -> str:
        lines = [
            "# Project Aleph-Omega Non-rfl Diamond Theorem Completion Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the Phase 35 theorem-strengthening milestone.",
            "",
            "Project Aleph-Omega now has a generated finite diamond diagram whose two source-to-target paths are proved equal as quotient morphisms using pointwise equivalence and `Quotient.sound`, rather than bare `rfl`.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {report.artifact_count()}",
            f"- Theorem artifacts: {len(report.theorem_artifacts())}",
            f"- Non-rfl artifacts: {len(report.non_rfl_artifacts())}",
            f"- Generated artifacts: {len(report.generated_artifacts())}",
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
                    f"- Proof character: {artifact.proof_character}",
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
                "> Project Aleph-Omega now contains a generated theorem-backed diamond diagram: two generated source-to-target paths are proved equal as quotient morphisms by pointwise translation equality, pointwise model-map equality, `PreservationEquivalent`, and `Quotient.sound`, rather than by bare definitional equality.",
                "",
                "## Why This Matters",
                "",
                "This is a real upgrade in proof quality.",
                "",
                "Earlier generated examples often relied on definitional equality or direct finite composition.",
                "",
                "The diamond theorem proves equality through the actual quotient equivalence relation.",
                "",
                "That makes the project more credible as a formal-methods research project rather than only a code-generation demo.",
                "",
                "## Boundary",
                "",
                "This is still finite and generated.",
                "",
                "The theorem is not yet a general theorem over arbitrary diagrams or arbitrary finite institutions.",
                "",
                "The next step is to abstract the diamond proof pattern into a reusable theorem schema.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: NontrivialDiamondTheoremCompletionReport,
        path: str = "docs/nontrivial_diamond_theorem_completion_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = NontrivialDiamondTheoremCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote non-rfl diamond theorem completion report to {output_path}")
