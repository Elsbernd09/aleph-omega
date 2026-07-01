"""
Tests for bridge case generation.
"""

from src.rigor.bridge_case_generator import (
    BridgeCase,
    BridgeCaseGenerator,
    BridgeCaseKind,
)
from src.rigor.finite_universe import SemanticFeature
from src.rigor.model_search import FiniteModelGenerator


def small_universe_cases():
    return FiniteModelGenerator().generate_universe_cases(
        features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        max_feature_set_size=1,
    )


def test_identity_case():
    universe = small_universe_cases()[0].universe

    case = BridgeCaseGenerator().identity_case(universe)

    assert isinstance(case, BridgeCase)
    assert case.kind == BridgeCaseKind.IDENTITY
    assert case.is_total()
    assert not case.has_feature_mismatch()
    assert "BridgeCase" in case.describe()


def test_collapse_case():
    cases = small_universe_cases()
    source = cases[0].universe
    target = cases[1].universe

    case = BridgeCaseGenerator().collapse_case(source, target)

    assert case.kind == BridgeCaseKind.COLLAPSE
    assert case.is_total()
    assert case.bridge.source == source
    assert case.bridge.target == target


def test_empty_partial_case():
    universe = small_universe_cases()[0].universe

    case = BridgeCaseGenerator().empty_partial_case(universe, universe)

    assert case.kind == BridgeCaseKind.EMPTY_PARTIAL
    assert not case.is_total()
    assert case.bridge.distortion_count() == universe.statement_count()


def test_same_feature_case_can_preserve_matching_features():
    universe = small_universe_cases()[0].universe

    case = BridgeCaseGenerator().same_feature_case(universe, universe)

    assert case.kind == BridgeCaseKind.SAME_FEATURE
    assert case.is_total()
    assert case.bridge.preservation_count() == universe.statement_count()


def test_generate_cases_for_pair():
    cases = small_universe_cases()
    source = cases[0].universe
    target = cases[1].universe

    generated = BridgeCaseGenerator().generate_cases_for_pair(source, target)

    assert len(generated) == 3
    kinds = {case.kind for case in generated}

    assert BridgeCaseKind.COLLAPSE in kinds
    assert BridgeCaseKind.EMPTY_PARTIAL in kinds
    assert BridgeCaseKind.SAME_FEATURE in kinds


def test_generate_cases_for_identity_pair_includes_identity():
    universe = small_universe_cases()[0].universe

    generated = BridgeCaseGenerator().generate_cases_for_pair(universe, universe)

    kinds = {case.kind for case in generated}

    assert BridgeCaseKind.IDENTITY in kinds
    assert len(generated) == 4


def test_generate_cases_all_pairs():
    universe_cases = small_universe_cases()

    generated = BridgeCaseGenerator().generate_cases(universe_cases)

    assert len(generated) > 0
    assert any(case.kind == BridgeCaseKind.IDENTITY for case in generated)
    assert any(case.kind == BridgeCaseKind.EMPTY_PARTIAL for case in generated)
    assert any(case.kind == BridgeCaseKind.SAME_FEATURE for case in generated)
