# Lean Standalone Quotient Category API

## Purpose

Phase 23B packages the quotient-category core into a clean standalone Lean API.

The project is still not using Mathlib's Category typeclass.

Instead, it exposes a small category-like interface directly inside the Aleph-Omega Lean core.

## Added API Names

The Lean file now defines:

- QuotientHom
- quotientId
- quotientComp
- quotientHomOf

## Added API Laws

The Lean file proves:

- quotient_api_left_identity
- quotient_api_right_identity
- quotient_api_associativity

## Added Extensionality Result

The Lean file also proves:

- quotient_hom_ext

This says equivalent preservation morphisms determine the same quotient hom.

## Why This Matters

The project now has a readable category-style interface:

- objects are FormalSystem values
- arrows are QuotientHom values
- identity is quotientId
- composition is quotientComp
- identity and associativity laws are Lean-checked

## Correct Research Claim

Project Aleph-Omega now has a standalone Lean quotient-category API for satisfaction-preserving morphisms modulo extensional equivalence.

This is still not a Mathlib Category instance, but it is a clean category-like formal core.
