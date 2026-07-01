"""
Python-to-Lean export completion report for Project Aleph-Omega.

This module summarizes the Python-to-Lean finite export track.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LeanExportArtifact:
    """
    One artifact from the Python-to-Lean export track.
    """

    name: str
    path: str
    contribution: str
    verification: str
    limitation: str

    def describe(self) -> str:
        return (
            f"LeanExportArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Verification: {self.verification}"
        )


@dataclass(frozen=True)
class LeanExportCompletionReport:
    """
    Completion report for the Python-to-Lean export track.
    """

    title: str
    artifacts: Tuple[LeanExportArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def lean_verified_artifacts(self) -> Tuple[LeanExportArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "Lean" in artifact.verification
            or "formal-stack" in artifact.verification
        )

    def exporter_artifacts(self) -> Tuple[LeanExportArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if "exporter" in artifact.name.lower()
            or "exporter" in artifact.contribution.lower()
        )

    def describe(self) -> str:
        return (
            f"LeanExportCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Lean-verified artifacts: {len(self.lean_verified_artifacts())}\n"
            f"Exporter artifacts: {len(self.exporter_artifacts())}"
        )


class LeanExportCompletionReportBuilder:
    """
    Builds the Python-to-Lean export completion report.
    """

    def build(self) -> LeanExportCompletionReport:
        artifacts = (
            LeanExportArtifact(
                name="Lean export blueprint",
                path="docs/lean_export_blueprint.md",
                contribution="Defines the technical plan for exporting finite Python semantic systems into Lean.",
                verification="Documentation and tests",
                limitation="Blueprint only.",
            ),
            LeanExportArtifact(
                name="Finite system exporter",
                path="src/rigor/lean_finite_system_exporter.py",
                contribution="Generates Lean finite formal systems from Python data.",
                verification="pytest plus Lean check of generated system file",
                limitation="Handles finite systems only.",
            ),
            LeanExportArtifact(
                name="Generated finite system",
                path="formal/generated/ExportedTinySystem.lean",
                contribution="Machine-generated Lean finite system with satisfaction facts.",
                verification="Lean checked by lean formal/generated/ExportedTinySystem.lean",
                limitation="Tiny example system.",
            ),
            LeanExportArtifact(
                name="Preservation morphism exporter",
                path="src/rigor/lean_morphism_exporter.py",
                contribution="Generates Lean source/target systems, translations, model maps, and preservation morphisms.",
                verification="pytest plus Lean check of generated morphism file",
                limitation="Requires total finite maps and total finite translations.",
            ),
            LeanExportArtifact(
                name="Generated preservation morphism",
                path="formal/generated/ExportedTinyMorphism.lean",
                contribution="Machine-generated Lean satisfaction-preserving morphism.",
                verification="Lean checked by lean formal/generated/ExportedTinyMorphism.lean",
                limitation="Tiny example morphism.",
            ),
            LeanExportArtifact(
                name="Generated Lean export checker",
                path="scripts/check_generated_lean_exports.sh",
                contribution="Regenerates generated Lean files and verifies them with Lean.",
                verification="Lean export verification script",
                limitation="Checks current generated examples only.",
            ),
            LeanExportArtifact(
                name="Formal stack integration",
                path="scripts/check_formal_stack.sh",
                contribution="Runs generated Lean export verification inside the main formal-stack gate.",
                verification="formal-stack verification",
                limitation="Depends on local Lean and elan setup.",
            ),
            LeanExportArtifact(
                name="Export verification documentation",
                path="docs/generated_lean_export_verification.md",
                contribution="Documents generated Lean export verification and formal-stack integration.",
                verification="Documentation and tests",
                limitation="Documentation only.",
            ),
        )

        return LeanExportCompletionReport(
            title="Project Aleph-Omega Python-to-Lean Export Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: LeanExportCompletionReport) -> str:
        lines = [
            "# Project Aleph-Omega Python-to-Lean Export Completion Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the Python-to-Lean finite export track.",
            "",
            "The project now generates Lean formal artifacts from Python finite semantic data and verifies those artifacts with Lean.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {report.artifact_count()}",
            f"- Lean-verified artifacts: {len(report.lean_verified_artifacts())}",
            f"- Exporter artifacts: {len(report.exporter_artifacts())}",
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
                "> Project Aleph-Omega now has a Python-to-Lean export pipeline that generates finite Lean formal systems and finite satisfaction-preserving morphisms from Python data, then verifies the generated Lean artifacts inside the formal-stack gate.",
                "",
                "## Why This Matters",
                "",
                "This changes the Python layer from a parallel implementation into a producer of machine-checkable formal artifacts.",
                "",
                "The project now has a reproducible bridge from executable finite semantics to Lean verification.",
                "",
                "## Boundary",
                "",
                "The exporter currently handles finite systems and total finite preservation morphisms.",
                "",
                "It does not yet export quotient-category Mathlib objects, arbitrary partial bridges, or large generated libraries.",
                "",
                "## Next Serious Step",
                "",
                "The next phase should add generated preservation-morphism examples into the experimental Mathlib project, not only standalone generated Lean files.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: LeanExportCompletionReport,
        path: str = "docs/lean_export_completion_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = LeanExportCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote Lean export completion report to {output_path}")
