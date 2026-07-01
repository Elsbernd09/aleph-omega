"""
Tests for repository checklist generation.
"""

from pathlib import Path

from src.rigor.repository_checklist import (
    ChecklistItem,
    RepositoryChecklist,
    RepositoryChecklistBuilder,
)


def test_repository_checklist_builds():
    checklist = RepositoryChecklistBuilder().build()

    assert isinstance(checklist, RepositoryChecklist)
    assert checklist.item_count() > 0
    assert "RepositoryChecklist" in checklist.describe()


def test_repository_checklist_is_complete():
    checklist = RepositoryChecklistBuilder().build()

    assert checklist.complete()
    assert len(checklist.incomplete_items()) == 0


def test_repository_checklist_categories():
    checklist = RepositoryChecklistBuilder().build()
    categories = checklist.categories()

    assert "repository" in categories
    assert "reviewer_readiness" in categories
    assert "research_artifacts" in categories
    assert "verification" in categories


def test_checklist_item_describe():
    item = RepositoryChecklistBuilder().build().items[0]

    assert isinstance(item, ChecklistItem)
    assert "ChecklistItem" in item.describe()
    assert item.status_label() in {"complete", "incomplete"}


def test_repository_checklist_markdown_contains_sections():
    checklist = RepositoryChecklistBuilder().build()
    markdown = RepositoryChecklistBuilder().to_markdown(checklist)

    assert "# Repository Checklist" in markdown
    assert "## Summary" in markdown
    assert "Checklist by Category" in markdown
    assert "Correct Research Framing" in markdown


def test_repository_checklist_write_markdown(tmp_path):
    checklist = RepositoryChecklistBuilder().build()
    output_path = tmp_path / "repository_checklist.md"

    written = RepositoryChecklistBuilder().write_markdown(
        checklist=checklist,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Repository Checklist" in written.read_text()
