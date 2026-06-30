"""
Bridge map model for Project ℵω.

A bridge map describes how statements, symbols, truth values, and proof
statuses are translated from one toy formal universe into another.

This module is intentionally heuristic. It does not claim that a bridge is a
complete functor, geometric morphism, interpretation, or formal equivalence.
It is a computational model for tracking preservation and distortion.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.toy_topoi.statements import ProofStatus
from src.toy_topoi.truth_values import TruthValue


class BridgeKind(str, Enum):
    """
    High-level kind of bridge between universes.
    """

    IDENTITY = "identity"
    LOGIC_FORGETFUL = "logic_forgetful"
    CONTRADICTION_COLLAPSING = "contradiction_collapsing"
    MODAL_FORGETFUL = "modal_forgetful"
    CONSTRUCTIVE_TO_CLASSICAL = "constructive_to_classical"
    CLASSICAL_TO_CONSTRUCTIVE = "classical_to_constructive"
    MANY_VALUED_TO_BINARY = "many_valued_to_binary"
    BINARY_TO_MANY_VALUED = "binary_to_many_valued"
    CONTEXTUAL_TRANSLATION = "contextual_translation"
    GENERATED_EXPERIMENTAL = "generated_experimental"


class BridgeRisk(str, Enum):
    """
    Risk level of a bridge.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass(frozen=True)
class SymbolMapping:
    """
    Maps one source symbol to a target symbol.
    """

    source_symbol: str
    target_symbol: Optional[str]
    preserves_meaning: bool = True
    notes: str = ""

    def is_loss(self) -> bool:
        """
        Returns whether the symbol is lost during translation.
        """

        return self.target_symbol is None

    def describe(self) -> str:
        """
        Returns a readable mapping description.
        """

        target = self.target_symbol if self.target_symbol is not None else "LOST"

        return (
            f"{self.source_symbol} -> {target} "
            f"(preserves_meaning={self.preserves_meaning})"
        )


@dataclass(frozen=True)
class FeatureMapping:
    """
    Maps one required source feature to a target feature.
    """

    source_feature: str
    target_feature: Optional[str]
    preserves_feature: bool = True
    notes: str = ""

    def is_loss(self) -> bool:
        """
        Returns whether the feature is lost during translation.
        """

        return self.target_feature is None

    def describe(self) -> str:
        """
        Returns a readable mapping description.
        """

        target = self.target_feature if self.target_feature is not None else "LOST"

        return (
            f"{self.source_feature} -> {target} "
            f"(preserves_feature={self.preserves_feature})"
        )


