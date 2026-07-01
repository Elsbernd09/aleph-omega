# Lean Formalization Plan

## Purpose

This document identifies the first realistic Lean formalization targets for Project Aleph-Omega.

The goal is not to formalize the entire codebase at once.

The goal is to formalize a small mathematical core:

1. finite satisfaction
2. satisfaction-preserving morphisms
3. identity preservation
4. composition preservation
5. category-like structure

## Summary

- Formalization targets: 5
- Highest priority targets: 3

## Targets

### 1. Finite Satisfaction Predicate

- Difficulty: introductory
- Priority: 1

Mathematical statement:

Define finite models, finite sentences, and a satisfaction predicate Sat : Model -> Sentence -> Prop.

Required definitions:

- Finite type of sentences
- Finite type of models
- Satisfaction predicate

Expected output: Lean definitions compiling without theorem burden.

### 2. Satisfaction-Preserving Morphism

- Difficulty: moderate
- Priority: 1

Mathematical statement:

Define a morphism as a sentence translation together with a model pairing such that source satisfaction implies target satisfaction of translated sentences.

Required definitions:

- Source finite system
- Target finite system
- Sentence translation
- Model pairing
- Preservation predicate

Expected output: Lean definition of satisfaction-preserving morphism.

### 3. Identity Preserves Satisfaction

- Difficulty: moderate
- Priority: 1

Mathematical statement:

For every finite system, the identity sentence translation and identity model pairing preserve satisfaction.

Required definitions:

- Identity sentence translation
- Identity model pairing
- Preservation predicate

Expected output: Lean theorem: identity_preserves_satisfaction.

### 4. Composition Preserves Satisfaction

- Difficulty: advanced
- Priority: 2

Mathematical statement:

If F preserves satisfaction and G preserves satisfaction, then G composed with F preserves satisfaction.

Required definitions:

- Composable morphisms
- Composition of sentence translations
- Composition of model pairings
- Preservation predicate

Expected output: Lean theorem: composition_preserves_satisfaction.

### 5. Preservation Morphisms Form a Category

- Difficulty: advanced
- Priority: 3

Mathematical statement:

Finite systems with satisfaction-preserving morphisms form a category-like structure with identity and composition.

Required definitions:

- Objects
- Morphisms
- Identity
- Composition
- Identity laws
- Associativity law

Expected output: Lean category-style theorem or structure.

## First Lean Milestone

The first serious milestone should be:

Define finite systems, satisfaction, satisfaction-preserving morphisms, and prove that the identity morphism preserves satisfaction.

This is small enough to be realistic and meaningful enough to increase mathematical credibility.

## Correct Research Framing

A Lean formalization plan is not the same as a Lean formalization.

Project Aleph-Omega should not claim machine verification until Lean files actually compile.

The careful claim is:

Project Aleph-Omega now has a concrete plan for formalizing its finite satisfaction-preservation core in Lean.
