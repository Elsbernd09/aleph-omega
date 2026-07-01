"""
Tests for standalone-to-Mathlib correspondence report.
"""

from pathlib import Path

from src.rigor.mathlib_correspondence_report import (
    MathlibCorrespondenceEntry,
    MathlibCorrespondenceReport,
    MathlibCorrespondenceReportBuilder,
)


def test_mathlib_correspondence_report_builds():
    report = MathlibCorrespondenceReportBuilder().build()

    assert isinstance(report, MathlibCorrespondenceReport)
    assert report.entry_count() >= 10
    assert len(report.strong_entries()) >= 7
    assert len(report.partial_entries()) >= 2
    assert "MathlibCorrespondenceReport" in report.describe()


def test_mathlib_correspondence_entry_describe():
    report = MathlibCorrespondenceReportBuilder().build()
    entry = report.entries[0]

    assert isinstance(entry, MathlibCorrespondenceEntry)
    assert "MathlibCorrespondenceEntry" in entry.describe()


def test_mathlib_correspondence_markdown_contains_core_links():
    report = MathlibCorrespondenceReportBuilder().build()
    markdown = MathlibCorrespondenceReportBuilder().to_markdown(report)

    assert "# Project Aleph-Omega Standalone-to-Mathlib Correspondence Report" in markdown
    assert "AlephOmegaQuotientCategory" in markdown
    assert "quotientFormalSystemCategory" in markdown
    assert "not yet definitionally unified" in markdown
    assert "concrete three-system Lean chain" in markdown


def test_mathlib_correspondence_write_markdown(tmp_path):
    report = MathlibCorrespondenceReportBuilder().build()
    output_path = tmp_path / "mathlib_correspondence_report.md"

    written = MathlibCorrespondenceReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Standalone-to-Mathlib Correspondence Report" in written.read_text()
