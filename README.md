# Project ℵω / Aleph-Omega

**A finite institution-inspired framework for satisfaction preservation, quotient morphisms, and Lean-checked semantic translation.**

Project Aleph-Omega studies one focused mathematical question:

> When a statement is translated from one formal system into another, what semantic content is preserved?

The repository combines a Python finite-computation layer, a Lean theorem-proving layer, a standalone Lake project scaffold, concrete finite Lean examples, quotient-category-style structure, manuscript documentation, and continuous integration for the formal stack.

## What the Project Does

Project Aleph-Omega builds a finite semantic framework for studying satisfaction preservation.

It defines:

- formal systems with models, sentences, and satisfaction relations,
- translations between systems,
- morphisms that preserve satisfaction,
- failure cases where preservation breaks,
- equivalence classes of morphisms,
- quotient morphisms,
- quotient-style composition,
- a standalone Lean quotient-category-like structure,
- concrete finite Lean examples,
- a Python computational analogue for finite experiments.

## Core Mathematical Idea

A preservation morphism has two parts:

```text
sentence translation:  φ ↦ F(φ)
model map:             m ↦ F(m)
```

The key preservation condition is:

```text
if source model m satisfies source sentence φ,
then target model F(m) satisfies translated sentence F(φ).
```

Symbolically:

```text
A ⊨ φ     implies     F(A) ⊨ F(φ)
```

## Lean Formalization

The Lean Formalization is located at:

```text
formal/lean/AlephOmegaCore.lean
```

The Lean core includes:

- `FormalSystem`
- `PreservationMorphism`
- `identity_preserves_satisfaction`
- `composition_preserves_satisfaction`
- `MorphismEquivalent`
- `QuotientMorphism`
- quotient composition
- quotient identity laws
- quotient associativity
- `AlephOmegaQuotientCategory`
- concrete finite systems: `TwoSystem`, `RenamedTwoSystem`, and `ThirdTwoSystem`
- concrete nontrivial preservation morphisms
- a concrete preservation chain
- quotient integration for the concrete chain

The strongest careful Lean claim is:

> Project ℵω contains a Lean-checked concrete finite preservation pipeline across three explicit formal systems, including nontrivial preservation morphisms, a nontrivial composition chain, and integration of that chain into a standalone quotient-category-like structure.

## Python Layer

The Python Layer is located in:

```text
src/rigor/
```

It implements finite computational analogues of the formal ideas, including:

- finite logical universes,
- finite institution-like systems,
- bridge translations,
- satisfaction preservation checkers,
- failure taxonomies,
- theorem inventories,
- quotient morphism analogues,
- quotient category checks,
- Lean/Python correspondence reports,
- manuscript generation utilities.

The Python layer should be read as a finite computational laboratory, not as a full proof assistant.

## Lake Project

The Lean formalization is also packaged as a standalone Lake project:

```text
formal/aleph_omega_lake/
```

Build it with:

```bash
./scripts/check_lake.sh
```

## Formal Stack Verification

To verify the full formal stack locally, run:

```bash
./scripts/check_formal_stack.sh
```

This checks:

- the primary Lean formalization,
- Lake synchronization,
- the Lake project build,
- the Python test suite.

## Continuous Integration

The repository includes GitHub Actions CI:

```text
.github/workflows/formal-stack.yml
```

The workflow verifies the Lean, Lake, synchronization, and Python formal stack on pushes and pull requests to `main`.

## Manuscript Package

The project includes a research manuscript layer:

```text
docs/project_aleph_omega_manuscript.md
docs/manuscript_theorem_inventory.md
docs/manuscript_figures.md
docs/manuscript_front_matter.md
docs/manuscript_completion_report.md
```

These documents explain the project’s definitions, theorem flow, architecture, contribution boundaries, and limitations.

## Key Documentation

Important reviewer-facing documents:

```text
docs/formal_claim_upgrade.md
docs/lean_formalization_index.md
docs/concrete_lean_completion_report.md
docs/correspondence_completion_report.md
docs/lean_packaging_completion_report.md
docs/manuscript_completion_report.md
```

## What This Project Is

Project ℵω is:

- a finite formal-methods research artifact,
- a semantic preservation laboratory,
- a Lean-supported quotient-category prototype,
- a bridge between finite computation and proof-assistant formalization,
- a serious mathematical-computation project.

## What This Project Is Not

Project ℵω is not yet:

- a universal theory of institutions,
- a proof about all logics,
- a full Mathlib `Category` instance,
- a complete Lean verification of every Python function,
- a solved open problem,
- a field-changing theorem.

