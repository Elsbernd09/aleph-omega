"""
Tests for architecture map generation.
"""

from pathlib import Path

from src.rigor.architecture_map import (
    ArchitectureLayer,
    ArchitectureMap,
    ArchitectureMapBuilder,
)


def test_architecture_map_builds():
    architecture_map = ArchitectureMapBuilder().build()

    assert isinstance(architecture_map, ArchitectureMap)
    assert architecture_map.layer_count() >= 8
    assert architecture_map.total_file_count() > 0
    assert "ArchitectureMap" in architecture_map.describe()


def test_architecture_layers_have_files_and_outputs():
    architecture_map = ArchitectureMapBuilder().build()

    assert all(isinstance(layer, ArchitectureLayer) for layer in architecture_map.layers)
    assert all(layer.file_count() > 0 for layer in architecture_map.layers)
    assert all(layer.output_count() > 0 for layer in architecture_map.layers)


def test_architecture_map_contains_key_layers():
    architecture_map = ArchitectureMapBuilder().build()
    names = architecture_map.layer_names()

    assert "Finite Universe Layer" in names
    assert "Finite Model Search Layer" in names
    assert "Verification Interface Layer" in names
    assert "Research Artifact Layer" in names


def test_architecture_map_markdown_contains_sections():
    architecture_map = ArchitectureMapBuilder().build()
    markdown = ArchitectureMapBuilder().to_markdown(architecture_map)

    assert "# Architecture Map" in markdown
    assert "## Summary" in markdown
    assert "## Layers" in markdown
    assert "Correct Research Framing" in markdown


def test_architecture_map_write_markdown(tmp_path):
    architecture_map = ArchitectureMapBuilder().build()
    output_path = tmp_path / "architecture_map.md"

    written = ArchitectureMapBuilder().write_markdown(
        architecture_map=architecture_map,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Architecture Map" in written.read_text()
