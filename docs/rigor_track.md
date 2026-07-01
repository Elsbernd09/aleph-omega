# Mathematical Rigor Track

The Mathematical Rigor Track turns Project ℵω from a computational architecture into a theorem-driven research program.

The purpose of this track is to extract precise mathematical definitions, state theorem candidates, prove finite toy versions, and prepare selected results for future formalization.

---

## Current Theorem Core

The first theorem target is the:

# Finite Bridge Distortion Theorem

Informally:

> If a total bridge translates statements from a finite source universe into a finite target universe, and the source contains a statement requiring a semantic feature absent from the target, then at least one translation is semantically distorted.

This theorem is implemented and documented in:

- `src/rigor/finite_universe.py`
- `src/rigor/bridge.py`
- `src/rigor/distortion.py`
- `src/rigor/theorem.py`
- `tests/test_rigor_finite_universe.py`
- `tests/test_rigor_bridge.py`
- `tests/test_rigor_distortion.py`
- `tests/test_rigor_theorem.py`
- `docs/theorem_target.md`
- `docs/bridge_distortion_proof.md`

---

## Mathematical Objects

The rigor track currently defines:

- finite semantic features
- finite statements
- finite logical universes
- total and partial bridges
- feature mismatch
- semantic preservation
- semantic distortion
- distortion witnesses
- theorem hypotheses
- theorem conclusions
- theorem instance checks

---

## Current Proof Status

The first theorem has:

- a precise finite statement
- executable model objects
- computational theorem checks
- unit tests
- a hand-written proof

The proof is located at:

```text
docs/bridge_distortion_proof.md

## Phase 11: Satisfaction-Based Semantics

Phase 11 strengthens the rigor track by moving beyond semantic feature labels into finite truth-value semantics and satisfaction-based preservation.

Implemented files:

- `src/rigor/semantics.py`
- `src/rigor/interpretation.py`
- `src/rigor/satisfaction.py`
- `src/rigor/preservation.py`
- `src/rigor/preservation_theorem.py`
- `src/rigor/examples.py`
- `tests/test_rigor_semantics.py`
- `tests/test_rigor_interpretation.py`
- `tests/test_rigor_satisfaction.py`
- `tests/test_rigor_preservation.py`
- `tests/test_rigor_preservation_theorem.py`
- `tests/test_rigor_examples.py`
- `docs/satisfaction_preservation_theorem.md`
- `docs/rigor_examples.md`

The main new theorem is the Finite Satisfaction Preservation Theorem:

> A bridge preserves satisfaction exactly when every satisfied source statement has a defined translated target statement that is also satisfied.

This gives the project a stronger semantic core. Distortion is no longer only feature loss; it can also be failure to preserve satisfaction.
