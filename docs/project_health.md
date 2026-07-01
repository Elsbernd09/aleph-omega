# Project Health Check

## Purpose

Phase 18A adds a project health check for Project Aleph-Omega.

The health check verifies that key source files, tests, documentation files, generated reports, and research artifacts exist.

---

## What It Checks

The health checker looks for:

- README
- rigor-track documentation
- generated research artifacts
- model-search report
- failure laboratory report
- verification report
- core source files
- core test files

---

## Why This Matters

A reviewer should be able to open the repository and quickly see that the main project artifacts are present.

The health check helps catch missing files before the project is shared.

---

## Run It

Run:

python3 -m src.rigor.project_health

Then run all tests:

python3 -m pytest

---

## Correct Research Framing

The health check does not verify mathematical truth.

It checks repository completeness and reviewer readiness.
