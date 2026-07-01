# Lean Machine Checking

## Purpose

Phase 21B installs Lean and adds a repository script for machine-checking the Project Aleph-Omega Lean core.

## Core File

The main Lean file is:

formal/lean/AlephOmegaCore.lean

## Checker Script

The checker script is:

scripts/check_lean.sh

Run it with:

./scripts/check_lean.sh

## Successful Output

If the Lean file compiles, the script prints:

Lean core formalization compiled successfully.

## Correct Research Claim

After successful compilation, the careful claim is:

Project Aleph-Omega has a machine-checked Lean prototype proving that identity morphisms preserve satisfaction and that composition of satisfaction-preserving morphisms preserves satisfaction in the formal core model.

This does not mean the entire Python project is machine-verified.

It means the central abstract proof pattern has a Lean-checked prototype.
