# Lean Two-Model / Two-Sentence Finite System

## Purpose

Phase 25A adds a concrete finite formal system directly inside Lean.

This moves Project Aleph-Omega closer to connecting the Python finite-universe implementation with the Lean formal core.

## Finite System

The Lean file now defines:

- TwoModel
- TwoSentence
- TwoSystem

The system has:

- model m0
- model m1
- sentence p
- sentence q

Satisfaction relation:

- m0 satisfies p
- m1 satisfies q
- m0 does not satisfy q
- m1 does not satisfy p

## Positive Theorems

Lean proves:

- m0 satisfies p
- m1 satisfies q
- identity preserves satisfaction
- identity composed with itself preserves satisfaction

## Failure Boundary

Lean also proves:

- a sentence-swap translation fails preservation
- the swap translation is not satisfaction-preserving

## Why This Matters

Earlier Lean examples used BoolSystem.

TwoSystem is closer to the Python finite-institution layer because it explicitly separates model names from sentence names.

This is a stronger concrete finite example.

## Correct Research Claim

Project Aleph-Omega now contains a Lean-checked concrete finite system with two models, two sentences, positive preservation theorems, and a negative preservation failure boundary.
