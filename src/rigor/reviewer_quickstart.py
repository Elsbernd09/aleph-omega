"""
Reviewer quickstart generator for Project Aleph-Omega.

This module creates a short guide for reviewers who want to understand and run
the project quickly.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReviewerQuickstart:
    """
    Reviewer quickstart artifact.
    """

    title: str
    body: str

    def section_count(self) -> int:
        """
        Counts markdown section headings.
        """

        return sum(1 for line in self.body.splitlines() if line.startswith("## "))

    def to_markdown(self) -> str:
        """
        Converts the quickstart to markdown.
        """

        return f"# {self.title}\n\n{self.body}"

    def describe(self) -> str:
        """
        Returns a readable quickstart summary.
        """

        return (
            f"ReviewerQuickstart\n"
            f"Title: {self.title}\n"
            f"Sections: {self.section_count()}"
        )


class ReviewerQuickstartBuilder:
    """
    Builds the reviewer quickstart document.
    """

    def build(self) -> ReviewerQuickstart:
        """
        Builds the standard reviewer quickstart.
        """

        body = "\n".join(
            [
                "## Purpose",
                "",
                "This quickstart helps a reviewer understand Project Aleph-Omega quickly.",
                "",
                "The project is a finite computational mathematics framework for studying semantic preservation and distortion across generated finite bridge systems.",
                "",
                "It should be reviewed as a finite model-bound research project, not as a universal proof about all mathematics.",
                "",
                "## Fastest Review Path",
                "",
                "Start with these files:",
                "",
                "1. README.md",
                "2. docs/research_abstract.md",
                "3. docs/final_research_memo.md",
                "4. docs/architecture_map.md",
                "5. docs/theorem_inventory.md",
                "6. docs/model_search_report.md",
                "7. docs/failure_lab_report.md",
                "8. docs/verification_report.md",
                "",
                "## Run the Full Test Suite",
                "",
                "Run:",
                "",
                "python3 -m pytest",
                "",
                "A passing test suite shows that the implemented finite framework, reports, and artifact generators are internally consistent.",
                "",
                "## Regenerate Core Reports",
                "",
                "Run:",
                "",
                "python3 -m src.rigor.search_report",
                "python3 -m src.rigor.failure_report",
                "python3 -m src.rigor.verification_report",
                "python3 -m src.rigor.research_abstract",
                "python3 -m src.rigor.theorem_inventory",
                "python3 -m src.rigor.architecture_map",
                "python3 -m src.rigor.final_research_memo",
                "python3 -m src.rigor.artifact_index",
                "",
                "## Check Repository Health",
                "",
                "Run:",
                "",
                "python3 -m src.rigor.project_health",
                "",
                "This checks whether key docs, reports, source files, and tests exist.",
                "",
                "## Main Technical Layers",
                "",
                "- finite logical universes",
                "- bridge and distortion analysis",
                "- satisfaction semantics",
                "- category-like bridge composition",
                "- functorial semantics",
                "- finite model search",
                "- failure laboratory",
                "- formal verification interface",
                "- research artifact generation",
                "",
                "## Correct Interpretation",
                "",
                "The strongest honest claim is:",
                "",
                "Project Aleph-Omega implements a finite computational laboratory for studying semantic preservation and distortion across generated finite bridge systems, with theorem-like claims recorded, tested, audited, and bounded by explicit limitations.",
                "",
                "The project should not be interpreted as proving universal results about all logics, categories, topoi, model theories, or mathematical foundations.",
                "",
            ]
        )

        return ReviewerQuickstart(
            title="Reviewer Quickstart",
            body=body,
        )

    def write_markdown(
        self,
        quickstart: ReviewerQuickstart,
        path: str = "docs/reviewer_quickstart.md",
    ) -> Path:
        """
        Writes the reviewer quickstart to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(quickstart.to_markdown())
        return output_path


if __name__ == "__main__":
    builder = ReviewerQuickstartBuilder()
    quickstart = builder.build()
    output_path = builder.write_markdown(quickstart)

    print(quickstart.describe())
    print(f"Wrote reviewer quickstart to {output_path}")
