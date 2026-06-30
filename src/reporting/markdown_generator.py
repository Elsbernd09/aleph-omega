"""
Markdown report generator for Project ℵω.

This module converts research artifact collections into polished Markdown
reports.

The report generator organizes existing computational outputs. It does not
create proofs or validate mathematical claims.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from src.reporting.artifact import (
    ArtifactRisk,
    ArtifactStatus,
    ResearchArtifact,
    ResearchArtifactCollection,
)


@dataclass(frozen=True)
class MarkdownReport:
    """
    A generated Markdown report.
    """

    title: str
    markdown: str
    artifact_count: int
    review_required_count: int
    generated_at: str
    metadata: Optional[Dict[str, str]] = None

    def line_count(self) -> int:
        """
        Counts report lines.
        """

        return len(self.markdown.splitlines())

    def word_count(self) -> int:
        """
        Counts report words.
        """

        return len(self.markdown.split())

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"MarkdownReport: {self.title}\n"
            f"Generated at: {self.generated_at}\n"
            f"Artifact count: {self.artifact_count}\n"
            f"Review required count: {self.review_required_count}\n"
            f"Line count: {self.line_count()}\n"
            f"Word count: {self.word_count()}"
        )


class MarkdownReportGenerator:
    """
    Generates Markdown reports from research artifact collections.
    """

    def generate(
        self,
        collection: ResearchArtifactCollection,
        title: str = "Project ℵω Research Report",
    ) -> MarkdownReport:
        """
        Generates a full Markdown report.
        """

        generated_at = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

        parts: List[str] = []
        parts.append(self._title_page(title, generated_at))
        parts.append(self._executive_summary(collection))
        parts.append(self._collection_metrics(collection))
        parts.append(self._phase_overview())
        parts.append(self._artifact_sections(collection))
        parts.append(self._review_queue(collection))
        parts.append(self._limitations())
        parts.append(self._next_steps())

        markdown = "\n\n".join(parts).rstrip() + "\n"

        return MarkdownReport(
            title=title,
            markdown=markdown,
            artifact_count=collection.artifact_count(),
            review_required_count=collection.review_required_count(),
            generated_at=generated_at,
            metadata={
                "average_confidence": str(collection.average_confidence()),
            },
        )

    @staticmethod
    def _title_page(title: str, generated_at: str) -> str:
        """
        Builds title section.
        """

        return (
            f"# {title}\n\n"
            f"**Generated:** {generated_at}\n\n"
            f"**Project:** Project ℵω — Trans-Axiomatic Architectonics\n\n"
            f"**Report type:** Computational research-system summary\n\n"
            f"> This report summarizes a software framework for experimenting with "
            f"toy formal universes, bridge translations, cognitive formalization, "
            f"and formalization planning. It is not a claim of completed proof."
        )

    @staticmethod
    def _executive_summary(collection: ResearchArtifactCollection) -> str:
        """
        Builds executive summary.
        """

        return (
            "## Executive Summary\n\n"
            f"{collection.summary or 'This report summarizes Project ℵω research artifacts.'}\n\n"
            f"The current system contains **{collection.artifact_count()}** reportable "
            f"artifact(s). **{collection.review_required_count()}** artifact(s) require "
            f"human review before being used in serious mathematical claims. The average "
            f"artifact confidence score is **{collection.average_confidence()} / 10**.\n\n"
            f"The project should be interpreted as a computational research framework, "
            f"not as a finished formal theory."
        )

    @staticmethod
    def _collection_metrics(collection: ResearchArtifactCollection) -> str:
        """
        Builds collection metrics section.
        """

        kind_counts = "\n".join(
            f"- **{kind}:** {count}"
            for kind, count in sorted(collection.artifacts_by_kind().items())
        ) or "- none"

        return (
            "## Collection Metrics\n\n"
            f"- **Artifact count:** {collection.artifact_count()}\n"
            f"- **Review required count:** {collection.review_required_count()}\n"
            f"- **Average confidence:** {collection.average_confidence()} / 10\n\n"
            "### Artifact Counts by Kind\n\n"
            f"{kind_counts}"
        )

    @staticmethod
    def _phase_overview() -> str:
        """
        Builds phase overview.
        """

        return (
            "## Phase Overview\n\n"
            "- **Phase 1:** Research framing and design documentation\n"
            "- **Phase 2:** Generative Axiom Engine\n"
            "- **Phase 3:** Toy Logical Universes\n"
            "- **Phase 4:** Toy Topos Simulator\n"
            "- **Phase 5:** Bridge Translation Engine\n"
            "- **Phase 6:** Cognitive Morphism Layer\n"
            "- **Phase 7:** Neural-Symbolic Formalization Layer\n"
            "- **Phase 8:** Meta-Theory / System Intelligence Layer\n"
            "- **Phase 9:** Unified Research Report + Output Layer"
        )

    @staticmethod
    def _artifact_sections(collection: ResearchArtifactCollection) -> str:
        """
        Builds artifact sections.
        """

        if not collection.artifacts:
            return "## Research Artifacts\n\nNo artifacts were provided."

        sections = "\n\n".join(
            artifact.markdown_section() for artifact in collection.artifacts
        )

        return f"## Research Artifacts\n\n{sections}"

    @staticmethod
    def _review_queue(collection: ResearchArtifactCollection) -> str:
        """
        Builds review queue section.
        """

        review_items = [
            artifact for artifact in collection.artifacts
            if artifact.requires_review()
        ]

        if not review_items:
            return (
                "## Human Review Queue\n\n"
                "No artifacts are currently marked as requiring urgent human review."
            )

        lines = []

        for artifact in review_items:
            lines.append(
                f"- **{artifact.title}** "
                f"({artifact.kind.value}, risk={artifact.risk.value}, "
                f"confidence={artifact.normalized_confidence()})"
            )

        return (
            "## Human Review Queue\n\n"
            "The following artifacts should be reviewed before being used in serious claims:\n\n"
            + "\n".join(lines)
        )

    @staticmethod
    def _limitations() -> str:
        """
        Builds limitations section.
        """

        return (
            "## Limitations\n\n"
            "- The system uses heuristic metrics, not formal mathematical guarantees.\n"
            "- Toy universes are simplified computational models, not complete topoi.\n"
            "- Bridge translations are diagnostics, not categorical equivalences.\n"
            "- Cognitive morphisms model the informal-to-formal transition, but do not model human cognition.\n"
            "- Lean-style sketches containing `sorry` are unfinished and not machine-checked proofs.\n"
            "- Any serious mathematical claim requires human review and formal verification."
        )

    @staticmethod
    def _next_steps() -> str:
        """
        Builds next steps section.
        """

        return (
            "## Recommended Next Steps\n\n"
            "1. Select one small statement from the system and formalize it carefully.\n"
            "2. Replace placeholder definitions with precise mathematical definitions.\n"
            "3. Create a minimal Lean file with no unresolved proof claims.\n"
            "4. Add stronger examples to the universe and bridge layers.\n"
            "5. Continue keeping project claims honest and clearly separated from proof completion."
        )

    def save(
        self,
        report: MarkdownReport,
        output_path: str,
    ) -> None:
        """
        Saves a Markdown report to disk.
        """

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report.markdown)


if __name__ == "__main__":
    from src.reporting.artifact import demo_artifact_collection

    generator = MarkdownReportGenerator()
    report = generator.generate(demo_artifact_collection())

    print(report.describe())
    print()
    print(report.markdown)
