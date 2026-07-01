"""
Satisfaction Preservation Theorem stress search.

This module generates small finite universes, bridge cases, and truth-value
interpretations, then checks satisfaction preservation across those cases.
"""

from dataclasses import dataclass
from itertools import product
from typing import Tuple

from src.rigor.bridge_case_generator import BridgeCase, BridgeCaseGenerator, BridgeCaseKind
from src.rigor.finite_universe import FiniteLogicalUniverse, SemanticFeature
from src.rigor.interpretation import UniverseInterpretation, explicit_interpretation
from src.rigor.model_search import FiniteModelGenerator
from src.rigor.preservation import BridgePreservationReport, SatisfactionPreservationAnalyzer
from src.rigor.semantics import FiniteTruthValue, classical_truth_space


@dataclass(frozen=True)
class InterpretationCase:
    """
    A generated interpretation case for a finite universe.
    """

    universe: FiniteLogicalUniverse
    interpretation: UniverseInterpretation
    true_count: int
    false_count: int

    def describe(self) -> str:
        """
        Returns a readable interpretation case description.
        """

        return (
            f"InterpretationCase\n"
            f"Universe: {self.universe.name}\n"
            f"True assignments: {self.true_count}\n"
            f"False assignments: {self.false_count}"
        )


@dataclass(frozen=True)
class SatisfactionSearchCase:
    """
    One generated satisfaction preservation search case.
    """

    bridge_case: BridgeCase
    source_case: InterpretationCase
    target_case: InterpretationCase
    source_interpretation: UniverseInterpretation
    target_interpretation: UniverseInterpretation
    preservation_report: BridgePreservationReport

    def has_distortion(self) -> bool:
        """
        Returns whether satisfaction distortion appears under the generated search.

        In this finite stress-search layer, distortion means:

        - the source interpretation has at least one TRUE statement, and
        - the bridge is not total, or
        - the generated preservation report does not preserve all satisfied sources.
        """

        if self.source_case.true_count == 0:
            return False

        if not self.bridge_case.bridge.is_total():
            return True

        return not self.preservation_report.all_satisfied_sources_preserved()

    def preserves_satisfaction(self) -> bool:
        """
        Returns whether this generated case preserves satisfaction.
        """

        return not self.has_distortion()

    def describe(self) -> str:
        """
        Returns a readable search case description.
        """

        return (
            f"SatisfactionSearchCase\n"
            f"Bridge kind: {self.bridge_case.kind.value}\n"
            f"Bridge: {self.bridge_case.bridge.name}\n"
            f"Preserves satisfaction: {self.preserves_satisfaction()}\n"
            f"Has distortion: {self.has_distortion()}\n"
            f"Distortion count: {self.preservation_report.distortion_count()}"
        )


@dataclass(frozen=True)
class SatisfactionSearchReport:
    """
    Report for satisfaction preservation stress search.
    """

    cases: Tuple[SatisfactionSearchCase, ...]

    def case_count(self) -> int:
        """
        Counts generated satisfaction cases.
        """

        return len(self.cases)

    def preserving_cases(self) -> Tuple[SatisfactionSearchCase, ...]:
        """
        Returns cases where satisfaction is preserved.
        """

        return tuple(case for case in self.cases if case.preserves_satisfaction())

    def distortion_cases(self) -> Tuple[SatisfactionSearchCase, ...]:
        """
        Returns cases where satisfaction distortion appears.
        """

        return tuple(case for case in self.cases if case.has_distortion())

    def cases_by_kind(self, kind: BridgeCaseKind) -> Tuple[SatisfactionSearchCase, ...]:
        """
        Returns cases of one bridge kind.
        """

        return tuple(case for case in self.cases if case.bridge_case.kind == kind)

    def preservation_rate(self) -> float:
        """
        Returns the fraction of cases preserving satisfaction.
        """

        if self.case_count() == 0:
            return 0.0

        return len(self.preserving_cases()) / self.case_count()

    def distortion_rate(self) -> float:
        """
        Returns the fraction of cases with distortion.
        """

        if self.case_count() == 0:
            return 0.0

        return len(self.distortion_cases()) / self.case_count()

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"SatisfactionSearchReport\n"
            f"Cases: {self.case_count()}\n"
            f"Preserving cases: {len(self.preserving_cases())}\n"
            f"Distortion cases: {len(self.distortion_cases())}\n"
            f"Preservation rate: {self.preservation_rate():.3f}\n"
            f"Distortion rate: {self.distortion_rate():.3f}"
        )


