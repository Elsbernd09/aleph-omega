"""
Tests for theorem inventory generation.
"""

from pathlib import Path

from src.rigor.theorem_inventory import (
    TheoremInventory,
    TheoremInventoryBuilder,
    TheoremInventoryItem,
)


def test_theorem_inventory_builds():
    inventory = TheoremInventoryBuilder().build()

    assert isinstance(inventory, TheoremInventory)
    assert inventory.item_count() >= 5
    assert len(inventory.strongly_verified_items()) > 0
    assert len(inventory.conjectural_items()) > 0
    assert "TheoremInventory" in inventory.describe()


def test_theorem_inventory_item_describe():
    inventory = TheoremInventoryBuilder().build()
    item = inventory.items[0]

    assert isinstance(item, TheoremInventoryItem)
    assert "TheoremInventoryItem" in item.describe()
    assert item.identifier.startswith("claim.")


def test_theorem_inventory_markdown_contains_sections():
    inventory = TheoremInventoryBuilder().build()
    markdown = TheoremInventoryBuilder().to_markdown(inventory)

    assert "# Theorem Inventory" in markdown
    assert "## Summary" in markdown
    assert "## Inventory" in markdown
    assert "Correct Research Framing" in markdown


def test_theorem_inventory_write_markdown(tmp_path):
    inventory = TheoremInventoryBuilder().build()
    output_path = tmp_path / "theorem_inventory.md"

    written = TheoremInventoryBuilder().write_markdown(
        inventory=inventory,
        path=str(output_path),
    )

    assert isinstance(written, Path)
    assert written.exists()
    assert "Theorem Inventory" in written.read_text()
