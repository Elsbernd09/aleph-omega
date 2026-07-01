"""
Tests for Lean standalone quotient category API artifacts.
"""

from pathlib import Path


def test_lean_core_contains_quotient_category_api_names():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "abbrev QuotientHom" in text
    assert "def quotientId" in text
    assert "def quotientComp" in text
    assert "def quotientHomOf" in text


def test_lean_core_contains_quotient_api_laws():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_api_left_identity" in text
    assert "theorem quotient_api_right_identity" in text
    assert "theorem quotient_api_associativity" in text


def test_lean_core_contains_quotient_api_extensionality():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_hom_ext" in text
    assert "theorem quotient_id_is_identity_class" in text
