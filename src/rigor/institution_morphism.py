"""
Finite institution morphisms for Project Aleph-Omega.

This module defines finite institution-like morphisms using existing bridge
translations.

A finite institution morphism here consists of:
- a source finite institution,
- a target finite institution,
- a bridge translating source sentences to target sentences,
- a finite pairing between source models and target models.

The key mathematical question is whether satisfaction is preserved across the
translation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from src.rigor.bridge import FiniteBridge
from src.rigor.finite_institution import FiniteInstitution, FiniteModel
from src.rigor.finite_universe import FiniteStatement


class MorphismConditionStatus(str, Enum):
    """
    Status of a finite institution morphism satisfaction condition.
    """

    PRESERVED = "preserved"
    UNDEFINED_TRANSLATION = "undefined_translation"
    TARGET_NOT_SATISFIED = "target_not_satisfied"
    NO_MODEL_PAIRINGS = "no_model_pairings"


@dataclass(frozen=True)
class ModelPairing:
    """
    Pairing between one source model and one target model.
    """

    source_model: FiniteModel
    target_model: FiniteModel

    def describe(self) -> str:
        """
        Returns a readable model pairing.
        """

        return (
            f"ModelPairing\n"
            f"Source model: {self.source_model.name}\n"
            f"Target model: {self.target_model.name}"
        )


@dataclass(frozen=True)
class SatisfactionConditionWitness:
    """
    Witness for one sentence/model satisfaction-condition check.
    """

    source_model: FiniteModel
    target_model: FiniteModel
    source_sentence: FiniteStatement
    target_sentence: Optional[FiniteStatement]
    source_satisfied: bool
    target_satisfied: bool
    status: MorphismConditionStatus

    def condition_holds(self) -> bool:
        """
        Returns whether this witness satisfies the preservation condition.
        """

        return self.status == MorphismConditionStatus.PRESERVED

    def describe(self) -> str:
        """
        Returns a readable witness.
        """

        target_name = self.target_sentence.name if self.target_sentence is not None else "undefined"

        return (
            f"SatisfactionConditionWitness\n"
            f"Source model: {self.source_model.name}\n"
            f"Target model: {self.target_model.name}\n"
            f"Source sentence: {self.source_sentence.name}\n"
            f"Target sentence: {target_name}\n"
            f"Source satisfied: {self.source_satisfied}\n"
            f"Target satisfied: {self.target_satisfied}\n"
            f"Status: {self.status.value}"
        )


@dataclass(frozen=True)
class InstitutionMorphismReport:
    """
    Report for a finite institution morphism satisfaction-condition check.
    """

    witnesses: Tuple[SatisfactionConditionWitness, ...]

    def witness_count(self) -> int:
        """
        Counts witnesses.
        """

        return len(self.witnesses)

    def failure_witnesses(self) -> Tuple[SatisfactionConditionWitness, ...]:
        """
        Returns witnesses where preservation failed.
        """

        return tuple(witness for witness in self.witnesses if not witness.condition_holds())

    def preserved_witnesses(self) -> Tuple[SatisfactionConditionWitness, ...]:
        """
        Returns witnesses where preservation held.
        """

        return tuple(witness for witness in self.witnesses if witness.condition_holds())

    def condition_holds(self) -> bool:
        """
        Returns whether the satisfaction condition holds for all witnesses.
        """

        return len(self.failure_witnesses()) == 0

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"InstitutionMorphismReport\n"
            f"Witnesses: {self.witness_count()}\n"
            f"Preserved witnesses: {len(self.preserved_witnesses())}\n"
            f"Failure witnesses: {len(self.failure_witnesses())}\n"
            f"Condition holds: {self.condition_holds()}"
        )


@dataclass(frozen=True)
class FiniteInstitutionMorphism:
    """
    Finite institution-like morphism.

    This uses a bridge to translate source sentences into target sentences.
    """

    name: str
    source: FiniteInstitution
    target: FiniteInstitution
    bridge: FiniteBridge
    model_pairings: Tuple[ModelPairing, ...]

    def model_pairing_count(self) -> int:
        """
        Counts model pairings.
        """

        return len(self.model_pairings)

    def translate_sentence(
        self,
        sentence: FiniteStatement,
    ) -> Optional[FiniteStatement]:
        """
        Translates a source sentence using the bridge.
        """

        return self.bridge.mapping.get(sentence)

    def check_satisfaction_condition(self) -> InstitutionMorphismReport:
        """
        Checks finite satisfaction preservation.

        For every paired source/target model and every source sentence:

        if the source model satisfies the source sentence,
        then the target model must satisfy the translated target sentence.
        """

        if not self.model_pairings:
            return InstitutionMorphismReport(
                witnesses=(
                    SatisfactionConditionWitness(
                        source_model=self.source.models[0],
                        target_model=self.target.models[0],
                        source_sentence=sorted(self.source.universe.statements, key=lambda item: item.name)[0],
                        target_sentence=None,
                        source_satisfied=False,
                        target_satisfied=False,
                        status=MorphismConditionStatus.NO_MODEL_PAIRINGS,
                    ),
                )
            )

        witnesses = []

        source_sentences = tuple(sorted(self.source.universe.statements, key=lambda item: item.name))

        for pairing in self.model_pairings:
            for source_sentence in source_sentences:
                source_satisfied = pairing.source_model.satisfies(source_sentence)

                target_sentence = self.translate_sentence(source_sentence)

                if not source_satisfied:
                    witnesses.append(
                        SatisfactionConditionWitness(
                            source_model=pairing.source_model,
                            target_model=pairing.target_model,
                            source_sentence=source_sentence,
                            target_sentence=target_sentence,
                            source_satisfied=False,
                            target_satisfied=False,
                            status=MorphismConditionStatus.PRESERVED,
                        )
                    )
                    continue

                if target_sentence is None:
                    witnesses.append(
                        SatisfactionConditionWitness(
                            source_model=pairing.source_model,
                            target_model=pairing.target_model,
                            source_sentence=source_sentence,
                            target_sentence=None,
                            source_satisfied=True,
                            target_satisfied=False,
                            status=MorphismConditionStatus.UNDEFINED_TRANSLATION,
                        )
                    )
                    continue

                target_satisfied = pairing.target_model.satisfies(target_sentence)

                if target_satisfied:
                    status = MorphismConditionStatus.PRESERVED
                else:
                    status = MorphismConditionStatus.TARGET_NOT_SATISFIED

                witnesses.append(
                    SatisfactionConditionWitness(
                        source_model=pairing.source_model,
                        target_model=pairing.target_model,
                        source_sentence=source_sentence,
                        target_sentence=target_sentence,
                        source_satisfied=True,
                        target_satisfied=target_satisfied,
                        status=status,
                    )
                )

        return InstitutionMorphismReport(witnesses=tuple(witnesses))

    def preserves_satisfaction(self) -> bool:
        """
        Returns whether this morphism preserves finite satisfaction.
        """

        return self.check_satisfaction_condition().condition_holds()

    def describe(self) -> str:
        """
        Returns a readable morphism description.
        """

        return (
            f"FiniteInstitutionMorphism\n"
            f"Name: {self.name}\n"
            f"Source institution: {self.source.name}\n"
            f"Target institution: {self.target.name}\n"
            f"Bridge: {self.bridge.name}\n"
            f"Model pairings: {self.model_pairing_count()}\n"
            f"Preserves satisfaction: {self.preserves_satisfaction()}"
        )


class InstitutionMorphismBuilder:
    """
    Builds finite institution morphisms.
    """

    def identity_morphism(
        self,
        institution: FiniteInstitution,
        bridge: FiniteBridge,
    ) -> FiniteInstitutionMorphism:
        """
        Builds an identity-style finite institution morphism.
        """

        pairings = tuple(
            ModelPairing(source_model=model, target_model=model)
            for model in institution.models
        )

        return FiniteInstitutionMorphism(
            name=f"Identity Morphism on {institution.name}",
            source=institution,
            target=institution,
            bridge=bridge,
            model_pairings=pairings,
        )

    def paired_morphism(
        self,
        name: str,
        source: FiniteInstitution,
        target: FiniteInstitution,
        bridge: FiniteBridge,
    ) -> FiniteInstitutionMorphism:
        """
        Builds a finite institution morphism by pairing models by index.
        """

        pairings = tuple(
            ModelPairing(source_model=source_model, target_model=target_model)
            for source_model, target_model in zip(source.models, target.models)
        )

        return FiniteInstitutionMorphism(
            name=name,
            source=source,
            target=target,
            bridge=bridge,
            model_pairings=pairings,
        )


if __name__ == "__main__":
    from src.rigor.bridge import identity_bridge
    from src.rigor.finite_institution import FiniteInstitutionBuilder
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
        name="Classical Institution",
        universe=universe,
        interpretations=(true_interpretation, false_interpretation),
    )

    morphism = InstitutionMorphismBuilder().identity_morphism(
        institution=institution,
        bridge=identity_bridge(universe),
    )

    print(morphism.describe())
    print()
    print(morphism.check_satisfaction_condition().describe())
