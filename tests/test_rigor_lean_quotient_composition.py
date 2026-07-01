"""
Tests for Lean quotient-composition well-definedness artifacts.
"""

from pathlib import Path


def test_lean_core_contains_quotient_composition_well_definedness():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_composition_well_defined" in text
    assert "quotientOf (composeMorphism F G) = quotientOf (composeMorphism F' G')" in text


def test_lean_core_contains_representative_change_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_left_representative_change" in text
    assert "theorem quotient_right_representative_change" in text


def test_lean_core_contains_quotient_identity_and_associativity():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_left_identity" in text
    assert "theorem quotient_right_identity" in text
    assert "theorem quotient_associativity" in text
