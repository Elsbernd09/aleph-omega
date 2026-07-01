# Project Aleph-Omega Quickstart

## Purpose

This quickstart shows reviewers how to run the Project Aleph-Omega formal stack locally.

The main verification command is:

```bash
./scripts/check_formal_stack.sh
```

That command checks the Lean core, Lake project synchronization, Lake build, and Python tests.

## Prerequisites

- Python 3
- pytest
- Lean installed through elan
- macOS or Linux shell environment

## Quickstart Steps

### Step 1: Install Python test dependency

```bash
python3 -m pip install pytest
```

Installs pytest, which is required for the Python test suite.

### Step 2: Check the primary Lean formalization

```bash
source "$HOME/.elan/env"
./scripts/check_lean.sh
```

Compiles the primary Lean file at formal/lean/AlephOmegaCore.lean.

### Step 3: Check Lake synchronization

```bash
./scripts/check_lake_sync.sh
```

Verifies that the primary Lean file and Lake project copy are identical.

### Step 4: Build the Lake project

```bash
source "$HOME/.elan/env"
./scripts/check_lake.sh
```

Builds the standalone Lean Lake project.

### Step 5: Run Python tests

```bash
python3 -m pytest
```

Runs the Python finite-computation and documentation-generation test suite.

### Step 6: Run the full formal stack

```bash
source "$HOME/.elan/env"
./scripts/check_formal_stack.sh
```

Runs the complete verification gate in one command.

## Expected Success Signal

The full formal-stack command should end with:

```text
Aleph-Omega formal stack verified successfully.
```

## What the Verification Means

A successful run means:

- the primary Lean formalization compiles,
- the Lake copy is synchronized with the primary Lean file,
- the Lake project builds,
- the Python test suite passes.

## What the Verification Does Not Mean

A successful run does not mean the project proves a universal theorem about all institutions or all logics.

It means the repository's stated finite Lean/Python formal stack is reproducible.
