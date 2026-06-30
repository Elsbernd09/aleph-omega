"""
Unit tests for the Project ℵω toy logical universe layer.

These tests verify that the toy_topoi package can:
- define truth-value spaces,
- apply toy logical connectives,
- represent formal universes,
- load the universe library,
- compare universes.
"""

from src.toy_topoi.comparator import UniverseComparator
from src.toy_topoi.connectives import ToyConnectiveAlgebra
from src.toy_topoi.library import (
    classical_universe,
    find_universe_by_name,
    get_universe_names,
    paraconsistent_universe,
    standard_universes,
)
from src.toy_topoi.truth_values import (
    LogicFamily,
    TruthValue,
    classical_truth_space,
    many_valued_truth_space,
    modal_truth_space,
    paraconsistent_truth_space,
)
from src.toy_topoi.universe import FormalUniverse


def test_classical_truth_space():
    truth_space = classical_truth_space()

    assert truth_space.logic_family == LogicFamily.CLASSICAL
    assert truth_space.contains(TruthValue.TRUE)
    assert truth_space.contains(TruthValue.FALSE)
    assert not truth_space.contains(TruthValue.BOTH)
    assert truth_space.size() == 2
    assert not truth_space.supports_contradiction()


def test_paraconsistent_truth_space_supports_contradiction():
    truth_space = paraconsistent_truth_space()

    assert truth_space.logic_family == LogicFamily.PARACONSISTENT
    assert truth_space.contains(TruthValue.BOTH)
    assert truth_space.supports_contradiction()
    assert truth_space.supports_unknown()


def test_many_valued_truth_space_supports_unknown():
    truth_space = many_valued_truth_space()

    assert truth_space.contains(TruthValue.UNKNOWN)
    assert truth_space.supports_unknown()
    assert truth_space.supports_contradiction()


def test_modal_truth_space_supports_modal_status():
    truth_space = modal_truth_space()

    assert truth_space.supports_modal_status()
    assert truth_space.contains(TruthValue.NECESSARY)
    assert truth_space.contains(TruthValue.POSSIBLE)


def test_classical_connective_behavior():
    algebra = ToyConnectiveAlgebra(classical_truth_space())

    assert algebra.negate(TruthValue.TRUE).value == TruthValue.FALSE
    assert algebra.negate(TruthValue.FALSE).value == TruthValue.TRUE
    assert algebra.conjunction(TruthValue.TRUE, TruthValue.FALSE).value == TruthValue.FALSE
    assert algebra.disjunction(TruthValue.TRUE, TruthValue.FALSE).value == TruthValue.TRUE
    assert algebra.implication(TruthValue.TRUE, TruthValue.FALSE).value == TruthValue.FALSE


def test_paraconsistent_connective_behavior():
    algebra = ToyConnectiveAlgebra(paraconsistent_truth_space())

    assert algebra.negate(TruthValue.BOTH).value == TruthValue.BOTH
    assert algebra.conjunction(TruthValue.BOTH, TruthValue.TRUE).value == TruthValue.BOTH
    assert algebra.disjunction(TruthValue.BOTH, TruthValue.FALSE).value == TruthValue.BOTH


def test_universe_model_scores():
    universe = classical_universe()

    assert isinstance(universe, FormalUniverse)
    assert universe.logic_family == LogicFamily.CLASSICAL
    assert universe.expressivity_score() > 0
    assert universe.stability_score() > 0
    assert universe.accepts_truth_value(TruthValue.TRUE)


def test_universe_library_loads():
    universes = standard_universes()
    names = get_universe_names()

    assert len(universes) >= 6
    assert "Classical Set-Theoretic Neighborhood" in names
    assert "Paraconsistent Contradiction-Tolerant Universe" in names


def test_find_universe_by_name():
    universe = find_universe_by_name("Classical Set-Theoretic Neighborhood")

    assert universe.logic_family == LogicFamily.CLASSICAL


def test_find_universe_by_name_raises_for_missing_universe():
    try:
        find_universe_by_name("Universe That Does Not Exist")
    except ValueError as error:
        assert "No universe found" in str(error)
    else:
        raise AssertionError("Expected ValueError for missing universe")


def test_universe_comparator_compares_two_universes():
    comparator = UniverseComparator()

    comparison = comparator.compare(
        classical_universe(),
        paraconsistent_universe(),
    )

    assert comparison.source_logic == "classical"
    assert comparison.target_logic == "paraconsistent"
    assert 0.0 <= comparison.compatibility_score <= 10.0
    assert "true" in comparison.shared_truth_values
    assert "false" in comparison.shared_truth_values


def test_universe_comparator_compare_all():
    comparator = UniverseComparator()
    universes = standard_universes()

    comparisons = comparator.compare_all(universes)

    assert len(comparisons) == len(universes) * (len(universes) - 1)
    assert all(0.0 <= comparison.compatibility_score <= 10.0 for comparison in comparisons)
