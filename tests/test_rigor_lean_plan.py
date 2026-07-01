"""
Tests for Lean formalization plan generation.
"""

from pathlib import Path

from src.rigor.lean_plan import (
    LeanFormalizationPlan,
    LeanFormalizationPlanBuilder,
    LeanFormalizationTarget,
)


def test_lean_plan_builds():
    plan = LeanFormalizationPlanBuilder().build()

    assert isinstance(plan, LeanFormalizationPlan)
    assert plan.target_count() >= 5
    assert len(plan.highest_priority_targets()) > 0
    assert "LeanFormalizationPlan" in plan.describe()


def test_lean_target_describe():
    plan = LeanFormalizationPlanBuilder().build()
    target = plan.targets[0]

    assert isinstance(target, LeanFormalizationTarget)
    assert "LeanFormalizationTarget" in target.describe()
    assert target.priority >= 1


def test_lean_plan_markdown_contains_sections():
    plan = LeanFormalizationPlanBuilder().build()
    markdown = LeanFormalizationPlanBuilder().to_markdown(plan)

    assert "# Lean Formalization Plan" in markdown
    assert "First Lean Milestone" in markdown
    assert "Correct Research Framing" in markdown
    assert "identity morphism preserves satisfaction" in markdown


def test_lean_plan_write_markdown(tmp_path):
    plan = LeanFormalizationPlanBuilder().build()
    output_path = tmp_path / "lean_formalization_plan.md"

    written = LeanFormalizationPlanBuilder().write_markdown(
        plan=plan,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Lean Formalization Plan" in written.read_text()
