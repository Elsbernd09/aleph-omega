"""
Public quickstart generator for Project Aleph-Omega.

This module generates a reviewer-facing quickstart guide for running and
verifying the project.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class QuickstartStep:
    """
    One quickstart step.
    """

    number: int
    title: str
    command: str
    purpose: str

    def to_markdown(self) -> str:
        """
        Converts the step to markdown.
        """

        lines = [
            f"### Step {self.number}: {self.title}",
            "",
            "```bash",
            self.command,
            "```",
            "",
            self.purpose,
        ]

        return "\n".join(lines)

    def describe(self) -> str:
        """
        Returns a readable step summary.
        """

        return (
            f"QuickstartStep\n"
            f"Number: {self.number}\n"
            f"Title: {self.title}"
        )


@dataclass(frozen=True)
class PublicQuickstart:
    """
    Reviewer-facing quickstart guide.
    """

    title: str
    steps: Tuple[QuickstartStep, ...]

    def step_count(self) -> int:
        """
        Counts quickstart steps.
        """

        return len(self.steps)

    def to_markdown(self) -> str:
        """
        Converts the quickstart to markdown.
        """

        lines = [
            f"# {self.title}",
            "",
            "## Purpose",
            "",
            "This quickstart shows reviewers how to run the Project Aleph-Omega formal stack locally.",
            "",
            "The main verification command is:",
            "",
            "```bash",
            "./scripts/check_formal_stack.sh",
            "```",
            "",
            "That command checks the Lean core, Lake project synchronization, Lake build, and Python tests.",
            "",
            "## Prerequisites",
            "",
            "- Python 3",
            "- pytest",
            "- Lean installed through elan",
            "- macOS or Linux shell environment",
            "",
            "## Quickstart Steps",
            "",
        ]

        for step in self.steps:
            lines.append(step.to_markdown())
            lines.append("")

        lines.extend(
            [
                "## Expected Success Signal",
                "",
                "The full formal-stack command should end with:",
                "",
                "```text",
                "Aleph-Omega formal stack verified successfully.",
                "```",
                "",
                "## What the Verification Means",
                "",
                "A successful run means:",
                "",
                "- the primary Lean formalization compiles,",
                "- the Lake copy is synchronized with the primary Lean file,",
                "- the Lake project builds,",
                "- the Python test suite passes.",
                "",
                "## What the Verification Does Not Mean",
                "",
                "A successful run does not mean the project proves a universal theorem about all institutions or all logics.",
                "",
                "It means the repository's stated finite Lean/Python formal stack is reproducible.",
                "",
            ]
        )

        return "\n".join(lines)

    def describe(self) -> str:
        """
        Returns a readable quickstart summary.
        """

        return (
            f"PublicQuickstart\n"
            f"Title: {self.title}\n"
            f"Steps: {self.step_count()}"
        )


class PublicQuickstartBuilder:
    """
    Builds the public quickstart guide.
    """

    def build(self) -> PublicQuickstart:
        """
        Builds the standard quickstart guide.
        """

        steps = (
            QuickstartStep(
                number=1,
                title="Install Python test dependency",
                command="python3 -m pip install pytest",
                purpose="Installs pytest, which is required for the Python test suite.",
            ),
            QuickstartStep(
                number=2,
                title="Check the primary Lean formalization",
                command='source "$HOME/.elan/env"\n./scripts/check_lean.sh',
                purpose="Compiles the primary Lean file at formal/lean/AlephOmegaCore.lean.",
            ),
            QuickstartStep(
                number=3,
                title="Check Lake synchronization",
                command="./scripts/check_lake_sync.sh",
                purpose="Verifies that the primary Lean file and Lake project copy are identical.",
            ),
            QuickstartStep(
                number=4,
                title="Build the Lake project",
                command='source "$HOME/.elan/env"\n./scripts/check_lake.sh',
                purpose="Builds the standalone Lean Lake project.",
            ),
            QuickstartStep(
                number=5,
                title="Run Python tests",
                command="python3 -m pytest",
                purpose="Runs the Python finite-computation and documentation-generation test suite.",
            ),
            QuickstartStep(
                number=6,
                title="Run the full formal stack",
                command='source "$HOME/.elan/env"\n./scripts/check_formal_stack.sh',
                purpose="Runs the complete verification gate in one command.",
            ),
        )

        return PublicQuickstart(
            title="Project Aleph-Omega Quickstart",
            steps=steps,
        )

    def write_markdown(
        self,
        quickstart: PublicQuickstart,
        path: str = "docs/quickstart.md",
    ) -> Path:
        """
        Writes the quickstart to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(quickstart.to_markdown())
        return output_path


if __name__ == "__main__":
    builder = PublicQuickstartBuilder()
    quickstart = builder.build()
    output_path = builder.write_markdown(quickstart)

    print(quickstart.describe())
    print(f"Wrote quickstart to {output_path}")