Those are future directions, not current claims.

## Running the Project

Run the Python test suite:

```bash
python3 -m pytest
```

Check the Lean core:

```bash
./scripts/check_lean.sh
```

Build the Lake project:

```bash
./scripts/check_lake.sh
```

Run the full formal stack:

```bash
./scripts/check_formal_stack.sh
```

## Repository Structure

```text
formal/
  lean/
    AlephOmegaCore.lean
  aleph_omega_lake/
    lakefile.lean
    AlephOmega.lean
    AlephOmega/
      AlephOmegaCore.lean

src/
  rigor/
    finite semantic and formal-reporting modules

tests/
  Python test suite

docs/
  manuscript, theorem inventory, reports, and reviewer documentation

scripts/
  Lean, Lake, sync, and formal-stack verification scripts
```

## Current Best Framing

The most accurate public description is:

> Project ℵω is a finite institution-inspired, Lean-supported research framework for studying satisfaction preservation under semantic translation. It includes a Python computational layer, a Lean-checked quotient-category-style formal core, concrete finite Lean examples, and a manuscript package that separates formal claims from computational analogues and explicit non-claims.

## License

Add a license before public release if one is not already present.

## Public Release Index

A reviewer-facing map of the documentation package is available at:

```text
docs/public_release_index.md
```

This index tells readers where to start, which documents contain the exact claims, and how to verify the formal stack.

## Quickstart

A reviewer-facing setup and verification guide is available at:

```text
docs/quickstart.md
```

The fastest complete verification command is:

```bash
./scripts/check_formal_stack.sh
```

## Verification Status

A reviewer-facing verification status page is available at:

```text
docs/verification_status.md
```

It separates Lean-checked results, Python-tested computational results, CI-checked infrastructure, and explicit non-claims.

## Public Release Completion Report

The public release package is summarized at:

```text
docs/public_release_completion_report.md
```

## PhD-Level Strengthening Track

The next research-strengthening track begins with Mathlib integration feasibility:

```text
docs/mathlib_integration_feasibility.md
```

This document analyzes what would be required to upgrade the standalone quotient-category-like Lean structure into a real Mathlib-compatible category instance.

### Phase 29B: Experimental Mathlib Scaffold

Project ℵω now includes a separate experimental Mathlib Lake project for future category-theory integration.

New location:

```text
formal/aleph_omega_mathlib/
```

Checker:

```bash
./scripts/check_mathlib_scaffold.sh
```

Careful claim:

> Project ℵω now has a separate experimental Mathlib scaffold. This is not yet a Mathlib Category instance for the main Aleph-Omega formalization.

### Phase 29C: Mathlib Category Smoke Instance

Project ℵω now includes an experimental Mathlib project with a real smoke-test `Category` instance.

Artifact:

```text
formal/aleph_omega_mathlib/AlephOmegaMathlib/CategorySmokeTest.lean
```

Careful claim:

> Project ℵω can now define and build a real Mathlib `Category` instance in its experimental Mathlib scaffold. This is not yet the Aleph-Omega quotient category instance.

### Phase 29D: Mathlib Formal System Category

Project ℵω now includes an experimental Mathlib `Category` instance for formal systems and satisfaction-preserving morphisms.

Artifact:

```text
formal/aleph_omega_mathlib/AlephOmegaMathlib/FormalSystemCategory.lean
```

Careful claim:

> Project ℵω now has a real Mathlib category instance for the direct preservation-morphism structure. This is not yet the quotient category instance.

### Phase 29E: Mathlib Direct Category Completion Report

Project ℵω now includes a completion report for its first serious Mathlib category-theory milestone.

Artifact:

```text
docs/mathlib_direct_category_completion_report.md
```

Careful claim:

> Project ℵω now contains an experimental Mathlib project with a real Category instance whose objects are formal systems and whose morphisms are satisfaction-preserving morphisms. This is still not yet the quotient category instance.

### Phase 30A: Mathlib Quotient Category Blueprint

Project ℵω now includes a technical blueprint for upgrading the direct Mathlib preservation-morphism category into a quotient category.

Artifact:

```text
docs/mathlib_quotient_category_blueprint.md
```

Careful claim:

> Project ℵω now has a detailed technical plan for a real Mathlib quotient category whose morphisms are equivalence classes of satisfaction-preserving morphisms. The quotient category instance itself is the next target.

### Phase 30B: Mathlib Quotient Category Prototype

Project ℵω now includes an experimental Mathlib quotient category prototype.

