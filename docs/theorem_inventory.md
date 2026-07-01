# Theorem Inventory

## Purpose

This document lists the theorem-like claims registered in Project Aleph-Omega.

It separates finite verified claims from conjectural generalizations.

## Summary

- Inventory items: 5
- Strongly verified items: 3
- Conjectural items: 1

## Inventory

### claim.bridge_distortion.finite

- Title: Finite Bridge Distortion Theorem
- Scope: finite_model
- Verification level: stress_tested
- Strongly verified: True
- Conjectural: False

Statement:

Within the implemented finite bridge model, bridges that fail structural preservation can be detected as distortion-bearing or vacuous instances according to the theorem checker.

Evidence:

- src/rigor/theorem.py
- src/rigor/bridge_distortion_search.py
- tests/test_rigor_bridge_distortion_search.py
- docs/bridge_distortion_search.md

Limitations:

- Finite model only.
- Does not prove a theorem about all logics or all categories.

### claim.satisfaction_preservation.finite

- Title: Finite Satisfaction Preservation
- Scope: finite_model
- Verification level: tested_by_unit_tests
- Strongly verified: False
- Conjectural: False

Statement:

Within the implemented finite semantics, satisfaction preservation can be measured by checking whether satisfied source statements translate to satisfied target statements.

Evidence:

- src/rigor/preservation.py
- src/rigor/preservation_theorem.py
- tests/test_rigor_preservation.py
- tests/test_rigor_preservation_theorem.py

Limitations:

- Uses finite truth-value interpretations.
- Does not cover arbitrary model theory.

### claim.composition_preservation.finite

- Title: Finite Composition Preservation
- Scope: finite_model
- Verification level: finite_proof
- Strongly verified: True
- Conjectural: False

Statement:

If two composable finite bridges preserve satisfaction under compatible interpretations, then their composite preserves satisfaction in the implemented finite model.

Evidence:

- src/rigor/composition_preservation_theorem.py
- docs/composition_preservation_theorem.md
- tests/test_rigor_composition_preservation_theorem.py

Limitations:

- Instance-level finite theorem.
- Compatibility of interpretations is assumed by the checker inputs.

### claim.model_search.no_counterexamples

- Title: No Generated Bridge-Distortion Counterexamples
- Scope: generated_search_space
- Verification level: stress_tested
- Strongly verified: True
- Conjectural: False

Statement:

In the generated finite search space, no counterexamples were found to the implemented Bridge Distortion Theorem.

Evidence:

- src/rigor/search_report.py
- docs/model_search_report.md
- tests/test_rigor_search_report.py

Limitations:

- Only applies to generated finite cases.
- Search space is finite and parameter-bound.

### claim.general_foundations

- Title: General Foundations Claim
- Scope: conjectural_generalization
- Verification level: conjectural
- Strongly verified: False
- Conjectural: True

Statement:

The finite Project Aleph-Omega framework may suggest patterns for studying translations between richer logical foundations.

Evidence:

- docs/rigor_track.md

Limitations:

- Not proven.
- Should not be presented as a solved foundations theorem.
- Requires substantial formalization to generalize.

## Correct Research Framing

The inventory is not a claim that all listed items are universal mathematical theorems.

It records the current scope, verification level, evidence, and limitations of each theorem-like statement.
