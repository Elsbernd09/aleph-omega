"""
Tests for quotient-category plan artifacts.
"""

from pathlib import Path

from src.rigor.quotient_category_plan import (
    QuotientCategoryPlan,
    QuotientCategoryPlanBuilder,
    QuotientCategoryStep,
)


def test_quotient_category_plan_builds():
    plan = QuotientCategoryPlanBuilder().build()

    assert isinstance(plan, QuotientCategoryPlan)
    assert plan.step_count() >= 6
    assert len(plan.advanced_steps()) >= 3
    assert "QuotientCategoryPlan" in plan.describe()


def test_quotient_category_step_describe():
    plan = QuotientCategoryPlanBuilder().build()
    step = plan.steps[0]

    assert isinstance(step, QuotientCategoryStep)
    assert "QuotientCategoryStep" in step.describe()


def test_quotient_category_markdown_contains_core_claims():
    plan = QuotientCategoryPlanBuilder().build()
    markdown = QuotientCategoryPlanBuilder().to_markdown(plan)

    assert "# Quotient Category Layer" in markdown
    assert "compose_respects_morphism_equivalence" in markdown
    assert "Mathlib category instance" in markdown
    assert "Correct Research Claim" in markdown


def test_quotient_category_plan_write_markdown(tmp_path):
    plan = QuotientCategoryPlanBuilder().build()
    output_path = tmp_path / "lean_quotient_category_layer.md"

    written = QuotientCategoryPlanBuilder().write_markdown(
        plan=plan,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Quotient Category Layer" in written.read_text()
