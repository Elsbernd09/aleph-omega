"""
Tests for verification report generation.
"""

from pathlib import Path

from src.rigor.verification_report import (
    VerificationReport,
    VerificationReportBuilder,
)


def test_verification_report_exists():
    report = VerificationReportBuilder().build()

    assert isinstance(report, VerificationReport)
    assert report.claim_count() >= 5
    assert "VerificationReport" in report.describe()


def test_verification_report_counts():
    report = VerificationReportBuilder().build()

    assert report.strongly_verified_count() > 0
    assert report.conjectural_count() > 0
    assert report.audit_failure_count() == 0
    assert report.verification_health_passes()


def test_verification_report_has_open_obligations():
    report = VerificationReportBuilder().build()

    assert report.open_obligation_count() > 0


def test_verification_report_markdown_contains_sections():
    report = VerificationReportBuilder().build()
    markdown = VerificationReportBuilder().to_markdown(report)

    assert "# Verification Report" in markdown
    assert "Registered Claims" in markdown
    assert "Audit Summary" in markdown
    assert "Open Proof Obligations" in markdown
    assert "Correct Research Framing" in markdown


def test_verification_report_write_markdown(tmp_path):
    report = VerificationReportBuilder().build()
    output_path = tmp_path / "verification_report.md"

    written = VerificationReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Verification Report" in written.read_text()
