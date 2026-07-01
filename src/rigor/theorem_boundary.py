"""
Theorem boundary analysis for Project Aleph-Omega.

This module studies the boundary between theorem success, vacuous success,
hypothesis failure, semantic distortion, and structural failure.

The goal is to explain why a generated case succeeds or fails.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple

from src.rigor.failure_extractor import ExtractedFailureCase, FailureExtractor
from src.rigor.failure_taxonomy import FailureKind
from src.rigor.finite_universe import SemanticFeature
from src.rigor.satisfaction_search import SatisfactionSearchCase, SatisfactionSearchRunner


class BoundaryStatus(str, Enum):
    """
    Boundary status for a generated semantic case.
    """

    VERIFIED_PRESERVATION = "verified_preservation"
    VACUOUS_PRESERVATION = "vacuous_preservation"
    HYPOTHESIS_FAILURE = "hypothesis_failure"
    SEMANTIC_DISTORTION = "semantic_distortion"
    STRUCTURAL_FAILURE = "structural_failure"


@dataclass(frozen=True)
class BoundaryClassification:
    """
    Boundary classification for one generated case.
    """

    status: BoundaryStatus
    bridge_name: str
    bridge_kind: str
    explanation: str

    def is_success(self) -> bool:
        """
        Returns whether the case represents successful preservation.
        """

        return self.status in {
            BoundaryStatus.VERIFIED_PRESERVATION,
            BoundaryStatus.VACUOUS_PRESERVATION,
        }

    def is_failure(self) -> bool:
        """
        Returns whether the case represents failure or boundary failure.
        """

        return not self.is_success()

    def describe(self) -> str:
        """
        Returns a readable boundary classification.
        """

        return (
            f"BoundaryClassification\n"
            f"Status: {self.status.value}\n"
            f"Bridge: {self.bridge_name}\n"
            f"Bridge kind: {self.bridge_kind}\n"
            f"Success: {self.is_success()}\n"
            f"Failure: {self.is_failure()}\n"
            f"Explanation: {self.explanation}"
        )


@dataclass(frozen=True)
class BoundaryAnalysisReport:
    """
    Report of theorem-boundary classifications.
    """

    classifications: Tuple[BoundaryClassification, ...]

    def case_count(self) -> int:
        """
        Counts boundary cases.
        """

        return len(self.classifications)

    def by_status(self, status: BoundaryStatus) -> Tuple[BoundaryClassification, ...]:
        """
        Returns classifications with a given status.
        """

        return tuple(item for item in self.classifications if item.status == status)

    def counts_by_status(self) -> Dict[str, int]:
        """
        Returns counts grouped by boundary status.
        """

        counts = {}

        for classification in self.classifications:
            key = classification.status.value
            counts[key] = counts.get(key, 0) + 1

        return counts

    def success_count(self) -> int:
        """
        Counts successful boundary classifications.
        """

        return sum(1 for item in self.classifications if item.is_success())

    def failure_count(self) -> int:
        """
        Counts failure boundary classifications.
        """

        return sum(1 for item in self.classifications if item.is_failure())

    def describe(self) -> str:
        """
        Returns a readable boundary report.
        """

        lines = [
            "BoundaryAnalysisReport",
            f"Cases: {self.case_count()}",
            f"Successes: {self.success_count()}",
            f"Failures: {self.failure_count()}",
            "Counts by status:",
        ]

        for status, count in sorted(self.counts_by_status().items()):
            lines.append(f"- {status}: {count}")

        return "\n".join(lines)


class TheoremBoundaryAnalyzer:
    """
    Analyzes theorem-boundary behavior in generated satisfaction cases.
    """

    def classify_satisfaction_case(
        self,
        case: SatisfactionSearchCase,
    ) -> BoundaryClassification:
        """
        Classifies one generated satisfaction case.
        """

        bridge = case.bridge_case.bridge

        if not case.has_distortion():
            if case.source_case.true_count == 0:
                return BoundaryClassification(
                    status=BoundaryStatus.VACUOUS_PRESERVATION,
                    bridge_name=bridge.name,
                    bridge_kind=case.bridge_case.kind.value,
                    explanation="Preservation holds vacuously because no source statement is satisfied.",
                )

            return BoundaryClassification(
                status=BoundaryStatus.VERIFIED_PRESERVATION,
                bridge_name=bridge.name,
                bridge_kind=case.bridge_case.kind.value,
                explanation="At least one source statement is satisfied and all satisfied sources are preserved.",
            )

        if not bridge.is_total():
            return BoundaryClassification(
                status=BoundaryStatus.STRUCTURAL_FAILURE,
                bridge_name=bridge.name,
                bridge_kind=case.bridge_case.kind.value,
                explanation="The bridge is not total, so at least one satisfied source statement lacks translation.",
            )

        if bridge.has_feature_mismatch():
            return BoundaryClassification(
                status=BoundaryStatus.HYPOTHESIS_FAILURE,
                bridge_name=bridge.name,
                bridge_kind=case.bridge_case.kind.value,
                explanation="The bridge violates a structural compatibility condition through feature mismatch.",
            )

        return BoundaryClassification(
            status=BoundaryStatus.SEMANTIC_DISTORTION,
            bridge_name=bridge.name,
            bridge_kind=case.bridge_case.kind.value,
            explanation="The bridge is structurally defined but fails to preserve satisfaction.",
        )

    def analyze_cases(
        self,
        cases: Tuple[SatisfactionSearchCase, ...],
    ) -> BoundaryAnalysisReport:
        """
        Analyzes many generated satisfaction cases.
        """

        return BoundaryAnalysisReport(
            classifications=tuple(self.classify_satisfaction_case(case) for case in cases)
        )

    def analyze_extracted_failures(
        self,
        failures: Tuple[ExtractedFailureCase, ...],
    ) -> BoundaryAnalysisReport:
        """
        Converts extracted failure cases into boundary classifications.
        """

        classifications = []

        for failure in failures:
            bridge = failure.search_case.bridge_case.bridge
            failure_kind = failure.failure_kind()

            if failure_kind == FailureKind.UNDEFINED_TRANSLATION:
                status = BoundaryStatus.STRUCTURAL_FAILURE
                explanation = "The extracted failure is caused by undefined translation."
            elif failure_kind == FailureKind.FEATURE_MISMATCH:
                status = BoundaryStatus.HYPOTHESIS_FAILURE
                explanation = "The extracted failure is caused by feature mismatch."
            else:
                status = BoundaryStatus.SEMANTIC_DISTORTION
                explanation = failure.classification.explanation

            classifications.append(
                BoundaryClassification(
                    status=status,
                    bridge_name=bridge.name,
                    bridge_kind=failure.search_case.bridge_case.kind.value,
                    explanation=explanation,
                )
            )

        return BoundaryAnalysisReport(classifications=tuple(classifications))

    def run(
        self,
        features: Tuple[SemanticFeature, ...] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size: int = 2,
    ) -> BoundaryAnalysisReport:
        """
        Runs satisfaction search and analyzes theorem boundaries.
        """

        satisfaction_report = SatisfactionSearchRunner().run(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        return self.analyze_cases(satisfaction_report.cases)


if __name__ == "__main__":
    report = TheoremBoundaryAnalyzer().run()

    print(report.describe())

    print()
    print("Sample boundary cases:")
    for classification in report.classifications[:5]:
        print()
        print(classification.describe())
