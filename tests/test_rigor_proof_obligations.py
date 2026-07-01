"""
Tests for proof obligation tracking.
"""

from src.rigor.claim_registry import standard_claim_registry
from src.rigor.proof_obligations import (
    ObligationKind,
    ObligationStatus,
    ProofObligation,
    ProofObligationReport,
    ProofObligationTracker,
)


def test_obligation_status_values():
    assert ObligationStatus.OPEN.value == "open"
    assert ObligationStatus.SATISFIED.value == "satisfied"
    assert ObligationStatus.CONJECTURAL.value == "conjectural"


def test_obligation_kind_values():
    assert ObligationKind.FORMAL_PROOF.value == "formal_proof"
    assert ObligationKind.STRESS_TEST.value == "stress_test"
    assert ObligationKind.GENERALIZATION.value == "generalization"


def test_build_report_exists():
    report = ProofObligationTracker().build_report()

    assert isinstance(report, ProofObligationReport)
    assert report.obligation_count() > 0
    assert "ProofObligationReport" in report.describe()


def test_obligations_for_one_claim():
    claim = standard_claim_registry().by_identifier("claim.composition_preservation.finite")
    obligations = ProofObligationTracker().obligations_for_claim(claim)

    assert len(obligations) >= 3
    assert all(isinstance(item, ProofObligation) for item in obligations)
    assert any(item.kind == ObligationKind.DOCUMENTATION for item in obligations)
    assert any(item.kind == ObligationKind.LIMITATION for item in obligations)


def test_report_has_open_and_closed_obligations():
    report = ProofObligationTracker().build_report()

    assert len(report.closed_obligations()) > 0
    assert len(report.open_obligations()) > 0


def test_by_claim_status_and_kind():
    report = ProofObligationTracker().build_report()

    claim_id = "claim.general_foundations"

    assert len(report.by_claim(claim_id)) > 0
    assert len(report.by_status(ObligationStatus.CONJECTURAL)) > 0
    assert len(report.by_kind(ObligationKind.DOCUMENTATION)) > 0


def test_obligation_describe():
    obligation = ProofObligationTracker().build_report().obligations[0]

    description = obligation.describe()

    assert "ProofObligation" in description
    assert "Identifier:" in description
