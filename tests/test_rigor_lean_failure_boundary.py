"""
Tests for the Lean failure-boundary artifact.
"""

from pathlib import Path


def test_lean_core_contains_bad_translation():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "def boolNegSentence" in text
    assert "def boolIdentityModel" in text


def test_lean_core_contains_failure_theorems():
    text = Path("formal/lean/AlephOmegaCore.lean").read_text()

    assert "theorem bool_bad_translation_failure" in text
    assert "theorem bool_bad_translation_not_preserving" in text
    assert "theorem preservation_not_automatic" in text
