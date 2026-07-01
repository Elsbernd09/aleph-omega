"""
Public release documentation index for Project Aleph-Omega.

This module generates a reviewer-facing index of the most important public
release artifacts.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class PublicReleaseDocument:
    """
    One public release document.
    """

    title: str
    path: str
    audience: str
    purpose: str
    status: str

    def describe(self) -> str:
        """
        Returns a readable document summary.
        """

        return (
            f"PublicReleaseDocument\n"
            f"Title: {self.title}\n"
            f"Path: {self.path}\n"
            f"Audience: {self.audience}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class PublicReleaseIndex:
    """
    Public release documentation index.
    """

    title: str
    documents: Tuple[PublicReleaseDocument, ...]

    def document_count(self) -> int:
        """
        Counts indexed documents.
        """

        return len(self.documents)

    def completed_documents(self) -> Tuple[PublicReleaseDocument, ...]:
        """
        Returns completed documents.
        """

        return tuple(document for document in self.documents if document.status == "complete")

    def describe(self) -> str:
        """
        Returns a readable index summary.
        """

        return (
            f"PublicReleaseIndex\n"
            f"Title: {self.title}\n"
            f"Documents: {self.document_count()}\n"
            f"Completed documents: {len(self.completed_documents())}"
        )


class PublicReleaseIndexBuilder:
    """
    Builds the public release documentation index.
    """

    def build(self) -> PublicReleaseIndex:
        """
        Builds the standard public release index.
        """

        documents = (
            PublicReleaseDocument(
                title="Public README",
                path="README.md",
                audience="general reviewers",
                purpose="Gives the clean public overview of the project, its claims, limitations, and run commands.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="README Archive",
                path="README_ARCHIVE.md",
                audience="development-history reviewers",
                purpose="Preserves the phase-by-phase development README before the public rewrite.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Academic Manuscript",
                path="docs/project_aleph_omega_manuscript.md",
                audience="technical reviewers",
                purpose="Explains the finite semantic framework, Lean core, quotient structure, examples, limitations, and future work.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Theorem and Claim Inventory",
                path="docs/manuscript_theorem_inventory.md",
                audience="mathematical reviewers",
                purpose="Separates definitions, Lean-checked theorems, Python-tested results, examples, and non-claims.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Manuscript Figures",
                path="docs/manuscript_figures.md",
                audience="visual reviewers",
                purpose="Provides architecture diagrams, theorem-flow diagrams, concrete-chain diagrams, and claim-boundary diagrams.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Manuscript Front Matter",
                path="docs/manuscript_front_matter.md",
                audience="submission reviewers",
                purpose="Contains the short abstract, extended abstract, keywords, contribution list, reviewer summary, and submission note.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Formal Claim Upgrade Log",
                path="docs/formal_claim_upgrade.md",
                audience="claim-boundary reviewers",
                purpose="Tracks the strongest careful claims and limitations after each formalization phase.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Lean Formalization Index",
                path="docs/lean_formalization_index.md",
                audience="Lean reviewers",
                purpose="Indexes the key Lean definitions and theorem artifacts.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Concrete Lean Completion Report",
                path="docs/concrete_lean_completion_report.md",
                audience="formal-methods reviewers",
                purpose="Summarizes the concrete finite Lean systems, nontrivial morphisms, preservation chain, and quotient integration.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Lean Packaging Completion Report",
                path="docs/lean_packaging_completion_report.md",
                audience="reproducibility reviewers",
                purpose="Explains the Lake project, sync guard, formal-stack build gate, and GitHub Actions CI.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Correspondence Completion Report",
                path="docs/correspondence_completion_report.md",
                audience="implementation reviewers",
                purpose="Explains how the Python computational layer corresponds to the Lean formal layer.",
                status="complete",
            ),
            PublicReleaseDocument(
                title="Public Release README Notes",
                path="docs/public_release_readme_notes.md",
                audience="public-release reviewers",
                purpose="Explains the public README rewrite and its claim boundaries.",
                status="complete",
            ),
        )

        return PublicReleaseIndex(
            title="Project Aleph-Omega Public Release Documentation Index",
            documents=documents,
        )

    def to_markdown(self, index: PublicReleaseIndex) -> str:
        """
        Converts the index to markdown.
        """

        lines = [
            "# Project Aleph-Omega Public Release Documentation Index",
            "",
            "## Purpose",
            "",
            "This document is the reviewer-facing map of the Project Aleph-Omega documentation package.",
            "",
            "It tells readers where to start depending on what they want to evaluate.",
            "",
            "## Quick Start",
            "",
            "- Start with `README.md` for the public overview.",
            "- Read `docs/project_aleph_omega_manuscript.md` for the full research-style explanation.",
            "- Read `docs/manuscript_theorem_inventory.md` for exact claims and theorem status.",
            "- Run `./scripts/check_formal_stack.sh` to verify the Lean, Lake, and Python stack locally.",
            "",
            "## Summary",
            "",
            f"- Documents indexed: {index.document_count()}",
            f"- Completed documents: {len(index.completed_documents())}",
            "",
            "## Documentation Map",
            "",
        ]

        for number, document in enumerate(index.documents, start=1):
            lines.extend(
                [
                    f"### {number}. {document.title}",
                    "",
                    f"- Path: `{document.path}`",
                    f"- Audience: {document.audience}",
                    f"- Status: {document.status}",
                    "",
                    f"Purpose: {document.purpose}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Suggested Reviewer Path",
                "",
                "A serious reviewer should read documents in this order:",
                "",
                "1. `README.md`",
                "2. `docs/manuscript_front_matter.md`",
                "3. `docs/project_aleph_omega_manuscript.md`",
                "4. `docs/manuscript_theorem_inventory.md`",
                "5. `docs/lean_formalization_index.md`",
                "6. `docs/lean_packaging_completion_report.md`",
                "",
                "Then run:",
                "",
                "```bash",
                "./scripts/check_formal_stack.sh",
                "```",
                "",
                "## Claim Boundary",
                "",
                "The public release should describe Project Aleph-Omega as a finite institution-inspired, Lean-supported research framework.",
                "",
                "It should not describe the project as a universal theory of institutions, a solved open problem, a full Mathlib Category instance, or a field-changing theorem.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        index: PublicReleaseIndex,
        path: str = "docs/public_release_index.md",
    ) -> Path:
        """
        Writes the public release index to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(index))
        return output_path


if __name__ == "__main__":
    builder = PublicReleaseIndexBuilder()
    index = builder.build()
    output_path = builder.write_markdown(index)

    print(index.describe())
    print(f"Wrote public release index to {output_path}")
