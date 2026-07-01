# Project Aleph-Omega Mathlib Quotient Category Blueprint

## Purpose

This document begins the next PhD-level strengthening milestone.

Phase 29 created a real Mathlib category for direct satisfaction-preserving morphisms.

Phase 30 prepares the harder target: a real Mathlib category whose morphisms are quotient classes of satisfaction-preserving morphisms.

## Why This Is Harder

The direct category uses raw preservation morphisms as arrows.

The quotient category uses equivalence classes of preservation morphisms as arrows.

That means composition must be independent of representative choice.

## Summary

- Obstacles indexed: 7
- Hard obstacles: 5

## Obstacles and Required Results

### 1. Morphism equivalence relation

- Problem: The quotient category requires a Setoid on PreservationMorphism A B.
- Needed result: Define equivalence by equality of translate and mapModel fields, then prove reflexivity, symmetry, and transitivity.
- Difficulty: medium
- Proposed solution: Reuse the extensional equivalence idea from the standalone Lean core inside the Mathlib project.

### 2. Quotient hom type

- Problem: The Mathlib Category Hom type must be a type of quotient classes, not raw morphisms.
- Needed result: Define QuotientPreservationHom A B as Quotient of the PreservationMorphism setoid.
- Difficulty: medium
- Proposed solution: Use Lean's Quotient type over the morphism setoid for each pair of formal systems.

### 3. Representative-independent composition

- Problem: Composition of quotient morphisms must not depend on the chosen representatives.
- Needed result: If F ~ F' and G ~ G', then composePreservation F G ~ composePreservation F' G'.
- Difficulty: high
- Proposed solution: Prove composition respects morphism equivalence before defining quotient composition with Quotient.liftOn₂.

### 4. Identity laws on quotients

- Problem: Mathlib requires id_comp and comp_id over quotient morphisms.
- Needed result: Prove quotient identity laws using quotient induction and the raw direct category laws.
- Difficulty: high
- Proposed solution: Use Quotient.inductionOn for one quotient argument at a time and reduce to extensional equality.

### 5. Associativity on quotients

- Problem: Mathlib requires associativity over quotient morphisms.
- Needed result: Prove quotient associativity using nested quotient induction.
- Difficulty: very high
- Proposed solution: First prove raw composition associativity extensionally, then lift to quotient representatives.

### 6. Proof-field irrelevance

- Problem: Two preservation morphisms may have the same translate and mapModel fields but different proof terms.
- Needed result: The quotient equivalence must intentionally ignore preserves proof-field differences.
- Difficulty: high
- Proposed solution: Use extensional equivalence over computational fields only, matching the standalone core.

### 7. Mathlib notation compatibility

- Problem: The quotient category must work with Mathlib notation: 𝟙, ≫, and A ⟶ B.
- Needed result: Define a real Category instance whose Hom field is the quotient hom type.
- Difficulty: high
- Proposed solution: Create a separate Lean file for the quotient category attempt to avoid destabilizing FormalSystemCategory.lean.

## Target Category

Objects:

- FormalSystem

Morphisms:

- equivalence classes of PreservationMorphism A B

Identity:

- quotient class of identityPreservation A

Composition:

- quotient class of composePreservation F G

## Strongest Claim After This Phase

> Project Aleph-Omega now has a detailed technical blueprint for upgrading the Mathlib direct preservation-morphism category into a Mathlib quotient category.

## Non-Claim

This phase does not yet create the quotient category instance.

The next phase should attempt the Lean implementation.
