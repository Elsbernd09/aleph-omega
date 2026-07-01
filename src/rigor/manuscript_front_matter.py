"""
Manuscript front matter for Project Aleph-Omega.

This module generates polished academic front matter:

- short abstract
- extended abstract
- keywords
- contribution list
- reviewer summary
- submission note
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class ManuscriptFrontMatter:
    """
    Front matter for the manuscript.
    """

    title: str
    short_abstract: str
    extended_abstract: str
    keywords: Tuple[str, ...]
    contributions: Tuple[str, ...]
    reviewer_summary: str
    submission_note: str

    def keyword_count(self) -> int:
        """
        Counts keywords.
        """

        return len(self.keywords)

    def contribution_count(self) -> int:
        """
        Counts contributions.
        """

        return len(self.contributions)

    def word_count(self) -> int:
        """
        Counts words in abstract-style fields.
        """

        text = " ".join(
            [
                self.short_abstract,
                self.extended_abstract,
                self.reviewer_summary,
                self.submission_note,
            ]
        )

        return len(text.split())

    def to_markdown(self) -> str:
        """
        Converts front matter to markdown.
        """

        lines = [
            f"# {self.title}",
            "",
            "## Short Abstract",
            "",
            self.short_abstract,
            "",
            "## Extended Abstract",
            "",
            self.extended_abstract,
            "",
            "## Keywords",
            "",
        ]

        for keyword in self.keywords:
            lines.append(f"- {keyword}")

        lines.extend(
            [
                "",
                "## Main Contributions",
                "",
            ]
        )

        for contribution in self.contributions:
            lines.append(f"- {contribution}")

        lines.extend(
            [
                "",
                "## Reviewer Summary",
                "",
                self.reviewer_summary,
                "",
                "## Submission Note",
                "",
                self.submission_note,
                "",
            ]
        )

        return "\n".join(lines)

    def describe(self) -> str:
        """
        Returns a readable front matter summary.
        """

        return (
            f"ManuscriptFrontMatter\n"
            f"Title: {self.title}\n"
            f"Keywords: {self.keyword_count()}\n"
            f"Contributions: {self.contribution_count()}\n"
            f"Words: {self.word_count()}"
        )


class ManuscriptFrontMatterBuilder:
    """
    Builds manuscript front matter.
    """

    def build(self) -> ManuscriptFrontMatter:
        """
        Builds standard front matter.
        """

        return ManuscriptFrontMatter(
            title=(
                "Project Aleph-Omega: A Finite Institution-Inspired Framework "
                "for Satisfaction Preservation and Quotient-Categorical Semantics"
            ),
            short_abstract=(
                "Project Aleph-Omega develops a finite computational and Lean-supported "
                "framework for studying when satisfaction is preserved under translations "
                "between formal systems. The project combines Python finite-model experiments "
                "with a Lean-checked abstract quotient-category core and concrete finite Lean examples."
            ),
            extended_abstract=(
                "This manuscript presents Project Aleph-Omega, a finite institution-inspired "
                "framework for studying satisfaction preservation under semantic translation. "
                "The Python layer implements finite logical universes, finite institution-like "
                "systems, bridge translations, finite morphism checkers, failure taxonomies, "
                "morphism equivalence, quotient morphism representatives, and a computational "
                "quotient-category analogue. The Lean layer formalizes the abstract core: formal "
                "systems, satisfaction-preserving morphisms, identity preservation, composition "
                "preservation, morphism equivalence, quotient morphisms, quotient composition, "
                "and a standalone quotient category-like structure. The Lean file also contains "
                "concrete finite systems, nontrivial preservation morphisms, a three-system "
                "preservation chain, and quotient-category integration for the concrete chain. "
                "The project does not claim a universal theorem about all institutions, logics, "
                "or categories. Its contribution is a finite, institution-inspired, proof-supported "
                "research architecture for investigating semantic preservation and failure boundaries."
            ),
            keywords=(
                "formal systems",
                "satisfaction preservation",
                "finite model semantics",
                "institution theory",
                "categorical logic",
                "quotient category",
                "Lean theorem proving",
                "formal verification",
                "semantic translation",
                "finite computation",
            ),
            contributions=(
                "A Python implementation of finite institution-like systems and satisfaction-preserving morphism checks.",
                "A failure taxonomy for finite semantic translation and preservation failures.",
                "A Lean-checked abstract core proving identity and composition preservation for satisfaction-preserving morphisms.",
                "A Lean-defined morphism equivalence relation and quotient morphism layer.",
                "A Lean-checked standalone quotient category-like structure with identity and associativity laws.",
                "Concrete finite Lean systems with positive satisfaction facts, negative satisfaction facts, nontrivial preservation morphisms, and a preservation chain.",
                "A documented Lean/Python correspondence layer separating machine-checked claims from computational analogues.",
                "A manuscript, theorem inventory, and figure appendix that explicitly distinguish claims, limitations, and future work.",
            ),
            reviewer_summary=(
                "For reviewers, the strongest part of the project is the Lean-checked formal core. "
                "The repository does not merely simulate a mathematical idea; it includes machine-checked "
                "definitions and theorems for satisfaction preservation, morphism equivalence, quotient "
                "composition, and a standalone quotient category-like structure. The Python layer should "
                "be read as a computational laboratory and correspondence analogue, not as a fully "
                "machine-verified implementation."
            ),
            submission_note=(
                "This manuscript should be submitted or presented as an independent finite formal-methods "
                "research artifact. It should not be framed as a solved open problem or as a replacement "
                "for institution theory. The correct framing is: a finite, institution-inspired, "
                "Lean-supported architecture for studying satisfaction preservation, semantic translation, "
                "quotient morphisms, and failure boundaries."
            ),
        )

    def write_markdown(
        self,
        front_matter: ManuscriptFrontMatter,
        path: str = "docs/manuscript_front_matter.md",
    ) -> Path:
        """
        Writes the front matter to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(front_matter.to_markdown())
        return output_path


if __name__ == "__main__":
    builder = ManuscriptFrontMatterBuilder()
    front_matter = builder.build()
    output_path = builder.write_markdown(front_matter)

    print(front_matter.describe())
    print(f"Wrote manuscript front matter to {output_path}")