class InterpretationGenerator:
    """
    Generates finite truth-value interpretations.
    """

    def generate_classical_interpretations(
        self,
        universe: FiniteLogicalUniverse,
    ) -> Tuple[InterpretationCase, ...]:
        """
        Generates all true/false assignments for the statements of one universe.
        """

        statements = tuple(sorted(universe.statements, key=lambda statement: statement.name))
        truth_space = classical_truth_space()

        if len(statements) == 0:
            interpretation = explicit_interpretation(
                universe=universe,
                truth_space=truth_space,
                assignments={},
            )

            return (
                InterpretationCase(
                    universe=universe,
                    interpretation=interpretation,
                    true_count=0,
                    false_count=0,
                ),
            )

        cases = []

        for values in product(
            [FiniteTruthValue.FALSE, FiniteTruthValue.TRUE],
            repeat=len(statements),
        ):
            assignments = {
                statement: value
                for statement, value in zip(statements, values)
            }

            interpretation = explicit_interpretation(
                universe=universe,
                truth_space=truth_space,
                assignments=assignments,
            )

            true_count = sum(1 for value in values if value == FiniteTruthValue.TRUE)
            false_count = sum(1 for value in values if value == FiniteTruthValue.FALSE)

            cases.append(
                InterpretationCase(
                    universe=universe,
                    interpretation=interpretation,
                    true_count=true_count,
                    false_count=false_count,
                )
            )

        return tuple(cases)


class SatisfactionSearchRunner:
    """
    Runs generated finite stress tests for satisfaction preservation.
    """

    def __init__(self) -> None:
        self.model_generator = FiniteModelGenerator()
        self.bridge_case_generator = BridgeCaseGenerator()
        self.interpretation_generator = InterpretationGenerator()
        self.preservation_analyzer = SatisfactionPreservationAnalyzer()

    def run(
        self,
        features: Tuple[SemanticFeature, ...] = (
            SemanticFeature.CLASSICAL_TRUTH,
            SemanticFeature.MODAL_NECESSITY,
        ),
        max_feature_set_size: int = 2,
    ) -> SatisfactionSearchReport:
        """
        Runs the satisfaction preservation stress search.
        """

        universe_cases = self.model_generator.generate_universe_cases(
            features=features,
            max_feature_set_size=max_feature_set_size,
        )

        bridge_cases = self.bridge_case_generator.generate_cases(universe_cases)

        interpretation_map = {
            universe_case.universe: self.interpretation_generator.generate_classical_interpretations(
                universe_case.universe
            )
            for universe_case in universe_cases
        }

        search_cases = []

        for bridge_case in bridge_cases:
            source_interpretations = interpretation_map[bridge_case.source]
            target_interpretations = interpretation_map[bridge_case.target]

            for source_case in source_interpretations:
                for target_case in target_interpretations:
                    preservation_report = self.preservation_analyzer.analyze_bridge(
                        bridge=bridge_case.bridge,
                        source_interpretation=source_case.interpretation,
                        target_interpretation=target_case.interpretation,
                    )

                    search_cases.append(
                        SatisfactionSearchCase(
                            bridge_case=bridge_case,
                            source_case=source_case,
                            target_case=target_case,
                            source_interpretation=source_case.interpretation,
                            target_interpretation=target_case.interpretation,
                            preservation_report=preservation_report,
                        )
                    )

        return SatisfactionSearchReport(cases=tuple(search_cases))


if __name__ == "__main__":
    report = SatisfactionSearchRunner().run()

    print(report.describe())
    print()

    print("Cases by bridge kind:")
    for kind in BridgeCaseKind:
        print(f"- {kind.value}: {len(report.cases_by_kind(kind))}")

    print()
    print("Sample distortion cases:")
    for case in report.distortion_cases()[:5]:
        print("- " + case.bridge_case.bridge.name)
