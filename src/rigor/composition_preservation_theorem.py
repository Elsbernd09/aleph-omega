"""
Composition Preservation Theorem for Project ℵω.

This theorem studies when satisfaction preservation is stable under bridge
composition.

Informal theorem:

If F: U -> V preserves satisfaction from I_U to I_V, and G: V -> W preserves
satisfaction from I_V to I_W, then the composite G ∘ F preserves satisfaction
from I_U to I_W.

In the finite implementation, this theorem is checked instance-by-instance.
"""

from dataclasses import dataclass
from enum import Enum

from src.rigor.bridge import FiniteBridge
from src.rigor.composition_preservation import (
    CompositionPreservationAnalyzer,
    CompositionPreservationCheck,
    CompositionPreservationStatus,
)
from src.rigor.interpretation import UniverseInterpretation


class CompositionPreservationTheoremStatus(str, Enum):
    """
    Status of the composition preservation theorem.
    """

    VERIFIED_FOR_INSTANCE = "verified_for_instance"
    HYPOTHESIS_FAILS_FOR_INSTANCE = "hypothesis_fails_for_instance"
    FAILED_FOR_INSTANCE = "failed_for_instance"
    NOT_COMPOSABLE = "not_composable"


@dataclass(frozen=True)
class CompositionPreservationTheoremCheck:
    """
    Result of checking the composition preservation theorem for one instance.
    """

    theorem_name: str
    first: FiniteBridge
    second: FiniteBridge
    source_interpretation: UniverseInterpretation
    middle_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    preservation_check: CompositionPreservationCheck
    status: CompositionPreservationTheoremStatus

    def hypothesis_holds(self) -> bool:
        """
        Hypothesis: first leg and second leg preserve satisfaction.
        """

        if self.preservation_check.first_check is None:
            return False

        if self.preservation_check.second_check is None:
            return False

        return (
            self.preservation_check.first_check.preserves_satisfaction()
            and self.preservation_check.second_check.preserves_satisfaction()
        )

    def conclusion_holds(self) -> bool:
        """
        Conclusion: composite preserves satisfaction.
        """

        if self.preservation_check.composite_check is None:
            return False

        return self.preservation_check.composite_check.preserves_satisfaction()

    def implication_holds(self) -> bool:
        """
        Checks hypothesis implies conclusion.
        """

        if not self.hypothesis_holds():
            return True

        return self.conclusion_holds()

    def is_nonvacuous_verification(self) -> bool:
        """
        Returns whether hypothesis and conclusion both hold.
        """

        return (
            self.status == CompositionPreservationTheoremStatus.VERIFIED_FOR_INSTANCE
            and self.hypothesis_holds()
            and self.conclusion_holds()
        )

    def describe(self) -> str:
        """
        Returns a readable theorem check.
        """

        return (
            f"CompositionPreservationTheoremCheck: {self.theorem_name}\n"
            f"First bridge: {self.first.name}\n"
            f"Second bridge: {self.second.name}\n"
            f"Status: {self.status.value}\n"
            f"Hypothesis holds: {self.hypothesis_holds()}\n"
            f"Conclusion holds: {self.conclusion_holds()}\n"
            f"Implication holds: {self.implication_holds()}\n"
            f"Nonvacuous verification: {self.is_nonvacuous_verification()}"
        )


class CompositionPreservationTheorem:
    """
    Finite Composition Preservation Theorem.
    """

    name = "Finite Composition Preservation Theorem"

    def check(
        self,
        first: FiniteBridge,
        second: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        middle_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
    ) -> CompositionPreservationTheoremCheck:
        """
        Checks the theorem for one bridge pair and three interpretations.
        """

        preservation_check = CompositionPreservationAnalyzer().check(
            first=first,
            second=second,
            source_interpretation=source_interpretation,
            middle_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
        )

        if preservation_check.status == CompositionPreservationStatus.NOT_COMPOSABLE:
            status = CompositionPreservationTheoremStatus.NOT_COMPOSABLE
        elif not (
            preservation_check.first_check is not None
            and preservation_check.second_check is not None
            and preservation_check.first_check.preserves_satisfaction()
            and preservation_check.second_check.preserves_satisfaction()
        ):
            status = CompositionPreservationTheoremStatus.HYPOTHESIS_FAILS_FOR_INSTANCE
        elif (
            preservation_check.composite_check is not None
            and preservation_check.composite_check.preserves_satisfaction()
        ):
            status = CompositionPreservationTheoremStatus.VERIFIED_FOR_INSTANCE
        else:
            status = CompositionPreservationTheoremStatus.FAILED_FOR_INSTANCE

        return CompositionPreservationTheoremCheck(
            theorem_name=self.name,
            first=first,
            second=second,
            source_interpretation=source_interpretation,
            middle_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
            preservation_check=preservation_check,
            status=status,
        )

    def theorem_statement(self) -> str:
        """
        Returns a readable theorem statement.
        """

        return (
            "Finite Composition Preservation Theorem:\n\n"
            "Let F: U -> V and G: V -> W be finite bridges. Let I_U, I_V, "
            "and I_W be interpretations of U, V, and W. If F preserves "
            "satisfaction from I_U to I_V, and G preserves satisfaction from "
            "I_V to I_W, then G ∘ F preserves satisfaction from I_U to I_W."
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

    theorem = CompositionPreservationTheorem()
    check = theorem.check(
        first=bridge_one,
        second=bridge_two,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    print(theorem.theorem_statement())
    print()
    print(check.describe())
