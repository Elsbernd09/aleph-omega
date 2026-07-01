"""
Satisfaction relation for the Project ℵω rigor track.

This module defines a finite satisfaction relation.

A statement is satisfied by a universe interpretation when:

1. the universe supports all semantic features required by the statement;
2. the statement has a valid truth-value interpretation;
3. the interpreted truth value is designated.

This gives the rigor track a clearer semantic core.
"""

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Tuple

from src.rigor.finite_universe import FiniteStatement, SemanticFeature
from src.rigor.interpretation import (
    InterpretationStatus,
    StatementInterpretationResult,
    UniverseInterpretation,
)


class SatisfactionStatus(str, Enum):
    """
    Status of a statement under a universe interpretation.
    """

    SATISFIED = "satisfied"
    NOT_DESIGNATED = "not_designated"
    INVALID_INTERPRETATION = "invalid_interpretation"
    UNINTERPRETED = "uninterpreted"
    FEATURE_INADMISSIBLE = "feature_inadmissible"


@dataclass(frozen=True)
class SatisfactionResult:
    """
    Result of checking satisfaction for one statement.
    """

    statement: FiniteStatement
    interpretation_result: StatementInterpretationResult
    status: SatisfactionStatus
    missing_features: FrozenSet[SemanticFeature]
    explanation: str = ""

    def is_satisfied(self) -> bool:
        """
        Returns whether the statement is satisfied.
        """

        return self.status == SatisfactionStatus.SATISFIED

    def has_feature_failure(self) -> bool:
        """
        Returns whether satisfaction failed because of missing features.
        """

        return self.status == SatisfactionStatus.FEATURE_INADMISSIBLE

    def describe(self) -> str:
        """
        Returns a readable satisfaction result.
        """

        missing = ", ".join(sorted(feature.value for feature in self.missing_features))

        return (
            f"SatisfactionResult\n"
            f"Statement: {self.statement.name}\n"
            f"Status: {self.status.value}\n"
            f"Satisfied: {self.is_satisfied()}\n"
            f"Missing features: {missing or 'none'}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


@dataclass(frozen=True)
class SatisfactionReport:
    """
    Satisfaction report for a universe interpretation.
    """

    interpretation: UniverseInterpretation
    results: Tuple[SatisfactionResult, ...]

    def satisfied_results(self) -> Tuple[SatisfactionResult, ...]:
        """
        Returns satisfied results.
        """

        return tuple(result for result in self.results if result.is_satisfied())

    def failed_results(self) -> Tuple[SatisfactionResult, ...]:
        """
        Returns failed satisfaction results.
        """

        return tuple(result for result in self.results if not result.is_satisfied())

    def feature_failures(self) -> Tuple[SatisfactionResult, ...]:
        """
        Returns results that failed due to missing semantic features.
        """

        return tuple(result for result in self.results if result.has_feature_failure())

    def satisfied_count(self) -> int:
        """
        Counts satisfied statements.
        """

        return len(self.satisfied_results())

    def failed_count(self) -> int:
        """
        Counts failed statements.
        """

        return len(self.failed_results())

    def all_satisfied(self) -> bool:
        """
        Returns whether every statement is satisfied.
        """

        return bool(self.results) and all(result.is_satisfied() for result in self.results)

    def describe(self) -> str:
        """
        Returns a readable satisfaction report.
        """

        return (
            f"SatisfactionReport\n"
            f"Universe: {self.interpretation.universe.name}\n"
            f"Truth space: {self.interpretation.truth_space.name}\n"
            f"Satisfied count: {self.satisfied_count()}\n"
            f"Failed count: {self.failed_count()}\n"
            f"All satisfied: {self.all_satisfied()}"
        )


class SatisfactionChecker:
    """
    Checks satisfaction of statements under universe interpretations.
    """

    def check_statement(
        self,
        interpretation: UniverseInterpretation,
        statement: FiniteStatement,
    ) -> SatisfactionResult:
        """
        Checks whether one statement is satisfied.
        """

        missing_features = interpretation.universe.missing_features_for(statement)

        interpretation_result = interpretation.interpret_statement(statement)

        if missing_features:
            return SatisfactionResult(
                statement=statement,
                interpretation_result=interpretation_result,
                status=SatisfactionStatus.FEATURE_INADMISSIBLE,
                missing_features=missing_features,
                explanation=(
                    "The universe does not support every feature required by the statement."
                ),
            )

        if interpretation_result.status == InterpretationStatus.UNINTERPRETED:
            return SatisfactionResult(
                statement=statement,
                interpretation_result=interpretation_result,
                status=SatisfactionStatus.UNINTERPRETED,
                missing_features=frozenset(),
                explanation="The statement has no assigned truth value.",
            )

        if interpretation_result.status == InterpretationStatus.INVALID_TRUTH_VALUE:
            return SatisfactionResult(
                statement=statement,
                interpretation_result=interpretation_result,
                status=SatisfactionStatus.INVALID_INTERPRETATION,
                missing_features=frozenset(),
                explanation="The assigned truth value is invalid for the truth-value space.",
            )

        if not interpretation_result.is_designated():
            return SatisfactionResult(
                statement=statement,
                interpretation_result=interpretation_result,
                status=SatisfactionStatus.NOT_DESIGNATED,
                missing_features=frozenset(),
                explanation="The assigned truth value is valid but not designated.",
            )

        return SatisfactionResult(
            statement=statement,
            interpretation_result=interpretation_result,
            status=SatisfactionStatus.SATISFIED,
            missing_features=frozenset(),
            explanation="The statement is admissible, validly interpreted, and designated.",
        )

    def check_interpretation(
        self,
        interpretation: UniverseInterpretation,
    ) -> SatisfactionReport:
        """
        Checks satisfaction for every statement in a universe interpretation.
        """

        results = tuple(
            self.check_statement(interpretation, statement)
            for statement in sorted(
                interpretation.universe.statements,
                key=lambda item: item.name,
            )
        )

        return SatisfactionReport(
            interpretation=interpretation,
            results=results,
        )


if __name__ == "__main__":
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

    report = SatisfactionChecker().check_interpretation(interpretation)

    print(report.describe())

    for result in report.results:
        print()
        print(result.describe())
