"""
Distortion accumulation for composed finite bridges.

This module studies how satisfaction distortion appears across a two-step
bridge chain:

F: U -> V
G: V -> W

The composite is:

G ∘ F: U -> W

The goal is to identify whether distortion appears in the first leg, second
leg, composite, or multiple places.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from src.rigor.bridge import FiniteBridge
from src.rigor.composition import compose_bridges
from src.rigor.interpretation import UniverseInterpretation
from src.rigor.preservation import BridgePreservationReport, SatisfactionPreservationAnalyzer


class DistortionAccumulationStatus(str, Enum):
    """
    Status of distortion accumulation across a bridge chain.
    """

    NO_DISTORTION = "no_distortion"
    FIRST_LEG_DISTORTION = "first_leg_distortion"
    SECOND_LEG_DISTORTION = "second_leg_distortion"
    COMPOSITE_DISTORTION = "composite_distortion"
    MULTIPLE_DISTORTIONS = "multiple_distortions"
    NOT_COMPOSABLE = "not_composable"


@dataclass(frozen=True)
class DistortionAccumulationReport:
    """
    Report describing distortion across a composed bridge pair.
    """

    first: FiniteBridge
    second: FiniteBridge
    composite: Optional[FiniteBridge]
    source_interpretation: UniverseInterpretation
    middle_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    first_report: Optional[BridgePreservationReport]
    second_report: Optional[BridgePreservationReport]
    composite_report: Optional[BridgePreservationReport]
    status: DistortionAccumulationStatus
    explanation: str = ""

    def first_distortion_count(self) -> int:
        """
        Counts first-leg distortions.
        """

        if self.first_report is None:
            return 0

        return self.first_report.distortion_count()

    def second_distortion_count(self) -> int:
        """
        Counts second-leg distortions.
        """

        if self.second_report is None:
            return 0

        return self.second_report.distortion_count()

    def composite_distortion_count(self) -> int:
        """
        Counts composite distortions.
        """

        if self.composite_report is None:
            return 0

        return self.composite_report.distortion_count()

    def total_distortion_pressure(self) -> int:
        """
        Total distortion count across first, second, and composite reports.
        """

        return (
            self.first_distortion_count()
            + self.second_distortion_count()
            + self.composite_distortion_count()
        )

    def has_any_distortion(self) -> bool:
        """
        Returns whether any distortion appears.
        """

        return self.total_distortion_pressure() > 0

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        composite_name = self.composite.name if self.composite is not None else "none"

        return (
            f"DistortionAccumulationReport\n"
            f"First bridge: {self.first.name}\n"
            f"Second bridge: {self.second.name}\n"
            f"Composite: {composite_name}\n"
            f"Status: {self.status.value}\n"
            f"First distortion count: {self.first_distortion_count()}\n"
            f"Second distortion count: {self.second_distortion_count()}\n"
            f"Composite distortion count: {self.composite_distortion_count()}\n"
            f"Total distortion pressure: {self.total_distortion_pressure()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


class DistortionAccumulationAnalyzer:
    """
    Analyzes distortion accumulation through bridge composition.
    """

    def __init__(self) -> None:
        self.preservation_analyzer = SatisfactionPreservationAnalyzer()

    def analyze(
        self,
        first: FiniteBridge,
        second: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        middle_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
    ) -> DistortionAccumulationReport:
        """
        Analyzes distortion across first, second, and composite bridges.
        """

        composition_result = compose_bridges(first, second)

        if composition_result.composite is None:
            return DistortionAccumulationReport(
                first=first,
                second=second,
                composite=None,
                source_interpretation=source_interpretation,
                middle_interpretation=middle_interpretation,
                target_interpretation=target_interpretation,
                first_report=None,
                second_report=None,
                composite_report=None,
                status=DistortionAccumulationStatus.NOT_COMPOSABLE,
                explanation="The bridges are not composable.",
            )

        composite = composition_result.composite

        first_report = self.preservation_analyzer.analyze_bridge(
            bridge=first,
            source_interpretation=source_interpretation,
            target_interpretation=middle_interpretation,
        )

        second_report = self.preservation_analyzer.analyze_bridge(
            bridge=second,
            source_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
        )

        composite_report = self.preservation_analyzer.analyze_bridge(
            bridge=composite,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
        )

        first_has = first_report.has_satisfaction_distortion()
        second_has = second_report.has_satisfaction_distortion()
        composite_has = composite_report.has_satisfaction_distortion()

        distortion_sites = sum([first_has, second_has, composite_has])

        if distortion_sites == 0:
            status = DistortionAccumulationStatus.NO_DISTORTION
            explanation = "No satisfaction distortion appears in either leg or the composite."
        elif distortion_sites > 1:
            status = DistortionAccumulationStatus.MULTIPLE_DISTORTIONS
            explanation = "Distortion appears in multiple parts of the bridge chain."
        elif first_has:
            status = DistortionAccumulationStatus.FIRST_LEG_DISTORTION
            explanation = "Distortion first appears in the first bridge."
        elif second_has:
            status = DistortionAccumulationStatus.SECOND_LEG_DISTORTION
            explanation = "Distortion appears in the second bridge."
        else:
            status = DistortionAccumulationStatus.COMPOSITE_DISTORTION
            explanation = "Distortion appears only at the composite level."

        return DistortionAccumulationReport(
            first=first,
            second=second,
            composite=composite,
            source_interpretation=source_interpretation,
            middle_interpretation=middle_interpretation,
            target_interpretation=target_interpretation,
            first_report=first_report,
            second_report=second_report,
            composite_report=composite_report,
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

    first = identity_bridge(universe)
    second = identity_bridge(universe)

    report = DistortionAccumulationAnalyzer().analyze(
        first=first,
        second=second,
        source_interpretation=interpretation,
        middle_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    print(report.describe())