Artifact:

```text
formal/aleph_omega_mathlib/AlephOmegaMathlib/QuotientFormalSystemCategory.lean
```

Careful claim:

> Project ℵω now contains an experimental Mathlib quotient category prototype whose morphisms are quotient classes of satisfaction-preserving morphisms. This should still be reviewed carefully before being treated as final.

### Phase 30C: Mathlib Quotient Category Completion Report

Project ℵω now includes a completion report for the experimental Mathlib quotient category prototype.

Artifact:

```text
docs/mathlib_quotient_category_completion_report.md
```

Careful claim:

> Project ℵω now contains an experimental Mathlib quotient category prototype whose morphisms are quotient classes of satisfaction-preserving morphisms, with representative-independent composition and a real Mathlib `Category` instance. It remains an experimental prototype pending cleanup and expert review.

### Phase 30D: Standalone-to-Mathlib Correspondence Report

Project ℵω now includes a correspondence report connecting the original standalone Lean core to the experimental Mathlib quotient category prototype.

Artifact:

```text
docs/mathlib_correspondence_report.md
```

Careful claim:

> Project ℵω now has a documented correspondence between its standalone Lean quotient-category core and its experimental Mathlib quotient category prototype. The two tracks are not yet definitionally unified.

### Phase 30E: Mathlib Concrete Three-System Chain

Project ℵω now ports the concrete three-system preservation chain into the experimental Mathlib quotient-category track.

Artifact:

```text
formal/aleph_omega_mathlib/AlephOmegaMathlib/ConcreteChain.lean
```

Careful claim:

> Project ℵω now has a concrete three-system preservation chain inside the experimental Mathlib quotient-category prototype.

### Phase 30F: Mathlib Strengthening Completion Report

Project ℵω now includes a completion report for the PhD-level Mathlib strengthening track.

Artifact:

```text
docs/mathlib_strengthening_completion_report.md
```

Careful claim:

> Project ℵω now has an experimental Mathlib category-theory track with a direct category, a quotient category prototype, representative-independent quotient composition, and a concrete three-system preservation chain.

### Phase 31A: Python-to-Lean Export Blueprint

Project ℵω now begins the Python-to-Lean finite model export track.

Artifact:

```text
docs/lean_export_blueprint.md
```

Careful claim:

> Project ℵω now has a technical blueprint for exporting finite Python semantic systems into Lean finite formal systems.

### Phase 31B: Python-to-Lean Finite System Exporter

Project ℵω now includes its first Python-to-Lean exporter for finite formal systems.

Artifacts:

```text
src/rigor/lean_finite_system_exporter.py
formal/generated/ExportedTinySystem.lean
docs/lean_finite_system_exporter.md
```

Careful claim:

> Project ℵω now has a Python-to-Lean exporter that generates a finite formal system with Lean-checkable satisfaction facts.

### Phase 31C: Python-to-Lean Preservation Morphism Exporter

Project ℵω now includes a Python-to-Lean exporter for finite satisfaction-preserving morphisms.

Artifacts:

```text
src/rigor/lean_morphism_exporter.py
formal/generated/ExportedTinyMorphism.lean
docs/lean_morphism_exporter.md
```

Careful claim:

> Project ℵω now has a Python-to-Lean exporter that generates Lean-checkable finite satisfaction-preserving morphisms.

### Phase 31D: Generated Lean Export Verification

Project ℵω now includes a script that regenerates Python-to-Lean exports and checks them with Lean.

Artifact:

```text
scripts/check_generated_lean_exports.sh
docs/generated_lean_export_verification.md
```

Command:

```bash
./scripts/check_generated_lean_exports.sh
```

Careful claim:

> Project ℵω now has reproducible Python-generated Lean finite-system and preservation-morphism exports verified by Lean.

### Phase 31E: Generated Lean Exports Integrated into Formal Stack

Project ℵω now verifies Python-generated Lean exports inside the main formal-stack gate.

Artifacts:

```text
scripts/check_formal_stack.sh
scripts/check_generated_lean_exports.sh
tests/test_rigor_formal_stack_generated_exports.py
```

Careful claim:

> Project ℵω now includes reproducible Python-generated Lean exports as part of its official formal verification pipeline.

### Phase 31F: Python-to-Lean Export Completion Report

Project ℵω now includes a completion report for the Python-to-Lean finite export pipeline.

Artifact:

```text
docs/lean_export_completion_report.md
```

Careful claim:

