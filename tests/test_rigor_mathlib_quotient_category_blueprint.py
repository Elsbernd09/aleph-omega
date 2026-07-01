"""
Tests for Mathlib quotient-category blueprint.
"""

from pathlib import Path

from src.rigor.mathlib_quotient_category_blueprint import (
    QuotientCategoryBlueprint,
    QuotientCategoryBlueprintBuilder,
    QuotientCategoryObstacle,
)


def test_quotient_category_blueprint_builds():
    blueprint = QuotientCategoryBlueprintBuilder().build()

    assert isinstance(blueprint, QuotientCategoryBlueprint)
    assert blueprint.obstacle_count() >= 7
    assert len(blueprint.hard_obstacles()) >= 4
    assert "QuotientCategoryBlueprint" in blueprint.describe()


def test_quotient_category_obstacle_describe():
    blueprint = QuotientCategoryBlueprintBuilder().build()
    obstacle = blueprint.obstacles[0]

    assert isinstance(obstacle, QuotientCategoryObstacle)
    assert "QuotientCategoryObstacle" in obstacle.describe()


def test_quotient_category_blueprint_markdown_contains_core_plan():
    blueprint = QuotientCategoryBlueprintBuilder().build()
    markdown = QuotientCategoryBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Mathlib Quotient Category Blueprint" in markdown
    assert "representative choice" in markdown
    assert "Quotient.liftOn" in markdown or "Quotient" in markdown
    assert "equivalence classes of PreservationMorphism" in markdown
    assert "Non-Claim" in markdown


def test_quotient_category_blueprint_write_markdown(tmp_path):
    blueprint = QuotientCategoryBlueprintBuilder().build()
    output_path = tmp_path / "mathlib_quotient_category_blueprint.md"

    written = QuotientCategoryBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Quotient Category Blueprint" in written.read_text()
