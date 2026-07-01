"""
Manuscript completion report for Project Aleph-Omega.

This module summarizes Phase 26, the research manuscript layer.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ManuscriptArtifact:
    """
    One manuscript-layer artifact.
    """

    name: str
    path: str
    purpose: str
    status: str

    def describe(self) -> str:
        """
        Returns a readable artifact summary.
        """

        return (
            f"ManuscriptArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class ManuscriptCompletionReport:
    """
    Completion report for the manuscript layer.
    """

    title: str
    artifacts: Tuple[ManuscriptArtifact, ...]

    def artifact_count(self) -> int:
        """
        Counts manuscript artifacts.
        """

        return len(self.artifacts)

    def completed_artifacts(self) -> Tuple[ManuscriptArtifact, ...]:
        """
        Returns completed artifacts.
        """

        return tuple(artifact for artifact in self.artifacts if artifact.status == "complete")

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"ManuscriptCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Completed artifacts: {len(self.completed_artifacts())}"
        )


class ManuscriptCompletionReportBuilder:
    """
    Builds the Phase 26 manuscript completion report.
    """

    def build(self) -> ManuscriptCompletionReport:
        """
        Builds the standard completion report.
        """

        artifacts = (
            ManuscriptArtifact(
                name="Academic manuscript draft",
                path="docs/project_aleph_omega_manuscript.md",
                purpose=(
                    "Provides the central paper-style explanation of the project, including "
                    "motivation, finite semantics, Lean formal core, quotient-category structure, "
                    "concrete examples, correspondence layer, limitations, and future work."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Theorem and claim inventory",
                path="docs/manuscript_theorem_inventory.md",
                purpose=(
                    "Separates definitions, Lean-checked theorems, Python-tested results, examples, "
                    "and explicit non-claims."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Manuscript figures",
                path="docs/manuscript_figures.md",
                purpose=(
                    "Provides Markdown-readable architecture diagrams, theorem-flow diagrams, "
                    "concrete-chain diagrams, quotient-category diagrams, and claim-boundary diagrams."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Front matter and submission package",
                path="docs/manuscript_front_matter.md",
                purpose=(
                    "Provides short abstract, extended abstract, keywords, contribution list, reviewer "
                    "summary, and submission framing note."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Formal claim upgrade log",
                path="docs/formal_claim_upgrade.md",
                purpose=(
                    "Records the strongest careful claims and limitations after each formalization phase."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Lean formalization index",
                path="docs/lean_formalization_index.md",
                purpose=(
                    "Indexes machine-checked Lean definitions and theorems."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Correspondence completion report",
                path="docs/correspondence_completion_report.md",
                purpose=(
                    "Explains the relationship between the Lean formal core and Python computational analogues."
                ),
                status="complete",
            ),
            ManuscriptArtifact(
                name="Concrete Lean completion report",
                path="docs/concrete_lean_completion_report.md",
                purpose=(
                    "Summarizes concrete finite Lean systems, nontrivial morphisms, preservation chains, "
                    "and quotient-category integration."
                ),
                status="complete",
            ),
        )

        return ManuscriptCompletionReport(
            title="Project Aleph-Omega Manuscript Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: ManuscriptCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Project Aleph-Omega Manuscript Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 26 completes the first research manuscript layer for Project Aleph-Omega.",
            "",
            "The manuscript package turns the repository into a reviewer-readable research artifact.",
            "",
            "## Summary",
            "",
            f"- Manuscript artifacts indexed: {report.artifact_count()}",
            f"- Completed artifacts: {len(report.completed_artifacts())}",
            "",
            "## Manuscript Artifacts",
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
                ]
            )

        lines.extend(
            [
                "## Strongest Current Manuscript Claim",
                "",
                "> Project Aleph-Omega is a finite institution-inspired, Lean-supported research framework for studying satisfaction preservation under semantic translation. It contains a Python computational layer, a Lean-checked abstract quotient-category core, concrete finite Lean examples, a Lean/Python correspondence layer, and a manuscript package that separates formal claims from computational analogues and non-claims.",
                "",
                "## Public Framing",
                "",
                "The project should be framed as:",
                "",
                "- a formal-methods research artifact",
                "- a finite semantics laboratory",
                "- a Lean-supported quotient-category prototype",
                "- a serious mathematical-computation project",
                "",
                "The project should not be framed as:",
                "",
                "- a solved open problem",
                "- a universal theory of institutions",
                "- a full Mathlib category instance",
                "- a complete verification of the Python implementation",
                "- a Gauss-level or field-changing theorem",
                "",
                "## Next Serious Milestones",
                "",
                "The next possible milestones are:",
                "",
                "1. build a Lake/Mathlib project and attempt a real Category instance,",
                "2. create a Python-to-Lean finite model exporter,",
                "3. polish the manuscript into a PDF-style research paper,",
                "4. add citations and a literature-review layer,",
                "5. prepare a GitHub release and LinkedIn/public summary.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: ManuscriptCompletionReport,
        path: str = "docs/manuscript_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = ManuscriptCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote manuscript completion report to {output_path}")
