"""
Tests for the Lean two-model / two-sentence finite system artifact.
"""

from pathlib import Path


def test_lean_core_contains_two_system_types():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "inductive TwoModel" in text
    assert "inductive TwoSentence" in text
    assert "def TwoSystem" in text


def test_lean_core_contains_two_system_positive_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem two_m0_satisfies_p" in text
    assert "theorem two_m1_satisfies_q" in text
    assert "theorem two_identity_preserves" in text
    assert "theorem two_identity_composition_preserves" in text


def test_lean_core_contains_two_system_failure_boundary():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def twoSwapSentence" in text
    assert "def twoIdentityModel" in text
    assert "theorem two_swap_translation_failure" in text
    assert "theorem two_swap_translation_not_preserving" in text
