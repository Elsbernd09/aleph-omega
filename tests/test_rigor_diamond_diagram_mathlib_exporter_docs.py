"""
Documentation tests for diamond diagram Mathlib exporter.
"""

from pathlib import Path


def test_diamond_diagram_mathlib_exporter_docs_exist():
    path = Path("docs/diamond_diagram_mathlib_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Generated Diamond Diagram Mathlib Exporter" in text
    assert "diamond_diagram_mathlib_exporter.py" in text
    assert "DiamondDiagram.lean" in text
    assert "q_diamond_paths_equal" in text
    assert "Quotient.sound" in text


def test_generated_index_imports_diamond_diagram():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean").read_text()

    assert "import AlephOmegaMathlib.Generated.DiamondDiagram" in text


def test_generated_mathlib_checker_generates_diamond_diagram():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "python3 -m src.rigor.diamond_diagram_mathlib_exporter" in text
    assert "import AlephOmegaMathlib.Generated.DiamondDiagram" in text
