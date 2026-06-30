"""
Core axiom data model for Project ℵω.

This module defines the Axiom object used by the Generative Axiom Engine.
The goal is not to represent all of mathematical logic. The goal is to create
a structured computational object that can be generated, scored, compared,
filtered, and transported across toy formal universes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class AxiomStatus(str, Enum):
    """
    Development status of an axiom candidate.
    """

    HAND_DESIGNED = "hand_designed"
    GENERATED = "generated"
    MUTATED = "mutated"
    RECOMBINED = "recombined"
    HUMAN_REVIEW_REQUIRED = "human_review_required"


class AxiomDomain(str, Enum):
    """
    Conceptual domain of an axiom.
    """

    IDENTITY = "identity"
    TRUTH = "truth"
    CONTEXT = "context"
    INFERENCE = "inference"
    TRANSPORT = "transport"
    CONTRADICTION = "contradiction"
    MODALITY = "modality"
    PRIME_GEOMETRY = "prime_geometry"
    COGNITIVE_MORPHISM = "cognitive_morphism"
    GENERAL_FOUNDATIONS = "general_foundations"


@dataclass(frozen=True)
class Axiom:
    """
    Represents a toy axiom inside an experimental formal system.

    An Axiom in Project ℵω is not automatically treated as true mathematics.
    It is an experimental formal assumption with metadata.

    Fields:
        name:
            Human-readable name of the axiom.

        informal_statement:
            Natural-language description of the assumption.

        symbolic_sketch:
            Semi-formal symbolic representation. This is not necessarily
            valid Lean or full first-order logic yet.

        domains:
            Conceptual domains the axiom belongs to.

        symbols_used:
            Symbols, predicates, or conceptual terms appearing in the axiom.

        compatible_universes:
            Toy universes where the axiom is expected to be meaningful.

        incompatible_universes:
            Toy universes where the axiom may fail or require reinterpretation.

        dependencies:
            Names of other axioms or concepts this axiom depends on.

        notes:
            Human-readable explanation of why the axiom matters.

        status:
            Whether the axiom was hand-designed, generated, mutated, etc.
    """

    name: str
    informal_statement: str
    symbolic_sketch: str
    domains: List[AxiomDomain]
    symbols_used: List[str]
    compatible_universes: List[str] = field(default_factory=list)
    incompatible_universes: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    notes: str = ""
    status: AxiomStatus = AxiomStatus.HAND_DESIGNED
    metadata: Optional[Dict[str, str]] = None

    def short_label(self) -> str:
        """
        Returns a compact label for tables and reports.
        """

        return f"{self.name} [{self.status.value}]"

    def domain_names(self) -> List[str]:
        """
        Returns domain names as strings.
        """

        return [domain.value for domain in self.domains]

    def symbol_count(self) -> int:
        """
        Counts unique symbols used by the axiom.
        """

        return len(set(self.symbols_used))

    def dependency_count(self) -> int:
        """
        Counts dependency links.
        """

        return len(set(self.dependencies))

    def universe_span(self) -> int:
        """
        Counts how many universes the axiom is marked as compatible with.
        """

        return len(set(self.compatible_universes))

    def describe(self) -> str:
        """
        Returns a readable multi-line description.
        """

        return (
            f"Name: {self.name}\n"
            f"Status: {self.status.value}\n"
            f"Domains: {', '.join(self.domain_names())}\n"
            f"Informal statement: {self.informal_statement}\n"
            f"Symbolic sketch: {self.symbolic_sketch}\n"
            f"Symbols used: {', '.join(self.symbols_used)}\n"
            f"Compatible universes: {', '.join(self.compatible_universes) or 'not specified'}\n"
            f"Incompatible universes: {', '.join(self.incompatible_universes) or 'not specified'}\n"
            f"Dependencies: {', '.join(self.dependencies) or 'none'}\n"
            f"Notes: {self.notes or 'none'}"
        )
