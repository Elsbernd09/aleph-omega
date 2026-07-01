# Lean/Python Formal Correspondence Manifest

## Purpose

This document connects the Project Aleph-Omega Python implementation to the Lean formalization core.

The purpose is to avoid overclaiming.

Lean proves the abstract theorem core.

Python implements finite computational models.

The correspondence layer explains how the two relate.

## Summary

- Correspondence entries: 10
- Lean-checked entries: 6
- Python-implemented entries: 6

## Correspondence Entries

### 1. Finite logical system

- Python artifact: `src/rigor/finite_universe.py`
- Lean artifact: `FormalSystem`
- Documentation artifact: `docs/lean_core_formalization.md`
- Status: Python-implemented and Lean-defined

Limitation: The Lean FormalSystem is abstract and does not directly encode all fields of FiniteLogicalUniverse.

### 2. Satisfaction relation

- Python artifact: `src/rigor/finite_institution.py`
- Lean artifact: `FormalSystem.Sat`
- Documentation artifact: `docs/finite_institution.md`
- Status: Python-implemented and Lean-defined

Limitation: Python computes satisfaction through finite interpretations; Lean abstracts satisfaction as a relation.

### 3. Satisfaction-preserving morphism

- Python artifact: `src/rigor/institution_morphism.py`
- Lean artifact: `PreservationMorphism`
- Documentation artifact: `docs/institution_morphism.md`
- Status: Python-implemented and Lean-defined

Limitation: Python checks preservation over finite witnesses; Lean stores preservation as a proof field.

### 4. Identity preservation

- Python artifact: `src/rigor/institution_satisfaction_theorem.py`
- Lean artifact: `identity_preserves_satisfaction`
- Documentation artifact: `docs/lean_formalization_index.md`
- Status: Lean-checked prototype

Limitation: The Lean theorem applies to the abstract formal core, not the entire Python implementation.

### 5. Composition preservation

- Python artifact: `src/rigor/institution_category.py`
- Lean artifact: `composition_preserves_satisfaction`
- Documentation artifact: `docs/lean_formalization_index.md`
- Status: Lean-checked prototype

Limitation: The Lean theorem proves the abstract preservation pattern; Python composition has additional implementation details.

### 6. Failure boundary

- Python artifact: `src/rigor/failure_taxonomy.py`
- Lean artifact: `preservation_not_automatic`
- Documentation artifact: `docs/lean_failure_boundary.md`
- Status: Python-implemented taxonomy and Lean-checked counterexample

Limitation: Lean proves one concrete BoolSystem counterexample, not completeness of the Python failure taxonomy.

### 7. Morphism equivalence

- Python artifact: `none`
- Lean artifact: `MorphismEquivalent`
- Documentation artifact: `docs/lean_morphism_equivalence.md`
- Status: Lean-defined and Lean-checked laws

Limitation: The Python layer does not yet implement morphism equivalence as a first-class object.

### 8. Quotient morphisms

- Python artifact: `none`
- Lean artifact: `QuotientMorphism`
- Documentation artifact: `docs/lean_setoid_quotient.md`
- Status: Lean-defined

Limitation: The quotient hom-type currently exists only in Lean.

### 9. Quotient composition

- Python artifact: `none`
- Lean artifact: `quotientCompose`
- Documentation artifact: `docs/lean_quotient_compose_operation.md`
- Status: Lean-defined and Lean-checked laws

Limitation: The quotient composition operation is not mirrored in Python.

### 10. Standalone quotient category

- Python artifact: `none`
- Lean artifact: `AlephOmegaQuotientCategory`
- Documentation artifact: `docs/standalone_category_completion_report.md`
- Status: Lean-defined structure with Lean-checked laws

Limitation: This is a standalone Lean category-like structure, not a Mathlib Category instance.

## Strongest Correct Claim

The strongest careful claim is:

> Project Aleph-Omega contains a Python implementation of finite semantic systems and a Lean-checked abstract formal core. The correspondence manifest identifies which computational concepts correspond to which Lean definitions and theorems.

## Important Limitation

The Python implementation is not fully machine-verified.

The Lean formalization proves the abstract mathematical core.

The correspondence between Python and Lean is documented and tested as an artifact, but not yet itself formally verified.

## Next Research Step

The next serious step is to make this correspondence sharper by either:

1. implementing Python-side morphism equivalence and quotient operations, or
2. moving the finite Python structures into Lean as concrete finite examples.

## Phase 24B Update: Python-Side Morphism Equivalence

The Python implementation now includes a computational analogue of the Lean `MorphismEquivalent` definition.

New artifacts:

- `src/rigor/python_morphism_equivalence.py`
- `tests/test_rigor_python_morphism_equivalence.py`
- `docs/python_morphism_equivalence.md`

Careful claim:

> Project Aleph-Omega now has both a Lean definition of morphism equivalence and a Python-side checker for extensional equivalence of finite institution morphisms.

## Phase 24D Update: Python-Side Quotient Category

The Python implementation now includes a computational analogue of the Lean standalone quotient category.

New artifacts:

- `src/rigor/python_quotient_category.py`
- `tests/test_rigor_python_quotient_category.py`
- `docs/python_quotient_category.md`

Careful claim:

> Project Aleph-Omega now has both a Lean standalone quotient category structure and a Python-side computational quotient category analogue for finite institution-like systems.
