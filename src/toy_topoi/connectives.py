"""
Logical connectives for Project ℵω toy logical universes.

This module implements simplified truth operations for toy logic systems:
negation, conjunction, disjunction, and implication.

Important:
These are educational toy models. They are not complete implementations of
classical logic, intuitionistic logic, paraconsistent logic, modal logic, or
fuzzy logic.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

from .truth_values import LogicFamily, TruthValue, TruthValueSpace


TruthPair = Tuple[TruthValue, TruthValue]


@dataclass(frozen=True)
class ConnectiveResult:
    """
    Result of applying a logical connective.

    The explanation field makes the toy logic behavior inspectable.
    """

    value: TruthValue
    explanation: str


class ToyConnectiveAlgebra:
    """
    Implements toy logical connectives for a given truth-value space.

    The algebra uses different behavior depending on the logic family.
    """

    def __init__(self, truth_space: TruthValueSpace):
        self.truth_space = truth_space
        self.logic_family = truth_space.logic_family

    def negate(self, value: TruthValue) -> ConnectiveResult:
        """
        Toy negation.
        """

        if not self.truth_space.contains(value):
            return ConnectiveResult(
                value=TruthValue.UNKNOWN,
                explanation=f"{value.value} is not in {self.truth_space.name}.",
            )

        if self.logic_family == LogicFamily.PARACONSISTENT:
            table: Dict[TruthValue, TruthValue] = {
                TruthValue.TRUE: TruthValue.FALSE,
                TruthValue.FALSE: TruthValue.TRUE,
                TruthValue.BOTH: TruthValue.BOTH,
                TruthValue.NEITHER: TruthValue.NEITHER,
            }
            return ConnectiveResult(
                value=table[value],
                explanation="Paraconsistent negation preserves both and neither.",
            )

        if self.logic_family == LogicFamily.MANY_VALUED:
            table = {
                TruthValue.TRUE: TruthValue.FALSE,
                TruthValue.FALSE: TruthValue.TRUE,
                TruthValue.BOTH: TruthValue.BOTH,
                TruthValue.UNKNOWN: TruthValue.UNKNOWN,
            }
            return ConnectiveResult(
                value=table[value],
                explanation="Many-valued negation preserves unknown and both.",
            )

        if self.logic_family == LogicFamily.MODAL:
            table = {
                TruthValue.TRUE: TruthValue.FALSE,
                TruthValue.FALSE: TruthValue.TRUE,
                TruthValue.NECESSARY: TruthValue.IMPOSSIBLE,
                TruthValue.IMPOSSIBLE: TruthValue.NECESSARY,
                TruthValue.POSSIBLE: TruthValue.CONTINGENT,
                TruthValue.CONTINGENT: TruthValue.POSSIBLE,
            }
            return ConnectiveResult(
                value=table[value],
                explanation="Modal negation swaps necessity/impossibility and possibility/contingency.",
            )

        if value == TruthValue.TRUE:
            return ConnectiveResult(
                value=TruthValue.FALSE,
                explanation="Standard negation maps true to false.",
            )

        if value == TruthValue.FALSE:
            return ConnectiveResult(
                value=TruthValue.TRUE,
                explanation="Standard negation maps false to true.",
            )

        return ConnectiveResult(
            value=TruthValue.UNKNOWN,
            explanation="Unsupported negation result becomes unknown.",
        )

    def conjunction(self, left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Toy conjunction: left AND right.
        """

        if not self._values_supported(left, right):
            return self._unsupported_pair_result(left, right)

        if self.logic_family == LogicFamily.PARACONSISTENT:
            return self._paraconsistent_and(left, right)

        if self.logic_family == LogicFamily.MANY_VALUED:
            return self._many_valued_and(left, right)

        if self.logic_family == LogicFamily.MODAL:
            return self._modal_and(left, right)

        if left == TruthValue.TRUE and right == TruthValue.TRUE:
            return ConnectiveResult(TruthValue.TRUE, "Both inputs are true.")

        if left == TruthValue.FALSE or right == TruthValue.FALSE:
            return ConnectiveResult(TruthValue.FALSE, "At least one input is false.")

        return ConnectiveResult(TruthValue.UNKNOWN, "Conjunction is unknown in this toy system.")

    def disjunction(self, left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Toy disjunction: left OR right.
        """

        if not self._values_supported(left, right):
            return self._unsupported_pair_result(left, right)

        if self.logic_family == LogicFamily.PARACONSISTENT:
            return self._paraconsistent_or(left, right)

        if self.logic_family == LogicFamily.MANY_VALUED:
            return self._many_valued_or(left, right)

        if self.logic_family == LogicFamily.MODAL:
            return self._modal_or(left, right)

        if left == TruthValue.TRUE or right == TruthValue.TRUE:
            return ConnectiveResult(TruthValue.TRUE, "At least one input is true.")

        if left == TruthValue.FALSE and right == TruthValue.FALSE:
            return ConnectiveResult(TruthValue.FALSE, "Both inputs are false.")

        return ConnectiveResult(TruthValue.UNKNOWN, "Disjunction is unknown in this toy system.")

    def implication(self, left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Toy implication: left IMPLIES right.
        """

        if not self._values_supported(left, right):
            return self._unsupported_pair_result(left, right)

        if self.logic_family == LogicFamily.INTUITIONISTIC:
            if left == TruthValue.TRUE and right == TruthValue.UNKNOWN:
                return ConnectiveResult(
                    TruthValue.UNKNOWN,
                    "Constructive implication needs evidence for the consequent.",
                )

        if self.logic_family in {LogicFamily.PARACONSISTENT, LogicFamily.MANY_VALUED}:
            if left == TruthValue.BOTH:
                return ConnectiveResult(
                    TruthValue.BOTH,
                    "Implication from a contradictory antecedent remains contradictory in this toy model.",
                )

            if right == TruthValue.BOTH:
                return ConnectiveResult(
                    TruthValue.BOTH,
                    "Contradictory consequent produces a contradictory implication status.",
                )

            if left == TruthValue.UNKNOWN or right == TruthValue.UNKNOWN:
                return ConnectiveResult(
                    TruthValue.UNKNOWN,
                    "Unknown truth value makes implication unknown.",
                )

        if left == TruthValue.TRUE and right == TruthValue.FALSE:
            return ConnectiveResult(TruthValue.FALSE, "True implies false is false.")

        if left == TruthValue.FALSE:
            return ConnectiveResult(TruthValue.TRUE, "False antecedent gives true implication in this toy model.")

        if left == TruthValue.TRUE and right == TruthValue.TRUE:
            return ConnectiveResult(TruthValue.TRUE, "True implies true is true.")

        return ConnectiveResult(TruthValue.UNKNOWN, "Implication result is unknown in this toy system.")

    def truth_table(self, operation: str) -> Dict[TruthPair, ConnectiveResult]:
        """
        Builds a truth table for one operation.

        Supported operations:
        - and
        - or
        - implies
        """

        table: Dict[TruthPair, ConnectiveResult] = {}

        for left in self.truth_space.values:
            for right in self.truth_space.values:
                if operation == "and":
                    table[(left, right)] = self.conjunction(left, right)
                elif operation == "or":
                    table[(left, right)] = self.disjunction(left, right)
                elif operation == "implies":
                    table[(left, right)] = self.implication(left, right)
                else:
                    raise ValueError(f"Unknown operation: {operation}")

        return table

    def _values_supported(self, left: TruthValue, right: TruthValue) -> bool:
        """
        Checks whether both values belong to the current truth space.
        """

        return self.truth_space.contains(left) and self.truth_space.contains(right)

    @staticmethod
    def _unsupported_pair_result(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Returns an unknown result for unsupported truth-value pairs.
        """

        return ConnectiveResult(
            TruthValue.UNKNOWN,
            f"Unsupported pair: {left.value}, {right.value}.",
        )

    @staticmethod
    def _paraconsistent_and(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified paraconsistent conjunction.
        """

        if TruthValue.FALSE in {left, right} and TruthValue.TRUE not in {left, right}:
            return ConnectiveResult(TruthValue.FALSE, "False dominates without true support.")

        if TruthValue.BOTH in {left, right}:
            return ConnectiveResult(TruthValue.BOTH, "Contradiction is preserved under conjunction.")

        if left == TruthValue.TRUE and right == TruthValue.TRUE:
            return ConnectiveResult(TruthValue.TRUE, "Both inputs are true.")

        if TruthValue.NEITHER in {left, right}:
            return ConnectiveResult(TruthValue.NEITHER, "Neither status is preserved.")

        return ConnectiveResult(TruthValue.FALSE, "Default paraconsistent conjunction result.")

    @staticmethod
    def _paraconsistent_or(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified paraconsistent disjunction.
        """

        if TruthValue.TRUE in {left, right} and TruthValue.FALSE not in {left, right}:
            return ConnectiveResult(TruthValue.TRUE, "True dominates without false conflict.")

        if TruthValue.BOTH in {left, right}:
            return ConnectiveResult(TruthValue.BOTH, "Contradiction is preserved under disjunction.")

        if left == TruthValue.FALSE and right == TruthValue.FALSE:
            return ConnectiveResult(TruthValue.FALSE, "Both inputs are false.")

        if TruthValue.NEITHER in {left, right}:
            return ConnectiveResult(TruthValue.NEITHER, "Neither status is preserved.")

        return ConnectiveResult(TruthValue.TRUE, "Default paraconsistent disjunction result.")

    @staticmethod
    def _many_valued_and(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified many-valued conjunction.
        """

        if TruthValue.FALSE in {left, right}:
            return ConnectiveResult(TruthValue.FALSE, "False dominates conjunction.")

        if TruthValue.UNKNOWN in {left, right}:
            return ConnectiveResult(TruthValue.UNKNOWN, "Unknown propagates through conjunction.")

        if TruthValue.BOTH in {left, right}:
            return ConnectiveResult(TruthValue.BOTH, "Both is preserved under conjunction.")

        return ConnectiveResult(TruthValue.TRUE, "Both inputs are true.")

    @staticmethod
    def _many_valued_or(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified many-valued disjunction.
        """

        if TruthValue.TRUE in {left, right}:
            return ConnectiveResult(TruthValue.TRUE, "True dominates disjunction.")

        if TruthValue.BOTH in {left, right}:
            return ConnectiveResult(TruthValue.BOTH, "Both is preserved under disjunction.")

        if TruthValue.UNKNOWN in {left, right}:
            return ConnectiveResult(TruthValue.UNKNOWN, "Unknown propagates through disjunction.")

        return ConnectiveResult(TruthValue.FALSE, "Both inputs are false.")

    @staticmethod
    def _modal_and(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified modal conjunction.
        """

        if TruthValue.IMPOSSIBLE in {left, right} or TruthValue.FALSE in {left, right}:
            return ConnectiveResult(TruthValue.FALSE, "Impossible or false blocks conjunction.")

        if left == TruthValue.NECESSARY and right == TruthValue.NECESSARY:
            return ConnectiveResult(TruthValue.NECESSARY, "Both inputs are necessary.")

        if TruthValue.POSSIBLE in {left, right}:
            return ConnectiveResult(TruthValue.POSSIBLE, "Conjunction is possible but not necessary.")

        if TruthValue.CONTINGENT in {left, right}:
            return ConnectiveResult(TruthValue.CONTINGENT, "Conjunction remains contingent.")

        return ConnectiveResult(TruthValue.TRUE, "Modal conjunction defaults to true.")

    @staticmethod
    def _modal_or(left: TruthValue, right: TruthValue) -> ConnectiveResult:
        """
        Simplified modal disjunction.
        """

        if TruthValue.NECESSARY in {left, right} or TruthValue.TRUE in {left, right}:
            return ConnectiveResult(TruthValue.TRUE, "Necessary or true makes disjunction true.")

        if left == TruthValue.IMPOSSIBLE and right == TruthValue.IMPOSSIBLE:
            return ConnectiveResult(TruthValue.IMPOSSIBLE, "Both inputs are impossible.")

        if TruthValue.POSSIBLE in {left, right}:
            return ConnectiveResult(TruthValue.POSSIBLE, "Disjunction is possible.")

        if TruthValue.CONTINGENT in {left, right}:
            return ConnectiveResult(TruthValue.CONTINGENT, "Disjunction remains contingent.")

        return ConnectiveResult(TruthValue.FALSE, "Modal disjunction defaults to false.")
