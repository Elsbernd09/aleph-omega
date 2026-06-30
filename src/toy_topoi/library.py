"""
Toy universe library for Project ℵω.

This module defines a starter collection of formal universes used by the toy
topos layer. These universes are simplified computational models. They are
not complete implementations of mathematical foundations, logic, or topos
theory.
"""

from typing import List

from .truth_values import (
    LogicFamily,
    classical_truth_space,
    intuitionistic_truth_space,
    paraconsistent_truth_space,
    many_valued_truth_space,
    modal_truth_space,
    fuzzy_symbolic_truth_space,
)
from .universe import FormalUniverse, UniverseMorphism, UniverseObject


def classical_universe() -> FormalUniverse:
    """
    Returns a toy classical universe.
    """

    return FormalUniverse(
        name="Classical Set-Theoretic Neighborhood",
        logic_family=LogicFamily.CLASSICAL,
        truth_space=classical_truth_space(),
        description=(
            "A toy universe representing ordinary two-valued mathematical "
            "reasoning. It accepts classical truth behavior, the law of "
            "excluded middle, and proof by contradiction."
        ),
        accepted_inference_rules=[
            "modus_ponens",
            "law_of_excluded_middle",
            "double_negation_elimination",
            "proof_by_contradiction",
            "universal_instantiation",
        ],
        rejected_inference_rules=[
            "local_contradiction_containment",
        ],
        objects=[
            UniverseObject(
                name="proposition",
                kind="logical_object",
                description="A statement that can be assigned true or false.",
            ),
            UniverseObject(
                name="set",
                kind="mathematical_object",
                description="A classical collection-like object.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="truth_assignment",
                source="proposition",
                target="truth_value",
                mapping_rule="assign each proposition either true or false",
                preserved_structure=["binary_truth"],
                lost_structure=["unknown_status", "both_status"],
            ),
        ],
        metadata={
            "role": "baseline universe",
            "risk": "contradictions are explosive",
        },
    )


def intuitionistic_universe() -> FormalUniverse:
    """
    Returns a toy intuitionistic universe.
    """

    return FormalUniverse(
        name="Intuitionistic Constructive Universe",
        logic_family=LogicFamily.INTUITIONISTIC,
        truth_space=intuitionistic_truth_space(),
        description=(
            "A toy universe representing constructive reasoning. Statements "
            "are accepted when proof evidence, construction, or a witness is "
            "available. Unsupported claims may remain unknown."
        ),
        accepted_inference_rules=[
            "modus_ponens",
            "constructive_proof",
            "witness_requirement",
            "direct_construction",
            "universal_instantiation",
        ],
        rejected_inference_rules=[
            "unrestricted_law_of_excluded_middle",
            "unrestricted_proof_by_contradiction",
            "double_negation_elimination_without_evidence",
        ],
        objects=[
            UniverseObject(
                name="construction",
                kind="proof_object",
                description="Evidence that builds or witnesses a statement.",
            ),
            UniverseObject(
                name="proof_goal",
                kind="formal_goal",
                description="A statement requiring constructive evidence.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="witness_map",
                source="existential_statement",
                target="construction",
                mapping_rule="map an existence claim to an explicit witness",
                preserved_structure=["constructive_evidence"],
                lost_structure=["nonconstructive_existence"],
            ),
        ],
        metadata={
            "role": "proof-sensitive universe",
            "risk": "some classical statements become unsupported",
        },
    )


def paraconsistent_universe() -> FormalUniverse:
    """
    Returns a toy paraconsistent universe.
    """

    return FormalUniverse(
        name="Paraconsistent Contradiction-Tolerant Universe",
        logic_family=LogicFamily.PARACONSISTENT,
        truth_space=paraconsistent_truth_space(),
        description=(
            "A toy universe where contradictions can be represented locally "
            "without making every statement derivable. This universe is useful "
            "for studying inconsistency without collapse."
        ),
        accepted_inference_rules=[
            "modus_ponens_restricted",
            "local_contradiction_containment",
            "truth_value_both",
            "non_explosive_reasoning",
        ],
        rejected_inference_rules=[
            "classical_explosion",
            "unrestricted_ex_falso",
        ],
        objects=[
            UniverseObject(
                name="contradictory_statement",
                kind="logical_object",
                description="A statement marked as both true and false.",
            ),
            UniverseObject(
                name="containment_region",
                kind="logical_context",
                description="A region where contradiction is tracked locally.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="containment_map",
                source="contradictory_statement",
                target="containment_region",
                mapping_rule="assign a contradiction to a local containment context",
                preserved_structure=["contradiction_marker"],
                lost_structure=["classical_global_stability"],
            ),
        ],
        metadata={
            "role": "contradiction experiment universe",
            "risk": "classical translation may be unstable",
        },
    )


