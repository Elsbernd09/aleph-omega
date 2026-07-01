"""
Preservation under bridge composition.

This module studies whether satisfaction preservation survives composition.

If:

F: U -> V
G: V -> W

and interpretations are given on U, V, and W, then we can compare:

1. F preserves satisfaction from U to V
2. G preserves satisfaction from V to W
3. G ∘ F preserves satisfaction from U to W

This prepares the project for a composition preservation theorem.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.rigor.bridge import FiniteBridge
from src.rigor.composition import compose_bridges
from src.rigor.interpretation import UniverseInterpretation
from src.rigor.preservation_theorem import (
    SatisfactionPreservationTheorem,
    SatisfactionPreservationTheoremCheck,
)


class CompositionPreservationStatus(str, Enum):
    """
    Status of preservation under composition.
    """

    PRESERVED_THROUGH_COMPOSITION = "preserved_through_composition"
    FIRST_LEG_FAILS = "first_leg_fails"
    SECOND_LEG_FAILS = "second_leg_fails"
    COMPOSITE_FAILS = "composite_fails"
    NOT_COMPOSABLE = "not_composable"


@dataclass(frozen=True)
class CompositionPreservationCheck:
    """
    Checks preservation through a composable bridge pair.
    """

    first: FiniteBridge
    second: FiniteBridge
    composite: Optional[FiniteBridge]
    source_interpretation: UniverseInterpretation
    middle_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    first_check: Optional[SatisfactionPreservationTheoremCheck]
    second_check: Optional[SatisfactionPreservationTheoremCheck]
    composite_check: Optional[SatisfactionPreservationTheoremCheck]
    status: CompositionPreservationStatus
    explanation: str = ""

    def is_successful(self) -> bool:
        """
        Returns whether preservation succeeds through composition.
        """

        return self.status == CompositionPreservationStatus.PRESERVED_THROUGH_COMPOSITION

    def describe(self) -> str:
        """
        Returns a readable composition preservation check.
        """

        composite_name = self.composite.name if self.composite is not None else "none"

        return (
            f"CompositionPreservationCheck\n"
            f"First bridge: {self.first.name}\n"
            f"Second bridge: {self.second.name}\n"
            f"Composite: {composite_name}\n"
            f"Status: {self.status.value}\n"
            f"Successful: {self.is_successful()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


class CompositionPreservationAnalyzer:
    """
    Analyzes preservation under bridge composition.
    """

    def __init__(self) -> None:
        self.theorem = SatisfactionPreservationTheorem()

    def check(
        self,
        first: FiniteBridge,
        second: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        middle_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
    ) -> CompositionPreservationCheck:
        """
        Checks whether preservation passes through second ∘ first.
        """

        composition_result = compose_bridges(first, second)

        if composition_result.composite is None:
            return CompositionPreservationCheck(
                first=first,
                second=second,
                composite=None,
                source_interpretation=source_interpretation,
                middle_interpretation=middle_interpretation,
                target_interpretation=target_interpretation,
                first_check=None,
                second_check=None,
                composite_check=None,
                status=CompositionPreservationStatus.NOT_COMPOSABLE,
                explanation="The bridges are not composable.",
            )

        composite = composition_result.composite

        first_check = self.theorem.check(
            bridge=first,
            source_interpretation=source_interpretation,
            target_interpretation=middle_interpretation,
        )

        second_check = self.theorem.check(
            bridge=second,
            source_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
        )

        composite_check = self.theorem.check(
            bridge=composite,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        )

        if not first_check.preserves_satisfaction():
            status = CompositionPreservationStatus.FIRST_LEG_FAILS
            explanation = "The first bridge fails satisfaction preservation."
        elif not second_check.preserves_satisfaction():
            status = CompositionPreservationStatus.SECOND_LEG_FAILS
            explanation = "The second bridge fails satisfaction preservation."
        elif not composite_check.preserves_satisfaction():
            status = CompositionPreservationStatus.COMPOSITE_FAILS
            explanation = "Both legs preserve satisfaction, but the composite fails."
        else:
            status = CompositionPreservationStatus.PRESERVED_THROUGH_COMPOSITION
            explanation = "Both legs and the composite preserve satisfaction."

        return CompositionPreservationCheck(
            first=first,
            second=second,
            composite=composite,
            source_interpretation=source_interpretation,
            middle_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
            first_check=first_check,
            second_check=second_check,
            composite_check=composite_check,
            status=status,
            explanation=explanation,
        )


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
    from src.rigor.finite_universe import classical_finite_universe
    from src.rigor.interpretation import constant_interpretation
    from src.rigor.semantics import FiniteTruthValue, classical_truth_space

    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    bridge_one = identity_bridge(universe)
    bridge_two = identity_bridge(universe)

    check = CompositionPreservationAnalyzer().check(
        first=bridge_one,
        second=bridge_two,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    print(check.describe())
