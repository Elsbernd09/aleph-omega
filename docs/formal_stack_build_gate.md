# Formal Stack Build Gate

## Purpose

Phase 27C adds one command that verifies the full Project Aleph-Omega formal stack.

The command is:

./scripts/check_formal_stack.sh

## What It Checks

The formal stack gate checks:

1. the primary Lean formalization,
2. Lake synchronization,
3. the standalone Lake project build,
4. the Python test suite.

## Scripts Used

The build gate calls:

- scripts/check_lean.sh
- scripts/check_lake_sync.sh
- scripts/check_lake.sh
- python3 -m pytest

## Why This Matters

Before this phase, the repository had multiple separate verification commands.

After this phase, a reviewer can run one command to check the full formal stack.

## Correct Research Claim

Project Aleph-Omega now includes a unified verification command that checks the Lean core, Lake project, synchronization guard, and Python computational test suite.
