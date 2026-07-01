"""
Failure laboratory report generation for Project Aleph-Omega.

This module turns extracted failure cases into a readable markdown report.

The report explains:
- how many generated failures were found,
- what kinds of failures occurred,
- sample failure cases,
- what these failures say about theorem boundaries.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from src.rigor.failure_extractor import (
    ExtractedFailureCase,
    FailureExtractionReport,
    FailureExtractor,
)
from src.rigor.failure_taxonomy import FailureKind
from src.rigor.finite_universe import SemanticFeature


@dataclass(frozen=True)
class FailureLabReport:
    """
    Research-style report for extracted semantic failure cases.
    """

    extraction_report: FailureExtractionReport

    def failure_count(self) -> int:
        """
        Counts extracted failures.
        """

        return self.extraction_report.failure_count()

    def counts_by_kind(self):
        """
        Returns failure counts grouped by kind.
        """

        return self.extraction_report.counts_by_kind()

    def sample_failures(
        self,
        limit: int = 5,
    ) -> Tuple[ExtractedFailureCase, ...]:
        """
        Returns a small sample of extracted failures.
        """

        return self.extraction_report.failures[:limit]

    def describe(self) -> str:
        """
        Returns a readable summary.
        """

        return (
            f"FailureLabReport\n"
            f"Extracted failures: {self.failure_count()}\n"
            f"Failure kinds: {len(self.counts_by_kind())}"
        )


class FailureLabReportBuilder:
    """
    Builds markdown reports for the failure laboratory.
    """

    def build(
        self,
        features: Tuple[SemanticFeature, ...] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size: int = 2,
    ) -> FailureLabReport:
        """
        Builds the failure lab report from generated finite search cases.
        """

        extraction_report = FailureExtractor().run(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        return FailureLabReport(extraction_report=extraction_report)

    def to_markdown(self, report: FailureLabReport) -> str:
        """
        Converts the failure lab report into markdown.
        """

        lines = [
            "# Failure Laboratory Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the generated semantic failure cases extracted from the finite satisfaction search layer.",
            "",
            "These failures are counterexample-like boundary cases. They are not necessarily formal theorem counterexamples, but they show where preservation assumptions fail.",
            "",
            "## Summary",
            "",
            f"- Extracted failure cases: {report.failure_count()}",
            f"- Failure kinds observed: {len(report.counts_by_kind())}",
            "",
            "## Counts by Failure Kind",
            "",
        ]

        counts = report.counts_by_kind()

        if not counts:
            lines.append("- none")

        for kind, count in sorted(counts.items()):
            lines.append(f"- {kind}: {count}")

        lines.extend(
            [
                "",
                "## Failure Kind Meanings",
                "",
                "- undefined_translation: a satisfied source statement has no defined target translation",
                "- target_not_satisfied: a satisfied source statement translates to a target statement that is not satisfied",
                "- feature_mismatch: a bridge maps statements across incompatible semantic features",
                "- partial_bridge_failure: a bridge does not translate every source statement",
                "- collapse_distortion: a collapse bridge loses satisfaction-preserving structure",
                "- multiple_failures: more than one failure mechanism appears at once",
                "",
                "## Sample Extracted Failures",
                "",
            ]
        )

        samples = report.sample_failures(limit=5)

        if not samples:
            lines.append("No failures were extracted.")

        for index, failure in enumerate(samples, start=1):
            lines.extend(
                [
                    f"### Sample Failure {index}",
                    "",
                    f"- Bridge: {failure.bridge_name()}",
                    f"- Bridge kind: {failure.search_case.bridge_case.kind.value}",
                    f"- Failure kind: {failure.failure_kind().value}",
                    f"- Preserves satisfaction: {failure.search_case.preserves_satisfaction()}",
                    f"- Has distortion: {failure.search_case.has_distortion()}",
                    f"- Explanation: {failure.classification.explanation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Theorem Boundary Interpretation",
                "",
                "The failure laboratory helps separate three concepts:",
                "",
                "1. A theorem counterexample",
                "2. A failed theorem hypothesis",
                "3. A semantic boundary case",
                "",
                "The extracted failures mostly represent boundary cases where preservation assumptions are not satisfied.",
                "",
                "This is useful because a serious theorem system should explain not only when a theorem succeeds, but also why nearby cases fail.",
                "",
                "## Correct Research Claim",
                "",
                "Project Aleph-Omega can now say:",
                "",
                "The finite search layer extracts, classifies, and reports generated semantic failure cases, making theorem boundaries explicit.",
                "",
                "This remains finite, computational, and model-bound.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: FailureLabReport,
        path: str = "docs/failure_lab_report.md",
    ) -> Path:
        """
        Writes the failure lab markdown report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = FailureLabReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote report to {output_path}")
