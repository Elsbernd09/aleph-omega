"""
Tests for quotient category completion report artifacts.
"""

from pathlib import Path

from src.rigor.quotient_category_report import (
    LeanQuotientClaim,
    QuotientCategoryCompletionReport,
    QuotientCategoryCompletionReportBuilder,
)


def test_quotient_category_completion_report_builds():
    report = QuotientCategoryCompletionReportBuilder().build()

    assert isinstance(report, QuotientCategoryCompletionReport)
    assert report.claim_count() >= 10
    assert len(report.machine_checked_claims()) >= 7
    assert "QuotientCategoryCompletionReport" in report.describe()


def test_lean_quotient_claim_describe():
    report = QuotientCategoryCompletionReportBuilder().build()
    claim = report.claims[0]

    assert isinstance(claim, LeanQuotientClaim)
    assert "LeanQuotientClaim" in claim.describe()


def test_quotient_category_report_markdown_contains_key_claims():
    report = QuotientCategoryCompletionReportBuilder().build()
    markdown = QuotientCategoryCompletionReportBuilder().to_markdown(report)

    assert "# Quotient Category Completion Report" in markdown
    assert "quotient_composition_well_defined" in markdown
    assert "quotient_associativity" in markdown
    assert "Strongest Current Claim" in markdown
    assert "not a complete Mathlib Category instance" in markdown


def test_quotient_category_report_write_markdown(tmp_path):
    report = QuotientCategoryCompletionReportBuilder().build()
    output_path = tmp_path / "quotient_category_completion_report.md"

    written = QuotientCategoryCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Quotient Category Completion Report" in written.read_text()
