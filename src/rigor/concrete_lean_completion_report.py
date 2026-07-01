"""
Concrete Lean structures completion report for Project Aleph-Omega.

This module summarizes Phase 25, which moves concrete finite structures directly
into the Lean formalization.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ConcreteLeanClaim:
    """
    One concrete Lean-supported claim.
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
            f"ConcreteLeanClaim\n"
            f"Name: {self.name}\n"
            f"Lean artifact: {self.lean_artifact}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class ConcreteLeanCompletionReport:
    """
    Completion report for Phase 25.
    """

    title: str
    claims: Tuple[ConcreteLeanClaim, ...]

    def claim_count(self) -> int:
        """
        Counts claims.
        """

        return len(self.claims)

    def lean_checked_claims(self) -> Tuple[ConcreteLeanClaim, ...]:
        """
        Returns Lean-checked claims.
        """

        return tuple(claim for claim in self.claims if "Lean-checked" in claim.status)

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"ConcreteLeanCompletionReport\n"
            f"Title: {self.title}\n"
            f"Claims: {self.claim_count()}\n"
            f"Lean-checked claims: {len(self.lean_checked_claims())}"
        )


class ConcreteLeanCompletionReportBuilder:
    """
    Builds the Phase 25 concrete Lean completion report.
    """

    def build(self) -> ConcreteLeanCompletionReport:
        """
        Builds the standard report.
        """

        claims = (
            ConcreteLeanClaim(
                name="Two-model finite system",
                lean_artifact="TwoSystem",
                status="Lean-defined",
                meaning=(
                    "A concrete finite formal system with two models and two sentences "
                    "is defined directly in Lean."
                ),
            ),
            ConcreteLeanClaim(
                name="Two-system positive satisfaction facts",
                lean_artifact="two_m0_satisfies_p / two_m1_satisfies_q",
                status="Lean-checked",
                meaning="Lean proves the positive satisfaction judgements in TwoSystem.",
            ),
            ConcreteLeanClaim(
                name="Two-system negative satisfaction facts",
                lean_artifact="two_m0_not_satisfy_q / two_m1_not_satisfy_p",
                status="Lean-checked",
                meaning="Lean proves the negative satisfaction judgements in TwoSystem.",
            ),
            ConcreteLeanClaim(
                name="Two-system failure boundary",
                lean_artifact="two_swap_translation_not_preserving",
                status="Lean-checked",
                meaning=(
                    "Lean proves a concrete sentence-swap translation does not preserve "
                    "satisfaction."
                ),
            ),
            ConcreteLeanClaim(
                name="Renamed finite system",
                lean_artifact="RenamedTwoSystem",
                status="Lean-defined",
                meaning="A second concrete finite formal system is defined in Lean.",
            ),
            ConcreteLeanClaim(
                name="Nontrivial preservation morphism",
                lean_artifact="twoToRenamedMorphism / two_to_renamed_preserves",
                status="Lean-checked",
                meaning=(
                    "Lean proves a non-identity morphism from TwoSystem to "
                    "RenamedTwoSystem preserves satisfaction."
                ),
            ),
            ConcreteLeanClaim(
                name="Third finite system",
                lean_artifact="ThirdTwoSystem",
                status="Lean-defined",
                meaning="A third concrete finite formal system is defined in Lean.",
            ),
            ConcreteLeanClaim(
                name="Second nontrivial preservation morphism",
                lean_artifact="renamedToThirdMorphism / renamed_to_third_preserves",
                status="Lean-checked",
                meaning=(
                    "Lean proves a non-identity morphism from RenamedTwoSystem to "
                    "ThirdTwoSystem preserves satisfaction."
                ),
            ),
            ConcreteLeanClaim(
                name="Nontrivial preservation chain",
                lean_artifact="twoToThirdComposite / two_to_third_composite_preserves",
                status="Lean-checked",
                meaning=(
                    "Lean proves the composed chain from TwoSystem to ThirdTwoSystem "
                    "preserves satisfaction."
                ),
            ),
            ConcreteLeanClaim(
                name="Concrete quotient chain",
                lean_artifact="qTwoToRenamed / qRenamedToThird / qTwoToThird",
                status="Lean-defined",
                meaning=(
                    "The concrete preservation chain is lifted into quotient homs."
                ),
            ),
            ConcreteLeanClaim(
                name="Quotient-category integration",
                lean_artifact="q_two_to_third_composition / quotient_category_composes_concrete_chain",
                status="Lean-checked",
                meaning=(
                    "Lean proves quotient composition matches the concrete preservation "
                    "chain composite."
                ),
            ),
        )

        return ConcreteLeanCompletionReport(
            title="Concrete Lean Structures Completion Report",
            claims=claims,
        )

    def to_markdown(self, report: ConcreteLeanCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Concrete Lean Structures Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 25 moves Project Aleph-Omega beyond abstract Lean definitions by adding concrete finite systems directly inside the Lean formalization.",
            "",
            "The phase demonstrates that the abstract satisfaction-preservation and quotient-category machinery applies to explicit finite examples.",
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
                "The strongest careful claim after Phase 25 is:",
                "",
                "> Project Aleph-Omega contains a Lean-checked concrete finite preservation pipeline across three explicit formal systems, including nontrivial preservation morphisms, a nontrivial composition chain, and integration of that chain into the standalone quotient-category structure.",
                "",
                "## Why This Matters",
                "",
                "This phase closes an important gap between abstract formalization and concrete examples.",
                "",
                "The project now has:",
                "",
                "- abstract Lean theorem core",
                "- standalone Lean quotient-category structure",
                "- concrete finite Lean systems",
                "- nontrivial Lean preservation morphisms",
                "- Lean-checked failure boundaries",
                "- Lean-checked quotient-category integration for concrete examples",
                "",
                "## Important Limitation",
                "",
                "The concrete systems are still small finite examples.",
                "",
                "They do not prove new results about all institutions or all logics.",
                "",
                "They do show that the formal system is executable as real Lean mathematics rather than only a conceptual description.",
                "",
                "## Next Serious Step",
                "",
                "The next milestone should be either:",
                "",
                "1. build a Lake/Mathlib project and attempt a real Category instance,",
                "2. write a full paper-style research manuscript, or",
                "3. create a finite-model-to-Lean export plan for generating Lean examples from Python data.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: ConcreteLeanCompletionReport,
        path: str = "docs/concrete_lean_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = ConcreteLeanCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote concrete Lean completion report to {output_path}")
