"""
Tests for semantic lab expansion blueprint.
"""

from pathlib import Path

from src.rigor.semantic_lab_expansion_blueprint import (
    SemanticLabExpansionBlueprint,
    SemanticLabExpansionBlueprintBuilder,
    SemanticLabExpansionRequirement,
)


def test_semantic_lab_expansion_blueprint_builds():
    blueprint = SemanticLabExpansionBlueprintBuilder().build()

    assert isinstance(blueprint, SemanticLabExpansionBlueprint)
    assert blueprint.requirement_count() >= 8
    assert len(blueprint.diagram_requirements()) >= 5
    assert len(blueprint.quotient_requirements()) >= 2
    assert len(blueprint.verified_requirements()) >= 7
    assert "SemanticLabExpansionBlueprint" in blueprint.describe()


def test_semantic_lab_expansion_requirement_describe():
    blueprint = SemanticLabExpansionBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, SemanticLabExpansionRequirement)
    assert "SemanticLabExpansionRequirement" in requirement.describe()


def test_semantic_lab_expansion_markdown_contains_core_plan():
    blueprint = SemanticLabExpansionBlueprintBuilder().build()
    markdown = SemanticLabExpansionBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Semantic Lab Expansion Blueprint" in markdown
    assert "Phase 35" in markdown
    assert "diamond diagram" in markdown
    assert "quotient-category commutativity theorem" in markdown
    assert "Non-Claim" in markdown


def test_semantic_lab_expansion_write_markdown(tmp_path):
    blueprint = SemanticLabExpansionBlueprintBuilder().build()
    output_path = tmp_path / "semantic_lab_expansion_blueprint.md"

    written = SemanticLabExpansionBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Semantic Lab Expansion Blueprint" in written.read_text()
