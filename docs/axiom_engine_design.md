# Axiom Engine Design

## Purpose

This document defines the design of the Generative Axiom Engine in Project ℵω.

The axiom engine is responsible for representing, generating, scoring, comparing, and filtering toy axiom systems.

The purpose is not to automatically discover final mathematical truth. The purpose is to create a computational laboratory where formal assumptions can be explored as structured objects.

## Core Idea

An axiom is a starting assumption inside a formal system.

Traditional mathematics usually begins with a chosen set of axioms. Project ℵω asks a different question:

What happens if axiom systems themselves become objects of computation?

The axiom engine treats axioms as data. It stores their statements, symbols, dependencies, complexity, novelty, contradiction risk, and interaction patterns.

## Axiom Object

Each axiom will eventually be represented as a structured object.

Important fields:

- name
- informal statement
- symbolic form
- symbols used
- arity
- quantifier depth
- logical connectives
- dependency profile
- complexity score
- novelty score
- contradiction risk
- expressivity contribution
- compatible universes
- incompatible universes

## Example Axiom

Name: Contextual Identity

Informal statement: Identity is preserved only relative to an interpretation context.

Possible symbolic sketch: identity(x, y, context) depends on the interpretation context.

This axiom is not presented as established mathematics. It is an experimental assumption used to study context-sensitive identity behavior.

## Axiom System

An axiom system is a collection of axioms together with metadata about their interactions.

An axiom system may contain:

- a name
- a list of axioms
- an intended universe
- an inference rule set
- a truth value space
- a contradiction policy
- a dependency graph
- an expressivity score
- a stability score
- a novelty score
- a risk score

## Generation Strategy

The first version of the axiom engine will use hand-designed templates.

Later versions may include generative search, mutation, recombination, and evolutionary scoring.

Possible generation methods:

- template-based generation
- symbolic mutation
- axiom recombination
- operator substitution
- truth-table variation
- dependency graph expansion
- random controlled generation
- evolutionary search

## Template-Based Generation

Template generation creates axioms from controlled patterns.

Example template:

For every object x, property P is preserved under transformation T if condition C holds.

This can generate many candidate axioms by changing object type, property, transformation, and condition.

Template generation is useful because it avoids meaningless random text while still producing variation.

## Mutation

Mutation modifies an existing axiom.

Possible mutation operations:

- replace a logical connective
- add a condition
- remove a condition
- change a quantifier
- introduce a context variable
- weaken a conclusion
- strengthen a conclusion
- replace equality with equivalence
- replace truth with provability

Mutation allows the engine to explore nearby formal systems.

## Recombination

Recombination combines parts of two or more axioms.

For example, an identity axiom and a context axiom may combine into a context-sensitive identity axiom.

Recombination is useful for producing axioms that are structurally related to existing assumptions but not identical to them.

## Scoring System

The axiom engine will score candidate axioms using heuristic metrics.

These metrics are not mathematical proofs. They are computational tools for ranking and filtering candidates.

## Complexity Score

Complexity measures how structurally complicated an axiom is.

Possible inputs:

- number of symbols
- number of variables
- number of quantifiers
- nesting depth
- number of logical connectives
- number of dependencies
- number of universe-specific operators

A very simple axiom may be too weak. A very complex axiom may be difficult to interpret. The engine should identify a productive middle zone.

## Novelty Score

Novelty measures how different a candidate axiom is from existing axioms.

Possible inputs:

- symbolic distance from known axioms
- difference in dependency graph
- unusual connective combinations
- new interaction with truth values
- new universe compatibility profile

Novelty does not mean truth. It only means structural difference.

## Contradiction Risk

Contradiction risk estimates whether an axiom may conflict with other axioms.

Possible risk signals:

- direct negation of an existing axiom
- incompatible truth value requirements
- conflict with universe consistency policy
- circular dependency
- unrestricted self-reference
- excessive inference strength

This is not a consistency proof. It is a warning system.

## Expressivity Contribution

Expressivity contribution estimates how much an axiom expands what the system can express.

An axiom may increase expressivity if it introduces:

- new object types
- new relations
- new transformations
- new interpretation contexts
- new modal statuses
- new proof statuses
- new bridge behavior

## Stability Score

Stability measures whether the axiom system remains usable after adding an axiom.

A stable axiom system should avoid immediate collapse, uncontrolled explosion, or total ambiguity.

Different universes may define stability differently.

In a classical universe, contradiction may be highly unstable.

In a paraconsistent universe, contradiction may be locally acceptable.

## Dependency Graph

The axiom engine will eventually represent axioms as nodes in a graph.

Edges may represent:

- depends on
- contradicts
- strengthens
- weakens
- generalizes
- specializes
- translates to
- blocks
- enables

This graph will help the project visualize how formal assumptions interact.

## Filtering

The engine should filter axioms before they enter experiments.

Possible filters:

- remove empty or meaningless axioms
- remove duplicate axioms
- remove axioms with excessive contradiction risk
- remove axioms outside the target universe language
- remove axioms with no expressivity contribution
- flag axioms requiring human review

## Human Review

Project ℵω should keep a human-in-the-loop design.

Generated axioms are candidates, not discoveries.

The system can rank and organize them, but mathematical interpretation still requires human judgment.

## Experimental Workflow

A typical axiom experiment may follow this sequence:

1. Select a target universe.
2. Generate candidate axioms.
3. Score the candidates.
4. Filter weak or dangerous candidates.
5. Add selected axioms to a toy axiom system.
6. Run inference or translation experiments.
7. Measure stability, expressivity, and bridge behavior.
8. Produce a research report.

## Design Principle

The axiom engine should be ambitious in structure but cautious in claims.

It should make formal assumptions explorable, not pretend to manufacture final mathematical truth.

## Summary

The Generative Axiom Engine is one of the central components of Project ℵω.

It turns axioms into computational objects. It allows axiom systems to be generated, scored, compared, filtered, and studied across different formal universes.

## Phase 2 Implementation Status

The first working version of the Generative Axiom Engine has now been implemented.

Implemented files:

- src/generative_axioms/axiom.py
- src/generative_axioms/library.py
- src/generative_axioms/evaluator.py
- src/generative_axioms/generator.py
- experiments/run_axiom_engine.py
- tests/test_generative_axioms.py

Current capabilities:

- represent axioms as structured Python objects
- load a hand-designed starter axiom library
- generate new candidate axioms from controlled templates
- mutate seed axioms into nearby candidate assumptions
- score axioms using heuristic metrics
- rank axioms by overall research interest
- run an experiment that prints a ranked axiom table
- test the main generative axiom engine components

The implemented evaluator currently scores:

- complexity
- novelty
- contradiction risk
- expressivity
- stability
- overall interest

These scores remain heuristic research instruments. They are useful for comparison and filtering, but they are not mathematical proofs.
