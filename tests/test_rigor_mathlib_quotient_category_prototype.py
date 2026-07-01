"""
Tests for Mathlib quotient category prototype.
"""

from pathlib import Path


def test_mathlib_quotient_category_file_exists():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/QuotientFormalSystemCategory.lean")

    assert path.exists()


def test_mathlib_quotient_category_core_definitions_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/QuotientFormalSystemCategory.lean").read_text()

    assert "def PreservationEquivalent" in text
    assert "instance preservationSetoid" in text
    assert "def QuotientPreservationHom" in text
    assert "def quotientComposePreservation" in text


def test_mathlib_quotient_category_instance_exists():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/QuotientFormalSystemCategory.lean").read_text()

    assert "structure QuotientFormalSystem" in text
    assert "instance quotientFormalSystemCategory" in text
    assert "Category (QuotientFormalSystem" in text
    assert "Hom A B := QuotientFormalSystemHom A B" in text


def test_mathlib_quotient_category_supporting_theorems_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/QuotientFormalSystemCategory.lean").read_text()

    assert "theorem preservation_equiv_refl" in text
    assert "theorem preservation_equiv_symm" in text
    assert "theorem preservation_equiv_trans" in text
    assert "theorem compose_preservation_respects_equivalence" in text
    assert "theorem quotient_bool_identity_composes" in text


def test_mathlib_entry_imports_quotient_category():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib.lean").read_text()

    assert "import AlephOmegaMathlib.QuotientFormalSystemCategory" in text


def test_mathlib_quotient_category_docs_exist():
    text = Path("docs/mathlib_quotient_category_prototype.md").read_text()

    assert "Mathlib Quotient Category Prototype" in text
    assert "quotientFormalSystemCategory" in text
    assert "prototype quotient category" in text
