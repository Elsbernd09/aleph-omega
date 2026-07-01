"""
Tests for theorem audit records.
"""

from src.rigor.claim_registry import (
    ClaimScope,
    FormalClaim,
    VerificationLevel,
    standard_claim_registry,
)
from src.rigor.theorem_audit import (
    AuditStatus,
    TheoremAuditRecord,
    TheoremAuditReport,
    TheoremAuditor,
)


def test_audit_status_values():
    assert AuditStatus.PASSED.value == "passed"
    assert AuditStatus.WARNING.value == "warning"
    assert AuditStatus.FAILED.value == "failed"


def test_audit_standard_registry():
    report = TheoremAuditor().audit_registry(standard_claim_registry())

    assert isinstance(report, TheoremAuditReport)
    assert report.record_count() >= 5
    assert report.all_passed_or_warned()
    assert "TheoremAuditReport" in report.describe()


def test_audit_claim_record_exists():
    claim = standard_claim_registry().by_identifier("claim.composition_preservation.finite")
    record = TheoremAuditor().audit_claim(claim)

    assert isinstance(record, TheoremAuditRecord)
    assert record.status in set(AuditStatus)
    assert "TheoremAuditRecord" in record.describe()


def test_empty_statement_fails():
    claim = FormalClaim(
        identifier="claim.bad.empty",
        title="Bad Empty Claim",
        statement="",
        scope=ClaimScope.FINITE_MODEL,
        verification_level=VerificationLevel.DOCUMENTED,
        evidence=("docs/formal_claim_registry.md",),
        limitations=("Finite model only.",),
    )

    record = TheoremAuditor().audit_claim(claim)

    assert record.failed()
    assert record.status == AuditStatus.FAILED


def test_missing_limitations_warns():
    claim = FormalClaim(
        identifier="claim.warn.no_limitations",
        title="No Limitations Claim",
        statement="This claim has a statement.",
        scope=ClaimScope.FINITE_MODEL,
        verification_level=VerificationLevel.DOCUMENTED,
        evidence=("docs/formal_claim_registry.md",),
        limitations=(),
    )

    record = TheoremAuditor().audit_claim(claim)

    assert record.has_warning()
    assert record.status == AuditStatus.WARNING


def test_conjectural_generalization_must_be_conjectural():
    claim = FormalClaim(
        identifier="claim.bad.general",
        title="Bad General Claim",
        statement="This tries to generalize.",
        scope=ClaimScope.CONJECTURAL_GENERALIZATION,
        verification_level=VerificationLevel.FINITE_PROOF,
        evidence=("docs/formal_claim_registry.md",),
        limitations=("Not proven.",),
    )

    record = TheoremAuditor().audit_claim(claim)

    assert record.failed()


def test_missing_evidence_file_warns():
    claim = FormalClaim(
        identifier="claim.warn.missing_file",
        title="Missing File Claim",
        statement="This claim cites a missing file.",
        scope=ClaimScope.FINITE_MODEL,
        verification_level=VerificationLevel.DOCUMENTED,
        evidence=("docs/this_file_should_not_exist.md",),
        limitations=("Finite model only.",),
    )

    record = TheoremAuditor().audit_claim(claim)

    assert record.has_warning()
