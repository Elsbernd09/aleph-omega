"""
Tests for the Lean checker script artifact.
"""

from pathlib import Path


def test_lean_checker_script_exists():
    path = Path("scripts/check_lean.sh")

    assert path.exists()
    assert path.read_text().strip()


def test_lean_checker_script_points_to_core_file():
    text = Path("scripts/check_lean.sh").read_text()

    assert "formal/lean/AlephOmegaCore.lean" in text
    assert "lean" in text
