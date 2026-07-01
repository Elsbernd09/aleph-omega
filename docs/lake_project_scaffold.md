# Lean Lake Project Scaffold

## Purpose

Phase 27A packages the Project Aleph-Omega Lean formalization as a standalone Lake project.

Earlier phases stored the Lean core at:

formal/lean/AlephOmegaCore.lean

Phase 27A adds a Lake project at:

formal/aleph_omega_lake

## Lake Project Files

The Lake project contains:

- formal/aleph_omega_lake/lakefile.lean
- formal/aleph_omega_lake/lean-toolchain
- formal/aleph_omega_lake/AlephOmega.lean
- formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean

## Build Script

Run:

./scripts/check_lake.sh

Successful output:

Aleph-Omega Lake project built successfully.

## Why This Matters

A single Lean file is useful, but a Lake project is closer to a serious formalization repository.

This prepares the project for possible future Mathlib integration.

## Correct Research Claim

Project Aleph-Omega now has a standalone Lake scaffold for building the Lean formal core.

This is not yet a Mathlib Category instance.
