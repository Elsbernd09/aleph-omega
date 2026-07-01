"""
Tests for the public-facing README.
"""

from pathlib import Path


def test_readme_archive_exists():
    assert Path("README_ARCHIVE.md").exists()


def test_public_readme_contains_core_sections():
    text = Path("README.md").read_text()

    assert "# Project ℵω / Aleph-Omega" in text
    assert "What the Project Does" in text
    assert "Lean Formalization" in text
    assert "Python Layer" in text
    assert "Formal Stack Verification" in text
    assert "What This Project Is Not" in text


def test_public_readme_contains_careful_claim_boundaries():
    text = Path("README.md").read_text()

    assert "not yet" in text
    assert "universal theory of institutions" in text
    assert "full Mathlib" in text
    assert "field-changing theorem" in text


def test_public_readme_contains_run_commands():
    text = Path("README.md").read_text()

    assert "./scripts/check_lean.sh" in text
    assert "./scripts/check_lake.sh" in text
    assert "./scripts/check_formal_stack.sh" in text
    assert "python3 -m pytest" in text


def test_public_readme_notes_exist():
    path = Path("docs/public_release_readme_notes.md")

    assert path.exists()
    text = path.read_text()

    assert "Public Release README Notes" in text
    assert "README_ARCHIVE.md" in text
    assert "without overclaiming" in text
