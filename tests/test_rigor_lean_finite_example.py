"""
Tests for the Lean finite example artifact.
"""

from pathlib import Path


def test_lean_core_contains_bool_system():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def BoolSystem" in text
    assert "Model := Bool" in text
    assert "Sentence := Bool" in text
    assert "Sat := fun m φ => m = φ" in text


def test_lean_core_contains_bool_example_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem bool_true_satisfies_true" in text
    assert "theorem bool_true_not_satisfy_false" in text
    assert "theorem bool_identity_preserves" in text
    assert "theorem bool_identity_composition_preserves" in text
    assert "theorem bool_identity_composition_true" in text
