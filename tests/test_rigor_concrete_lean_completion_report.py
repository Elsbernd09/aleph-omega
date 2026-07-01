"""
Tests for concrete Lean completion report.
"""

from pathlib import Path

from src.rigor.concrete_lean_completion_report import (
    ConcreteLeanClaim,
    ConcreteLeanCompletionReport,
    ConcreteLeanCompletionReportBuilder,
)


def test_concrete_lean_completion_report_builds():
    report = ConcreteLeanCompletionReportBuilder().build()

    assert isinstance(report, ConcreteLeanCompletionReport)
    assert report.claim_count() >= 10
    assert len(report.lean_checked_claims()) >= 7
    assert "ConcreteLeanCompletionReport" in report.describe()


def test_concrete_lean_claim_describe():
    report = ConcreteLeanCompletionReportBuilder().build()
    claim = report.claims[0]

    assert isinstance(claim, ConcreteLeanClaim)
    assert "ConcreteLeanClaim" in claim.describe()


def test_concrete_lean_markdown_contains_key_claims():
    report = ConcreteLeanCompletionReportBuilder().build()
    markdown = ConcreteLeanCompletionReportBuilder().to_markdown(report)

    assert "# Concrete Lean Structures Completion Report" in markdown
    assert "twoToThirdComposite" in markdown
    assert "quotient_category_composes_concrete_chain" in markdown
    assert "Strongest Current Claim" in markdown
    assert "small finite examples" in markdown


def test_concrete_lean_write_markdown(tmp_path):
    report = ConcreteLeanCompletionReportBuilder().build()
    output_path = tmp_path / "concrete_lean_completion_report.md"

    written = ConcreteLeanCompletionReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Concrete Lean Structures Completion Report" in written.read_text()
