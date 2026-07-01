"""
Tests for Lean formalization index documentation.
"""

from pathlib import Path


def test_lean_formalization_index_exists():
    path = Path("docs/lean_formalization_index.md")

    assert path.exists()
    assert "Machine-Checked Core" in path.read_text()
    assert "Machine-Checked Positive Results" in path.read_text()
    assert "Machine-Checked Negative Results" in path.read_text()


def test_formal_claim_upgrade_exists():
    path = Path("docs/formal_claim_upgrade.md")

    assert path.exists()
    text = path.read_text()

    assert "Machine-checked Lean prototype" in text
    assert "identity_preserves_satisfaction" in text
    assert "composition_preserves_satisfaction" in text
    assert "preservation_not_automatic" in text
