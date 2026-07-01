"""
Tests for GitHub Actions formal stack CI workflow.
"""

from pathlib import Path


def test_github_actions_workflow_exists():
    path = Path(".github/workflows/formal-stack.yml")

    assert path.exists()


def test_github_actions_workflow_contains_core_steps():
    text = Path(".github/workflows/formal-stack.yml").read_text()

    assert "Aleph-Omega Formal Stack" in text
    assert "actions/checkout" in text
    assert "actions/setup-python" in text
    assert "elan-init.sh" in text
    assert "./scripts/check_formal_stack.sh" in text


def test_github_actions_workflow_runs_on_main():
    text = Path(".github/workflows/formal-stack.yml").read_text()

    assert "push:" in text
    assert "pull_request:" in text
    assert "main" in text


def test_github_actions_documentation_exists():
    path = Path("docs/github_actions_formal_ci.md")

    assert path.exists()
    text = path.read_text()

    assert "GitHub Actions Formal Stack CI" in text
    assert ".github/workflows/formal-stack.yml" in text
    assert "./scripts/check_formal_stack.sh" in text
