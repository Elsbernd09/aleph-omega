"""
Final research memo generator for Project Aleph-Omega.

This module creates a polished research-style memo summarizing the rigor track.
"""

from dataclasses import dataclass
from pathlib import Path

from src.rigor.architecture_map import ArchitectureMapBuilder
from src.rigor.research_abstract import ResearchAbstractBuilder
from src.rigor.theorem_inventory import TheoremInventoryBuilder
from src.rigor.verification_report import VerificationReportBuilder


@dataclass(frozen=True)
class FinalResearchMemo:
    """
    Final research memo artifact.
    """

    title: str
    body: str

    def section_count(self) -> int:
        """
        Counts markdown section headings.
        """

        return sum(1 for line in self.body.splitlines() if line.startswith("## "))

    def word_count(self) -> int:
        """
        Counts words in the memo.
        """

        return len(self.body.split())

    def to_markdown(self) -> str:
        """
        Converts the memo to markdown.
        """

        return f"# {self.title}\n\n{self.body}"

    def describe(self) -> str:
        """
        Returns a readable memo summary.
        """

        return (
            f"FinalResearchMemo\n"
            f"Title: {self.title}\n"
            f"Sections: {self.section_count()}\n"
            f"Words: {self.word_count()}"
        )


class FinalResearchMemoBuilder:
    """
    Builds the final research memo.
    """

    def build(self) -> FinalResearchMemo:
        """
        Builds the final memo from existing project artifact builders.
        """

        abstract = ResearchAbstractBuilder().build()
        architecture_map = ArchitectureMapBuilder().build()
        theorem_inventory = TheoremInventoryBuilder().build()
        verification_report = VerificationReportBuilder().build()

        body_lines = [
            "## Abstract",
            "",
            abstract.abstract,
            "",
            "## Project Purpose",
            "",
            "Project Aleph-Omega is a finite computational research framework for studying semantic bridges between small logical universes.",
            "",
            "The project does not claim to solve mathematical foundations. Its value is that it builds a disciplined finite laboratory where theorem-like claims can be implemented, tested, searched, audited, and carefully bounded.",
            "",
            "## Core Research Question",
            "",
            "The central question is:",
            "",
            "When meaning is translated from one finite logical universe into another, what is preserved, what is distorted, and how can those outcomes be measured?",
            "",
            "The project answers this question inside a finite model by defining universes, bridge morphisms, truth-value interpretations, satisfaction preservation, distortion, composition, model search, failure taxonomy, and verification records.",
            "",
            "## Architecture Summary",
            "",
            f"The rigor track currently contains {architecture_map.layer_count()} mapped architecture layers and {architecture_map.total_file_count()} mapped implementation or test files.",
            "",
            "The major layers are:",
            "",
        ]

        for layer in architecture_map.layers:
            body_lines.append(f"- {layer.name}: {layer.purpose}")

        body_lines.extend(
            [
                "",
                "## Theorem Inventory Summary",
                "",
                f"The theorem inventory currently records {theorem_inventory.item_count()} theorem-like claims.",
                "",
                f"Strongly verified finite or stress-tested items: {len(theorem_inventory.strongly_verified_items())}.",
                "",
                f"Conjectural items: {len(theorem_inventory.conjectural_items())}.",
                "",
                "The inventory is designed to prevent overclaiming by recording scope, verification level, evidence, and limitations for every major claim.",
                "",
                "## Model Search and Stress Testing",
                "",
                "The finite model-search layer generates small logical universes, bridge cases, and truth-value interpretations.",
                "",
                "It then measures preservation, distortion, and generated theorem behavior.",
                "",
                "The careful result is not that a universal theorem has been proved for all mathematics. The careful result is that the implemented theorem machinery has been tested against generated finite cases, and the search reports record where the claims survived and where semantic distortion appeared.",
                "",
                "## Failure Laboratory",
                "",
                "The failure laboratory extracts counterexample-like semantic failure cases from generated searches.",
                "",
                "These are not necessarily formal theorem counterexamples. Many are boundary cases where a theorem hypothesis fails, a bridge is partial, a translation is undefined, or a target statement is not satisfied.",
                "",
                "This layer makes the project stronger because it studies failure instead of hiding it.",
                "",
                "## Verification Interface",
                "",
                f"The verification layer currently records {verification_report.claim_count()} formal claims.",
                "",
                f"Strongly verified claims: {verification_report.strongly_verified_count()}.",
                "",
                f"Conjectural claims: {verification_report.conjectural_count()}.",
                "",
                f"Open proof obligations: {verification_report.open_obligation_count()}.",
                "",
                "This layer separates finite verified claims from conjectural generalizations and makes unfinished verification work explicit.",
                "",
                "## Main Contribution",
                "",
                "The main contribution of Project Aleph-Omega is a finite, code-backed research framework for studying preservation and distortion under semantic translation.",
                "",
                "It combines:",
                "",
                "- finite logical universes",
                "- bridge morphisms",
                "- semantic distortion analysis",
                "- satisfaction preservation",
                "- categorical composition checks",
                "- functorial semantics examples",
                "- generated finite model search",
                "- failure taxonomy",
                "- theorem boundary analysis",
                "- claim auditing",
                "- proof obligation tracking",
                "- exportable research artifacts",
                "",
                "## Correct Research Claim",
                "",
                "The strongest honest claim is:",
                "",
                "Project Aleph-Omega implements a finite computational laboratory for studying semantic preservation and distortion across generated finite bridge systems, with theorem-like claims recorded, tested, audited, and bounded by explicit limitations.",
                "",
                "It should not be described as a universal solution to mathematical foundations.",
                "",
                "It should not be described as a proof of general theorems about all logics, categories, topoi, or model theories.",
                "",
                "## Future Work",
                "",
                "The natural next steps are:",
                "",
                "1. formalize selected finite theorems in a proof assistant such as Lean",
                "2. extend generated search spaces while keeping computational limits explicit",
                "3. add richer truth-value structures and richer bridge types",
                "4. strengthen proof obligations into formal proof scripts where possible",
                "5. compare the finite framework to established ideas in institution theory, categorical logic, and model theory",
                "",
                "## Closing Summary",
                "",
                "Project Aleph-Omega is strongest when framed as a serious finite computational mathematics project.",
                "",
                "Its seriousness comes from discipline: precise scope, generated tests, failure classification, theorem-boundary analysis, audit records, and explicit limitations.",
                "",
            ]
        )

        return FinalResearchMemo(
            title="Project Aleph-Omega Final Research Memo",
            body="\n".join(body_lines),
        )

    def write_markdown(
        self,
        memo: FinalResearchMemo,
        path: str = "docs/final_research_memo.md",
    ) -> Path:
        """
        Writes the final memo to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(memo.to_markdown())
        return output_path


if __name__ == "__main__":
    builder = FinalResearchMemoBuilder()
    memo = builder.build()
    output_path = builder.write_markdown(memo)

    print(memo.describe())
    print(f"Wrote final research memo to {output_path}")
