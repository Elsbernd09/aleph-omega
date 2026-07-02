"""
Tests for Mathlib quotient composition exporter.
"""

from pathlib import Path

from src.rigor.mathlib_quotient_composition_exporter import (
    MathlibQuotientCompositionExporter,
    MathlibQuotientCompositionExportResult,
)


def test_mathlib_quotient_composition_exporter_renders_imports():
    lean = MathlibQuotientCompositionExporter().render()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotient" in lean
    assert "namespace AlephOmegaMathlib" in lean
    assert "namespace Generated" in lean


def test_mathlib_quotient_composition_exporter_renders_system_and_morphisms():
    lean = MathlibQuotientCompositionExporter().render()

    assert "def ThirdTinyMathlibSystem : FormalSystem" in lean
    assert "def TinyMathlibSecondPreservationMorphism" in lean
    assert "def TinyMathlibCompositePreservationMorphism" in lean
    assert "def QThirdTinyMathlibSystem : QuotientFormalSystem" in lean


def test_mathlib_quotient_composition_exporter_renders_quotient_composition():
    lean = MathlibQuotientCompositionExporter().render()

    assert "def qTinyMathlibSecondPreservation" in lean
    assert "def qTinyMathlibCompositePreservation" in lean
    assert "quotientComposePreservation qTinyMathlibPreservation qTinyMathlibSecondPreservation" in lean
    assert "theorem q_category_tiny_mathlib_generated_composition" in lean


def test_mathlib_quotient_composition_exporter_writes_file(tmp_path):
    output_path = tmp_path / "ExportedTinyMathlibQuotientComposition.lean"

    result = MathlibQuotientCompositionExporter().export(path=str(output_path))

    assert isinstance(result, MathlibQuotientCompositionExportResult)
    assert result.output_path.exists()
    assert result.import_name == "AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotientComposition"
    assert result.composition_theorem_name == "q_category_tiny_mathlib_generated_composition"
    assert "MathlibQuotientCompositionExportResult" in result.describe()


def test_mathlib_quotient_composition_exporter_main_output_path_generation():
    result = MathlibQuotientCompositionExporter().export()

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibQuotientComposition.lean")

    assert path.exists()
    assert result.output_path == path
