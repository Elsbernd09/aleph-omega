# Project Aleph-Omega Generated Semantic Lab Artifact Index

## Purpose

This document indexes the generated finite semantic lab artifacts.

It identifies each generated system, preservation morphism, quotient wrapper, and quotient-composition theorem in the semantic lab.

## Summary

- Artifacts indexed: 13
- Systems: 4
- Morphisms: 6
- Quotient artifacts: 5
- Theorems: 2

## Artifact Table

| Name | Kind | Lean name | Location | Role | Verification |
|---|---|---|---|---|---|
| Lab System A | finite system | `LabSystemASystem` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | First object in the generated semantic lab. | Mathlib Lake build |
| Lab System B | finite system | `LabSystemBSystem` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Second object in the generated semantic lab. | Mathlib Lake build |
| Lab System C | finite system | `LabSystemCSystem` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Third object in the generated semantic lab. | Mathlib Lake build |
| Lab System D | finite system | `LabSystemDSystem` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Fourth object in the generated semantic lab. | Mathlib Lake build |
| Lab Morphism AB | preservation morphism | `LabMorphismABMorphism` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated satisfaction-preserving morphism from A to B. | Mathlib Lake build |
| Lab Morphism BC | preservation morphism | `LabMorphismBCMorphism` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated satisfaction-preserving morphism from B to C. | Mathlib Lake build |
| Lab Morphism CD | preservation morphism | `LabMorphismCDMorphism` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated satisfaction-preserving morphism from C to D. | Mathlib Lake build |
| Quotient Lab Morphism AB | quotient morphism | `qLabMorphismAB` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Quotient class of the generated A-to-B morphism. | Mathlib Lake build |
| Quotient Lab Morphism BC | quotient morphism | `qLabMorphismBC` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Quotient class of the generated B-to-C morphism. | Mathlib Lake build |
| Quotient Lab Morphism CD | quotient morphism | `qLabMorphismCD` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Quotient class of the generated C-to-D morphism. | Mathlib Lake build |
| Composition ABC | quotient composition theorem | `q_category_lab_composition_abc` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated theorem proving quotient-category composition along A -> B -> C. | Mathlib Lake build |
| Composition BCD | quotient composition theorem | `q_category_lab_composition_bcd` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated theorem proving quotient-category composition along B -> C -> D. | Mathlib Lake build |
| Semantic Lab Lean File | generated Mathlib file | `AlephOmegaMathlib.Generated.SemanticLab` | `formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated/SemanticLab.lean` | Generated Mathlib file containing the full finite semantic lab. | Generated Mathlib checker and formal-stack gate |

## Strongest Current Claim

> Project Aleph-Omega now has a reviewer-facing index of the generated finite semantic lab, including four generated systems, three generated preservation morphisms, quotient morphism classes, and two generated quotient-category composition theorems.

## Boundary

This is a static index for the current generated semantic lab.

It is not yet an automatic parser over arbitrary generated Lean files.
