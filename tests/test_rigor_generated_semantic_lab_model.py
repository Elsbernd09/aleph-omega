"""
Tests for generated finite semantic lab data model.
"""

from pathlib import Path

import pytest

from src.rigor.generated_semantic_lab_model import (
    GeneratedSemanticLab,
    GeneratedSemanticLabChain,
    GeneratedSemanticLabModelDocumenter,
    build_standard_semantic_lab,
)


def test_standard_semantic_lab_builds_and_validates():
    lab = build_standard_semantic_lab()
    lab.validate()

    assert isinstance(lab, GeneratedSemanticLab)
    assert lab.chain_count() == 3
    assert lab.system_count() == 4
    assert lab.morphism_count() == 3
    assert "GeneratedSemanticLab" in lab.describe()


def test_standard_semantic_lab_contains_expected_chains():
    lab = build_standard_semantic_lab()
    names = {chain.name for chain in lab.chains}

    assert "TwoSystemChain" in names
    assert "ThreeSystemChain" in names
    assert "FourSystemChain" in names


def test_semantic_lab_chain_describe():
    lab = build_standard_semantic_lab()
    chain = lab.chains[0]

    assert isinstance(chain, GeneratedSemanticLabChain)
    assert chain.system_count() == 2
    assert chain.morphism_count() == 1
    assert "GeneratedSemanticLabChain" in chain.describe()


def test_semantic_lab_rejects_empty_lab():
    bad_lab = GeneratedSemanticLab(name="", chains=())

    with pytest.raises(ValueError):
        bad_lab.validate()


def test_semantic_lab_model_docs_write(tmp_path):
    lab = build_standard_semantic_lab()
    output_path = tmp_path / "generated_semantic_lab_model.md"

    written = GeneratedSemanticLabModelDocumenter().write_markdown(
        lab=lab,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()

    text = written.read_text()
    assert "Generated Semantic Lab Data Model" in text
    assert "FourSystemChain" in text
    assert "multiple finite systems" in text
