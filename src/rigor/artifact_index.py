"""
Artifact index for Project Aleph-Omega.

This module creates an index of important generated artifacts, documentation
files, reports, and research outputs.

The goal is reviewer readiness: make it easy to find the core project outputs.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ArtifactIndexItem:
    """
    One indexed project artifact.
    """

    title: str
    path: str
    category: str
    description: str

    def exists(self) -> bool:
        """
        Returns whether the artifact exists.
        """

        return Path(self.path).exists()

    def describe(self) -> str:
        """
        Returns a readable artifact item.
        """

        return (
            f"ArtifactIndexItem\n"
            f"Title: {self.title}\n"
            f"Path: {self.path}\n"
            f"Category: {self.category}\n"
            f"Exists: {self.exists()}\n"
            f"Description: {self.description}"
        )


@dataclass(frozen=True)
class ArtifactIndex:
    """
    Index of important project artifacts.
    """

    items: Tuple[ArtifactIndexItem, ...]

    def item_count(self) -> int:
        """
        Counts indexed artifacts.
        """

        return len(self.items)

    def existing_items(self) -> Tuple[ArtifactIndexItem, ...]:
        """
        Returns artifacts that exist.
        """

        return tuple(item for item in self.items if item.exists())

    def missing_items(self) -> Tuple[ArtifactIndexItem, ...]:
        """
        Returns artifacts that are missing.
        """

        return tuple(item for item in self.items if not item.exists())

    def by_category(self, category: str) -> Tuple[ArtifactIndexItem, ...]:
        """
        Returns artifacts in a category.
        """

        return tuple(item for item in self.items if item.category == category)

    def categories(self) -> Tuple[str, ...]:
        """
        Returns artifact categories.
        """

        return tuple(sorted({item.category for item in self.items}))

    def complete(self) -> bool:
        """
        Returns whether all indexed artifacts exist.
        """

        return len(self.missing_items()) == 0

    def describe(self) -> str:
        """
        Returns a readable artifact index summary.
        """

        return (
            f"ArtifactIndex\n"
            f"Items: {self.item_count()}\n"
            f"Existing: {len(self.existing_items())}\n"
            f"Missing: {len(self.missing_items())}\n"
            f"Complete: {self.complete()}"
        )


class ArtifactIndexBuilder:
    """
    Builds the standard project artifact index.
    """

    def build(self) -> ArtifactIndex:
        """
        Builds the artifact index.
        """

        items = (
            ArtifactIndexItem(
                title="README",
                path="README.md",
                category="root",
                description="Main repository entry point.",
            ),
            ArtifactIndexItem(
                title="Rigor Track",
                path="docs/rigor_track.md",
                category="overview",
                description="Longitudinal record of the rigor-track phases.",
            ),
            ArtifactIndexItem(
                title="Research Abstract",
                path="docs/research_abstract.md",
                category="research_artifact",
                description="Concise academic-style project abstract.",
            ),
            ArtifactIndexItem(
                title="Theorem Inventory",
                path="docs/theorem_inventory.md",
                category="research_artifact",
                description="Inventory of theorem-like claims, scope, evidence, and limitations.",
            ),
            ArtifactIndexItem(
                title="Architecture Map",
                path="docs/architecture_map.md",
                category="research_artifact",
                description="Layer-by-layer map of the project architecture.",
            ),
            ArtifactIndexItem(
                title="Final Research Memo",
                path="docs/final_research_memo.md",
                category="research_artifact",
                description="Polished research memo summarizing the project.",
            ),
            ArtifactIndexItem(
                title="Model Search Report",
                path="docs/model_search_report.md",
                category="model_search",
                description="Generated report summarizing finite model-search results.",
            ),
            ArtifactIndexItem(
                title="Failure Lab Report",
                path="docs/failure_lab_report.md",
                category="failure_lab",
                description="Generated report summarizing semantic failure cases.",
            ),
            ArtifactIndexItem(
                title="Verification Report",
                path="docs/verification_report.md",
                category="verification",
                description="Generated report summarizing claims, audits, and proof obligations.",
            ),
            ArtifactIndexItem(
                title="Project Health",
                path="docs/project_health.md",
                category="reviewer_readiness",
                description="Documentation for the project health check.",
            ),
            ArtifactIndexItem(
                title="Formal Verification Interface",
                path="docs/formal_verification_interface.md",
                category="verification",
                description="Overview of claim registry, audit records, and proof obligations.",
            ),
            ArtifactIndexItem(
                title="Failure Laboratory",
                path="docs/failure_lab.md",
                category="failure_lab",
                description="Overview of failure taxonomy, extraction, and theorem-boundary analysis.",
            ),
            ArtifactIndexItem(
                title="Finite Model Search",
                path="docs/model_search.md",
                category="model_search",
                description="Overview of generated finite model search and stress testing.",
            ),
            ArtifactIndexItem(
                title="Research Artifacts",
                path="docs/research_artifacts.md",
                category="research_artifact",
                description="Overview of generated research artifact layer.",
            ),
        )

        return ArtifactIndex(items=items)

    def to_markdown(self, index: ArtifactIndex) -> str:
        """
        Converts the artifact index to markdown.
        """

        lines = [
            "# Artifact Index",
            "",
            "## Purpose",
            "",
            "This index lists the most important Project Aleph-Omega artifacts for reviewers.",
            "",
            "It is meant to make the repository easier to navigate.",
            "",
            "## Summary",
            "",
            f"- Indexed artifacts: {index.item_count()}",
            f"- Existing artifacts: {len(index.existing_items())}",
            f"- Missing artifacts: {len(index.missing_items())}",
            f"- Complete: {index.complete()}",
            "",
            "## Artifacts by Category",
            "",
        ]

        for category in index.categories():
            lines.extend(
                [
                    f"### {category}",
                    "",
                ]
            )

            for item in index.by_category(category):
                status = "exists" if item.exists() else "missing"
                lines.extend(
                    [
                        f"- {item.title}",
                        f"  - Path: `{item.path}`",
                        f"  - Status: {status}",
                        f"  - Description: {item.description}",
                    ]
                )

            lines.append("")

        lines.extend(
            [
                "## Correct Research Framing",
                "",
                "The artifact index is a navigation aid.",
                "",
                "It does not verify mathematical correctness.",
                "",
                "It helps reviewers find the project outputs quickly.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        index: ArtifactIndex,
        path: str = "docs/artifact_index.md",
    ) -> Path:
        """
        Writes the artifact index to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(index))
        return output_path


if __name__ == "__main__":
    builder = ArtifactIndexBuilder()
    index = builder.build()
    output_path = builder.write_markdown(index)

    print(index.describe())
    print(f"Wrote artifact index to {output_path}")

    if index.missing_items():
        print()
        print("Missing artifacts:")
        for item in index.missing_items():
            print("- " + item.path)
