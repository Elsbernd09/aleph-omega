"""
Satisfaction-based semantic preservation for the Project ℵω rigor track.

This module strengthens bridge distortion analysis by defining preservation
through satisfaction.

A bridge preserves satisfaction for a statement when:

- the source statement is satisfied under the source interpretation; and
- the translated target statement is also satisfied under the target interpretation.

If the source is satisfied but the target translation is not satisfied, then
the bridge creates satisfaction distortion.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from src.rigor.bridge import FiniteBridge, BridgeTranslation
from src.rigor.finite_universe import FiniteStatement
from src.rigor.interpretation import UniverseInterpretation
from src.rigor.satisfaction import (
    SatisfactionChecker,
    SatisfactionResult,
    SatisfactionStatus,
)


class PreservationResultStatus(str, Enum):
    """
    Status of satisfaction preservation under a bridge.
    """

    PRESERVED = "preserved"
    SOURCE_NOT_SATISFIED = "source_not_satisfied"
    TARGET_NOT_SATISFIED = "target_not_satisfied"
    UNDEFINED_TRANSLATION = "undefined_translation"


@dataclass(frozen=True)
class SatisfactionPreservationResult:
    """
    Preservation result for one translated statement.
    """

    source_statement: FiniteStatement
    target_statement: Optional[FiniteStatement]
    bridge_translation: BridgeTranslation
    source_satisfaction: SatisfactionResult
    target_satisfaction: Optional[SatisfactionResult]
    status: PreservationResultStatus
    explanation: str = ""

    def is_preserved(self) -> bool:
        """
        Returns whether satisfaction was preserved.
        """

        return self.status == PreservationResultStatus.PRESERVED

    def is_distorted(self) -> bool:
        """
        Returns whether satisfaction preservation failed after source satisfaction.
        """

        return self.status in {
            PreservationResultStatus.TARGET_NOT_SATISFIED,
            PreservationResultStatus.UNDEFINED_TRANSLATION,
        }

    def describe(self) -> str:
        """
        Returns a readable result description.
        """

        target = self.target_statement.name if self.target_statement else "undefined"
        target_status = (
            self.target_satisfaction.status.value
            if self.target_satisfaction is not None
            else "none"
        )

        return (
            f"SatisfactionPreservationResult\n"
            f"Source statement: {self.source_statement.name}\n"
            f"Target statement: {target}\n"
            f"Source satisfaction: {self.source_satisfaction.status.value}\n"
            f"Target satisfaction: {target_status}\n"
            f"Status: {self.status.value}\n"
            f"Preserved: {self.is_preserved()}\n"
            f"Distorted: {self.is_distorted()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


@dataclass(frozen=True)
class BridgePreservationReport:
    """
    Satisfaction preservation report for a bridge.
    """

    bridge: FiniteBridge
    source_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    results: Tuple[SatisfactionPreservationResult, ...]

    def preserved_results(self) -> Tuple[SatisfactionPreservationResult, ...]:
        """
        Returns preserved results.
        """

        return tuple(result for result in self.results if result.is_preserved())

    def distorted_results(self) -> Tuple[SatisfactionPreservationResult, ...]:
        """
        Returns distorted results.
        """

        return tuple(result for result in self.results if result.is_distorted())

    def preserved_count(self) -> int:
        """
        Counts preserved results.
        """

        return len(self.preserved_results())

    def distortion_count(self) -> int:
        """
        Counts satisfaction distortions.
        """

        return len(self.distorted_results())

    def has_satisfaction_distortion(self) -> bool:
        """
        Returns whether any satisfied source statement fails after translation.
        """

        return self.distortion_count() > 0

    def all_satisfied_sources_preserved(self) -> bool:
        """
        Returns whether all satisfied source statements are preserved.
        """

        return not self.has_satisfaction_distortion()

    def describe(self) -> str:
        """
        Returns a readable report description.
        """

        return (
            f"BridgePreservationReport\n"
            f"Bridge: {self.bridge.name}\n"
            f"Source interpretation: {self.source_interpretation.truth_space.name}\n"
            f"Target interpretation: {self.target_interpretation.truth_space.name}\n"
            f"Preserved count: {self.preserved_count()}\n"
            f"Distortion count: {self.distortion_count()}\n"
            f"All satisfied sources preserved: {self.all_satisfied_sources_preserved()}"
        )


class SatisfactionPreservationAnalyzer:
    """
    Analyzes whether a bridge preserves satisfaction.
    """

    def __init__(self) -> None:
        self.satisfaction_checker = SatisfactionChecker()

    def analyze_statement(
        self,
        bridge: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
        statement: FiniteStatement,
    ) -> SatisfactionPreservationResult:
        """
        Analyzes satisfaction preservation for one source statement.
        """

        bridge_translation = bridge.translate(statement)

        source_satisfaction = self.satisfaction_checker.check_statement(
            source_interpretation,
            statement,
        )

        if not source_satisfaction.is_satisfied():
            return SatisfactionPreservationResult(
                source_statement=statement,
                target_statement=bridge_translation.target_statement,
                bridge_translation=bridge_translation,
                source_satisfaction=source_satisfaction,
                target_satisfaction=None,
                status=PreservationResultStatus.SOURCE_NOT_SATISFIED,
                explanation=(
                    "The source statement is not satisfied, so preservation is not required."
                ),
            )

        if bridge_translation.target_statement is None:
            return SatisfactionPreservationResult(
                source_statement=statement,
                target_statement=None,
                bridge_translation=bridge_translation,
                source_satisfaction=source_satisfaction,
                target_satisfaction=None,
                status=PreservationResultStatus.UNDEFINED_TRANSLATION,
                explanation=(
                    "The source statement is satisfied, but the bridge is undefined on it."
                ),
            )

        target_satisfaction = self.satisfaction_checker.check_statement(
            target_interpretation,
            bridge_translation.target_statement,
        )

        if not target_satisfaction.is_satisfied():
            return SatisfactionPreservationResult(
                source_statement=statement,
                target_statement=bridge_translation.target_statement,
                bridge_translation=bridge_translation,
                source_satisfaction=source_satisfaction,
                target_satisfaction=target_satisfaction,
                status=PreservationResultStatus.TARGET_NOT_SATISFIED,
                explanation=(
                    "The source statement is satisfied, but the translated target statement "
                    "is not satisfied."
                ),
            )

        return SatisfactionPreservationResult(
            source_statement=statement,
            target_statement=bridge_translation.target_statement,
            bridge_translation=bridge_translation,
            source_satisfaction=source_satisfaction,
            target_satisfaction=target_satisfaction,
            status=PreservationResultStatus.PRESERVED,
            explanation="The source statement and translated target statement are both satisfied.",
        )

    def analyze_bridge(
        self,
        bridge: FiniteBridge,
        source_interpretation: UniverseInterpretation,
        target_interpretation: UniverseInterpretation,
    ) -> BridgePreservationReport:
        """
        Analyzes satisfaction preservation for every source statement.
        """

        results = tuple(
            self.analyze_statement(
                bridge=bridge,
                source_interpretation=source_interpretation,
                target_interpretation=target_interpretation,
                statement=statement,
            )
            for statement in sorted(bridge.source.statements, key=lambda item: item.name)
        )

        return BridgePreservationReport(
            bridge=bridge,
            source_interpretation=source_interpretation,
            target_interpretation=target_interpretation,
            results=results,
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

    report = SatisfactionPreservationAnalyzer().analyze_bridge(
        bridge=bridge,
        source_interpretation=interpretation,
        target_interpretation=interpretation,
    )

    print(report.describe())

    for result in report.results:
        print()
        print(result.describe())
