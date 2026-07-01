"""
Finite institution satisfaction theorem for Project Aleph-Omega.

This module states and checks the finite satisfaction condition for finite
institution-like morphisms.

The theorem is finite and model-bound.
"""

from dataclasses import dataclass
from enum import Enum

from src.rigor.institution_morphism import (
    FiniteInstitutionMorphism,
    InstitutionMorphismReport,
    MorphismConditionStatus,
)


class InstitutionTheoremStatus(str, Enum):
    """
    Status of the finite institution satisfaction theorem.
    """

    VERIFIED_FOR_INSTANCE = "verified_for_instance"
    FAILED_FOR_INSTANCE = "failed_for_instance"
    VACUOUS_FOR_INSTANCE = "vacuous_for_instance"


@dataclass(frozen=True)
class InstitutionSatisfactionTheoremCheck:
    """
    Result of checking the finite institution satisfaction theorem.
    """

    theorem_name: str
    morphism: FiniteInstitutionMorphism
    report: InstitutionMorphismReport
    status: InstitutionTheoremStatus

    def hypothesis_holds(self) -> bool:
        """
        Hypothesis: every witness satisfies the finite satisfaction condition.
        """

        return self.report.condition_holds()

    def has_source_satisfied_witness(self) -> bool:
        """
        Returns whether at least one witness has a satisfied source sentence.
        """

        return any(witness.source_satisfied for witness in self.report.witnesses)

    def conclusion_holds(self) -> bool:
        """
        Conclusion: the morphism preserves satisfaction.
        """

        return self.morphism.preserves_satisfaction()

    def is_nonvacuous_verification(self) -> bool:
        """
        Returns whether the theorem is verified with at least one satisfied source.
        """

        return (
            self.status == InstitutionTheoremStatus.VERIFIED_FOR_INSTANCE
            and self.has_source_satisfied_witness()
            and self.conclusion_holds()
        )

    def describe(self) -> str:
        """
        Returns a readable theorem check.
        """

        return (
            f"InstitutionSatisfactionTheoremCheck\n"
            f"Theorem: {self.theorem_name}\n"
            f"Morphism: {self.morphism.name}\n"
            f"Status: {self.status.value}\n"
            f"Hypothesis holds: {self.hypothesis_holds()}\n"
            f"Conclusion holds: {self.conclusion_holds()}\n"
            f"Has source-satisfied witness: {self.has_source_satisfied_witness()}\n"
            f"Nonvacuous verification: {self.is_nonvacuous_verification()}"
        )


class InstitutionSatisfactionTheorem:
    """
    Finite Institution Satisfaction Theorem.

    Statement:

    For a finite institution-like morphism, if every source-satisfied sentence
    translates to a target-satisfied sentence across all paired models, then the
    morphism preserves finite satisfaction.
    """

    name = "Finite Institution Satisfaction Theorem"

    def check(
        self,
        morphism: FiniteInstitutionMorphism,
    ) -> InstitutionSatisfactionTheoremCheck:
        """
        Checks the theorem for one finite institution morphism.
        """

        report = morphism.check_satisfaction_condition()

        if report.condition_holds():
            if any(witness.source_satisfied for witness in report.witnesses):
                status = InstitutionTheoremStatus.VERIFIED_FOR_INSTANCE
            else:
                status = InstitutionTheoremStatus.VACUOUS_FOR_INSTANCE
        else:
            status = InstitutionTheoremStatus.FAILED_FOR_INSTANCE

        return InstitutionSatisfactionTheoremCheck(
            theorem_name=self.name,
            morphism=morphism,
            report=report,
            status=status,
        )

    def theorem_statement(self) -> str:
        """
        Returns a readable theorem statement.
        """

        return (
            "Finite Institution Satisfaction Theorem:\n\n"
            "Let F be a finite institution-like morphism. If, for every paired "
            "source and target model and every source sentence phi, source "
            "satisfaction of phi implies target satisfaction of the translated "
            "sentence F(phi), then F preserves finite satisfaction."
        )


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
    from src.rigor.finite_institution import FiniteInstitutionBuilder
    from src.rigor.finite_universe import classical_finite_universe
    from src.rigor.institution_morphism import InstitutionMorphismBuilder
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
        name="Classical Institution",
        universe=universe,
        interpretations=(interpretation,),
    )

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(universe),
    )

    theorem = InstitutionSatisfactionTheorem()
    check = theorem.check(morphism)

    print(theorem.theorem_statement())
    print()
    print(check.describe())
