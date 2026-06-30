"""
Template-based axiom generator for Project ℵω.

This module creates experimental axiom candidates from controlled templates
and simple mutation rules.

Important:
Generated axioms are not automatically true mathematics.
They are candidate assumptions for exploration, scoring, filtering, and
human review.
"""

from dataclasses import replace
from itertools import product
from typing import Iterable, List, Optional

from .axiom import Axiom, AxiomDomain, AxiomStatus


class AxiomGenerator:
    """
    Generates toy axiom candidates using templates and mutations.

    The generator is intentionally conservative. It does not create random
    meaningless text. Instead, it uses controlled mathematical templates so
    the generated axioms remain readable and inspectable.
    """

    def generate_contextual_axioms(self) -> List[Axiom]:
        """
        Generates axioms involving context-dependent evaluation.

        These axioms are useful for studying how truth, identity, and proof
        status may depend on a surrounding formal universe or interpretation
        context.
        """

        objects = ["statement", "object", "proof_goal"]
        properties = ["truth", "identity", "validity"]
        contexts = ["formal_universe", "interpretation_context", "bridge_context"]

        generated: List[Axiom] = []

        for obj, prop, context in product(objects, properties, contexts):
            name = f"Contextual {prop.title()} of {obj.title()}"

            generated.append(
                Axiom(
                    name=name,
                    informal_statement=(
                        f"The {prop} of a {obj} is evaluated relative to a "
                        f"chosen {context}."
                    ),
                    symbolic_sketch=f"{prop}({obj}, {context}) depends_on {context}",
                    domains=[
                        AxiomDomain.CONTEXT,
                        AxiomDomain.TRUTH if prop != "identity" else AxiomDomain.IDENTITY,
                    ],
                    symbols_used=[
                        prop,
                        obj,
                        context,
                        "depends_on",
                    ],
                    compatible_universes=[
                        "classical",
                        "intuitionistic",
                        "many_valued",
                        "modal",
                    ],
                    incompatible_universes=[],
                    dependencies=[
                        "interpretation_context",
                        "formal_universe",
                    ],
                    notes=(
                        "Generated from a controlled context-dependence template. "
                        "Requires human review before use in serious experiments."
                    ),
                    status=AxiomStatus.GENERATED,
                )
            )

        return generated

    def generate_transport_axioms(self) -> List[Axiom]:
        """
        Generates axioms involving transport between universes.

        These axioms are useful for bridge experiments.
        """

        transported_items = ["statement", "truth_value", "proof_status", "symbol"]
        effects = ["preserved", "distorted", "weakened", "made_ambiguous", "lost"]
        bridge_types = [
            "classical_to_intuitionistic",
            "paraconsistent_to_classical",
            "modal_to_classical",
            "fuzzy_to_classical",
        ]

        generated: List[Axiom] = []

        for item, effect, bridge in product(transported_items, effects, bridge_types):
            readable_effect = effect.replace("_", " ")

            generated.append(
                Axiom(
                    name=f"Transport {item.title()} {readable_effect.title()}",
                    informal_statement=(
                        f"When a {item} is transported across a {bridge} bridge, "
                        f"it may be {readable_effect}."
                    ),
                    symbolic_sketch=f"transport({item}, {bridge}) -> {effect}({item})",
                    domains=[
                        AxiomDomain.TRANSPORT,
                        AxiomDomain.CONTEXT,
                    ],
                    symbols_used=[
                        "transport",
                        item,
                        bridge,
                        effect,
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
                    dependencies=[
                        "bridge",
                        "source_universe",
                        "target_universe",
                    ],
                    notes=(
                        "Generated from a controlled bridge-transport template. "
                        "Useful for testing preservation and distortion scoring."
                    ),
                    status=AxiomStatus.GENERATED,
                )
            )

        return generated

    def generate_contradiction_axioms(self) -> List[Axiom]:
        """
        Generates axioms involving contradiction behavior.

        These are especially relevant for paraconsistent and many-valued
        universes.
        """

        contradiction_modes = [
            "contained_locally",
            "propagated_globally",
            "converted_to_unknown",
            "marked_unstable",
        ]

        generated: List[Axiom] = []

        for mode in contradiction_modes:
            readable_mode = mode.replace("_", " ")

            generated.append(
                Axiom(
                    name=f"Contradiction {readable_mode.title()}",
                    informal_statement=(
                        f"A contradiction between a statement and its negation "
                        f"may be {readable_mode} depending on the universe."
                    ),
                    symbolic_sketch=f"contradiction(P, not_P, U) -> {mode}(P, U)",
                    domains=[
                        AxiomDomain.CONTRADICTION,
                        AxiomDomain.TRUTH,
                        AxiomDomain.INFERENCE,
                    ],
                    symbols_used=[
                        "contradiction",
                        "statement",
                        "negation",
                        "universe",
                        mode,
                    ],
                    compatible_universes=[
                        "paraconsistent",
                        "many_valued",
                    ],
                    incompatible_universes=[
                        "strict_classical",
                    ],
                    dependencies=[
                        "truth_value_space",
                        "contradiction_policy",
                    ],
                    notes=(
                        "Generated from a contradiction-behavior template. "
                        "High-risk candidates require careful interpretation."
                    ),
                    status=AxiomStatus.GENERATED,
                )
            )

        return generated

    def mutate_axiom(self, axiom: Axiom) -> List[Axiom]:
        """
        Produces simple mutations of one axiom.

        Mutations are nearby candidate assumptions. They should not be treated
        as validated mathematics.
        """

        mutations: List[Axiom] = []

        mutations.append(
            replace(
                axiom,
                name=f"Weakened {axiom.name}",
                informal_statement=(
                    axiom.informal_statement
                    + " This version weakens the claim by treating it as conditional."
                ),
                symbolic_sketch=f"if condition(C) then {axiom.symbolic_sketch}",
                symbols_used=axiom.symbols_used + ["condition"],
                notes=(
                    axiom.notes
                    + " Mutation: weakened by adding an explicit condition."
                ),
                status=AxiomStatus.MUTATED,
            )
        )

        mutations.append(
            replace(
                axiom,
                name=f"Contextualized {axiom.name}",
                informal_statement=(
                    axiom.informal_statement
                    + " This version explicitly depends on a formal universe."
                ),
                symbolic_sketch=f"{axiom.symbolic_sketch} relative_to universe(U)",
                domains=list(set(axiom.domains + [AxiomDomain.CONTEXT])),
                symbols_used=axiom.symbols_used + ["universe", "relative_to"],
                dependencies=axiom.dependencies + ["formal_universe"],
                notes=(
                    axiom.notes
                    + " Mutation: contextualized by adding a universe parameter."
                ),
                status=AxiomStatus.MUTATED,
            )
        )

        return mutations

    def generate_all(self, seed_axioms: Optional[Iterable[Axiom]] = None) -> List[Axiom]:
        """
        Generates all starter candidate axioms.

        If seed axioms are provided, the generator also creates mutations of
        those seed axioms.
        """

        generated: List[Axiom] = []
        generated.extend(self.generate_contextual_axioms())
        generated.extend(self.generate_transport_axioms())
        generated.extend(self.generate_contradiction_axioms())

        if seed_axioms:
            for axiom in seed_axioms:
                generated.extend(self.mutate_axiom(axiom))

        return generated


if __name__ == "__main__":
    from .library import foundational_axioms

    generator = AxiomGenerator()
    generated_axioms = generator.generate_all(seed_axioms=foundational_axioms())

    print(f"Generated {len(generated_axioms)} candidate axioms.")
    print()

    for axiom in generated_axioms[:10]:
        print(axiom.describe())
        print("-" * 80)
