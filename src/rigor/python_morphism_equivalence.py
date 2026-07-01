"""
Python-side morphism equivalence for Project Aleph-Omega.

This module mirrors the Lean concept MorphismEquivalent.

Two finite institution morphisms are extensionally equivalent when:

1. they have the same source institution,
2. they have the same target institution,
3. they translate every source sentence to the same target sentence,
4. they pair source models to target models in the same extensional way.

This does not prove the Lean theorem inside Python.
It implements the computational analogue of the Lean equivalence relation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.institution_morphism import FiniteInstitutionMorphism


class PythonMorphismEquivalenceStatus(str, Enum):
    """
    Status of Python-side morphism equivalence.
    """

    EQUIVALENT = "equivalent"
    DIFFERENT_SOURCE = "different_source"
    DIFFERENT_TARGET = "different_target"
    DIFFERENT_TRANSLATION = "different_translation"
    DIFFERENT_MODEL_PAIRING = "different_model_pairing"


@dataclass(frozen=True)
class PythonMorphismEquivalenceReport:
    """
    Report comparing two Python finite institution morphisms.
    """

    first_name: str
    second_name: str
    status: PythonMorphismEquivalenceStatus
    explanation: str

    def equivalent(self) -> bool:
        """
        Returns whether the two morphisms are equivalent.
        """

        return self.status == PythonMorphismEquivalenceStatus.EQUIVALENT

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"PythonMorphismEquivalenceReport\n"
            f"First: {self.first_name}\n"
            f"Second: {self.second_name}\n"
            f"Status: {self.status.value}\n"
            f"Equivalent: {self.equivalent()}\n"
            f"Explanation: {self.explanation}"
        )


class PythonMorphismEquivalenceChecker:
    """
    Checks extensional equivalence of Python finite institution morphisms.
    """

    def translation_signature(
        self,
        morphism: FiniteInstitutionMorphism,
    ) -> Tuple[Tuple[str, str], ...]:
        """
        Returns the sentence-translation signature of a morphism.

        Each entry is:

        source sentence name -> target sentence name or undefined.
        """

        entries = []

        source_sentences = tuple(
            sorted(morphism.source.universe.statements, key=lambda item: item.name)
        )

        for source_sentence in source_sentences:
            target_sentence = morphism.translate_sentence(source_sentence)

            if target_sentence is None:
                target_name = "undefined"
            else:
                target_name = target_sentence.name

            entries.append((source_sentence.name, target_name))

        return tuple(entries)

    def model_pairing_signature(
        self,
        morphism: FiniteInstitutionMorphism,
    ) -> Tuple[Tuple[str, str], ...]:
        """
        Returns the model-pairing signature of a morphism.
        """

        return tuple(
            sorted(
                (
                    pairing.source_model.name,
                    pairing.target_model.name,
                )
                for pairing in morphism.model_pairings
            )
        )

    def check(
        self,
        first: FiniteInstitutionMorphism,
        second: FiniteInstitutionMorphism,
    ) -> PythonMorphismEquivalenceReport:
        """
        Checks whether two morphisms are extensionally equivalent.
        """

        if first.source != second.source:
            return PythonMorphismEquivalenceReport(
                first_name=first.name,
                second_name=second.name,
                status=PythonMorphismEquivalenceStatus.DIFFERENT_SOURCE,
                explanation="The morphisms have different source institutions.",
            )

        if first.target != second.target:
            return PythonMorphismEquivalenceReport(
                first_name=first.name,
                second_name=second.name,
                status=PythonMorphismEquivalenceStatus.DIFFERENT_TARGET,
                explanation="The morphisms have different target institutions.",
            )

        first_translation = self.translation_signature(first)
        second_translation = self.translation_signature(second)

        if first_translation != second_translation:
            return PythonMorphismEquivalenceReport(
                first_name=first.name,
                second_name=second.name,
                status=PythonMorphismEquivalenceStatus.DIFFERENT_TRANSLATION,
                explanation="The morphisms translate at least one source sentence differently.",
            )

        first_pairing = self.model_pairing_signature(first)
        second_pairing = self.model_pairing_signature(second)

        if first_pairing != second_pairing:
            return PythonMorphismEquivalenceReport(
                first_name=first.name,
                second_name=second.name,
                status=PythonMorphismEquivalenceStatus.DIFFERENT_MODEL_PAIRING,
                explanation="The morphisms pair source and target models differently.",
            )

        return PythonMorphismEquivalenceReport(
            first_name=first.name,
            second_name=second.name,
            status=PythonMorphismEquivalenceStatus.EQUIVALENT,
            explanation="The morphisms have the same source, target, sentence translation, and model pairing signatures.",
        )

    def equivalent(
        self,
        first: FiniteInstitutionMorphism,
        second: FiniteInstitutionMorphism,
    ) -> bool:
        """
        Convenience method returning only the equivalence boolean.
        """

        return self.check(first, second).equivalent()


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
        name="Demo Institution",
        universe=universe,
        interpretations=(interpretation,),
    )

    first = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(universe),
    )

    second = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(universe),
    )

    report = PythonMorphismEquivalenceChecker().check(first, second)

    print(report.describe())
