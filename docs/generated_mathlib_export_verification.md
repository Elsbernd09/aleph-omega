# Generated Mathlib Export Verification

## Purpose

Phase 32D adds a verification script for Python-generated Mathlib-track artifacts.

The script regenerates the Mathlib-targeted finite system and preservation morphism, rebuilds the generated import index, and checks the experimental Mathlib project.

## Script

```text
scripts/check_generated_mathlib_exports.sh
```

## What It Checks

- Mathlib-targeted finite system export
- Mathlib-targeted preservation morphism export
- generated Mathlib import index
- Lake build of the experimental Mathlib project

## Command

Run:

```bash
./scripts/check_generated_mathlib_exports.sh
```

## Expected Final Output

```text
Generated Mathlib exports verified successfully.
```

## Why This Matters

This makes the Mathlib-targeted export track reproducible.

Reviewers can now regenerate Python-produced Mathlib artifacts and verify them with one command.

## Strongest Claim

Project Aleph-Omega now has a reproducible script that regenerates Python-produced Mathlib finite-system and preservation-morphism exports and verifies them through the experimental Mathlib Lake build.

## Boundary

This verifies the current generated Mathlib examples only.

Future phases should integrate this script into the full formal-stack gate.

## Formal Stack Integration

Phase 32E integrates generated Mathlib export verification into the main formal-stack gate.

The main verification command now includes:

```bash
./scripts/check_generated_mathlib_exports.sh
```

This means the project checks Python-generated Mathlib finite systems and preservation morphisms as part of the official formal verification pipeline.

Primary command:

```bash
./scripts/check_formal_stack.sh
```
