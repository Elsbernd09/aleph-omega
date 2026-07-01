"""
Tests for Python-to-Lean preservation morphism exporter.
"""

from pathlib import Path

import pytest

from src.rigor.lean_finite_system_exporter import ExportedFiniteSystem
from src.rigor.lean_morphism_exporter import (
    ExportedFiniteMorphism,
    LeanMorphismExportResult,
    LeanMorphismExporter,
    tiny_export_morphism,
)


def test_exported_morphism_validates():
    morphism = tiny_export_morphism()
    morphism.validate()


def test_exported_morphism_rejects_non_preserving_map():
    source = ExportedFiniteSystem(
        name="BadSource",
        models=("m0",),
        sentences=("p",),
        satisfying_pairs=(("m0", "p"),),
    )

    target = ExportedFiniteSystem(
        name="BadTarget",
        models=("a",),
        sentences=("alpha",),
        satisfying_pairs=(),
    )

    bad = ExportedFiniteMorphism(
        name="BadMorphism",
        source=source,
        target=target,
        model_map={"m0": "a"},
        sentence_map={"p": "alpha"},
    )

    with pytest.raises(ValueError):
        bad.validate()


def test_morphism_exporter_renders_lean_code():
    lean = LeanMorphismExporter().render(tiny_export_morphism())

    assert "namespace AlephOmegaGeneratedMorphism" in lean
    assert "structure PreservationMorphism" in lean
    assert "def SourceTinySystem" in lean
    assert "def TargetTinySystem" in lean
    assert "def TinyPreservationTranslate" in lean
    assert "def TinyPreservationModelMap" in lean
    assert "theorem tinypreservation_preserves" in lean
    assert "def TinyPreservationMorphism" in lean


def test_morphism_exporter_writes_file(tmp_path):
    output_path = tmp_path / "ExportedTinyMorphism.lean"

    result = LeanMorphismExporter().export(
        tiny_export_morphism(),
        path=str(output_path),
    )

    assert isinstance(result, LeanMorphismExportResult)
    assert result.output_path.exists()
    assert result.source_system_name == "SourceTiny"
    assert result.target_system_name == "TargetTiny"
    assert "LeanMorphismExportResult" in result.describe()


def test_morphism_exporter_main_output_path_generation():
    result = LeanMorphismExporter().export(tiny_export_morphism())

    assert Path("formal/generated/ExportedTinyMorphism.lean").exists()
    assert result.output_path == Path("formal/generated/ExportedTinyMorphism.lean")
