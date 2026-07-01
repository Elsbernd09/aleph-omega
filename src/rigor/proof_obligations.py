"""
Proof obligation tracker for Project Aleph-Omega.

This module records open proof obligations associated with registered formal
claims.

A proof obligation is something the project must prove, test, clarify, or
explicitly mark as outside scope.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from src.rigor.claim_registry import FormalClaim, standard_claim_registry


class ObligationStatus(str, Enum):
    """
    Status of a proof obligation.
    """

    OPEN = "open"
    SATISFIED = "satisfied"
    OUT_OF_SCOPE = "out_of_scope"
    CONJECTURAL = "conjectural"


class ObligationKind(str, Enum):
    """
    Kind of proof obligation.
    """

    FORMAL_PROOF = "formal_proof"
    UNIT_TEST = "unit_test"
    STRESS_TEST = "stress_test"
    DOCUMENTATION = "documentation"
    LIMITATION = "limitation"
    GENERALIZATION = "generalization"


@dataclass(frozen=True)
class ProofObligation:
    """
    A proof obligation attached to a formal claim.
    """

    identifier: str
    claim_identifier: str
    kind: ObligationKind
    status: ObligationStatus
    description: str
    evidence: Tuple[str, ...] = ()

    def is_closed(self) -> bool:
        """
        Returns whether this obligation is no longer open.
        """

        return self.status in {
            ObligationStatus.SATISFIED,
            ObligationStatus.OUT_OF_SCOPE,
            ObligationStatus.CONJECTURAL,
        }

    def is_open(self) -> bool:
        """
        Returns whether this obligation is still open.
        """

        return self.status == ObligationStatus.OPEN

    def describe(self) -> str:
        """
        Returns a readable proof obligation.
        """

        evidence_text = "; ".join(self.evidence) if self.evidence else "none"

        return (
            f"ProofObligation\n"
            f"Identifier: {self.identifier}\n"
            f"Claim: {self.claim_identifier}\n"
            f"Kind: {self.kind.value}\n"
            f"Status: {self.status.value}\n"
            f"Open: {self.is_open()}\n"
            f"Closed: {self.is_closed()}\n"
            f"Description: {self.description}\n"
            f"Evidence: {evidence_text}"
        )


@dataclass(frozen=True)
class ProofObligationReport:
    """
    Report of proof obligations.
    """

    obligations: Tuple[ProofObligation, ...]

    def obligation_count(self) -> int:
        """
        Counts obligations.
        """

        return len(self.obligations)

    def open_obligations(self) -> Tuple[ProofObligation, ...]:
        """
        Returns open obligations.
        """

        return tuple(item for item in self.obligations if item.is_open())

    def closed_obligations(self) -> Tuple[ProofObligation, ...]:
        """
        Returns closed obligations.
        """

        return tuple(item for item in self.obligations if item.is_closed())

    def by_claim(self, claim_identifier: str) -> Tuple[ProofObligation, ...]:
        """
        Returns obligations for one claim.
        """

        return tuple(
            item for item in self.obligations
            if item.claim_identifier == claim_identifier
        )

    def by_status(self, status: ObligationStatus) -> Tuple[ProofObligation, ...]:
        """
        Returns obligations with one status.
        """

        return tuple(item for item in self.obligations if item.status == status)

    def by_kind(self, kind: ObligationKind) -> Tuple[ProofObligation, ...]:
        """
        Returns obligations of one kind.
        """

        return tuple(item for item in self.obligations if item.kind == kind)

    def describe(self) -> str:
        """
        Returns a readable report.
        """

        return (
            f"ProofObligationReport\n"
            f"Obligations: {self.obligation_count()}\n"
            f"Open obligations: {len(self.open_obligations())}\n"
            f"Closed obligations: {len(self.closed_obligations())}"
        )


class ProofObligationTracker:
    """
    Builds proof obligations from the standard claim registry.
    """

    def obligations_for_claim(self, claim: FormalClaim) -> Tuple[ProofObligation, ...]:
        """
        Returns proof obligations for one registered claim.
        """

        obligations = []

        obligations.append(
            ProofObligation(
                identifier=f"{claim.identifier}.documentation",
                claim_identifier=claim.identifier,
                kind=ObligationKind.DOCUMENTATION,
                status=ObligationStatus.SATISFIED if claim.evidence else ObligationStatus.OPEN,
                description="The claim should have documented evidence records.",
                evidence=claim.evidence,
            )
        )

        obligations.append(
            ProofObligation(
                identifier=f"{claim.identifier}.limitations",
                claim_identifier=claim.identifier,
                kind=ObligationKind.LIMITATION,
                status=ObligationStatus.SATISFIED if claim.limitations else ObligationStatus.OPEN,
                description="The claim should list limitations to prevent overclaiming.",
                evidence=claim.limitations,
            )
        )

        if claim.is_conjectural():
            obligations.append(
                ProofObligation(
                    identifier=f"{claim.identifier}.generalization",
                    claim_identifier=claim.identifier,
                    kind=ObligationKind.GENERALIZATION,
                    status=ObligationStatus.CONJECTURAL,
                    description="The claim is a conjectural generalization and is not proven in this project.",
                    evidence=claim.limitations,
                )
            )
        elif claim.is_strongly_verified():
            obligations.append(
                ProofObligation(
                    identifier=f"{claim.identifier}.stress_or_proof",
                    claim_identifier=claim.identifier,
                    kind=ObligationKind.STRESS_TEST,
                    status=ObligationStatus.SATISFIED,
                    description="The claim has finite proof or generated stress-test support.",
                    evidence=claim.evidence,
                )
            )
        else:
            obligations.append(
                ProofObligation(
                    identifier=f"{claim.identifier}.additional_verification",
                    claim_identifier=claim.identifier,
                    kind=ObligationKind.FORMAL_PROOF,
                    status=ObligationStatus.OPEN,
                    description="The claim has support, but stronger proof or stress testing could further improve it.",
                    evidence=claim.evidence,
                )
            )

        return tuple(obligations)

    def build_report(self) -> ProofObligationReport:
        """
        Builds proof obligations for the standard claim registry.
        """

        obligations = []

        for claim in standard_claim_registry().claims:
            obligations.extend(self.obligations_for_claim(claim))

        return ProofObligationReport(obligations=tuple(obligations))


if __name__ == "__main__":
    report = ProofObligationTracker().build_report()

    print(report.describe())
    print()

    print("Open obligations:")
    for obligation in report.open_obligations():
        print()
        print(obligation.describe())
