"""
Tests for artifact index generation.
"""

from pathlib import Path

from src.rigor.artifact_index import (
    ArtifactIndex,
    ArtifactIndexBuilder,
    ArtifactIndexItem,
)


def test_artifact_index_builds():
    index = ArtifactIndexBuilder().build()

    assert isinstance(index, ArtifactIndex)
    assert index.item_count() > 0
    assert "ArtifactIndex" in index.describe()


def test_artifact_index_items_exist():
    index = ArtifactIndexBuilder().build()

    assert len(index.existing_items()) > 0
    assert index.complete()
    assert len(index.missing_items()) == 0


def test_artifact_index_categories():
    index = ArtifactIndexBuilder().build()
    categories = index.categories()

    assert "research_artifact" in categories
    assert "model_search" in categories
    assert "verification" in categories
    assert "failure_lab" in categories


def test_artifact_index_item_describe():
    item = ArtifactIndexBuilder().build().items[0]

    assert isinstance(item, ArtifactIndexItem)
    assert "ArtifactIndexItem" in item.describe()


def test_artifact_index_markdown_contains_sections():
    index = ArtifactIndexBuilder().build()
    markdown = ArtifactIndexBuilder().to_markdown(index)

    assert "# Artifact Index" in markdown
    assert "## Summary" in markdown
    assert "Artifacts by Category" in markdown
    assert "Correct Research Framing" in markdown


def test_artifact_index_write_markdown(tmp_path):
    index = ArtifactIndexBuilder().build()
    output_path = tmp_path / "artifact_index.md"

    written = ArtifactIndexBuilder().write_markdown(
        index=index,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Artifact Index" in written.read_text()