@dataclass(frozen=True)
class BridgeMap:
    """
    Translation bridge between two toy formal universes.
    """

    name: str
    source_universe_name: str
    target_universe_name: str
    kind: BridgeKind
    symbol_mappings: List[SymbolMapping] = field(default_factory=list)
    feature_mappings: List[FeatureMapping] = field(default_factory=list)
    truth_value_mapping: Dict[TruthValue, TruthValue] = field(default_factory=dict)
    proof_status_mapping: Dict[ProofStatus, ProofStatus] = field(default_factory=dict)
    risk: BridgeRisk = BridgeRisk.MEDIUM
    notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def is_identity_bridge(self) -> bool:
        """
        Returns whether this bridge maps a universe to itself.
        """

        return self.source_universe_name == self.target_universe_name

    def map_symbol(self, symbol: str) -> Optional[str]:
        """
        Maps a symbol using the bridge map.

        If no explicit mapping is present, the symbol is preserved by default.
        """

        for mapping in self.symbol_mappings:
            if mapping.source_symbol == symbol:
                return mapping.target_symbol

        return symbol

    def map_feature(self, feature: str) -> Optional[str]:
        """
        Maps a feature using the bridge map.

        If no explicit mapping is present, the feature is preserved by default.
        """

        for mapping in self.feature_mappings:
            if mapping.source_feature == feature:
                return mapping.target_feature

        return feature

    def map_truth_value(self, truth_value: TruthValue) -> TruthValue:
        """
        Maps a truth value.

        If no explicit mapping exists, the truth value is preserved.
        """

        return self.truth_value_mapping.get(truth_value, truth_value)

    def map_proof_status(self, proof_status: ProofStatus) -> ProofStatus:
        """
        Maps a proof status.

        If no explicit mapping exists, the proof status is preserved.
        """

        return self.proof_status_mapping.get(proof_status, proof_status)

    def lost_symbol_names(self) -> List[str]:
        """
        Returns explicitly lost symbols.
        """

        return sorted(
            mapping.source_symbol
            for mapping in self.symbol_mappings
            if mapping.is_loss()
        )

    def lost_feature_names(self) -> List[str]:
        """
        Returns explicitly lost features.
        """

        return sorted(
            mapping.source_feature
            for mapping in self.feature_mappings
            if mapping.is_loss()
        )

    def symbol_preservation_rate(self) -> float:
        """
        Computes explicit symbol preservation rate.
        """

        if not self.symbol_mappings:
            return 1.0

        preserved = sum(1 for mapping in self.symbol_mappings if not mapping.is_loss())
        return round(preserved / len(self.symbol_mappings), 3)

    def feature_preservation_rate(self) -> float:
        """
        Computes explicit feature preservation rate.
        """

        if not self.feature_mappings:
            return 1.0

        preserved = sum(1 for mapping in self.feature_mappings if not mapping.is_loss())
        return round(preserved / len(self.feature_mappings), 3)

    def bridge_strength_score(self) -> float:
        """
        Computes a toy bridge strength score from 0 to 10.

        Higher means the bridge is expected to preserve more structure.
        """

        score = 10.0
        score -= (1.0 - self.symbol_preservation_rate()) * 3.0
        score -= (1.0 - self.feature_preservation_rate()) * 4.0

        if self.risk == BridgeRisk.MEDIUM:
            score -= 1.0
        elif self.risk == BridgeRisk.HIGH:
            score -= 2.0
        elif self.risk == BridgeRisk.EXTREME:
            score -= 3.5

        if self.kind in {
            BridgeKind.CONTRADICTION_COLLAPSING,
            BridgeKind.MODAL_FORGETFUL,
            BridgeKind.MANY_VALUED_TO_BINARY,
        }:
            score -= 1.0

        if self.kind == BridgeKind.IDENTITY:
            score += 1.0

        return round(max(0.0, min(10.0, score)), 2)

    def describe(self) -> str:
        """
        Returns a readable bridge description.
        """

        symbol_lines = "\n".join(
            f"  - {mapping.describe()}" for mapping in self.symbol_mappings
        ) or "  - none"

        feature_lines = "\n".join(
            f"  - {mapping.describe()}" for mapping in self.feature_mappings
        ) or "  - none"

        truth_lines = "\n".join(
            f"  - {source.value} -> {target.value}"
            for source, target in self.truth_value_mapping.items()
        ) or "  - default preserve"

        proof_lines = "\n".join(
            f"  - {source.value} -> {target.value}"
            for source, target in self.proof_status_mapping.items()
        ) or "  - default preserve"

        return (
            f"BridgeMap: {self.name}\n"
            f"Source universe: {self.source_universe_name}\n"
            f"Target universe: {self.target_universe_name}\n"
            f"Kind: {self.kind.value}\n"
            f"Risk: {self.risk.value}\n"
            f"Bridge strength score: {self.bridge_strength_score()}\n"
            f"Symbol preservation rate: {self.symbol_preservation_rate()}\n"
            f"Feature preservation rate: {self.feature_preservation_rate()}\n"
            f"Symbol mappings:\n{symbol_lines}\n"
            f"Feature mappings:\n{feature_lines}\n"
            f"Truth-value mappings:\n{truth_lines}\n"
            f"Proof-status mappings:\n{proof_lines}\n"
            f"Notes: {self.notes or 'none'}"
        )


def identity_bridge(universe_name: str) -> BridgeMap:
    """
    Creates an identity bridge for a universe.
    """

    return BridgeMap(
        name=f"Identity Bridge: {universe_name}",
        source_universe_name=universe_name,
        target_universe_name=universe_name,
        kind=BridgeKind.IDENTITY,
        risk=BridgeRisk.LOW,
        notes="Preserves the universe by translating it into itself.",
    )


