"""
Lean formalization plan for Project Aleph-Omega.

This module generates a formalization roadmap for moving selected finite
Project Aleph-Omega results into Lean.

The goal is to identify a small, realistic theorem target rather than trying to
formalize the entire project at once.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LeanFormalizationTarget:
    """
    One Lean formalization target.
    """

    name: str
    mathematical_statement: str
    difficulty: str
    priority: int
    required_definitions: Tuple[str, ...]
    expected_output: str

    def describe(self) -> str:
        """
        Returns a readable Lean target.
        """

        return (
            f"LeanFormalizationTarget\n"
            f"Name: {self.name}\n"
            f"Difficulty: {self.difficulty}\n"
            f"Priority: {self.priority}\n"
            f"Expected output: {self.expected_output}"
        )


@dataclass(frozen=True)
class LeanFormalizationPlan:
    """
    Lean formalization plan.
    """

    targets: Tuple[LeanFormalizationTarget, ...]

    def target_count(self) -> int:
        """
        Counts formalization targets.
        """

        return len(self.targets)

    def highest_priority_targets(self) -> Tuple[LeanFormalizationTarget, ...]:
        """
        Returns targets with priority 1.
        """

        return tuple(target for target in self.targets if target.priority == 1)

    def describe(self) -> str:
        """
        Returns a readable plan summary.
        """

        return (
            f"LeanFormalizationPlan\n"
            f"Targets: {self.target_count()}\n"
            f"Highest priority targets: {len(self.highest_priority_targets())}"
        )


class LeanFormalizationPlanBuilder:
    """
    Builds the standard Lean formalization plan.
    """

    def build(self) -> LeanFormalizationPlan:
        """
        Builds the Lean plan.
        """

        targets = (
            LeanFormalizationTarget(
                name="Finite Satisfaction Predicate",
                mathematical_statement=(
                    "Define finite models, finite sentences, and a satisfaction "
                    "predicate Sat : Model -> Sentence -> Prop."
                ),
                difficulty="introductory",
                priority=1,
                required_definitions=(
                    "Finite type of sentences",
                    "Finite type of models",
                    "Satisfaction predicate",
                ),
                expected_output="Lean definitions compiling without theorem burden.",
            ),
            LeanFormalizationTarget(
                name="Satisfaction-Preserving Morphism",
                mathematical_statement=(
                    "Define a morphism as a sentence translation together with a "
                    "model pairing such that source satisfaction implies target "
                    "satisfaction of translated sentences."
                ),
                difficulty="moderate",
                priority=1,
                required_definitions=(
                    "Source finite system",
                    "Target finite system",
                    "Sentence translation",
                    "Model pairing",
                    "Preservation predicate",
                ),
                expected_output="Lean definition of satisfaction-preserving morphism.",
            ),
            LeanFormalizationTarget(
                name="Identity Preserves Satisfaction",
                mathematical_statement=(
                    "For every finite system, the identity sentence translation "
                    "and identity model pairing preserve satisfaction."
                ),
                difficulty="moderate",
                priority=1,
                required_definitions=(
                    "Identity sentence translation",
                    "Identity model pairing",
                    "Preservation predicate",
                ),
                expected_output="Lean theorem: identity_preserves_satisfaction.",
            ),
            LeanFormalizationTarget(
                name="Composition Preserves Satisfaction",
                mathematical_statement=(
                    "If F preserves satisfaction and G preserves satisfaction, "
                    "then G composed with F preserves satisfaction."
                ),
                difficulty="advanced",
                priority=2,
                required_definitions=(
                    "Composable morphisms",
                    "Composition of sentence translations",
                    "Composition of model pairings",
                    "Preservation predicate",
                ),
                expected_output="Lean theorem: composition_preserves_satisfaction.",
            ),
            LeanFormalizationTarget(
                name="Preservation Morphisms Form a Category",
                mathematical_statement=(
                    "Finite systems with satisfaction-preserving morphisms form "
                    "a category-like structure with identity and composition."
                ),
                difficulty="advanced",
                priority=3,
                required_definitions=(
                    "Objects",
                    "Morphisms",
                    "Identity",
                    "Composition",
                    "Identity laws",
                    "Associativity law",
                ),
                expected_output="Lean category-style theorem or structure.",
            ),
        )

        return LeanFormalizationPlan(targets=targets)

    def to_markdown(self, plan: LeanFormalizationPlan) -> str:
        """
        Converts the Lean plan to markdown.
        """

        lines = [
            "# Lean Formalization Plan",
            "",
            "## Purpose",
            "",
            "This document identifies the first realistic Lean formalization targets for Project Aleph-Omega.",
            "",
            "The goal is not to formalize the entire codebase at once.",
            "",
            "The goal is to formalize a small mathematical core:",
            "",
            "1. finite satisfaction",
            "2. satisfaction-preserving morphisms",
            "3. identity preservation",
            "4. composition preservation",
            "5. category-like structure",
            "",
            "## Summary",
            "",
            f"- Formalization targets: {plan.target_count()}",
            f"- Highest priority targets: {len(plan.highest_priority_targets())}",
            "",
            "## Targets",
            "",
        ]

        for index, target in enumerate(plan.targets, start=1):
            lines.extend(
                [
                    f"### {index}. {target.name}",
                    "",
                    f"- Difficulty: {target.difficulty}",
                    f"- Priority: {target.priority}",
                    "",
                    "Mathematical statement:",
                    "",
                    target.mathematical_statement,
                    "",
                    "Required definitions:",
                    "",
                ]
            )

            for definition in target.required_definitions:
                lines.append(f"- {definition}")

            lines.extend(
                [
                    "",
                    f"Expected output: {target.expected_output}",
                    "",
                ]
            )

        lines.extend(
            [
                "## First Lean Milestone",
                "",
                "The first serious milestone should be:",
                "",
                "Define finite systems, satisfaction, satisfaction-preserving morphisms, and prove that the identity morphism preserves satisfaction.",
                "",
                "This is small enough to be realistic and meaningful enough to increase mathematical credibility.",
                "",
                "## Correct Research Framing",
                "",
                "A Lean formalization plan is not the same as a Lean formalization.",
                "",
                "Project Aleph-Omega should not claim machine verification until Lean files actually compile.",
                "",
                "The careful claim is:",
                "",
                "Project Aleph-Omega now has a concrete plan for formalizing its finite satisfaction-preservation core in Lean.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        plan: LeanFormalizationPlan,
        path: str = "docs/lean_formalization_plan.md",
    ) -> Path:
        """
        Writes the Lean plan to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(plan))
        return output_path


if __name__ == "__main__":
    builder = LeanFormalizationPlanBuilder()
    plan = builder.build()
    output_path = builder.write_markdown(plan)

    print(plan.describe())
    print(f"Wrote Lean formalization plan to {output_path}")
