"""
Public verification status generator for Project Aleph-Omega.

This module generates a reviewer-facing verification status page explaining what
is Lean-checked, Python-tested, CI-checked, and explicitly not claimed.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class VerificationItem:
    """
    One verification-status item.
    """

    name: str
    status: str
    evidence: str
    limitation: str

    def describe(self) -> str:
        """
        Returns a readable item summary.
        """

        return (
            f"VerificationItem\n"
            f"Name: {self.name}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class PublicVerificationStatus:
    """
    Public verification status page.
    """

    title: str
    items: Tuple[VerificationItem, ...]

    def item_count(self) -> int:
        """
        Counts verification items.
        """

        return len(self.items)

    def lean_checked_items(self) -> Tuple[VerificationItem, ...]:
        """
        Returns Lean-checked items.
        """

        return tuple(item for item in self.items if "Lean-checked" in item.status)

    def python_tested_items(self) -> Tuple[VerificationItem, ...]:
        """
        Returns Python-tested items.
        """

        return tuple(item for item in self.items if "Python-tested" in item.status)

    def ci_checked_items(self) -> Tuple[VerificationItem, ...]:
        """
        Returns CI-checked items.
        """

        return tuple(item for item in self.items if "CI-checked" in item.status)

    def describe(self) -> str:
        """
        Returns a readable status summary.
        """

        return (
            f"PublicVerificationStatus\n"
            f"Title: {self.title}\n"
            f"Items: {self.item_count()}\n"
            f"Lean-checked: {len(self.lean_checked_items())}\n"
            f"Python-tested: {len(self.python_tested_items())}\n"
            f"CI-checked: {len(self.ci_checked_items())}"
        )


class PublicVerificationStatusBuilder:
    """
    Builds the public verification status page.
    """

    def build(self) -> PublicVerificationStatus:
        """
        Builds the standard verification status page.
        """

        items = (
            VerificationItem(
                name="Primary Lean formalization",
                status="Lean-checked",
                evidence="formal/lean/AlephOmegaCore.lean and ./scripts/check_lean.sh",
                limitation="Checks the standalone Lean formalization, not every Python implementation detail.",
            ),
            VerificationItem(
                name="Satisfaction preservation under identity",
                status="Lean-checked",
                evidence="identity_preserves_satisfaction",
                limitation="Applies to the Lean FormalSystem abstraction.",
            ),
            VerificationItem(
                name="Satisfaction preservation under composition",
                status="Lean-checked",
                evidence="composition_preserves_satisfaction",
                limitation="Applies to Lean PreservationMorphism objects.",
            ),
            VerificationItem(
                name="Morphism equivalence laws",
                status="Lean-checked",
                evidence="morphism_equiv_refl / morphism_equiv_symm / morphism_equiv_trans",
                limitation="Uses extensional equality of translation and model maps.",
            ),
            VerificationItem(
                name="Quotient morphism composition",
                status="Lean-checked",
                evidence="quotient_composition_well_defined and quotientComp",
                limitation="Standalone quotient layer, not yet Mathlib Category.",
            ),
            VerificationItem(
                name="Standalone quotient-category structure",
                status="Lean-checked",
                evidence="AlephOmegaQuotientCategory",
                limitation="Custom Lean structure, not a Mathlib Category instance.",
            ),
            VerificationItem(
                name="Concrete finite preservation chain",
                status="Lean-checked",
                evidence="TwoSystem, RenamedTwoSystem, ThirdTwoSystem, twoToThirdComposite",
                limitation="Concrete finite example, not universal theorem.",
            ),
            VerificationItem(
                name="Python finite semantic laboratory",
                status="Python-tested",
                evidence="src/rigor/ and python3 -m pytest",
                limitation="Computational analogue, not proof-assistant verification.",
            ),
            VerificationItem(
                name="Lake project build",
                status="Locally checked and CI-checked",
                evidence="formal/aleph_omega_lake/ and ./scripts/check_lake.sh",
                limitation="Packages the standalone Lean core; Mathlib integration is future work.",
            ),
            VerificationItem(
                name="Full formal stack",
                status="Locally checked and CI-checked",
                evidence="./scripts/check_formal_stack.sh and .github/workflows/formal-stack.yml",
                limitation="CI success means reproducibility of the stated stack, not universal mathematical generality.",
            ),
            VerificationItem(
                name="Public documentation package",
                status="Python-tested",
                evidence="README.md, docs/quickstart.md, docs/public_release_index.md, and documentation tests",
                limitation="Documentation supports review, but the authoritative proofs are in Lean.",
            ),
            VerificationItem(
                name="Universal institution theorem",
                status="Explicitly not claimed",
                evidence="README.md and docs/manuscript_theorem_inventory.md",
                limitation="The project does not prove a theorem about all institutions, all logics, or all categories.",
            ),
        )

        return PublicVerificationStatus(
            title="Project Aleph-Omega Verification Status",
            items=items,
        )

    def to_markdown(self, status: PublicVerificationStatus) -> str:
        """
        Converts verification status to markdown.
        """

        lines = [
            "# Project Aleph-Omega Verification Status",
            "",
            "## Purpose",
            "",
            "This page explains what parts of Project Aleph-Omega are Lean-checked, Python-tested, CI-checked, and explicitly not claimed.",
            "",
            "## Summary",
            "",
            f"- Verification items: {status.item_count()}",
            f"- Lean-checked items: {len(status.lean_checked_items())}",
            f"- Python-tested items: {len(status.python_tested_items())}",
            f"- CI-checked items: {len(status.ci_checked_items())}",
            "",
            "## Verification Table",
            "",
            "| Item | Status | Evidence | Limitation |",
            "|---|---|---|---|",
        ]

        for item in status.items:
            lines.append(
                f"| {item.name} | {item.status} | `{item.evidence}` | {item.limitation} |"
            )

        lines.extend(
            [
                "",
                "## Main Verification Command",
                "",
                "Run:",
                "",
                "```bash",
                "./scripts/check_formal_stack.sh",
                "```",
                "",
                "Expected final output:",
                "",
                "```text",
                "Aleph-Omega formal stack verified successfully.",
                "```",
                "",
                "## Strongest Careful Verification Claim",
                "",
                "> Project Aleph-Omega has a reproducible formal stack containing a Lean-checked abstract core, concrete finite Lean examples, a Lake build scaffold, Python-tested finite computational analogues, and GitHub Actions CI.",
                "",
                "## Boundary",
                "",
                "This does not mean Project Aleph-Omega proves a universal theorem about all institutions, all logics, or all categories.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        status: PublicVerificationStatus,
        path: str = "docs/verification_status.md",
    ) -> Path:
        """
        Writes the verification status page to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(status))
        return output_path


if __name__ == "__main__":
    builder = PublicVerificationStatusBuilder()
    status = builder.build()
    output_path = builder.write_markdown(status)

    print(status.describe())
    print(f"Wrote verification status to {output_path}")
