"""
Tests for Mathlib integration feasibility report.
"""

from pathlib import Path

from src.rigor.mathlib_integration_feasibility import (
    MathlibFeasibilityReport,
    MathlibFeasibilityReportBuilder,
    MathlibRequirement,
)


def test_mathlib_feasibility_report_builds():
    report = MathlibFeasibilityReportBuilder().build()

    assert isinstance(report, MathlibFeasibilityReport)
    assert report.requirement_count() >= 8
    assert len(report.high_difficulty_requirements()) >= 3
    assert "MathlibFeasibilityReport" in report.describe()


def test_mathlib_requirement_describe():
    report = MathlibFeasibilityReportBuilder().build()
    requirement = report.requirements[0]

    assert isinstance(requirement, MathlibRequirement)
    assert "MathlibRequirement" in requirement.describe()


def test_mathlib_feasibility_markdown_contains_core_boundaries():
    report = MathlibFeasibilityReportBuilder().build()
    markdown = MathlibFeasibilityReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Mathlib Integration Feasibility Report" in markdown
    assert "Mathlib `Category` instance" in markdown
    assert "quotient morphisms" in markdown
    assert "universe levels" in markdown
    assert "Non-Claim" in markdown


def test_mathlib_feasibility_write_markdown(tmp_path):
    report = MathlibFeasibilityReportBuilder().build()
    output_path = tmp_path / "mathlib_integration_feasibility.md"

    written = MathlibFeasibilityReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Mathlib Integration Feasibility Report" in written.read_text()
