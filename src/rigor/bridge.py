"""
Finite bridge model for the Project ℵω rigor track.

A bridge is a finite translation map between statements in two finite logical
universes.

This module is intentionally small and precise. It prepares the project for
a formal Bridge Distortion Theorem.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Optional, Tuple

from src.rigor.finite_universe import (
    FiniteLogicalUniverse,
    FiniteStatement,
    SemanticFeature,
)


class BridgeTotality(str, Enum):
    """
    Whether a bridge is total or partial on the source universe's statements.
    """

    TOTAL = "total"
    PARTIAL = "partial"


class PreservationStatus(str, Enum):
    """
    Whether a translated statement preserves required semantic features.
    """

    PRESERVED = "preserved"
    DISTORTED = "distorted"


@dataclass(frozen=True)
class BridgeTranslation:
    """
    Translation result for one finite statement.
    """

    source_statement: FiniteStatement
    target_statement: Optional[FiniteStatement]
    missing_features: FrozenSet[SemanticFeature] = field(default_factory=frozenset)

    def is_defined(self) -> bool:
        """
        Returns whether the bridge defines a target statement.
        """

        return self.target_statement is not None

    def is_distorted(self) -> bool:
        """
        A translation is distorted if it is undefined or if required source
        features are missing in the target universe.
        """

        return (not self.is_defined()) or bool(self.missing_features)

    def preservation_status(self) -> PreservationStatus:
        """
        Returns preservation status.
        """

        if self.is_distorted():
            return PreservationStatus.DISTORTED

        return PreservationStatus.PRESERVED

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        target = self.target_statement.name if self.target_statement else "undefined"
        missing = ", ".join(sorted(feature.value for feature in self.missing_features))

        return (
            f"BridgeTranslation\n"
            f"Source statement: {self.source_statement.name}\n"
            f"Target statement: {target}\n"
            f"Missing features: {missing or 'none'}\n"
            f"Status: {self.preservation_status().value}"
        )


@dataclass(frozen=True)
class FiniteBridge:
    """
    A finite bridge between two finite logical universes.

    The bridge map sends source statements to target statements. If a source
    statement is absent from the map, then the bridge is undefined on that
    statement.

    A translation preserves semantic adequacy only when the target universe
    supports every feature required by the source statement.
    """

    name: str
    source: FiniteLogicalUniverse
    target: FiniteLogicalUniverse
    mapping: Dict[FiniteStatement, FiniteStatement] = field(default_factory=dict)
    description: str = ""

    def translate(self, statement: FiniteStatement) -> BridgeTranslation:
        """
        Translates one source statement.
        """

        target_statement = self.mapping.get(statement)

        if target_statement is None:
            return BridgeTranslation(
                source_statement=statement,
                target_statement=None,
                missing_features=statement.required_features,
            )

        missing_features = frozenset(
            statement.required_features.difference(self.target.supported_features)
        )

        return BridgeTranslation(
            source_statement=statement,
            target_statement=target_statement,
            missing_features=missing_features,
        )

    def translations(self) -> Tuple[BridgeTranslation, ...]:
        """
        Translates every statement in the source universe.
        """

        return tuple(
            self.translate(statement)
            for statement in sorted(self.source.statements, key=lambda item: item.name)
        )

    def totality(self) -> BridgeTotality:
        """
        Determines whether the bridge is total on source statements.
        """

        if all(statement in self.mapping for statement in self.source.statements):
            return BridgeTotality.TOTAL

        return BridgeTotality.PARTIAL

    def is_total(self) -> bool:
        """
        Returns whether the bridge is total.
        """

        return self.totality() == BridgeTotality.TOTAL

    def distorted_translations(self) -> Tuple[BridgeTranslation, ...]:
        """
        Returns distorted translations.
        """

        return tuple(
            translation
            for translation in self.translations()
            if translation.is_distorted()
        )

    def preserved_translations(self) -> Tuple[BridgeTranslation, ...]:
        """
        Returns preserved translations.
        """

        return tuple(
            translation
            for translation in self.translations()
            if not translation.is_distorted()
        )

    def distortion_count(self) -> int:
        """
        Counts distorted translations.
        """

        return len(self.distorted_translations())

    def preservation_count(self) -> int:
        """
        Counts preserved translations.
        """

        return len(self.preserved_translations())

    def source_features_absent_from_target(self) -> FrozenSet[SemanticFeature]:
        """
        Returns semantic features supported by source but absent from target.
        """

        return self.source.features_absent_from(self.target)

    def has_feature_mismatch(self) -> bool:
        """
        Returns whether the source supports any feature absent from the target.
        """

        return bool(self.source_features_absent_from_target())

    def statements_using_absent_features(self) -> Tuple[FiniteStatement, ...]:
        """
        Returns source statements requiring features absent from the target.
        """

        absent = self.source_features_absent_from_target()

        return tuple(
            statement
            for statement in sorted(self.source.statements, key=lambda item: item.name)
            if bool(statement.required_features.intersection(absent))
        )

    def describe(self) -> str:
        """
        Returns a readable bridge description.
        """

        return (
            f"FiniteBridge: {self.name}\n"
            f"Source: {self.source.name}\n"
            f"Target: {self.target.name}\n"
            f"Totality: {self.totality().value}\n"
            f"Feature mismatch: {self.has_feature_mismatch()}\n"
            f"Preserved translations: {self.preservation_count()}\n"
            f"Distorted translations: {self.distortion_count()}\n"
            f"Description: {self.description or 'not provided'}"
        )


def identity_bridge(universe: FiniteLogicalUniverse) -> FiniteBridge:
    """
    Builds the identity bridge on a universe.
    """

    mapping = {statement: statement for statement in universe.statements}

    return FiniteBridge(
        name=f"Identity Bridge on {universe.name}",
        source=universe,
        target=universe,
        mapping=mapping,
        description="Every statement maps to itself.",
    )


def collapse_bridge(
    name: str,
    source: FiniteLogicalUniverse,
    target: FiniteLogicalUniverse,
    target_statement_name: str = "collapsed_statement",
) -> FiniteBridge:
    """
    Builds a total collapse bridge.

    Every source statement maps to one simple target statement whose required
    features are exactly the features supported by the target universe.
    """

    collapsed_target_statement = FiniteStatement.from_features(
        name=target_statement_name,
        features=target.supported_features,
        informal_reading="A collapsed target statement used by a bridge.",
    )

    mapping = {
        statement: collapsed_target_statement
        for statement in source.statements
    }

    return FiniteBridge(
        name=name,
        source=source,
        target=target,
        mapping=mapping,
        description="A total bridge that collapses source statements into one target statement.",
    )


if __name__ == "__main__":
    from src.rigor.finite_universe import classical_finite_universe, modal_finite_universe

    source = modal_finite_universe()
    target = classical_finite_universe()
    bridge = collapse_bridge(
        name="Modal to Classical Collapse Bridge",
        source=source,
        target=target,
    )

    print(bridge.describe())

    for translation in bridge.translations():
        print()
        print(translation.describe())
