"""
Documentation tests for Mathlib-targeted finite system exporter.
"""

from pathlib import Path


def test_mathlib_finite_system_exporter_docs_exist():
    path = Path("docs/mathlib_finite_system_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Mathlib-Targeted Finite System Exporter" in text
    assert "src/rigor/mathlib_finite_system_exporter.py" in text
    assert "ExportedTinyMathlibSystem.lean" in text
    assert "experimental Mathlib category-theory track" in text


def test_mathlib_generated_index_exists():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean")

    assert path.exists()
    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem" in path.read_text()


def test_mathlib_entry_imports_generated_index():
    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib.lean")

    assert "import AlephOmegaMathlib.Generated" in path.read_text()
