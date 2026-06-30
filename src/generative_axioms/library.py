"""
Hand-designed axiom library for Project ℵω.

This module defines a starter set of experimental axioms used by the
Generative Axiom Engine. These axioms are not claimed to be true mathematics.
They are structured toy assumptions for testing representation, scoring,
comparison, and later bridge-transport behavior.
"""

from typing import List

from .axiom import Axiom, AxiomDomain, AxiomStatus


def foundational_axioms() -> List[Axiom]:
    """
    Returns a starter library of hand-designed experimental axioms.

    The axioms are grouped around identity, context, truth, contradiction,
    inference, transport, modality, prime geometry, and cognitive morphism.
    """

    return [
        Axiom(
            name="Contextual Identity",
            informal_statement=(
                "Identity between objects is evaluated relative to an "
                "interpretation context rather than assumed to be absolute."
            ),
            symbolic_sketch="identity(x, y, C) depends_on context(C)",
            domains=[
                AxiomDomain.IDENTITY,
                AxiomDomain.CONTEXT,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=["identity", "object", "context", "depends_on"],
            compatible_universes=[
                "classical",
                "intuitionistic",
                "many_valued",
                "modal",
            ],
            incompatible_universes=[],
            dependencies=["interpretation_context"],
            notes=(
                "This axiom lets the system study how equality-like relations "
                "may change when a statement moves between contexts."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Truth Relativity",
            informal_statement=(
                "The truth status of a statement is determined inside a "
                "chosen formal universe."
            ),
            symbolic_sketch="truth(P, U) where U is a formal_universe",
            domains=[
                AxiomDomain.TRUTH,
                AxiomDomain.CONTEXT,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=["truth", "statement", "universe", "evaluation"],
            compatible_universes=[
                "classical",
                "intuitionistic",
                "paraconsistent",
                "many_valued",
                "modal",
                "fuzzy",
            ],
            incompatible_universes=[],
            dependencies=["formal_universe", "truth_value_space"],
            notes=(
                "This axiom supports the project philosophy that statements "
                "are interpreted inside universes rather than in isolation."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Local Contradiction Containment",
            informal_statement=(
                "A contradiction may remain local inside a universe without "
                "forcing all statements to become derivable."
            ),
            symbolic_sketch="contradiction(P, not_P) does_not_imply arbitrary(Q)",
            domains=[
                AxiomDomain.CONTRADICTION,
                AxiomDomain.INFERENCE,
                AxiomDomain.TRUTH,
            ],
            symbols_used=[
                "contradiction",
                "negation",
                "implication",
                "arbitrary_statement",
            ],
            compatible_universes=[
                "paraconsistent",
                "many_valued",
            ],
            incompatible_universes=[
                "strict_classical",
            ],
            dependencies=["negation", "inference_rule", "truth_value_space"],
            notes=(
                "This axiom supports experiments in paraconsistent reasoning, "
                "where inconsistency does not automatically collapse the system."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Constructive Witness Requirement",
            informal_statement=(
                "An existential statement is accepted only when a witness or "
                "construction is available."
            ),
            symbolic_sketch="exists(x, P(x)) requires witness(x)",
            domains=[
                AxiomDomain.INFERENCE,
                AxiomDomain.TRUTH,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=[
                "exists",
                "property",
                "witness",
                "construction",
            ],
            compatible_universes=[
                "intuitionistic",
            ],
            incompatible_universes=[],
            dependencies=["proof_status", "witness"],
            notes=(
                "This axiom models the constructive emphasis that existence "
                "requires explicit mathematical evidence."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Transport Distortion",
            informal_statement=(
                "When a statement is transported from one universe to another, "
                "some symbolic or semantic structure may be preserved while "
                "other structure may be distorted or lost."
            ),
            symbolic_sketch="transport(P, U_source, U_target) -> preservation + distortion + loss",
            domains=[
                AxiomDomain.TRANSPORT,
                AxiomDomain.CONTEXT,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=[
                "transport",
                "statement",
                "source_universe",
                "target_universe",
                "preservation",
                "distortion",
                "loss",
            ],
            compatible_universes=[
                "classical",
                "intuitionistic",
                "paraconsistent",
                "many_valued",
                "modal",
                "fuzzy",
            ],
            incompatible_universes=[],
            dependencies=["bridge", "formal_universe"],
            notes=(
                "This axiom is central to the Bridge Engine because it makes "
                "translation effects explicit rather than hidden."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Modal Status Expansion",
            informal_statement=(
                "A statement may be classified not only as true or false, "
                "but also as necessary, possible, impossible, or contingent."
            ),
            symbolic_sketch="modal_status(P) in {necessary, possible, impossible, contingent}",
            domains=[
                AxiomDomain.MODALITY,
                AxiomDomain.TRUTH,
            ],
            symbols_used=[
                "statement",
                "necessary",
                "possible",
                "impossible",
                "contingent",
            ],
            compatible_universes=[
                "modal",
            ],
            incompatible_universes=[
                "strict_classical_without_modal_operators",
            ],
            dependencies=["modal_status", "truth_value_space"],
            notes=(
                "This axiom supports modal-universe experiments where truth "
                "is enriched by necessity and possibility."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Prime Relational Embedding",
            informal_statement=(
                "A prime number can be represented as a node in a relational "
                "structure whose edges encode arithmetic or geometric features."
            ),
            symbolic_sketch="prime(p) -> node(p) in graph G with arithmetic_edges",
            domains=[
                AxiomDomain.PRIME_GEOMETRY,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=[
                "prime",
                "node",
                "graph",
                "edge",
                "arithmetic_relation",
            ],
            compatible_universes=[
                "classical",
                "many_valued",
            ],
            incompatible_universes=[],
            dependencies=["prime", "graph_representation"],
            notes=(
                "This axiom supports the Prime Geometry Lab. It is a modeling "
                "assumption, not a proof of a number-theoretic conjecture."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
        Axiom(
            name="Intuition Formalization Gap",
            informal_statement=(
                "Informal mathematical intuition may contain structure that "
                "is not yet explicit as definitions, assumptions, or proof goals."
            ),
            symbolic_sketch="intuition(I) -> partial_structure(objects, relations, goals, ambiguities)",
            domains=[
                AxiomDomain.COGNITIVE_MORPHISM,
                AxiomDomain.CONTEXT,
                AxiomDomain.GENERAL_FOUNDATIONS,
            ],
            symbols_used=[
                "intuition",
                "object",
                "relation",
                "goal",
                "ambiguity",
                "formalization",
            ],
            compatible_universes=[
                "classical",
                "intuitionistic",
                "modal",
            ],
            incompatible_universes=[],
            dependencies=["cognitive_morphism", "symbolic_statement"],
            notes=(
                "This axiom supports the Cognitive Morphism Engine by treating "
                "intuition as partially structured but not yet formalized."
            ),
            status=AxiomStatus.HAND_DESIGNED,
        ),
    ]


def get_axiom_names() -> List[str]:
    """
    Returns the names of all starter axioms.
    """

    return [axiom.name for axiom in foundational_axioms()]


def find_axiom_by_name(name: str) -> Axiom:
    """
    Finds an axiom by exact name.

    Raises:
        ValueError: if no axiom with the given name exists.
    """

    for axiom in foundational_axioms():
        if axiom.name == name:
            return axiom

    raise ValueError(f"No axiom found with name: {name}")


if __name__ == "__main__":
    for axiom in foundational_axioms():
        print(axiom.describe())
        print("-" * 80)
