"""
Tests for Lean standalone quotient category structure artifacts.
"""

from pathlib import Path


def test_lean_core_contains_standalone_category_structure():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "structure StandaloneQuotientCategory" in text
    assert "Hom : FormalSystem -> FormalSystem -> Type" in text
    assert "left_id" in text
    assert "right_id" in text
    assert "assoc" in text


def test_lean_core_contains_aleph_omega_category_instance():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def AlephOmegaQuotientCategory" in text
    assert "Hom := QuotientHom" in text
    assert "id := quotientId" in text
    assert "comp := fun F G => quotientComp F G" in text


def test_lean_core_contains_category_identification_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem quotient_category_hom_is_quotient_hom" in text
    assert "theorem quotient_category_id_is_quotient_id" in text
    assert "theorem quotient_category_comp_is_quotient_comp" in text
