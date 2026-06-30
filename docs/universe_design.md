# Universe Design

## Purpose

This document defines the universe layer of Project ℵω.

In this project, a universe is not a physical cosmos. It is a modeled formal environment: a mathematical context with its own language, axioms, inference rules, truth values, objects, morphisms, and interpretation rules.

The universe layer is inspired by category theory and topos-theoretic thinking, but the first implementation will use simplified toy models. The goal is to make different logical environments computationally visible and comparable.

## Core Definition

A universe is a formal context in which statements can be expressed, interpreted, evaluated, and transformed.

A universe contains:

- a name
- a formal system
- a truth value space
- a consistency policy
- a collection of objects
- a collection of morphisms
- a collection of statements
- internal inference rules
- metadata describing its mathematical behavior

## Why Universes Matter

Ordinary mathematical software usually assumes one background logic. Project ℵω makes that background explicit.

This allows the project to ask questions such as:

- What happens to truth when a statement moves from classical logic to paraconsistent logic?
- What happens to contradiction when the target universe does not explode?
- What information is preserved by a translation?
- What information is lost?
- Which systems are more expressive?
- Which systems are more stable?
- Which systems are more fragile?

## Universe Type 1: Classical Universe

The classical universe represents ordinary two-valued mathematical reasoning.

Truth values:

- true
- false

Core assumptions:

- a statement is either true or false
- contradictions are fatal
- the law of excluded middle is accepted
- implication behaves classically

This universe acts as the baseline for comparison.

## Universe Type 2: Intuitionistic Universe

The intuitionistic universe models constructive reasoning.

In this universe, proving a statement matters more than assigning abstract truth to it.

A statement is accepted when there is a construction, witness, or proof.

Important difference from classical logic:

- the law of excluded middle is not automatically accepted
- existence claims require constructive evidence
- proof status is central

This universe allows Project ℵω to compare truth-based reasoning with proof-based reasoning.

## Universe Type 3: Paraconsistent Universe

The paraconsistent universe allows contradictions to exist locally without making every statement derivable.

In classical logic, a contradiction can cause explosion: from contradiction, anything follows.

In a paraconsistent universe, contradiction is contained.

This allows the project to study inconsistent but nontrivial systems.

Possible truth values:

- true
- false
- both true and false
- neither true nor false

This universe is important for studying systems where inconsistency should not automatically destroy all reasoning.

## Universe Type 4: Many-Valued Universe

The many-valued universe allows more than two truth states.

Possible truth values may include:

- true
- false
- unknown
- both
- neither
- unstable

This universe is useful for modeling uncertainty, incomplete information, partial interpretation, and statements whose truth depends on additional context.

## Universe Type 5: Modal Universe

The modal universe studies necessity, possibility, and contingency.

Instead of asking only whether a statement is true, modal reasoning asks whether a statement is necessarily true, possibly true, impossible, or contingent.

Possible modal statuses:

- necessary
- possible
- impossible
- contingent
- unknown

This universe allows the project to study statements across possible worlds or interpretation contexts.

## Universe Type 6: Fuzzy Universe

The fuzzy universe models truth by degree.

Instead of truth being only true or false, truth may be represented by values between 0 and 1.

This is useful for experiments where statements are partially satisfied, approximately true, or graded by confidence.

Example:

- 0.0 means completely false
- 0.5 means partially true or undecided
- 1.0 means completely true

The fuzzy universe allows Project ℵω to study gradual truth behavior.

## Universe Type 7: Experimental Generated Universe

The experimental generated universe is produced by the generative axiom engine.

It may contain unusual axioms, modified inference rules, alternative truth tables, or new consistency policies.

These universes are not assumed to be mathematically valid. They are experimental objects used for computational exploration.

The purpose is to study how different formal assumptions create different logical behavior.

## Universe Metadata

Each universe should eventually store metadata such as:

- logical family
- accepted truth values
- accepted inference rules
- contradiction policy
- expressivity score
- stability score
- translation compatibility
- generated or hand-designed status
- notes about limitations

## Universe Comparison

Project ℵω will eventually compare universes using structural metrics.

Possible metrics:

- truth preservation
- contradiction containment
- inference strength
- expressivity
- translation loss
- semantic distortion
- proof compatibility
- Lean formalization difficulty

## Design Principle

A universe should be simple enough to compute with, but rich enough to reveal meaningful differences between formal systems.

The first versions will be toy universes. This is intentional. Toy universes make the system inspectable, testable, and expandable.

## Summary

The universe layer is the heart of Project ℵω.

It makes mathematical background assumptions explicit. It allows statements to be studied not only by their content, but by the formal worlds in which they are interpreted.

## Phase 3 Implementation Status

The first working version of the Toy Logical Universe layer has now been implemented.

Implemented files:

- src/toy_topoi/truth_values.py
- src/toy_topoi/connectives.py
- src/toy_topoi/universe.py
- src/toy_topoi/library.py
- src/toy_topoi/comparator.py
- experiments/run_universe_comparison.py
- tests/test_toy_topoi.py

Current capabilities:

- define named truth values
- define truth-value spaces
- represent classical, intuitionistic, paraconsistent, many-valued, modal, fuzzy, and generated toy logic families
- represent consistency policies
- apply toy logical connectives such as negation, conjunction, disjunction, and implication
- define formal universes as structured Python objects
- define objects and morphisms inside universes
- load a standard universe library
- compare universes by truth values, inference rules, contradiction support, unknown support, modal support, expressivity, stability, and compatibility
- run a universe comparison experiment
- test the main toy universe components

The implemented universe layer remains a simplified toy model. It is not a complete implementation of topos theory, category theory, modal logic, fuzzy logic, intuitionistic logic, or paraconsistent logic. Its purpose is to make different formal environments computationally visible and comparable.
