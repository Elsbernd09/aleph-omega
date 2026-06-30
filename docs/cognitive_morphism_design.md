# Cognitive Morphism Design

## Purpose

This document defines the Cognitive Morphism Engine in Project ℵω.

The Cognitive Morphism Engine studies the transformation from informal mathematical intuition into structured symbolic statements and early proof-assistant sketches.

The purpose is not to instantly generate complete 10,000-page proofs. The purpose is to model the first stages of mathematical formalization: turning intuition into objects, relations, claims, dependencies, and proof goals.

## Core Idea

Human mathematical thinking often begins before formal notation.

A mathematician may first notice a pattern, analogy, shape, obstruction, symmetry, or tension. Only later does that intuition become a definition, lemma, theorem, or proof.

Project ℵω treats this transition as a morphism-like process.

The source is informal cognition.

The target is symbolic mathematical structure.

The cognitive morphism asks:

What structure is preserved when intuition becomes formal language?

## Cognitive Morphism Object

A cognitive morphism is a structured transformation from intuition to symbolic form.

It will eventually contain:

- raw intuition text
- detected mathematical objects
- detected relations
- detected operations
- candidate definitions
- candidate assumptions
- candidate theorem statement
- proof goal sketch
- universe compatibility
- Lean skeleton
- confidence score
- ambiguity report

## Input Layer

The input layer accepts informal mathematical language.

Example inputs:

- I feel like primes are behaving like points connected by hidden geometric paths.
- This contradiction seems local, not system-destroying.
- The statement feels true in classical logic but not constructively true.
- The object seems unchanged only when the context stays fixed.

These inputs are not formal proofs. They are intuition fragments.

## Object Detection

The engine should detect mathematical objects mentioned in the intuition.

Possible detected objects:

- number
- prime
- set
- type
- object
- morphism
- universe
- statement
- proof
- contradiction
- context
- graph
- curve
- transformation
- symmetry

Object detection creates the first bridge from language to structure.

## Relation Detection

The engine should detect relationships between objects.

Possible relations:

- equals
- implies
- preserves
- transforms into
- contradicts
- depends on
- generalizes
- specializes
- maps to
- fails under
- becomes true in
- becomes false in

Relations are essential because mathematics is not only about objects. It is about structured relationships.

## Operation Detection

The engine should detect mathematical operations or transformations.

Possible operations:

- transport
- deformation
- negation
- implication
- quantification
- translation
- restriction
- extension
- composition
- abstraction
- specialization

These operations help the system infer what kind of formal structure the intuition might require.

## Candidate Statement Construction

After detecting objects, relations, and operations, the engine should build a candidate statement.

Example intuition:

Identity seems to depend on context.

Candidate symbolic statement:

For objects x and y, identity(x, y) is evaluated relative to an interpretation context C.

Possible theorem sketch:

If two objects are identical in context C, they may not remain identical after transport to context D.

The candidate statement is not automatically true. It is a structured hypothesis.

## Universe Compatibility

The engine should estimate which universe can express the candidate statement.

Example:

- statements about proof evidence may fit an intuitionistic universe
- statements about contradiction containment may fit a paraconsistent universe
- statements about degrees of truth may fit a fuzzy universe
- statements about necessity and possibility may fit a modal universe
- ordinary binary statements may fit a classical universe

Universe compatibility helps route intuitions into the right formal environment.

## Ambiguity Report

Mathematical intuition is often ambiguous.

The engine should not hide ambiguity.

It should report unclear parts such as:

- undefined objects
- missing relations
- vague terms
- multiple possible interpretations
- missing quantifiers
- unclear universe
- unclear proof goal
- unsupported symbolic leap

A good ambiguity report is valuable because it shows what must be clarified before formalization.

## Lean Skeleton Generation

The engine will eventually generate simple Lean-style theorem skeletons.

Early examples should be modest.

The goal is not complete proof automation. The goal is to produce a structured starting point.

A Lean skeleton may contain:

- theorem name
- variables
- assumptions
- conclusion
- placeholder proof body
- comments explaining missing proof obligations

Example skeleton idea:

theorem contextual_identity_transport : ... := by

  sorry

The use of sorry is acceptable in early sketches because the project is identifying proof structure, not pretending the proof is complete.