> Project ℵω now has a Python-to-Lean export pipeline that generates finite Lean formal systems and finite satisfaction-preserving morphisms from Python data, then verifies the generated Lean artifacts inside the formal-stack gate.

### Phase 32A: Mathlib Export Integration Blueprint

Project ℵω now begins the track for moving Python-generated Lean artifacts into the experimental Mathlib category-theory project.

Artifact:

```text
docs/mathlib_export_integration_blueprint.md
```

Careful claim:

> Project ℵω now has a precise plan for moving Python-generated Lean artifacts into its experimental Mathlib category-theory track.

### Phase 32B: Mathlib-Targeted Finite System Exporter

Project ℵω now has a Python exporter that generates finite FormalSystem artifacts directly inside the experimental Mathlib category-theory track.

Artifacts:

```text
src/rigor/mathlib_finite_system_exporter.py
formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibSystem.lean
docs/mathlib_finite_system_exporter.md
```

Careful claim:

> Project ℵω now has a Python exporter that generates finite FormalSystem artifacts directly inside the experimental Mathlib category-theory track.

### Phase 32C: Mathlib-Targeted Preservation Morphism Exporter

Project ℵω now has a Python exporter that generates finite PreservationMorphism artifacts directly inside the experimental Mathlib category-theory track.

Artifacts:

```text
src/rigor/mathlib_morphism_exporter.py
formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibMorphism.lean
docs/mathlib_morphism_exporter.md
```

Careful claim:

> Project ℵω now has a Python exporter that generates finite PreservationMorphism artifacts directly inside the experimental Mathlib category-theory track.

### Phase 32D: Generated Mathlib Export Verification

Project ℵω now includes a script that regenerates Python-produced Mathlib-track exports and verifies them through the experimental Mathlib Lake build.

Artifacts:

```text
scripts/check_generated_mathlib_exports.sh
docs/generated_mathlib_export_verification.md
```

Command:

```bash
./scripts/check_generated_mathlib_exports.sh
```

Careful claim:

> Project ℵω now has a reproducible script that regenerates Python-produced Mathlib finite-system and preservation-morphism exports and verifies them through the experimental Mathlib Lake build.

### Phase 32E: Generated Mathlib Exports Integrated into Formal Stack

Project ℵω now verifies Python-generated Mathlib exports inside the main formal-stack gate.

Artifacts:

```text
scripts/check_formal_stack.sh
scripts/check_generated_mathlib_exports.sh
tests/test_rigor_formal_stack_generated_mathlib_exports.py
```

Careful claim:

> Project ℵω now includes reproducible Python-generated Mathlib finite-system and preservation-morphism exports as part of its official formal verification pipeline.

### Phase 32F: Generated Mathlib Export Completion Report

Project ℵω now includes a completion report for the Python-to-Mathlib export pipeline.

Artifact:

```text
docs/mathlib_export_completion_report.md
```

Careful claim:

> Project ℵω now has a Python-to-Mathlib export pipeline that generates finite FormalSystem and PreservationMorphism artifacts directly inside the experimental Mathlib category-theory track and verifies them through the formal-stack gate.

### Phase 33A: Generated Quotient Category Export Blueprint

Project ℵω now begins the generated quotient-category export track.

Artifact:

```text
docs/generated_quotient_export_blueprint.md
```

Careful claim:

> Project ℵω now has a precise plan for generating quotient-category artifacts from Python-produced Mathlib preservation morphisms.

### Phase 33B: Generated Quotient Wrapper Exporter

Project ℵω now has a Python exporter that generates quotient-category wrapper artifacts for Python-produced Mathlib preservation morphisms.

Artifacts:

```text
src/rigor/mathlib_quotient_wrapper_exporter.py
formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibQuotient.lean
docs/mathlib_quotient_wrapper_exporter.md
```

Verification update:

```text
scripts/check_generated_mathlib_exports.sh now regenerates and verifies the generated quotient wrapper.
```

Careful claim:

> Project ℵω now has a Python exporter that generates quotient-category wrapper artifacts for Python-produced Mathlib preservation morphisms and verifies them through the generated Mathlib export checker.

### Phase 33C: Generated Quotient Composition Exporter

Project ℵω now generates a quotient-category composition theorem inside the experimental Mathlib track.

Artifacts:

```text
src/rigor/mathlib_quotient_composition_exporter.py
formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/ExportedTinyMathlibQuotientComposition.lean
docs/mathlib_quotient_composition_exporter.md
```

Careful claim:

> Project ℵω now generates a finite quotient-category composition theorem inside the experimental Mathlib category-theory track.
