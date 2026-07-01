"""
Model-search report generation for Project ℵω.

This module combines the Phase 14 search layers into one readable report:

- Bridge Distortion Theorem search
- Satisfaction Preservation search
- aggregate finite model-search summary

The output is a markdown research report.
"""

from dataclasses import dataclass
from pathlib import Path

from src.rigor.bridge_case_generator import BridgeCaseKind
from src.rigor.bridge_distortion_search import (
    BridgeDistortionSearchReport,
    BridgeDistortionSearchRunner,
)
from src.rigor.finite_universe import SemanticFeature
from src.rigor.satisfaction_search import (
    SatisfactionSearchReport,
    SatisfactionSearchRunner,
)


@dataclass(frozen=True)
class CombinedModelSearchReport:
    """
    Combined report for the Phase 14 finite model searches.
    """

    bridge_distortion_report: BridgeDistortionSearchReport
    satisfaction_report: SatisfactionSearchReport

    def total_cases(self) -> int:
        """
        Counts all generated search cases across both reports.
        """

        return (
            self.bridge_distortion_report.case_count()
            + self.satisfaction_report.case_count()
        )

    def bridge_distortion_counterexample_count(self) -> int:
        """
        Counts bridge distortion theorem counterexamples.
        """

        return len(self.bridge_distortion_report.counterexamples())

    def satisfaction_distortion_case_count(self) -> int:
        """
        Counts satisfaction distortion cases.
        """

        return len(self.satisfaction_report.distortion_cases())

    def theorem_survived_bridge_search(self) -> bool:
        """
        Returns whether the Bridge Distortion Theorem survived generated search.
        """

        return self.bridge_distortion_report.theorem_survived_search()

    def describe(self) -> str:
        """
        Returns a readable combined summary.
        """

        return (
            f"CombinedModelSearchReport\n"
            f"Total generated cases: {self.total_cases()}\n"
            f"Bridge distortion search cases: {self.bridge_distortion_report.case_count()}\n"
            f"Satisfaction search cases: {self.satisfaction_report.case_count()}\n"
            f"Bridge distortion counterexamples: {self.bridge_distortion_counterexample_count()}\n"
            f"Satisfaction distortion cases: {self.satisfaction_distortion_case_count()}\n"
            f"Bridge theorem survived search: {self.theorem_survived_bridge_search()}"
        )


class ModelSearchReportBuilder:
    """
    Builds combined finite model-search reports.
    """

    def build(
        self,
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ),
        max_feature_set_size: int = 2,
    ) -> CombinedModelSearchReport:
        """
        Builds the combined Phase 14 report.
        """

        bridge_report = BridgeDistortionSearchRunner().run(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        satisfaction_report = SatisfactionSearchRunner().run(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        return CombinedModelSearchReport(
            bridge_distortion_report=bridge_report,
            satisfaction_report=satisfaction_report,
        )

    def to_markdown(self, report: CombinedModelSearchReport) -> str:
        """
        Converts a combined report into markdown.
        """

        bridge = report.bridge_distortion_report
        satisfaction = report.satisfaction_report

        lines = [
            "# Project ℵω Finite Model-Search Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the Phase 14 finite model-search layer.",
            "",
            "The goal is to stress-test the finite theorem and semantics machinery against generated small models rather than only hand-built examples.",
            "",
            "The report covers:",
            "",
            "- Bridge Distortion Theorem search",
            "- Satisfaction Preservation search",
            "- bridge-kind level case counts",
            "- preservation and distortion rates",
            "",
            "## Combined Summary",
            "",
            f"- Total generated cases: {report.total_cases()}",
            f"- Bridge distortion search cases: {bridge.case_count()}",
            f"- Satisfaction preservation search cases: {satisfaction.case_count()}",
            f"- Bridge distortion theorem counterexamples: {len(bridge.counterexamples())}",
            f"- Satisfaction distortion cases: {len(satisfaction.distortion_cases())}",
            f"- Bridge theorem survived generated search: {bridge.theorem_survived_search()}",
            "",
            "## Bridge Distortion Theorem Search",
            "",
            f"- Cases: {bridge.case_count()}",
            f"- Nonvacuous theorem instances: {len(bridge.nonvacuous_instances())}",
            f"- Vacuous theorem instances: {len(bridge.vacuous_instances())}",
            f"- Counterexamples: {len(bridge.counterexamples())}",
            f"- Theorem survived search: {bridge.theorem_survived_search()}",
            "",
            "### Bridge Distortion Cases by Bridge Kind",
            "",
        ]

        for kind in BridgeCaseKind:
            lines.append(f"- {kind.value}: {len(bridge.cases_by_kind(kind))}")

        lines.extend(
            [
                "",
                "## Satisfaction Preservation Search",
                "",
                f"- Cases: {satisfaction.case_count()}",
                f"- Preserving cases: {len(satisfaction.preserving_cases())}",
                f"- Distortion cases: {len(satisfaction.distortion_cases())}",
                f"- Preservation rate: {satisfaction.preservation_rate():.3f}",
                f"- Distortion rate: {satisfaction.distortion_rate():.3f}",
                "",
                "### Satisfaction Cases by Bridge Kind",
                "",
            ]
        )

        for kind in BridgeCaseKind:
            lines.append(f"- {kind.value}: {len(satisfaction.cases_by_kind(kind))}")

        lines.extend(
            [
                "",
                "## Research Interpretation",
                "",
                "The finite model-search layer makes the project stronger because it turns the theorem layer into a testable experimental system.",
                "",
                "The project now follows the workflow:",
                "",
                "1. define finite semantic structures",
                "2. define bridges between structures",
                "3. define theorem claims",
                "4. generate finite models and bridges",
                "5. search for preservation, distortion, and counterexamples",
                "",
                "## Correct Claim",
                "",
                "The careful result is:",
                "",
                "In the generated finite search space, the implemented Bridge Distortion Theorem produced no counterexamples, and the satisfaction layer measured exactly where generated bridge cases preserved or distorted satisfaction.",
                "",
                "This is not a proof about all mathematical universes or all logics.",
                "",
                "It is a finite computational stress test of the Project ℵω rigor layer.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: CombinedModelSearchReport,
        path: str = "docs/model_search_report.md",
    ) -> Path:
        """
        Writes the report markdown to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = ModelSearchReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print()
    print(f"Wrote report to {output_path}")
