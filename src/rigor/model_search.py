"""
Finite model search for the Project ℵω rigor track.

This module generates small finite logical universes and bridge cases for
stress-testing theorem claims.

The goal is not to search all possible mathematics. The goal is to test the
finite Project ℵω theorem layer against many small generated cases.
"""

from dataclasses import dataclass
from itertools import combinations
from typing import FrozenSet, Iterable, Tuple

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
)
from src.rigor.theorem import BridgeDistortionTheorem, TheoremCheck, TheoremStatus


@dataclass(frozen=True)
class GeneratedUniverseCase:
    """
    A generated finite logical universe case.
    """

    universe: FiniteLogicalUniverse
    feature_set: FrozenSet[SemanticFeature]
    statement_count: int

    def describe(self) -> str:
        """
        Returns a readable generated case description.
        """

        features = ", ".join(sorted(feature.value for feature in self.feature_set))

        return (
            f"GeneratedUniverseCase\n"
            f"Universe: {self.universe.name}\n"
            f"Features: {features or 'none'}\n"
            f"Statement count: {self.statement_count}"
        )


@dataclass(frozen=True)
class GeneratedBridgeCase:
    """
    A generated bridge case.
    """

    source: FiniteLogicalUniverse
    target: FiniteLogicalUniverse
    bridge: FiniteBridge
    theorem_check: TheoremCheck

    def is_counterexample_to_bridge_distortion_theorem(self) -> bool:
        """
        Returns whether this generated case violates the theorem implication.
        """

        return self.theorem_check.status == TheoremStatus.FAILED_FOR_INSTANCE

    def is_nonvacuous_theorem_instance(self) -> bool:
        """
        Returns whether this is a nonvacuous verified theorem instance.
        """

        return self.theorem_check.is_nonvacuous_verification()

    def describe(self) -> str:
        """
        Returns a readable bridge case description.
        """

        return (
            f"GeneratedBridgeCase\n"
            f"Source: {self.source.name}\n"
            f"Target: {self.target.name}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Theorem status: {self.theorem_check.status.value}\n"
            f"Counterexample: {self.is_counterexample_to_bridge_distortion_theorem()}"
        )


@dataclass(frozen=True)
class ModelSearchReport:
    """
    Report for finite model search.
    """

    universe_cases: Tuple[GeneratedUniverseCase, ...]
    bridge_cases: Tuple[GeneratedBridgeCase, ...]

    def universe_count(self) -> int:
        """
        Counts generated universes.
        """

        return len(self.universe_cases)

    def bridge_case_count(self) -> int:
        """
        Counts generated bridge cases.
        """

        return len(self.bridge_cases)

    def counterexamples(self) -> Tuple[GeneratedBridgeCase, ...]:
        """
        Returns theorem counterexamples.
        """

        return tuple(
            case for case in self.bridge_cases
            if case.is_counterexample_to_bridge_distortion_theorem()
        )

    def nonvacuous_instances(self) -> Tuple[GeneratedBridgeCase, ...]:
        """
        Returns nonvacuous verified theorem instances.
        """

        return tuple(
            case for case in self.bridge_cases
            if case.is_nonvacuous_theorem_instance()
        )

    def vacuous_instances(self) -> Tuple[GeneratedBridgeCase, ...]:
        """
        Returns vacuous theorem instances.
        """

        return tuple(
            case for case in self.bridge_cases
            if case.theorem_check.status == TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE
        )

    def theorem_survived_search(self) -> bool:
        """
        Returns whether no counterexamples were found.
        """

        return len(self.counterexamples()) == 0

    def describe(self) -> str:
        """
        Returns a readable model-search report.
        """

        return (
            f"ModelSearchReport\n"
            f"Universe cases: {self.universe_count()}\n"
            f"Bridge cases: {self.bridge_case_count()}\n"
            f"Nonvacuous theorem instances: {len(self.nonvacuous_instances())}\n"
            f"Vacuous theorem instances: {len(self.vacuous_instances())}\n"
            f"Counterexamples found: {len(self.counterexamples())}\n"
            f"Theorem survived search: {self.theorem_survived_search()}"
        )


