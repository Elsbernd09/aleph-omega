"""
Documentation tests for Mathlib-targeted preservation morphism exporter.
"""

from pathlib import Path


def test_mathlib_morphism_exporter_docs_exist():
    path = Path("docs/mathlib_morphism_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Mathlib-Targeted Preservation Morphism Exporter" in text
    assert "src/rigor/mathlib_morphism_exporter.py" in text
    assert "ExportedTinyMathlibMorphism.lean" in text
    assert "experimental Mathlib category-theory track" in text


def test_mathlib_generated_index_imports_morphism():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean")

    assert path.exists()
    text = path.read_text()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem" in text
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism" in text
