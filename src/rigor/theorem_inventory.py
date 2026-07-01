"""
Theorem inventory generator for Project Aleph-Omega.

This module exports the registered formal claims into a readable theorem-style
inventory. The goal is to make the project's mathematical claims easy to review.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple

from src.rigor.claim_registry import (
    FormalClaim,
    standard_claim_registry,
)


@dataclass(frozen=True)
class TheoremInventoryItem:
    """
    One theorem-like claim inventory item.
    """

    identifier: str
    title: str
    statement: str
    scope: str
    verification_level: str
    evidence: Tuple[str, ...]
    limitations: Tuple[str, ...]
    conjectural: bool
    strongly_verified: bool

    def describe(self) -> str:
        """
        Returns a readable inventory item.
        """

        return (
            f"TheoremInventoryItem\n"
            f"Identifier: {self.identifier}\n"
            f"Title: {self.title}\n"
            f"Scope: {self.scope}\n"
            f"Verification level: {self.verification_level}\n"
            f"Strongly verified: {self.strongly_verified}\n"
            f"Conjectural: {self.conjectural}"
        )


@dataclass(frozen=True)
class TheoremInventory:
    """
    Inventory of theorem-like claims.
    """

    items: Tuple[TheoremInventoryItem, ...]

    def item_count(self) -> int:
        """
        Counts inventory items.
        """

        return len(self.items)

    def strongly_verified_items(self) -> Tuple[TheoremInventoryItem, ...]:
        """
        Returns strongly verified items.
        """

        return tuple(item for item in self.items if item.strongly_verified)

    def conjectural_items(self) -> Tuple[TheoremInventoryItem, ...]:
        """
        Returns conjectural items.
        """

        return tuple(item for item in self.items if item.conjectural)

    def describe(self) -> str:
        """
        Returns a readable inventory summary.
        """

        return (
            f"TheoremInventory\n"
            f"Items: {self.item_count()}\n"
            f"Strongly verified items: {len(self.strongly_verified_items())}\n"
            f"Conjectural items: {len(self.conjectural_items())}"
        )


class TheoremInventoryBuilder:
    """
    Builds theorem inventory artifacts.
    """

    def item_from_claim(self, claim: FormalClaim) -> TheoremInventoryItem:
        """
        Converts one formal claim into an inventory item.
        """

        return TheoremInventoryItem(
            identifier=claim.identifier,
            title=claim.title,
            statement=claim.statement,
            scope=claim.scope.value,
            verification_level=claim.verification_level.value,
            evidence=claim.evidence,
            limitations=claim.limitations,
            conjectural=claim.is_conjectural(),
            strongly_verified=claim.is_strongly_verified(),
        )

    def build(self) -> TheoremInventory:
        """
        Builds the standard theorem inventory.
        """

        registry = standard_claim_registry()

        return TheoremInventory(
            items=tuple(self.item_from_claim(claim) for claim in registry.claims)
        )

    def to_markdown(self, inventory: TheoremInventory) -> str:
        """
        Converts the inventory into markdown.
        """

        lines = [
            "# Theorem Inventory",
            "",
            "## Purpose",
            "",
            "This document lists the theorem-like claims registered in Project Aleph-Omega.",
            "",
            "It separates finite verified claims from conjectural generalizations.",
            "",
            "## Summary",
            "",
            f"- Inventory items: {inventory.item_count()}",
            f"- Strongly verified items: {len(inventory.strongly_verified_items())}",
            f"- Conjectural items: {len(inventory.conjectural_items())}",
            "",
            "## Inventory",
            "",
        ]

        for item in inventory.items:
            lines.extend(
                [
                    f"### {item.identifier}",
                    "",
                    f"- Title: {item.title}",
                    f"- Scope: {item.scope}",
                    f"- Verification level: {item.verification_level}",
                    f"- Strongly verified: {item.strongly_verified}",
                    f"- Conjectural: {item.conjectural}",
                    "",
                    "Statement:",
                    "",
                    item.statement,
                    "",
                    "Evidence:",
                    "",
                ]
            )

            for evidence in item.evidence:
                lines.append(f"- {evidence}")

            lines.extend(
                [
                    "",
                    "Limitations:",
                    "",
                ]
            )

            for limitation in item.limitations:
                lines.append(f"- {limitation}")

            lines.append("")

        lines.extend(
            [
                "## Correct Research Framing",
                "",
                "The inventory is not a claim that all listed items are universal mathematical theorems.",
                "",
                "It records the current scope, verification level, evidence, and limitations of each theorem-like statement.",
                "",
            ]
        )

        return "\n".join(lines)

    def write_markdown(
        self,
        inventory: TheoremInventory,
        path: str = "docs/theorem_inventory.md",
    ) -> Path:
        """
        Writes the theorem inventory to disk.
        """

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(inventory))
        return output_path


if __name__ == "__main__":
    builder = TheoremInventoryBuilder()
    inventory = builder.build()
    output_path = builder.write_markdown(inventory)

    print(inventory.describe())
    print(f"Wrote theorem inventory to {output_path}")
