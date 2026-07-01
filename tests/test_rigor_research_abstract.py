"""
Tests for research abstract generation.
"""

from pathlib import Path

from src.rigor.research_abstract import ResearchAbstract, ResearchAbstractBuilder


def test_research_abstract_builds():
    abstract = ResearchAbstractBuilder().build()

    assert isinstance(abstract, ResearchAbstract)
    assert "Project Aleph-Omega" in abstract.title
    assert abstract.word_count() > 50
    assert abstract.keyword_count() >= 5
    assert "ResearchAbstract" in abstract.describe()


def test_research_abstract_markdown():
    abstract = ResearchAbstractBuilder().build()
    markdown = abstract.to_markdown()

    assert "# Project Aleph-Omega" in markdown
    assert "## Abstract" in markdown
    assert "## Keywords" in markdown
    assert "finite model search" in markdown


def test_write_research_abstract(tmp_path):
    abstract = ResearchAbstractBuilder().build()
    output_path = tmp_path / "research_abstract.md"

    written = ResearchAbstractBuilder().write_markdown(
        abstract=abstract,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Project Aleph-Omega" in written.read_text()