def paraconsistent_to_classical_bridge(
    source_universe_name: str,
    target_universe_name: str,
) -> BridgeMap:
    """
    Creates a bridge from a contradiction-tolerant universe to a classical one.
    """

    return BridgeMap(
        name="Paraconsistent to Classical Collapse Bridge",
        source_universe_name=source_universe_name,
        target_universe_name=target_universe_name,
        kind=BridgeKind.CONTRADICTION_COLLAPSING,
        symbol_mappings=[
            SymbolMapping("both", None, False, "Classical logic cannot preserve BOTH."),
            SymbolMapping("neither", None, False, "Classical logic cannot preserve NEITHER."),
            SymbolMapping("contradiction", None, False, "Contradiction support is collapsed."),
        ],
        feature_mappings=[
            FeatureMapping(
                "contradiction_support",
                None,
                False,
                "Classical explosion does not preserve local contradiction containment.",
            )
        ],
        truth_value_mapping={
            TruthValue.BOTH: TruthValue.FALSE,
            TruthValue.NEITHER: TruthValue.FALSE,
            TruthValue.UNKNOWN: TruthValue.FALSE,
        },
        proof_status_mapping={
            ProofStatus.CONTRADICTORY: ProofStatus.REFUTED,
            ProofStatus.HUMAN_REVIEW_REQUIRED: ProofStatus.HUMAN_REVIEW_REQUIRED,
        },
        risk=BridgeRisk.HIGH,
        notes=(
            "This bridge intentionally shows how contradiction-tolerant meaning "
            "is damaged when transported into a strict classical universe."
        ),
    )


def modal_to_classical_bridge(
    source_universe_name: str,
    target_universe_name: str,
) -> BridgeMap:
    """
    Creates a bridge from a modal universe to a classical one.
    """

    return BridgeMap(
        name="Modal to Classical Forgetful Bridge",
        source_universe_name=source_universe_name,
        target_universe_name=target_universe_name,
        kind=BridgeKind.MODAL_FORGETFUL,
        symbol_mappings=[
            SymbolMapping("possible", None, False, "Possibility is erased."),
            SymbolMapping("necessary", None, False, "Necessity is erased."),
            SymbolMapping("contingent", None, False, "Contingency is erased."),
            SymbolMapping("impossible", None, False, "Impossibility is erased."),
        ],
        feature_mappings=[
            FeatureMapping(
                "modal_support",
                None,
                False,
                "Classical truth values do not preserve modal status.",
            )
        ],
        truth_value_mapping={
            TruthValue.POSSIBLE: TruthValue.TRUE,
            TruthValue.NECESSARY: TruthValue.TRUE,
            TruthValue.CONTINGENT: TruthValue.TRUE,
            TruthValue.IMPOSSIBLE: TruthValue.FALSE,
            TruthValue.UNKNOWN: TruthValue.FALSE,
        },
        risk=BridgeRisk.HIGH,
        notes=(
            "This bridge collapses modal structure into ordinary true/false status."
        ),
    )


def intuitionistic_to_classical_bridge(
    source_universe_name: str,
    target_universe_name: str,
) -> BridgeMap:
    """
    Creates a bridge from constructive reasoning to classical reasoning.
    """

    return BridgeMap(
        name="Constructive to Classical Weakening Bridge",
        source_universe_name=source_universe_name,
        target_universe_name=target_universe_name,
        kind=BridgeKind.CONSTRUCTIVE_TO_CLASSICAL,
        symbol_mappings=[
            SymbolMapping(
                "witness",
                None,
                False,
                "Witness information may be forgotten by classical existence.",
            )
        ],
        feature_mappings=[
            FeatureMapping(
                "constructive_evidence",
                "existential_reasoning",
                False,
                "Constructive evidence weakens into ordinary existence.",
            )
        ],
        proof_status_mapping={
            ProofStatus.UNKNOWN: ProofStatus.UNTESTED,
            ProofStatus.HUMAN_REVIEW_REQUIRED: ProofStatus.HUMAN_REVIEW_REQUIRED,
        },
        risk=BridgeRisk.MEDIUM,
        notes=(
            "This bridge preserves some existential meaning while weakening "
            "the requirement for explicit construction."
        ),
    )


def starter_bridge_maps() -> List[BridgeMap]:
    """
    Returns starter bridge maps for Phase 5 experiments.
    """

    return [
        paraconsistent_to_classical_bridge(
            source_universe_name="Paraconsistent Contradiction-Tolerant Universe",
            target_universe_name="Classical Set-Theoretic Neighborhood",
        ),
        modal_to_classical_bridge(
            source_universe_name="Modal Possibility Universe",
            target_universe_name="Classical Set-Theoretic Neighborhood",
        ),
        intuitionistic_to_classical_bridge(
            source_universe_name="Intuitionistic Constructive Universe",
            target_universe_name="Classical Set-Theoretic Neighborhood",
        ),
    ]


if __name__ == "__main__":
    for bridge in starter_bridge_maps():
        print(bridge.describe())
        print("-" * 80)