class FiniteModelGenerator:
    """
    Generates small finite universes and bridge cases.
    """

    def feature_subsets(
        self,
        features: Iterable[SemanticFeature],
        max_size: int,
    ) -> Tuple[FrozenSet[SemanticFeature], ...]:
        """
        Generates nonempty feature subsets up to max_size.
        """

        feature_list = tuple(features)
        subsets = []

        for size in range(1, max_size + 1):
            for combo in combinations(feature_list, size):
                subsets.append(frozenset(combo))

        return tuple(subsets)

    def universe_from_features(
        self,
        name: str,
        features: FrozenSet[SemanticFeature],
    ) -> FiniteLogicalUniverse:
        """
        Builds a finite universe whose statements each require one supported feature.
        """

        statements = []

        for feature in sorted(features, key=lambda item: item.value):
            statements.append(
                FiniteStatement.from_features(
                    name=f"{name.lower().replace(' ', '_')}_{feature.value}_statement",
                    features=[feature],
                    informal_reading=f"A generated statement requiring {feature.value}.",
                )
            )

        return FiniteLogicalUniverse.build(
            name=name,
            supported_features=features,
            statements=statements,
            description="Generated universe for finite model search.",
        )

    def generate_universe_cases(
        self,
        features: Iterable[SemanticFeature],
        max_feature_set_size: int = 2,
    ) -> Tuple[GeneratedUniverseCase, ...]:
        """
        Generates finite universe cases from feature subsets.
        """

        cases = []

        for index, feature_set in enumerate(
            self.feature_subsets(features, max_feature_set_size),
            start=1,
        ):
            universe = self.universe_from_features(
                name=f"Generated Universe {index}",
                features=feature_set,
            )

            cases.append(
                GeneratedUniverseCase(
                    universe=universe,
                    feature_set=feature_set,
                    statement_count=universe.statement_count(),
                )
            )

        return tuple(cases)

    def generate_bridge_cases(
        self,
        universe_cases: Tuple[GeneratedUniverseCase, ...],
    ) -> Tuple[GeneratedBridgeCase, ...]:
        """
        Generates bridge cases from universe pairs.

        For equal source/target universes, identity bridges are used.
        For different universes, collapse bridges are used.
        """

        theorem = BridgeDistortionTheorem()
        bridge_cases = []

        for source_case in universe_cases:
            for target_case in universe_cases:
                source = source_case.universe
                target = target_case.universe

                if source == target:
                    bridge = identity_bridge(source)
                else:
                    bridge = collapse_bridge(
                        name=f"{source.name} to {target.name} Collapse",
                        source=source,
                        target=target,
                    )

                theorem_check = theorem.check(bridge)

                bridge_cases.append(
                    GeneratedBridgeCase(
                        source=source,
                        target=target,
                        bridge=bridge,
                        theorem_check=theorem_check,
                    )
                )

        return tuple(bridge_cases)

    def run_bridge_distortion_search(
        self,
        features: Iterable[SemanticFeature] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ),
        max_feature_set_size: int = 2,
    ) -> ModelSearchReport:
        """
        Runs a finite model search for the Bridge Distortion Theorem.
        """

        universe_cases = self.generate_universe_cases(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        bridge_cases = self.generate_bridge_cases(universe_cases)

        return ModelSearchReport(
            universe_cases=universe_cases,
            bridge_cases=bridge_cases,
        )


if __name__ == "__main__":
    report = FiniteModelGenerator().run_bridge_distortion_search()

    print(report.describe())

    print()
    print("Sample nonvacuous instances:")
    for case in report.nonvacuous_instances()[:5]:
        print("- " + case.bridge.name)
