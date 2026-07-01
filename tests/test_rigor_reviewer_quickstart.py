"""
Tests for reviewer quickstart generation.
"""

from pathlib import Path

from src.rigor.reviewer_quickstart import (
    ReviewerQuickstart,
    ReviewerQuickstartBuilder,
)


def test_reviewer_quickstart_builds():
    quickstart = ReviewerQuickstartBuilder().build()

    assert isinstance(quickstart, ReviewerQuickstart)
    assert quickstart.section_count() >= 5
    assert "ReviewerQuickstart" in quickstart.describe()


def test_reviewer_quickstart_markdown_contains_sections():
    quickstart = ReviewerQuickstartBuilder().build()
    markdown = quickstart.to_markdown()

    assert "# Reviewer Quickstart" in markdown
    assert "Fastest Review Path" in markdown
    assert "Run the Full Test Suite" in markdown
    assert "Correct Interpretation" in markdown


def test_reviewer_quickstart_write_markdown(tmp_path):
    quickstart = ReviewerQuickstartBuilder().build()
    output_path = tmp_path / "reviewer_quickstart.md"

    written = ReviewerQuickstartBuilder().write_markdown(
        quickstart=quickstart,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Reviewer Quickstart" in written.read_text()
