"""
Tests for Python-to-Lean finite system exporter.
"""

from pathlib import Path

import pytest

from src.rigor.lean_finite_system_exporter import (
    ExportedFiniteSystem,
    LeanExportResult,
    LeanFiniteSystemExporter,
    lean_safe_identifier,
    tiny_export_system,
)


def test_lean_safe_identifier_handles_invalid_names():
    assert lean_safe_identifier("Model 1", "m") == "model_1"
    assert lean_safe_identifier("123", "m") == "m_123"
    assert lean_safe_identifier("!!!", "m") == "m"


def test_exported_finite_system_validates():
    system = tiny_export_system()
    system.validate()

    bad = ExportedFiniteSystem(
        name="Bad",
        models=("m0",),
        sentences=("p",),
        satisfying_pairs=(("missing", "p"),),
    )

    with pytest.raises(ValueError):
        bad.validate()


def test_exporter_renders_lean_system():
    system = tiny_export_system()
    lean = LeanFiniteSystemExporter().render(system)

    assert "namespace AlephOmegaGenerated" in lean
    assert "structure FormalSystem" in lean
    assert "inductive ExportedTinyModel" in lean
    assert "inductive ExportedTinySentence" in lean
    assert "def ExportedTinySystem" in lean
    assert "theorem exportedtiny_m0_p_sat" in lean
    assert "theorem exportedtiny_m0_q_not_sat" in lean


def test_exporter_writes_lean_file(tmp_path):
    system = tiny_export_system()
    output_path = tmp_path / "ExportedTinySystem.lean"

    result = LeanFiniteSystemExporter().export(system, path=str(output_path))

    assert isinstance(result, LeanExportResult)
    assert result.output_path.exists()
    assert result.model_count == 2
    assert result.sentence_count == 2
    assert result.positive_theorem_count == 2
    assert result.negative_theorem_count == 2
    assert "LeanExportResult" in result.describe()


def test_exporter_main_output_path_generation():
    result = LeanFiniteSystemExporter().export(tiny_export_system())

    assert Path("formal/generated/ExportedTinySystem.lean").exists()
    assert result.output_path == Path("formal/generated/ExportedTinySystem.lean")
