"""
Truth-value system for Project ℵω toy logical universes.

This module defines truth values and truth-value spaces used by the toy
universe layer. These structures are simplified educational models, not full
implementations of mathematical logic or topos theory.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class TruthValue(str, Enum):
    """
    Named truth values used across toy logical universes.
    """

    TRUE = "true"
    FALSE = "false"
    BOTH = "both"
    NEITHER = "neither"
    UNKNOWN = "unknown"
    NECESSARY = "necessary"
    POSSIBLE = "possible"
    IMPOSSIBLE = "impossible"
    CONTINGENT = "contingent"


class LogicFamily(str, Enum):
    """
    Major families of toy logic used in Project ℵω.
    """

    CLASSICAL = "classical"
    INTUITIONISTIC = "intuitionistic"
    PARACONSISTENT = "paraconsistent"
    MANY_VALUED = "many_valued"
    MODAL = "modal"
    FUZZY = "fuzzy"
    GENERATED = "generated"


class ConsistencyPolicy(str, Enum):
    """
    How a universe responds to contradiction.
    """

    CLASSICAL_EXPLOSION = "classical_explosion"
    CONSTRUCTIVE_REJECTION = "constructive_rejection"
    PARACONSISTENT_CONTAINMENT = "paraconsistent_containment"
    UNKNOWN_ABSORPTION = "unknown_absorption"
    MODAL_RECLASSIFICATION = "modal_reclassification"
    FUZZY_DEGRADATION = "fuzzy_degradation"
    GENERATED_POLICY = "generated_policy"


@dataclass(frozen=True)
class TruthValueSpace:
    """
    A finite or symbolic truth-value space.

    For early toy universes, truth values are represented as named values.
    Later phases may add richer fuzzy truth degrees or algebraic truth tables.
    """

    name: str
    logic_family: LogicFamily
    values: List[TruthValue]
    consistency_policy: ConsistencyPolicy
    description: str
    metadata: Optional[Dict[str, str]] = None

    def contains(self, value: TruthValue) -> bool:
        """
        Checks whether a truth value belongs to this space.
        """

        return value in self.values

    def value_names(self) -> List[str]:
        """
        Returns truth-value names as strings.
        """

        return [value.value for value in self.values]

    def size(self) -> int:
        """
        Returns the number of named truth values.
        """

        return len(self.values)

    def supports_contradiction(self) -> bool:
        """
        Returns whether the truth space can explicitly represent contradiction.
        """

        return TruthValue.BOTH in self.values

    def supports_unknown(self) -> bool:
        """
        Returns whether the truth space can explicitly represent unknown truth.
        """

        return TruthValue.UNKNOWN in self.values or TruthValue.NEITHER in self.values

    def supports_modal_status(self) -> bool:
        """
        Returns whether the truth space includes modal truth statuses.
        """

        modal_values = {
            TruthValue.NECESSARY,
            TruthValue.POSSIBLE,
            TruthValue.IMPOSSIBLE,
            TruthValue.CONTINGENT,
        }

        return any(value in self.values for value in modal_values)

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        return (
            f"TruthValueSpace: {self.name}\n"
            f"Logic family: {self.logic_family.value}\n"
            f"Values: {', '.join(self.value_names())}\n"
            f"Consistency policy: {self.consistency_policy.value}\n"
            f"Supports contradiction: {self.supports_contradiction()}\n"
            f"Supports unknown: {self.supports_unknown()}\n"
            f"Supports modal status: {self.supports_modal_status()}\n"
            f"Description: {self.description}"
        )


def classical_truth_space() -> TruthValueSpace:
    """
    Standard two-valued classical truth space.
    """

    return TruthValueSpace(
        name="Classical Two-Valued Truth Space",
        logic_family=LogicFamily.CLASSICAL,
        values=[TruthValue.TRUE, TruthValue.FALSE],
        consistency_policy=ConsistencyPolicy.CLASSICAL_EXPLOSION,
        description=(
            "A toy truth space with exactly true and false. Contradiction is "
            "treated as unstable under the classical-explosion policy."
        ),
    )


def intuitionistic_truth_space() -> TruthValueSpace:
    """
    Constructive truth space.

    This toy model still uses true and false as named values, but its policy
    emphasizes constructive rejection of unsupported claims.
    """

    return TruthValueSpace(
        name="Intuitionistic Constructive Truth Space",
        logic_family=LogicFamily.INTUITIONISTIC,
        values=[TruthValue.TRUE, TruthValue.FALSE, TruthValue.UNKNOWN],
        consistency_policy=ConsistencyPolicy.CONSTRUCTIVE_REJECTION,
        description=(
            "A toy constructive truth space where unsupported claims may remain "
            "unknown rather than being assigned classical truth."
        ),
    )


def paraconsistent_truth_space() -> TruthValueSpace:
    """
    Paraconsistent truth space allowing both true and false.
    """

    return TruthValueSpace(
        name="Paraconsistent Truth Space",
        logic_family=LogicFamily.PARACONSISTENT,
        values=[
            TruthValue.TRUE,
            TruthValue.FALSE,
            TruthValue.BOTH,
            TruthValue.NEITHER,
        ],
        consistency_policy=ConsistencyPolicy.PARACONSISTENT_CONTAINMENT,
        description=(
            "A toy truth space where contradictions can be represented locally "
            "without immediate collapse."
        ),
    )


def many_valued_truth_space() -> TruthValueSpace:
    """
    Many-valued truth space with true, false, both, and unknown.
    """

    return TruthValueSpace(
        name="Many-Valued Truth Space",
        logic_family=LogicFamily.MANY_VALUED,
        values=[
            TruthValue.TRUE,
            TruthValue.FALSE,
            TruthValue.BOTH,
            TruthValue.UNKNOWN,
        ],
        consistency_policy=ConsistencyPolicy.UNKNOWN_ABSORPTION,
        description=(
            "A toy truth space with more than two truth values, allowing both "
            "contradiction and unknown status."
        ),
    )


def modal_truth_space() -> TruthValueSpace:
    """
    Modal truth space with possibility and necessity statuses.
    """

    return TruthValueSpace(
        name="Modal Truth Space",
        logic_family=LogicFamily.MODAL,
        values=[
            TruthValue.TRUE,
            TruthValue.FALSE,
            TruthValue.NECESSARY,
            TruthValue.POSSIBLE,
            TruthValue.IMPOSSIBLE,
            TruthValue.CONTINGENT,
        ],
        consistency_policy=ConsistencyPolicy.MODAL_RECLASSIFICATION,
        description=(
            "A toy modal truth space that classifies statements using necessity, "
            "possibility, impossibility, and contingency."
        ),
    )


def fuzzy_symbolic_truth_space() -> TruthValueSpace:
    """
    Symbolic fuzzy truth space.

    Full continuous fuzzy truth values will be implemented later. This early
    version uses named endpoint and uncertainty states.
    """

    return TruthValueSpace(
        name="Symbolic Fuzzy Truth Space",
        logic_family=LogicFamily.FUZZY,
        values=[TruthValue.TRUE, TruthValue.FALSE, TruthValue.UNKNOWN],
        consistency_policy=ConsistencyPolicy.FUZZY_DEGRADATION,
        description=(
            "A symbolic placeholder for fuzzy logic. Later phases may represent "
            "truth degrees numerically between 0 and 1."
        ),
    )


def all_standard_truth_spaces() -> List[TruthValueSpace]:
    """
    Returns all hand-designed standard truth-value spaces.
    """

    return [
        classical_truth_space(),
        intuitionistic_truth_space(),
        paraconsistent_truth_space(),
        many_valued_truth_space(),
        modal_truth_space(),
        fuzzy_symbolic_truth_space(),
    ]


if __name__ == "__main__":
    for truth_space in all_standard_truth_spaces():
        print(truth_space.describe())
        print("-" * 80)
