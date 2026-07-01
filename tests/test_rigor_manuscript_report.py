"""
Tests for Project Aleph-Omega manuscript generation.
"""

from pathlib import Path

from src.rigor.manuscript_report import (
    ManuscriptReport,
    ManuscriptReportBuilder,
    ManuscriptSection,
)


def test_manuscript_report_builds():
    report = ManuscriptReportBuilder().build()

    assert isinstance(report, ManuscriptReport)
    assert report.section_count() >= 15
    assert report.word_count() > 1000
    assert "ManuscriptReport" in report.describe()


def test_manuscript_sections_build():
    report = ManuscriptReportBuilder().build()
    section = report.sections[0]

    assert isinstance(section, ManuscriptSection)
    assert section.word_count() > 10
    assert section.to_markdown().startswith("## ")


def test_manuscript_markdown_contains_key_claims():
    report = ManuscriptReportBuilder().build()
    markdown = report.to_markdown()

    assert "# Project Aleph-Omega" in markdown
    assert "Lean Formal Core" in markdown
    assert "Standalone Quotient Category" in markdown
    assert "Concrete Finite Lean Examples" in markdown
    assert "Careful Final Claim" in markdown


def test_manuscript_write_markdown(tmp_path):
    report = ManuscriptReportBuilder().build()
    output_path = tmp_path / "project_aleph_omega_manuscript.md"

    written = ManuscriptReportBuilder().write_markdown(
        report=report,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Project Aleph-Omega" in written.read_text()
