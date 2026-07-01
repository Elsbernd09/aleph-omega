"""
Tests for the Lean core formalization artifact.
"""

from pathlib import Path


def test_lean_core_file_exists():
    path = Path("formal/lean/AlephOmegaCore.lean")

    assert path.exists()
    assert path.read_text().strip()


def test_lean_core_contains_main_definitions():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "structure FormalSystem" in text
    assert "structure PreservationMorphism" in text
    assert "def identityMorphism" in text
    assert "def composeMorphism" in text


def test_lean_core_contains_main_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem composition_preserves_satisfaction" in text
    assert "theorem identity_preserves_satisfaction" in text
