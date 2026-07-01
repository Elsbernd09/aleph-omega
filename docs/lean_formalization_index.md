# Lean Formalization Index

## Purpose

This document indexes the Lean formalization artifacts in Project Aleph-Omega.

The goal is to separate machine-checked claims from computational tests and written proof sketches.

---

## Main Lean File

The main Lean file is:

formal/lean/AlephOmegaCore.lean

---

## Machine-Checked Core

The Lean file defines:

- FormalSystem
- PreservationMorphism
- identityMorphism
- composeMorphism
- BoolSystem
- concrete failure-boundary maps

---

## Machine-Checked Positive Results

The Lean file proves:

- identity morphisms preserve satisfaction
- composition of satisfaction-preserving morphisms preserves satisfaction
- left identity law for sentence translation
- left identity law for model maps
- right identity law for sentence translation
- right identity law for model maps
- associativity law for sentence translation
- associativity law for model maps
- associativity of satisfaction preservation
- BoolSystem true satisfies true
- BoolSystem identity preserves satisfaction
- BoolSystem identity composition preserves satisfaction

---

## Machine-Checked Negative Results

The Lean file also proves:

- true does not satisfy false in BoolSystem
- a bad Bool sentence translation fails preservation
- the bad Bool translation is not satisfaction-preserving
- satisfaction preservation is not automatic

---

## Checker Script

The checker script is:

scripts/check_lean.sh

Run:

./scripts/check_lean.sh

Successful output:

Lean core formalization compiled successfully.

---

## Correct Claim

Project Aleph-Omega has a Lean-checked prototype for the abstract satisfaction-preservation core.

This does not machine-verify the entire Python implementation.

It does machine-check the central abstract proof pattern:

identity and composition preserve satisfaction when morphisms are defined as satisfaction-preserving.
