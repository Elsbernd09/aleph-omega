"""
Lean/Python correspondence completion report for Project Aleph-Omega.

This module summarizes Phase 24, which connects the Lean formal core to the
Python computational implementation.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class CorrespondenceCompletionClaim:
    """
    One correspondence completion claim.
    """

    name: str
    lean_artifact: str
    python_artifact: str
    status: str
    limitation: str

    def describe(self) -> str:
        """
        Returns a readable claim.
        """

        return (
            f"CorrespondenceCompletionClaim\n"
            f"Name: {self.name}\n"
            f"Lean artifact: {self.lean_artifact}\n"
            f"Python artifact: {self.python_artifact}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class CorrespondenceCompletionReport:
    """
    Completion report for Phase 24.
    """

    title: str
    claims: Tuple[CorrespondenceCompletionClaim, ...]

    def claim_count(self) -> int:
        """
        Counts claims.
        """

        return len(self.claims)

    def completed_correspondences(self) -> Tuple[CorrespondenceCompletionClaim, ...]:
        """
        Returns completed correspondence claims.
        """

        return tuple(claim for claim in self.claims if "correspondence" in claim.status.lower())

    def describe(self) -> str:
        """
        Returns a readable report summary.
        """

        return (
            f"CorrespondenceCompletionReport\n"
            f"Title: {self.title}\n"
            f"Claims: {self.claim_count()}\n"
            f"Completed correspondences: {len(self.completed_correspondences())}"
        )


class CorrespondenceCompletionReportBuilder:
    """
    Builds the Phase 24 correspondence completion report.
    """

    def build(self) -> CorrespondenceCompletionReport:
        """
        Builds the standard report.
        """

        claims = (
            CorrespondenceCompletionClaim(
                name="Formal system correspondence",
                lean_artifact="FormalSystem",
                python_artifact="FiniteLogicalUniverse / FiniteInstitution",
                status="Documented correspondence",
                limitation=(
                    "Lean uses an abstract relation; Python uses finite data structures "
                    "and concrete interpretation logic."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Satisfaction relation correspondence",
                lean_artifact="FormalSystem.Sat",
                python_artifact="FiniteModel.satisfies",
                status="Documented correspondence",
                limitation=(
                    "Python satisfaction is computed, while Lean satisfaction is an "
                    "abstract proposition."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Preservation morphism correspondence",
                lean_artifact="PreservationMorphism",
                python_artifact="FiniteInstitutionMorphism",
                status="Documented correspondence",
                limitation=(
                    "Lean stores proof of preservation; Python checks finite witnesses."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Morphism equivalence correspondence",
                lean_artifact="MorphismEquivalent",
                python_artifact="PythonMorphismEquivalenceChecker",
                status="Implemented correspondence",
                limitation=(
                    "Python compares extensional signatures but does not machine-prove "
                    "equivalence laws."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Quotient morphism correspondence",
                lean_artifact="QuotientMorphism",
                python_artifact="PythonQuotientMorphism",
                status="Implemented correspondence",
                limitation=(
                    "Lean uses quotient types; Python stores representatives and signatures."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Quotient identity correspondence",
                lean_artifact="quotientIdentity / quotientId",
                python_artifact="PythonQuotientCategory.identity",
                status="Implemented correspondence",
                limitation=(
                    "Python constructs identity quotient representatives rather than a "
                    "proof-assistant quotient identity."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Quotient composition correspondence",
                lean_artifact="quotientCompose / quotientComp",
                python_artifact="PythonQuotientMorphismBuilder.compose",
                status="Implemented correspondence",
                limitation=(
                    "Lean proves well-definedness; Python computes representative composition."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Standalone quotient category correspondence",
                lean_artifact="AlephOmegaQuotientCategory",
                python_artifact="PythonQuotientCategory",
                status="Implemented correspondence",
                limitation=(
                    "Lean packages laws as proofs; Python checks laws on finite examples."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Failure boundary correspondence",
                lean_artifact="preservation_not_automatic",
                python_artifact="failure_taxonomy.py",
                status="Partial correspondence",
                limitation=(
                    "Lean proves a concrete BoolSystem counterexample; Python classifies "
                    "broader implementation-level failures."
                ),
            ),
            CorrespondenceCompletionClaim(
                name="Full implementation verification",
                lean_artifact="none",
                python_artifact="entire Python implementation",
                status="Not completed",
                limitation=(
                    "The full Python system is not machine-verified by Lean."
                ),
            ),
        )

        return CorrespondenceCompletionReport(
            title="Lean/Python Correspondence Completion Report",
            claims=claims,
        )

    def to_markdown(self, report: CorrespondenceCompletionReport) -> str:
        """
        Converts the report to markdown.
        """

        lines = [
            "# Lean/Python Correspondence Completion Report",
            "",
            "## Purpose",
            "",
            "Phase 24 completes the first formal correspondence layer between Project Aleph-Omega's Lean core and Python implementation.",
            "",
            "The goal is to clearly explain which Python artifacts correspond to which Lean artifacts.",
            "",
            "This avoids overclaiming while making the project more rigorous.",
            "",
            "## Summary",
            "",
            f"- Claims indexed: {report.claim_count()}",
            f"- Completed correspondence claims: {len(report.completed_correspondences())}",
            "",
            "## Correspondence Claims",
            "",
        ]

        for index, claim in enumerate(report.claims, start=1):
            lines.extend(
                [
                    f"### {index}. {claim.name}",
                    "",
                    f"- Lean artifact: `{claim.lean_artifact}`",
                    f"- Python artifact: `{claim.python_artifact}`",
                    f"- Status: {claim.status}",
                    "",
                    f"Limitation: {claim.limitation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Current Claim",
                "",
                "The strongest careful claim after Phase 24 is:",
                "",
                "> Project Aleph-Omega contains a Lean-checked abstract quotient-category core and a Python computational analogue for finite institution-like systems, with a documented correspondence layer connecting formal systems, satisfaction, preservation morphisms, morphism equivalence, quotient morphisms, quotient composition, and quotient category structure.",
                "",
                "## Important Limitation",
                "",
                "The Python implementation is not fully machine-verified by Lean.",
                "",
                "The Lean layer proves the abstract mathematical core.",
                "",
                "The Python layer implements computational analogues.",
                "",
                "The correspondence layer documents and tests the connection as a research artifact.",
                "",
                "## Next Serious Step",
                "",
                "The next research milestone should be one of:",
                "",
                "1. move concrete finite Python structures into Lean as finite examples,",
                "2. create a Lake/Mathlib project and attempt a real Category instance,",
                "3. write an academic paper-style exposition separating formal results from computational analogues.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: CorrespondenceCompletionReport,
        path: str = "docs/correspondence_completion_report.md",
    ) -> Path:
        """
        Writes the report to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = CorrespondenceCompletionReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote correspondence completion report to {output_path}")
