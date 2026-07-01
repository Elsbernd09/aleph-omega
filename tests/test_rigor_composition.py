"""
Tests for bridge composition in the Project ℵω rigor track.
"""

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.composition import (
    BridgeCompositionResult,
    CompositionStatus,
    bridges_are_composable,
    compose_bridges,
    compose_chain,
    same_bridge_mapping,
)
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
)


def test_identity_bridges_are_composable():
    universe = classical_finite_universe()

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    assert bridges_are_composable(first, second)

    result = compose_bridges(first, second)

    assert isinstance(result, BridgeCompositionResult)
    assert result.status == CompositionStatus.COMPOSABLE
    assert result.has_composite()
    assert result.composite is not None
    assert result.composite.is_total()
    assert same_bridge_mapping(result.composite, first)


def test_noncomposable_bridges_fail():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    first = identity_bridge(classical)
    second = identity_bridge(modal)

    result = compose_bridges(first, second)

    assert not bridges_are_composable(first, second)
    assert result.status == CompositionStatus.NOT_COMPOSABLE
    assert not result.has_composite()
    assert result.composite is None


def test_collapse_after_identity_equals_collapse():
    source = modal_finite_universe()
    target = classical_finite_universe()

    identity = identity_bridge(source)

    collapse = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    result = compose_bridges(identity, collapse)

    assert result.has_composite()
    assert result.composite is not None
    assert same_bridge_mapping(result.composite, collapse)


def test_identity_after_collapse_equals_collapse():
    source = modal_finite_universe()
    target = classical_finite_universe()

    collapse = collapse_bridge(
        name="Modal to Classical Collapse",
        source=source,
        target=target,
    )

    identity = identity_bridge(target)

    result = compose_bridges(collapse, identity)

    assert result.has_composite()
    assert result.composite is not None
    assert same_bridge_mapping(result.composite, collapse)


def test_partial_composition_can_be_partial():
    source_statement = FiniteStatement.from_features(
        name="source_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    middle_statement = FiniteStatement.from_features(
        name="middle_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    target_statement = FiniteStatement.from_features(
        name="target_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = FiniteLogicalUniverse.build(
        name="Source",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[source_statement],
    )

    middle = FiniteLogicalUniverse.build(
        name="Middle",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[middle_statement],
    )

    target = FiniteLogicalUniverse.build(
        name="Target",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[target_statement],
    )

    first = FiniteBridge(
        name="First",
        source=source,
        target=middle,
        mapping={source_statement: middle_statement},
    )

    second = FiniteBridge(
        name="Second Empty",
        source=middle,
        target=target,
        mapping={},
    )

    result = compose_bridges(first, second)

    assert result.has_composite()
    assert result.composite is not None
    assert not result.composite.is_total()
    assert result.composite.distortion_count() == 1


def test_compose_chain_identity_three_times():
    universe = classical_finite_universe()

    first = identity_bridge(universe)
    second = identity_bridge(universe)
    third = identity_bridge(universe)

    composite = compose_chain((first, second, third), name="Triple Identity")

    assert composite is not None
    assert composite.name == "Triple Identity"
    assert same_bridge_mapping(composite, first)


def test_compose_chain_returns_none_for_bad_chain():
    classical = classical_finite_universe()
    modal = modal_finite_universe()

    first = identity_bridge(classical)
    second = identity_bridge(modal)

    composite = compose_chain((first, second))

    assert composite is None


def test_composition_describe():
    universe = classical_finite_universe()

    result = compose_bridges(
        identity_bridge(universe),
        identity_bridge(universe),
    )

    assert "BridgeCompositionResult" in result.describe()
