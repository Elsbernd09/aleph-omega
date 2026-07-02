"""
Tests that generated Mathlib export verification includes Phase 33 quotient wrappers.
"""

from pathlib import Path


def test_generated_mathlib_checker_generates_quotient_wrapper():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "python3 -m src.rigor.mathlib_quotient_wrapper_exporter" in text
    assert "ExportedTinyMathlibQuotient" in text


def test_generated_mathlib_checker_rebuilds_index_with_quotient_import():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotient" in text
