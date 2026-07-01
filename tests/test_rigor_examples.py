"""
Tests for rigor-track examples and counterexamples.
"""

from src.rigor.examples import (
    ExampleKind,
    RigorExample,
    feature_mismatch_without_used_feature_example,
    identity_preservation_example,
    modal_to_classical_distortion_example,
    paraconsistent_to_classical_distortion_example,
    standard_rigor_examples,
    undefined_translation_failure_example,
)
from src.rigor.theorem import TheoremStatus
from src.rigor.preservation_theorem import PreservationTheoremStatus


def test_modal_to_classical_distortion_example():
    example = modal_to_classical_distortion_example()

    assert isinstance(example, RigorExample)
    assert example.kind == ExampleKind.NONVACUOUS_DISTORTION
    assert example.distortion_check.status == TheoremStatus.VERIFIED_FOR_INSTANCE
    assert example.distortion_check.is_nonvacuous_verification()


def test_paraconsistent_to_classical_distortion_example():
    example = paraconsistent_to_classical_distortion_example()

    assert example.kind == ExampleKind.NONVACUOUS_DISTORTION
    assert example.distortion_check.status == TheoremStatus.VERIFIED_FOR_INSTANCE


def test_identity_preservation_example():
    example = identity_preservation_example()

    assert example.kind == ExampleKind.SATISFACTION_PRESERVATION
    assert example.preservation_check.status == PreservationTheoremStatus.PRESERVES_SATISFACTION
    assert example.preservation_check.is_nonvacuous_preservation()


def test_undefined_translation_failure_example():
    example = undefined_translation_failure_example()

    assert example.kind == ExampleKind.SATISFACTION_FAILURE
    assert example.preservation_check.status == PreservationTheoremStatus.FAILS_SATISFACTION_PRESERVATION
    assert example.preservation_check.distortion_count() >= 1


def test_feature_mismatch_without_used_feature_example_is_vacuous_for_distortion_theorem():
    example = feature_mismatch_without_used_feature_example()

    assert example.kind == ExampleKind.FEATURE_MISMATCH_NO_USED_FEATURE
    assert example.distortion_check.status == TheoremStatus.VACUOUSLY_TRUE_FOR_INSTANCE
    assert example.distortion_check.implication_holds()


def test_standard_rigor_examples():
    examples = standard_rigor_examples()

    assert len(examples) == 5
    names = {example.name for example in examples}

    assert "Modal to Classical Distortion" in names
    assert "Classical Identity Preservation" in names
    assert "Undefined Translation Failure" in names


def test_example_describe():
    example = identity_preservation_example()

    assert "RigorExample" in example.describe()
    assert "Classical Identity Preservation" in example.describe()
