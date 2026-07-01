"""
Tests for Lean concrete quotient morphism chain artifacts.
"""

from pathlib import Path


def test_lean_core_contains_concrete_quotient_homs():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def qTwoToRenamed" in text
    assert "def qRenamedToThird" in text
    assert "def qTwoToThird" in text


def test_lean_core_contains_concrete_quotient_composition():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem q_two_to_third_composition" in text
    assert "theorem quotient_category_composes_concrete_chain" in text


def test_lean_core_contains_concrete_quotient_laws():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem q_two_to_renamed_left_identity" in text
    assert "theorem q_two_to_renamed_right_identity" in text
    assert "theorem q_concrete_chain_associativity_with_identity" in text
