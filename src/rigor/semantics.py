"""
Finite truth-value semantics for the Project ℵω rigor track.

This module strengthens the mathematical core by giving finite logical
universes explicit truth-value spaces and semantic operations.

The goal is still modest: define finite semantics clearly enough to support
stronger preservation and distortion theorems.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Tuple


class FiniteTruthValue(str, Enum):
    """
    Finite truth values used in the rigor-track semantics.
    """

    TRUE = "true"
    FALSE = "false"
    BOTH = "both"
    NEITHER = "neither"
    UNKNOWN = "unknown"
    NECESSARY_TRUE = "necessary_true"
    POSSIBLY_TRUE = "possibly_true"


class SemanticOperation(str, Enum):
    """
    Semantic operations available in a finite truth-value space.
    """

    NEGATION = "negation"
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    IMPLICATION = "implication"
    MODAL_NECESSITY = "modal_necessity"
    MODAL_POSSIBILITY = "modal_possibility"


@dataclass(frozen=True)
class FiniteTruthValueSpace:
    """
    A finite truth-value space.

    Mathematically, this is a finite set of truth values together with a finite
    set of supported semantic operations.
    """

    name: str
    values: FrozenSet[FiniteTruthValue]
    operations: FrozenSet[SemanticOperation] = field(default_factory=frozenset)
    designated_values: FrozenSet[FiniteTruthValue] = field(default_factory=frozenset)
    description: str = ""

    @staticmethod
    def build(
        name: str,
        values: Iterable[FiniteTruthValue],
        operations: Iterable[SemanticOperation] = (),
        designated_values: Iterable[FiniteTruthValue] = (),
        description: str = "",
    ) -> "FiniteTruthValueSpace":
        """
        Builds a finite truth-value space.
        """

        return FiniteTruthValueSpace(
            name=name,
            values=frozenset(values),
            operations=frozenset(operations),
            designated_values=frozenset(designated_values),
            description=description,
        )

    def has_value(self, value: FiniteTruthValue) -> bool:
        """
        Checks whether the truth-value space contains a truth value.
        """

        return value in self.values

    def supports_operation(self, operation: SemanticOperation) -> bool:
        """
        Checks whether the truth-value space supports an operation.
        """

        return operation in self.operations

    def is_designated(self, value: FiniteTruthValue) -> bool:
        """
        Checks whether a truth value is designated.
        """

        return value in self.designated_values

    def value_count(self) -> int:
        """
        Counts truth values.
        """

        return len(self.values)

    def operation_count(self) -> int:
        """
        Counts semantic operations.
        """

        return len(self.operations)

    def values_absent_from(
        self,
        other: "FiniteTruthValueSpace",
    ) -> FrozenSet[FiniteTruthValue]:
        """
        Returns truth values present in this space but absent from another.
        """

        return frozenset(self.values.difference(other.values))

    def operations_absent_from(
        self,
        other: "FiniteTruthValueSpace",
    ) -> FrozenSet[SemanticOperation]:
        """
        Returns operations present in this space but absent from another.
        """

        return frozenset(self.operations.difference(other.operations))

    def is_at_least_as_expressive_as(
        self,
        other: "FiniteTruthValueSpace",
    ) -> bool:
        """
        Checks whether this truth-value space contains all values and operations
        of another truth-value space.
        """

        return (
            other.values.issubset(self.values)
            and other.operations.issubset(self.operations)
        )

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        values = ", ".join(sorted(value.value for value in self.values))
        operations = ", ".join(sorted(operation.value for operation in self.operations))
        designated = ", ".join(sorted(value.value for value in self.designated_values))

        return (
            f"FiniteTruthValueSpace: {self.name}\n"
            f"Values: {values or 'none'}\n"
            f"Operations: {operations or 'none'}\n"
            f"Designated values: {designated or 'none'}\n"
            f"Description: {self.description or 'not provided'}"
        )


@dataclass(frozen=True)
class TruthValueInterpretation:
    """
    Interpretation of a statement as a truth value inside a finite truth-value space.
    """

    statement_name: str
    truth_value: FiniteTruthValue
    truth_space: FiniteTruthValueSpace
    explanation: str = ""

    def is_valid_in_space(self) -> bool:
        """
        Returns whether the assigned truth value belongs to the truth-value space.
        """

        return self.truth_space.has_value(self.truth_value)

    def is_designated(self) -> bool:
        """
        Returns whether the interpretation is designated.
        """

        return self.truth_space.is_designated(self.truth_value)

    def describe(self) -> str:
        """
        Returns a readable interpretation description.
        """

        return (
            f"TruthValueInterpretation\n"
            f"Statement: {self.statement_name}\n"
            f"Truth value: {self.truth_value.value}\n"
            f"Truth space: {self.truth_space.name}\n"
            f"Valid in space: {self.is_valid_in_space()}\n"
            f"Designated: {self.is_designated()}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


def classical_truth_space() -> FiniteTruthValueSpace:
    """
    Classical two-valued truth space.
    """

    return FiniteTruthValueSpace.build(
        name="Classical Truth Space",
        values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.FALSE,
        ],
        operations=[
            SemanticOperation.NEGATION,
            SemanticOperation.CONJUNCTION,
            SemanticOperation.DISJUNCTION,
            SemanticOperation.IMPLICATION,
        ],
        designated_values=[FiniteTruthValue.TRUE],
        description="Two-valued classical truth space.",
    )


def paraconsistent_truth_space() -> FiniteTruthValueSpace:
    """
    Paraconsistent truth space with both and neither.
    """

    return FiniteTruthValueSpace.build(
        name="Paraconsistent Truth Space",
        values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.FALSE,
            FiniteTruthValue.BOTH,
            FiniteTruthValue.NEITHER,
        ],
        operations=[
            SemanticOperation.NEGATION,
            SemanticOperation.CONJUNCTION,
            SemanticOperation.DISJUNCTION,
            SemanticOperation.IMPLICATION,
        ],
        designated_values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.BOTH,
        ],
        description="Truth space that can tolerate both truth and falsity.",
    )


def modal_truth_space() -> FiniteTruthValueSpace:
    """
    Modal truth space with necessity and possibility markers.
    """

    return FiniteTruthValueSpace.build(
        name="Modal Truth Space",
        values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.FALSE,
            FiniteTruthValue.NECESSARY_TRUE,
            FiniteTruthValue.POSSIBLY_TRUE,
        ],
        operations=[
            SemanticOperation.NEGATION,
            SemanticOperation.CONJUNCTION,
            SemanticOperation.DISJUNCTION,
            SemanticOperation.IMPLICATION,
            SemanticOperation.MODAL_NECESSITY,
            SemanticOperation.MODAL_POSSIBILITY,
        ],
        designated_values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.NECESSARY_TRUE,
        ],
        description="Truth space with modal necessity and possibility values.",
    )


def many_valued_truth_space() -> FiniteTruthValueSpace:
    """
    Simple many-valued truth space.
    """

    return FiniteTruthValueSpace.build(
        name="Many-Valued Truth Space",
        values=[
            FiniteTruthValue.TRUE,
            FiniteTruthValue.FALSE,
            FiniteTruthValue.UNKNOWN,
        ],
        operations=[
            SemanticOperation.NEGATION,
            SemanticOperation.CONJUNCTION,
            SemanticOperation.DISJUNCTION,
        ],
        designated_values=[FiniteTruthValue.TRUE],
        description="Three-valued truth space with unknown.",
    )


def standard_truth_spaces() -> Tuple[FiniteTruthValueSpace, ...]:
    """
    Returns standard rigor-track truth spaces.
    """

    return (
        classical_truth_space(),
        paraconsistent_truth_space(),
        modal_truth_space(),
        many_valued_truth_space(),
    )


def truth_space_index() -> Dict[str, FiniteTruthValueSpace]:
    """
    Returns truth spaces indexed by name.
    """

    return {space.name: space for space in standard_truth_spaces()}


if __name__ == "__main__":
    for space in standard_truth_spaces():
        print(space.describe())
        print()
