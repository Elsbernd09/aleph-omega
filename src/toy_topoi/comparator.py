"""
Universe comparison engine for Project ℵω.

This module compares toy formal universes by truth values, logic family,
consistency policy, inference rules, expressivity, stability, and translation
compatibility.

These comparisons are heuristic. They are not mathematical equivalence proofs.
"""

from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from .truth_values import LogicFamily, TruthValue
from .universe import FormalUniverse


@dataclass(frozen=True)
class UniverseComparison:
    """
    Stores comparison results between two toy universes.
    """

    source_name: str
    target_name: str
    source_logic: str
    target_logic: str
    shared_truth_values: List[str]
    source_only_truth_values: List[str]
    target_only_truth_values: List[str]
    shared_inference_rules: List[str]
    source_only_inference_rules: List[str]
    target_only_inference_rules: List[str]
    contradiction_compatibility: str
    unknown_compatibility: str
    modal_compatibility: str
    expressivity_gap: float
    stability_gap: float
    compatibility_score: float
    interpretation: str

    def as_dict(self) -> Dict[str, object]:
        """
        Converts the comparison into a dictionary.
        """

        return {
            "source_name": self.source_name,
            "target_name": self.target_name,
            "source_logic": self.source_logic,
            "target_logic": self.target_logic,
            "shared_truth_values": self.shared_truth_values,
            "source_only_truth_values": self.source_only_truth_values,
            "target_only_truth_values": self.target_only_truth_values,
            "shared_inference_rules": self.shared_inference_rules,
            "source_only_inference_rules": self.source_only_inference_rules,
            "target_only_inference_rules": self.target_only_inference_rules,
            "contradiction_compatibility": self.contradiction_compatibility,
            "unknown_compatibility": self.unknown_compatibility,
            "modal_compatibility": self.modal_compatibility,
            "expressivity_gap": self.expressivity_gap,
            "stability_gap": self.stability_gap,
            "compatibility_score": self.compatibility_score,
            "interpretation": self.interpretation,
        }


