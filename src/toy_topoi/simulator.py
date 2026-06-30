"""
Toy topos simulator for Project ℵω.

This module coordinates statements, universes, internal-language analysis,
and toy truth evaluation.

It does not implement full topos theory. Instead, it builds an inspectable
experimental simulator inspired by the idea that a mathematical statement
can behave differently inside different formal universes.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .internal_language import InternalLanguageAnalysis, InternalLanguageAnalyzer
from .statements import Statement, StatementEvaluation
from .universe import FormalUniverse


@dataclass(frozen=True)
class SimulationResult:
    """
    Result of evaluating one statement inside one universe.
    """

    statement: Statement
    universe: FormalUniverse
    analysis: InternalLanguageAnalysis
    evaluation: StatementEvaluation

    def summary_row(self) -> Dict[str, object]:
        """
        Returns compact data for tables and reports.
        """

        return {
            "statement": self.statement.name,
            "universe": self.universe.name,
            "logic": self.universe.logic_family.value,
            "truth_value": self.evaluation.truth_value.value,
            "proof_status": self.evaluation.proof_status.value,
            "universe_fit_score": self.analysis.universe_fit_score,
            "ambiguity_score": self.analysis.ambiguity_score,
            "formalization_readiness": self.analysis.formalization_readiness,
        }

    def describe(self) -> str:
        """
        Returns a readable simulation report.
        """

        return (
            f"SimulationResult\n"
            f"Statement: {self.statement.name}\n"
            f"Universe: {self.universe.name}\n"
            f"Logic family: {self.universe.logic_family.value}\n"
            f"Truth value: {self.evaluation.truth_value.value}\n"
            f"Proof status: {self.evaluation.proof_status.value}\n"
            f"Universe fit score: {self.analysis.universe_fit_score}\n"
            f"Ambiguity score: {self.analysis.ambiguity_score}\n"
            f"Formalization readiness: {self.analysis.formalization_readiness}\n"
            f"Explanation: {self.evaluation.explanation}"
        )


@dataclass(frozen=True)
class StatementProfile:
    """
    Cross-universe profile for one statement.

    This shows how one statement behaves across many universes.
    """

    statement: Statement
    results: List[SimulationResult]

    def best_fit(self) -> Optional[SimulationResult]:
        """
        Returns the universe where the statement has the highest fit score.
        """

        if not self.results:
            return None

        return max(self.results, key=lambda result: result.analysis.universe_fit_score)

    def worst_fit(self) -> Optional[SimulationResult]:
        """
        Returns the universe where the statement has the lowest fit score.
        """

        if not self.results:
            return None

        return min(self.results, key=lambda result: result.analysis.universe_fit_score)

    def truth_values_seen(self) -> List[str]:
        """
        Returns truth values assigned across universes.
        """

        return sorted({result.evaluation.truth_value.value for result in self.results})

    def proof_statuses_seen(self) -> List[str]:
        """
        Returns proof statuses assigned across universes.
        """

        return sorted({result.evaluation.proof_status.value for result in self.results})

    def average_fit_score(self) -> float:
        """
        Computes average universe-fit score.
        """

        if not self.results:
            return 0.0

        total = sum(result.analysis.universe_fit_score for result in self.results)
        return round(total / len(self.results), 2)

    def describe(self) -> str:
        """
        Returns a readable cross-universe profile.
        """

        best = self.best_fit()
        worst = self.worst_fit()

        return (
            f"StatementProfile\n"
            f"Statement: {self.statement.name}\n"
            f"Universes evaluated: {len(self.results)}\n"
            f"Average fit score: {self.average_fit_score()}\n"
            f"Truth values seen: {', '.join(self.truth_values_seen()) or 'none'}\n"
            f"Proof statuses seen: {', '.join(self.proof_statuses_seen()) or 'none'}\n"
            f"Best fit: {best.universe.name if best else 'none'}\n"
            f"Worst fit: {worst.universe.name if worst else 'none'}"
        )


class ToyToposSimulator:
    """
    Coordinates statement evaluation across toy formal universes.

    The simulator uses the InternalLanguageAnalyzer to evaluate how well a
    statement fits inside a universe and to produce a toy truth/proof status.
    """

    def __init__(self, universes: List[FormalUniverse], statements: List[Statement]):
        self.universes = universes
        self.statements = statements
        self.analyzer = InternalLanguageAnalyzer()

    def evaluate_statement_in_universe(
        self,
        statement: Statement,
        universe: FormalUniverse,
    ) -> SimulationResult:
        """
        Evaluates one statement inside one universe.
        """

        analysis = self.analyzer.analyze(statement, universe)
        evaluation = analysis.to_evaluation()

        return SimulationResult(
            statement=statement,
            universe=universe,
            analysis=analysis,
            evaluation=evaluation,
        )

    def evaluate_statement_across_universes(self, statement: Statement) -> StatementProfile:
        """
        Evaluates one statement across all simulator universes.
        """

        results = [
            self.evaluate_statement_in_universe(statement, universe)
            for universe in self.universes
        ]

        return StatementProfile(statement=statement, results=results)

    def evaluate_all(self) -> List[SimulationResult]:
        """
        Evaluates all statements across all universes.
        """

        results: List[SimulationResult] = []

        for statement in self.statements:
            for universe in self.universes:
                results.append(self.evaluate_statement_in_universe(statement, universe))

        return results

    def statement_profiles(self) -> List[StatementProfile]:
        """
        Returns cross-universe profiles for every statement.
        """

        return [
            self.evaluate_statement_across_universes(statement)
            for statement in self.statements
        ]

    def ranked_results_by_fit(self) -> List[SimulationResult]:
        """
        Returns all simulation results ranked by universe-fit score.
        """

        return sorted(
            self.evaluate_all(),
            key=lambda result: result.analysis.universe_fit_score,
            reverse=True,
        )

    def ranked_results_by_ambiguity(self) -> List[SimulationResult]:
        """
        Returns all simulation results ranked by ambiguity score, highest first.
        """

        return sorted(
            self.evaluate_all(),
            key=lambda result: result.analysis.ambiguity_score,
            reverse=True,
        )

    def summary_table(self) -> List[Dict[str, object]]:
        """
        Returns compact rows for every simulation result.
        """

        return [result.summary_row() for result in self.evaluate_all()]


if __name__ == "__main__":
    from .library import standard_universes
    from .statements import starter_statements

    simulator = ToyToposSimulator(
        universes=standard_universes(),
        statements=starter_statements(),
    )

    print("Toy Topos Simulator Summary")
    print("=" * 80)

    for profile in simulator.statement_profiles():
        print(profile.describe())
        print("-" * 80)

    print("Top results by universe fit")
    print("=" * 80)

    for result in simulator.ranked_results_by_fit()[:10]:
        print(result.describe())
        print("-" * 80)
