"""
Tests for generated diamond diagram data model.
"""

from pathlib import Path

import pytest

from src.rigor.generated_diamond_diagram_model import (
    GeneratedDiamondDiagram,
    GeneratedDiamondDiagramDocumenter,
    build_standard_diamond_diagram,
)


def test_standard_diamond_diagram_builds_and_validates():
    diagram = build_standard_diamond_diagram()
    diagram.validate()

    assert isinstance(diagram, GeneratedDiamondDiagram)
    assert len(diagram.systems()) == 4
    assert len(diagram.morphisms()) == 4
    assert diagram.paths_agree_on_models()
    assert diagram.paths_agree_on_sentences()
    assert "GeneratedDiamondDiagram" in diagram.describe()


def test_standard_diamond_upper_and_lower_paths_agree():
    diagram = build_standard_diamond_diagram()

    for model in diagram.source.models:
        assert diagram.upper_path_model_map(model) == diagram.lower_path_model_map(model)

    for sentence in diagram.source.sentences:
        assert diagram.upper_path_sentence_map(sentence) == diagram.lower_path_sentence_map(sentence)


def test_standard_diamond_contains_expected_morphisms():
    diagram = build_standard_diamond_diagram()
    names = {morphism.name for morphism in diagram.morphisms()}

    assert "DiamondMorphismAB" in names
    assert "DiamondMorphismAC" in names
    assert "DiamondMorphismBD" in names
    assert "DiamondMorphismCD" in names


def test_diamond_rejects_broken_path_agreement():
    diagram = build_standard_diamond_diagram()

    broken_lower_to_target = type(diagram.lower_to_target)(
        name=diagram.lower_to_target.name,
        source=diagram.lower_to_target.source,
        target=diagram.lower_to_target.target,
        model_map={"c0": "d1", "c1": "d0"},
        sentence_map=diagram.lower_to_target.sentence_map,
    )

    broken = type(diagram)(
        name=diagram.name,
        source=diagram.source,
        upper=diagram.upper,
        lower=diagram.lower,
        target=diagram.target,
        source_to_upper=diagram.source_to_upper,
        source_to_lower=diagram.source_to_lower,
        upper_to_target=diagram.upper_to_target,
        lower_to_target=broken_lower_to_target,
        description=diagram.description,
    )

    with pytest.raises(ValueError):
        broken.validate()


def test_generated_diamond_docs_write(tmp_path):
    diagram = build_standard_diamond_diagram()
    output_path = tmp_path / "generated_diamond_diagram_model.md"

    written = GeneratedDiamondDiagramDocumenter().write_markdown(
        diagram=diagram,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()

    text = written.read_text()
    assert "Generated Diamond Diagram Data Model" in text
    assert "A -> B -> D" in text
    assert "equal as quotient morphisms" in text
