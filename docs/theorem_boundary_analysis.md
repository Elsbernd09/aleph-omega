# Theorem Boundary Analysis

## Purpose

Phase 15D adds theorem boundary analysis to Project Aleph-Omega.

The goal is to explain the boundary between theorem success, vacuous success, hypothesis failure, semantic distortion, and structural failure.

---

## Boundary Statuses

The analyzer classifies generated cases as:

- verified preservation
- vacuous preservation
- hypothesis failure
- semantic distortion
- structural failure

---

## Verified Preservation

A case has verified preservation when at least one source statement is satisfied and every satisfied source statement translates into a satisfied target statement.

This is the strongest success case.

---

## Vacuous Preservation

A case has vacuous preservation when no source statement is satisfied.

Then preservation technically holds, but it is not a strong example because there was no satisfied statement to preserve.

---

## Hypothesis Failure

A case has hypothesis failure when a required compatibility condition is violated.

For example, a bridge may have feature mismatch.

This means the theorem may not apply.

---

## Structural Failure

A case has structural failure when the bridge itself does not provide enough structure.

For example, a satisfied source statement may have no defined translation.

---

## Semantic Distortion

A case has semantic distortion when the bridge exists structurally but still fails to preserve satisfaction.

This is the most important kind of semantic boundary case.

---

## Why This Matters

Theorem boundary analysis makes the project more serious because it separates:

1. strong theorem success
2. vacuous theorem success
3. failed assumptions
4. structural failure
5. semantic failure

This prevents the project from overstating results.

---

## Correct Research Claim

Project Aleph-Omega can now say:

The finite search layer classifies theorem-boundary behavior, distinguishing verified preservation, vacuous preservation, hypothesis failure, structural failure, and semantic distortion.

This remains finite, computational, and model-bound.
