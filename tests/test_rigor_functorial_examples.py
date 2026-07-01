"""
Tests for functorial semantics examples.
"""

from src.rigor.composition_preservation_theorem import (
    CompositionPreservationTheoremStatus,
)
from src.rigor.distortion_accumulation import DistortionAccumulationStatus
from src.rigor.functorial_examples import (
    FunctorialExampleKind,
    FunctorialSemanticsExample,
    first_leg_distortion_example,
    identity_transport_example,
    preserved_composition_example,
    second_leg_distortion_example,
    standard_functorial_examples,
)
from src.rigor.semantic_transport import TransportStatus


def test_identity_transport_example():
    example = identity_transport_example()

    assert isinstance(example, FunctorialSemanticsExample)
    assert example.kind == FunctorialExampleKind.IDENTITY_TRANSPORT
    assert example.first_transport.status == TransportStatus.SUCCESS
    assert example.theorem_check.status == CompositionPreservationTheoremStatus.VERIFIED_FOR_INSTANCE
    assert example.distortion_report.status == DistortionAccumulationStatus.NO_DISTORTION
    assert example.is_semantically_well_behaved()


def test_preserved_composition_example():
    example = preserved_composition_example()

    assert example.kind == FunctorialExampleKind.PRESERVED_COMPOSITION
    assert example.theorem_check.status == CompositionPreservationTheoremStatus.VERIFIED_FOR_INSTANCE
    assert example.distortion_report.status == DistortionAccumulationStatus.NO_DISTORTION
    assert example.is_semantically_well_behaved()


def test_first_leg_distortion_example():
    example = first_leg_distortion_example()

    assert example.kind == FunctorialExampleKind.FIRST_LEG_DISTORTION
    assert example.theorem_check.status == CompositionPreservationTheoremStatus.HYPOTHESIS_FAILS_FOR_INSTANCE
    assert example.distortion_report.first_distortion_count() == 1
    assert not example.is_semantically_well_behaved()


def test_second_leg_distortion_example():
    example = second_leg_distortion_example()

    assert example.kind == FunctorialExampleKind.SECOND_LEG_DISTORTION
    assert example.theorem_check.status == CompositionPreservationTheoremStatus.HYPOTHESIS_FAILS_FOR_INSTANCE
    assert example.distortion_report.second_distortion_count() == 1
    assert not example.is_semantically_well_behaved()


def test_standard_functorial_examples():
    examples = standard_functorial_examples()

    assert len(examples) == 4

    names = {example.name for example in examples}

    assert "Identity Transport Example" in names
    assert "Preserved Composition Example" in names
    assert "First-Leg Distortion Example" in names
    assert "Second-Leg Distortion Example" in names


def test_functorial_example_describe():
    example = preserved_composition_example()
    description = example.describe()

    assert "FunctorialSemanticsExample" in description
    assert "Semantically well behaved: True" in description
