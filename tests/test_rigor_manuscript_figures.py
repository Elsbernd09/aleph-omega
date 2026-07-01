"""
Tests for manuscript figure generation.
"""

from pathlib import Path

from src.rigor.manuscript_figures import (
    ManuscriptFigure,
    ManuscriptFigureBuilder,
    ManuscriptFigureSet,
)


def test_manuscript_figure_set_builds():
    figure_set = ManuscriptFigureBuilder().build()

    assert isinstance(figure_set, ManuscriptFigureSet)
    assert figure_set.figure_count() >= 6
    assert "ManuscriptFigureSet" in figure_set.describe()


def test_manuscript_figure_builds():
    figure_set = ManuscriptFigureBuilder().build()
    figure = figure_set.figures[0]

    assert isinstance(figure, ManuscriptFigure)
    assert figure.number == "1"
    assert "ManuscriptFigure" in figure.describe()
    assert "```text" in figure.to_markdown()


def test_manuscript_figures_markdown_contains_key_diagrams():
    figure_set = ManuscriptFigureBuilder().build()
    markdown = figure_set.to_markdown()

    assert "# Project Aleph-Omega Manuscript Figures" in markdown
    assert "Project Architecture" in markdown
    assert "Lean Theorem Flow" in markdown
    assert "Concrete Lean Chain" in markdown
    assert "Claim Boundary" in markdown


def test_manuscript_figures_write_markdown(tmp_path):
    figure_set = ManuscriptFigureBuilder().build()
    output_path = tmp_path / "manuscript_figures.md"

    written = ManuscriptFigureBuilder().write_markdown(
        figure_set=figure_set,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Manuscript Figures" in written.read_text()
