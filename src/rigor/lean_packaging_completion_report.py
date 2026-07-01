"""
Lean packaging completion report for Project Aleph-Omega.

This module summarizes Phase 27, which packages the Lean formalization as a
standalone Lake project and adds formal-stack verification infrastructure.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LeanPackagingArtifact:
    """
    One Lean packaging artifact.
    """

    name: str
    path: str
    purpose: str
    verification_role: str
    status: str

    def describe(self) -> str:
        """
        Returns a readable artifact summary.
        """

        return (
            f"LeanPackagingArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class LeanPackagingCompletionReport:
    """
    Completion report for the Lean packaging layer.
    """

    title: str
    artifacts: Tuple[LeanPackagingArtifact, ...]

    def artifact_count(self) -> int:
        """
        Counts artifacts.
        """

        return len(self.artifacts)

    def completed_artifacts(self) -> Tuple[LeanPackagingArtifact, ...]:
        """
        Returns completed artifacts.
        """

        return tuple(artifact for artifact in self.artifacts if artifact.status == "complete")

    def ci_artifacts(self) -> Tuple[LeanPackagingArtifact, ...]:
        """
        Returns CI-related artifacts.
        """

        return tuple(
            artifact
            for artifact in self.artifacts
            if "CI" in artifact.verification_role or "GitHub Actions" in artifact.name
        )

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"LeanPackagingCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Completed artifacts: {len(self.completed_artifacts())}\n"
            f"CI artifacts: {len(self.ci_artifacts())}"
        )


class LeanPackagingCompletionReportBuilder:
    """
    Builds the Phase 27 Lean packaging completion report.
    """

    def build(self) -> LeanPackagingCompletionReport:
        """
        Builds the standard report.
        """

        artifacts = (
            LeanPackagingArtifact(
                name="Primary Lean core",
                path="formal/lean/AlephOmegaCore.lean",
                purpose=(
                    "Stores the primary Lean formalization containing FormalSystem, "
                    "PreservationMorphism, morphism equivalence, quotient morphisms, "
                    "the standalone quotient-category structure, and concrete finite examples."
                ),
                verification_role="Primary machine-checked formalization file.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Lake project scaffold",
                path="formal/aleph_omega_lake/",
                purpose=(
                    "Packages the Lean core as a standalone Lake project with a lean_lib entry point."
                ),
                verification_role="Allows the formal core to build as a Lean project rather than only as one file.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Lake sync script",
                path="scripts/sync_lake_core.sh",
                purpose="Copies the primary Lean core into the Lake project location.",
                verification_role="Prevents manual copy errors before Lake builds.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Lake sync checker",
                path="scripts/check_lake_sync.sh",
                purpose="Checks that the primary Lean core and Lake-project copy are identical.",
                verification_role="Guards against stale Lean code in the Lake project.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Lake build checker",
                path="scripts/check_lake.sh",
                purpose="Checks synchronization and builds the standalone Lake project.",
                verification_role="Verifies the Lake-packaged formalization builds successfully.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Unified formal stack checker",
                path="scripts/check_formal_stack.sh",
                purpose=(
                    "Runs the primary Lean check, Lake synchronization check, Lake build, and Python tests."
                ),
                verification_role="One-command verification gate for the full formal stack.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="GitHub Actions formal CI",
                path=".github/workflows/formal-stack.yml",
                purpose="Runs the formal stack verification automatically on pushes and pull requests.",
                verification_role="CI verification for Lean, Lake, synchronization, and Python tests.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="Formal stack build gate documentation",
                path="docs/formal_stack_build_gate.md",
                purpose="Explains the unified formal verification command.",
                verification_role="Reviewer-facing documentation for reproducing formal checks.",
                status="complete",
            ),
            LeanPackagingArtifact(
                name="GitHub Actions CI documentation",
                path="docs/github_actions_formal_ci.md",
                purpose="Explains the GitHub Actions formal-stack workflow.",
                verification_role="Reviewer-facing documentation for continuous integration.",
                status="complete",
            ),
        )

        return LeanPackagingCompletionReport(
            title="Project Aleph-Omega Lean Packaging Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: LeanPackagingCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Project Aleph-Omega Lean Packaging Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 27 packages the Project Aleph-Omega Lean formalization into a more serious formal-verification workflow.",
            "",
            "The phase adds a Lake project scaffold, synchronization guard, unified formal-stack build gate, and GitHub Actions continuous integration.",
            "",
            "## Summary",
            "",
            f"- Packaging artifacts indexed: {report.artifact_count()}",
            f"- Completed artifacts: {len(report.completed_artifacts())}",
            f"- CI-related artifacts: {len(report.ci_artifacts())}",
            "",
            "## Packaging Artifacts",
            "",
        ]

        for index, artifact in enumerate(report.artifacts, start=1):
            lines.extend(
                [
                    f"### {index}. {artifact.name}",
                    "",
                    f"- Path: `{artifact.path}`",
                    f"- Status: {artifact.status}",
                    "",
                    f"Purpose: {artifact.purpose}",
                    "",
                    f"Verification role: {artifact.verification_role}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Current Packaging Claim",
                "",
                "> Project Aleph-Omega now packages its Lean formal core as a standalone Lake project and provides a unified formal-stack verification gate covering the primary Lean file, Lake synchronization, Lake build, and Python computational tests, with GitHub Actions continuous integration for pushed versions of the repository.",
                "",
                "## Important Limitation",
                "",
                "This is still not a Mathlib Category instance.",
                "",
                "The Lake project currently packages the existing standalone Lean formalization. Future work can integrate Mathlib and attempt a true Category typeclass instance.",
                "",
                "## Reviewer Command",
                "",
                "A reviewer can run:",
                "",
                "```bash",
                "./scripts/check_formal_stack.sh",
                "```",
                "",
                "This verifies the primary Lean formalization, Lake synchronization, Lake build, and Python test suite.",
                "",
                "## Next Serious Milestones",
                "",
                "The next possible milestones are:",
                "",
                "1. Mathlib integration planning,",
                "2. a real category-instance feasibility layer,",
                "3. Python-to-Lean finite model export,",
                "4. a polished GitHub release package,",
                "5. public-facing README cleanup.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: LeanPackagingCompletionReport,
        path: str = "docs/lean_packaging_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = LeanPackagingCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote Lean packaging completion report to {output_path}")
