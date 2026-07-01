"""
Tests for the Mathlib category smoke instance.
"""

from pathlib import Path


def test_mathlib_smoke_category_instance_exists():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean").read_text()

    assert "instance smokeCategory : Category SmokeObject" in text
    assert "Hom A B := SmokeHom A B" in text
    assert "id A := SmokeId A" in text
    assert "comp f g := SmokeComp f g" in text


def test_mathlib_smoke_category_theorems_exist():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean").read_text()

    assert "theorem smoke_category_id_is_smoke_id" in text
    assert "theorem smoke_category_comp_is_smoke_comp" in text
    assert "theorem smoke_category_left_identity" in text
    assert "theorem smoke_category_right_identity" in text
    assert "theorem smoke_category_assoc" in text


def test_mathlib_category_smoke_docs_exist():
    path = Path("docs/mathlib_category_smoke_instance.md")

    assert path.exists()
    text = path.read_text()

    assert "Mathlib Category Smoke Instance" in text
    assert "real Mathlib `Category` instance" in text
    assert "Non-Claim" in text
