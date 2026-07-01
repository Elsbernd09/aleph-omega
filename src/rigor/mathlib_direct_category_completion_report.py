"""
Mathlib direct category completion report for Project Aleph-Omega.

This module summarizes the Mathlib direct-category milestone: a real Mathlib
Category instance for formal systems and satisfaction-preserving morphisms.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class MathlibDirectCategoryArtifact:
    """
    One artifact from the Mathlib direct-category milestone.
    """

    name: str
    path: str
    role: str
    status: str
    limitation: str

    def describe(self) -> str:
        return (
            f"MathlibDirectCategoryArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class MathlibDirectCategoryCompletionReport:
    """
    Completion report for the Mathlib direct category layer.
    """

    title: str
    artifacts: Tuple[MathlibDirectCategoryArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def completed_artifacts(self) -> Tuple[MathlibDirectCategoryArtifact, ...]:
        return tuple(
            artifact
            for artifact in self.artifacts
            if artifact.status == "complete"
            or "Mathlib-checked" in artifact.status
            or "Mathlib-defined" in artifact.status
        )

    def mathlib_checked_artifacts(self) -> Tuple[MathlibDirectCategoryArtifact, ...]:
        return tuple(artifact for artifact in self.artifacts if "Mathlib" in artifact.status)

    def describe(self) -> str:
        return (
            f"MathlibDirectCategoryCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Completed artifacts: {len(self.completed_artifacts())}\n"
            f"Mathlib artifacts: {len(self.mathlib_checked_artifacts())}"
        )


class MathlibDirectCategoryCompletionReportBuilder:
    """
    Builds the Mathlib direct category completion report.
    """

    def build(self) -> MathlibDirectCategoryCompletionReport:
        artifacts = (
            MathlibDirectCategoryArtifact(
                name="Experimental Mathlib scaffold",
                path="formal/aleph_omega_mathlib/",
                role="Separate Lake project for Mathlib integration experiments.",
                status="complete",
                limitation="Separate from the primary verified Lean stack.",
            ),
            MathlibDirectCategoryArtifact(
                name="Mathlib category smoke instance",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean",
                role="Confirms the project can define and build a real Mathlib Category instance.",
                status="Mathlib-checked",
                limitation="Toy smoke-test category, not the main Aleph-Omega category.",
            ),
            MathlibDirectCategoryArtifact(
                name="FormalSystem",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean",
                role="Defines formal systems as objects for the Mathlib direct category.",
                status="Mathlib-defined",
                limitation="Separate definition from the original standalone Lean core.",
            ),
            MathlibDirectCategoryArtifact(
                name="PreservationMorphism",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean",
                role="Defines satisfaction-preserving morphisms as arrows.",
                status="Mathlib-defined",
                limitation="Direct morphisms only; quotient morphisms are not included yet.",
            ),
            MathlibDirectCategoryArtifact(
                name="formalSystemCategory",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean",
                role="Real Mathlib Category instance for formal systems and preservation morphisms.",
                status="Mathlib-checked",
                limitation="This is not yet the quotient category instance.",
            ),
            MathlibDirectCategoryArtifact(
                name="Boolean formal-system examples",
                path="formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean",
                role="Concrete examples showing identity morphisms preserve Boolean satisfaction.",
                status="Mathlib-checked",
                limitation="Small finite examples only.",
            ),
            MathlibDirectCategoryArtifact(
                name="Mathlib scaffold checker",
                path="scripts/check_mathlib_scaffold.sh",
                role="Builds the experimental Mathlib project.",
                status="complete",
                limitation="Mathlib builds can be slower and more version-sensitive than the primary stack.",
            ),
            MathlibDirectCategoryArtifact(
                name="Direct category documentation",
                path="docs/mathlib_formal_system_category.md",
                role="Explains the formal-system Mathlib category and its boundary.",
                status="complete",
                limitation="Documentation is not a proof; the proof artifact is the Lean file.",
            ),
        )

        return MathlibDirectCategoryCompletionReport(
            title="Project Aleph-Omega Mathlib Direct Category Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: MathlibDirectCategoryCompletionReport) -> str:
        lines = [
            "# Project Aleph-Omega Mathlib Direct Category Completion Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the first serious Mathlib category-theory milestone in Project Aleph-Omega.",
            "",
            "The project now has an experimental Mathlib Lake project containing a real Mathlib Category instance for formal systems and satisfaction-preserving morphisms.",
            "",
            "## Summary",
            "",
            f"- Artifacts indexed: {report.artifact_count()}",
            f"- Completed artifacts: {len(report.completed_artifacts())}",
            f"- Mathlib-checked or Mathlib-defined artifacts: {len(report.mathlib_checked_artifacts())}",
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
                    f"- Status: {artifact.status}",
                    "",
                    f"Role: {artifact.role}",
                    "",
                    f"Limitation: {artifact.limitation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Current Mathlib Claim",
                "",
                "> Project Aleph-Omega now contains an experimental Mathlib project with a real Category instance whose objects are formal systems and whose morphisms are satisfaction-preserving morphisms.",
                "",
                "## Why This Is a PhD-Level Upgrade",
                "",
                "This moves the project beyond a custom category-like Lean structure and into actual Mathlib category-theory infrastructure.",
                "",
                "It demonstrates that the central semantic-preservation structure can be expressed as a real Mathlib Category.",
                "",
                "## Important Boundary",
                "",
                "This is the direct preservation-morphism category, not yet the quotient category.",
                "",
                "The quotient category remains harder because it requires quotient morphisms, representative independence, quotient induction, and proof-shape compatibility with Mathlib.",
                "",
                "## Next Step",
                "",
                "The next serious phase is to analyze whether the quotient morphism layer can be lifted into a real Mathlib Category instance.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: MathlibDirectCategoryCompletionReport,
        path: str = "docs/mathlib_direct_category_completion_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = MathlibDirectCategoryCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote Mathlib direct category completion report to {output_path}")
