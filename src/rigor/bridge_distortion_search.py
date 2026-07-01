"""
Bridge Distortion Theorem stress search.

This module stress-tests the finite Bridge Distortion Theorem against richer
generated bridge cases.

It uses the bridge case generator from Phase 14B and checks whether any
generated bridge violates the theorem implication.
"""

from dataclasses import dataclass
from typing import Tuple

from src.rigor.bridge_case_generator import BridgeCase, BridgeCaseGenerator, BridgeCaseKind
from src.rigor.finite_universe import SemanticFeature
from src.rigor.model_search import FiniteModelGenerator
from src.rigor.theorem import BridgeDistortionTheorem, TheoremCheck, TheoremStatus


@dataclass(frozen=True)
class BridgeDistortionSearchCase:
    """
    One bridge distortion theorem search case.
    """

    bridge_case: BridgeCase
    theorem_check: TheoremCheck

    def is_counterexample(self) -> bool:
        """
        Returns whether this case violates the theorem.
        """

        return self.theorem_check.status == TheoremStatus.FAILED_FOR_INSTANCE

    def is_nonvacuous(self) -> bool:
        """
        Returns whether this is a nonvacuous verified theorem instance.
        """

        return self.theorem_check.is_nonvacuous_verification()

    def is_vacuous(self) -> bool:
        """
        Returns whether this is a vacuous theorem instance.
        """

        return self.theorem_check.status == TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE

    def describe(self) -> str:
        """
        Returns a readable case description.
        """

        return (
            f"BridgeDistortionSearchCase\n"
            f"Bridge kind: {self.bridge_case.kind.value}\n"
            f"Bridge: {self.bridge_case.bridge.name}\n"
            f"Theorem status: {self.theorem_check.status.value}\n"
            f"Counterexample: {self.is_counterexample()}\n"
            f"Nonvacuous: {self.is_nonvacuous()}\n"
            f"Vacuous: {self.is_vacuous()}"
        )


@dataclass(frozen=True)
class BridgeDistortionSearchReport:
    """
    Report for Bridge Distortion Theorem stress search.
    """

    cases: Tuple[BridgeDistortionSearchCase, ...]

    def case_count(self) -> int:
        """
        Counts generated theorem-search cases.
        """

        return len(self.cases)

    def counterexamples(self) -> Tuple[BridgeDistortionSearchCase, ...]:
        """
        Returns all counterexamples.
        """

        return tuple(case for case in self.cases if case.is_counterexample())

    def nonvacuous_instances(self) -> Tuple[BridgeDistortionSearchCase, ...]:
        """
        Returns all nonvacuous verified theorem instances.
        """

        return tuple(case for case in self.cases if case.is_nonvacuous())

    def vacuous_instances(self) -> Tuple[BridgeDistortionSearchCase, ...]:
        """
        Returns all vacuous theorem instances.
        """

        return tuple(case for case in self.cases if case.is_vacuous())

    def cases_by_kind(self, kind: BridgeCaseKind) -> Tuple[BridgeDistortionSearchCase, ...]:
        """
        Returns cases of a particular bridge kind.
        """

        return tuple(case for case in self.cases if case.bridge_case.kind == kind)

    def theorem_survived_search(self) -> bool:
        """
        Returns whether the theorem survived all generated cases.
        """

        return len(self.counterexamples()) == 0

    def describe(self) -> str:
        """
        Returns a readable search report.
        """

        return (
            f"BridgeDistortionSearchReport\n"
            f"Cases: {self.case_count()}\n"
            f"Nonvacuous instances: {len(self.nonvacuous_instances())}\n"
            f"Vacuous instances: {len(self.vacuous_instances())}\n"
            f"Counterexamples: {len(self.counterexamples())}\n"
            f"Theorem survived search: {self.theorem_survived_search()}"
        )


class BridgeDistortionSearchRunner:
    """
    Runs generated finite stress tests for the Bridge Distortion Theorem.
    """

    def __init__(self) -> None:
        self.model_generator = FiniteModelGenerator()
        self.bridge_case_generator = BridgeCaseGenerator()
        self.theorem = BridgeDistortionTheorem()

    def run(
        self,
        features: Tuple[SemanticFeature, ...] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ),
        max_feature_set_size: int = 2,
    ) -> BridgeDistortionSearchReport:
        """
        Runs the bridge distortion stress search.
        """

        universe_cases = self.model_generator.generate_universe_cases(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        bridge_cases = self.bridge_case_generator.generate_cases(universe_cases)

        search_cases = []

        for bridge_case in bridge_cases:
            theorem_check = self.theorem.check(bridge_case.bridge)

            search_cases.append(
                BridgeDistortionSearchCase(
                    bridge_case=bridge_case,
                    theorem_check=theorem_check,
                )
            )

        return BridgeDistortionSearchReport(cases=tuple(search_cases))


if __name__ == "__main__":
    report = BridgeDistortionSearchRunner().run()

    print(report.describe())
    print()

    print("Cases by bridge kind:")
    for kind in BridgeCaseKind:
        print(f"- {kind.value}: {len(report.cases_by_kind(kind))}")

    print()
    print("Sample nonvacuous instances:")
    for case in report.nonvacuous_instances()[:5]:
        print("- " + case.bridge_case.bridge.name)
