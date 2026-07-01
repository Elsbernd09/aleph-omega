# Project Aleph-Omega Verification Status

## Purpose

This page explains what parts of Project Aleph-Omega are Lean-checked, Python-tested, CI-checked, and explicitly not claimed.

## Summary

- Verification items: 12
- Lean-checked items: 7
- Python-tested items: 2
- CI-checked items: 2

## Verification Table

| Item | Status | Evidence | Limitation |
|---|---|---|---|
| Primary Lean formalization | Lean-checked | `formal/lean/AlephOmegaCore.lean and ./scripts/check_lean.sh` | Checks the standalone Lean formalization, not every Python implementation detail. |
| Satisfaction preservation under identity | Lean-checked | `identity_preserves_satisfaction` | Applies to the Lean FormalSystem abstraction. |
| Satisfaction preservation under composition | Lean-checked | `composition_preserves_satisfaction` | Applies to Lean PreservationMorphism objects. |
| Morphism equivalence laws | Lean-checked | `morphism_equiv_refl / morphism_equiv_symm / morphism_equiv_trans` | Uses extensional equality of translation and model maps. |
| Quotient morphism composition | Lean-checked | `quotient_composition_well_defined and quotientComp` | Standalone quotient layer, not yet Mathlib Category. |
| Standalone quotient-category structure | Lean-checked | `AlephOmegaQuotientCategory` | Custom Lean structure, not a Mathlib Category instance. |
| Concrete finite preservation chain | Lean-checked | `TwoSystem, RenamedTwoSystem, ThirdTwoSystem, twoToThirdComposite` | Concrete finite example, not universal theorem. |
| Python finite semantic laboratory | Python-tested | `src/rigor/ and python3 -m pytest` | Computational analogue, not proof-assistant verification. |
| Lake project build | Locally checked and CI-checked | `formal/aleph_omega_lake/ and ./scripts/check_lake.sh` | Packages the standalone Lean core; Mathlib integration is future work. |
| Full formal stack | Locally checked and CI-checked | `./scripts/check_formal_stack.sh and .github/workflows/formal-stack.yml` | CI success means reproducibility of the stated stack, not universal mathematical generality. |
| Public documentation package | Python-tested | `README.md, docs/quickstart.md, docs/public_release_index.md, and documentation tests` | Documentation supports review, but the authoritative proofs are in Lean. |
| Universal institution theorem | Explicitly not claimed | `README.md and docs/manuscript_theorem_inventory.md` | The project does not prove a theorem about all institutions, all logics, or all categories. |

## Main Verification Command

Run:

```bash
./scripts/check_formal_stack.sh
```

Expected final output:

```text
Aleph-Omega formal stack verified successfully.
```

## Strongest Careful Verification Claim

> Project Aleph-Omega has a reproducible formal stack containing a Lean-checked abstract core, concrete finite Lean examples, a Lake build scaffold, Python-tested finite computational analogues, and GitHub Actions CI.

## Boundary

This does not mean Project Aleph-Omega proves a universal theorem about all institutions, all logics, or all categories.
