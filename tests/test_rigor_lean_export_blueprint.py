"""
Tests for Python-to-Lean export blueprint.
"""

from pathlib import Path

from src.rigor.lean_export_blueprint import (
    LeanExportBlueprint,
    LeanExportBlueprintBuilder,
    LeanExportRequirement,
)


def test_lean_export_blueprint_builds():
    blueprint = LeanExportBlueprintBuilder().build()

    assert isinstance(blueprint, LeanExportBlueprint)
    assert blueprint.requirement_count() >= 8
    assert "LeanExportBlueprint" in blueprint.describe()


def test_lean_export_requirement_describe():
    blueprint = LeanExportBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, LeanExportRequirement)
    assert "LeanExportRequirement" in requirement.describe()


def test_lean_export_blueprint_markdown_contains_core_plan():
    blueprint = LeanExportBlueprintBuilder().build()
    markdown = LeanExportBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Python-to-Lean Export Blueprint" in markdown
    assert "inductive Model" in markdown
    assert "Sat := fun m φ" in markdown
    assert "PreservationMorphism" in markdown
    assert "Non-Claim" in markdown


def test_lean_export_blueprint_write_markdown(tmp_path):
    blueprint = LeanExportBlueprintBuilder().build()
    output_path = tmp_path / "lean_export_blueprint.md"

    written = LeanExportBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Python-to-Lean Export Blueprint" in written.read_text()
