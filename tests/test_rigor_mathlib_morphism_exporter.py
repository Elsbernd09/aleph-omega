"""
Tests for Mathlib-targeted preservation morphism exporter.
"""

from pathlib import Path

from src.rigor.mathlib_morphism_exporter import (
    MathlibMorphismExportResult,
    MathlibMorphismExporter,
    tiny_mathlib_export_morphism,
)


def test_mathlib_morphism_exporter_renders_mathlib_import():
    lean = MathlibMorphismExporter().render(tiny_mathlib_export_morphism())

    assert "import AlephOmegaMathlib.FormalSystemCategory" in lean
    assert "namespace AlephOmegaMathlib" in lean
    assert "namespace Generated" in lean
    assert "structure PreservationMorphism" not in lean
    assert "def TinyMathlibPreservationMorphism" in lean


def test_mathlib_morphism_exporter_renders_core_definitions():
    lean = MathlibMorphismExporter().render(tiny_mathlib_export_morphism())

    assert "def SourceTinyMathlibSystem" in lean
    assert "def TargetTinyMathlibSystem" in lean
    assert "def TinyMathlibPreservationTranslate" in lean
    assert "def TinyMathlibPreservationModelMap" in lean
    assert "theorem tinymathlibpreservation_preserves" in lean


def test_mathlib_morphism_exporter_writes_file(tmp_path):
    output_path = tmp_path / "ExportedTinyMathlibMorphism.lean"

    result = MathlibMorphismExporter().export(
        tiny_mathlib_export_morphism(),
        path=str(output_path),
    )

    assert isinstance(result, MathlibMorphismExportResult)
    assert result.output_path.exists()
    assert result.source_system_name == "SourceTinyMathlib"
    assert result.target_system_name == "TargetTinyMathlib"
    assert "MathlibMorphismExportResult" in result.describe()


def test_mathlib_morphism_exporter_main_output_path_generation():
    result = MathlibMorphismExporter().export(tiny_mathlib_export_morphism())

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibMorphism.lean")

    assert path.exists()
    assert result.output_path == path
    assert result.import_name == "AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism"
