"""
Tests for generated finite semantic lab blueprint.
"""

from pathlib import Path

from src.rigor.generated_semantic_lab_blueprint import (
    GeneratedSemanticLabBlueprint,
    GeneratedSemanticLabBlueprintBuilder,
    GeneratedSemanticLabRequirement,
)


def test_generated_semantic_lab_blueprint_builds():
    blueprint = GeneratedSemanticLabBlueprintBuilder().build()

    assert isinstance(blueprint, GeneratedSemanticLabBlueprint)
    assert blueprint.requirement_count() >= 8
    assert len(blueprint.quotient_requirements()) >= 2
    assert len(blueprint.verified_requirements()) >= 6
    assert "GeneratedSemanticLabBlueprint" in blueprint.describe()


def test_generated_semantic_lab_requirement_describe():
    blueprint = GeneratedSemanticLabBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, GeneratedSemanticLabRequirement)
    assert "GeneratedSemanticLabRequirement" in requirement.describe()


def test_generated_semantic_lab_blueprint_markdown_contains_core_plan():
    blueprint = GeneratedSemanticLabBlueprintBuilder().build()
    markdown = GeneratedSemanticLabBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Generated Finite Semantic Lab Blueprint" in markdown
    assert "Phase 34" in markdown
    assert "finite semantic laboratory" in markdown
    assert "four-system extended chain" in markdown
    assert "Non-Claim" in markdown


def test_generated_semantic_lab_blueprint_write_markdown(tmp_path):
    blueprint = GeneratedSemanticLabBlueprintBuilder().build()
    output_path = tmp_path / "generated_semantic_lab_blueprint.md"

    written = GeneratedSemanticLabBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Finite Semantic Lab Blueprint" in written.read_text()
