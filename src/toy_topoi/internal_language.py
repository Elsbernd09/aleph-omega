"""
Internal language layer for Project ℵω toy topoi.

This module analyzes how a statement fits inside a toy formal universe.

It does not perform full theorem proving. Instead, it provides a structured
compatibility analysis: whether the statement's symbols, kind, proof status,
and truth requirements appear meaningful inside a chosen universe.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from .statements import ProofStatus, Statement, StatementEvaluation, StatementKind
from .truth_values import LogicFamily, TruthValue
from .universe import FormalUniverse


@dataclass(frozen=True)
class InternalLanguageAnalysis:
    """
    Stores the analysis of a statement inside a universe.
    """

    statement_name: str
    universe_name: str
    supported_symbols: List[str]
    unsupported_symbols: List[str]
    required_features: List[str]
    available_features: List[str]
    missing_features: List[str]
    universe_fit_score: float
    ambiguity_score: float
    formalization_readiness: float
    recommended_truth_value: TruthValue
    recommended_proof_status: ProofStatus
    explanation: str

    def as_dict(self) -> Dict[str, object]:
        """
        Converts the analysis into a dictionary.
        """

        return {
            "statement_name": self.statement_name,
            "universe_name": self.universe_name,
            "supported_symbols": self.supported_symbols,
            "unsupported_symbols": self.unsupported_symbols,
            "required_features": self.required_features,
            "available_features": self.available_features,
            "missing_features": self.missing_features,
            "universe_fit_score": self.universe_fit_score,
            "ambiguity_score": self.ambiguity_score,
            "formalization_readiness": self.formalization_readiness,
            "recommended_truth_value": self.recommended_truth_value.value,
            "recommended_proof_status": self.recommended_proof_status.value,
            "explanation": self.explanation,
        }

    def to_evaluation(self) -> StatementEvaluation:
        """
        Converts this analysis into a statement evaluation object.
        """

        return StatementEvaluation(
            statement_name=self.statement_name,
            universe_name=self.universe_name,
            truth_value=self.recommended_truth_value,
            proof_status=self.recommended_proof_status,
            explanation=self.explanation,
            required_human_review=True,
            metadata={
                "universe_fit_score": str(self.universe_fit_score),
                "ambiguity_score": str(self.ambiguity_score),
                "formalization_readiness": str(self.formalization_readiness),
            },
        )


class InternalLanguageAnalyzer:
    """
    Analyzes statements inside toy formal universes.

    The analyzer is intentionally heuristic. It is designed to expose the
    relationship between statements and universes, not to prove theorems.
    """

    def analyze(self, statement: Statement, universe: FormalUniverse) -> InternalLanguageAnalysis:
        """
        Analyzes one statement inside one universe.
        """

        required_features = self._required_features(statement)
        available_features = self._available_features(universe)

        missing_features = sorted(set(required_features).difference(available_features))

        supported_symbols, unsupported_symbols = self._symbol_support(statement, universe)

        universe_fit_score = self._universe_fit_score(
            statement=statement,
            universe=universe,
            unsupported_symbols=unsupported_symbols,
            missing_features=missing_features,
        )

        ambiguity_score = self._ambiguity_score(statement, unsupported_symbols, missing_features)
        formalization_readiness = self._formalization_readiness(
            statement=statement,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
        )

        truth_value = self._recommend_truth_value(statement, universe, missing_features)
        proof_status = self._recommend_proof_status(statement, universe, missing_features)

        explanation = self._explanation(
            statement=statement,
            universe=universe,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
            missing_features=missing_features,
            unsupported_symbols=unsupported_symbols,
            truth_value=truth_value,
            proof_status=proof_status,
        )

        return InternalLanguageAnalysis(
            statement_name=statement.name,
            universe_name=universe.name,
            supported_symbols=supported_symbols,
            unsupported_symbols=unsupported_symbols,
            required_features=required_features,
            available_features=available_features,
            missing_features=missing_features,
            universe_fit_score=universe_fit_score,
            ambiguity_score=ambiguity_score,
            formalization_readiness=formalization_readiness,
            recommended_truth_value=truth_value,
            recommended_proof_status=proof_status,
            explanation=explanation,
        )

    def evaluate(self, statement: Statement, universe: FormalUniverse) -> StatementEvaluation:
        """
        Produces a StatementEvaluation for a statement inside a universe.
        """

        return self.analyze(statement, universe).to_evaluation()

    @staticmethod
    def _required_features(statement: Statement) -> List[str]:
        """
        Infers broad features required by a statement.
        """

        features: Set[str] = set()

        symbols = {symbol.lower() for symbol in statement.required_symbols}
        symbolic_form = statement.symbolic_form.lower()
        raw_text = statement.raw_text.lower()

        if "not" in symbols or "not(" in symbolic_form:
            features.add("negation")

        if "and" in symbols or " and " in symbolic_form:
            features.add("conjunction")

        if "or" in symbols or " or " in symbolic_form:
            features.add("disjunction")

        if "implies" in symbols or "imply" in raw_text or "->" in symbolic_form:
            features.add("implication")

        if "both" in symbols or statement.kind == StatementKind.CONTRADICTION:
            features.add("contradiction_support")

        if "unknown" in symbols:
            features.add("unknown_support")

        if "possible" in symbols or "necessary" in symbols or statement.kind == StatementKind.MODAL_CLAIM:
            features.add("modal_support")

        if "witness" in symbols or "construct" in raw_text:
            features.add("constructive_evidence")

        if "context" in symbols or "identity" in symbols:
            features.add("context_sensitivity")

        if "exists" in symbols:
            features.add("existential_reasoning")

        return sorted(features)

    @staticmethod
    def _available_features(universe: FormalUniverse) -> List[str]:
        """
        Infers broad features available in a universe.
        """

        features: Set[str] = {
            "negation",
            "conjunction",
            "disjunction",
            "implication",
        }

        rules = {rule.lower() for rule in universe.accepted_inference_rules}
        logic = universe.logic_family

        if universe.supports_contradiction():
            features.add("contradiction_support")

        if universe.supports_unknown():
            features.add("unknown_support")

        if universe.supports_modal_status():
            features.add("modal_support")

        if logic == LogicFamily.INTUITIONISTIC or "witness_requirement" in rules:
            features.add("constructive_evidence")

        if "context_sensitive_evaluation" in rules:
            features.add("context_sensitivity")

        if logic in {LogicFamily.CLASSICAL, LogicFamily.INTUITIONISTIC}:
            features.add("existential_reasoning")

        if logic == LogicFamily.MANY_VALUED:
            features.add("context_sensitivity")

        return sorted(features)

    @staticmethod
    def _symbol_support(statement: Statement, universe: FormalUniverse) -> tuple[List[str], List[str]]:
        """
        Estimates whether statement symbols are supported by a universe.
        """

        broadly_supported = {
            "forall",
            "exists",
            "and",
            "or",
            "not",
            "implies",
            "truth",
            "property",
            "statement",
            "identity",
            "context",
            "requires",
            "arbitrary",
        }

        if universe.supports_contradiction():
            broadly_supported.update({"both", "contradiction"})

        if universe.supports_unknown():
            broadly_supported.update({"unknown", "neither"})

        if universe.supports_modal_status():
            broadly_supported.update({"possible", "necessary", "impossible", "contingent"})

        if universe.logic_family == LogicFamily.INTUITIONISTIC:
            broadly_supported.update({"witness", "construction"})

        supported = []
        unsupported = []

        for symbol in statement.required_symbols:
            if symbol.lower() in broadly_supported:
                supported.append(symbol)
            else:
                unsupported.append(symbol)

        return sorted(supported), sorted(unsupported)

    @staticmethod
    def _universe_fit_score(
        statement: Statement,
        universe: FormalUniverse,
        unsupported_symbols: List[str],
        missing_features: List[str],
    ) -> float:
        """
        Computes a heuristic universe-fit score.
        """

        score = 8.0
        score -= len(unsupported_symbols) * 0.9
        score -= len(missing_features) * 1.2

        if statement.origin_universe == universe.name:
            score += 1.0

        if statement.kind == StatementKind.CONTRADICTION and universe.supports_contradiction():
            score += 1.0

        if statement.kind == StatementKind.MODAL_CLAIM and universe.supports_modal_status():
            score += 1.0

        if statement.kind == StatementKind.FUZZY_CLAIM and universe.logic_family == LogicFamily.FUZZY:
            score += 1.0

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _ambiguity_score(
        statement: Statement,
        unsupported_symbols: List[str],
        missing_features: List[str],
    ) -> float:
        """
        Computes a heuristic ambiguity score.
        """

        score = 0.0
        score += len(unsupported_symbols) * 1.1
        score += len(missing_features) * 1.2

        if not statement.symbolic_form:
            score += 2.0

        if statement.variable_count() == 0 and statement.kind not in {
            StatementKind.DEFINITION,
            StatementKind.AXIOMATIC_ASSUMPTION,
        }:
            score += 0.5

        if "may" in statement.raw_text.lower():
            score += 0.7

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _formalization_readiness(
        statement: Statement,
        universe_fit_score: float,
        ambiguity_score: float,
    ) -> float:
        """
        Estimates how ready the statement is for Lean-style formalization.
        """

        score = 5.0
        score += universe_fit_score * 0.35
        score -= ambiguity_score * 0.45
        score += min(statement.symbol_count() * 0.2, 1.0)
        score += min(statement.variable_count() * 0.2, 1.0)

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _recommend_truth_value(
        statement: Statement,
        universe: FormalUniverse,
        missing_features: List[str],
    ) -> TruthValue:
        """
        Recommends a toy truth value for a statement inside a universe.
        """

        if missing_features:
            if universe.accepts_truth_value(TruthValue.UNKNOWN):
                return TruthValue.UNKNOWN
            return TruthValue.FALSE

        if statement.kind == StatementKind.CONTRADICTION:
            if universe.accepts_truth_value(TruthValue.BOTH):
                return TruthValue.BOTH
            return TruthValue.FALSE

        if statement.kind == StatementKind.MODAL_CLAIM:
            if universe.accepts_truth_value(TruthValue.POSSIBLE):
                return TruthValue.POSSIBLE
            if universe.accepts_truth_value(TruthValue.UNKNOWN):
                return TruthValue.UNKNOWN

        return TruthValue.TRUE if universe.accepts_truth_value(TruthValue.TRUE) else universe.truth_space.values[0]

    @staticmethod
    def _recommend_proof_status(
        statement: Statement,
        universe: FormalUniverse,
        missing_features: List[str],
    ) -> ProofStatus:
        """
        Recommends a proof status.
        """

        if missing_features:
            return ProofStatus.HUMAN_REVIEW_REQUIRED

        if statement.kind == StatementKind.AXIOMATIC_ASSUMPTION:
            return ProofStatus.ASSUMED

        if statement.kind == StatementKind.CONTRADICTION:
            if universe.supports_contradiction():
                return ProofStatus.CONTRADICTORY
            return ProofStatus.REFUTED

        if universe.logic_family == LogicFamily.INTUITIONISTIC:
            return ProofStatus.UNKNOWN

        return ProofStatus.UNTESTED

    @staticmethod
    def _explanation(
        statement: Statement,
        universe: FormalUniverse,
        universe_fit_score: float,
        ambiguity_score: float,
        missing_features: List[str],
        unsupported_symbols: List[str],
        truth_value: TruthValue,
        proof_status: ProofStatus,
    ) -> str:
        """
        Builds a human-readable explanation.
        """

        parts = [
            f"The statement '{statement.name}' was analyzed inside '{universe.name}'.",
            f"Universe fit score: {universe_fit_score}.",
            f"Ambiguity score: {ambiguity_score}.",
            f"Recommended truth value: {truth_value.value}.",
            f"Recommended proof status: {proof_status.value}.",
        ]

        if missing_features:
            parts.append("Missing features: " + ", ".join(missing_features) + ".")

        if unsupported_symbols:
            parts.append("Unsupported symbols: " + ", ".join(unsupported_symbols) + ".")

        if not missing_features and not unsupported_symbols:
            parts.append("The statement appears structurally interpretable in this toy universe.")

        parts.append("This is a heuristic internal-language analysis, not a proof.")

        return " ".join(parts)


if __name__ == "__main__":
    from .library import standard_universes
    from .statements import starter_statements

    analyzer = InternalLanguageAnalyzer()

    statement = starter_statements()[0]

    for universe in standard_universes():
        analysis = analyzer.analyze(statement, universe)
        print(analysis.as_dict())
        print("-" * 80)
