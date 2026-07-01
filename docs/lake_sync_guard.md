# Lake Synchronization Guard

## Purpose

Phase 27B adds synchronization protection between the original Lean core and the Lake-project Lean core.

The main Lean file is:

formal/lean/AlephOmegaCore.lean

The Lake copy is:

formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean

## Sync Script

Run:

./scripts/sync_lake_core.sh

This copies the main Lean core into the Lake project.

## Sync Check

Run:

./scripts/check_lake_sync.sh

This verifies that both Lean files are identical.

## Lake Build

Run:

./scripts/check_lake.sh

This now checks synchronization before building the Lake project.

## Why This Matters

Once a project has two Lean entry points, drift becomes a serious risk.

The sync guard prevents the repository from accidentally building stale formalization code.

## Correct Research Claim

Project Aleph-Omega now has a synchronization guard ensuring that the standalone Lake project builds the same Lean core as the primary formalization file.
