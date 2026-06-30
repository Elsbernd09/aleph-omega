"""
Translation result model for Project ℵω bridge systems.

This module defines the data structures used when a statement is translated
from one toy formal universe into another.

The goal is not to prove that the translation is mathematically complete.
The goal is to make preservation, distortion, weakening, and loss visible.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from src.toy_topoi.statements import ProofStatus, Statement
from src.toy_topoi.truth_values import TruthValue


class TranslationStatus(str, Enum):
    """
    High-level status of a universe-to-universe translation.
    """

    EXACT = "exact"
    PRESERVED = "preserved"
    WEAKENED = "weakened"
    DISTORTED = "distorted"
    PARTIAL = "partial"
    FAILED = "failed"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"


class MeaningChangeKind(str, Enum):
    """
    Kinds of meaning changes that may occur during translation.
    """

    NO_CHANGE = "no_change"
    TRUTH_VALUE_CHANGE = "truth_value_change"
    PROOF_STATUS_CHANGE = "proof_status_change"
    SYMBOL_LOSS = "symbol_loss"
    FEATURE_LOSS = "feature_loss"
    CONTRADICTION_COLLAPSE = "contradiction_collapse"
    MODAL_COLLAPSE = "modal_collapse"
    CONSTRUCTIVE_WEAKENING = "constructive_weakening"
    CONTEXT_ERASURE = "context_erasure"
    AMBIGUITY_INCREASE = "ambiguity_increase"


@dataclass(frozen=True)
class MeaningChange:
    """
    Records one specific meaning change during translation.
    """

    kind: MeaningChangeKind
    description: str
    severity: float = 0.0

    def normalized_severity(self) -> float:
        """
        Returns severity clamped between 0 and 10.
        """

        return round(max(0.0, min(10.0, self.severity)), 2)

    def describe(self) -> str:
        """
        Returns a readable change description.
        """

        return (
            f"MeaningChange(kind={self.kind.value}, "
            f"severity={self.normalized_severity()}, "
            f"description={self.description})"
        )


@dataclass(frozen=True)
class TranslationResult:
    """
    Result of translating one statement between two universes.
    """

    source_statement: Statement
    translated_statement: Statement
    source_universe_name: str
    target_universe_name: str
    source_truth_value: TruthValue
    target_truth_value: TruthValue
    source_proof_status: ProofStatus
    target_proof_status: ProofStatus
    preserved_symbols: List[str] = field(default_factory=list)
    lost_symbols: List[str] = field(default_factory=list)
    added_symbols: List[str] = field(default_factory=list)
    preserved_features: List[str] = field(default_factory=list)
    lost_features: List[str] = field(default_factory=list)
    meaning_changes: List[MeaningChange] = field(default_factory=list)
    translation_status: TranslationStatus = TranslationStatus.REQUIRES_HUMAN_REVIEW
    translation_confidence: float = 0.0
    notes: str = ""
    metadata: Optional[Dict[str, str]] = None

    def symbol_preservation_score(self) -> float:
        """
        Scores how many source symbols survived the translation.
        """

        total = len(set(self.preserved_symbols + self.lost_symbols))

        if total == 0:
            return 10.0

        score = 10.0 * len(set(self.preserved_symbols)) / total
        return round(max(0.0, min(10.0, score)), 2)

    def feature_preservation_score(self) -> float:
        """
        Scores how many required features survived the translation.
        """

        total = len(set(self.preserved_features + self.lost_features))

        if total == 0:
            return 10.0

        score = 10.0 * len(set(self.preserved_features)) / total
        return round(max(0.0, min(10.0, score)), 2)

    def average_meaning_change_severity(self) -> float:
        """
        Computes average severity across meaning changes.
        """

        if not self.meaning_changes:
            return 0.0

        total = sum(change.normalized_severity() for change in self.meaning_changes)
        return round(total / len(self.meaning_changes), 2)

    def distortion_score(self) -> float:
        """
        Computes a toy distortion score from 0 to 10.

        Higher means the translation changed more meaning.
        """

        symbol_loss = 10.0 - self.symbol_preservation_score()
        feature_loss = 10.0 - self.feature_preservation_score()
        severity = self.average_meaning_change_severity()

        score = symbol_loss * 0.35 + feature_loss * 0.35 + severity * 0.30
        return round(max(0.0, min(10.0, score)), 2)

    def is_high_quality_translation(self) -> bool:
        """
        Returns whether the translation appears high quality.
        """

        return (
            self.translation_confidence >= 7.0
            and self.distortion_score() <= 3.0
            and self.translation_status in {
                TranslationStatus.EXACT,
                TranslationStatus.PRESERVED,
                TranslationStatus.WEAKENED,
            }
        )

    def summary_row(self) -> Dict[str, object]:
        """
        Returns compact table data.
        """

        return {
            "statement": self.source_statement.name,
            "source_universe": self.source_universe_name,
            "target_universe": self.target_universe_name,
            "source_truth": self.source_truth_value.value,
            "target_truth": self.target_truth_value.value,
            "source_proof": self.source_proof_status.value,
            "target_proof": self.target_proof_status.value,
            "status": self.translation_status.value,
            "confidence": self.translation_confidence,
            "symbol_preservation": self.symbol_preservation_score(),
            "feature_preservation": self.feature_preservation_score(),
            "distortion": self.distortion_score(),
        }

    def describe(self) -> str:
        """
        Returns a readable translation report.
        """

        changes = "\n".join(
            f"  - {change.describe()}" for change in self.meaning_changes
        ) or "  - none"

        return (
            f"TranslationResult\n"
            f"Statement: {self.source_statement.name}\n"
            f"Source universe: {self.source_universe_name}\n"
            f"Target universe: {self.target_universe_name}\n"
            f"Source truth value: {self.source_truth_value.value}\n"
            f"Target truth value: {self.target_truth_value.value}\n"
            f"Source proof status: {self.source_proof_status.value}\n"
            f"Target proof status: {self.target_proof_status.value}\n"
            f"Translation status: {self.translation_status.value}\n"
            f"Translation confidence: {self.translation_confidence}\n"
            f"Symbol preservation score: {self.symbol_preservation_score()}\n"
            f"Feature preservation score: {self.feature_preservation_score()}\n"
            f"Distortion score: {self.distortion_score()}\n"
            f"Preserved symbols: {', '.join(self.preserved_symbols) or 'none'}\n"
            f"Lost symbols: {', '.join(self.lost_symbols) or 'none'}\n"
            f"Added symbols: {', '.join(self.added_symbols) or 'none'}\n"
            f"Preserved features: {', '.join(self.preserved_features) or 'none'}\n"
            f"Lost features: {', '.join(self.lost_features) or 'none'}\n"
            f"Meaning changes:\n{changes}\n"
            f"Notes: {self.notes or 'none'}"
        )
