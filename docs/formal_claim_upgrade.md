# Formal Claim Upgrade

## Purpose

This document upgrades the claim status of selected Project Aleph-Omega results after the Lean formalization track.

---

## Claim Status Categories

Project Aleph-Omega uses the following levels of rigor:

1. Conceptual proposal
2. Computational implementation
3. Unit-tested implementation
4. Finite model-tested result
5. Written proof sketch
6. Machine-checked Lean prototype

---

## Machine-Checked Claims

The following claims now have Lean prototype support:

### Claim 1: Identity Preservation

For any formal system, the identity morphism preserves satisfaction.

Status:

Machine-checked Lean prototype.

Lean theorem:

identity_preserves_satisfaction

---

### Claim 2: Composition Preservation

If F preserves satisfaction and G preserves satisfaction, then G after F preserves satisfaction.

Status:

Machine-checked Lean prototype.

Lean theorem:

composition_preserves_satisfaction

---

### Claim 3: Category-Style Identity Laws

Left and right identity laws hold for sentence translation and model maps.

Status:

Machine-checked Lean prototype.

Lean theorems:

- left_identity_translation
- left_identity_model_map
- right_identity_translation
- right_identity_model_map

---

### Claim 4: Category-Style Associativity Laws

Associativity holds for sentence translation and model maps.

Status:

Machine-checked Lean prototype.

Lean theorems:

- associativity_translation
- associativity_model_map
- associativity_preserves_satisfaction

---

### Claim 5: Preservation Is Not Automatic

There exists a concrete BoolSystem translation that does not preserve satisfaction.

Status:

Machine-checked Lean prototype.

Lean theorem:

preservation_not_automatic

---

## Claims Not Yet Machine-Checked

The following remain computational or documentary claims:

- Python bridge distortion theorem
- finite model search exhaustiveness
- failure taxonomy completeness
- institution morphism checker correspondence with Lean definitions
- category structure of the full Python implementation
- relationship to full institution theory
- any general claim beyond the minimal Lean formal core

---

## Correct Research Claim

The careful upgraded claim is:

Project Aleph-Omega contains a Lean-checked prototype of its central satisfaction-preservation core, including identity preservation, composition preservation, category-style laws, a concrete finite example, and a concrete failure boundary.

This is stronger than a pure coding project.

It is not yet a fully formalized research theory.

## Phase 22 Claim Upgrade: Quotient Category Foundation

Phase 22 adds a Lean-checked quotient-category foundation for satisfaction-preserving morphisms modulo extensional equivalence.

Machine-checked prototype results now include:

- morphism equivalence laws
- identity laws up to morphism equivalence
- associativity up to morphism equivalence
- composition compatibility with equivalence
- Setoid construction for preservation morphisms
- quotient hom-types
- equality of quotient classes for equivalent morphisms
- quotient composition well-definedness
- quotient identity laws
- quotient associativity

Strongest careful claim:

> Project Aleph-Omega has a Lean-checked quotient-category foundation for satisfaction-preserving morphisms modulo extensional equivalence. This is not yet a complete Mathlib Category instance.

## Phase 23 Claim Upgrade: Standalone Quotient Category Structure

Phase 23 turns the quotient-category foundation into an actual standalone Lean category-like structure.

Lean-supported artifacts now include:

- quotient composition operation
- quotient left identity law
- quotient right identity law
- quotient associativity law
- standalone quotient category API
- StandaloneQuotientCategory structure
- AlephOmegaQuotientCategory instance

Strongest careful claim:

> Project Aleph-Omega has a Lean-defined standalone quotient category structure whose objects are formal systems and whose arrows are quotient homs of satisfaction-preserving morphisms modulo extensional equivalence. The structure includes Lean-checked identity and associativity laws.

Limitation:

> This is still not a Mathlib Category instance.
