"""
Failure taxonomy for Project Aleph-Omega.

This module classifies how finite semantic bridge systems can fail.

The point is not only to show theorem success, but to describe the boundary
between preservation and distortion.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge_case_generator import BridgeCase
from src.rigor.satisfaction_search import SatisfactionSearchCase


class FailureKind(str, Enum):
    """
    Kinds of semantic or structural failure.
    """

    NO_FAILURE = "no_failure"
    UNDEFINED_TRANSLATION = "undefined_translation"
    TARGET_NOT_SATISFIED = "target_not_satisfied"
    FEATURE_MISMATCH = "feature_mismatch"
    PARTIAL_BRIDGE_FAILURE = "partial_bridge_failure"
    COLLAPSE_DISTORTION = "collapse_distortion"
    MULTIPLE_FAILURES = "multiple_failures"


@dataclass(frozen=True)
class FailureClassification:
    """
    Classification of one generated failure case.
    """

    kind: FailureKind
    bridge_name: str
    bridge_kind: str
    explanation: str

    def is_failure(self) -> bool:
        """
        Returns whether this classification describes a real failure.
        """

        return self.kind != FailureKind.NO_FAILURE

    def describe(self) -> str:
        """
        Returns a readable classification.
        """

        return (
            f"FailureClassification\n"
            f"Kind: {self.kind.value}\n"
            f"Bridge: {self.bridge_name}\n"
            f"Bridge kind: {self.bridge_kind}\n"
            f"Failure: {self.is_failure()}\n"
            f"Explanation: {self.explanation}"
        )


class FailureClassifier:
    """
    Classifies failures in bridge and satisfaction search cases.
    """

    def classify_bridge_case(self, bridge_case: BridgeCase) -> FailureClassification:
        """
        Classifies structural bridge failure.
        """

        has_partial_failure = not bridge_case.bridge.is_total()
        has_feature_mismatch = bridge_case.bridge.has_feature_mismatch()

        if has_partial_failure and has_feature_mismatch:
            kind = FailureKind.MULTIPLE_FAILURES
            explanation = "The bridge is partial and also contains feature mismatch."
        elif has_partial_failure:
            kind = FailureKind.PARTIAL_BRIDGE_FAILURE
            explanation = "The bridge does not define translations for every source statement."
        elif has_feature_mismatch:
            kind = FailureKind.FEATURE_MISMATCH
            explanation = "The bridge maps at least one statement to a target with incompatible semantic features."
        else:
            kind = FailureKind.NO_FAILURE
            explanation = "No structural bridge failure detected."

        return FailureClassification(
            kind=kind,
            bridge_name=bridge_case.bridge.name,
            bridge_kind=bridge_case.kind.value,
            explanation=explanation,
        )

    def classify_satisfaction_case(
        self,
        search_case: SatisfactionSearchCase,
    ) -> FailureClassification:
        """
        Classifies satisfaction-level failure.
        """

        if not search_case.has_distortion():
            return FailureClassification(
                kind=FailureKind.NO_FAILURE,
                bridge_name=search_case.bridge_case.bridge.name,
                bridge_kind=search_case.bridge_case.kind.value,
                explanation="Satisfaction is preserved in this generated case.",
            )

        bridge = search_case.bridge_case.bridge

        if not bridge.is_total():
            return FailureClassification(
                kind=FailureKind.UNDEFINED_TRANSLATION,
                bridge_name=bridge.name,
                bridge_kind=search_case.bridge_case.kind.value,
                explanation="A satisfied source statement has no defined target translation.",
            )

        if bridge.has_feature_mismatch():
            return FailureClassification(
                kind=FailureKind.FEATURE_MISMATCH,
                bridge_name=bridge.name,
                bridge_kind=search_case.bridge_case.kind.value,
                explanation="Satisfaction distortion occurs together with semantic feature mismatch.",
            )

        if search_case.bridge_case.kind.value == "collapse":
            return FailureClassification(
                kind=FailureKind.COLLAPSE_DISTORTION,
                bridge_name=bridge.name,
                bridge_kind=search_case.bridge_case.kind.value,
                explanation="A collapse bridge identifies source statements in a way that can lose satisfaction.",
            )

        return FailureClassification(
            kind=FailureKind.TARGET_NOT_SATISFIED,
            bridge_name=bridge.name,
            bridge_kind=search_case.bridge_case.kind.value,
            explanation="A satisfied source statement translates to a target statement that is not satisfied.",
        )

    def classify_many_satisfaction_cases(
        self,
        cases: Tuple[SatisfactionSearchCase, ...],
    ) -> Tuple[FailureClassification, ...]:
        """
        Classifies many satisfaction search cases.
        """

        return tuple(self.classify_satisfaction_case(case) for case in cases)


if __name__ == "__main__":
    from src.rigor.finite_universe import SemanticFeature
    from src.rigor.satisfaction_search import SatisfactionSearchRunner

    report = SatisfactionSearchRunner().run(
        features=(
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size=1,
    )

    classifier = FailureClassifier()
    classifications = classifier.classify_many_satisfaction_cases(report.cases)

    failure_cases = [item for item in classifications if item.is_failure()]

    print(f"Classified cases: {len(classifications)}")
    print(f"Failures: {len(failure_cases)}")

    for item in failure_cases[:5]:
        print()
        print(item.describe())
