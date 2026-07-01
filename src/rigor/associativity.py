"""
Associativity checks for finite universe categories.

For bridges:

f: A -> B
g: B -> C
h: C -> D

Associativity says:

h ∘ (g ∘ f) = (h ∘ g) ∘ f

In this project, compose_bridges(first, second) means second ∘ first.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.category import FiniteUniverseCategory
from src.rigor.composition import compose_bridges, same_bridge_mapping


class AssociativityStatus(str, Enum):
    """
    Status of an associativity check.
    """

    HOLDS = "holds"
    NOT_COMPOSABLE = "not_composable"
    FAILS = "fails"


@dataclass(frozen=True)
class AssociativityCheck:
    """
    Associativity check for one triple of bridges.
    """

    first: FiniteBridge
    second: FiniteBridge
    third: FiniteBridge
    status: AssociativityStatus
    left_associated: FiniteBridge = None
    right_associated: FiniteBridge = None
    explanation: str = ""

    def holds(self) -> bool:
        """
        Returns whether associativity holds.
        """

        return self.status == AssociativityStatus.HOLDS

    def is_composable_triple(self) -> bool:
        """
        Returns whether this triple was composable.
        """

        return self.status != AssociativityStatus.NOT_COMPOSABLE

    def describe(self) -> str:
        """
        Returns a readable associativity check.
        """

        left_name = self.left_associated.name if self.left_associated else "none"
        right_name = self.right_associated.name if self.right_associated else "none"

        return (
            f"AssociativityCheck\n"
            f"First: {self.first.name}\n"
            f"Second: {self.second.name}\n"
            f"Third: {self.third.name}\n"
            f"Status: {self.status.value}\n"
            f"Left-associated composite: {left_name}\n"
            f"Right-associated composite: {right_name}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


@dataclass(frozen=True)
class AssociativityReport:
    """
    Associativity report for a finite universe category.
    """

    category: FiniteUniverseCategory
    checks: Tuple[AssociativityCheck, ...]

    def composable_checks(self) -> Tuple[AssociativityCheck, ...]:
        """
        Returns checks for composable triples.
        """

        return tuple(check for check in self.checks if check.is_composable_triple())

    def failing_checks(self) -> Tuple[AssociativityCheck, ...]:
        """
        Returns failing associativity checks.
        """

        return tuple(
            check for check in self.composable_checks()
            if not check.holds()
        )

    def holds(self) -> bool:
        """
        Returns whether associativity holds for all composable triples.
        """

        return len(self.failing_checks()) == 0

    def check_count(self) -> int:
        """
        Counts all checked triples.
        """

        return len(self.checks)

    def composable_count(self) -> int:
        """
        Counts composable checked triples.
        """

        return len(self.composable_checks())

    def failure_count(self) -> int:
        """
        Counts associativity failures.
        """

        return len(self.failing_checks())

    def describe(self) -> str:
        """
        Returns a readable associativity report.
        """

        return (
            f"AssociativityReport\n"
            f"Category: {self.category.name}\n"
            f"Check count: {self.check_count()}\n"
            f"Composable count: {self.composable_count()}\n"
            f"Failure count: {self.failure_count()}\n"
            f"Associativity holds: {self.holds()}"
        )


class AssociativityAnalyzer:
    """
    Analyzer for associativity of bridge composition.
    """

    def check_triple(
        self,
        first: FiniteBridge,
        second: FiniteBridge,
        third: FiniteBridge,
    ) -> AssociativityCheck:
        """
        Checks associativity for one triple.

        first: A -> B
        second: B -> C
        third: C -> D
        """

        first_second = compose_bridges(first, second)

        if first_second.composite is None:
            return AssociativityCheck(
                first=first,
                second=second,
                third=third,
                status=AssociativityStatus.NOT_COMPOSABLE,
                explanation="The first two bridges are not composable.",
            )

        second_third = compose_bridges(second, third)

        if second_third.composite is None:
            return AssociativityCheck(
                first=first,
                second=second,
                third=third,
                status=AssociativityStatus.NOT_COMPOSABLE,
                explanation="The second and third bridges are not composable.",
            )

        left_result = compose_bridges(first_second.composite, third)
        right_result = compose_bridges(first, second_third.composite)

        if left_result.composite is None or right_result.composite is None:
            return AssociativityCheck(
                first=first,
                second=second,
                third=third,
                status=AssociativityStatus.NOT_COMPOSABLE,
                left_associated=left_result.composite,
                right_associated=right_result.composite,
                explanation="One associated composite could not be constructed.",
            )

        if same_bridge_mapping(left_result.composite, right_result.composite):
            return AssociativityCheck(
                first=first,
                second=second,
                third=third,
                status=AssociativityStatus.HOLDS,
                left_associated=left_result.composite,
                right_associated=right_result.composite,
                explanation="Both associated composites have the same source, target, and mapping.",
            )

        return AssociativityCheck(
            first=first,
            second=second,
            third=third,
            status=AssociativityStatus.FAILS,
            left_associated=left_result.composite,
            right_associated=right_result.composite,
            explanation="The associated composites differ.",
        )

    def check_category(
        self,
        category: FiniteUniverseCategory,
    ) -> AssociativityReport:
        """
        Checks associativity for every morphism triple in a category.
        """

        morphisms = sorted(category.morphisms, key=lambda item: item.name)
        checks = []

        for first in morphisms:
            for second in morphisms:
                for third in morphisms:
                    check = self.check_triple(first, second, third)
                    checks.append(check)

        return AssociativityReport(
            category=category,
            checks=tuple(checks),
        )


if __name__ == "__main__":
    from src.rigor.category import starter_finite_universe_category

    category = starter_finite_universe_category()
    report = AssociativityAnalyzer().check_category(category)

    print(report.describe())

    for check in report.composable_checks():
        print()
        print(check.describe())
