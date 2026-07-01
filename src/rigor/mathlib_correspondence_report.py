"""
Mathlib correspondence report for Project Aleph-Omega.

This module compares the original standalone Lean formal core with the
experimental Mathlib quotient category prototype.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class MathlibCorrespondenceEntry:
    """
    One correspondence between standalone Lean and experimental Mathlib artifacts.
    """

    concept: str
    standalone_artifact: str
    mathlib_artifact: str
    correspondence: str
    status: str
    limitation: str

    def describe(self) -> str:
        return (
            f"MathlibCorrespondenceEntry\n"
            f"Concept: {self.concept}\n"
            f"Standalone: {self.standalone_artifact}\n"
            f"Mathlib: {self.mathlib_artifact}\n"
            f"Status: {self.status}"
        )


@dataclass(frozen=True)
class MathlibCorrespondenceReport:
    """
    Correspondence report between standalone Lean and Mathlib tracks.
    """

    title: str
    entries: Tuple[MathlibCorrespondenceEntry, ...]

    def entry_count(self) -> int:
        return len(self.entries)

    def strong_entries(self) -> Tuple[MathlibCorrespondenceEntry, ...]:
        return tuple(entry for entry in self.entries if "strong" in entry.status.lower())

    def partial_entries(self) -> Tuple[MathlibCorrespondenceEntry, ...]:
        return tuple(entry for entry in self.entries if "partial" in entry.status.lower())

    def describe(self) -> str:
        return (
            f"MathlibCorrespondenceReport\n"
            f"Title: {self.title}\n"
            f"Entries: {self.entry_count()}\n"
            f"Strong entries: {len(self.strong_entries())}\n"
            f"Partial entries: {len(self.partial_entries())}"
        )


class MathlibCorrespondenceReportBuilder:
    """
    Builds the standalone-to-Mathlib correspondence report.
    """

    def build(self) -> MathlibCorrespondenceReport:
        entries = (
            MathlibCorrespondenceEntry(
                concept="Formal system",
                standalone_artifact="FormalSystem in formal/lean/AlephOmegaCore.lean",
                mathlib_artifact="FormalSystem in FormalSystemCategory.lean",
                correspondence="Both define systems with models, sentences, and a satisfaction relation.",
                status="strong correspondence",
                limitation="They are separate Lean definitions, not definitionally identical.",
            ),
            MathlibCorrespondenceEntry(
                concept="Satisfaction-preserving morphism",
                standalone_artifact="PreservationMorphism",
                mathlib_artifact="PreservationMorphism",
                correspondence="Both use sentence translation, model map, and a preservation proof.",
                status="strong correspondence",
                limitation="They live in separate Lean files/projects.",
            ),
            MathlibCorrespondenceEntry(
                concept="Identity morphism",
                standalone_artifact="identityMorphism",
                mathlib_artifact="identityPreservation",
                correspondence="Both represent the satisfaction-preserving identity morphism.",
                status="strong correspondence",
                limitation="Naming and implementation details differ.",
            ),
            MathlibCorrespondenceEntry(
                concept="Composition",
                standalone_artifact="composeMorphism",
                mathlib_artifact="composePreservation",
                correspondence="Both compose sentence translation and model maps while preserving satisfaction.",
                status="strong correspondence",
                limitation="Composition is adapted to Mathlib category conventions in the Mathlib track.",
            ),
            MathlibCorrespondenceEntry(
                concept="Direct category",
                standalone_artifact="StandaloneQuotientCategory was quotient-focused, not direct raw morphism category.",
                mathlib_artifact="formalSystemCategory",
                correspondence="The Mathlib track adds a real direct Category instance absent from the original standalone layer.",
                status="new Mathlib strengthening",
                limitation="This is an added formalization, not a one-to-one migration.",
            ),
            MathlibCorrespondenceEntry(
                concept="Morphism equivalence",
                standalone_artifact="MorphismEquivalent",
                mathlib_artifact="PreservationEquivalent",
                correspondence="Both identify morphisms by translation and model-map behavior, ignoring proof-field differences.",
                status="strong correspondence",
                limitation="The Mathlib version is rebuilt for the experimental project.",
            ),
            MathlibCorrespondenceEntry(
                concept="Quotient morphism",
                standalone_artifact="QuotientMorphism / QuotientHom",
                mathlib_artifact="QuotientPreservationHom",
                correspondence="Both represent quotient classes of satisfaction-preserving morphisms.",
                status="strong correspondence",
                limitation="The Mathlib version uses the new FormalSystemCategory definitions.",
            ),
            MathlibCorrespondenceEntry(
                concept="Representative-independent composition",
                standalone_artifact="quotient_composition_well_defined",
                mathlib_artifact="compose_preservation_respects_equivalence",
                correspondence="Both prove that composition respects morphism equivalence.",
                status="strong correspondence",
                limitation="The proof names and exact theorem shapes differ.",
            ),
            MathlibCorrespondenceEntry(
                concept="Quotient category",
                standalone_artifact="AlephOmegaQuotientCategory",
                mathlib_artifact="quotientFormalSystemCategory",
                correspondence="Both package quotient homs, identity, composition, and category laws.",
                status="strong conceptual correspondence",
                limitation="The Mathlib prototype uses a wrapper object type to avoid category-instance conflicts.",
            ),
            MathlibCorrespondenceEntry(
                concept="Concrete finite examples",
                standalone_artifact="TwoSystem / RenamedTwoSystem / ThirdTwoSystem",
                mathlib_artifact="BoolFormalSystem / QuotientBoolFormalSystem",
                correspondence="Both contain finite concrete examples, but the examples are not the same yet.",
                status="partial correspondence",
                limitation="Future work should port the three-system concrete chain into the Mathlib project.",
            ),
            MathlibCorrespondenceEntry(
                concept="CI verification",
                standalone_artifact="./scripts/check_formal_stack.sh",
                mathlib_artifact="./scripts/check_mathlib_scaffold.sh",
                correspondence="Both tracks have local verification commands.",
                status="partial correspondence",
                limitation="The Mathlib scaffold is not yet integrated into the main GitHub Actions formal-stack workflow.",
            ),
        )

        return MathlibCorrespondenceReport(
            title="Project Aleph-Omega Standalone-to-Mathlib Correspondence Report",
            entries=entries,
        )

    def to_markdown(self, report: MathlibCorrespondenceReport) -> str:
        lines = [
            "# Project Aleph-Omega Standalone-to-Mathlib Correspondence Report",
            "",
            "## Purpose",
            "",
            "This report explains how the original standalone Lean formal core corresponds to the experimental Mathlib quotient category prototype.",
            "",
            "The project now has two formal tracks:",
            "",
            "1. the original standalone Lean core,",
            "2. the experimental Mathlib category-theory track.",
            "",
            "## Summary",
            "",
            f"- Correspondence entries: {report.entry_count()}",
            f"- Strong correspondence entries: {len(report.strong_entries())}",
            f"- Partial correspondence entries: {len(report.partial_entries())}",
            "",
            "## Correspondence Table",
            "",
            "| Concept | Standalone artifact | Mathlib artifact | Correspondence | Status | Limitation |",
            "|---|---|---|---|---|---|",
        ]

        for entry in report.entries:
            lines.append(
                f"| {entry.concept} | `{entry.standalone_artifact}` | `{entry.mathlib_artifact}` | {entry.correspondence} | {entry.status} | {entry.limitation} |"
            )

        lines.extend(
            [
                "",
                "## Strongest Current Correspondence Claim",
                "",
                "> Project Aleph-Omega now has a documented correspondence between its original standalone Lean quotient-category core and its experimental Mathlib quotient category prototype.",
                "",
                "## Important Boundary",
                "",
                "The two tracks are not yet definitionally unified.",
                "",
                "The Mathlib track is a reconstruction and strengthening of the standalone ideas inside Mathlib infrastructure.",
                "",
                "## Next Serious Step",
                "",
                "The next phase should port the concrete three-system Lean chain into the experimental Mathlib project, so the Mathlib track has the same concrete example strength as the standalone core.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        report: MathlibCorrespondenceReport,
        path: str = "docs/mathlib_correspondence_report.md",
    ) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(report))
        return output_path


if __name__ == "__main__":
    builder = MathlibCorrespondenceReportBuilder()
    report = builder.build()
    output_path = builder.write_markdown(report)

    print(report.describe())
    print(f"Wrote Mathlib correspondence report to {output_path}")
