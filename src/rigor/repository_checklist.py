"""
Repository checklist generator for Project Aleph-Omega.

This module creates a final reviewer-readiness checklist for the repository.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ChecklistItem:
    """
    One repository checklist item.
    """

    title: str
    category: str
    completed: bool
    evidence: Tuple[str, ...]
    explanation: str

    def status_label(self) -> str:
        """
        Returns a readable status label.
        """

        return "complete" if self.completed else "incomplete"

    def describe(self) -> str:
        """
        Returns a readable checklist item.
        """

        evidence_text = "; ".join(self.evidence) if self.evidence else "none"

        return (
            f"ChecklistItem\n"
            f"Title: {self.title}\n"
            f"Category: {self.category}\n"
            f"Status: {self.status_label()}\n"
            f"Evidence: {evidence_text}\n"
            f"Explanation: {self.explanation}"
        )


@dataclass(frozen=True)
class RepositoryChecklist:
    """
    Final repository checklist.
    """

    items: Tuple[ChecklistItem, ...]

    def item_count(self) -> int:
        """
        Counts checklist items.
        """

        return len(self.items)

    def completed_items(self) -> Tuple[ChecklistItem, ...]:
        """
        Returns completed items.
        """

        return tuple(item for item in self.items if item.completed)

    def incomplete_items(self) -> Tuple[ChecklistItem, ...]:
        """
        Returns incomplete items.
        """

        return tuple(item for item in self.items if not item.completed)

    def complete(self) -> bool:
        """
        Returns whether every checklist item is complete.
        """

        return len(self.incomplete_items()) == 0

    def categories(self) -> Tuple[str, ...]:
        """
        Returns checklist categories.
        """

        return tuple(sorted({item.category for item in self.items}))

    def describe(self) -> str:
        """
        Returns a readable checklist summary.
        """

        return (
            f"RepositoryChecklist\n"
            f"Items: {self.item_count()}\n"
            f"Completed: {len(self.completed_items())}\n"
            f"Incomplete: {len(self.incomplete_items())}\n"
            f"Complete: {self.complete()}"
        )


class RepositoryChecklistBuilder:
    """
    Builds the standard final repository checklist.
    """

    def build(self) -> RepositoryChecklist:
        """
        Builds the repository checklist.
        """

        items = (
            ChecklistItem(
                title="README exists",
                category="repository",
                completed=Path("README.md").exists(),
                evidence=("README.md",),
                explanation="The repository has a main entry point.",
            ),
            ChecklistItem(
                title="Reviewer quickstart exists",
                category="reviewer_readiness",
                completed=Path("docs/reviewer_quickstart.md").exists(),
                evidence=("docs/reviewer_quickstart.md",),
                explanation="A reviewer has a short guide for understanding and running the project.",
            ),
            ChecklistItem(
                title="Artifact index exists",
                category="reviewer_readiness",
                completed=Path("docs/artifact_index.md").exists(),
                evidence=("docs/artifact_index.md",),
                explanation="The repo has a central index of important artifacts.",
            ),
            ChecklistItem(
                title="Project health check exists",
                category="reviewer_readiness",
                completed=Path("src/rigor/project_health.py").exists(),
                evidence=("src/rigor/project_health.py", "tests/test_rigor_project_health.py"),
                explanation="The repo can check whether major artifacts exist.",
            ),
            ChecklistItem(
                title="Research abstract generated",
                category="research_artifacts",
                completed=Path("docs/research_abstract.md").exists(),
                evidence=("docs/research_abstract.md",),
                explanation="The repo includes a concise research abstract.",
            ),
            ChecklistItem(
                title="Final research memo generated",
                category="research_artifacts",
                completed=Path("docs/final_research_memo.md").exists(),
                evidence=("docs/final_research_memo.md",),
                explanation="The repo includes a polished final research memo.",
            ),
            ChecklistItem(
                title="Theorem inventory generated",
                category="research_artifacts",
                completed=Path("docs/theorem_inventory.md").exists(),
                evidence=("docs/theorem_inventory.md",),
                explanation="The repo records theorem-like claims with scope and limitations.",
            ),
            ChecklistItem(
                title="Model-search report generated",
                category="model_search",
                completed=Path("docs/model_search_report.md").exists(),
                evidence=("docs/model_search_report.md",),
                explanation="The repo includes generated finite model-search results.",
            ),
            ChecklistItem(
                title="Failure laboratory report generated",
                category="failure_lab",
                completed=Path("docs/failure_lab_report.md").exists(),
                evidence=("docs/failure_lab_report.md",),
                explanation="The repo includes generated semantic failure analysis.",
            ),
            ChecklistItem(
                title="Verification report generated",
                category="verification",
                completed=Path("docs/verification_report.md").exists(),
                evidence=("docs/verification_report.md",),
                explanation="The repo includes claim audit and proof obligation reporting.",
            ),
            ChecklistItem(
                title="Core test suite present",
                category="testing",
                completed=Path("tests").exists(),
                evidence=("tests/",),
                explanation="The repository includes tests for the rigor-track modules.",
            ),
            ChecklistItem(
                title="Core source package present",
                category="source",
                completed=Path("src/rigor").exists(),
                evidence=("src/rigor/",),
                explanation="The repository includes the rigor-track source package.",
            ),
        )

        return RepositoryChecklist(items=items)

    def to_markdown(self, checklist: RepositoryChecklist) -> str:
        """
        Converts the checklist to markdown.
        """

        lines = [
            "# Repository Checklist",
            "",
            "## Purpose",
            "",
            "This checklist summarizes repository readiness for Project Aleph-Omega.",
            "",
            "It helps a reviewer see whether the main source files, docs, reports, and research artifacts are present.",
            "",
            "## Summary",
            "",
            f"- Checklist items: {checklist.item_count()}",
            f"- Completed items: {len(checklist.completed_items())}",
            f"- Incomplete items: {len(checklist.incomplete_items())}",
            f"- Complete: {checklist.complete()}",
            "",
            "## Checklist by Category",
            "",
        ]

        for category in checklist.categories():
            lines.extend(
                [
                    f"### {category}",
                    "",
                ]
            )

            for item in checklist.items:
                if item.category != category:
                    continue

                mark = "x" if item.completed else " "
                lines.extend(
                    [
                        f"- [{mark}] {item.title}",
                        f"  - Evidence: {', '.join(item.evidence)}",
                        f"  - Explanation: {item.explanation}",
                    ]
                )

            lines.append("")

        lines.extend(
            [
                "## Correct Research Framing",
                "",
                "The checklist verifies repository readiness, not mathematical truth.",
                "",
                "Mathematical claims are handled separately through theorem inventory, model search, failure analysis, and verification reports.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        checklist: RepositoryChecklist,
        path: str = "docs/repository_checklist.md",
    ) -> Path:
        """
        Writes the repository checklist to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(checklist))
        return output_path


if __name__ == "__main__":
    builder = RepositoryChecklistBuilder()
    checklist = builder.build()
    output_path = builder.write_markdown(checklist)

    print(checklist.describe())
    print(f"Wrote repository checklist to {output_path}")

    if checklist.incomplete_items():
        print()
        print("Incomplete items:")
        for item in checklist.incomplete_items():
            print("- " + item.title)
