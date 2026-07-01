"""
Tests for finite universe category structure.
"""

from src.rigor.bridge import collapse_bridge, identity_bridge
from src.rigor.category import (
    FiniteUniverseCategory,
    starter_finite_universe_category,
)
from src.rigor.finite_universe import (
    classical_finite_universe,
    modal_finite_universe,
)


def test_starter_category_exists():
    category = starter_finite_universe_category()

    assert isinstance(category, FiniteUniverseCategory)
    assert category.object_count() == 2
    assert category.morphism_count() == 3
    assert category.identity_laws_hold()
    assert "Starter Finite Universe Category" in category.describe()


def test_category_has_objects_and_morphisms():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=modal,
        target=classical,
    )

    category = FiniteUniverseCategory.build(
        name="Test Category",
        objects=(classical, modal),
        morphisms=(
            identity_bridge(classical),
            identity_bridge(modal),
            bridge,
        ),
    )

    assert category.has_object(classical)
    assert category.has_object(modal)
    assert category.has_morphism(bridge)


def test_identities_created_for_all_objects():
    category = starter_finite_universe_category()

    identities = category.identities()

    assert len(identities) == category.object_count()
    assert all(identity.is_total() for identity in identities)


def test_morphisms_from_and_to():
    category = starter_finite_universe_category()

    classical = next(
        universe for universe in category.objects
        if universe.name == "Finite Classical Universe"
    )

    modal = next(
        universe for universe in category.objects
        if universe.name == "Finite Modal Universe"
    )

    from_modal = category.morphisms_from(modal)
    to_classical = category.morphisms_to(classical)

    assert len(from_modal) >= 2
    assert len(to_classical) >= 2


def test_composable_pairs_and_composite_closure():
    category = starter_finite_universe_category()

    pairs = category.composable_pairs()
    composites = category.composite_closure()

    assert len(pairs) >= 3
    assert len(composites) == len(pairs)
    assert all(composite.source in category.objects for composite in composites)
    assert all(composite.target in category.objects for composite in composites)


def test_identity_law_for_modal_to_classical_bridge():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Collapse",
        source=modal,
        target=classical,
    )

    category = FiniteUniverseCategory.build(
        name="Identity Law Test Category",
        objects=(classical, modal),
        morphisms=(
            identity_bridge(classical),
            identity_bridge(modal),
            bridge,
        ),
    )

    assert category.identity_law_holds_for(bridge)


def test_custom_category_description():
    category = starter_finite_universe_category()

    description = category.describe()

    assert "FiniteUniverseCategory" in description
    assert "Object count" in description
    assert "Morphism count" in description
    assert "Identity laws hold" in description
