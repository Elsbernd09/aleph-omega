"""
Tests for manuscript front matter generation.
"""

from pathlib import Path

from src.rigor.manuscript_front_matter import (
    ManuscriptFrontMatter,
    ManuscriptFrontMatterBuilder,
)


def test_manuscript_front_matter_builds():
    front_matter = ManuscriptFrontMatterBuilder().build()

    assert isinstance(front_matter, ManuscriptFrontMatter)
    assert front_matter.keyword_count() >= 8
    assert front_matter.contribution_count() >= 6
    assert front_matter.word_count() > 200
    assert "ManuscriptFrontMatter" in front_matter.describe()


def test_manuscript_front_matter_markdown_contains_sections():
    front_matter = ManuscriptFrontMatterBuilder().build()
    markdown = front_matter.to_markdown()

    assert "# Project Aleph-Omega" in markdown
    assert "## Short Abstract" in markdown
    assert "## Extended Abstract" in markdown
    assert "## Main Contributions" in markdown
    assert "## Reviewer Summary" in markdown
    assert "## Submission Note" in markdown


def test_manuscript_front_matter_contains_careful_claim_language():
    front_matter = ManuscriptFrontMatterBuilder().build()
    markdown = front_matter.to_markdown()

    assert "does not claim a universal theorem" in markdown
    assert "Lean-checked formal core" in markdown
    assert "not as a fully machine-verified implementation" in markdown


def test_manuscript_front_matter_write_markdown(tmp_path):
    front_matter = ManuscriptFrontMatterBuilder().build()
    output_path = tmp_path / "manuscript_front_matter.md"

    written = ManuscriptFrontMatterBuilder().write_markdown(
        front_matter=front_matter,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Short Abstract" in written.read_text()
