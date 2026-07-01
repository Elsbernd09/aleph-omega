"""
Tests for institution-theoretic exposition generation.
"""

from pathlib import Path

from src.rigor.institution_exposition import (
    InstitutionExposition,
    InstitutionExpositionBuilder,
)


def test_institution_exposition_builds():
    exposition = InstitutionExpositionBuilder().build()

    assert isinstance(exposition, InstitutionExposition)
    assert "Institution-Theoretic Upgrade" in exposition.title
    assert exposition.section_count() >= 10
    assert exposition.word_count() > 500
    assert "InstitutionExposition" in exposition.describe()


def test_institution_exposition_markdown_contains_sections():
    exposition = InstitutionExpositionBuilder().build()
    markdown = exposition.to_markdown()

    assert "# Institution-Theoretic Upgrade" in markdown
    assert "Finite Institution Satisfaction Theorem" in markdown
    assert "Category-Like Structure" in markdown
    assert "Correct Research Claim" in markdown


def test_institution_exposition_write_markdown(tmp_path):
    exposition = InstitutionExpositionBuilder().build()
    output_path = tmp_path / "institution_theoretic_upgrade.md"

    written = InstitutionExpositionBuilder().write_markdown(
        exposition=exposition,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Institution-Theoretic Upgrade" in written.read_text()
