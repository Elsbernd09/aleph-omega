"""
Topos-inspired object model for Project ℵω.

This module defines lightweight objects, morphisms, and diagrams for the toy
topos simulator.

Important:
This is not a full implementation of category theory or topos theory.
It is a simplified computational model inspired by objects, morphisms,
structure preservation, and internal mathematical environments.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class ToposObjectKind(str, Enum):
    """
    Kinds of objects that may live inside a toy topos-like universe.
    """

    GENERIC_OBJECT = "generic_object"
    TRUTH_OBJECT = "truth_object"
    STATEMENT_OBJECT = "statement_object"
    PROOF_OBJECT = "proof_object"
    CONTEXT_OBJECT = "context_object"
    PRIME_OBJECT = "prime_object"
    GRAPH_OBJECT = "graph_object"
    SUBOBJECT = "subobject"
    PRODUCT_OBJECT = "product_object"
    EXPONENTIAL_OBJECT = "exponential_object"
    GENERATED_OBJECT = "generated_object"


class MorphismKind(str, Enum):
    """
    Kinds of morphisms used in the toy topos simulator.
    """

    STRUCTURE_PRESERVING = "structure_preserving"
    TRUTH_ASSIGNMENT = "truth_assignment"
    INCLUSION = "inclusion"
    PROJECTION = "projection"
    TRANSPORT = "transport"
    INTERPRETATION = "interpretation"
    CONTEXT_SHIFT = "context_shift"
    PROOF_EXTRACTION = "proof_extraction"
    GENERATED_MORPHISM = "generated_morphism"


@dataclass(frozen=True)
class ToposObject:
    """
    A lightweight object inside a toy topos-like universe.

    Fields:
        name:
            Human-readable name.

        kind:
            Object kind.

        description:
            Explanation of the object.

        internal_symbols:
            Symbols associated with the object.

        properties:
            Structural properties of the object.

        universe_name:
            Universe where the object lives.

        metadata:
            Optional additional information.
    """

    name: str
    kind: ToposObjectKind
    description: str = ""
    internal_symbols: List[str] = field(default_factory=list)
    properties: List[str] = field(default_factory=list)
    universe_name: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def symbol_count(self) -> int:
        """
        Counts unique internal symbols.
        """

        return len(set(self.internal_symbols))

    def property_count(self) -> int:
        """
        Counts unique properties.
        """

        return len(set(self.properties))

    def structural_weight(self) -> float:
        """
        Computes a lightweight structural weight score.
        """

        score = 0.0
        score += self.symbol_count() * 0.7
        score += self.property_count() * 0.9

        if self.kind in {
            ToposObjectKind.TRUTH_OBJECT,
            ToposObjectKind.PROOF_OBJECT,
            ToposObjectKind.EXPONENTIAL_OBJECT,
        }:
            score += 1.0

        if self.kind == ToposObjectKind.SUBOBJECT:
            score += 0.75

        return round(min(score, 10.0), 2)

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        return (
            f"ToposObject: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Universe: {self.universe_name or 'not specified'}\n"
            f"Internal symbols: {', '.join(self.internal_symbols) or 'none'}\n"
            f"Properties: {', '.join(self.properties) or 'none'}\n"
            f"Structural weight: {self.structural_weight()}\n"
            f"Description: {self.description or 'none'}"
        )


@dataclass(frozen=True)
class ToposMorphism:
    """
    A lightweight morphism between two toy topos objects.

    Fields:
        name:
            Human-readable morphism name.

        source:
            Source object name.

        target:
            Target object name.

        kind:
            Morphism kind.

        mapping_rule:
            Human-readable symbolic rule.

        preserved_structure:
            Information preserved by the morphism.

        lost_structure:
            Information lost or distorted by the morphism.

        universe_name:
            Universe where the morphism lives.

        metadata:
            Optional additional information.
    """

    name: str
    source: str
    target: str
    kind: MorphismKind
    mapping_rule: str
    preserved_structure: List[str] = field(default_factory=list)
    lost_structure: List[str] = field(default_factory=list)
    universe_name: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def preservation_score(self) -> float:
        """
        Computes a simple preservation score.
        """

        preserved = len(set(self.preserved_structure))
        lost = len(set(self.lost_structure))
        total = max(preserved + lost, 1)

        return round(10.0 * preserved / total, 2)

    def distortion_score(self) -> float:
        """
        Computes a simple distortion score.
        """

        return round(10.0 - self.preservation_score(), 2)

    def describe(self) -> str:
        """
        Returns a readable description.
        """

        return (
            f"ToposMorphism: {self.name}\n"
            f"Kind: {self.kind.value}\n"
            f"Source: {self.source}\n"
            f"Target: {self.target}\n"
            f"Universe: {self.universe_name or 'not specified'}\n"
            f"Mapping rule: {self.mapping_rule}\n"
            f"Preserved structure: {', '.join(self.preserved_structure) or 'none'}\n"
            f"Lost structure: {', '.join(self.lost_structure) or 'none'}\n"
            f"Preservation score: {self.preservation_score()}\n"
            f"Distortion score: {self.distortion_score()}"
        )


@dataclass(frozen=True)
class ToposDiagram:
    """
    A small diagram consisting of objects and morphisms.

    This is a lightweight category-inspired structure for experiments.
    """

    name: str
    objects: List[ToposObject] = field(default_factory=list)
    morphisms: List[ToposMorphism] = field(default_factory=list)
    description: str = ""
    metadata: Optional[Dict[str, str]] = None

    def object_names(self) -> List[str]:
        """
        Returns object names.
        """

        return [obj.name for obj in self.objects]

    def morphism_names(self) -> List[str]:
        """
        Returns morphism names.
        """

        return [morphism.name for morphism in self.morphisms]

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

    def average_preservation_score(self) -> float:
        """
        Computes average morphism preservation score.
        """

        if not self.morphisms:
            return 0.0

        total = sum(morphism.preservation_score() for morphism in self.morphisms)
        return round(total / len(self.morphisms), 2)

    def structural_density(self) -> float:
        """
        Computes a simple diagram density score.

        This is not a categorical invariant. It is a toy metric for comparing
        diagrams inside experiments.
        """

        possible_edges = max(self.object_count() * (self.object_count() - 1), 1)
        density = self.morphism_count() / possible_edges

        return round(min(density * 10.0, 10.0), 2)

    def validate_references(self) -> bool:
        """
        Checks whether all morphism source and target references exist.
        """

        names = set(self.object_names())

        for morphism in self.morphisms:
            if morphism.source not in names or morphism.target not in names:
                return False

        return True

    def describe(self) -> str:
        """
        Returns a readable diagram description.
        """

        return (
            f"ToposDiagram: {self.name}\n"
            f"Objects: {self.object_count()} ({', '.join(self.object_names()) or 'none'})\n"
            f"Morphisms: {self.morphism_count()} ({', '.join(self.morphism_names()) or 'none'})\n"
            f"Valid references: {self.validate_references()}\n"
            f"Average preservation score: {self.average_preservation_score()}\n"
            f"Structural density: {self.structural_density()}\n"
            f"Description: {self.description or 'none'}"
        )


def starter_topos_diagram() -> ToposDiagram:
    """
    Creates a starter toy diagram for Phase 4 experiments.
    """

    statement_object = ToposObject(
        name="Statement",
        kind=ToposObjectKind.STATEMENT_OBJECT,
        description="A proposition-like object inside a formal universe.",
        internal_symbols=["P", "truth", "interpretation"],
        properties=["interpretable", "truth_evaluable"],
        universe_name="Generic Toy Universe",
    )

    truth_object = ToposObject(
        name="TruthObject",
        kind=ToposObjectKind.TRUTH_OBJECT,
        description="A symbolic object representing available truth values.",
        internal_symbols=["true", "false", "unknown", "both"],
        properties=["classifies_statements"],
        universe_name="Generic Toy Universe",
    )

    context_object = ToposObject(
        name="Context",
        kind=ToposObjectKind.CONTEXT_OBJECT,
        description="An interpretation environment for statements.",
        internal_symbols=["C", "U"],
        properties=["interpretation_dependent"],
        universe_name="Generic Toy Universe",
    )

    truth_assignment = ToposMorphism(
        name="truth_assignment",
        source="Statement",
        target="TruthObject",
        kind=MorphismKind.TRUTH_ASSIGNMENT,
        mapping_rule="assign a statement to a truth value inside a context",
        preserved_structure=["statement_identity", "truth_status"],
        lost_structure=["informal_ambiguity"],
        universe_name="Generic Toy Universe",
    )

    interpretation = ToposMorphism(
        name="interpretation",
        source="Context",
        target="Statement",
        kind=MorphismKind.INTERPRETATION,
        mapping_rule="interpret a symbolic statement under a context",
        preserved_structure=["symbolic_form", "context_dependency"],
        lost_structure=[],
        universe_name="Generic Toy Universe",
    )

    return ToposDiagram(
        name="Starter Internal Truth Diagram",
        objects=[statement_object, truth_object, context_object],
        morphisms=[truth_assignment, interpretation],
        description=(
            "A starter diagram showing how statements, contexts, and truth "
            "objects interact in the toy topos layer."
        ),
    )


if __name__ == "__main__":
    diagram = starter_topos_diagram()
    print(diagram.describe())
    print("-" * 80)

    for obj in diagram.objects:
        print(obj.describe())
        print("-" * 80)

    for morphism in diagram.morphisms:
        print(morphism.describe())
        print("-" * 80)
