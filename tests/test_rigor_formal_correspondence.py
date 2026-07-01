"""
Tests for Lean/Python formal correspondence manifest.
"""

from pathlib import Path

from src.rigor.formal_correspondence import (
    FormalCorrespondenceBuilder,
    FormalCorrespondenceEntry,
    FormalCorrespondenceManifest,
)


def test_formal_correspondence_manifest_builds():
    manifest = FormalCorrespondenceBuilder().build()

    assert isinstance(manifest, FormalCorrespondenceManifest)
    assert manifest.entry_count() >= 10
    assert len(manifest.lean_checked_entries()) >= 4
    assert len(manifest.python_implemented_entries()) >= 5
    assert "FormalCorrespondenceManifest" in manifest.describe()


def test_formal_correspondence_entry_describe():
    manifest = FormalCorrespondenceBuilder().build()
    entry = manifest.entries[0]

    assert isinstance(entry, FormalCorrespondenceEntry)
    assert "FormalCorrespondenceEntry" in entry.describe()


def test_formal_correspondence_markdown_contains_key_artifacts():
    manifest = FormalCorrespondenceBuilder().build()
    markdown = FormalCorrespondenceBuilder().to_markdown(manifest)

    assert "# Lean/Python Formal Correspondence Manifest" in markdown
    assert "PreservationMorphism" in markdown
    assert "AlephOmegaQuotientCategory" in markdown
    assert "Strongest Correct Claim" in markdown
    assert "not fully machine-verified" in markdown


def test_formal_correspondence_write_markdown(tmp_path):
    manifest = FormalCorrespondenceBuilder().build()
    output_path = tmp_path / "formal_correspondence_manifest.md"

    written = FormalCorrespondenceBuilder().write_markdown(
        manifest=manifest,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Lean/Python Formal Correspondence Manifest" in written.read_text()
