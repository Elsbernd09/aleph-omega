"""
Tests for categorical examples.
"""

from src.rigor.category_examples import (
    CategoryExample,
    CategoryExampleKind,
    collapse_structure_example,
    custom_chain_category_example,
    identity_law_example,
    standard_category_examples,
    starter_category_example,
)


def test_starter_category_example():
    example = starter_category_example()

    assert isinstance(example, CategoryExample)
    assert example.kind == CategoryExampleKind.STARTER_CATEGORY
    assert example.is_well_behaved()
    assert example.category.object_count() == 2


def test_identity_law_example():
    example = identity_law_example()

    assert example.kind == CategoryExampleKind.IDENTITY_LAW
    assert example.is_well_behaved()
    assert example.category.object_count() == 1
    assert example.category.morphism_count() == 1


def test_collapse_structure_example():
    example = collapse_structure_example()

    assert example.kind == CategoryExampleKind.COLLAPSE_STRUCTURE
    assert example.is_well_behaved()
    assert example.category.object_count() == 2
    assert example.category.morphism_count() == 3


def test_custom_chain_category_example():
    example = custom_chain_category_example()

    assert example.kind == CategoryExampleKind.COMPOSITION_CHAIN
    assert example.is_well_behaved()
    assert example.category.object_count() == 4
    assert example.category.morphism_count() >= 7


def test_standard_category_examples():
    examples = standard_category_examples()

    assert len(examples) == 4
    assert all(example.is_well_behaved() for example in examples)

    names = {example.name for example in examples}
    assert "Starter Finite Universe Category Example" in names
    assert "Custom Composition Chain Example" in names


def test_category_example_describe():
    example = starter_category_example()

    description = example.describe()

    assert "CategoryExample" in description
    assert "Identity laws hold: True" in description
    assert "Associativity holds: True" in description
