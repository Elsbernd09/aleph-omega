"""
Formal universe data model for Project ℵω.

A FormalUniverse is a toy computational model of a mathematical context.
It contains a truth-value space, a logic family, a consistency policy,
descriptive metadata, and eventually objects, morphisms, statements, and
inference rules.

This is not a full implementation of topos theory. It is a simplified,
inspectable model inspired by the idea that different mathematical universes
may have different internal logics.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .connectives import ToyConnectiveAlgebra
from .truth_values import (
    ConsistencyPolicy,
    LogicFamily,
    TruthValue,
    TruthValueSpace,
)


@dataclass(frozen=True)
class UniverseObject:
    """
    A named object inside a toy formal universe.

    Early versions only store name, kind, and metadata.
    Later phases may add richer structure.
    """

    name: str
    kind: str
    description: str = ""
    metadata: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class UniverseMorphism:
    """
    A structure-preserving relationship between two universe objects.

    This is a lightweight representation inspired by category-theoretic
    morphisms. It is not claiming full categorical rigor yet.
    """

    name: str
    source: str
    target: str
    mapping_rule: str
    preserved_structure: List[str] = field(default_factory=list)
    lost_structure: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class FormalUniverse:
    """
    Represents a toy formal mathematical universe.

    Fields:
        name:
            Human-readable universe name.

        logic_family:
            Logical family of the universe.

        truth_space:
            Truth-value space used inside the universe.

        description:
            Human-readable explanation.

        accepted_inference_rules:
            Names of inference rules accepted in this toy universe.

        rejected_inference_rules:
            Names of inference rules rejected or restricted.

        objects:
            Objects contained in the universe.

        morphisms:
            Relationships between objects.

        metadata:
            Additional notes for experiments.
    """

    name: str
    logic_family: LogicFamily
    truth_space: TruthValueSpace
    description: str
    accepted_inference_rules: List[str] = field(default_factory=list)
    rejected_inference_rules: List[str] = field(default_factory=list)
    objects: List[UniverseObject] = field(default_factory=list)
    morphisms: List[UniverseMorphism] = field(default_factory=list)
    metadata: Optional[Dict[str, str]] = None

    def consistency_policy(self) -> ConsistencyPolicy:
        """
        Returns the universe's consistency policy.
        """

        return self.truth_space.consistency_policy

    def connective_algebra(self) -> ToyConnectiveAlgebra:
        """
        Returns the toy connective algebra for this universe.
        """

        return ToyConnectiveAlgebra(self.truth_space)

    def accepts_truth_value(self, value: TruthValue) -> bool:
        """
        Checks whether this universe accepts a truth value.
        """

        return self.truth_space.contains(value)

    def supports_contradiction(self) -> bool:
        """
        Checks whether this universe can explicitly represent contradiction.
        """

        return self.truth_space.supports_contradiction()

    def supports_unknown(self) -> bool:
        """
        Checks whether this universe can explicitly represent unknown truth.
        """

        return self.truth_space.supports_unknown()

    def supports_modal_status(self) -> bool:
        """
        Checks whether this universe supports modal truth statuses.
        """

        return self.truth_space.supports_modal_status()

    def inference_rule_count(self) -> int:
        """
        Counts accepted inference rules.
        """

        return len(set(self.accepted_inference_rules))

    def rejected_rule_count(self) -> int:
        """
        Counts rejected or restricted inference rules.
        """

        return len(set(self.rejected_inference_rules))

    def object_count(self) -> int:
        """
        Counts objects.
        """

        return len(self.objects)

    def morphism_count(self) -> int:
        """
        Counts morphisms.
        """

        return len(self.morphisms)

    def expressivity_score(self) -> float:
        """
        Computes a simple toy expressivity score.

        This is a heuristic. It rewards truth-space richness, inference rules,
        objects, morphisms, and special truth behaviors.
        """

        score = 0.0
        score += self.truth_space.size() * 1.0
        score += self.inference_rule_count() * 0.5
        score += self.object_count() * 0.25
        score += self.morphism_count() * 0.35

        if self.supports_contradiction():
            score += 1.0

        if self.supports_unknown():
            score += 0.75

        if self.supports_modal_status():
            score += 1.25

        return round(min(score, 10.0), 2)

    def stability_score(self) -> float:
        """
        Computes a simple toy stability score.

        Classical and constructive universes start stable.
        Paraconsistent universes remain stable if contradiction is contained.
        Many-valued and fuzzy universes may lose some stability because truth
        interpretation is less binary.
        """

        base = 8.0

        if self.logic_family == LogicFamily.CLASSICAL:
            base += 0.5

        if self.logic_family == LogicFamily.INTUITIONISTIC:
            base += 0.75

        if self.logic_family == LogicFamily.PARACONSISTENT:
            base += 0.25 if self.supports_contradiction() else -1.0

        if self.logic_family == LogicFamily.MANY_VALUED:
            base -= 0.25

        if self.logic_family == LogicFamily.FUZZY:
            base -= 0.5

        if self.logic_family == LogicFamily.MODAL:
            base -= 0.1

        base -= self.rejected_rule_count() * 0.1

        return round(max(0.0, min(base, 10.0)), 2)

    def describe(self) -> str:
        """
        Returns a readable description of the universe.
        """

        return (
            f"FormalUniverse: {self.name}\n"
            f"Logic family: {self.logic_family.value}\n"
            f"Truth values: {', '.join(self.truth_space.value_names())}\n"
            f"Consistency policy: {self.consistency_policy().value}\n"
            f"Accepted inference rules: {', '.join(self.accepted_inference_rules) or 'none'}\n"
            f"Rejected/restricted rules: {', '.join(self.rejected_inference_rules) or 'none'}\n"
            f"Objects: {self.object_count()}\n"
            f"Morphisms: {self.morphism_count()}\n"
            f"Expressivity score: {self.expressivity_score()}\n"
            f"Stability score: {self.stability_score()}\n"
            f"Description: {self.description}"
        )
