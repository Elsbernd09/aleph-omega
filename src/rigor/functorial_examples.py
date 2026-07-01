"""
Functorial semantics examples for Project ℵω.

These examples connect:

- bridge composition,
- semantic transport,
- satisfaction preservation,
- composition preservation,
- distortion accumulation.

The goal is to show when semantic preservation behaves well under composition
and when distortion appears in a bridge chain.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge, identity_bridge
from src.rigor.composition_preservation_theorem import (
    CompositionPreservationTheorem,
    CompositionPreservationTheoremCheck,
)
from src.rigor.distortion_accumulation import (
    DistortionAccumulationAnalyzer,
    DistortionAccumulationReport,
)
from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
    classical_finite_universe,
)
from src.rigor.interpretation import UniverseInterpretation, constant_interpretation
from src.rigor.semantic_transport import SemanticTransportReport, SemanticTransporter
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


class FunctorialExampleKind(str, Enum):
    """
    Kinds of functorial semantics examples.
    """

    IDENTITY_TRANSPORT = "identity_transport"
    PRESERVED_COMPOSITION = "preserved_composition"
    FIRST_LEG_DISTORTION = "first_leg_distortion"
    SECOND_LEG_DISTORTION = "second_leg_distortion"
    TRANSPORT_CHAIN = "transport_chain"


@dataclass(frozen=True)
class FunctorialSemanticsExample:
    """
    Example connecting bridge composition and semantics.
    """

    name: str
    kind: FunctorialExampleKind
    first: FiniteBridge
    second: FiniteBridge
    source_interpretation: UniverseInterpretation
    middle_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    first_transport: SemanticTransportReport
    theorem_check: CompositionPreservationTheoremCheck
    distortion_report: DistortionAccumulationReport
    explanation: str

    def is_semantically_well_behaved(self) -> bool:
        """
        Returns whether the composition theorem verifies and no distortion accumulates.
        """

        return (
            self.theorem_check.is_nonvacuous_verification()
            and not self.distortion_report.has_any_distortion()
        )

    def describe(self) -> str:
        """
        Returns a readable example description.
        """

        return (
            f"FunctorialSemanticsExample: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"First bridge: {self.first.name}\n"
            f"Second bridge: {self.second.name}\n"
            f"Transport status: {self.first_transport.status.value}\n"
            f"Composition theorem status: {self.theorem_check.status.value}\n"
            f"Distortion status: {self.distortion_report.status.value}\n"
            f"Semantically well behaved: {self.is_semantically_well_behaved()}\n"
            f"Explanation: {self.explanation}"
        )


def make_three_universe_chain():
    """
    Builds a simple chain A -> B -> C with one classical statement in each universe.
    """

    statement_a = FiniteStatement.from_features(
        name="a",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    statement_b = FiniteStatement.from_features(
        name="b",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    statement_c = FiniteStatement.from_features(
        name="c",
        features=[SemanticFeature.CLASSICAL_TRUTH],
    )

    universe_a = FiniteLogicalUniverse.build(
        name="Functorial Universe A",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_a],
    )

    universe_b = FiniteLogicalUniverse.build(
        name="Functorial Universe B",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_b],
    )

    universe_c = FiniteLogicalUniverse.build(
        name="Functorial Universe C",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=[statement_c],
    )

    first = FiniteBridge(
        name="F: A to B",
        source=universe_a,
        target=universe_b,
        mapping={statement_a: statement_b},
    )

    second = FiniteBridge(
        name="G: B to C",
        source=universe_b,
        target=universe_c,
        mapping={statement_b: statement_c},
    )

    return universe_a, universe_b, universe_c, first, second


def preserved_composition_example() -> FunctorialSemanticsExample:
    """
    Example where both legs and the composite preserve satisfaction.
    """

    universe_a, universe_b, universe_c, first, second = make_three_universe_chain()
    truth_space = classical_truth_space()

    source_interpretation = constant_interpretation(
        universe=universe_a,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    middle_interpretation = constant_interpretation(
        universe=universe_b,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=universe_c,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    first_transport = SemanticTransporter().transport(
        bridge=first,
        source_interpretation=source_interpretation,
        target_truth_space=truth_space,
    )

    theorem_check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    distortion_report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    return FunctorialSemanticsExample(
        name="Preserved Composition Example",
        kind=FunctorialExampleKind.PRESERVED_COMPOSITION,
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
        first_transport=first_transport,
        theorem_check=theorem_check,
        distortion_report=distortion_report,
        explanation=(
            "Every statement is interpreted as true. Both bridge legs preserve "
            "satisfaction, and the composite preserves satisfaction."
        ),
    )


def first_leg_distortion_example() -> FunctorialSemanticsExample:
    """
    Example where distortion enters at the first bridge.
    """

    universe_a, universe_b, universe_c, first, second = make_three_universe_chain()
    truth_space = classical_truth_space()

    source_interpretation = constant_interpretation(
        universe=universe_a,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    middle_interpretation = constant_interpretation(
        universe=universe_b,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    target_interpretation = constant_interpretation(
        universe=universe_c,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    first_transport = SemanticTransporter().transport(
        bridge=first,
        source_interpretation=source_interpretation,
        target_truth_space=truth_space,
    )

    theorem_check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    distortion_report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    return FunctorialSemanticsExample(
        name="First-Leg Distortion Example",
        kind=FunctorialExampleKind.FIRST_LEG_DISTORTION,
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
        first_transport=first_transport,
        theorem_check=theorem_check,
        distortion_report=distortion_report,
        explanation=(
            "The source statement is satisfied, but its middle translation is not "
            "satisfied, so distortion enters at the first bridge."
        ),
    )


def second_leg_distortion_example() -> FunctorialSemanticsExample:
    """
    Example where distortion enters at the second bridge.
    """

    universe_a, universe_b, universe_c, first, second = make_three_universe_chain()
    truth_space = classical_truth_space()

    source_interpretation = constant_interpretation(
        universe=universe_a,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    middle_interpretation = constant_interpretation(
        universe=universe_b,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    target_interpretation = constant_interpretation(
        universe=universe_c,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    first_transport = SemanticTransporter().transport(
        bridge=first,
        source_interpretation=source_interpretation,
        target_truth_space=truth_space,
    )

    theorem_check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    distortion_report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
    )

    return FunctorialSemanticsExample(
        name="Second-Leg Distortion Example",
        kind=FunctorialExampleKind.SECOND_LEG_DISTORTION,
        first=first,
        second=second,
        source_interpretation=source_interpretation,
        middle_interpretation=middle_interpretation,
        target_interpretation=target_interpretation,
        first_transport=first_transport,
        theorem_check=theorem_check,
        distortion_report=distortion_report,
        explanation=(
            "The first bridge preserves satisfaction, but the second bridge maps a "
            "satisfied middle statement to an unsatisfied target statement."
        ),
    )


def identity_transport_example() -> FunctorialSemanticsExample:
    """
    Example where identity transport preserves a classical interpretation.
    """

    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    first_transport = SemanticTransporter().transport(
        bridge=first,
        source_interpretation=interpretation,
        target_truth_space=truth_space,
    )

    theorem_check = CompositionPreservationTheorem().check(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    distortion_report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    return FunctorialSemanticsExample(
        name="Identity Transport Example",
        kind=FunctorialExampleKind.IDENTITY_TRANSPORT,
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
        first_transport=first_transport,
        theorem_check=theorem_check,
        distortion_report=distortion_report,
        explanation=(
            "Identity transport sends each statement to itself and preserves its "
            "truth-value assignment."
        ),
    )


def standard_functorial_examples() -> Tuple[FunctorialSemanticsExample, ...]:
    """
    Returns all standard functorial semantics examples.
    """

    return (
        identity_transport_example(),
        preserved_composition_example(),
        first_leg_distortion_example(),
        second_leg_distortion_example(),
    )


if __name__ == "__main__":
    for example in standard_functorial_examples():
        print(example.describe())
        print()
