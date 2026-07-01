# Mathlib Project Scaffold

## Purpose

Phase 29B adds a separate experimental Mathlib Lake project.

The existing Lean stack remains untouched.

The new experimental project lives at:

formal/aleph_omega_mathlib/

## Why Separate?

Mathlib integration can be fragile because it involves:

- Lake dependency resolution,
- Lean toolchain versions,
- universe levels,
- category-theory imports,
- proof-shape compatibility.

Keeping the Mathlib experiment separate protects the existing verified formal stack.

## Files Added

- formal/aleph_omega_mathlib/lakefile.lean
- formal/aleph_omega_mathlib/lean-toolchain
- formal/aleph_omega_mathlib/AlephOmegaMathlib.lean
- formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean
- scripts/check_mathlib_scaffold.sh

## Smoke Test

The smoke test imports:

Mathlib.CategoryTheory.Category.Basic

and defines a tiny category-like function system with identity and associativity proofs.

## Correct Claim

Project Aleph-Omega now has a separate experimental Mathlib scaffold for testing future category-theory integration.

## Non-Claim

This phase does not yet create a Mathlib `Category` instance for Project Aleph-Omega.
