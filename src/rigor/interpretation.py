"""
Statement interpretation functions for the Project ℵω rigor track.

This module connects finite statements to finite truth-value semantics.

It gives the project a clearer semantic layer:
- statements can be assigned truth values;
- interpretations can be checked for validity;
- universes can be interpreted through truth-value spaces.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Optional, Tuple

from src.rigor.finite_universe import FiniteLogicalUniverse, FiniteStatement
from src.rigor.semantics import (
    FiniteTruthValue,
    FiniteTruthValueSpace,
    TruthValueInterpretation,
)


class InterpretationStatus(str, Enum):
    """
    Status of a statement interpretation.
    """

    VALID = "valid"
    INVALID_TRUTH_VALUE = "invalid_truth_value"
    UNINTERPRETED = "uninterpreted"


@dataclass(frozen=True)
class StatementInterpretationResult:
    """
    Result of interpreting one finite statement.
    """

    statement: FiniteStatement
    interpretation: Optional[TruthValueInterpretation]
    status: InterpretationStatus
    explanation: str = ""

    def is_valid(self) -> bool:
        """
        Returns whether the interpretation is valid.
        """

        return self.status == InterpretationStatus.VALID

    def is_designated(self) -> bool:
        """
        Returns whether the interpreted truth value is designated.
        """

        return (
            self.interpretation is not None
            and self.interpretation.is_valid_in_space()
            and self.interpretation.is_designated()
        )

    def describe(self) -> str:
        """
        Returns a readable result description.
        """

        truth_value = (
            self.interpretation.truth_value.value
            if self.interpretation is not None
            else "none"
        )

        return (
            f"StatementInterpretationResult\n"
            f"Statement: {self.statement.name}\n"
            f"Truth value: {truth_value}\n"
            f"Status: {self.status.value}\n"
            f"Designated: {self.is_designated()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


@dataclass(frozen=True)
class UniverseInterpretation:
    """
    Interpretation of finite statements inside a truth-value space.
    """

    universe: FiniteLogicalUniverse
    truth_space: FiniteTruthValueSpace
    assignment: Dict[FiniteStatement, FiniteTruthValue] = field(default_factory=dict)
    description: str = ""

    def interpret_statement(
        self,
        statement: FiniteStatement,
    ) -> StatementInterpretationResult:
        """
        Interprets one statement.
        """

        if statement not in self.assignment:
            return StatementInterpretationResult(
                statement=statement,
                interpretation=None,
                status=InterpretationStatus.UNINTERPRETED,
                explanation="No truth value was assigned to this statement.",
            )

        truth_value = self.assignment[statement]

        interpretation = TruthValueInterpretation(
            statement_name=statement.name,
            truth_value=truth_value,
            truth_space=self.truth_space,
            explanation=f"Assigned by interpretation of {self.universe.name}.",
        )

        if not interpretation.is_valid_in_space():
            return StatementInterpretationResult(
                statement=statement,
                interpretation=interpretation,
                status=InterpretationStatus.INVALID_TRUTH_VALUE,
                explanation=(
                    "The assigned truth value is not contained in the truth-value space."
                ),
            )

        return StatementInterpretationResult(
            statement=statement,
            interpretation=interpretation,
            status=InterpretationStatus.VALID,
            explanation="The assigned truth value is valid in the truth-value space.",
        )

    def results(self) -> Tuple[StatementInterpretationResult, ...]:
        """
        Interprets all statements in the universe.
        """

        return tuple(
            self.interpret_statement(statement)
            for statement in sorted(self.universe.statements, key=lambda item: item.name)
        )

    def valid_results(self) -> Tuple[StatementInterpretationResult, ...]:
        """
        Returns valid interpretation results.
        """

        return tuple(result for result in self.results() if result.is_valid())

    def invalid_results(self) -> Tuple[StatementInterpretationResult, ...]:
        """
        Returns invalid or uninterpreted results.
        """

        return tuple(result for result in self.results() if not result.is_valid())

    def designated_results(self) -> Tuple[StatementInterpretationResult, ...]:
        """
        Returns valid designated interpretation results.
        """

        return tuple(result for result in self.results() if result.is_designated())

    def is_total(self) -> bool:
        """
        Returns whether every statement in the universe is assigned a truth value.
        """

        return all(statement in self.assignment for statement in self.universe.statements)

    def is_valid_interpretation(self) -> bool:
        """
        Returns whether every interpreted statement is valid.
        """

        return self.is_total() and all(result.is_valid() for result in self.results())

    def validity_count(self) -> int:
        """
        Counts valid interpretations.
        """

        return len(self.valid_results())

    def designated_count(self) -> int:
        """
        Counts designated interpretations.
        """

        return len(self.designated_results())

    def describe(self) -> str:
        """
        Returns a readable universe interpretation description.
        """

        return (
            f"UniverseInterpretation\n"
            f"Universe: {self.universe.name}\n"
            f"Truth space: {self.truth_space.name}\n"
            f"Total: {self.is_total()}\n"
            f"Valid interpretation: {self.is_valid_interpretation()}\n"
            f"Valid count: {self.validity_count()}\n"
            f"Designated count: {self.designated_count()}\n"
            f"Description: {self.description or 'not provided'}"
        )


def constant_interpretation(
    universe: FiniteLogicalUniverse,
    truth_space: FiniteTruthValueSpace,
    value: FiniteTruthValue,
    description: str = "",
) -> UniverseInterpretation:
    """
    Assigns the same truth value to every statement in a universe.
    """

    assignment = {
        statement: value
        for statement in universe.statements
    }

    return UniverseInterpretation(
        universe=universe,
        truth_space=truth_space,
        assignment=assignment,
        description=description or f"Constant interpretation assigning {value.value}.",
    )


def explicit_interpretation(
    universe: FiniteLogicalUniverse,
    truth_space: FiniteTruthValueSpace,
    assignments: Dict[str, FiniteTruthValue],
    description: str = "",
) -> UniverseInterpretation:
    """
    Builds an interpretation from statement names to truth values.
    """

    assignment = {}

    for statement in universe.statements:
        if statement.name in assignments:
            assignment[statement] = assignments[statement.name]

    return UniverseInterpretation(
        universe=universe,
        truth_space=truth_space,
        assignment=assignment,
        description=description or "Explicit interpretation by statement name.",
    )


if __name__ == "__main__":
    from src.rigor.finite_universe import classical_finite_universe
    from src.rigor.semantics import classical_truth_space

    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    print(interpretation.describe())

    for result in interpretation.results():
        print()
        print(result.describe())
