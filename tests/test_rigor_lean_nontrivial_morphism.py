"""
Tests for Lean nontrivial preservation morphism artifacts.
"""

from pathlib import Path


def test_lean_core_contains_renamed_two_system():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "inductive RenamedModel" in text
    assert "inductive RenamedSentence" in text
    assert "def RenamedTwoSystem" in text


def test_lean_core_contains_nontrivial_maps():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def twoToRenamedSentence" in text
    assert "def twoToRenamedModel" in text
    assert "theorem two_to_renamed_preserves" in text
    assert "def twoToRenamedMorphism" in text


def test_lean_core_contains_nontrivial_preservation_examples():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem two_to_renamed_m0_p" in text
    assert "theorem two_to_renamed_m1_q" in text
    assert "theorem two_to_renamed_then_identity_preserves" in text
    assert "theorem identity_then_two_to_renamed_preserves" in text
