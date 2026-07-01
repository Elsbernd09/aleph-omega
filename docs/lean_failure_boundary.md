# Lean Failure Boundary

## Purpose

Phase 21E adds a concrete Lean-checked failure boundary.

The goal is to show that satisfaction preservation is not automatic.

A sentence translation can destroy satisfaction.

## Bool Failure Example

The BoolSystem has:

- models as Bool
- sentences as Bool
- satisfaction as equality

The bad translation flips sentences:

true becomes false.

The model map keeps models unchanged.

So for model true and sentence true:

- source satisfaction holds
- translated target sentence is false
- target satisfaction fails

## Lean Theorems Added

The Lean file now proves:

- a concrete bad translation failure witness
- the bad Bool translation is not satisfaction-preserving
- preservation is not automatic

## Why This Matters

This makes the theorem stronger as a research artifact.

A serious theorem should have a boundary.

This phase shows exactly why satisfaction preservation must be required as a condition.

## Correct Research Claim

Project Aleph-Omega has a Lean-checked example proving that satisfaction preservation is not automatic.

The project now has both:

- positive preservation theorems
- negative failure-boundary examples
