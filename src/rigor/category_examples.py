"""
Categorical examples for the Project ℵω rigor track.

These examples show how finite logical universes and bridges behave like a
small category-like structure with identities and associative composition.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.associativity import AssociativityAnalyzer, AssociativityReport
from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.category import FiniteUniverseCategory, starter_finite_universe_category
from src.rigor.composition import compose_chain
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)
from src.rigor.identity_laws import IdentityLawAnalyzer, IdentityLawReport


class CategoryExampleKind(str, Enum):
    """
    Types of categorical examples.
    """

    STARTER_CATEGORY = "starter_category"
    IDENTITY_LAW = "identity_law"
    ASSOCIATIVITY = "associativity"
    COMPOSITION_CHAIN = "composition_chain"
    COLLAPSE_STRUCTURE = "collapse_structure"


@dataclass(frozen=True)
class CategoryExample:
    """
    A documented category-style example.
    """

    name: str
    kind: CategoryExampleKind
    category: FiniteUniverseCategory
    identity_report: IdentityLawReport
    associativity_report: AssociativityReport
    explanation: str

    def is_well_behaved(self) -> bool:
        """
        Returns whether identity and associativity checks pass.
        """

        return self.identity_report.holds() and self.associativity_report.holds()

    def describe(self) -> str:
        """
        Returns a readable example description.
        """

        return (
            f"CategoryExample: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Category: {self.category.name}\n"
            f"Identity laws hold: {self.identity_report.holds()}\n"
            f"Associativity holds: {self.associativity_report.holds()}\n"
            f"Well behaved: {self.is_well_behaved()}\n"
            f"Explanation: {self.explanation}"
        )


def starter_category_example() -> CategoryExample:
    """
    Basic example using the starter finite universe category.
    """

    category = starter_finite_universe_category()

    return CategoryExample(
        name="Starter Finite Universe Category Example",
        kind=CategoryExampleKind.STARTER_CATEGORY,
        category=category,
        identity_report=IdentityLawAnalyzer().check_category(category),
        associativity_report=AssociativityAnalyzer().check_category(category),
        explanation=(
            "The starter category contains classical and modal finite universes, "
            "identity bridges, and a modal-to-classical collapse bridge."
        ),
    )


def identity_law_example() -> CategoryExample:
    """
    Example focused on identity laws.
    """

    classical = classical_finite_universe()
    category = FiniteUniverseCategory.build(
        name="Classical Identity Category",
        objects=(classical,),
        morphisms=(identity_bridge(classical),),
        description="A one-object category-like structure with only identity.",
    )

    return CategoryExample(
        name="Classical Identity Law Example",
        kind=CategoryExampleKind.IDENTITY_LAW,
        category=category,
        identity_report=IdentityLawAnalyzer().check_category(category),
        associativity_report=AssociativityAnalyzer().check_category(category),
        explanation=(
            "A one-object identity-only structure satisfies identity and associativity "
            "in the simplest possible way."
        ),
    )


def collapse_structure_example() -> CategoryExample:
    """
    Example with a collapse bridge from modal to classical.
    """

    modal = modal_finite_universe()
    classical = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=modal,
        target=classical,
    )

    category = FiniteUniverseCategory.build(
        name="Collapse Structure Category",
        objects=(modal, classical),
        morphisms=(
            identity_bridge(modal),
            identity_bridge(classical),
            bridge,
        ),
        description="A two-object structure with a modal-to-classical collapse bridge.",
    )

    return CategoryExample(
        name="Collapse Structure Example",
        kind=CategoryExampleKind.COLLAPSE_STRUCTURE,
        category=category,
        identity_report=IdentityLawAnalyzer().check_category(category),
        associativity_report=AssociativityAnalyzer().check_category(category),
        explanation=(
            "This example shows that the collapse bridge still behaves correctly "
            "with identity and associative composition, even though it may distort "
            "semantic features."
        ),
    )


def custom_chain_category_example() -> CategoryExample:
    """
    Example with a composable chain A -> B -> C -> D.
    """

    statement_a = FiniteStatement.from_features(
        name="a",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )
    statement_b = FiniteStatement.from_features(
        name="b",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )
    statement_c = FiniteStatement.from_features(
        name="c",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )
    statement_d = FiniteStatement.from_features(
        name="d",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    universe_a = FiniteLogicalUniverse.build(
        name="Chain Universe A",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_a],
    )
    universe_b = FiniteLogicalUniverse.build(
        name="Chain Universe B",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_b],
    )
    universe_c = FiniteLogicalUniverse.build(
        name="Chain Universe C",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_c],
    )
    universe_d = FiniteLogicalUniverse.build(
        name="Chain Universe D",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_d],
    )

    first = FiniteBridge(
        name="f: A to B",
        source=universe_a,
        target=universe_b,
        mapping={statement_a: statement_b},
    )
    second = FiniteBridge(
        name="g: B to C",
        source=universe_b,
        target=universe_c,
        mapping={statement_b: statement_c},
    )
    third = FiniteBridge(
        name="h: C to D",
        source=universe_c,
        target=universe_d,
        mapping={statement_c: statement_d},
    )

    composite = compose_chain(
        bridges=(first, second, third),
        name="h ∘ g ∘ f",
    )

    morphisms = (
        first,
        second,
        third,
        identity_bridge(universe_a),
        identity_bridge(universe_b),
        identity_bridge(universe_c),
        identity_bridge(universe_d),
    )

    if composite is not None:
        morphisms = morphisms + (composite,)

    category = FiniteUniverseCategory.build(
        name="Custom Chain Category",
        objects=(universe_a, universe_b, universe_c, universe_d),
        morphisms=morphisms,
        description="A chain category-like structure with explicit composite.",
    )

    return CategoryExample(
        name="Custom Composition Chain Example",
        kind=CategoryExampleKind.COMPOSITION_CHAIN,
        category=category,
        identity_report=IdentityLawAnalyzer().check_category(category),
        associativity_report=AssociativityAnalyzer().check_category(category),
        explanation=(
            "This example demonstrates a finite chain of bridges and the composite "
            "h ∘ g ∘ f."
        ),
    )


def standard_category_examples() -> Tuple[CategoryExample, ...]:
    """
    Returns all standard category examples.
    """

    return (
        starter_category_example(),
        identity_law_example(),
        collapse_structure_example(),
        custom_chain_category_example(),
    )


if __name__ == "__main__":
    for example in standard_category_examples():
        print(example.describe())
        print()
