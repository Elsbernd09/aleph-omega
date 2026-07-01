"""
Quotient category completion report for Project Aleph-Omega.

This module summarizes the Lean quotient-category strengthening work completed
in Phase 22.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LeanQuotientClaim:
    """
    One Lean-supported quotient-category claim.
    """

    name: str
    lean_theorem: str
    status: str
    meaning: str

    def describe(self) -> str:
        """
        Returns a readable claim summary.
        """

        return (
            f"LeanQuotientClaim\n"
            f"Name: {self.name}\n"
            f"Lean theorem: {self.lean_theorem}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class QuotientCategoryCompletionReport:
    """
    Completion report for Phase 22.
    """

    title: str
    claims: Tuple[LeanQuotientClaim, ...]

    def claim_count(self) -> int:
        """
        Counts claims.
        """

        return len(self.claims)

    def machine_checked_claims(self) -> Tuple[LeanQuotientClaim, ...]:
        """
        Returns machine-checked claims.
        """

        return tuple(claim for claim in self.claims if claim.status == "Lean-checked prototype")

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"QuotientCategoryCompletionReport\n"
            f"Title: {self.title}\n"
            f"Claims: {self.claim_count()}\n"
            f"Machine-checked prototype claims: {len(self.machine_checked_claims())}"
        )


class QuotientCategoryCompletionReportBuilder:
    """
    Builds the quotient category completion report.
    """

    def build(self) -> QuotientCategoryCompletionReport:
        """
        Builds the standard report.
        """

        claims = (
            LeanQuotientClaim(
                name="Morphism equivalence",
                lean_theorem="MorphismEquivalent",
                status="Lean-defined",
                meaning=(
                    "Two preservation morphisms are equivalent when they have "
                    "the same sentence translation and model map."
                ),
            ),
            LeanQuotientClaim(
                name="Equivalence relation laws",
                lean_theorem="morphism_equiv_refl / morphism_equiv_symm / morphism_equiv_trans",
                status="Lean-checked prototype",
                meaning="Morphism equivalence is reflexive, symmetric, and transitive.",
            ),
            LeanQuotientClaim(
                name="Identity laws up to equivalence",
                lean_theorem="left_identity_equivalent / right_identity_equivalent",
                status="Lean-checked prototype",
                meaning="Identity morphisms behave correctly up to extensional equivalence.",
            ),
            LeanQuotientClaim(
                name="Associativity up to equivalence",
                lean_theorem="associativity_equivalent",
                status="Lean-checked prototype",
                meaning="Morphism composition is associative up to extensional equivalence.",
            ),
            LeanQuotientClaim(
                name="Composition respects equivalence",
                lean_theorem="compose_respects_morphism_equivalence",
                status="Lean-checked prototype",
                meaning="Equivalent representatives produce equivalent composites.",
            ),
            LeanQuotientClaim(
                name="Setoid of preservation morphisms",
                lean_theorem="morphismSetoid",
                status="Lean-defined",
                meaning="Preservation morphisms are packaged with extensional equivalence as a Setoid.",
            ),
            LeanQuotientClaim(
                name="Quotient hom-type",
                lean_theorem="QuotientMorphism",
                status="Lean-defined",
                meaning="Arrows are represented as equivalence classes of preservation morphisms.",
            ),
            LeanQuotientClaim(
                name="Equivalent morphisms share quotient class",
                lean_theorem="equivalent_morphisms_same_quotient",
                status="Lean-checked prototype",
                meaning="Equivalent preservation morphisms determine the same quotient arrow.",
            ),
            LeanQuotientClaim(
                name="Quotient composition well-definedness",
                lean_theorem="quotient_composition_well_defined",
                status="Lean-checked prototype",
                meaning="Composition of quotient arrows is independent of representative choice.",
            ),
            LeanQuotientClaim(
                name="Quotient identity laws",
                lean_theorem="quotient_left_identity / quotient_right_identity",
                status="Lean-checked prototype",
                meaning="Identity laws hold at the quotient-class level.",
            ),
            LeanQuotientClaim(
                name="Quotient associativity",
                lean_theorem="quotient_associativity",
                status="Lean-checked prototype",
                meaning="Associativity holds at the quotient-class level.",
            ),
        )

        return QuotientCategoryCompletionReport(
            title="Quotient Category Completion Report",
            claims=claims,
        )

    def to_markdown(self, report: QuotientCategoryCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Quotient Category Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 22 strengthens the Project Aleph-Omega Lean formalization from category-style laws to a quotient-category foundation.",
            "",
            "The key idea is that preservation morphisms should be identified extensionally when they have the same sentence translation and the same model map.",
            "",
            "## Summary",
            "",
            f"- Claims indexed: {report.claim_count()}",
            f"- Machine-checked prototype claims: {len(report.machine_checked_claims())}",
            "",
            "## Lean-Supported Claims",
            "",
        ]

        for index, claim in enumerate(report.claims, start=1):
            lines.extend(
                [
                    f"### {index}. {claim.name}",
                    "",
                    f"- Lean theorem or definition: `{claim.lean_theorem}`",
                    f"- Status: {claim.status}",
                    "",
                    claim.meaning,
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Current Claim",
                "",
                "The strongest careful claim after Phase 22 is:",
                "",
                "> Project Aleph-Omega has a Lean-checked quotient-category foundation for satisfaction-preserving morphisms modulo extensional equivalence, including equivalence laws, identity laws, associativity, Setoid construction, quotient hom-types, and quotient composition well-definedness.",
                "",
                "## Important Limitation",
                "",
                "This is still not a complete Mathlib Category instance.",
                "",
                "It is a Lean-checked quotient-category foundation.",
                "",
                "The next formal milestone would be to either:",
                "",
                "1. define a standalone quotient category structure in Lean, or",
                "2. integrate with Mathlib's Category typeclass.",
                "",
                "## Why This Matters",
                "",
                "This work is significantly stronger than a normal programming project because it contains proof-assistant-checked mathematical structure.",
                "",
                "It also avoids overclaiming by separating:",
                "",
                "- Lean-checked prototype claims",
                "- Python-tested computational claims",
                "- documentary or conjectural claims",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: QuotientCategoryCompletionReport,
        path: str = "docs/quotient_category_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = QuotientCategoryCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote quotient category completion report to {output_path}")
