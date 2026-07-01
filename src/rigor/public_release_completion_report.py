"""
Public release completion report for Project Aleph-Omega.

This module summarizes Phase 28, the public release package.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class PublicReleaseArtifact:
    """
    One public-release artifact.
    """

    name: str
    path: str
    purpose: str
    status: str

    def describe(self) -> str:
        return (
            f"PublicReleaseArtifact\n"
            f"Name: {self.name}\n"
            f"Path: {self.path}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class PublicReleaseCompletionReport:
    """
    Public release completion report.
    """

    title: str
    artifacts: Tuple[PublicReleaseArtifact, ...]

    def artifact_count(self) -> int:
        return len(self.artifacts)

    def completed_artifacts(self) -> Tuple[PublicReleaseArtifact, ...]:
        return tuple(artifact for artifact in self.artifacts if artifact.status == "complete")

    def describe(self) -> str:
        return (
            f"PublicReleaseCompletionReport\n"
            f"Title: {self.title}\n"
            f"Artifacts: {self.artifact_count()}\n"
            f"Completed artifacts: {len(self.completed_artifacts())}"
        )


class PublicReleaseCompletionReportBuilder:
    """
    Builds the Phase 28 public release completion report.
    """

    def build(self) -> PublicReleaseCompletionReport:
        artifacts = (
            PublicReleaseArtifact(
                name="Public README",
                path="README.md",
                purpose="Provides a clean public overview, project framing, run commands, and claim boundaries.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="README archive",
                path="README_ARCHIVE.md",
                purpose="Preserves the development-phase README history.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Public release notes",
                path="docs/public_release_readme_notes.md",
                purpose="Explains the README rewrite and public framing.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Public release index",
                path="docs/public_release_index.md",
                purpose="Maps the reviewer-facing documentation package.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Quickstart guide",
                path="docs/quickstart.md",
                purpose="Shows reviewers how to run the Lean, Lake, and Python verification stack.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Verification status page",
                path="docs/verification_status.md",
                purpose="Separates Lean-checked, Python-tested, CI-checked, and explicitly non-claimed results.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Public README tests",
                path="tests/test_rigor_public_readme.py",
                purpose="Checks the public README contains core sections, careful claims, and run commands.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Public release index tests",
                path="tests/test_rigor_public_release_index.py",
                purpose="Checks the public release documentation map.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Quickstart tests",
                path="tests/test_rigor_public_quickstart.py",
                purpose="Checks the quickstart guide and verification commands.",
                status="complete",
            ),
            PublicReleaseArtifact(
                name="Verification status tests",
                path="tests/test_rigor_public_verification_status.py",
                purpose="Checks the public verification status page.",
                status="complete",
            ),
        )

        return PublicReleaseCompletionReport(
            title="Project Aleph-Omega Public Release Completion Report",
            artifacts=artifacts,
        )

    def to_markdown(self, report: PublicReleaseCompletionReport) -> str:
        lines = [
            "# Project Aleph-Omega Public Release Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 28 prepares Project Aleph-Omega for public review by replacing the development README with a clean public front page and adding reviewer-facing documentation.",
            "",
            "## Summary",
            "",
            f"- Public-release artifacts indexed: {report.artifact_count()}",
            f"- Completed artifacts: {len(report.completed_artifacts())}",
            "",
            "## Public Release Artifacts",
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
                "## Strongest Current Public Claim",
                "",
                "> Project Aleph-Omega is publicly organized as a finite institution-inspired, Lean-supported research framework for studying satisfaction preservation under semantic translation, with a reproducible formal stack and explicit claim boundaries.",
                "",
                "## Public Boundary",
                "",
                "The project should not be described as a universal theory of institutions, a solved open problem, a full Mathlib Category instance, or a field-changing theorem.",
                "",
                "## Reviewer Starting Point",
                "",
                "Start with:",
                "",
                "```text",
                "README.md",
                "docs/public_release_index.md",
                "docs/quickstart.md",
                "docs/verification_status.md",
                "```",
                "",
                "Then verify with:",
                "",
                "```bash",
                "./scripts/check_formal_stack.sh",
                "```",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: PublicReleaseCompletionReport,
        path: str = "docs/public_release_completion_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = PublicReleaseCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote public release completion report to {output_path}")
