"""
Documentation tests for Mathlib quotient wrapper exporter.
"""

from pathlib import Path


def test_mathlib_quotient_wrapper_exporter_docs_exist():
    path = Path("docs/mathlib_quotient_wrapper_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Mathlib Generated Quotient Wrapper Exporter" in text
    assert "src/rigor/mathlib_quotient_wrapper_exporter.py" in text
    assert "ExportedTinyMathlibQuotient.lean" in text
    assert "qCategoryTinyMathlibPreservation" in text


def test_generated_index_imports_quotient_wrapper():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean")

    assert path.exists()
    text = path.read_text()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotient" in text
