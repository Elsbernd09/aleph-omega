"""
Tests for generated Mathlib export integration in the formal stack.
"""

from pathlib import Path


def test_formal_stack_runs_generated_mathlib_exports():
    text = Path("scripts/check_formal_stack.sh").read_text()

    assert "./scripts/check_generated_mathlib_exports.sh" in text
    assert "Checking generated Mathlib exports" in text


def test_generated_mathlib_export_checker_is_executable_script():
    path = Path("scripts/check_generated_mathlib_exports.sh")
    text = path.read_text()

    assert path.exists()
    assert text.startswith("#!/usr/bin/env bash")
    assert "set -euo pipefail" in text
    assert "python3 -m src.rigor.mathlib_finite_system_exporter" in text
    assert "python3 -m src.rigor.mathlib_morphism_exporter" in text
    assert "./scripts/check_mathlib_scaffold.sh" in text


def test_generated_mathlib_export_docs_mention_formal_stack():
    text = Path("docs/generated_mathlib_export_verification.md").read_text()

    assert "Formal Stack Integration" in text
    assert "./scripts/check_formal_stack.sh" in text
    assert "official formal verification pipeline" in text
