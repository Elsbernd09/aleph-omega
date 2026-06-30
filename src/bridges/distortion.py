"""
Distortion metrics for Project ℵω bridge translations.

This module analyzes TranslationResult objects and produces a structured
distortion report.

The goal is to measure how much meaning appears to change when a statement is
translated from one toy formal universe into another.

These are heuristic research metrics, not formal semantic invariants.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from src.bridges.translation_result import TranslationResult


class TranslationGrade(str, Enum):
    """
    Human-readable translation quality grade.
    """

    EXCELLENT = "excellent"
    GOOD = "good"
    MODERATE = "moderate"
    WEAK = "weak"
    SEVERE = "severe"
    FAILED = "failed"


@dataclass(frozen=True)
class DistortionReport:
    """
    Structured distortion report for one translation.
    """

    statement_name: str
    source_universe_name: str
    target_universe_name: str
    symbol_distortion: float
    feature_distortion: float
    truth_distortion: float
    proof_distortion: float
    semantic_severity: float
    confidence_penalty: float
    overall_distortion_index: float
    translation_grade: TranslationGrade
    explanation: str
    metadata: Optional[Dict[str, str]] = None

    def as_dict(self) -> Dict[str, object]:
        """
        Converts the report into dictionary form.
        """

        return {
            "statement_name": self.statement_name,
            "source_universe_name": self.source_universe_name,
            "target_universe_name": self.target_universe_name,
            "symbol_distortion": self.symbol_distortion,
            "feature_distortion": self.feature_distortion,
            "truth_distortion": self.truth_distortion,
            "proof_distortion": self.proof_distortion,
            "semantic_severity": self.semantic_severity,
            "confidence_penalty": self.confidence_penalty,
            "overall_distortion_index": self.overall_distortion_index,
            "translation_grade": self.translation_grade.value,
            "explanation": self.explanation,
        }

    def describe(self) -> str:
        """
        Returns a readable distortion report.
        """

        return (
            f"DistortionReport\n"
            f"Statement: {self.statement_name}\n"
            f"Source universe: {self.source_universe_name}\n"
            f"Target universe: {self.target_universe_name}\n"
            f"Symbol distortion: {self.symbol_distortion}\n"
            f"Feature distortion: {self.feature_distortion}\n"
            f"Truth distortion: {self.truth_distortion}\n"
            f"Proof distortion: {self.proof_distortion}\n"
            f"Semantic severity: {self.semantic_severity}\n"
            f"Confidence penalty: {self.confidence_penalty}\n"
            f"Overall distortion index: {self.overall_distortion_index}\n"
            f"Translation grade: {self.translation_grade.value}\n"
            f"Explanation: {self.explanation}"
        )


class DistortionAnalyzer:
    """
    Analyzes distortion in TranslationResult objects.
    """

    def analyze(self, result: TranslationResult) -> DistortionReport:
        """
        Produces a distortion report for one translation result.
        """

        symbol_distortion = self._symbol_distortion(result)
        feature_distortion = self._feature_distortion(result)
        truth_distortion = self._truth_distortion(result)
        proof_distortion = self._proof_distortion(result)
        semantic_severity = self._semantic_severity(result)
        confidence_penalty = self._confidence_penalty(result)

        overall = self._overall_distortion_index(
            symbol_distortion=symbol_distortion,
            feature_distortion=feature_distortion,
            truth_distortion=truth_distortion,
            proof_distortion=proof_distortion,
            semantic_severity=semantic_severity,
            confidence_penalty=confidence_penalty,
        )

        grade = self._grade(overall)

        explanation = self._explanation(
            result=result,
            symbol_distortion=symbol_distortion,
            feature_distortion=feature_distortion,
            truth_distortion=truth_distortion,
            proof_distortion=proof_distortion,
            semantic_severity=semantic_severity,
            confidence_penalty=confidence_penalty,
            overall=overall,
            grade=grade,
        )

        return DistortionReport(
            statement_name=result.source_statement.name,
            source_universe_name=result.source_universe_name,
            target_universe_name=result.target_universe_name,
            symbol_distortion=symbol_distortion,
            feature_distortion=feature_distortion,
            truth_distortion=truth_distortion,
            proof_distortion=proof_distortion,
            semantic_severity=semantic_severity,
            confidence_penalty=confidence_penalty,
            overall_distortion_index=overall,
            translation_grade=grade,
            explanation=explanation,
            metadata={
                "translation_status": result.translation_status.value,
                "translation_confidence": str(result.translation_confidence),
                "result_distortion_score": str(result.distortion_score()),
            },
        )

    def analyze_many(self, results: List[TranslationResult]) -> List[DistortionReport]:
        """
        Produces distortion reports for many translation results.
        """

        return [self.analyze(result) for result in results]

    @staticmethod
    def _symbol_distortion(result: TranslationResult) -> float:
        """
        Computes symbol distortion from symbol preservation score.
        """

        return round(10.0 - result.symbol_preservation_score(), 2)

    @staticmethod
    def _feature_distortion(result: TranslationResult) -> float:
        """
        Computes feature distortion from feature preservation score.
        """

        return round(10.0 - result.feature_preservation_score(), 2)

    @staticmethod
    def _truth_distortion(result: TranslationResult) -> float:
        """
        Scores distortion caused by truth-value change.
        """

        if result.source_truth_value == result.target_truth_value:
            return 0.0

        source = result.source_truth_value.value
        target = result.target_truth_value.value

        severe_pairs = {
            ("both", "false"),
            ("possible", "true"),
            ("necessary", "true"),
            ("contingent", "true"),
            ("unknown", "false"),
            ("neither", "false"),
        }

        if (source, target) in severe_pairs:
            return 7.5

        return 5.0

    @staticmethod
    def _proof_distortion(result: TranslationResult) -> float:
        """
        Scores distortion caused by proof-status change.
        """

        if result.source_proof_status == result.target_proof_status:
            return 0.0

        source = result.source_proof_status.value
        target = result.target_proof_status.value

        severe_pairs = {
            ("contradictory", "refuted"),
            ("machine_checked", "untested"),
            ("derived", "unknown"),
            ("assumed", "refuted"),
        }

        if (source, target) in severe_pairs:
            return 7.0

        return 4.0

    @staticmethod
    def _semantic_severity(result: TranslationResult) -> float:
        """
        Computes average meaning-change severity.
        """

        return result.average_meaning_change_severity()

    @staticmethod
    def _confidence_penalty(result: TranslationResult) -> float:
        """
        Converts low translation confidence into a distortion penalty.
        """

        return round(max(0.0, 10.0 - result.translation_confidence), 2)

    @staticmethod
    def _overall_distortion_index(
        symbol_distortion: float,
        feature_distortion: float,
        truth_distortion: float,
        proof_distortion: float,
        semantic_severity: float,
        confidence_penalty: float,
    ) -> float:
        """
        Computes weighted overall distortion index from 0 to 10.
        """

        score = 0.0
        score += symbol_distortion * 0.18
        score += feature_distortion * 0.22
        score += truth_distortion * 0.18
        score += proof_distortion * 0.12
        score += semantic_severity * 0.20
        score += confidence_penalty * 0.10

        return round(max(0.0, min(10.0, score)), 2)

    @staticmethod
    def _grade(overall: float) -> TranslationGrade:
        """
        Converts overall distortion into a translation grade.
        """

        if overall <= 1.5:
            return TranslationGrade.EXCELLENT

        if overall <= 3.0:
            return TranslationGrade.GOOD

        if overall <= 4.75:
            return TranslationGrade.MODERATE

        if overall <= 6.5:
            return TranslationGrade.WEAK

        if overall <= 8.25:
            return TranslationGrade.SEVERE

        return TranslationGrade.FAILED

    @staticmethod
    def _explanation(
        result: TranslationResult,
        symbol_distortion: float,
        feature_distortion: float,
        truth_distortion: float,
        proof_distortion: float,
        semantic_severity: float,
        confidence_penalty: float,
        overall: float,
        grade: TranslationGrade,
    ) -> str:
        """
        Builds a readable explanation.
        """

        return (
            f"The translation of '{result.source_statement.name}' from "
            f"'{result.source_universe_name}' to '{result.target_universe_name}' "
            f"received overall distortion index {overall} and grade "
            f"'{grade.value}'. Component scores: symbol distortion "
            f"{symbol_distortion}, feature distortion {feature_distortion}, "
            f"truth distortion {truth_distortion}, proof distortion "
            f"{proof_distortion}, semantic severity {semantic_severity}, "
            f"confidence penalty {confidence_penalty}. Translation status was "
            f"'{result.translation_status.value}' with confidence "
            f"{result.translation_confidence}."
        )


def rank_reports_by_distortion(reports: List[DistortionReport]) -> List[DistortionReport]:
    """
    Ranks reports from most distorted to least distorted.
    """

    return sorted(
        reports,
        key=lambda report: report.overall_distortion_index,
        reverse=True,
    )


def rank_reports_by_quality(reports: List[DistortionReport]) -> List[DistortionReport]:
    """
    Ranks reports from least distorted to most distorted.
    """

    return sorted(
        reports,
        key=lambda report: report.overall_distortion_index,
    )


if __name__ == "__main__":
    from src.bridges.bridge_map import starter_bridge_maps
    from src.bridges.translator import UniverseTranslator
    from src.toy_topoi.library import find_universe_by_name
    from src.toy_topoi.statements import starter_statements

    translator = UniverseTranslator()
    analyzer = DistortionAnalyzer()

    translation_results = []

    for bridge in starter_bridge_maps():
        source_universe = find_universe_by_name(bridge.source_universe_name)
        target_universe = find_universe_by_name(bridge.target_universe_name)

        if source_universe is None or target_universe is None:
            continue

        for statement in starter_statements():
            if statement.origin_universe == bridge.source_universe_name:
                translation_results.append(
                    translator.translate(
                        statement=statement,
                        source_universe=source_universe,
                        target_universe=target_universe,
                        bridge=bridge,
                    )
                )

    reports = analyzer.analyze_many(translation_results)

    for report in rank_reports_by_distortion(reports):
        print(report.describe())
        print("-" * 80)
