# Project Aleph-Omega Standalone-to-Mathlib Correspondence Report

## Purpose

This report explains how the original standalone Lean formal core corresponds to the experimental Mathlib quotient category prototype.

The project now has two formal tracks:

1. the original standalone Lean core,
2. the experimental Mathlib category-theory track.

## Summary

- Correspondence entries: 11
- Strong correspondence entries: 8
- Partial correspondence entries: 2

## Correspondence Table

| Concept | Standalone artifact | Mathlib artifact | Correspondence | Status | Limitation |
|---|---|---|---|---|---|
| Formal system | `FormalSystem in formal/lean/AlephOmegaCore.lean` | `FormalSystem in FormalSystemCategory.lean` | Both define systems with models, sentences, and a satisfaction relation. | strong correspondence | They are separate Lean definitions, not definitionally identical. |
| Satisfaction-preserving morphism | `PreservationMorphism` | `PreservationMorphism` | Both use sentence translation, model map, and a preservation proof. | strong correspondence | They live in separate Lean files/projects. |
| Identity morphism | `identityMorphism` | `identityPreservation` | Both represent the satisfaction-preserving identity morphism. | strong correspondence | Naming and implementation details differ. |
| Composition | `composeMorphism` | `composePreservation` | Both compose sentence translation and model maps while preserving satisfaction. | strong correspondence | Composition is adapted to Mathlib category conventions in the Mathlib track. |
| Direct category | `StandaloneQuotientCategory was quotient-focused, not direct raw morphism category.` | `formalSystemCategory` | The Mathlib track adds a real direct Category instance absent from the original standalone layer. | new Mathlib strengthening | This is an added formalization, not a one-to-one migration. |
| Morphism equivalence | `MorphismEquivalent` | `PreservationEquivalent` | Both identify morphisms by translation and model-map behavior, ignoring proof-field differences. | strong correspondence | The Mathlib version is rebuilt for the experimental project. |
| Quotient morphism | `QuotientMorphism / QuotientHom` | `QuotientPreservationHom` | Both represent quotient classes of satisfaction-preserving morphisms. | strong correspondence | The Mathlib version uses the new FormalSystemCategory definitions. |
| Representative-independent composition | `quotient_composition_well_defined` | `compose_preservation_respects_equivalence` | Both prove that composition respects morphism equivalence. | strong correspondence | The proof names and exact theorem shapes differ. |
| Quotient category | `AlephOmegaQuotientCategory` | `quotientFormalSystemCategory` | Both package quotient homs, identity, composition, and category laws. | strong conceptual correspondence | The Mathlib prototype uses a wrapper object type to avoid category-instance conflicts. |
| Concrete finite examples | `TwoSystem / RenamedTwoSystem / ThirdTwoSystem` | `BoolFormalSystem / QuotientBoolFormalSystem` | Both contain finite concrete examples, but the examples are not the same yet. | partial correspondence | Future work should port the three-system concrete chain into the Mathlib project. |
| CI verification | `./scripts/check_formal_stack.sh` | `./scripts/check_mathlib_scaffold.sh` | Both tracks have local verification commands. | partial correspondence | The Mathlib scaffold is not yet integrated into the main GitHub Actions formal-stack workflow. |

## Strongest Current Correspondence Claim

> Project Aleph-Omega now has a documented correspondence between its original standalone Lean quotient-category core and its experimental Mathlib quotient category prototype.

## Important Boundary

The two tracks are not yet definitionally unified.

The Mathlib track is a reconstruction and strengthening of the standalone ideas inside Mathlib infrastructure.

## Next Serious Step

The next phase should port the concrete three-system Lean chain into the experimental Mathlib project, so the Mathlib track has the same concrete example strength as the standalone core.
