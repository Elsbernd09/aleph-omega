"""
Bridge composition for the Project ℵω rigor track.

This module defines composition of finite bridges.

If F: U -> V and G: V -> W, then the composite bridge G ∘ F maps each
source statement s in U to G(F(s)) in W whenever both translations are defined.

This is the first step toward treating finite logical universes and bridges as
a category-like structure.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.finite_universe import FiniteLogicalUniverse, FiniteStatement


class CompositionStatus(str, Enum):
    """
    Status of bridge composition.
    """

    COMPOSABLE = "composable"
    NOT_COMPOSABLE = "not_composable"


@dataclass(frozen=True)
class BridgeCompositionResult:
    """
    Result of composing two bridges.
    """

    first: FiniteBridge
    second: FiniteBridge
    status: CompositionStatus
    composite: Optional[FiniteBridge]
    explanation: str = ""

    def is_composable(self) -> bool:
        """
        Returns whether the two bridges are composable.
        """

        return self.status == CompositionStatus.COMPOSABLE

    def has_composite(self) -> bool:
        """
        Returns whether a composite bridge exists.
        """

        return self.composite is not None

    def describe(self) -> str:
        """
        Returns a readable composition result.
        """

        composite_name = self.composite.name if self.composite is not None else "none"

        return (
            f"BridgeCompositionResult\n"
            f"First bridge: {self.first.name}\n"
            f"Second bridge: {self.second.name}\n"
            f"Status: {self.status.value}\n"
            f"Composite: {composite_name}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


def bridges_are_composable(first: FiniteBridge, second: FiniteBridge) -> bool:
    """
    Checks whether two bridges are composable.

    first: U -> V
    second: V -> W

    They are composable exactly when first.target == second.source.
    """

    return first.target == second.source


def compose_bridges(
    first: FiniteBridge,
    second: FiniteBridge,
    name: str = "",
) -> BridgeCompositionResult:
    """
    Composes two finite bridges.

    The composite is second ∘ first.

    If first maps s to t, and second maps t to r, then the composite maps
    s to r.

    If either leg is undefined for a statement, the composite is undefined
    for that statement.
    """

    if not bridges_are_composable(first, second):
        return BridgeCompositionResult(
            first=first,
            second=second,
            status=CompositionStatus.NOT_COMPOSABLE,
            composite=None,
            explanation=(
                "The target universe of the first bridge is not the source universe "
                "of the second bridge."
            ),
        )

    composite_mapping: Dict[FiniteStatement, FiniteStatement] = {}

    for source_statement in first.source.statements:
        middle_statement = first.mapping.get(source_statement)

        if middle_statement is None:
            continue

        target_statement = second.mapping.get(middle_statement)

        if target_statement is None:
            continue

        composite_mapping[source_statement] = target_statement

    composite = FiniteBridge(
        name=name or f"{second.name} ∘ {first.name}",
        source=first.source,
        target=second.target,
        mapping=composite_mapping,
        description=(
            "Composite bridge formed by applying the first bridge and then the second bridge."
        ),
    )

    return BridgeCompositionResult(
        first=first,
        second=second,
        status=CompositionStatus.COMPOSABLE,
        composite=composite,
        explanation="The bridges are composable and a composite bridge was constructed.",
    )


def compose_chain(
    bridges: Tuple[FiniteBridge, ...],
    name: str = "",
) -> Optional[FiniteBridge]:
    """
    Composes a chain of bridges from left to right.

    For bridges (F, G, H), this returns H ∘ G ∘ F when all adjacent bridges
    are composable.

    Returns None if the chain is empty or if some adjacent pair is not composable.
    """

    if not bridges:
        return None

    current = bridges[0]

    for next_bridge in bridges[1:]:
        result = compose_bridges(current, next_bridge)

        if not result.has_composite():
            return None

        current = result.composite

    if name:
        current = FiniteBridge(
            name=name,
            source=current.source,
            target=current.target,
            mapping=current.mapping,
            description=current.description,
        )

    return current


def same_bridge_mapping(left: FiniteBridge, right: FiniteBridge) -> bool:
    """
    Checks whether two bridges have the same source, target, and mapping.
    """

    return (
        left.source == right.source
        and left.target == right.target
        and left.mapping == right.mapping
    )


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
    from src.rigor.finite_universe import classical_finite_universe

    universe = classical_finite_universe()

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    result = compose_bridges(first, second)

    print(result.describe())

    if result.composite is not None:
        print()
        print(result.composite.describe())
