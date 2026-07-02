"""
Tests for nontrivial quotient path equivalence blueprint.
"""

from pathlib import Path

from src.rigor.nontrivial_quotient_path_equivalence_blueprint import (
    NontrivialQuotientPathEquivalenceBlueprint,
    NontrivialQuotientPathEquivalenceBlueprintBuilder,
    QuotientPathEquivalenceRequirement,
)


def test_nontrivial_quotient_path_equivalence_blueprint_builds():
    blueprint = NontrivialQuotientPathEquivalenceBlueprintBuilder().build()

    assert isinstance(blueprint, NontrivialQuotientPathEquivalenceBlueprint)
    assert blueprint.requirement_count() >= 9
    assert len(blueprint.theorem_requirements()) >= 7
    assert len(blueprint.non_rfl_requirements()) >= 3
    assert "NontrivialQuotientPathEquivalenceBlueprint" in blueprint.describe()


def test_quotient_path_equivalence_requirement_describe():
    blueprint = NontrivialQuotientPathEquivalenceBlueprintBuilder().build()
    requirement = blueprint.requirements[0]

    assert isinstance(requirement, QuotientPathEquivalenceRequirement)
    assert "QuotientPathEquivalenceRequirement" in requirement.describe()


def test_nontrivial_quotient_path_equivalence_markdown_contains_core_plan():
    blueprint = NontrivialQuotientPathEquivalenceBlueprintBuilder().build()
    markdown = NontrivialQuotientPathEquivalenceBlueprintBuilder().to_markdown(blueprint)

    assert "# Project Aleph-Omega Nontrivial Quotient Path Equivalence Blueprint" in markdown
    assert "A -> B -> D" in markdown
    assert "A -> C -> D" in markdown
    assert "Quotient.sound" in markdown
    assert "Non-Claim" in markdown


def test_nontrivial_quotient_path_equivalence_write_markdown(tmp_path):
    blueprint = NontrivialQuotientPathEquivalenceBlueprintBuilder().build()
    output_path = tmp_path / "nontrivial_quotient_path_equivalence_blueprint.md"

    written = NontrivialQuotientPathEquivalenceBlueprintBuilder().write_markdown(
        blueprint=blueprint,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Nontrivial Quotient Path Equivalence Blueprint" in written.read_text()
