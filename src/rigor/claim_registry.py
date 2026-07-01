"""
Formal claim registry for Project Aleph-Omega.

This module records mathematical claims, their scope, their verification level,
and their current evidence.

The goal is to avoid overclaiming. A claim can be:
- implemented,
- tested on finite generated cases,
- proved in a finite model,
- documented,
- or still conjectural.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class ClaimScope(str, Enum):
    """
    Scope of a mathematical claim.
    """

    FINITE_MODEL = "finite_model"
    GENERATED_SEARCH_SPACE = "generated_search_space"
    IMPLEMENTATION_LEVEL = "implementation_level"
    HUMAN_PROOF_SKETCH = "human_proof_sketch"
    CONJECTURAL_GENERALIZATION = "conjectural_generalization"


class VerificationLevel(str, Enum):
    """
    Verification level of a claim.
    """

    UNCHECKED = "unchecked"
    DOCUMENTED = "documented"
    TESTED_BY_UNIT_TESTS = "tested_by_unit_tests"
    STRESS_TESTED = "stress_tested"
    FINITE_PROOF = "finite_proof"
    CONJECTURAL = "conjectural"


@dataclass(frozen=True)
class FormalClaim:
    """
    A registered mathematical claim.
    """

    identifier: str
    title: str
    statement: str
    scope: ClaimScope
    verification_level: VerificationLevel
    evidence: Tuple[str, ...]
    limitations: Tuple[str, ...] = ()

    def is_strongly_verified(self) -> bool:
        """
        Returns whether the claim has strong finite-model support.
        """

        return self.verification_level in {
            VerificationLevel.STRESS_TESTED,
            VerificationLevel.FINITE_PROOF,
        }

    def is_conjectural(self) -> bool:
        """
        Returns whether the claim is conjectural.
        """

        return (
            self.verification_level == VerificationLevel.CONJECTURAL
            or self.scope == ClaimScope.CONJECTURAL_GENERALIZATION
        )

    def describe(self) -> str:
        """
        Returns a readable claim description.
        """

        evidence_text = "; ".join(self.evidence) if self.evidence else "none"
        limitations_text = "; ".join(self.limitations) if self.limitations else "none"

        return (
            f"FormalClaim\n"
            f"Identifier: {self.identifier}\n"
            f"Title: {self.title}\n"
            f"Scope: {self.scope.value}\n"
            f"Verification level: {self.verification_level.value}\n"
            f"Strongly verified: {self.is_strongly_verified()}\n"
            f"Conjectural: {self.is_conjectural()}\n"
            f"Statement: {self.statement}\n"
            f"Evidence: {evidence_text}\n"
            f"Limitations: {limitations_text}"
        )


@dataclass(frozen=True)
class ClaimRegistry:
    """
    Registry of formal claims.
    """

    claims: Tuple[FormalClaim, ...]

    def claim_count(self) -> int:
        """
        Counts claims.
        """

        return len(self.claims)

    def by_identifier(self, identifier: str) -> FormalClaim:
        """
        Finds a claim by identifier.
        """

        for claim in self.claims:
            if claim.identifier == identifier:
                return claim

        raise KeyError(f"No claim with identifier: {identifier}")

    def by_scope(self, scope: ClaimScope) -> Tuple[FormalClaim, ...]:
        """
        Returns claims with a given scope.
        """

        return tuple(claim for claim in self.claims if claim.scope == scope)

    def by_verification_level(
        self,
        level: VerificationLevel,
    ) -> Tuple[FormalClaim, ...]:
        """
        Returns claims with a given verification level.
        """

        return tuple(claim for claim in self.claims if claim.verification_level == level)

    def strongly_verified_claims(self) -> Tuple[FormalClaim, ...]:
        """
        Returns strongly verified claims.
        """

        return tuple(claim for claim in self.claims if claim.is_strongly_verified())

    def conjectural_claims(self) -> Tuple[FormalClaim, ...]:
        """
        Returns conjectural claims.
        """

        return tuple(claim for claim in self.claims if claim.is_conjectural())

    def describe(self) -> str:
        """
        Returns a readable registry summary.
        """

        return (
            f"ClaimRegistry\n"
            f"Claims: {self.claim_count()}\n"
            f"Strongly verified claims: {len(self.strongly_verified_claims())}\n"
            f"Conjectural claims: {len(self.conjectural_claims())}"
        )


def standard_claim_registry() -> ClaimRegistry:
    """
    Returns the standard Project Aleph-Omega formal claim registry.
    """

    claims = (
        FormalClaim(
            identifier="claim.bridge_distortion.finite",
            title="Finite Bridge Distortion Theorem",
            statement=(
                "Within the implemented finite bridge model, bridges that fail "
                "structural preservation can be detected as distortion-bearing "
                "or vacuous instances according to the theorem checker."
            ),
            scope=ClaimScope.FINITE_MODEL,
            verification_level=VerificationLevel.STRESS_TESTED,
            evidence=(
                "src/rigor/theorem.py",
                "src/rigor/bridge_distortion_search.py",
                "tests/test_rigor_bridge_distortion_search.py",
                "docs/bridge_distortion_search.md",
            ),
            limitations=(
                "Finite model only.",
                "Does not prove a theorem about all logics or all categories.",
            ),
        ),
        FormalClaim(
            identifier="claim.satisfaction_preservation.finite",
            title="Finite Satisfaction Preservation",
            statement=(
                "Within the implemented finite semantics, satisfaction preservation "
                "can be measured by checking whether satisfied source statements "
                "translate to satisfied target statements."
            ),
            scope=ClaimScope.FINITE_MODEL,
            verification_level=VerificationLevel.TESTED_BY_UNIT_TESTS,
            evidence=(
                "src/rigor/preservation.py",
                "src/rigor/preservation_theorem.py",
                "tests/test_rigor_preservation.py",
                "tests/test_rigor_preservation_theorem.py",
            ),
            limitations=(
                "Uses finite truth-value interpretations.",
                "Does not cover arbitrary model theory.",
            ),
        ),
        FormalClaim(
            identifier="claim.composition_preservation.finite",
            title="Finite Composition Preservation",
            statement=(
                "If two composable finite bridges preserve satisfaction under "
                "compatible interpretations, then their composite preserves satisfaction "
                "in the implemented finite model."
            ),
            scope=ClaimScope.FINITE_MODEL,
            verification_level=VerificationLevel.FINITE_PROOF,
            evidence=(
                "src/rigor/composition_preservation_theorem.py",
                "docs/composition_preservation_theorem.md",
                "tests/test_rigor_composition_preservation_theorem.py",
            ),
            limitations=(
                "Instance-level finite theorem.",
                "Compatibility of interpretations is assumed by the checker inputs.",
            ),
        ),
        FormalClaim(
            identifier="claim.model_search.no_counterexamples",
            title="No Generated Bridge-Distortion Counterexamples",
            statement=(
                "In the generated finite search space, no counterexamples were found "
                "to the implemented Bridge Distortion Theorem."
            ),
            scope=ClaimScope.GENERATED_SEARCH_SPACE,
            verification_level=VerificationLevel.STRESS_TESTED,
            evidence=(
                "src/rigor/search_report.py",
                "docs/model_search_report.md",
                "tests/test_rigor_search_report.py",
            ),
            limitations=(
                "Only applies to generated finite cases.",
                "Search space is finite and parameter-bound.",
            ),
        ),
        FormalClaim(
            identifier="claim.general_foundations",
            title="General Foundations Claim",
            statement=(
                "The finite Project Aleph-Omega framework may suggest patterns for "
                "studying translations between richer logical foundations."
            ),
            scope=ClaimScope.CONJECTURAL_GENERALIZATION,
            verification_level=VerificationLevel.CONJECTURAL,
            evidence=(
                "docs/rigor_track.md",
            ),
            limitations=(
                "Not proven.",
                "Should not be presented as a solved foundations theorem.",
                "Requires substantial formalization to generalize.",
            ),
        ),
    )

    return ClaimRegistry(claims=claims)


if __name__ == "__main__":
    registry = standard_claim_registry()

    print(registry.describe())
    print()

    for claim in registry.claims:
        print(claim.describe())
        print()
