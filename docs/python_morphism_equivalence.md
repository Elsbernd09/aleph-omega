# Python-Side Morphism Equivalence

## Purpose

Phase 24B adds a Python-side analogue of the Lean definition MorphismEquivalent.

The goal is to make the Python implementation correspond more closely to the Lean formal core.

## Definition

Two finite institution morphisms are Python-equivalent when:

- they have the same source institution
- they have the same target institution
- they translate every source sentence to the same target sentence
- they have the same source-model to target-model pairing signature

## Lean Correspondence

The Lean definition is:

MorphismEquivalent

The Python implementation is:

PythonMorphismEquivalenceChecker

## Why This Matters

The Lean layer already proves laws about morphism equivalence.

This phase gives the Python layer a matching computational concept.

That makes the Lean/Python correspondence sharper.

## Correct Research Claim

Project Aleph-Omega now implements a Python-side morphism equivalence checker corresponding to the Lean MorphismEquivalent definition.

This does not mean the Python checker itself is machine-verified by Lean.
