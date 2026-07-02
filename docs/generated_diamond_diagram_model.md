# Generated Diamond Diagram Data Model

## Purpose

Phase 35C defines the Python data model for a generated finite diamond diagram.

The diamond has two distinct paths from a source system to a target system.

```text
        B
      /   \
A           D
      \   /
        C
```

## Summary

- Diagram name: StandardGeneratedDiamond
- Systems: 4
- Morphisms: 4
- Paths agree on models: True
- Paths agree on sentences: True

## Systems

- DiamondSystemA
- DiamondSystemB
- DiamondSystemC
- DiamondSystemD

## Morphisms

- DiamondMorphismAB: DiamondSystemA -> DiamondSystemB
- DiamondMorphismAC: DiamondSystemA -> DiamondSystemC
- DiamondMorphismBD: DiamondSystemB -> DiamondSystemD
- DiamondMorphismCD: DiamondSystemC -> DiamondSystemD

## Path Agreement

The upper path A -> B -> D and lower path A -> C -> D agree pointwise on:

- source models,
- source sentences.

This prepares the Lean/Mathlib theorem that the two paths are equal as quotient morphisms.

## Strongest Claim

> Project Aleph-Omega now has a Python data model for a generated finite diamond diagram whose two distinct paths agree pointwise on models and sentence translations.

## Boundary

This phase defines the Python diamond data model only.

The next phase should export this diamond into Mathlib and prove quotient path equivalence.
