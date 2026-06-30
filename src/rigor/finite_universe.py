"""
Finite logical universe model for the Project ℵω rigor track.

This module gives a small, precise mathematical model for the Bridge
Distortion Theorem.

The goal is not to model all of logic. The goal is to define a finite
structure clear enough that statements, semantic features, bridges, and
distortion can later be stated as actual mathematical objects.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Iterable, Set


class SemanticFeature(str, Enum):
    """
    Semantic features that a finite logical universe may support.
    """

    CLASSICAL_TRUTH = "classical_truth"
    CONSTRUCTIVE_WITNESS = "constructive_witness"
    CONTRADICTION_TOLERANCE = "contradiction_tolerance"
    MODAL_NECESSITY = "modal_necessity"
    MODAL_POSSIBILITY = "modal_possibility"
    MANY_VALUED_TRUTH = "many_valued_truth"
    FUZZY_DEGREE = "fuzzy_degree"
    RESOURCE_SENSITIVITY = "resource_sensitivity"


@dataclass(frozen=True)
class FiniteStatement:
    """
    A finite statement represented by a name and required semantic features.

    A statement is semantically admissible in a universe only if the universe
    supports every feature required by the statement.
    """

    name: str
    required_features: FrozenSet[SemanticFeature] = field(default_factory=frozenset)
    informal_reading: str = ""

    @staticmethod
    def from_features(
        name: str,
        features: Iterable[SemanticFeature],
        informal_reading: str = "",
    ) -> "FiniteStatement":
        """
        Builds a finite statement from an iterable of semantic features.
        """

        return FiniteStatement(
            name=name,
            required_features=frozenset(features),
            informal_reading=informal_reading,
        )

    def requires(self, feature: SemanticFeature) -> bool:
        """
        Checks whether the statement requires a semantic feature.
        """

        return feature in self.required_features

    def feature_count(self) -> int:
        """
        Counts required semantic features.
        """

        return len(self.required_features)

    def describe(self) -> str:
        """
        Returns a readable statement description.
        """

        features = ", ".join(sorted(feature.value for feature in self.required_features))

        return (
            f"FiniteStatement: {self.name}\n"
            f"Required features: {features or 'none'}\n"
            f"Informal reading: {self.informal_reading or 'not provided'}"
        )


@dataclass(frozen=True)
class FiniteLogicalUniverse:
    """
    A finite logical universe.

    Mathematically, this is a finite object containing:

    - a name
    - a finite set of supported semantic features
    - a finite set of available statements

    A statement is admissible in the universe if all of its required features
    are supported by the universe.
    """

    name: str
    supported_features: FrozenSet[SemanticFeature]
    statements: FrozenSet[FiniteStatement] = field(default_factory=frozenset)
    description: str = ""

    @staticmethod
    def build(
        name: str,
        supported_features: Iterable[SemanticFeature],
        statements: Iterable[FiniteStatement] = (),
        description: str = "",
    ) -> "FiniteLogicalUniverse":
        """
        Builds a finite logical universe from iterable inputs.
        """

        return FiniteLogicalUniverse(
            name=name,
            supported_features=frozenset(supported_features),
            statements=frozenset(statements),
            description=description,
        )

    def supports(self, feature: SemanticFeature) -> bool:
        """
        Checks whether the universe supports a semantic feature.
        """

        return feature in self.supported_features

    def feature_count(self) -> int:
        """
        Counts supported semantic features.
        """

        return len(self.supported_features)

    def statement_count(self) -> int:
        """
        Counts statements.
        """

        return len(self.statements)

    def supports_all_required_features(self, statement: FiniteStatement) -> bool:
        """
        Checks whether the universe supports every feature required by a statement.
        """

        return statement.required_features.issubset(self.supported_features)

    def missing_features_for(self, statement: FiniteStatement) -> FrozenSet[SemanticFeature]:
        """
        Returns features required by the statement but missing from the universe.
        """

        return frozenset(statement.required_features.difference(self.supported_features))

    def admissible_statements(self) -> FrozenSet[FiniteStatement]:
        """
        Returns statements admissible in the universe.
        """

        return frozenset(
            statement
            for statement in self.statements
            if self.supports_all_required_features(statement)
        )

    def inadmissible_statements(self) -> FrozenSet[FiniteStatement]:
        """
        Returns statements not admissible in the universe.
        """

        return frozenset(
            statement
            for statement in self.statements
            if not self.supports_all_required_features(statement)
        )

    def is_at_least_as_expressive_as(self, other: "FiniteLogicalUniverse") -> bool:
        """
        Checks feature-set expressivity.

        U is at least as expressive as V when every feature supported by V is
        also supported by U.
        """

        return other.supported_features.issubset(self.supported_features)

    def features_absent_from(self, other: "FiniteLogicalUniverse") -> FrozenSet[SemanticFeature]:
        """
        Returns features supported by this universe but not by another universe.
        """

        return frozenset(self.supported_features.difference(other.supported_features))

    def describe(self) -> str:
        """
        Returns a readable universe description.
        """

        features = ", ".join(sorted(feature.value for feature in self.supported_features))

        return (
            f"FiniteLogicalUniverse: {self.name}\n"
            f"Supported features: {features or 'none'}\n"
            f"Statement count: {self.statement_count()}\n"
            f"Admissible statement count: {len(self.admissible_statements())}\n"
            f"Description: {self.description or 'not provided'}"
        )


def classical_finite_universe() -> FiniteLogicalUniverse:
    """
    Minimal classical universe.
    """

    statements = [
        FiniteStatement.from_features(
            name="excluded_middle_statement",
            features=[SemanticFeature.CLASSICAL_TRUTH],
            informal_reading="A statement governed by classical true/false semantics.",
        )
    ]

    return FiniteLogicalUniverse.build(
        name="Finite Classical Universe",
        supported_features=[SemanticFeature.CLASSICAL_TRUTH],
        statements=statements,
        description="A finite universe with only classical truth support.",
    )


def paraconsistent_finite_universe() -> FiniteLogicalUniverse:
    """
    Minimal paraconsistent universe.
    """

    statements = [
        FiniteStatement.from_features(
            name="controlled_contradiction_statement",
            features=[
                SemanticFeature.CLASSICAL_TRUTH,
                SemanticFeature.CONTRADICTION_TOLERANCE,
            ],
            informal_reading="A statement that may tolerate both truth and falsity.",
        )
    ]

    return FiniteLogicalUniverse.build(
        name="Finite Paraconsistent Universe",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.CONTRADICTION_TOLERANCE,
        ],
        statements=statements,
        description="A finite universe that supports controlled contradiction.",
    )


def modal_finite_universe() -> FiniteLogicalUniverse:
    """
    Minimal modal universe.
    """

    statements = [
        FiniteStatement.from_features(
            name="necessary_truth_statement",
            features=[
                SemanticFeature.CLASSICAL_TRUTH,
                SemanticFeature.MODAL_NECESSITY,
            ],
            informal_reading="A statement whose interpretation involves necessity.",
        ),
        FiniteStatement.from_features(
            name="possible_truth_statement",
            features=[
                SemanticFeature.CLASSICAL_TRUTH,
                SemanticFeature.MODAL_POSSIBILITY,
            ],
            informal_reading="A statement whose interpretation involves possibility.",
        ),
    ]

    return FiniteLogicalUniverse.build(
        name="Finite Modal Universe",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
            SemanticFeature.MODAL_POSSIBILITY,
        ],
        statements=statements,
        description="A finite universe with modal semantic features.",
    )


def intuitionistic_finite_universe() -> FiniteLogicalUniverse:
    """
    Minimal intuitionistic universe.
    """

    statements = [
        FiniteStatement.from_features(
            name="constructive_witness_statement",
            features=[
                SemanticFeature.CLASSICAL_TRUTH,
                SemanticFeature.CONSTRUCTIVE_WITNESS,
            ],
            informal_reading="A statement whose assertion depends on constructive evidence.",
        )
    ]

    return FiniteLogicalUniverse.build(
        name="Finite Intuitionistic Universe",
        supported_features=[
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.CONSTRUCTIVE_WITNESS,
        ],
        statements=statements,
        description="A finite universe requiring constructive witness information.",
    )


def standard_rigor_universes() -> Set[FiniteLogicalUniverse]:
    """
    Returns the starter finite universes for the rigor track.
    """

    return {
        classical_finite_universe(),
        paraconsistent_finite_universe(),
        modal_finite_universe(),
        intuitionistic_finite_universe(),
    }


if __name__ == "__main__":
    for universe in sorted(standard_rigor_universes(), key=lambda item: item.name):
        print(universe.describe())
        print()
