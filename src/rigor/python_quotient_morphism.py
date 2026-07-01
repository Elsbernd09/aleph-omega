"""
Python-side quotient morphisms for Project Aleph-Omega.

This module mirrors the Lean quotient morphism layer.

Lean side:
- QuotientMorphism
- quotientOf
- quotientIdentity
- quotientCompose

Python side:
- PythonQuotientMorphism
- PythonQuotientMorphismBuilder
- representative-based quotient composition

This is a computational analogue, not a proof assistant quotient.
"""

from dataclasses import dataclass
from typing import Optional

from src.rigor.composition import compose_bridges
from src.rigor.institution_morphism import FiniteInstitutionMorphism, InstitutionMorphismBuilder, ModelPairing
from src.rigor.python_morphism_equivalence import PythonMorphismEquivalenceChecker


@dataclass(frozen=True)
class PythonQuotientMorphism:
    """
    Python-side quotient morphism.

    This stores one representative morphism and an equivalence signature.

    It is not a true mathematical quotient type in Python.
    It is a computational representative of a quotient class.
    """

    representative: FiniteInstitutionMorphism
    equivalence_signature: str

    def source_name(self) -> str:
        """
        Returns source institution name.
        """

        return self.representative.source.name

    def target_name(self) -> str:
        """
        Returns target institution name.
        """

        return self.representative.target.name

    def equivalent_to(self, other: "PythonQuotientMorphism") -> bool:
        """
        Checks whether two quotient morphisms have the same equivalence signature.
        """

        return self.equivalence_signature == other.equivalence_signature

    def describe(self) -> str:
        """
        Returns a readable quotient morphism.
        """

        return (
            f"PythonQuotientMorphism\n"
            f"Representative: {self.representative.name}\n"
            f"Source: {self.source_name()}\n"
            f"Target: {self.target_name()}\n"
            f"Signature: {self.equivalence_signature}"
        )


class PythonQuotientMorphismBuilder:
    """
    Builds Python-side quotient morphism representatives.
    """

    def __init__(self) -> None:
        self.equivalence_checker = PythonMorphismEquivalenceChecker()

    def signature_for(
        self,
        morphism: FiniteInstitutionMorphism,
    ) -> str:
        """
        Builds a stable extensional signature for a morphism.
        """

        translation_signature = self.equivalence_checker.translation_signature(morphism)
        pairing_signature = self.equivalence_checker.model_pairing_signature(morphism)

        return (
            f"source={morphism.source.name}|"
            f"target={morphism.target.name}|"
            f"translation={translation_signature}|"
            f"pairing={pairing_signature}"
        )

    def quotient_of(
        self,
        morphism: FiniteInstitutionMorphism,
    ) -> PythonQuotientMorphism:
        """
        Converts a morphism into a Python quotient morphism representative.
        """

        return PythonQuotientMorphism(
            representative=morphism,
            equivalence_signature=self.signature_for(morphism),
        )

    def identity(
        self,
        institution,
        bridge,
    ) -> PythonQuotientMorphism:
        """
        Builds the quotient identity morphism.
        """

        morphism = InstitutionMorphismBuilder().identity_morphism(
            institution=institution,
            bridge=bridge,
        )

        return self.quotient_of(morphism)

    def compose(
        self,
        first: PythonQuotientMorphism,
        second: PythonQuotientMorphism,
    ) -> Optional[PythonQuotientMorphism]:
        """
        Composes quotient morphism representatives.

        The order is second after first.
        """

        first_morphism = first.representative
        second_morphism = second.representative

        if first_morphism.target != second_morphism.source:
            return None

        bridge_result = compose_bridges(first_morphism.bridge, second_morphism.bridge)

        if bridge_result.composite is None:
            return None

        pairings = []

        for first_pairing in first_morphism.model_pairings:
            for second_pairing in second_morphism.model_pairings:
                if first_pairing.target_model == second_pairing.source_model:
                    pairings.append(
                        ModelPairing(
                            source_model=first_pairing.source_model,
                            target_model=second_pairing.target_model,
                        )
                    )

        composite = FiniteInstitutionMorphism(
            name=f"{second_morphism.name} after {first_morphism.name}",
            source=first_morphism.source,
            target=second_morphism.target,
            bridge=bridge_result.composite,
            model_pairings=tuple(pairings),
        )

        if not composite.preserves_satisfaction():
            return None

        return self.quotient_of(composite)


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
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

    builder = PythonQuotientMorphismBuilder()

    identity = builder.identity(
        institution=institution,
        bridge=identity_bridge(universe),
    )

    print(identity.describe())
