# Formal Verification Interface

## Purpose

Phase 16 adds a formal verification interface to Project Aleph-Omega.

The purpose is not to claim full machine proof.

The purpose is to separate:

- formal claim records
- finite theorem checks
- theorem audit records
- proof obligations
- verification reports
- conjectural generalizations

This helps the project avoid overclaiming.

---

## Implemented Files

Phase 16 added:

- src/rigor/claim_registry.py
- src/rigor/theorem_audit.py
- src/rigor/proof_obligations.py
- src/rigor/verification_report.py

with tests:

- tests/test_rigor_claim_registry.py
- tests/test_rigor_theorem_audit.py
- tests/test_rigor_proof_obligations.py
- tests/test_rigor_verification_report.py

and docs:

- docs/formal_claim_registry.md
- docs/theorem_audit.md
- docs/proof_obligations.md
- docs/verification_report.md
- docs/formal_verification_interface.md

---

## Formal Claim Registry

The claim registry records theorem-like claims with:

- identifier
- title
- statement
- scope
- verification level
- evidence
- limitations

This separates finite verified claims from conjectural claims.

---

## Theorem Audit Records

The theorem audit system checks whether each claim has:

- a nonempty statement
- evidence records
- limitations
- correct conjectural marking
- evidence files that exist when they are local project files

The audit does not prove the claim.

It checks whether the claim is responsibly recorded.

---

## Proof Obligation Tracker

The proof obligation tracker records what remains open.

Examples:

- stronger formal proof
- more stress testing
- more documentation
- clearer limitation statements
- conjectural generalization work

This makes unfinished verification work explicit.

---

## Verification Report

The verification report combines:

- claim registry
- theorem audit report
- proof obligation report

Generate it with:

python3 -m src.rigor.verification_report

This writes:

docs/verification_report.md

---

## Correct Research Framing

Project Aleph-Omega can now honestly claim:

The project includes a formal verification interface that records finite claims, audits theorem-like statements, tracks proof obligations, and separates verified finite results from conjectural generalizations.

It should not claim:

The project is fully machine-verified.

It should not claim:

The project proves universal theorems about all mathematical foundations.

The strongest claims remain finite, computational, and model-bound.

---

## Why Phase 16 Matters

Phase 16 makes the project more serious because it adds research discipline.

Instead of treating every theorem-like statement as equally proven, the project now asks:

1. What exactly is the claim?
2. What is its scope?
3. What evidence supports it?
4. What limitations apply?
5. What obligations remain open?
6. Is the claim finite, tested, proved, or conjectural?

That is the right attitude for serious mathematical work.
