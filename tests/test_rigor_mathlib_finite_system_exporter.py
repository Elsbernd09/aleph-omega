"""
Tests for Mathlib-targeted finite system exporter.
"""

from pathlib import Path

from src.rigor.mathlib_finite_system_exporter import (
    MathlibFiniteSystemExportResult,
    MathlibFiniteSystemExporter,
    tiny_mathlib_export_system,
)


def test_mathlib_finite_system_exporter_renders_mathlib_import():
    lean = MathlibFiniteSystemExporter().render(tiny_mathlib_export_system())

    assert "import AlephOmegaMathlib.FormalSystemCategory" in lean
    assert "namespace AlephOmegaMathlib" in lean
    assert "namespace Generated" in lean
    assert "structure FormalSystem" not in lean
    assert "def ExportedTinyMathlibSystem : FormalSystem" in lean


def test_mathlib_finite_system_exporter_renders_core_definitions():
    lean = MathlibFiniteSystemExporter().render(tiny_mathlib_export_system())

    assert "inductive ExportedTinyMathlibModel" in lean
    assert "inductive ExportedTinyMathlibSentence" in lean
    assert "theorem exportedtinymathlib_m0_p_sat" in lean
    assert "theorem exportedtinymathlib_m0_q_not_sat" in lean


def test_mathlib_finite_system_exporter_writes_file(tmp_path):
    output_path = tmp_path / "ExportedTinyMathlibSystem.lean"

    result = MathlibFiniteSystemExporter().export(
        tiny_mathlib_export_system(),
        path=str(output_path),
    )

    assert isinstance(result, MathlibFiniteSystemExportResult)
    assert result.output_path.exists()
    assert result.model_count == 2
    assert result.sentence_count == 2
    assert result.positive_theorem_count == 2
    assert result.negative_theorem_count == 2
    assert "MathlibFiniteSystemExportResult" in result.describe()


def test_mathlib_finite_system_exporter_main_output_path_generation():
    result = MathlibFiniteSystemExporter().export(tiny_mathlib_export_system())

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibSystem.lean")

    assert path.exists()
    assert result.output_path == path
    assert result.import_name == "AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem"
