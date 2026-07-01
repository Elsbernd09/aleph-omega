"""
Tests for Lean morphism-equivalence artifacts.
"""

from pathlib import Path


def test_lean_core_contains_morphism_equivalence_definition():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def MorphismEquivalent" in text
    assert "F.translate φ = G.translate φ" in text
    assert "F.mapModel m = G.mapModel m" in text


def test_lean_core_contains_equivalence_relation_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem morphism_equiv_refl" in text
    assert "theorem morphism_equiv_symm" in text
    assert "theorem morphism_equiv_trans" in text


def test_lean_core_contains_category_laws_as_equivalence():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem left_identity_equivalent" in text
    assert "theorem right_identity_equivalent" in text
    assert "theorem associativity_equivalent" in text
