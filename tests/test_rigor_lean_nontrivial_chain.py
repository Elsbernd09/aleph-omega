"""
Tests for Lean nontrivial preservation chain artifacts.
"""

from pathlib import Path


def test_lean_core_contains_third_two_system():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "inductive ThirdModel" in text
    assert "inductive ThirdSentence" in text
    assert "def ThirdTwoSystem" in text


def test_lean_core_contains_renamed_to_third_morphism():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def renamedToThirdSentence" in text
    assert "def renamedToThirdModel" in text
    assert "theorem renamed_to_third_preserves" in text
    assert "def renamedToThirdMorphism" in text


def test_lean_core_contains_two_to_third_composite():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def twoToThirdComposite" in text
    assert "theorem two_to_third_composite_preserves" in text
    assert "theorem two_to_third_m0_p" in text
    assert "theorem two_to_third_m1_q" in text


def test_lean_core_contains_composite_translation_and_model_map_facts():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem two_to_third_translates_p" in text
    assert "theorem two_to_third_translates_q" in text
    assert "theorem two_to_third_maps_m0" in text
    assert "theorem two_to_third_maps_m1" in text
