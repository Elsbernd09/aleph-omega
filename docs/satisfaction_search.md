# Satisfaction Preservation Stress Search

## Purpose

Phase 14D stress-tests satisfaction preservation across generated finite models.

The search generates:

- finite logical universes
- bridge cases
- truth-value interpretations
- preservation reports

This moves the project from hand-picked examples toward systematic finite model testing.

---

## What Is Being Tested

For a bridge F from U to V, the search asks:

If a source statement is satisfied in U, does its translated target statement remain satisfied in V?

If yes, satisfaction is preserved.

If no, satisfaction distortion appears.

---

## Generated Interpretations

For each finite universe, the search generates all classical true/false assignments over its finite statement set.

For a universe with n statements, this produces 2^n interpretations.

---

## Generated Bridge Cases

The search reuses the richer Phase 14B bridge generator.

It checks:

- identity bridges
- collapse bridges
- empty partial bridges
- same-feature bridges

---

## Reported Metrics

The search reports:

- total cases
- preserving cases
- distortion cases
- preservation rate
- distortion rate
- cases by bridge kind

---

## Correct Research Claim

A careful claim is:

In the generated finite search space, the system measures exactly which generated bridges preserve satisfaction and which generate satisfaction distortion.

This is not a universal theorem about all logics.

It is a finite computational stress test of the Project Aleph-Omega satisfaction semantics layer.

---

## Why This Matters

This phase makes the project stronger because it adds systematic finite experimentation.

Instead of only saying that a theorem works on examples, the project now generates many finite cases and records when preservation succeeds or fails.

That creates a stronger mathematical workflow:

1. define semantics
2. define preservation
3. generate finite models
4. generate finite bridges
5. generate interpretations
6. measure preservation and distortion
