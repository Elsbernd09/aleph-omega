"""
Finite universe category for the Project ℵω rigor track.

This module organizes finite logical universes and finite bridges into a
category-like structure.

Objects:
- finite logical universes

Morphisms:
- finite bridges

Identity:
- identity bridge on each universe

Composition:
- bridge composition from src.rigor.composition

This is category-like because we are working with finite computational objects,
but the structure is designed to support identity and associativity checks.
"""

from dataclasses import dataclass, field
from typing import FrozenSet, Tuple

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.composition import compose_bridges, same_bridge_mapping
from src.rigor.finite_universe import FiniteLogicalUniverse


@dataclass(frozen=True)
class FiniteUniverseCategory:
    """
    A finite category-like structure of logical universes and bridges.
    """

    name: str
    objects: FrozenSet[FiniteLogicalUniverse] = field(default_factory=frozenset)
    morphisms: Tuple[FiniteBridge, ...] = field(default_factory=tuple)
    description: str = ""

    @staticmethod
    def build(
        name: str,
        objects: Tuple[FiniteLogicalUniverse, ...],
        morphisms: Tuple[FiniteBridge, ...],
        description: str = "",
    ) -> "FiniteUniverseCategory":
        """
        Builds a finite universe category.
        """

        return FiniteUniverseCategory(
            name=name,
            objects=frozenset(objects),
            morphisms=tuple(morphisms),
            description=description,
        )

    def object_count(self) -> int:
        """
        Counts objects.
        """

        return len(self.objects)

    def morphism_count(self) -> int:
        """
        Counts morphisms.
        """

        return len(self.morphisms)

    def has_object(self, universe: FiniteLogicalUniverse) -> bool:
        """
        Checks whether a universe is an object of the category.
        """

        return universe in self.objects

    def has_morphism(self, bridge: FiniteBridge) -> bool:
        """
        Checks whether a bridge is a morphism of the category.
        """

        return bridge in self.morphisms

    def identity_for(self, universe: FiniteLogicalUniverse) -> FiniteBridge:
        """
        Returns the identity bridge for a universe.
        """

        return identity_bridge(universe)

    def identities(self) -> Tuple[FiniteBridge, ...]:
        """
        Returns identity bridges for all objects.
        """

        return tuple(
            identity_bridge(universe)
            for universe in sorted(self.objects, key=lambda item: item.name)
        )

    def morphisms_from(
        self,
        source: FiniteLogicalUniverse,
    ) -> Tuple[FiniteBridge, ...]:
        """
        Returns morphisms with a given source.
        """

        return tuple(
            bridge
            for bridge in sorted(self.morphisms, key=lambda item: item.name)
            if bridge.source == source
        )

    def morphisms_to(
        self,
        target: FiniteLogicalUniverse,
    ) -> Tuple[FiniteBridge, ...]:
        """
        Returns morphisms with a given target.
        """

        return tuple(
            bridge
            for bridge in sorted(self.morphisms, key=lambda item: item.name)
            if bridge.target == target
        )

    def composable_pairs(self) -> Tuple[Tuple[FiniteBridge, FiniteBridge], ...]:
        """
        Returns all composable morphism pairs.

        A pair (f, g) is composable when f.target == g.source.
        The composite is g ∘ f.
        """

        pairs = []

        for first in self.morphisms:
            for second in self.morphisms:
                if first.target == second.source:
                    pairs.append((first, second))

        return tuple(
            sorted(
                pairs,
                key=lambda pair: (pair[0].name, pair[1].name),
            )
        )

    def composite_closure(self) -> Tuple[FiniteBridge, ...]:
        """
        Returns composites of all composable pairs.
        """

        composites = []

        for first, second in self.composable_pairs():
            result = compose_bridges(first, second)

            if result.composite is not None:
                composites.append(result.composite)

        return tuple(composites)

    def identity_law_holds_for(self, bridge: FiniteBridge) -> bool:
        """
        Checks left and right identity laws for one bridge.

        For f: A -> B:
        - f ∘ id_A = f
        - id_B ∘ f = f
        """

        left_identity = identity_bridge(bridge.source)
        right_identity = identity_bridge(bridge.target)

        left_result = compose_bridges(left_identity, bridge)
        right_result = compose_bridges(bridge, right_identity)

        return (
            left_result.composite is not None
            and right_result.composite is not None
            and same_bridge_mapping(left_result.composite, bridge)
            and same_bridge_mapping(right_result.composite, bridge)
        )

    def identity_laws_hold(self) -> bool:
        """
        Checks identity laws for every morphism.
        """

        return all(
            self.identity_law_holds_for(bridge)
            for bridge in self.morphisms
        )

    def describe(self) -> str:
        """
        Returns a readable category description.
        """

        return (
            f"FiniteUniverseCategory: {self.name}\n"
            f"Object count: {self.object_count()}\n"
            f"Morphism count: {self.morphism_count()}\n"
            f"Composable pair count: {len(self.composable_pairs())}\n"
            f"Identity laws hold: {self.identity_laws_hold()}\n"
            f"Description: {self.description or 'not provided'}"
        )


def starter_finite_universe_category() -> FiniteUniverseCategory:
    """
    Builds a small starter category with classical and modal universes.
    """

    from src.rigor.bridge import collapse_bridge
    from src.rigor.finite_universe import (
        classical_finite_universe,
        modal_finite_universe,
    )

    classical = classical_finite_universe()
    modal = modal_finite_universe()

    id_classical = identity_bridge(classical)
    id_modal = identity_bridge(modal)

    modal_to_classical = collapse_bridge(
        name="Modal to Classical Collapse",
        source=modal,
        target=classical,
    )

    return FiniteUniverseCategory.build(
        name="Starter Finite Universe Category",
        objects=(classical, modal),
        morphisms=(id_classical, id_modal, modal_to_classical),
        description=(
            "A small category-like structure with classical and modal finite universes."
        ),
    )


if __name__ == "__main__":
    category = starter_finite_universe_category()

    print(category.describe())

    print()
    print("Objects:")
    for universe in sorted(category.objects, key=lambda item: item.name):
        print(f"- {universe.name}")

    print()
    print("Morphisms:")
    for bridge in sorted(category.morphisms, key=lambda item: item.name):
        print(f"- {bridge.name}: {bridge.source.name} -> {bridge.target.name}")
