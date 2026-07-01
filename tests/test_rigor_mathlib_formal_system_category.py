"""
Tests for the Mathlib formal system category instance.
"""

from pathlib import Path


def test_mathlib_formal_system_category_file_exists():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean")

    assert path.exists()


def test_mathlib_formal_system_category_definitions_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean").read_text()

    assert "structure FormalSystem" in text
    assert "structure PreservationMorphism" in text
    assert "def identityPreservation" in text
    assert "def composePreservation" in text


def test_mathlib_formal_system_category_instance_exists():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean").read_text()

    assert "instance formalSystemCategory : Category" in text
    assert "Hom A B := PreservationMorphism A B" in text
    assert "id A := identityPreservation A" in text
    assert "comp F G := composePreservation F G" in text


def test_mathlib_formal_system_category_theorems_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean").read_text()

    assert "theorem formal_category_id_is_identity" in text
    assert "theorem formal_category_comp_is_compose" in text
    assert "def BoolFormalSystem" in text
    assert "theorem bool_formal_category_identity_preserves_true" in text


def test_mathlib_entry_imports_formal_system_category():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib.lean").read_text()

    assert "import AlephOmegaMathlib.FormalSystemCategory" in text


def test_mathlib_formal_system_category_docs_exist():
    text = Path("docs/mathlib_formal_system_category.md").read_text()

    assert "Mathlib Formal System Category" in text
    assert "formalSystemCategory" in text
    assert "not yet the quotient category" in text