## Confidence Score

The engine should attach a confidence score to each transformation.

Possible scoring inputs:

- clarity of object detection
- clarity of relation detection
- number of ambiguities
- universe compatibility
- symbolic completeness
- Lean skeleton feasibility

A high confidence score means the intuition was translated into a relatively clear symbolic structure.

A low confidence score means the result needs human review.

## Human Review

The Cognitive Morphism Engine should remain human-in-the-loop.

Mathematical intuition cannot be blindly converted into valid proof.

The system can organize, clarify, and structure intuition, but human judgment is required to determine whether the resulting statement is meaningful, true, or worth formalizing.

## Experimental Workflow

A typical cognitive morphism experiment may follow this sequence:

1. Enter an informal mathematical intuition.
2. Detect mathematical objects.
3. Detect relations and operations.
4. Construct a candidate symbolic statement.
5. Identify compatible universes.
6. Generate an ambiguity report.
7. Produce a Lean theorem skeleton.
8. Save the result as a formalization attempt.

## Design Principle

The engine should translate intuition into structure without pretending that structure is proof.

Its value is in making hidden mathematical thought explicit.

## Summary

The Cognitive Morphism Engine is the intuition-to-formalization layer of Project ℵω.

It studies how informal mathematical insight can become symbolic structure.

It detects objects, relations, operations, ambiguity, universe compatibility, and Lean skeletons.

This allows Project ℵω to study not only formal systems, but also the transition from human mathematical imagination into formal mathematical language.

## Phase 6 Implementation Status

The first working Cognitive Morphism Layer has now been implemented.

Implemented files:

- src/cognitive_morphism/intuition.py
- src/cognitive_morphism/morphism.py
- src/cognitive_morphism/formalizer.py
- src/cognitive_morphism/gap_analyzer.py
- experiments/run_cognitive_morphism.py
- tests/test_cognitive_morphism.py

Current capabilities:

- represent informal mathematical intuitions
- classify intuition kinds such as analogy, category-structural intuition, contradiction tolerance, modal possibility, and constructive evidence
- track clarity level and formalization risk
- estimate conceptual richness and formalization readiness
- represent cognitive morphisms from intuition to symbolic statement
- track preserved properties, lost properties, added formal structure, preserved metaphors, and lost metaphors
- generate starter symbolic statements from informal intuitions
- infer statement kind, required symbols, free variables, and likely origin universe
- calculate formalization confidence, meaning drift, and formalization quality
- analyze the formalization gap between intuition and generated statement
- calculate review urgency, gap severity, and overall gap index
- rank formalizations by quality and severity
- run a cognitive morphism experiment
- test the cognitive morphism layer

The cognitive morphism layer is a heuristic modeling system. It does not claim to model human cognition, prove mathematical correctness, or automatically produce complete theorem formalizations. Its purpose is to make the informal-to-formal transition visible and reviewable.

## Phase 7 Implementation Status

The first working Neural-Symbolic Formalization Layer has now been implemented.

Implemented files:

- src/cognitive_morphism/formalization_target.py
- src/cognitive_morphism/lean_sketch.py
- src/cognitive_morphism/proof_obligation.py
- src/cognitive_morphism/formalization_planner.py
- experiments/run_neural_symbolic_formalization.py
- tests/test_neural_symbolic_formalization.py

Current capabilities:

- build formalization targets from generated statements
- classify formal targets as definitions, axioms, theorems, lemmas, structures, examples, or commentary sketches
- estimate formalization difficulty and readiness
- infer required definitions, assumptions, and Lean-style imports
- generate conservative Lean-style proof sketches
- include explicit warnings for unfinished `sorry` placeholders
- identify missing definitions, missing assumptions, semantic encoding requirements, and unresolved proof placeholders
- produce proof-obligation reports
- calculate proof burden and obligation indexes
- create ordered formalization plans
- recommend next formalization actions
- rank plans by burden and readiness
- run a full neural-symbolic formalization experiment
- test the full Phase 7 pipeline

This layer is intentionally honest about proof status. It does not claim that generated sketches are completed proofs. Any generated Lean-style theorem with `sorry` is unfinished. The purpose is to create a structured roadmap from informal intuition to formalization target, proof sketch, proof obligations, and next actions.
