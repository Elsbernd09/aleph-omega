# Project Aleph-Omega Mathlib Export Integration Blueprint

## Purpose

This document starts Phase 32: moving Python-generated Lean exports into the experimental Mathlib track.

Phase 31 proved that Python can generate standalone Lean finite systems and preservation morphisms.

Phase 32 aims to generate artifacts that live inside the Mathlib Lake project and use the existing Mathlib formalization types.

## Summary

- Integration requirements indexed: 8
- Mathlib-targeted requirements: 8

## Requirements

### 1. Reuse Mathlib FormalSystem definition

- Current Phase 31 state: Generated files define their own standalone FormalSystem structure.
- Mathlib target: `AlephOmegaMathlib.FormalSystemCategory.FormalSystem`
- Challenge: Generated standalone files are self-contained and do not import the Mathlib project.
- Planned solution: Generate Mathlib-targeted files that import AlephOmegaMathlib.FormalSystemCategory instead of redefining FormalSystem.

### 2. Reuse Mathlib PreservationMorphism definition

- Current Phase 31 state: Generated morphism file defines its own PreservationMorphism structure.
- Mathlib target: `AlephOmegaMathlib.FormalSystemCategory.PreservationMorphism`
- Challenge: Standalone generated morphisms are not objects of the Mathlib category.
- Planned solution: Emit generated morphisms using the existing Mathlib PreservationMorphism type.

### 3. Generate inside Mathlib namespace

- Current Phase 31 state: Generated files use AlephOmegaGenerated and AlephOmegaGeneratedMorphism namespaces.
- Mathlib target: `AlephOmegaMathlib.Generated namespace`
- Challenge: Names must avoid collisions with hand-written Mathlib artifacts.
- Planned solution: Generate into AlephOmegaMathlib.Generated with deterministic names.

### 4. Place generated files in Mathlib project

- Current Phase 31 state: Generated files are written to formal/generated.
- Mathlib target: `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/`
- Challenge: Generated files must be discovered by the Mathlib Lake build.
- Planned solution: Write generated Mathlib files under the AlephOmegaMathlib library tree and import them from an index file.

### 5. Generate Mathlib-compatible finite systems

- Current Phase 31 state: Generated finite systems compile standalone with Lean.
- Mathlib target: `Mathlib-checked generated FormalSystem definitions.`
- Challenge: The generated file must compile inside the Mathlib Lake project.
- Planned solution: Emit imports and namespace conventions matching the existing experimental Mathlib project.

### 6. Generate Mathlib-compatible preservation morphisms

- Current Phase 31 state: Generated morphism file compiles standalone with Lean.
- Mathlib target: `Mathlib-checked generated PreservationMorphism definitions.`
- Challenge: Preservation proofs must still reduce by finite case analysis after importing Mathlib structures.
- Planned solution: Reuse the same exhaustive proof strategy but target imported Mathlib definitions.

### 7. Import generated file in AlephOmegaMathlib

- Current Phase 31 state: Generated standalone files are not part of AlephOmegaMathlib.lean.
- Mathlib target: `AlephOmegaMathlib.lean imports generated Mathlib export index.`
- Challenge: Generated files should not break normal Mathlib build if regenerated.
- Planned solution: Create stable generated index file and keep deterministic generated outputs.

### 8. Verification script integration

- Current Phase 31 state: check_generated_lean_exports.sh checks standalone generated Lean files.
- Mathlib target: `check_mathlib_scaffold.sh checks generated Mathlib exports through Lake.`
- Challenge: Need to regenerate Mathlib-targeted exports before Lake build.
- Planned solution: Add a dedicated generated-Mathlib export checker before full integration into the Mathlib scaffold.

## First Implementation Target

The first implementation target should generate one Mathlib-compatible finite system file under:

```text
formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/
```

It should import:

```lean
import AlephOmegaMathlib.FormalSystemCategory
```

and define a generated `FormalSystem` using the imported Mathlib-track structure.

## Strongest Claim After This Phase

> Project Aleph-Omega now has a precise plan for moving Python-generated Lean artifacts into its experimental Mathlib category-theory track.

## Non-Claim

This phase does not yet generate Mathlib-integrated Lean files.

The next phase should implement the first Mathlib-targeted finite system exporter.
