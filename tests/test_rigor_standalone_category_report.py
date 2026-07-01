"""
Tests for standalone category completion report artifacts.
"""

from pathlib import Path

from src.rigor.standalone_category_report import (
    StandaloneCategoryClaim,
    StandaloneCategoryCompletionReport,
    StandaloneCategoryCompletionReportBuilder,
)


def test_standalone_category_report_builds():
    report = StandaloneCategoryCompletionReportBuilder().build()

    assert isinstance(report, StandaloneCategoryCompletionReport)
    assert report.claim_count() >= 8
    assert len(report.lean_checked_claims()) >= 5
    assert "StandaloneCategoryCompletionReport" in report.describe()


def test_standalone_category_claim_describe():
    report = StandaloneCategoryCompletionReportBuilder().build()
    claim = report.claims[0]

    assert isinstance(claim, StandaloneCategoryClaim)
    assert "StandaloneCategoryClaim" in claim.describe()


def test_standalone_category_report_markdown_contains_key_claims():
    report = StandaloneCategoryCompletionReportBuilder().build()
    markdown = StandaloneCategoryCompletionReportBuilder().to_markdown(report)

    assert "# Standalone Quotient Category Completion Report" in markdown
    assert "AlephOmegaQuotientCategory" in markdown
    assert "StandaloneQuotientCategory" in markdown
    assert "Strongest Current Claim" in markdown
    assert "not yet a Mathlib Category instance" in markdown


def test_standalone_category_report_write_markdown(tmp_path):
    report = StandaloneCategoryCompletionReportBuilder().build()
    output_path = tmp_path / "standalone_category_completion_report.md"

    written = StandaloneCategoryCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Standalone Quotient Category Completion Report" in written.read_text()
