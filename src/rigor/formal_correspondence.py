"""
Formal correspondence layer for Project Aleph-Omega.

This module connects Python implementation artifacts to Lean formalization
artifacts.

The purpose is not to prove that the Python code is fully verified.

The purpose is to create a precise manifest showing which Python concepts
correspond to which Lean definitions and theorems.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class FormalCorrespondenceEntry:
    """
    One correspondence entry between Python and Lean artifacts.
    """

    concept: str
    python_artifact: str
    lean_artifact: str
    documentation_artifact: str
    status: str
    limitation: str

    def describe(self) -> str:
        """
        Returns a readable correspondence entry.
        """

        return (
            f"FormalCorrespondenceEntry\n"
            f"Concept: {self.concept}\n"
            f"Python artifact: {self.python_artifact}\n"
            f"Lean artifact: {self.lean_artifact}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class FormalCorrespondenceManifest:
    """
    Manifest connecting Python implementation to Lean formalization.
    """

    title: str
    entries: Tuple[FormalCorrespondenceEntry, ...]

    def entry_count(self) -> int:
        """
        Counts correspondence entries.
        """

        return len(self.entries)

    def lean_checked_entries(self) -> Tuple[FormalCorrespondenceEntry, ...]:
        """
        Returns entries with Lean-checked status.
        """

        return tuple(entry for entry in self.entries if "Lean-checked" in entry.status)

    def python_implemented_entries(self) -> Tuple[FormalCorrespondenceEntry, ...]:
        """
        Returns entries with Python implementation.
        """

        return tuple(entry for entry in self.entries if entry.python_artifact != "none")

    def describe(self) -> str:
        """
        Returns a readable manifest summary.
        """

        return (
            f"FormalCorrespondenceManifest\n"
            f"Title: {self.title}\n"
            f"Entries: {self.entry_count()}\n"
            f"Lean-checked entries: {len(self.lean_checked_entries())}\n"
            f"Python-implemented entries: {len(self.python_implemented_entries())}"
        )


class FormalCorrespondenceBuilder:
    """
    Builds the formal correspondence manifest.
    """

    def build(self) -> FormalCorrespondenceManifest:
        """
        Builds the standard correspondence manifest.
        """

        entries = (
            FormalCorrespondenceEntry(
                concept="Finite logical system",
                python_artifact="src/rigor/finite_universe.py",
                lean_artifact="FormalSystem",
                documentation_artifact="docs/lean_core_formalization.md",
                status="Python-implemented and Lean-defined",
                limitation=(
                    "The Lean FormalSystem is abstract and does not directly encode "
                    "all fields of FiniteLogicalUniverse."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Satisfaction relation",
                python_artifact="src/rigor/finite_institution.py",
                lean_artifact="FormalSystem.Sat",
                documentation_artifact="docs/finite_institution.md",
                status="Python-implemented and Lean-defined",
                limitation=(
                    "Python computes satisfaction through finite interpretations; "
                    "Lean abstracts satisfaction as a relation."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Satisfaction-preserving morphism",
                python_artifact="src/rigor/institution_morphism.py",
                lean_artifact="PreservationMorphism",
                documentation_artifact="docs/institution_morphism.md",
                status="Python-implemented and Lean-defined",
                limitation=(
                    "Python checks preservation over finite witnesses; Lean stores "
                    "preservation as a proof field."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Identity preservation",
                python_artifact="src/rigor/institution_satisfaction_theorem.py",
                lean_artifact="identity_preserves_satisfaction",
                documentation_artifact="docs/lean_formalization_index.md",
                status="Lean-checked prototype",
                limitation=(
                    "The Lean theorem applies to the abstract formal core, not the "
                    "entire Python implementation."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Composition preservation",
                python_artifact="src/rigor/institution_category.py",
                lean_artifact="composition_preserves_satisfaction",
                documentation_artifact="docs/lean_formalization_index.md",
                status="Lean-checked prototype",
                limitation=(
                    "The Lean theorem proves the abstract preservation pattern; "
                    "Python composition has additional implementation details."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Failure boundary",
                python_artifact="src/rigor/failure_taxonomy.py",
                lean_artifact="preservation_not_automatic",
                documentation_artifact="docs/lean_failure_boundary.md",
                status="Python-implemented taxonomy and Lean-checked counterexample",
                limitation=(
                    "Lean proves one concrete BoolSystem counterexample, not "
                    "completeness of the Python failure taxonomy."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Morphism equivalence",
                python_artifact="none",
                lean_artifact="MorphismEquivalent",
                documentation_artifact="docs/lean_morphism_equivalence.md",
                status="Lean-defined and Lean-checked laws",
                limitation=(
                    "The Python layer does not yet implement morphism equivalence "
                    "as a first-class object."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Quotient morphisms",
                python_artifact="none",
                lean_artifact="QuotientMorphism",
                documentation_artifact="docs/lean_setoid_quotient.md",
                status="Lean-defined",
                limitation=(
                    "The quotient hom-type currently exists only in Lean."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Quotient composition",
                python_artifact="none",
                lean_artifact="quotientCompose",
                documentation_artifact="docs/lean_quotient_compose_operation.md",
                status="Lean-defined and Lean-checked laws",
                limitation=(
                    "The quotient composition operation is not mirrored in Python."
                ),
            ),
            FormalCorrespondenceEntry(
                concept="Standalone quotient category",
                python_artifact="none",
                lean_artifact="AlephOmegaQuotientCategory",
                documentation_artifact="docs/standalone_category_completion_report.md",
                status="Lean-defined structure with Lean-checked laws",
                limitation=(
                    "This is a standalone Lean category-like structure, not a "
                    "Mathlib Category instance."
                ),
            ),
        )

        return FormalCorrespondenceManifest(
            title="Lean/Python Formal Correspondence Manifest",
            entries=entries,
        )

    def to_markdown(self, manifest: FormalCorrespondenceManifest) -> str:
        """
        Converts the manifest to markdown.
        """

        lines = [
            "# Lean/Python Formal Correspondence Manifest",
            "",
            "## Purpose",
            "",
            "This document connects the Project Aleph-Omega Python implementation to the Lean formalization core.",
            "",
            "The purpose is to avoid overclaiming.",
            "",
            "Lean proves the abstract theorem core.",
            "",
            "Python implements finite computational models.",
            "",
            "The correspondence layer explains how the two relate.",
            "",
            "## Summary",
            "",
            f"- Correspondence entries: {manifest.entry_count()}",
            f"- Lean-checked entries: {len(manifest.lean_checked_entries())}",
            f"- Python-implemented entries: {len(manifest.python_implemented_entries())}",
            "",
            "## Correspondence Entries",
            "",
        ]

        for index, entry in enumerate(manifest.entries, start=1):
            lines.extend(
                [
                    f"### {index}. {entry.concept}",
                    "",
                    f"- Python artifact: `{entry.python_artifact}`",
                    f"- Lean artifact: `{entry.lean_artifact}`",
                    f"- Documentation artifact: `{entry.documentation_artifact}`",
                    f"- Status: {entry.status}",
                    "",
                    f"Limitation: {entry.limitation}",
                    "",
                ]
            )

        lines.extend(
            [
                "## Strongest Correct Claim",
                "",
                "The strongest careful claim is:",
                "",
                "> Project Aleph-Omega contains a Python implementation of finite semantic systems and a Lean-checked abstract formal core. The correspondence manifest identifies which computational concepts correspond to which Lean definitions and theorems.",
                "",
                "## Important Limitation",
                "",
                "The Python implementation is not fully machine-verified.",
                "",
                "The Lean formalization proves the abstract mathematical core.",
                "",
                "The correspondence between Python and Lean is documented and tested as an artifact, but not yet itself formally verified.",
                "",
                "## Next Research Step",
                "",
                "The next serious step is to make this correspondence sharper by either:",
                "",
                "1. implementing Python-side morphism equivalence and quotient operations, or",
                "2. moving the finite Python structures into Lean as concrete finite examples.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        manifest: FormalCorrespondenceManifest,
        path: str = "docs/formal_correspondence_manifest.md",
    ) -> Path:
        """
        Writes the manifest to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(manifest))
        return output_path


if __name__ == "__main__":
    builder = FormalCorrespondenceBuilder()
    manifest = builder.build()
    output_path = builder.write_markdown(manifest)

    print(manifest.describe())
    print(f"Wrote formal correspondence manifest to {output_path}")
