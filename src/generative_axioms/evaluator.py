"""
Axiom evaluator for Project ℵω.

This module scores experimental axioms using transparent heuristic metrics.

Important:
These scores are not mathematical proofs.
They are computational tools for ranking, filtering, comparing, and studying
toy axioms inside the Generative Axiom Engine.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set

from .axiom import Axiom, AxiomDomain


@dataclass(frozen=True)
class AxiomScore:
    """
    Stores heuristic scores for an axiom.

    All scores are on an approximate 0 to 10 scale.

    These values are not claims of mathematical truth. They are research
    instrumentation: a way to compare candidate assumptions inside a toy
    computational framework.
    """

    complexity: float
    novelty: float
    contradiction_risk: float
    expressivity: float
    stability: float
    overall_interest: float

    def as_dict(self) -> Dict[str, float]:
        """
        Converts the score object into a dictionary.
        """

        return {
            "complexity": self.complexity,
            "novelty": self.novelty,
            "contradiction_risk": self.contradiction_risk,
            "expressivity": self.expressivity,
            "stability": self.stability,
            "overall_interest": self.overall_interest,
        }


class AxiomEvaluator:
    """
    Evaluates experimental axioms using heuristic structural metrics.

    The evaluator is intentionally simple and inspectable. It does not try to
    prove consistency, independence, completeness, or mathematical truth.
    Instead, it gives the project a disciplined way to rank and compare
    candidate assumptions.
    """

    def __init__(self, reference_axioms: Optional[Iterable[Axiom]] = None):
        self.reference_axioms = list(reference_axioms or [])

    def evaluate(self, axiom: Axiom) -> AxiomScore:
        """
        Returns all heuristic scores for one axiom.
        """

        complexity = self.complexity_score(axiom)
        novelty = self.novelty_score(axiom)
        contradiction_risk = self.contradiction_risk_score(axiom)
        expressivity = self.expressivity_score(axiom)
        stability = self.stability_score(axiom, contradiction_risk)

        overall_interest = self.overall_interest_score(
            complexity=complexity,
            novelty=novelty,
            contradiction_risk=contradiction_risk,
            expressivity=expressivity,
            stability=stability,
        )

        return AxiomScore(
            complexity=complexity,
            novelty=novelty,
            contradiction_risk=contradiction_risk,
            expressivity=expressivity,
            stability=stability,
            overall_interest=overall_interest,
        )

    def complexity_score(self, axiom: Axiom) -> float:
        """
        Estimates structural complexity.

        Inputs:
        - number of unique symbols
        - number of conceptual domains
        - number of dependencies
        - length of symbolic sketch
        - number of compatible and incompatible universes
        """

        symbol_component = min(axiom.symbol_count() * 0.9, 4.0)
        domain_component = min(len(axiom.domains) * 0.8, 2.4)
        dependency_component = min(axiom.dependency_count() * 0.7, 2.1)
        universe_component = min(
            (len(axiom.compatible_universes) + len(axiom.incompatible_universes)) * 0.25,
            1.5,
        )
        sketch_component = min(len(axiom.symbolic_sketch.split()) * 0.15, 2.0)

        return self._clamp(
            symbol_component
            + domain_component
            + dependency_component
            + universe_component
            + sketch_component
        )

    def novelty_score(self, axiom: Axiom) -> float:
        """
        Estimates novelty compared with the reference axiom library.

        The score is based on how different the axiom's symbols and domains
        are from the existing reference set.
        """

        if not self.reference_axioms:
            return 6.0

        current_symbols = set(axiom.symbols_used)
        current_domains = set(axiom.domains)

        similarities: List[float] = []

        for reference in self.reference_axioms:
            if reference.name == axiom.name:
                continue

            reference_symbols = set(reference.symbols_used)
            reference_domains = set(reference.domains)

            symbol_similarity = self._jaccard_similarity(
                current_symbols,
                reference_symbols,
            )
            domain_similarity = self._jaccard_similarity(
                current_domains,
                reference_domains,
            )

            combined_similarity = 0.7 * symbol_similarity + 0.3 * domain_similarity
            similarities.append(combined_similarity)

        if not similarities:
            return 6.0

        max_similarity = max(similarities)
        novelty = 10.0 * (1.0 - max_similarity)

        return self._clamp(novelty)

    def contradiction_risk_score(self, axiom: Axiom) -> float:
        """
        Estimates contradiction risk.

        This is not a consistency proof. It is a warning signal based on words,
        domains, universe incompatibility, and dependency structure.
        """

        risk = 0.0

        contradiction_terms = {
            "contradiction",
            "not",
            "negation",
            "both",
            "false",
            "inconsistent",
            "collapse",
            "explosion",
        }

        symbols = {symbol.lower() for symbol in axiom.symbols_used}
        sketch_words = {word.strip("(),.{}").lower() for word in axiom.symbolic_sketch.split()}

        risk += len(symbols.intersection(contradiction_terms)) * 1.2
        risk += len(sketch_words.intersection(contradiction_terms)) * 0.8

        if AxiomDomain.CONTRADICTION in axiom.domains:
            risk += 2.0

        if "strict_classical" in axiom.incompatible_universes:
            risk += 1.5

        if "strict_classical_without_modal_operators" in axiom.incompatible_universes:
            risk += 0.8

        if axiom.dependency_count() > 3:
            risk += 0.7

        return self._clamp(risk)

    def expressivity_score(self, axiom: Axiom) -> float:
        """
        Estimates how much expressive power an axiom contributes.

        Axiom expressivity increases when the axiom introduces more domains,
        symbols, universe compatibility, and structural concepts.
        """

        domain_component = min(len(set(axiom.domains)) * 1.1, 3.3)
        symbol_component = min(axiom.symbol_count() * 0.7, 3.5)
        universe_component = min(axiom.universe_span() * 0.45, 2.7)
        dependency_component = min(axiom.dependency_count() * 0.4, 1.2)

        return self._clamp(
            domain_component
            + symbol_component
            + universe_component
            + dependency_component
        )

    def stability_score(self, axiom: Axiom, contradiction_risk: Optional[float] = None) -> float:
        """
        Estimates whether the axiom is stable enough to use in experiments.

        Higher contradiction risk lowers stability.
        Compatibility with multiple universes can increase stability.
        Excessive incompatibility can reduce stability.
        """

        if contradiction_risk is None:
            contradiction_risk = self.contradiction_risk_score(axiom)

        base = 8.0
        base -= contradiction_risk * 0.55
        base += min(axiom.universe_span() * 0.25, 1.0)
        base -= min(len(axiom.incompatible_universes) * 0.5, 2.0)

        return self._clamp(base)

    def overall_interest_score(
        self,
        complexity: float,
        novelty: float,
        contradiction_risk: float,
        expressivity: float,
        stability: float,
    ) -> float:
        """
        Combines scores into an overall research-interest metric.

        The engine rewards expressivity, novelty, and moderate complexity.
        It penalizes excessive contradiction risk but does not eliminate all
        contradiction because some universes are designed to study it.
        """

        ideal_complexity = 6.5
        complexity_balance = 10.0 - abs(complexity - ideal_complexity)

        score = (
            0.25 * complexity_balance
            + 0.25 * novelty
            + 0.25 * expressivity
            + 0.20 * stability
            - 0.15 * contradiction_risk
        )

        return self._clamp(score)

    def rank_axioms(self, axioms: Iterable[Axiom]) -> List[tuple[Axiom, AxiomScore]]:
        """
        Returns axioms ranked by overall interest score.
        """

        scored = [(axiom, self.evaluate(axiom)) for axiom in axioms]
        return sorted(scored, key=lambda item: item[1].overall_interest, reverse=True)

    @staticmethod
    def _jaccard_similarity(left: Set[object], right: Set[object]) -> float:
        """
        Computes Jaccard similarity between two sets.
        """

        if not left and not right:
            return 1.0

        union = left.union(right)

        if not union:
            return 0.0

        return len(left.intersection(right)) / len(union)

    @staticmethod
    def _clamp(value: float, lower: float = 0.0, upper: float = 10.0) -> float:
        """
        Keeps scores in a stable range.
        """

        return max(lower, min(upper, round(value, 2)))
