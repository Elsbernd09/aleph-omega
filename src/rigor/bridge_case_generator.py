"""
Bridge case generator for finite theorem stress testing.

This module generates multiple kinds of finite bridge test cases:
- identity bridges,
- collapse bridges,
- empty partial bridges,
- same-feature bridges,
- feature-mismatch bridges.

The goal is to stress-test theorem behavior beyond a small number of hand-built examples.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import FiniteLogicalUniverse, FiniteStatement
from src.rigor.model_search import GeneratedUniverseCase


class BridgeCaseKind(str, Enum):
    """
    Kinds of generated bridge cases.
    """

    IDENTITY = "identity"
    COLLAPSE = "collapse"
    EMPTY_PARTIAL = "empty_partial"
    SAME_FEATURE = "same_feature"


@dataclass(frozen=True)
class BridgeCase:
    """
    A generated bridge case with metadata.
    """

    kind: BridgeCaseKind
    source: FiniteLogicalUniverse
    target: FiniteLogicalUniverse
    bridge: FiniteBridge
    explanation: str = ""

    def is_total(self) -> bool:
        """
        Returns whether the bridge is total.
        """

        return self.bridge.is_total()

    def has_feature_mismatch(self) -> bool:
        """
        Returns whether the bridge has feature mismatch.
        """

        return self.bridge.has_feature_mismatch()

    def describe(self) -> str:
        """
        Returns a readable bridge case description.
        """

        return (
            f"BridgeCase\n"
            f"Kind: {self.kind.value}\n"
            f"Source: {self.source.name}\n"
            f"Target: {self.target.name}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Total: {self.is_total()}\n"
            f"Feature mismatch: {self.has_feature_mismatch()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


class BridgeCaseGenerator:
    """
    Generates bridge cases from finite universe cases.
    """

    def identity_case(self, universe: FiniteLogicalUniverse) -> BridgeCase:
        """
        Generates an identity bridge case.
        """

        return BridgeCase(
            kind=BridgeCaseKind.IDENTITY,
            source=universe,
            target=universe,
            bridge=identity_bridge(universe),
            explanation="Identity bridge on one finite universe.",
        )

    def collapse_case(
        self,
        source: FiniteLogicalUniverse,
        target: FiniteLogicalUniverse,
    ) -> BridgeCase:
        """
        Generates a collapse bridge case.
        """

        return BridgeCase(
            kind=BridgeCaseKind.COLLAPSE,
            source=source,
            target=target,
            bridge=collapse_bridge(
                name=f"{source.name} to {target.name} Collapse",
                source=source,
                target=target,
            ),
            explanation="Total collapse bridge from source statements to a target statement.",
        )

    def empty_partial_case(
        self,
        source: FiniteLogicalUniverse,
        target: FiniteLogicalUniverse,
    ) -> BridgeCase:
        """
        Generates an empty partial bridge case.
        """

        return BridgeCase(
            kind=BridgeCaseKind.EMPTY_PARTIAL,
            source=source,
            target=target,
            bridge=FiniteBridge(
                name=f"{source.name} to {target.name} Empty Partial Bridge",
                source=source,
                target=target,
                mapping={},
                description="Empty partial bridge with no defined statement mappings.",
            ),
            explanation="Partial bridge with no statement translations.",
        )

    def same_feature_case(
        self,
        source: FiniteLogicalUniverse,
        target: FiniteLogicalUniverse,
    ) -> BridgeCase:
        """
        Generates a bridge that maps statements requiring the same feature when possible.

        If no same-feature matches exist, the bridge may be partial.
        """

        mapping = {}

        target_statements = sorted(target.statements, key=lambda item: item.name)

        for source_statement in sorted(source.statements, key=lambda item: item.name):
            match = self._find_same_feature_statement(
                source_statement=source_statement,
                target_statements=target_statements,
            )

            if match is not None:
                mapping[source_statement] = match

        bridge = FiniteBridge(
            name=f"{source.name} to {target.name} Same-Feature Bridge",
            source=source,
            target=target,
            mapping=mapping,
            description="Bridge mapping source statements to target statements with matching required features.",
        )

        return BridgeCase(
            kind=BridgeCaseKind.SAME_FEATURE,
            source=source,
            target=target,
            bridge=bridge,
            explanation="Bridge attempts to preserve required semantic feature sets exactly.",
        )

    @staticmethod
    def _find_same_feature_statement(
        source_statement: FiniteStatement,
        target_statements: Tuple[FiniteStatement, ...],
    ) -> FiniteStatement:
        """
        Finds a target statement with exactly the same required features.
        """

        for target_statement in target_statements:
            if target_statement.required_features == source_statement.required_features:
                return target_statement

        return None

    def generate_cases_for_pair(
        self,
        source: FiniteLogicalUniverse,
        target: FiniteLogicalUniverse,
    ) -> Tuple[BridgeCase, ...]:
        """
        Generates bridge cases for one source-target universe pair.
        """

        cases = [
            self.collapse_case(source, target),
            self.empty_partial_case(source, target),
            self.same_feature_case(source, target),
        ]

        if source == target:
            cases.insert(0, self.identity_case(source))

        return tuple(cases)

    def generate_cases(
        self,
        universe_cases: Tuple[GeneratedUniverseCase, ...],
    ) -> Tuple[BridgeCase, ...]:
        """
        Generates bridge cases for all source-target pairs.
        """

        cases = []

        for source_case in universe_cases:
            for target_case in universe_cases:
                cases.extend(
                    self.generate_cases_for_pair(
                        source=source_case.universe,
                        target=target_case.universe,
                    )
                )

        return tuple(cases)


if __name__ == "__main__":
    from src.rigor.finite_universe import SemanticFeature
    from src.rigor.model_search import FiniteModelGenerator

    universe_cases = FiniteModelGenerator().generate_universe_cases(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=1,
    )

    cases = BridgeCaseGenerator().generate_cases(universe_cases)

    print(f"Generated bridge cases: {len(cases)}")
    for case in cases[:8]:
        print()
        print(case.describe())
