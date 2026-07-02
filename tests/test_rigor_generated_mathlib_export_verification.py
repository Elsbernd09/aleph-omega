"""
Tests for generated Mathlib export verification script.
"""

from pathlib import Path


def test_generated_mathlib_export_script_exists():
    path = Path("scripts/check_generated_mathlib_exports.sh")

    assert path.exists()


def test_generated_mathlib_export_script_generates_exports():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "python3 -m src.rigor.mathlib_finite_system_exporter" in text
    assert "python3 -m src.rigor.mathlib_morphism_exporter" in text


def test_generated_mathlib_export_script_rebuilds_index():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism" in text


def test_generated_mathlib_export_script_checks_mathlib_scaffold():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "./scripts/check_mathlib_scaffold.sh" in text
    assert "Generated Mathlib exports verified successfully." in text


def test_generated_mathlib_export_docs_exist():
    path = Path("docs/generated_mathlib_export_verification.md")

    assert path.exists()
    text = path.read_text()

    assert "Generated Mathlib Export Verification" in text
    assert "./scripts/check_generated_mathlib_exports.sh" in text
    assert "experimental Mathlib Lake build" in text
