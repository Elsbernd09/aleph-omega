"""
Tests for Lean Setoid and quotient hom-type artifacts.
"""

from pathlib import Path


def test_lean_core_contains_morphism_setoid():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "instance morphismSetoid" in text
    assert "Setoid (PreservationMorphism A B)" in text
    assert "r := MorphismEquivalent" in text


def test_lean_core_contains_quotient_hom_type():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def QuotientMorphism" in text
    assert "Quotient (@morphismSetoid A B)" in text
    assert "def quotientIdentity" in text
    assert "def quotientOf" in text


def test_lean_core_contains_quotient_correctness_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem equivalent_morphisms_same_quotient" in text
    assert "theorem quotient_refl" in text
    assert "theorem quotient_identity_def" in text
