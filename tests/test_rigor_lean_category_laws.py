"""
Tests for Lean category-law artifacts.
"""

from pathlib import Path


def test_lean_core_contains_identity_laws():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem left_identity_translation" in text
    assert "theorem left_identity_model_map" in text
    assert "theorem right_identity_translation" in text
    assert "theorem right_identity_model_map" in text


def test_lean_core_contains_associativity_laws():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem associativity_translation" in text
    assert "theorem associativity_model_map" in text
    assert "theorem associativity_preserves_satisfaction" in text
