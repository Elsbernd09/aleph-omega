"""
Examples and counterexamples for the Project ℵω rigor track.

This module collects finite theorem examples showing:
- nonvacuous bridge distortion,
- vacuous theorem cases,
- satisfaction preservation,
- satisfaction preservation failure,
- feature mismatch without theorem applicability.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge, collapse_bridge, identity_bridge
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
    modal_finite_universe,
    paraconsistent_finite_universe,
)
from src.rigor.interpretation import UniverseInterpretation, constant_interpretation
from src.rigor.preservation_theorem import (
    SatisfactionPreservationTheorem,
    SatisfactionPreservationTheoremCheck,
)
from src.rigor.semantics import FiniteTruthValue, classical_truth_space, modal_truth_space
from src.rigor.theorem import BridgeDistortionTheorem, TheoremCheck


class ExampleKind(str, Enum):
    """
    Kind of rigor-track example.
    """

    NONVACUOUS_DISTORTION = "nonvacuous_distortion"
    VACUOUS_DISTORTION = "vacuous_distortion"
    SATISFACTION_PRESERVATION = "satisfaction_preservation"
    SATISFACTION_FAILURE = "satisfaction_failure"
    FEATURE_MISMATCH_NO_USED_FEATURE = "feature_mismatch_no_used_feature"


@dataclass(frozen=True)
class RigorExample:
    """
    A documented mathematical example or counterexample.
    """

    name: str
    kind: ExampleKind
    bridge: FiniteBridge
    distortion_check: TheoremCheck
    preservation_check: SatisfactionPreservationTheoremCheck
    explanation: str

    def describe(self) -> str:
        """
        Returns a readable example description.
        """

        return (
            f"RigorExample: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Distortion theorem status: {self.distortion_check.status.value}\n"
            f"Preservation theorem status: {self.preservation_check.status.value}\n"
            f"Explanation: {self.explanation}"
        )


def modal_to_classical_distortion_example() -> RigorExample:
    """
    Nonvacuous example of feature distortion from modal to classical.
    """

    source = modal_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Modal to Classical Distortion Example",
        source=source,
        target=target,
    )

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=modal_truth_space(),
        value=FiniteTruthValue.NECESSARY_TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=target,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    return RigorExample(
        name="Modal to Classical Distortion",
        kind=ExampleKind.NONVACUOUS_DISTORTION,
        bridge=bridge,
        distortion_check=BridgeDistortionTheorem().check(bridge),
        preservation_check=SatisfactionPreservationTheorem().check(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        ),
        explanation=(
            "A modal source universe has necessity and possibility features absent "
            "from the classical target universe, so feature distortion occurs."
        ),
    )


def paraconsistent_to_classical_distortion_example() -> RigorExample:
    """
    Nonvacuous example of contradiction-tolerance loss.
    """

    source = paraconsistent_finite_universe()
    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Paraconsistent to Classical Distortion Example",
        source=source,
        target=target,
    )

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=target,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    return RigorExample(
        name="Paraconsistent to Classical Distortion",
        kind=ExampleKind.NONVACUOUS_DISTORTION,
        bridge=bridge,
        distortion_check=BridgeDistortionTheorem().check(bridge),
        preservation_check=SatisfactionPreservationTheorem().check(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        ),
        explanation=(
            "A paraconsistent statement requiring contradiction tolerance is translated "
            "into a classical target that lacks contradiction tolerance."
        ),
    )


def identity_preservation_example() -> RigorExample:
    """
    Example where identity bridge preserves satisfaction.
    """

    universe = classical_finite_universe()
    bridge = identity_bridge(universe)

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    return RigorExample(
        name="Classical Identity Preservation",
        kind=ExampleKind.SATISFACTION_PRESERVATION,
        bridge=bridge,
        distortion_check=BridgeDistortionTheorem().check(bridge),
        preservation_check=SatisfactionPreservationTheorem().check(
            bridge=bridge,
            source_interpretation=interpretation,
            target_interpretation=interpretation,
        ),
        explanation=(
            "The identity bridge on a classical universe preserves satisfied classical "
            "statements."
        ),
    )


def undefined_translation_failure_example() -> RigorExample:
    """
    Example where a satisfied source statement has no target translation.
    """

    universe = classical_finite_universe()
    bridge = FiniteBridge(
        name="Undefined Translation Failure Example",
        source=universe,
        target=universe,
        mapping={},
    )

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    return RigorExample(
        name="Undefined Translation Failure",
        kind=ExampleKind.SATISFACTION_FAILURE,
        bridge=bridge,
        distortion_check=BridgeDistortionTheorem().check(bridge),
        preservation_check=SatisfactionPreservationTheorem().check(
            bridge=bridge,
            source_interpretation=interpretation,
            target_interpretation=interpretation,
        ),
        explanation=(
            "The source statement is satisfied, but the bridge is undefined, so "
            "satisfaction preservation fails."
        ),
    )


def feature_mismatch_without_used_feature_example() -> RigorExample:
    """
    Example where source has an extra feature, but no statement uses it.

    This shows why the theorem needs the hypothesis that some statement requires
    an absent feature.
    """

    statement = FiniteStatement.from_features(
        name="plain_classical_statement",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    source = FiniteLogicalUniverse.build(
        name="Richer Source With Unused Extra Feature",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ],
        statements=[statement],
    )

    target = classical_finite_universe()

    bridge = collapse_bridge(
        name="Unused Feature Collapse Example",
        source=source,
        target=target,
    )

    source_interpretation = constant_interpretation(
        universe=source,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=target,
        truth_space=classical_truth_space(),
        value=FiniteTruthValue.TRUE,
    )

    return RigorExample(
        name="Feature Mismatch Without Used Feature",
        kind=ExampleKind.FEATURE_MISMATCH_NO_USED_FEATURE,
        bridge=bridge,
        distortion_check=BridgeDistortionTheorem().check(bridge),
        preservation_check=SatisfactionPreservationTheorem().check(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        ),
        explanation=(
            "The source universe supports an extra modal feature, but the only source "
            "statement does not require it. This makes the distortion theorem's main "
            "hypothesis false."
        ),
    )


def standard_rigor_examples() -> Tuple[RigorExample, ...]:
    """
    Returns all standard examples.
    """

    return (
        modal_to_classical_distortion_example(),
        paraconsistent_to_classical_distortion_example(),
        identity_preservation_example(),
        undefined_translation_failure_example(),
        feature_mismatch_without_used_feature_example(),
    )


if __name__ == "__main__":
    for example in standard_rigor_examples():
        print(example.describe())
        print()
