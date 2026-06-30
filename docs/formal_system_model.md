# Formal System Model

This document defines the conceptual model behind Project ℵω.

Project ℵω treats formal mathematical environments as computational objects. Instead of assuming one fixed background logic, the project represents axioms, inference rules, truth values, propositions, objects, morphisms, and translations as data structures.

This file is a design specification for the mathematical objects that later Python and Lean modules will represent.

## Core Objects

The main objects are:

- FormalSystem
- Axiom
- InferenceRule
- TruthValueSpace
- Statement
- Universe
- Morphism
- Bridge
- InterpretationContext

## Formal System

A formal system is a structured environment in which mathematical statements can be formed, interpreted, and reasoned about.

A formal system contains a language, axioms, inference rules, a truth value space, an interpretation context, a consistency policy, and an expressivity profile.

## Axiom

An axiom is a starting assumption inside a system. Project ℵω does not treat generated axioms as automatically true. It treats them as experimental assumptions whose consequences can be explored.

## Inference Rule

An inference rule specifies how new statements can be derived from existing statements. Different universes may allow different inference rules.

## Truth Value Space

A truth value space defines the possible truth states of propositions. Classical logic uses true and false. Paraconsistent and many-valued systems may allow values such as both, neither, or unknown.

## Statement

A statement is a proposition, claim, formula, or symbolic expression that can be interpreted inside a formal universe.

## Universe

A universe is a modeled formal context containing objects, statements, axioms, inference rules, and an internal truth system.

## Morphism

A morphism is a structure-preserving relationship between objects, statements, axiom systems, or entire universes.

## Bridge

A bridge is a translation mechanism between universes. It studies what happens to a statement when it moves from one formal universe to another.

## Interpretation Context

An interpretation context gives meaning to symbols. The same symbolic statement may mean different things under different contexts.

## Summary

Project ℵω treats formal systems as computational objects. Axioms become data. Inference rules become data. Truth spaces become data. Universes become data. Translations become data. Proof sketches become data.
