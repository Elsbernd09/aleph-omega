"""
Finite institution-like systems for Project Aleph-Omega.

This module connects the Project Aleph-Omega finite rigor track to the language
of institution theory.

In institution theory, a logic is often abstracted through:
- signatures,
- sentences,
- models,
- a satisfaction relation.

This module defines a finite, model-bound version of that structure.

It is not a full implementation of general institution theory.
It is a finite institution-like system designed for computational theorem
experiments.
"""

from dataclasses import dataclass
from typing import FrozenSet, Tuple

from src.rigor.finite_universe import FiniteLogicalUniverse, FiniteStatement
from src.rigor.interpretation import UniverseInterpretation


@dataclass(frozen=True)
class FiniteSignature:
    """
    A finite signature.

    In this project, a finite signature is represented by a name and a finite
    collection of symbols.

    The symbols are intentionally simple strings because this layer is designed
    to connect the existing finite universe framework to institution-theoretic
    language without claiming full generality.
    """

    name: str
    symbols: FrozenSet[str]

    @staticmethod
    def build(name: str, symbols: Tuple[str, ...]) -> "FiniteSignature":
        """
        Builds a finite signature.
        """

        return FiniteSignature(name=name, symbols=frozenset(symbols))

    def symbol_count(self) -> int:
        """
        Counts symbols.
        """

        return len(self.symbols)

    def describe(self) -> str:
        """
        Returns a readable signature description.
        """

        return (
            f"FiniteSignature\n"
            f"Name: {self.name}\n"
            f"Symbols: {self.symbol_count()}"
        )


@dataclass(frozen=True)
class FiniteModel:
    """
    A finite model for a finite signature.

    In this project, a model is backed by a UniverseInterpretation.
    """

    name: str
    signature: FiniteSignature
    interpretation: UniverseInterpretation

    def satisfies(self, sentence: FiniteStatement) -> bool:
        """
        Returns whether this model satisfies a finite sentence.

        This method is defensive because earlier Project Aleph-Omega layers use
        different names for interpretation fields.
        """

        value = None

        # First: inspect every attribute on the interpretation.
        interpretation_fields = vars(self.interpretation)

        for field_value in interpretation_fields.values():
            if isinstance(field_value, dict):
                value = field_value.get(sentence)

                if value is None:
                    value = field_value.get(sentence.name)

                if value is None:
                    for key, candidate_value in field_value.items():
                        if getattr(key, "name", None) == sentence.name:
                            value = candidate_value
                            break

            if value is not None:
                break

        # Second: look for direct truth-value-like fields.
        if value is None:
            for field_name, field_value in interpretation_fields.items():
                lowered = field_name.lower()

                if any(token in lowered for token in ("truth", "value", "assignment")):
                    if hasattr(field_value, "name") or hasattr(field_value, "value"):
                        value = field_value
                        break

        # Third: fallback for constant interpretations described textually.
        if value is None:
            description = getattr(self.interpretation, "description", "").lower()

            if "assigning true" in description or "assigned true" in description:
                for candidate in getattr(self.interpretation.truth_space, "values", ()):
                    if getattr(candidate, "value", "") == "true" or getattr(candidate, "name", "") == "TRUE":
                        value = candidate
                        break

            if "assigning false" in description or "assigned false" in description:
                for candidate in getattr(self.interpretation.truth_space, "values", ()):
                    if getattr(candidate, "value", "") == "false" or getattr(candidate, "name", "") == "FALSE":
                        value = candidate
                        break

        if value is None:
            return False

        return self.interpretation.truth_space.is_designated(value)

    def describe(self) -> str:
        """
        Returns a readable model description.
        """

        return (
            f"FiniteModel\n"
            f"Name: {self.name}\n"
            f"Signature: {self.signature.name}\n"
            f"Universe: {self.interpretation.universe.name}"
        )


@dataclass(frozen=True)
class SatisfactionJudgement:
    """
    One finite satisfaction judgement.

    This records whether a model satisfies a sentence.
    """

    model: FiniteModel
    sentence: FiniteStatement
    satisfied: bool

    def describe(self) -> str:
        """
        Returns a readable judgement.
        """

        return (
            f"SatisfactionJudgement\n"
            f"Model: {self.model.name}\n"
            f"Sentence: {self.sentence.name}\n"
            f"Satisfied: {self.satisfied}"
        )


@dataclass(frozen=True)
class FiniteInstitution:
    """
    A finite institution-like system.

    This consists of:
    - one finite signature,
    - one finite logical universe of sentences,
    - a finite tuple of models,
    - an induced satisfaction relation.
    """

    name: str
    signature: FiniteSignature
    universe: FiniteLogicalUniverse
    models: Tuple[FiniteModel, ...]

    def sentence_count(self) -> int:
        """
        Counts finite sentences.
        """

        return self.universe.statement_count()

    def model_count(self) -> int:
        """
        Counts finite models.
        """

        return len(self.models)

    def satisfaction_judgements(self) -> Tuple[SatisfactionJudgement, ...]:
        """
        Returns all model-sentence satisfaction judgements.
        """

        judgements = []

        for model in self.models:
            for sentence in sorted(self.universe.statements, key=lambda item: item.name):
                judgements.append(
                    SatisfactionJudgement(
                        model=model,
                        sentence=sentence,
                        satisfied=model.satisfies(sentence),
                    )
                )

        return tuple(judgements)

    def satisfied_judgement_count(self) -> int:
        """
        Counts satisfied judgements.
        """

        return sum(1 for judgement in self.satisfaction_judgements() if judgement.satisfied)

    def describe(self) -> str:
        """
        Returns a readable institution description.
        """

        return (
            f"FiniteInstitution\n"
            f"Name: {self.name}\n"
            f"Signature: {self.signature.name}\n"
            f"Sentences: {self.sentence_count()}\n"
            f"Models: {self.model_count()}\n"
            f"Satisfied judgements: {self.satisfied_judgement_count()}"
        )


class FiniteInstitutionBuilder:
    """
    Builds finite institution-like systems from existing Project Aleph-Omega objects.
    """

    def from_universe_and_interpretations(
        self,
        name: str,
        universe: FiniteLogicalUniverse,
        interpretations: Tuple[UniverseInterpretation, ...],
    ) -> FiniteInstitution:
        """
        Builds a finite institution-like system from a universe and interpretations.
        """

        symbols = tuple(sorted(statement.name for statement in universe.statements))

        signature = FiniteSignature.build(
            name=f"{name} Signature",
            symbols=symbols,
        )

        models = tuple(
            FiniteModel(
                name=f"{name} Model {index}",
                signature=signature,
                interpretation=interpretation,
            )
            for index, interpretation in enumerate(interpretations, start=1)
        )

        return FiniteInstitution(
            name=name,
            signature=signature,
            universe=universe,
            models=models,
        )


if __name__ == "__main__":
    from src.rigor.finite_universe import classical_finite_universe
    from src.rigor.interpretation import constant_interpretation
    from src.rigor.semantics import FiniteTruthValue, classical_truth_space

    universe = classical_finite_universe()
    truth_space = classical_truth_space()

    true_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.TRUE,
    )

    false_interpretation = constant_interpretation(
        universe=universe,
        truth_space=truth_space,
        value=FiniteTruthValue.FALSE,
    )

    institution = FiniteInstitutionBuilder().from_universe_and_interpretations(
        name="Classical Finite Institution",
        universe=universe,
        interpretations=(true_interpretation, false_interpretation),
    )

    print(institution.describe())
    print()

    for judgement in institution.satisfaction_judgements():
        print(judgement.describe())
