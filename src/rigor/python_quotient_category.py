"""
Python-side quotient category layer for Project Aleph-Omega.

This module mirrors the Lean standalone quotient category structure.

Lean side:
- StandaloneQuotientCategory
- AlephOmegaQuotientCategory
- QuotientHom
- quotientId
- quotientComp

Python side:
- PythonQuotientCategory
- identity quotient morphisms
- quotient morphism composition
- computational identity/associativity checks

This is a computational analogue, not a proof-assistant category.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.bridge import identity_bridge
from src.rigor.finite_institution import FiniteInstitution
from src.rigor.python_quotient_morphism import (
    PythonQuotientMorphism,
    PythonQuotientMorphismBuilder,
)


class PythonQuotientCategoryLawStatus(str, Enum):
    """
    Status for Python-side quotient category law checks.
    """

    HOLDS = "holds"
    FAILS = "fails"
    NOT_COMPOSABLE = "not_composable"


@dataclass(frozen=True)
class PythonQuotientCategoryLawReport:
    """
    Report for a Python quotient category law check.
    """

    law_name: str
    status: PythonQuotientCategoryLawStatus
    explanation: str

    def holds(self) -> bool:
        """
        Returns whether the law holds.
        """

        return self.status == PythonQuotientCategoryLawStatus.HOLDS

    def describe(self) -> str:
        """
        Returns a readable law report.
        """

        return (
            f"PythonQuotientCategoryLawReport\n"
            f"Law: {self.law_name}\n"
            f"Status: {self.status.value}\n"
            f"Holds: {self.holds()}\n"
            f"Explanation: {self.explanation}"
        )


@dataclass(frozen=True)
class PythonQuotientCategory:
    """
    Python-side quotient category analogue.

    Objects are finite institution-like systems.

    Arrows are PythonQuotientMorphism representatives.
    """

    name: str
    objects: Tuple[FiniteInstitution, ...]

    def object_count(self) -> int:
        """
        Counts objects.
        """

        return len(self.objects)

    def identity(
        self,
        institution: FiniteInstitution,
    ) -> PythonQuotientMorphism:
        """
        Builds the identity quotient morphism for an institution.
        """

        return PythonQuotientMorphismBuilder().identity(
            institution=institution,
            bridge=identity_bridge(institution.universe),
        )

    def compose(
        self,
        first: PythonQuotientMorphism,
        second: PythonQuotientMorphism,
    ):
        """
        Composes quotient morphisms.

        The order is second after first.
        """

        return PythonQuotientMorphismBuilder().compose(first, second)

    def check_left_identity(
        self,
        morphism: PythonQuotientMorphism,
    ) -> PythonQuotientCategoryLawReport:
        """
        Checks left identity computationally.
        """

        left_identity = self.identity(morphism.representative.source)
        composite = self.compose(left_identity, morphism)

        if composite is None:
            return PythonQuotientCategoryLawReport(
                law_name="Left Identity",
                status=PythonQuotientCategoryLawStatus.NOT_COMPOSABLE,
                explanation="The left identity composite could not be formed.",
            )

        if composite.equivalent_to(morphism):
            return PythonQuotientCategoryLawReport(
                law_name="Left Identity",
                status=PythonQuotientCategoryLawStatus.HOLDS,
                explanation="The left identity composite has the same quotient signature.",
            )

        return PythonQuotientCategoryLawReport(
            law_name="Left Identity",
            status=PythonQuotientCategoryLawStatus.FAILS,
            explanation="The left identity composite has a different quotient signature.",
        )

    def check_right_identity(
        self,
        morphism: PythonQuotientMorphism,
    ) -> PythonQuotientCategoryLawReport:
        """
        Checks right identity computationally.
        """

        right_identity = self.identity(morphism.representative.target)
        composite = self.compose(morphism, right_identity)

        if composite is None:
            return PythonQuotientCategoryLawReport(
                law_name="Right Identity",
                status=PythonQuotientCategoryLawStatus.NOT_COMPOSABLE,
                explanation="The right identity composite could not be formed.",
            )

        if composite.equivalent_to(morphism):
            return PythonQuotientCategoryLawReport(
                law_name="Right Identity",
                status=PythonQuotientCategoryLawStatus.HOLDS,
                explanation="The right identity composite has the same quotient signature.",
            )

        return PythonQuotientCategoryLawReport(
            law_name="Right Identity",
            status=PythonQuotientCategoryLawStatus.FAILS,
            explanation="The right identity composite has a different quotient signature.",
        )

    def check_associativity(
        self,
        first: PythonQuotientMorphism,
        second: PythonQuotientMorphism,
        third: PythonQuotientMorphism,
    ) -> PythonQuotientCategoryLawReport:
        """
        Checks associativity computationally.

        Compares:

        third after (second after first)

        with:

        (third after second) after first
        """

        second_after_first = self.compose(first, second)

        if second_after_first is None:
            return PythonQuotientCategoryLawReport(
                law_name="Associativity",
                status=PythonQuotientCategoryLawStatus.NOT_COMPOSABLE,
                explanation="The composite second after first could not be formed.",
            )

        left = self.compose(second_after_first, third)

        third_after_second = self.compose(second, third)

        if third_after_second is None:
            return PythonQuotientCategoryLawReport(
                law_name="Associativity",
                status=PythonQuotientCategoryLawStatus.NOT_COMPOSABLE,
                explanation="The composite third after second could not be formed.",
            )

        right = self.compose(first, third_after_second)

        if left is None or right is None:
            return PythonQuotientCategoryLawReport(
                law_name="Associativity",
                status=PythonQuotientCategoryLawStatus.NOT_COMPOSABLE,
                explanation="One side of the associativity comparison could not be formed.",
            )

        if left.equivalent_to(right):
            return PythonQuotientCategoryLawReport(
                law_name="Associativity",
                status=PythonQuotientCategoryLawStatus.HOLDS,
                explanation="Both associativity parenthesizations have the same quotient signature.",
            )

        return PythonQuotientCategoryLawReport(
            law_name="Associativity",
            status=PythonQuotientCategoryLawStatus.FAILS,
            explanation="The associativity parenthesizations have different quotient signatures.",
        )

    def describe(self) -> str:
        """
        Returns a readable category description.
        """

        return (
            f"PythonQuotientCategory\n"
            f"Name: {self.name}\n"
            f"Objects: {self.object_count()}"
        )


if __name__ == "__main__":
    from src.rigor.finite_institution import FiniteInstitutionBuilder
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

    institution = FiniteInstitutionBuilder().from_universe_and_interpretations(
        name="Demo Institution",
        universe=universe,
        interpretations=(interpretation,),
    )

    category = PythonQuotientCategory(
        name="Demo Python Quotient Category",
        objects=(institution,),
    )

    identity = category.identity(institution)

    print(category.describe())
    print()
    print(category.check_left_identity(identity).describe())
    print(category.check_right_identity(identity).describe())
    print(category.check_associativity(identity, identity, identity).describe())
