# GitHub Actions Formal Stack CI

## Purpose

Phase 27D adds continuous integration for the Project Aleph-Omega formal stack.

Every push to main and every pull request to main now runs a GitHub Actions workflow.

## Workflow File

The workflow is located at:

.github/workflows/formal-stack.yml

## What It Checks

The workflow checks:

1. repository checkout,
2. Python setup,
3. pytest installation,
4. Lean installation through elan,
5. Lake Lean-core synchronization,
6. unified formal stack verification.

## Main Command

The workflow ultimately runs:

./scripts/check_formal_stack.sh

That command checks:

- the primary Lean formalization,
- Lake synchronization,
- Lake project build,
- Python tests.

## Why This Matters

Local verification is useful, but CI is stronger.

With this workflow, every pushed version of the repository can be automatically checked by GitHub.

## Correct Research Claim

Project Aleph-Omega now has GitHub Actions continuous integration for the Lean, Lake, and Python formal stack.
