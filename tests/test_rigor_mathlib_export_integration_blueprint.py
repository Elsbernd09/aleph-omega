"""
Tests for Mathlib export integration blueprint.
"""

from pathlib import Path

from src.rigor.mathlib_export_integration_blueprint import (
    MathlibExportIntegrationBlueprint,
    MathlibExportIntegrationBlueprintBuilder,
    MathlibExportIntegrationRequirement,
)


def test_mathlib_export_integration_blueprint_builds():
    blueprint = MathlibExportIntegrationBlueprintBuilder().build()

    assert isinstance(blueprint, MathlibExportIntegrationBlueprint)
    assert blueprint.requirement_count() >= 8
    assert len(blueprint.mathlib_targets()) >= 7
    assert "MathlibExportIntegrationBlueprint" in blueprint.describe()


def test_mathlib_export_integration_requirement_describe():
    blueprint = MathlibExportIntegrationBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, MathlibExportIntegrationRequirement)
    assert "MathlibExportIntegrationRequirement" in requirement.describe()


def test_mathlib_export_integration_markdown_contains_core_plan():
    blueprint = MathlibExportIntegrationBlueprintBuilder().build()
    markdown = MathlibExportIntegrationBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Mathlib Export Integration Blueprint" in markdown
    assert "Phase 32" in markdown
    assert "AlephOmegaMathlib.FormalSystemCategory" in markdown
    assert "formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/" in markdown
    assert "Non-Claim" in markdown


def test_mathlib_export_integration_write_markdown(tmp_path):
    blueprint = MathlibExportIntegrationBlueprintBuilder().build()
    output_path = tmp_path / "mathlib_export_integration_blueprint.md"

    written = MathlibExportIntegrationBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Export Integration Blueprint" in written.read_text()
