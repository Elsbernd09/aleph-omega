"""
Tests for generated diamond diagram Mathlib exporter.
"""

from pathlib import Path

from src.rigor.diamond_diagram_mathlib_exporter import (
    DiamondDiagramMathlibExporter,
    DiamondDiagramMathlibExportResult,
)


def test_diamond_diagram_mathlib_exporter_renders_systems():
    lean = DiamondDiagramMathlibExporter().render()

    assert "def DiamondSystemASystem : FormalSystem" in lean
    assert "def DiamondSystemBSystem : FormalSystem" in lean
    assert "def DiamondSystemCSystem : FormalSystem" in lean
    assert "def DiamondSystemDSystem : FormalSystem" in lean


def test_diamond_diagram_mathlib_exporter_renders_morphisms():
    lean = DiamondDiagramMathlibExporter().render()

    assert "def DiamondMorphismABMorphism" in lean
    assert "def DiamondMorphismACMorphism" in lean
    assert "def DiamondMorphismBDMorphism" in lean
    assert "def DiamondMorphismCDMorphism" in lean


def test_diamond_diagram_mathlib_exporter_renders_nontrivial_equivalence_theorems():
    lean = DiamondDiagramMathlibExporter().render()

    assert "theorem diamond_path_translation_equivalence" in lean
    assert "theorem diamond_path_model_map_equivalence" in lean
    assert "theorem diamond_paths_preservation_equivalent" in lean
    assert "apply Quotient.sound" in lean
    assert "theorem q_diamond_paths_equal" in lean
    assert "theorem q_category_diamond_commutes" in lean


def test_diamond_diagram_mathlib_exporter_writes_file(tmp_path):
    output_path = tmp_path / "DiamondDiagram.lean"

    result = DiamondDiagramMathlibExporter().export(path=str(output_path))

    assert isinstance(result, DiamondDiagramMathlibExportResult)
    assert result.output_path.exists()
    assert result.import_name == "AlephOmegaMathlib.Generated.DiamondDiagram"
    assert result.system_count == 4
    assert result.morphism_count == 4
    assert result.path_equivalence_theorem == "q_diamond_paths_equal"
    assert "DiamondDiagramMathlibExportResult" in result.describe()


def test_diamond_diagram_mathlib_exporter_main_output_path_generation():
    result = DiamondDiagramMathlibExporter().export()

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/DiamondDiagram.lean")

    assert path.exists()
    assert result.output_path == path
