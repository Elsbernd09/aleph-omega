"""
Documentation tests for semantic lab Mathlib exporter.
"""

from pathlib import Path


def test_semantic_lab_mathlib_exporter_docs_exist():
    path = Path("docs/semantic_lab_mathlib_exporter.md")

    assert path.exists()
    text = path.read_text()

    assert "Generated Semantic Lab Mathlib Exporter" in text
    assert "semantic_lab_mathlib_exporter.py" in text
    assert "SemanticLab.lean" in text
    assert "q_category_lab_composition_abc" in text


def test_generated_index_imports_semantic_lab():
    text = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean").read_text()

    assert "import AlephOmegaMathlib.Generated.SemanticLab" in text


def test_generated_mathlib_checker_generates_semantic_lab():
    text = Path("scripts/check_generated_mathlib_exports.sh").read_text()

    assert "python3 -m src.rigor.semantic_lab_mathlib_exporter" in text
    assert "import AlephOmegaMathlib.Generated.SemanticLab" in text
