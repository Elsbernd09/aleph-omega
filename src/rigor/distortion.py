"""
Rigorous distortion model for finite logical universes.

This module defines semantic distortion in a small finite setting.

The goal is to support a precise Bridge Distortion Theorem:

If a total bridge translates from a source universe with semantic features
absent from the target universe, and if at least one source statement requires
one of those absent features, then at least one translation is distorted.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Tuple

from src.rigor.bridge import FiniteBridge, BridgeTranslation
from src.rigor.finite_universe import FiniteStatement, SemanticFeature


class DistortionKind(str, Enum):
    """
    Kinds of distortion in a finite bridge translation.
    """

    UNDEFINED_TRANSLATION = "undefined_translation"
    FEATURE_LOSS = "feature_loss"
    PRESERVED = "preserved"


@dataclass(frozen=True)
class DistortionWitness:
    """
    A witness that a translation is distorted.

    In the theorem track, a witness is important because it gives a concrete
    statement and a concrete missing feature set.
    """

    source_statement: FiniteStatement
    missing_features: FrozenSet[SemanticFeature] = field(default_factory=frozenset)
    kind: DistortionKind = DistortionKind.PRESERVED
    explanation: str = ""

    def is_real_witness(self) -> bool:
        """
        Returns whether this object witnesses distortion.
        """

        return self.kind != DistortionKind.PRESERVED

    def missing_feature_count(self) -> int:
        """
        Counts missing features.
        """

        return len(self.missing_features)

    def describe(self) -> str:
        """
        Returns a readable witness description.
        """

        features = ", ".join(sorted(feature.value for feature in self.missing_features))

        return (
            f"DistortionWitness\n"
            f"Statement: {self.source_statement.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Missing features: {features or 'none'}\n"
            f"Explanation: {self.explanation or 'not provided'}"
        )


@dataclass(frozen=True)
class BridgeDistortionReport:
    """
    Distortion report for a finite bridge.
    """

    bridge: FiniteBridge
    witnesses: Tuple[DistortionWitness, ...]
    translations: Tuple[BridgeTranslation, ...]

    def witness_count(self) -> int:
        """
        Counts real distortion witnesses.
        """

        return sum(1 for witness in self.witnesses if witness.is_real_witness())

    def has_distortion(self) -> bool:
        """
        Returns whether the bridge has at least one distortion witness.
        """

        return self.witness_count() > 0

    def preserved_count(self) -> int:
        """
        Counts preserved translations.
        """

        return sum(1 for witness in self.witnesses if not witness.is_real_witness())

    def feature_loss_witnesses(self) -> Tuple[DistortionWitness, ...]:
        """
        Returns witnesses caused by feature loss.
        """

        return tuple(
            witness
            for witness in self.witnesses
            if witness.kind == DistortionKind.FEATURE_LOSS
        )

    def undefined_witnesses(self) -> Tuple[DistortionWitness, ...]:
        """
        Returns witnesses caused by undefined translations.
        """

        return tuple(
            witness
            for witness in self.witnesses
            if witness.kind == DistortionKind.UNDEFINED_TRANSLATION
        )

    def theorem_hypothesis_holds(self) -> bool:
        """
        Checks the main Bridge Distortion Theorem hypothesis.

        Hypothesis:
        - the bridge is total;
        - source has at least one feature absent from target;
        - at least one source statement requires an absent feature.
        """

        return (
            self.bridge.is_total()
            and self.bridge.has_feature_mismatch()
            and bool(self.bridge.statements_using_absent_features())
        )

    def theorem_conclusion_holds(self) -> bool:
        """
        Checks the expected theorem conclusion: at least one distortion exists.
        """

        return self.has_distortion()

    def theorem_verified_for_bridge(self) -> bool:
        """
        Checks implication form:

        If the theorem hypothesis holds, then the conclusion holds.

        If the hypothesis does not hold, this returns True because the implication
        is vacuously true for this bridge.
        """

        if not self.theorem_hypothesis_holds():
            return True

        return self.theorem_conclusion_holds()

    def describe(self) -> str:
        """
        Returns a readable report description.
        """

        return (
            f"BridgeDistortionReport\n"
            f"Bridge: {self.bridge.name}\n"
            f"Hypothesis holds: {self.theorem_hypothesis_holds()}\n"
            f"Conclusion holds: {self.theorem_conclusion_holds()}\n"
            f"Theorem verified for bridge: {self.theorem_verified_for_bridge()}\n"
            f"Witness count: {self.witness_count()}\n"
            f"Preserved count: {self.preserved_count()}"
        )


class DistortionAnalyzer:
    """
    Analyzes a finite bridge for semantic distortion.
    """

    def analyze_translation(
        self,
        translation: BridgeTranslation,
    ) -> DistortionWitness:
        """
        Produces a distortion witness for one translation.
        """

        if not translation.is_defined():
            return DistortionWitness(
                source_statement=translation.source_statement,
                missing_features=translation.missing_features,
                kind=DistortionKind.UNDEFINED_TRANSLATION,
                explanation=(
                    "The bridge is undefined on this source statement, so semantic "
                    "preservation fails."
                ),
            )

        if translation.missing_features:
            return DistortionWitness(
                source_statement=translation.source_statement,
                missing_features=translation.missing_features,
                kind=DistortionKind.FEATURE_LOSS,
                explanation=(
                    "The target universe does not support every semantic feature "
                    "required by the source statement."
                ),
            )

        return DistortionWitness(
            source_statement=translation.source_statement,
            missing_features=frozenset(),
            kind=DistortionKind.PRESERVED,
            explanation="The target universe supports all required source features.",
        )

    def analyze_bridge(self, bridge: FiniteBridge) -> BridgeDistortionReport:
        """
        Produces a bridge distortion report.
        """

        translations = bridge.translations()
        witnesses = tuple(
            self.analyze_translation(translation)
            for translation in translations
        )

        return BridgeDistortionReport(
            bridge=bridge,
            witnesses=witnesses,
            translations=translations,
        )


if __name__ == "__main__":
    from src.rigor.bridge import collapse_bridge
    from src.rigor.finite_universe import classical_finite_universe, modal_finite_universe

    source = modal_finite_universe()
    target = classical_finite_universe()
    bridge = collapse_bridge(
        name="Modal to Classical Collapse Bridge",
        source=source,
        target=target,
    )

    analyzer = DistortionAnalyzer()
    report = analyzer.analyze_bridge(bridge)

    print(report.describe())

    for witness in report.witnesses:
        print()
        print(witness.describe())
