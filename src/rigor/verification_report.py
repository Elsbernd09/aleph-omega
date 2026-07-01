"""
Verification report generation for Project Aleph-Omega.

This module combines:
- formal claim registry,
- theorem audit records,
- proof obligations,

into one verification report.
"""

from dataclasses import dataclass
from pathlib import Path

from src.rigor.claim_registry import ClaimRegistry, standard_claim_registry
from src.rigor.proof_obligations import (
    ProofObligationReport,
    ProofObligationTracker,
)
from src.rigor.theorem_audit import (
    TheoremAuditReport,
    TheoremAuditor,
)


@dataclass(frozen=True)
class VerificationReport:
    """
    Combined verification report.
    """

    claim_registry: ClaimRegistry
    audit_report: TheoremAuditReport
    obligation_report: ProofObligationReport

    def claim_count(self) -> int:
        """
        Counts registered claims.
        """

        return self.claim_registry.claim_count()

    def strongly_verified_count(self) -> int:
        """
        Counts strongly verified claims.
        """

        return len(self.claim_registry.strongly_verified_claims())

    def conjectural_count(self) -> int:
        """
        Counts conjectural claims.
        """

        return len(self.claim_registry.conjectural_claims())

    def audit_failure_count(self) -> int:
        """
        Counts failed audit records.
        """

        return len(self.audit_report.failed_records())

    def open_obligation_count(self) -> int:
        """
        Counts open proof obligations.
        """

        return len(self.obligation_report.open_obligations())

    def verification_health_passes(self) -> bool:
        """
        Returns whether the verification layer has no audit failures.
        """

        return self.audit_failure_count() == 0

    def describe(self) -> str:
        """
        Returns a readable verification summary.
        """

        return (
            f"VerificationReport\n"
            f"Claims: {self.claim_count()}\n"
            f"Strongly verified claims: {self.strongly_verified_count()}\n"
            f"Conjectural claims: {self.conjectural_count()}\n"
            f"Audit failures: {self.audit_failure_count()}\n"
            f"Open obligations: {self.open_obligation_count()}\n"
            f"Verification health passes: {self.verification_health_passes()}"
        )


class VerificationReportBuilder:
    """
    Builds verification reports from the standard registry.
    """

    def build(self) -> VerificationReport:
        """
        Builds the combined verification report.
        """

        registry = standard_claim_registry()
        audit_report = TheoremAuditor().audit_registry(registry)
        obligation_report = ProofObligationTracker().build_report()

        return VerificationReport(
            claim_registry=registry,
            audit_report=audit_report,
            obligation_report=obligation_report,
        )

    def to_markdown(self, report: VerificationReport) -> str:
        """
        Converts the verification report into markdown.
        """

        lines = [
            "# Verification Report",
            "",
            "## Purpose",
            "",
            "This report summarizes the formal verification interface for Project Aleph-Omega.",
            "",
            "It separates implemented finite claims, audited claim records, proof obligations, and conjectural generalizations.",
            "",
            "## Summary",
            "",
            f"- Registered claims: {report.claim_count()}",
            f"- Strongly verified claims: {report.strongly_verified_count()}",
            f"- Conjectural claims: {report.conjectural_count()}",
            f"- Audit failures: {report.audit_failure_count()}",
            f"- Open proof obligations: {report.open_obligation_count()}",
            f"- Verification health passes: {report.verification_health_passes()}",
            "",
            "## Registered Claims",
            "",
        ]

        for claim in report.claim_registry.claims:
            lines.extend(
                [
                    f"### {claim.identifier}",
                    "",
                    f"- Title: {claim.title}",
                    f"- Scope: {claim.scope.value}",
                    f"- Verification level: {claim.verification_level.value}",
                    f"- Strongly verified: {claim.is_strongly_verified()}",
                    f"- Conjectural: {claim.is_conjectural()}",
                    "",
                    "Statement:",
                    "",
                    claim.statement,
                    "",
                    "Limitations:",
                    "",
                ]
            )

            for limitation in claim.limitations:
                lines.append(f"- {limitation}")

            lines.append("")

        lines.extend(
            [
                "## Audit Summary",
                "",
                f"- Audit records: {report.audit_report.record_count()}",
                f"- Passed: {len(report.audit_report.passed_records())}",
                f"- Warnings: {len(report.audit_report.warning_records())}",
                f"- Failed: {len(report.audit_report.failed_records())}",
                "",
                "## Open Proof Obligations",
                "",
            ]
        )

        open_obligations = report.obligation_report.open_obligations()

        if not open_obligations:
            lines.append("- none")
        else:
            for obligation in open_obligations:
                lines.extend(
                    [
                        f"- {obligation.identifier}",
                        f"  - Claim: {obligation.claim_identifier}",
                        f"  - Kind: {obligation.kind.value}",
                        f"  - Description: {obligation.description}",
                    ]
                )

        lines.extend(
            [
                "",
                "## Conjectural Claims",
                "",
            ]
        )

        conjectural_claims = report.claim_registry.conjectural_claims()

        if not conjectural_claims:
            lines.append("- none")
        else:
            for claim in conjectural_claims:
                lines.append(f"- {claim.identifier}: {claim.title}")

        lines.extend(
            [
                "",
                "## Correct Research Framing",
                "",
                "The strongest Project Aleph-Omega claims remain finite, computational, and model-bound.",
                "",
                "The verification layer does not turn the project into a full formal proof assistant development.",
                "",
                "It does make the project more responsible by separating finite verified claims from conjectural generalizations.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: VerificationReport,
        path: str = "docs/verification_report.md",
    ) -> Path:
        """
        Writes the verification report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = VerificationReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote report to {output_path}")
