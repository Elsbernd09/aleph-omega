# Architecture Map

## Purpose

This document maps the major rigor-track layers of Project Aleph-Omega.

It shows how the project moves from finite logical objects to theorem checks, model search, failure analysis, verification records, and exportable research artifacts.

## Summary

- Architecture layers: 9
- Mapped files: 68

## Layers

### 1. Finite Universe Layer

Purpose: Defines finite logical universes, statements, and semantic features.

Files:

- src/rigor/finite_universe.py
- tests/test_rigor_finite_universe.py

Outputs:

- finite statements
- finite logical universes
- semantic feature sets

### 2. Bridge and Distortion Layer

Purpose: Defines finite bridges and detects structural distortion.

Files:

- src/rigor/bridge.py
- src/rigor/distortion.py
- src/rigor/theorem.py
- tests/test_rigor_bridge.py
- tests/test_rigor_distortion.py
- tests/test_rigor_theorem.py

Outputs:

- finite bridges
- distortion reports
- bridge distortion theorem checks

### 3. Satisfaction Semantics Layer

Purpose: Defines truth-value spaces, interpretations, satisfaction, and preservation.

Files:

- src/rigor/semantics.py
- src/rigor/interpretation.py
- src/rigor/satisfaction.py
- src/rigor/preservation.py
- src/rigor/preservation_theorem.py
- tests/test_rigor_semantics.py
- tests/test_rigor_interpretation.py
- tests/test_rigor_satisfaction.py
- tests/test_rigor_preservation.py
- tests/test_rigor_preservation_theorem.py

Outputs:

- truth-value spaces
- universe interpretations
- satisfaction reports
- preservation theorem checks

### 4. Category and Composition Layer

Purpose: Defines bridge composition, identity laws, associativity, and category-like structure.

Files:

- src/rigor/composition.py
- src/rigor/category.py
- src/rigor/identity_laws.py
- src/rigor/associativity.py
- tests/test_rigor_composition.py
- tests/test_rigor_category.py
- tests/test_rigor_identity_laws.py
- tests/test_rigor_associativity.py

Outputs:

- composed bridges
- identity law reports
- associativity reports
- finite universe categories

### 5. Functorial Semantics Layer

Purpose: Connects composition with semantic transport and preservation under composition.

Files:

- src/rigor/semantic_transport.py
- src/rigor/composition_preservation.py
- src/rigor/composition_preservation_theorem.py
- src/rigor/distortion_accumulation.py
- src/rigor/functorial_examples.py
- tests/test_rigor_semantic_transport.py
- tests/test_rigor_composition_preservation.py
- tests/test_rigor_composition_preservation_theorem.py
- tests/test_rigor_distortion_accumulation.py
- tests/test_rigor_functorial_examples.py

Outputs:

- semantic transport reports
- composition preservation checks
- distortion accumulation reports
- functorial examples

### 6. Finite Model Search Layer

Purpose: Generates finite structures and stress-tests theorem-like claims.

Files:

- src/rigor/model_search.py
- src/rigor/bridge_case_generator.py
- src/rigor/bridge_distortion_search.py
- src/rigor/satisfaction_search.py
- src/rigor/search_report.py
- tests/test_rigor_model_search.py
- tests/test_rigor_bridge_case_generator.py
- tests/test_rigor_bridge_distortion_search.py
- tests/test_rigor_satisfaction_search.py
- tests/test_rigor_search_report.py

Outputs:

- generated universes
- generated bridges
- search reports
- model-search markdown report

### 7. Failure Laboratory Layer

Purpose: Extracts, classifies, and reports generated semantic failure cases.

Files:

- src/rigor/failure_taxonomy.py
- src/rigor/failure_extractor.py
- src/rigor/failure_report.py
- src/rigor/theorem_boundary.py
- tests/test_rigor_failure_taxonomy.py
- tests/test_rigor_failure_extractor.py
- tests/test_rigor_failure_report.py
- tests/test_rigor_theorem_boundary.py

Outputs:

- failure classifications
- extracted failure cases
- failure lab report
- theorem boundary analysis

### 8. Verification Interface Layer

Purpose: Records claims, audits theorem-like statements, and tracks proof obligations.

Files:

- src/rigor/claim_registry.py
- src/rigor/theorem_audit.py
- src/rigor/proof_obligations.py
- src/rigor/verification_report.py
- tests/test_rigor_claim_registry.py
- tests/test_rigor_theorem_audit.py
- tests/test_rigor_proof_obligations.py
- tests/test_rigor_verification_report.py

Outputs:

- formal claim registry
- theorem audit report
- proof obligation report
- verification report

### 9. Research Artifact Layer

Purpose: Exports human-readable research artifacts from the project.

Files:

- src/rigor/research_abstract.py
- src/rigor/theorem_inventory.py
- src/rigor/architecture_map.py
- tests/test_rigor_research_abstract.py
- tests/test_rigor_theorem_inventory.py
- tests/test_rigor_architecture_map.py

Outputs:

- research abstract
- theorem inventory
- architecture map

## Architecture Interpretation

The architecture is intentionally layered.

The lower layers define finite mathematical objects.

The middle layers define theorem-like checks, composition, preservation, and generated search.

The upper layers classify failure, audit claims, track proof obligations, and export research artifacts.

This structure makes the project easier to review and harder to overstate.

## Correct Research Framing

The architecture map describes the implemented finite research system.

It does not imply that the project proves universal results about all mathematical foundations.
