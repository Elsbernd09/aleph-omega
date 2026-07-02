"""
Tests for generated semantic lab artifact index.
"""

from pathlib import Path

from src.rigor.generated_semantic_lab_artifact_index import (
    GeneratedSemanticLabArtifactIndex,
    GeneratedSemanticLabArtifactIndexBuilder,
    GeneratedSemanticLabIndexedArtifact,
)


def test_generated_semantic_lab_artifact_index_builds():
    index = GeneratedSemanticLabArtifactIndexBuilder().build()

    assert isinstance(index, GeneratedSemanticLabArtifactIndex)
    assert index.artifact_count() >= 13
    assert len(index.system_artifacts()) >= 4
    assert len(index.morphism_artifacts()) >= 3
    assert len(index.quotient_artifacts()) >= 5
    assert len(index.theorem_artifacts()) >= 2
    assert "GeneratedSemanticLabArtifactIndex" in index.describe()


def test_generated_semantic_lab_indexed_artifact_describe():
    index = GeneratedSemanticLabArtifactIndexBuilder().build()
    artifact = index.artifacts[0]

    assert isinstance(artifact, GeneratedSemanticLabIndexedArtifact)
    assert "GeneratedSemanticLabIndexedArtifact" in artifact.describe()


def test_generated_semantic_lab_artifact_index_markdown_contains_core_artifacts():
    index = GeneratedSemanticLabArtifactIndexBuilder().build()
    markdown = GeneratedSemanticLabArtifactIndexBuilder().to_markdown(index)

    assert "# Project Aleph-Omega Generated Semantic Lab Artifact Index" in markdown
    assert "LabSystemASystem" in markdown
    assert "LabMorphismABMorphism" in markdown
    assert "q_category_lab_composition_abc" in markdown
    assert "Boundary" in markdown


def test_generated_semantic_lab_artifact_index_write_markdown(tmp_path):
    index = GeneratedSemanticLabArtifactIndexBuilder().build()
    output_path = tmp_path / "generated_semantic_lab_artifact_index.md"

    written = GeneratedSemanticLabArtifactIndexBuilder().write_markdown(
        index=index,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Generated Semantic Lab Artifact Index" in written.read_text()
