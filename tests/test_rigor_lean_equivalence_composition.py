"""
Tests for Lean equivalence-compatible composition artifacts.
"""

from pathlib import Path


def test_lean_core_contains_composition_equivalence_compatibility():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem compose_respects_morphism_equivalence" in text
    assert "MorphismEquivalent (composeMorphism F G) (composeMorphism F' G')" in text


def test_lean_core_contains_equivalent_transport_theorem():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem equivalent_morphisms_transport_satisfaction" in text
    assert "B.Sat (G.mapModel m) (G.translate φ)" in text


def test_lean_core_contains_left_and_right_composition_respect():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem left_composition_respects_equivalence" in text
    assert "theorem right_composition_respects_equivalence" in text
