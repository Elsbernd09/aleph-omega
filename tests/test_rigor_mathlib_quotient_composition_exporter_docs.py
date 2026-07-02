"""
Documentation tests for Mathlib quotient composition exporter.
"""

from pathlib import Path


def test_mathlib_quotient_composition_exporter_docs_exist():
    path = Path("docs/mathlib_quotient_composition_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Mathlib Generated Quotient Composition Exporter" in text
    assert "mathlib_quotient_composition_exporter.py" in text
    assert "ExportedTinyMathlibQuotientComposition.lean" in text
    assert "q_category_tiny_mathlib_generated_composition" in text


def test_generated_index_imports_quotient_composition():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean").read_text()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotientComposition" in text


def test_generated_mathlib_checker_generates_quotient_composition():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "python3 -m src.rigor.mathlib_quotient_composition_exporter" in text
    assert "ExportedTinyMathlibQuotientComposition" in text
