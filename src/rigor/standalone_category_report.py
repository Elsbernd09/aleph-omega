"""
Standalone category completion report for Project Aleph-Omega.

This module summarizes Phase 23: the Lean standalone quotient category structure.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class StandaloneCategoryClaim:
    """
    One Lean-supported standalone category claim.
    """

    name: str
    lean_artifact: str
    status: str
    meaning: str

    def describe(self) -> str:
        """
        Returns a readable claim summary.
        """

        return (
            f"StandaloneCategoryClaim\n"
            f"Name: {self.name}\n"
            f"Lean artifact: {self.lean_artifact}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class StandaloneCategoryCompletionReport:
    """
    Completion report for Phase 23.
    """

    title: str
    claims: Tuple[StandaloneCategoryClaim, ...]

    def claim_count(self) -> int:
        """
        Counts claims.
        """

        return len(self.claims)

    def lean_checked_claims(self) -> Tuple[StandaloneCategoryClaim, ...]:
        """
        Returns Lean-checked claims.
        """

        return tuple(claim for claim in self.claims if claim.status == "Lean-checked")

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"StandaloneCategoryCompletionReport\n"
            f"Title: {self.title}\n"
            f"Claims: {self.claim_count()}\n"
            f"Lean-checked claims: {len(self.lean_checked_claims())}"
        )


class StandaloneCategoryCompletionReportBuilder:
    """
    Builds the standalone category completion report.
    """

    def build(self) -> StandaloneCategoryCompletionReport:
        """
        Builds the standard report.
        """

        claims = (
            StandaloneCategoryClaim(
                name="Quotient composition operation",
                lean_artifact="quotientCompose",
                status="Lean-defined",
                meaning=(
                    "Composition is defined directly on quotient morphisms using "
                    "the previously proved quotient-composition well-definedness theorem."
                ),
            ),
            StandaloneCategoryClaim(
                name="Quotient left identity",
                lean_artifact="quotient_category_left_identity",
                status="Lean-checked",
                meaning="The quotient identity composed on the left acts as identity.",
            ),
            StandaloneCategoryClaim(
                name="Quotient right identity",
                lean_artifact="quotient_category_right_identity",
                status="Lean-checked",
                meaning="The quotient identity composed on the right acts as identity.",
            ),
            StandaloneCategoryClaim(
                name="Quotient associativity",
                lean_artifact="quotient_category_associativity",
                status="Lean-checked",
                meaning="Composition of quotient morphisms is associative.",
            ),
            StandaloneCategoryClaim(
                name="Standalone quotient category API",
                lean_artifact="QuotientHom / quotientId / quotientComp",
                status="Lean-defined",
                meaning=(
                    "The quotient-category core is exposed through readable API names."
                ),
            ),
            StandaloneCategoryClaim(
                name="API identity laws",
                lean_artifact="quotient_api_left_identity / quotient_api_right_identity",
                status="Lean-checked",
                meaning="The standalone API satisfies left and right identity laws.",
            ),
            StandaloneCategoryClaim(
                name="API associativity",
                lean_artifact="quotient_api_associativity",
                status="Lean-checked",
                meaning="The standalone API satisfies associativity.",
            ),
            StandaloneCategoryClaim(
                name="Standalone category structure",
                lean_artifact="StandaloneQuotientCategory",
                status="Lean-defined",
                meaning=(
                    "A custom Lean structure packages hom-types, identity, composition, "
                    "left identity, right identity, and associativity."
                ),
            ),
            StandaloneCategoryClaim(
                name="Aleph-Omega quotient category",
                lean_artifact="AlephOmegaQuotientCategory",
                status="Lean-defined",
                meaning=(
                    "The standalone category structure is instantiated with FormalSystem "
                    "objects and QuotientHom arrows."
                ),
            ),
            StandaloneCategoryClaim(
                name="Category operation identification",
                lean_artifact=(
                    "quotient_category_hom_is_quotient_hom / "
                    "quotient_category_id_is_quotient_id / "
                    "quotient_category_comp_is_quotient_comp"
                ),
                status="Lean-checked",
                meaning=(
                    "The packaged category structure agrees with the earlier quotient "
                    "hom, identity, and composition definitions."
                ),
            ),
        )

        return StandaloneCategoryCompletionReport(
            title="Standalone Quotient Category Completion Report",
            claims=claims,
        )

    def to_markdown(self, report: StandaloneCategoryCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Standalone Quotient Category Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 23 turns the quotient-category foundation into a standalone Lean category-like structure.",
            "",
            "This is not a Mathlib Category instance.",
            "",
            "It is a custom Lean structure that packages objects, hom-types, identity arrows, composition, and category laws.",
            "",
            "## Summary",
            "",
            f"- Claims indexed: {report.claim_count()}",
            f"- Lean-checked claims: {len(report.lean_checked_claims())}",
            "",
            "## Lean-Supported Claims",
            "",
        ]

        for index, claim in enumerate(report.claims, start=1):
            lines.extend(
                [
                    f"### {index}. {claim.name}",
                    "",
                    f"- Lean artifact: `{claim.lean_artifact}`",
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
                "The strongest careful claim after Phase 23 is:",
                "",
                "> Project Aleph-Omega has a Lean-defined standalone quotient category structure whose objects are formal systems and whose arrows are quotient homs of satisfaction-preserving morphisms modulo extensional equivalence. The structure includes Lean-checked identity and associativity laws.",
                "",
                "## Important Limitation",
                "",
                "This is not yet a Mathlib Category instance.",
                "",
                "It is a standalone category-like Lean structure.",
                "",
                "A future phase may attempt a full Mathlib integration, but that requires a Lake/Mathlib project setup.",
                "",
                "## Why This Matters",
                "",
                "This phase moves the project beyond computational modeling and into proof-assistant-checked mathematical structure.",
                "",
                "The project now has:",
                "",
                "- abstract formal systems",
                "- satisfaction-preserving morphisms",
                "- morphism equivalence",
                "- quotient morphisms",
                "- quotient composition",
                "- quotient identity laws",
                "- quotient associativity",
                "- a packaged standalone category-like structure",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: StandaloneCategoryCompletionReport,
        path: str = "docs/standalone_category_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = StandaloneCategoryCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote standalone category completion report to {output_path}")
