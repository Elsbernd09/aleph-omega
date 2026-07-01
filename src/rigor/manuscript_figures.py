"""
Manuscript figures for Project Aleph-Omega.

This module generates text-based architecture diagrams for the academic
manuscript.

The diagrams are intentionally Markdown-friendly so they render clearly on
GitHub without requiring external image generation.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ManuscriptFigure:
    """
    One manuscript figure.
    """

    number: str
    title: str
    caption: str
    diagram: str

    def to_markdown(self) -> str:
        """
        Converts the figure to markdown.
        """

        return (
            f"## Figure {self.number}: {self.title}\n\n"
            f"```text\n{self.diagram}\n```\n\n"
            f"Caption: {self.caption}"
        )

    def describe(self) -> str:
        """
        Returns a readable figure summary.
        """

        return (
            f"ManuscriptFigure\n"
            f"Number: {self.number}\n"
            f"Title: {self.title}"
        )


@dataclass(frozen=True)
class ManuscriptFigureSet:
    """
    Set of manuscript figures.
    """

    title: str
    figures: Tuple[ManuscriptFigure, ...]

    def figure_count(self) -> int:
        """
        Counts figures.
        """

        return len(self.figures)

    def to_markdown(self) -> str:
        """
        Converts the figure set to markdown.
        """

        lines = [
            f"# {self.title}",
            "",
            "These figures summarize the architecture, theorem flow, Lean/Python correspondence, and quotient-category structure of Project Aleph-Omega.",
            "",
        ]

        for figure in self.figures:
            lines.append(figure.to_markdown())
            lines.append("")

        return "\n".join(lines)

    def describe(self) -> str:
        """
        Returns a readable figure-set summary.
        """

        return (
            f"ManuscriptFigureSet\n"
            f"Title: {self.title}\n"
            f"Figures: {self.figure_count()}"
        )


class ManuscriptFigureBuilder:
    """
    Builds manuscript figures.
    """

    def build(self) -> ManuscriptFigureSet:
        """
        Builds the standard manuscript figure set.
        """

        figures = (
            ManuscriptFigure(
                number="1",
                title="Project Architecture",
                caption=(
                    "Project Aleph-Omega has a Python finite-computation layer, a Lean formal core, "
                    "and a correspondence layer connecting the two."
                ),
                diagram=(
                    "Project Aleph-Omega\n"
                    "|\n"
                    "+-- Python finite computation layer\n"
                    "|   +-- finite logical universes\n"
                    "|   +-- finite institution-like systems\n"
                    "|   +-- finite morphism checkers\n"
                    "|   +-- failure taxonomy\n"
                    "|   +-- quotient morphism analogues\n"
                    "|   +-- quotient category analogue\n"
                    "|\n"
                    "+-- Lean formal core\n"
                    "|   +-- FormalSystem\n"
                    "|   +-- PreservationMorphism\n"
                    "|   +-- MorphismEquivalent\n"
                    "|   +-- QuotientMorphism\n"
                    "|   +-- quotientCompose\n"
                    "|   +-- AlephOmegaQuotientCategory\n"
                    "|\n"
                    "+-- Correspondence layer\n"
                    "    +-- artifact manifest\n"
                    "    +-- claim inventory\n"
                    "    +-- completion reports"
                ),
            ),
            ManuscriptFigure(
                number="2",
                title="Satisfaction Preservation Pattern",
                caption=(
                    "A preservation morphism translates sentences and maps models so that source "
                    "satisfaction implies target satisfaction."
                ),
                diagram=(
                    "Source system A                         Target system B\n"
                    "----------------                         ----------------\n"
                    "model m                                  model F.model(m)\n"
                    "sentence phi                             sentence F.translate(phi)\n"
                    "\n"
                    "A.Sat(m, phi)  --------------------->   B.Sat(F.model(m), F.translate(phi))\n"
                    "                  preservation"
                ),
            ),
            ManuscriptFigure(
                number="3",
                title="Lean Theorem Flow",
                caption=(
                    "The Lean formalization builds from satisfaction preservation to morphism equivalence, "
                    "quotient morphisms, quotient composition, and a standalone quotient category."
                ),
                diagram=(
                    "FormalSystem\n"
                    "   |\n"
                    "   v\n"
                    "PreservationMorphism\n"
                    "   |\n"
                    "   +--> identity_preserves_satisfaction\n"
                    "   +--> composition_preserves_satisfaction\n"
                    "   |\n"
                    "   v\n"
                    "MorphismEquivalent\n"
                    "   |\n"
                    "   +--> equivalence laws\n"
                    "   +--> composition respects equivalence\n"
                    "   |\n"
                    "   v\n"
                    "QuotientMorphism\n"
                    "   |\n"
                    "   +--> quotient composition well-defined\n"
                    "   +--> quotient identity laws\n"
                    "   +--> quotient associativity\n"
                    "   |\n"
                    "   v\n"
                    "AlephOmegaQuotientCategory"
                ),
            ),
            ManuscriptFigure(
                number="4",
                title="Concrete Lean Chain",
                caption=(
                    "The concrete Lean layer contains three finite systems connected by nontrivial "
                    "satisfaction-preserving morphisms."
                ),
                diagram=(
                    "TwoSystem                    RenamedTwoSystem                  ThirdTwoSystem\n"
                    "---------                    ----------------                  --------------\n"
                    "m0 satisfies p      --->     a satisfies alpha        --->      x satisfies gamma\n"
                    "m1 satisfies q      --->     b satisfies beta         --->      y satisfies delta\n"
                    "\n"
                    "twoToRenamedMorphism          renamedToThirdMorphism\n"
                    "\n"
                    "Composite:\n"
                    "TwoSystem --------------------------------------------------> ThirdTwoSystem\n"
                    "m0 maps to x, p maps to gamma\n"
                    "m1 maps to y, q maps to delta"
                ),
            ),
            ManuscriptFigure(
                number="5",
                title="Quotient Category Integration",
                caption=(
                    "Concrete preservation morphisms are lifted into quotient homs and composed inside "
                    "the standalone quotient category structure."
                ),
                diagram=(
                    "twoToRenamedMorphism          renamedToThirdMorphism\n"
                    "          |                              |\n"
                    "          v                              v\n"
                    "qTwoToRenamed                   qRenamedToThird\n"
                    "          \\                              /\n"
                    "           \\                            /\n"
                    "            v                          v\n"
                    "        quotientComp(qTwoToRenamed, qRenamedToThird)\n"
                    "                         |\n"
                    "                         v\n"
                    "                    qTwoToThird\n"
                    "\n"
                    "Lean theorem:\n"
                    "q_two_to_third_composition"
                ),
            ),
            ManuscriptFigure(
                number="6",
                title="Claim Boundary",
                caption=(
                    "The project separates Lean-checked claims, Python-tested claims, documented "
                    "correspondences, and explicit non-claims."
                ),
                diagram=(
                    "Claim status hierarchy\n"
                    "----------------------\n"
                    "Lean-checked theorem\n"
                    "   > Python-tested computational result\n"
                    "       > documented correspondence\n"
                    "           > manuscript explanation\n"
                    "               > conjectural future work\n"
                    "\n"
                    "Explicit non-claims:\n"
                    "- not a universal theorem about all institutions\n"
                    "- not a full Mathlib Category instance\n"
                    "- not full machine verification of Python implementation\n"
                    "- not a field-changing theorem yet"
                ),
            ),
        )

        return ManuscriptFigureSet(
            title="Project Aleph-Omega Manuscript Figures",
            figures=figures,
        )

    def write_markdown(
        self,
        figure_set: ManuscriptFigureSet,
        path: str = "docs/manuscript_figures.md",
    ) -> Path:
        """
        Writes the figure set to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(figure_set.to_markdown())
        return output_path


if __name__ == "__main__":
    builder = ManuscriptFigureBuilder()
    figure_set = builder.build()
    output_path = builder.write_markdown(figure_set)

    print(figure_set.describe())
    print(f"Wrote manuscript figures to {output_path}")
