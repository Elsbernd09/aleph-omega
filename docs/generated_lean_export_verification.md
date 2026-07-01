# Generated Lean Export Verification

## Purpose

Phase 31D adds a verification script for Python-generated Lean artifacts.

The script regenerates the exported Lean files and then checks them with Lean.

## Script

```text
scripts/check_generated_lean_exports.sh
```

## What It Checks

The script checks:

- generated finite system export,
- generated preservation morphism export,
- Lean compilation of formal/generated/ExportedTinySystem.lean,
- Lean compilation of formal/generated/ExportedTinyMorphism.lean.

## Command

Run:

```bash
./scripts/check_generated_lean_exports.sh
```

## Expected Final Output

```text
Generated Lean exports verified successfully.
```

## Why This Matters

This makes the Python-to-Lean export track reproducible.

Instead of manually generating and checking Lean files, reviewers can run one command.

## Strongest Claim

Project Aleph-Omega now has a script that regenerates Python-to-Lean finite exports and verifies them with Lean.

## Boundary

This verifies the current generated examples only.

Future phases should integrate generated Lean export verification into the full formal-stack gate.