class UniverseComparator:
    """
    Compares toy formal universes.

    The goal is to make structural differences between logical environments
    explicit and inspectable.
    """

    def compare(self, source: FormalUniverse, target: FormalUniverse) -> UniverseComparison:
        """
        Compares a source universe to a target universe.
        """

        source_truth = set(source.truth_space.values)
        target_truth = set(target.truth_space.values)

        shared_truth = self._sorted_truth_values(source_truth.intersection(target_truth))
        source_only_truth = self._sorted_truth_values(source_truth.difference(target_truth))
        target_only_truth = self._sorted_truth_values(target_truth.difference(source_truth))

        source_rules = set(source.accepted_inference_rules)
        target_rules = set(target.accepted_inference_rules)

        shared_rules = sorted(source_rules.intersection(target_rules))
        source_only_rules = sorted(source_rules.difference(target_rules))
        target_only_rules = sorted(target_rules.difference(source_rules))

        contradiction_compatibility = self._feature_compatibility(
            source.supports_contradiction(),
            target.supports_contradiction(),
            feature_name="contradiction",
        )

        unknown_compatibility = self._feature_compatibility(
            source.supports_unknown(),
            target.supports_unknown(),
            feature_name="unknown truth",
        )

        modal_compatibility = self._feature_compatibility(
            source.supports_modal_status(),
            target.supports_modal_status(),
            feature_name="modal status",
        )

        expressivity_gap = round(abs(source.expressivity_score() - target.expressivity_score()), 2)
        stability_gap = round(abs(source.stability_score() - target.stability_score()), 2)

        compatibility_score = self._compatibility_score(
            source=source,
            target=target,
            shared_truth_count=len(shared_truth),
            source_truth_count=len(source_truth),
            target_truth_count=len(target_truth),
            shared_rule_count=len(shared_rules),
            source_rule_count=len(source_rules),
            target_rule_count=len(target_rules),
            expressivity_gap=expressivity_gap,
            stability_gap=stability_gap,
        )

        interpretation = self._interpretation(
            source=source,
            target=target,
            compatibility_score=compatibility_score,
            contradiction_compatibility=contradiction_compatibility,
            modal_compatibility=modal_compatibility,
        )

        return UniverseComparison(
            source_name=source.name,
            target_name=target.name,
            source_logic=source.logic_family.value,
            target_logic=target.logic_family.value,
            shared_truth_values=shared_truth,
            source_only_truth_values=source_only_truth,
            target_only_truth_values=target_only_truth,
            shared_inference_rules=shared_rules,
            source_only_inference_rules=source_only_rules,
            target_only_inference_rules=target_only_rules,
            contradiction_compatibility=contradiction_compatibility,
            unknown_compatibility=unknown_compatibility,
            modal_compatibility=modal_compatibility,
            expressivity_gap=expressivity_gap,
            stability_gap=stability_gap,
            compatibility_score=compatibility_score,
            interpretation=interpretation,
        )

    def compare_all(self, universes: List[FormalUniverse]) -> List[UniverseComparison]:
        """
        Compares every ordered pair of distinct universes.
        """

        comparisons: List[UniverseComparison] = []

        for source in universes:
            for target in universes:
                if source.name != target.name:
                    comparisons.append(self.compare(source, target))

        return comparisons

    @staticmethod
    def _sorted_truth_values(values: Set[TruthValue]) -> List[str]:
        """
        Sorts truth values by their string names.
        """

        return sorted(value.value for value in values)

    @staticmethod
    def _feature_compatibility(source_has: bool, target_has: bool, feature_name: str) -> str:
        """
        Explains whether a feature is preserved between source and target.
        """

        if source_has and target_has:
            return f"{feature_name} preserved"

        if source_has and not target_has:
            return f"{feature_name} lost in target"

        if not source_has and target_has:
            return f"{feature_name} added in target"

        return f"{feature_name} absent in both"

    @staticmethod
    def _ratio(shared: int, left_count: int, right_count: int) -> float:
        """
        Computes a symmetric overlap ratio.
        """

        denominator = max(left_count, right_count, 1)
        return shared / denominator

    def _compatibility_score(
        self,
        source: FormalUniverse,
        target: FormalUniverse,
        shared_truth_count: int,
        source_truth_count: int,
        target_truth_count: int,
        shared_rule_count: int,
        source_rule_count: int,
        target_rule_count: int,
        expressivity_gap: float,
        stability_gap: float,
    ) -> float:
        """
        Computes a heuristic compatibility score from 0 to 10.
        """

        truth_overlap = self._ratio(shared_truth_count, source_truth_count, target_truth_count)
        rule_overlap = self._ratio(shared_rule_count, source_rule_count, target_rule_count)

        score = 0.0
        score += truth_overlap * 3.0
        score += rule_overlap * 2.0
        score += max(0.0, 2.0 - expressivity_gap * 0.25)
        score += max(0.0, 2.0 - stability_gap * 0.30)

        if source.logic_family == target.logic_family:
            score += 1.0

        if source.supports_contradiction() and not target.supports_contradiction():
            score -= 1.0

        if source.supports_modal_status() and not target.supports_modal_status():
            score -= 0.8

        if source.logic_family == LogicFamily.INTUITIONISTIC and target.logic_family == LogicFamily.CLASSICAL:
            score += 0.2

        if source.logic_family == LogicFamily.CLASSICAL and target.logic_family == LogicFamily.INTUITIONISTIC:
            score -= 0.3

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _interpretation(
        source: FormalUniverse,
        target: FormalUniverse,
        compatibility_score: float,
        contradiction_compatibility: str,
        modal_compatibility: str,
    ) -> str:
        """
        Produces a human-readable interpretation.
        """

        if compatibility_score >= 7.5:
            base = "high compatibility"
        elif compatibility_score >= 5.0:
            base = "moderate compatibility"
        elif compatibility_score >= 3.0:
            base = "low compatibility"
        else:
            base = "severe translation difficulty"

        notes: List[str] = []

        if "lost in target" in contradiction_compatibility:
            notes.append("contradiction information may collapse or be erased")

        if "lost in target" in modal_compatibility:
            notes.append("modal information may be lost")

        if source.logic_family == LogicFamily.CLASSICAL and target.logic_family == LogicFamily.INTUITIONISTIC:
            notes.append("classical assumptions may require constructive evidence")

        if source.logic_family == LogicFamily.PARACONSISTENT and target.logic_family == LogicFamily.CLASSICAL:
            notes.append("locally contained contradictions may become classically unstable")

        if not notes:
            notes.append("major structural features are relatively interpretable")

        return f"{base}: " + "; ".join(notes)
