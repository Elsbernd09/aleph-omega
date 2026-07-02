"""
Tests for Mathlib quotient wrapper exporter.
"""

from pathlib import Path

from src.rigor.mathlib_quotient_wrapper_exporter import (
    MathlibQuotientWrapperExporter,
    MathlibQuotientWrapperExportResult,
)


def test_mathlib_quotient_wrapper_exporter_renders_core_imports():
    lean = MathlibQuotientWrapperExporter().render()

    assert "import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism" in lean
    assert "import AlephOmegaMathlib.QuotientFormalSystemCategory" in lean
    assert "namespace AlephOmegaMathlib" in lean
    assert "namespace Generated" in lean


def test_mathlib_quotient_wrapper_exporter_renders_quotient_artifacts():
    lean = MathlibQuotientWrapperExporter().render()

    assert "def QSourceTinyMathlibSystem : QuotientFormalSystem" in lean
    assert "def QTargetTinyMathlibSystem : QuotientFormalSystem" in lean
    assert "def qTinyMathlibPreservation" in lean
    assert "QuotientPreservationHom SourceTinyMathlibSystem TargetTinyMathlibSystem" in lean
    assert "quotientPreservationOf TinyMathlibPreservationMorphism" in lean
    assert "def qCategoryTinyMathlibPreservation" in lean


def test_mathlib_quotient_wrapper_exporter_writes_file(tmp_path):
    output_path = tmp_path / "ExportedTinyMathlibQuotient.lean"

    result = MathlibQuotientWrapperExporter().export(path=str(output_path))

    assert isinstance(result, MathlibQuotientWrapperExportResult)
    assert result.output_path.exists()
    assert result.import_name == "AlephOmegaMathlib.Generated.ExportedTinyMathlibQuotient"
    assert result.quotient_morphism_name == "qTinyMathlibPreservation"
    assert "MathlibQuotientWrapperExportResult" in result.describe()


def test_mathlib_quotient_wrapper_exporter_main_output_path_generation():
    result = MathlibQuotientWrapperExporter().export()

    path = Path("formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibQuotient.lean")

    assert path.exists()
    assert result.output_path == path
