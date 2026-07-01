"""
Tests for Lean quotient composition operation artifacts.
"""

from pathlib import Path


def test_lean_core_contains_quotient_compose_operation():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def quotientCompose" in text
    assert "Quotient.liftOn₂" in text
    assert "quotient_composition_well_defined" in text


def test_lean_core_contains_quotient_category_laws():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_category_left_identity" in text
    assert "theorem quotient_category_right_identity" in text
    assert "theorem quotient_category_associativity" in text
