"""
Satisfaction Preservation Theorem for Project ℵω.

This module states and checks a stronger theorem using the satisfaction
relation.

The theorem is instance-based and finite:

A bridge preserves satisfaction for an interpreted source/target pair exactly
when every satisfied source statement has a defined translated target statement
that is also satisfied.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.interpretation import UniverseInterpretation
from src.rigor.preservation import (
    BridgePreservationReport,
    PreservationResultStatus,
    SatisfactionPreservationAnalyzer,
)


class PreservationTheoremStatus(str, Enum):
    """
    Status of a satisfaction preservation theorem check.
    """

    PRESERVES_SATISFACTION = "preserves_satisfaction"
    FAILS_SATISFACTION_PRESERVATION = "fails_satisfaction_preservation"
    VACUOUSLY_PRESERVES_SATISFACTION = "vacuously_preserves_satisfaction"


@dataclass(frozen=True)
class SatisfactionPreservationTheoremCheck:
    """
    Result of checking the satisfaction preservation theorem for one bridge and
    two interpretations.
    """

    theorem_name: str
    bridge: FiniteBridge
    source_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    report: BridgePreservationReport
    status: PreservationTheoremStatus

    def satisfied_source_count(self) -> int:
        """
        Counts source statements that are satisfied.
        """

        return sum(
            1
            for result in self.report.results
            if result.source_satisfaction.is_satisfied()
        )

    def has_satisfied_sources(self) -> bool:
        """
        Returns whether the source interpretation satisfies at least one statement.
        """

        return self.satisfied_source_count() > 0

    def distortion_count(self) -> int:
        """
        Counts satisfaction preservation distortions.
        """

        return self.report.distortion_count()

    def preserves_satisfaction(self) -> bool:
        """
        Returns whether satisfaction is preserved for all satisfied source statements.
        """

        return self.report.all_satisfied_sources_preserved()

    def is_nonvacuous_preservation(self) -> bool:
        """
        Returns whether preservation holds and there is at least one satisfied source.
        """

        return (
            self.status == PreservationTheoremStatus.PRESERVES_SATISFACTION
            and self.has_satisfied_sources()
        )

    def describe(self) -> str:
        """
        Returns a readable theorem check.
        """

        return (
            f"SatisfactionPreservationTheoremCheck: {self.theorem_name}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Status: {self.status.value}\n"
            f"Satisfied source count: {self.satisfied_source_count()}\n"
            f"Distortion count: {self.distortion_count()}\n"
            f"Preserves satisfaction: {self.preserves_satisfaction()}\n"
            f"Nonvacuous preservation: {self.is_nonvacuous_preservation()}"
        )


class SatisfactionPreservationTheorem:
    """
    Finite Satisfaction Preservation Theorem.

    A bridge preserves satisfaction for given source and target interpretations
    exactly when every satisfied source statement translates into a satisfied
    target statement.

    If no source statements are satisfied, preservation holds vacuously.
    """

    name = "Finite Satisfaction Preservation Theorem"

    def check(
        self,
        bridge: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
    ) -> SatisfactionPreservationTheoremCheck:
        """
        Checks the theorem for one bridge and interpretation pair.
        """

        report = SatisfactionPreservationAnalyzer().analyze_bridge(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        )

        satisfied_source_count = sum(
            1
            for result in report.results
            if result.source_satisfaction.is_satisfied()
        )

        if satisfied_source_count == 0:
            status = PreservationTheoremStatus.VACUOUSLY_PRESERVES_SATISFACTION
        elif report.has_satisfaction_distortion():
            status = PreservationTheoremStatus.FAILS_SATISFACTION_PRESERVATION
        else:
            status = PreservationTheoremStatus.PRESERVES_SATISFACTION

        return SatisfactionPreservationTheoremCheck(
            theorem_name=self.name,
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
            report=report,
            status=status,
        )

    def check_many(
        self,
        cases: Tuple[
            Tuple[FiniteBridge, UniverseInterpretation, UniverseInterpretation],
            ...
        ],
    ) -> Tuple[SatisfactionPreservationTheoremCheck, ...]:
        """
        Checks many bridge/interpretation cases.
        """

        return tuple(
            self.check(
                bridge=bridge,
                source_interpretation=source_interpretation,
                target_interpretation=target_interpretation,
            )
            for bridge, source_interpretation, target_interpretation in cases
        )

    def theorem_statement(self) -> str:
        """
        Returns the theorem statement in readable form.
        """

        return (
            "Finite Satisfaction Preservation Theorem:\n\n"
            "Let U and V be finite logical universes. Let B: U -> V be a finite "
            "bridge. Let I_U be an interpretation of U and I_V be an interpretation "
            "of V. The bridge B preserves satisfaction from I_U to I_V exactly when "
            "for every statement s in U, if s is satisfied under I_U, then B(s) is "
            "defined and B(s) is satisfied under I_V.\n\n"
            "If there exists a satisfied source statement whose translation is "
            "undefined or not satisfied, then B fails satisfaction preservation."
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

    bridge = identity_bridge(universe)

    theorem = SatisfactionPreservationTheorem()
    check = theorem.check(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    print(theorem.theorem_statement())
    print()
    print(check.describe())
