# Failure Extractor

## Purpose

Phase 15B extracts counterexample-like failure cases from the finite satisfaction search layer.

These cases are not necessarily formal counterexamples to theorems.

They are generated cases where satisfaction preservation fails.

---

## What Gets Extracted

The extractor scans generated satisfaction search cases and keeps the cases where distortion appears.

Each extracted case includes:

- the bridge
- the bridge kind
- the failure kind
- whether satisfaction was preserved
- whether distortion appeared
- an explanation from the failure taxonomy

---

## Why These Are Counterexample-Like

A formal counterexample would disprove a theorem.

A counterexample-like failure case is different.

It shows a boundary condition where preservation fails because one of the necessary assumptions is not satisfied.

For example:

- a satisfied source statement has no translation
- a translated target statement is not satisfied
- a bridge collapses statements and loses semantic information
- a bridge has feature mismatch

---

## Why This Matters

This phase makes the project stronger because it does not hide failure cases.

Instead, it extracts them and studies them.

That is closer to serious mathematical research:

1. state theorem
2. test theorem
3. identify failed assumptions
4. classify boundary cases
5. refine theorem statements

---

## Correct Research Claim

Project Aleph-Omega can now say:

The finite search layer extracts and classifies generated semantic failure cases, allowing the project to study theorem boundaries rather than only successful examples.

This is finite and model-bound.
