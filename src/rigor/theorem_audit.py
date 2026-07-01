"""
Theorem audit records for Project Aleph-Omega.

This module audits registered claims by checking whether they have:
- evidence files,
- limitations,
- verification levels,
- clear scope,
- conjectural marking when needed.

The audit does not prove the claims. It checks that the project records them
responsibly.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Tuple

from src.rigor.claim_registry import (
    ClaimRegistry,
    ClaimScope,
    FormalClaim,
    VerificationLevel,
    standard_claim_registry,
)


class AuditStatus(str, Enum):
    """
    Status of a theorem or claim audit.
    """

    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"


@dataclass(frozen=True)
class TheoremAuditRecord:
    """
    Audit record for one formal claim.
    """

    claim: FormalClaim
    status: AuditStatus
    messages: Tuple[str, ...]

    def passed(self) -> bool:
        """
        Returns whether the audit passed.
        """

        return self.status == AuditStatus.PASSED

    def has_warning(self) -> bool:
        """
        Returns whether the audit has a warning.
        """

        return self.status == AuditStatus.WARNING

    def failed(self) -> bool:
        """
        Returns whether the audit failed.
        """

        return self.status == AuditStatus.FAILED

    def describe(self) -> str:
        """
        Returns a readable audit record.
        """

        message_text = "; ".join(self.messages) if self.messages else "none"

        return (
            f"TheoremAuditRecord\n"
            f"Claim: {self.claim.identifier}\n"
            f"Title: {self.claim.title}\n"
            f"Status: {self.status.value}\n"
            f"Messages: {message_text}"
        )


@dataclass(frozen=True)
class TheoremAuditReport:
    """
    Audit report for a claim registry.
    """

    records: Tuple[TheoremAuditRecord, ...]

    def record_count(self) -> int:
        """
        Counts audit records.
        """

        return len(self.records)

    def passed_records(self) -> Tuple[TheoremAuditRecord, ...]:
        """
        Returns passed records.
        """

        return tuple(record for record in self.records if record.passed())

    def warning_records(self) -> Tuple[TheoremAuditRecord, ...]:
        """
        Returns warning records.
        """

        return tuple(record for record in self.records if record.has_warning())

    def failed_records(self) -> Tuple[TheoremAuditRecord, ...]:
        """
        Returns failed records.
        """

        return tuple(record for record in self.records if record.failed())

    def all_passed_or_warned(self) -> bool:
        """
        Returns whether no record failed.
        """

        return len(self.failed_records()) == 0

    def describe(self) -> str:
        """
        Returns a readable audit report.
        """

        return (
            f"TheoremAuditReport\n"
            f"Records: {self.record_count()}\n"
            f"Passed: {len(self.passed_records())}\n"
            f"Warnings: {len(self.warning_records())}\n"
            f"Failed: {len(self.failed_records())}\n"
            f"No failures: {self.all_passed_or_warned()}"
        )


class TheoremAuditor:
    """
    Audits formal claims for responsible theorem-record hygiene.
    """

    def audit_claim(self, claim: FormalClaim) -> TheoremAuditRecord:
        """
        Audits one claim.
        """

        messages = []
        status = AuditStatus.PASSED

        if not claim.statement.strip():
            messages.append("Claim statement is empty.")
            status = AuditStatus.FAILED

        if not claim.evidence:
            messages.append("Claim has no evidence records.")
            status = AuditStatus.FAILED

        if not claim.limitations:
            messages.append("Claim has no limitations listed.")
            if status != AuditStatus.FAILED:
                status = AuditStatus.WARNING

        if claim.scope == ClaimScope.CONJECTURAL_GENERALIZATION:
            if claim.verification_level != VerificationLevel.CONJECTURAL:
                messages.append("Conjectural generalization is not marked conjectural.")
                status = AuditStatus.FAILED

        if claim.verification_level == VerificationLevel.CONJECTURAL:
            if "not proven" not in " ".join(claim.limitations).lower():
                messages.append("Conjectural claim should explicitly state that it is not proven.")
                if status != AuditStatus.FAILED:
                    status = AuditStatus.WARNING

        missing_files = self.missing_evidence_files(claim)

        if missing_files:
            messages.append(
                "Missing evidence files: " + ", ".join(missing_files)
            )
            if status != AuditStatus.FAILED:
                status = AuditStatus.WARNING

        if not messages:
            messages.append("Audit passed.")

        return TheoremAuditRecord(
            claim=claim,
            status=status,
            messages=tuple(messages),
        )

    def missing_evidence_files(self, claim: FormalClaim) -> Tuple[str, ...]:
        """
        Returns evidence paths that look like local project files but do not exist.
        """

        missing = []

        for item in claim.evidence:
            if item.startswith(("src/", "tests/", "docs/")):
                if not Path(item).exists():
                    missing.append(item)

        return tuple(missing)

    def audit_registry(self, registry: ClaimRegistry) -> TheoremAuditReport:
        """
        Audits every claim in a registry.
        """

        return TheoremAuditReport(
            records=tuple(self.audit_claim(claim) for claim in registry.claims)
        )


if __name__ == "__main__":
    report = TheoremAuditor().audit_registry(standard_claim_registry())

    print(report.describe())
    print()

    for record in report.records:
        print(record.describe())
        print()
