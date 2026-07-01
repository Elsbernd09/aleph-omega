"""
Tests for public quickstart generation.
"""

from pathlib import Path

from src.rigor.public_quickstart import (
    PublicQuickstart,
    PublicQuickstartBuilder,
    QuickstartStep,
)


def test_public_quickstart_builds():
    quickstart = PublicQuickstartBuilder().build()

    assert isinstance(quickstart, PublicQuickstart)
    assert quickstart.step_count() >= 6
    assert "PublicQuickstart" in quickstart.describe()


def test_quickstart_step_markdown():
    quickstart = PublicQuickstartBuilder().build()
    step = quickstart.steps[0]

    assert isinstance(step, QuickstartStep)
    assert "QuickstartStep" in step.describe()
    assert "```bash" in step.to_markdown()


def test_public_quickstart_markdown_contains_core_commands():
    quickstart = PublicQuickstartBuilder().build()
    markdown = quickstart.to_markdown()

    assert "# Project Aleph-Omega Quickstart" in markdown
    assert "./scripts/check_lean.sh" in markdown
    assert "./scripts/check_lake.sh" in markdown
    assert "./scripts/check_formal_stack.sh" in markdown
    assert "python3 -m pytest" in markdown
    assert "Aleph-Omega formal stack verified successfully." in markdown


def test_public_quickstart_write_markdown(tmp_path):
    quickstart = PublicQuickstartBuilder().build()
    output_path = tmp_path / "quickstart.md"

    written = PublicQuickstartBuilder().write_markdown(
        quickstart=quickstart,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Project Aleph-Omega Quickstart" in written.read_text()
