"""
Tests for public release documentation index.
"""

from pathlib import Path

from src.rigor.public_release_index import (
    PublicReleaseDocument,
    PublicReleaseIndex,
    PublicReleaseIndexBuilder,
)


def test_public_release_index_builds():
    index = PublicReleaseIndexBuilder().build()

    assert isinstance(index, PublicReleaseIndex)
    assert index.document_count() >= 10
    assert len(index.completed_documents()) >= 10
    assert "PublicReleaseIndex" in index.describe()


def test_public_release_document_describe():
    index = PublicReleaseIndexBuilder().build()
    document = index.documents[0]

    assert isinstance(document, PublicReleaseDocument)
    assert "PublicReleaseDocument" in document.describe()


def test_public_release_index_markdown_contains_core_documents():
    index = PublicReleaseIndexBuilder().build()
    markdown = PublicReleaseIndexBuilder().to_markdown(index)

    assert "# Project Aleph-Omega Public Release Documentation Index" in markdown
    assert "README.md" in markdown
    assert "docs/project_aleph_omega_manuscript.md" in markdown
    assert "docs/manuscript_theorem_inventory.md" in markdown
    assert "./scripts/check_formal_stack.sh" in markdown
    assert "Claim Boundary" in markdown


def test_public_release_index_write_markdown(tmp_path):
    index = PublicReleaseIndexBuilder().build()
    output_path = tmp_path / "public_release_index.md"

    written = PublicReleaseIndexBuilder().write_markdown(
        index=index,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Public Release Documentation Index" in written.read_text()
