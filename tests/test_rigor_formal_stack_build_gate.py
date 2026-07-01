"""
Tests for the unified formal stack build gate.
"""

from pathlib import Path


def test_formal_stack_checker_exists():
    assert Path("scripts/check_formal_stack.sh").exists()


def test_formal_stack_checker_calls_core_checks():
    text = Path("scripts/check_formal_stack.sh").read_text()

    assert "./scripts/check_lean.sh" in text
    assert "./scripts/check_lake_sync.sh" in text
    assert "./scripts/check_lake.sh" in text
    assert "python3 -m pytest" in text


def test_formal_stack_documentation_exists():
    path = Path("docs/formal_stack_build_gate.md")

    assert path.exists()
    text = path.read_text()

    assert "Formal Stack Build Gate" in text
    assert "./scripts/check_formal_stack.sh" in text
    assert "Lean core" in text or "Lean formalization" in text
