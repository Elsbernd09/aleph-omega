# Failure Laboratory Layer

## Purpose

Phase 15 adds a failure laboratory to Project Aleph-Omega.

The goal is to study not only theorem success, but also theorem boundaries and generated semantic failures.

A serious mathematical system should explain:

- when preservation succeeds
- when preservation holds vacuously
- when assumptions fail
- when structure fails
- when semantic distortion appears

---

## Implemented Files

Phase 15 added:

- src/rigor/failure_taxonomy.py
- src/rigor/failure_extractor.py
- src/rigor/failure_report.py
- src/rigor/theorem_boundary.py

with tests:

- tests/test_rigor_failure_taxonomy.py
- tests/test_rigor_failure_extractor.py
- tests/test_rigor_failure_report.py
- tests/test_rigor_theorem_boundary.py

and docs:

- docs/failure_taxonomy.md
- docs/failure_extractor.md
- docs/failure_lab_report.md
- docs/theorem_boundary_analysis.md
- docs/failure_lab.md

---

## Failure Taxonomy

The taxonomy classifies generated failure cases into finite kinds:

- no failure
- undefined translation
- target not satisfied
- feature mismatch
- partial bridge failure
- collapse distortion
- multiple failures

This lets the project describe why preservation fails.

---

## Failure Extractor

The failure extractor scans generated satisfaction search cases and extracts cases where satisfaction distortion occurs.

These are counterexample-like cases.

They are not always formal theorem counterexamples.

Instead, they often show that a theorem hypothesis failed or that a semantic boundary was reached.

---

## Failure Laboratory Report

The failure report turns extracted failures into a readable research artifact.

It includes:

- total extracted failures
- counts by failure kind
- sample failure cases
- theorem-boundary interpretation
- careful research framing

Generate the report by running:

python3 -m src.rigor.failure_report

This writes:

docs/failure_lab_report.md

---

## Theorem Boundary Analysis

The theorem boundary analyzer separates generated cases into:

- verified preservation
- vacuous preservation
- hypothesis failure
- semantic distortion
- structural failure

This is important because not every successful case is equally strong.

A vacuous success is logically valid but weaker than verified preservation.

A hypothesis failure is not the same as a theorem counterexample.

A structural failure is different from semantic distortion.

---

## Correct Research Framing

Project Aleph-Omega can now honestly claim:

The finite search layer extracts, classifies, and reports generated semantic failure cases, while theorem-boundary analysis distinguishes verified preservation, vacuous preservation, hypothesis failure, structural failure, and semantic distortion.

This remains finite, computational, and model-bound.

---

## Why Phase 15 Matters

Phase 15 makes the project more serious because it studies failure instead of hiding it.

The workflow is now:

1. define theorem claims
2. generate finite models
3. test preservation and distortion
4. extract failure cases
5. classify failure mechanisms
6. analyze theorem boundaries
7. report results carefully

This is a stronger research process than only presenting successful examples.
