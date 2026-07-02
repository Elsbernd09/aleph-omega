"""
Tests for generated semantic lab Mathlib exporter.
"""

from pathlib import Path

from src.rigor.semantic_lab_mathlib_exporter import (
    SemanticLabMathlibExporter,
    SemanticLabMathlibExportResult,
)


def test_semantic_lab_mathlib_exporter_renders_systems():
    lean = SemanticLabMathlibExporter().render()

    assert "def LabSystemASystem : FormalSystem" in lean
    assert "def LabSystemBSystem : FormalSystem" in lean
    assert "def LabSystemCSystem : FormalSystem" in lean
    assert "def LabSystemDSystem : FormalSystem" in lean


def test_semantic_lab_mathlib_exporter_renders_morphisms():
    lean = SemanticLabMathlibExporter().render()

    assert "def LabMorphismABMorphism" in lean
    assert "def LabMorphismBCMorphism" in lean
    assert "def LabMorphismCDMorphism" in lean
    assert "def qLabMorphismAB" in lean
    assert "def qCategoryLabMorphismCD" in lean


def test_semantic_lab_mathlib_exporter_renders_compositions():
    lean = SemanticLabMathlibExporter().render()

    assert "def qLabCompositeAC" in lean
    assert "def qLabCompositeBD" in lean
    assert "theorem q_category_lab_composition_abc" in lean
    assert "theorem q_category_lab_composition_bcd" in lean


def test_semantic_lab_mathlib_exporter_writes_file(tmp_path):
    output_path = tmp_path / "SemanticLab.lean"

    result = SemanticLabMathlibExporter().export(path=str(output_path))

    assert isinstance(result, SemanticLabMathlibExportResult)
    assert result.output_path.exists()
    assert result.import_name == "AlephOmegaMathlib.Generated.SemanticLab"
    assert result.system_count == 4
    assert result.morphism_count == 3
    assert result.quotient_composition_count == 2
    assert "SemanticLabMathlibExportResult" in result.describe()


def test_semantic_lab_mathlib_exporter_main_output_path_generation():
    result = SemanticLabMathlibExporter().export()

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean")

    assert path.exists()
    assert result.output_path == path
