"""
Tests for generated Lean artifact index.
"""

from pathlib import Path

from src.rigor.generated_lean_artifact_index import (
    GeneratedLeanArtifact,
    GeneratedLeanArtifactIndex,
    GeneratedLeanArtifactIndexBuilder,
)


def test_generated_lean_artifact_index_builds():
    index = GeneratedLeanArtifactIndexBuilder().build()

    assert isinstance(index, GeneratedLeanArtifactIndex)
    assert index.artifact_count() >= 9
    assert len(index.standalone_artifacts()) >= 2
    assert len(index.mathlib_artifacts()) >= 5
    assert len(index.quotient_artifacts()) >= 2
    assert len(index.verified_artifacts()) >= 7
    assert "GeneratedLeanArtifactIndex" in index.describe()


def test_generated_lean_artifact_describe():
    index = GeneratedLeanArtifactIndexBuilder().build()
    artifact = index.artifacts[0]

    assert isinstance(artifact, GeneratedLeanArtifact)
    assert "GeneratedLeanArtifact" in artifact.describe()


def test_generated_lean_artifact_index_markdown_contains_core_artifacts():
    index = GeneratedLeanArtifactIndexBuilder().build()
    markdown = GeneratedLeanArtifactIndexBuilder().to_markdown(index)

    assert "# Project Aleph-Omega Generated Lean Artifact Index" in markdown
    assert "ExportedTinyMathlibQuotientComposition" in markdown
    assert "Generated Mathlib checker" in markdown
    assert "quotient composition theorems" in markdown
    assert "Boundary" in markdown


def test_generated_lean_artifact_index_write_markdown(tmp_path):
    index = GeneratedLeanArtifactIndexBuilder().build()
    output_path = tmp_path / "generated_lean_artifact_index.md"

    written = GeneratedLeanArtifactIndexBuilder().write_markdown(
        index=index,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Lean Artifact Index" in written.read_text()