def many_valued_universe() -> FormalUniverse:
    """
    Returns a toy many-valued universe.
    """

    return FormalUniverse(
        name="Many-Valued Indeterminate Universe",
        logic_family=LogicFamily.MANY_VALUED,
        truth_space=many_valued_truth_space(),
        description=(
            "A toy universe with more than two truth values. Statements may be "
            "true, false, both, or unknown. This universe is useful for partial "
            "information and indeterminate interpretation."
        ),
        accepted_inference_rules=[
            "many_valued_evaluation",
            "unknown_propagation",
            "partial_truth_tracking",
            "context_sensitive_evaluation",
        ],
        rejected_inference_rules=[
            "strict_binary_truth_only",
        ],
        objects=[
            UniverseObject(
                name="indeterminate_statement",
                kind="logical_object",
                description="A statement whose truth is incomplete or unstable.",
            ),
            UniverseObject(
                name="truth_status",
                kind="semantic_object",
                description="A non-binary truth classification.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="unknown_assignment",
                source="incomplete_statement",
                target="truth_status",
                mapping_rule="map incomplete information to unknown truth value",
                preserved_structure=["partial_information"],
                lost_structure=["binary_decision"],
            ),
        ],
        metadata={
            "role": "partial truth universe",
            "risk": "truth tables may become less decisive",
        },
    )


def modal_universe() -> FormalUniverse:
    """
    Returns a toy modal universe.
    """

    return FormalUniverse(
        name="Modal Possibility Universe",
        logic_family=LogicFamily.MODAL,
        truth_space=modal_truth_space(),
        description=(
            "A toy universe where statements can be classified by necessity, "
            "possibility, impossibility, or contingency. This universe studies "
            "truth across possible contexts."
        ),
        accepted_inference_rules=[
            "necessitation",
            "possibility_intro",
            "modal_distribution",
            "possible_world_evaluation",
        ],
        rejected_inference_rules=[
            "modal_status_erasure",
            "strict_binary_truth_only",
        ],
        objects=[
            UniverseObject(
                name="possible_world",
                kind="semantic_context",
                description="A context in which a statement may be evaluated.",
            ),
            UniverseObject(
                name="modal_statement",
                kind="logical_object",
                description="A statement carrying modal status.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="accessibility_relation",
                source="possible_world",
                target="possible_world",
                mapping_rule="relate one possible context to another",
                preserved_structure=["modal_reachability"],
                lost_structure=[],
            ),
        ],
        metadata={
            "role": "possibility and necessity universe",
            "risk": "modal information may be lost in classical transport",
        },
    )


def fuzzy_universe() -> FormalUniverse:
    """
    Returns a symbolic toy fuzzy universe.
    """

    return FormalUniverse(
        name="Symbolic Fuzzy Approximation Universe",
        logic_family=LogicFamily.FUZZY,
        truth_space=fuzzy_symbolic_truth_space(),
        description=(
            "A symbolic toy universe for approximate truth. This early version "
            "uses named values rather than continuous degrees, but it prepares "
            "the architecture for later fuzzy scoring."
        ),
        accepted_inference_rules=[
            "graded_truth_placeholder",
            "approximate_evaluation",
            "confidence_sensitive_reasoning",
        ],
        rejected_inference_rules=[
            "strict_binary_truth_only",
        ],
        objects=[
            UniverseObject(
                name="graded_statement",
                kind="logical_object",
                description="A statement intended to support approximate truth.",
            ),
            UniverseObject(
                name="confidence_marker",
                kind="semantic_object",
                description="A symbolic placeholder for degree of confidence.",
            ),
        ],
        morphisms=[
            UniverseMorphism(
                name="confidence_assignment",
                source="graded_statement",
                target="confidence_marker",
                mapping_rule="assign a symbolic confidence marker to a statement",
                preserved_structure=["approximation"],
                lost_structure=["exact_binary_truth"],
            ),
        ],
        metadata={
            "role": "approximate truth universe",
            "risk": "currently symbolic, not continuous",
        },
    )


def generated_experimental_universe() -> FormalUniverse:
    """
    Returns a placeholder generated experimental universe.
    """

    return FormalUniverse(
        name="Generated Experimental Universe",
        logic_family=LogicFamily.GENERATED,
        truth_space=many_valued_truth_space(),
        description=(
            "A placeholder universe representing future generated formal "
            "systems. It uses many-valued truth behavior until generated truth "
            "spaces are implemented."
        ),
        accepted_inference_rules=[
            "generated_rule_placeholder",
            "context_sensitive_evaluation",
        ],
        rejected_inference_rules=[
            "unverified_rule_claims",
        ],
        objects=[
            UniverseObject(
                name="generated_object",
                kind="experimental_object",
                description="A placeholder object produced by a future generator.",
            ),
        ],
        morphisms=[],
        metadata={
            "role": "future generated universe placeholder",
            "risk": "requires human review",
        },
    )


def standard_universes() -> List[FormalUniverse]:
    """
    Returns all hand-designed standard toy universes.
    """

    return [
        classical_universe(),
        intuitionistic_universe(),
        paraconsistent_universe(),
        many_valued_universe(),
        modal_universe(),
        fuzzy_universe(),
        generated_experimental_universe(),
    ]


def get_universe_names() -> List[str]:
    """
    Returns the names of all standard universes.
    """

    return [universe.name for universe in standard_universes()]


def find_universe_by_name(name: str) -> FormalUniverse:
    """
    Finds a universe by exact name.

    Raises:
        ValueError: if no universe with the given name exists.
    """

    for universe in standard_universes():
        if universe.name == name:
            return universe

    raise ValueError(f"No universe found with name: {name}")


if __name__ == "__main__":
    for universe in standard_universes():
        print(universe.describe())
        print("-" * 80)
