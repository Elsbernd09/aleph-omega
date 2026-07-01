# Failure Taxonomy

## Purpose

Phase 15 adds a failure taxonomy to Project Aleph-Omega.

A serious theorem system should not only show successful cases.

It should also explain how failure occurs.

---

## Failure Kinds

The taxonomy classifies generated bridge and satisfaction failures into:

- no failure
- undefined translation
- target not satisfied
- feature mismatch
- partial bridge failure
- collapse distortion
- multiple failures

---

## Structural Failures

A structural bridge failure happens before truth values are considered.

Examples:

- a bridge is partial
- a bridge has no translation for some source statement
- a bridge maps a statement to a target with incompatible semantic features

---

## Satisfaction Failures

A satisfaction failure happens when a source statement is satisfied but the bridge fails to preserve that satisfaction.

Examples:

- the satisfied source statement has no target translation
- the target translation exists but is not satisfied
- collapse identifies statements in a way that loses truth preservation

---

## Why This Matters

Phase 14 searched for preservation and distortion.

Phase 15 explains the failure modes.

This makes the project more research-like because it distinguishes:

- theorem success
- vacuous success
- structural failure
- semantic failure
- distortion caused by collapse
- distortion caused by undefined translation

---

## Correct Research Claim

Project Aleph-Omega can now say:

The finite search layer not only measures preservation and distortion, but also classifies generated failure cases according to a finite taxonomy.

This is a finite model-bound analysis, not a universal classification of all possible mathematical failure modes.
