# Project Aleph-Omega Public Release Documentation Index

## Purpose

This document is the reviewer-facing map of the Project Aleph-Omega documentation package.

It tells readers where to start depending on what they want to evaluate.

## Quick Start

- Start with `README.md` for the public overview.
- Read `docs/project_aleph_omega_manuscript.md` for the full research-style explanation.
- Read `docs/manuscript_theorem_inventory.md` for exact claims and theorem status.
- Run `./scripts/check_formal_stack.sh` to verify the Lean, Lake, and Python stack locally.

## Summary

- Documents indexed: 12
- Completed documents: 12

## Documentation Map

### 1. Public README

- Path: `README.md`
- Audience: general reviewers
- Status: complete

Purpose: Gives the clean public overview of the project, its claims, limitations, and run commands.

### 2. README Archive

- Path: `README_ARCHIVE.md`
- Audience: development-history reviewers
- Status: complete

Purpose: Preserves the phase-by-phase development README before the public rewrite.

### 3. Academic Manuscript

- Path: `docs/project_aleph_omega_manuscript.md`
- Audience: technical reviewers
- Status: complete

Purpose: Explains the finite semantic framework, Lean core, quotient structure, examples, limitations, and future work.

### 4. Theorem and Claim Inventory

- Path: `docs/manuscript_theorem_inventory.md`
- Audience: mathematical reviewers
- Status: complete

Purpose: Separates definitions, Lean-checked theorems, Python-tested results, examples, and non-claims.

### 5. Manuscript Figures

- Path: `docs/manuscript_figures.md`
- Audience: visual reviewers
- Status: complete

Purpose: Provides architecture diagrams, theorem-flow diagrams, concrete-chain diagrams, and claim-boundary diagrams.

### 6. Manuscript Front Matter

- Path: `docs/manuscript_front_matter.md`
- Audience: submission reviewers
- Status: complete

Purpose: Contains the short abstract, extended abstract, keywords, contribution list, reviewer summary, and submission note.

### 7. Formal Claim Upgrade Log

- Path: `docs/formal_claim_upgrade.md`
- Audience: claim-boundary reviewers
- Status: complete

Purpose: Tracks the strongest careful claims and limitations after each formalization phase.

### 8. Lean Formalization Index

- Path: `docs/lean_formalization_index.md`
- Audience: Lean reviewers
- Status: complete

Purpose: Indexes the key Lean definitions and theorem artifacts.

### 9. Concrete Lean Completion Report

- Path: `docs/concrete_lean_completion_report.md`
- Audience: formal-methods reviewers
- Status: complete

Purpose: Summarizes the concrete finite Lean systems, nontrivial morphisms, preservation chain, and quotient integration.

### 10. Lean Packaging Completion Report

- Path: `docs/lean_packaging_completion_report.md`
- Audience: reproducibility reviewers
- Status: complete

Purpose: Explains the Lake project, sync guard, formal-stack build gate, and GitHub Actions CI.

### 11. Correspondence Completion Report

- Path: `docs/correspondence_completion_report.md`
- Audience: implementation reviewers
- Status: complete

Purpose: Explains how the Python computational layer corresponds to the Lean formal layer.

### 12. Public Release README Notes

- Path: `docs/public_release_readme_notes.md`
- Audience: public-release reviewers
- Status: complete

Purpose: Explains the public README rewrite and its claim boundaries.

## Suggested Reviewer Path

A serious reviewer should read documents in this order:

1. `README.md`
2. `docs/manuscript_front_matter.md`
3. `docs/project_aleph_omega_manuscript.md`
4. `docs/manuscript_theorem_inventory.md`
5. `docs/lean_formalization_index.md`
6. `docs/lean_packaging_completion_report.md`

Then run:

```bash
./scripts/check_formal_stack.sh
```

## Claim Boundary

The public release should describe Project Aleph-Omega as a finite institution-inspired, Lean-supported research framework.

It should not describe the project as a universal theory of institutions, a solved open problem, a full Mathlib Category instance, or a field-changing theorem.
