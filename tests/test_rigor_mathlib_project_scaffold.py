"""
Tests for experimental Mathlib project scaffold.
"""

from pathlib import Path


def test_mathlib_project_files_exist():
    root = Path("formal/aleph_omega_mathlib")

    assert (root / "lakefile.lean").exists()
    assert (root / "lean-toolchain").exists()
    assert (root / "AlephOmegaMathlib.lean").exists()
    assert (root / "AlephOmegaMathlib" / "CategorySmokeTest.lean").exists()


def test_mathlib_lakefile_mentions_mathlib():
    text = Path("formal/aleph_omega_mathlib/lakefile.lean").read_text()

    assert "require mathlib" in text
    assert "mathlib4" in text
    assert "lean_lib AlephOmegaMathlib" in text


def test_mathlib_smoke_test_imports_category_basic():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean").read_text()

    assert "Mathlib.CategoryTheory.Category.Basic" in text
    assert "SmokeObject" in text
    assert "smoke_associativity" in text


def test_mathlib_scaffold_script_exists():
    text = Path("scripts/check_mathlib_scaffold.sh").read_text()

    assert "formal/aleph_omega_mathlib" in text
    assert "lake build" in text


def test_mathlib_scaffold_docs_exist():
    text = Path("docs/mathlib_project_scaffold.md").read_text()

    assert "Mathlib Project Scaffold" in text
    assert "Non-Claim" in text
