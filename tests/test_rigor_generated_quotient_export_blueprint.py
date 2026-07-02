"""
Tests for generated quotient-category export blueprint.
"""

from pathlib import Path

from src.rigor.generated_quotient_export_blueprint import (
    GeneratedQuotientExportBlueprint,
    GeneratedQuotientExportBlueprintBuilder,
    GeneratedQuotientExportRequirement,
)


def test_generated_quotient_export_blueprint_builds():
    blueprint = GeneratedQuotientExportBlueprintBuilder().build()

    assert isinstance(blueprint, GeneratedQuotientExportBlueprint)
    assert blueprint.requirement_count() >= 8
    assert len(blueprint.quotient_targets()) >= 6
    assert "GeneratedQuotientExportBlueprint" in blueprint.describe()


def test_generated_quotient_export_requirement_describe():
    blueprint = GeneratedQuotientExportBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, GeneratedQuotientExportRequirement)
    assert "GeneratedQuotientExportRequirement" in requirement.describe()


def test_generated_quotient_export_markdown_contains_core_plan():
    blueprint = GeneratedQuotientExportBlueprintBuilder().build()
    markdown = GeneratedQuotientExportBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Generated Quotient Category Export Blueprint" in markdown
    assert "Phase 33" in markdown
    assert "QuotientFormalSystemCategory" in markdown
    assert "qTinyMathlibPreservation" in markdown
    assert "Non-Claim" in markdown


def test_generated_quotient_export_write_markdown(tmp_path):
    blueprint = GeneratedQuotientExportBlueprintBuilder().build()
    output_path = tmp_path / "generated_quotient_export_blueprint.md"

    written = GeneratedQuotientExportBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Quotient Category Export Blueprint" in written.read_text()
