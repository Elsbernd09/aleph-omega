"""
Failure extractor for Project Aleph-Omega.

This module extracts counterexample-like semantic failure cases from the
finite satisfaction search layer.

These are not necessarily counterexamples to the formal theorem. They are
generated cases where satisfaction preservation fails and the failure can be
classified.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from src.rigor.failure_taxonomy import FailureClassification, FailureClassifier, FailureKind
from src.rigor.finite_universe import SemanticFeature
from src.rigor.satisfaction_search import SatisfactionSearchCase, SatisfactionSearchRunner


@dataclass(frozen=True)
class ExtractedFailureCase:
    """
    A generated semantic failure case with classification.
    """

    search_case: SatisfactionSearchCase
    classification: FailureClassification

    def bridge_name(self) -> str:
        """
        Returns the bridge name.
        """

        return self.search_case.bridge_case.bridge.name

    def failure_kind(self) -> FailureKind:
        """
        Returns the failure kind.
        """

        return self.classification.kind

    def describe(self) -> str:
        """
        Returns a readable extracted failure case.
        """

        return (
            f"ExtractedFailureCase\n"
            f"Bridge: {self.bridge_name()}\n"
            f"Bridge kind: {self.search_case.bridge_case.kind.value}\n"
            f"Failure kind: {self.failure_kind().value}\n"
            f"Preserves satisfaction: {self.search_case.preserves_satisfaction()}\n"
            f"Has distortion: {self.search_case.has_distortion()}\n"
            f"Explanation: {self.classification.explanation}"
        )


@dataclass(frozen=True)
class FailureExtractionReport:
    """
    Report of extracted failure cases.
    """

    failures: Tuple[ExtractedFailureCase, ...]

    def failure_count(self) -> int:
        """
        Counts extracted failure cases.
        """

        return len(self.failures)

    def by_kind(self, kind: FailureKind) -> Tuple[ExtractedFailureCase, ...]:
        """
        Returns failures of a given kind.
        """

        return tuple(failure for failure in self.failures if failure.failure_kind() == kind)

    def counts_by_kind(self) -> Dict[str, int]:
        """
        Returns failure counts grouped by kind.
        """

        counts = {}

        for failure in self.failures:
            key = failure.failure_kind().value
            counts[key] = counts.get(key, 0) + 1

        return counts

    def has_failures(self) -> bool:
        """
        Returns whether any failures were extracted.
        """

        return self.failure_count() > 0

    def describe(self) -> str:
        """
        Returns a readable extraction report.
        """

        lines = [
            "FailureExtractionReport",
            f"Extracted failures: {self.failure_count()}",
            "Counts by kind:",
        ]

        counts = self.counts_by_kind()

        if not counts:
            lines.append("- none")

        for kind, count in sorted(counts.items()):
            lines.append(f"- {kind}: {count}")

        return "\n".join(lines)


class FailureExtractor:
    """
    Extracts classified semantic failure cases from satisfaction search results.
    """

    def __init__(self) -> None:
        self.classifier = FailureClassifier()

    def extract_from_cases(
        self,
        cases: Tuple[SatisfactionSearchCase, ...],
    ) -> FailureExtractionReport:
        """
        Extracts all classified failures from generated satisfaction cases.
        """

        failures = []

        for case in cases:
            classification = self.classifier.classify_satisfaction_case(case)

            if classification.is_failure():
                failures.append(
                    ExtractedFailureCase(
                        search_case=case,
                        classification=classification,
                    )
                )

        return FailureExtractionReport(failures=tuple(failures))

    def run(
        self,
        features: Tuple[SemanticFeature, ...] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size: int = 2,
    ) -> FailureExtractionReport:
        """
        Runs satisfaction search and extracts classified failures.
        """

        satisfaction_report = SatisfactionSearchRunner().run(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        return self.extract_from_cases(satisfaction_report.cases)


if __name__ == "__main__":
    report = FailureExtractor().run()

    print(report.describe())
    print()

    print("Sample extracted failures:")
    for failure in report.failures[:5]:
        print()
        print(failure.describe())
