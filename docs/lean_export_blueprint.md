# Project Aleph-Omega Python-to-Lean Export Blueprint

## Purpose

This document begins the Python-to-Lean finite model export track.

The goal is to generate Lean finite systems automatically from Python finite semantic data.

## Why This Matters

Project Aleph-Omega already has Python finite semantic systems and hand-written Lean examples.

The next serious upgrade is to connect them by generating Lean definitions from Python data.

That turns the Python layer from a parallel analogue into a producer of machine-checkable Lean artifacts.

## Summary

- Export requirements indexed: 9

## Requirements

### 1. Finite model enumeration

- Python source: `FiniteInstitution.models`
- Lean target: `inductive Model where ...`
- Challenge: Python objects may have arbitrary names not valid as Lean constructors.
- Planned solution: Normalize names into Lean-safe identifiers and preserve original names in comments.

### 2. Finite sentence enumeration

- Python source: `FiniteInstitution.sentences`
- Lean target: `inductive Sentence where ...`
- Challenge: Sentence names may contain symbols or whitespace.
- Planned solution: Generate sanitized constructors such as s0, s1, s2 with comment metadata.

### 3. Satisfaction relation

- Python source: `FiniteModel.satisfies(sentence)`
- Lean target: `Sat := fun m φ => match m, φ with ...`
- Challenge: Need exhaustive finite match cases.
- Planned solution: Emit True for satisfying pairs and False for all other cases.

### 4. Positive satisfaction proofs

- Python source: `pairs where model satisfies sentence`
- Lean target: `theorem exported_model_satisfies_sentence : System.Sat m s := by trivial`
- Challenge: Names must be unique and readable.
- Planned solution: Generate deterministic theorem names from model and sentence indices.

### 5. Negative satisfaction proofs

- Python source: `pairs where model does not satisfy sentence`
- Lean target: `theorem exported_model_not_satisfy_sentence : ¬ System.Sat m s := by intro h; cases h`
- Challenge: False cases must reduce definitionally.
- Planned solution: Use match-defined Sat so negative proofs reduce to False.

### 6. Bridge translation export

- Python source: `FiniteBridge.statement_mapping`
- Lean target: `def exportedTranslate : Source.Sentence -> Target.Sentence`
- Challenge: Partial bridges may not map every sentence.
- Planned solution: First support total bridges; document partial bridge export as future work.

### 7. Model map export

- Python source: `ModelPairing.source_model -> target_model`
- Lean target: `def exportedMapModel : Source.Model -> Target.Model`
- Challenge: Model pairings must be total for Lean function export.
- Planned solution: Require total finite pairings in the first exporter version.

### 8. Preservation morphism export

- Python source: `FiniteInstitutionMorphism`
- Lean target: `def exportedMorphism : PreservationMorphism Source Target`
- Challenge: Need a Lean proof that all satisfying source pairs map to satisfying target pairs.
- Planned solution: Generate proof by exhaustive cases over finite source models and sentences.

### 9. Exporter validation

- Python source: `generated Lean file`
- Lean target: `lean generated_file.lean`
- Challenge: Export is only meaningful if Lean accepts the generated file.
- Planned solution: Add script-level validation that runs Lean on generated artifacts.

## First Export Target

The first exporter should generate a simple finite Lean system with:

- an inductive model type,
- an inductive sentence type,
- a match-defined satisfaction relation,
- positive satisfaction theorems,
- negative satisfaction theorems.

## Later Export Target

The later exporter should generate:

- translations,
- model maps,
- preservation morphisms,
- exhaustive preservation proofs.

## Strongest Claim After This Phase

> Project Aleph-Omega now has a technical blueprint for exporting finite Python semantic systems into Lean finite formal systems.

## Non-Claim

This phase does not yet generate Lean code.

The next phase should implement the first exporter.
