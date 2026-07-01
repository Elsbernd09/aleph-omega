"""
Tests for generated Lean export verification script.
"""

from pathlib import Path


def test_generated_lean_export_script_exists():
    path = Path("scripts/check_generated_lean_exports.sh")

    assert path.exists()


def test_generated_lean_export_script_contains_generation_steps():
    text = Path("scripts/check_generated_lean_exports.sh").read_text()

    assert "python3 -m src.rigor.lean_finite_system_exporter" in text
    assert "python3 -m src.rigor.lean_morphism_exporter" in text


def test_generated_lean_export_script_checks_lean_files():
    text = Path("scripts/check_generated_lean_exports.sh").read_text()

    assert "lean formal/generated/ExportedTinySystem.lean" in text
    assert "lean formal/generated/ExportedTinyMorphism.lean" in text
    assert "Generated Lean exports verified successfully." in text


def test_generated_lean_export_docs_exist():
    path = Path("docs/generated_lean_export_verification.md")

    assert path.exists()
    text = path.read_text()

    assert "Generated Lean Export Verification" in text
    assert "./scripts/check_generated_lean_exports.sh" in text
    assert "Generated Lean exports verified successfully." in text
