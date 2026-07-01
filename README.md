# Project ℵω: Trans-Axiomatic Architectonics

A computational laboratory for generative axiom systems, toy logical universes, bridge translation, and neural-symbolic formalization.

## Overview

Project ℵω studies formal mathematical systems as computational objects.

Instead of assuming one fixed mathematical background, the project makes the background itself explicit. Axioms, inference rules, truth values, statements, universes, morphisms, and proof sketches are represented as structured objects that can eventually be generated, compared, translated, and analyzed.

The project is inspired by mathematical logic, category theory, topos theory, type theory, proof assistants, and symbolic artificial intelligence.

Its goal is not to claim solutions to open problems. Its goal is to build a serious experimental framework for exploring how formal systems behave.

## Core Research Question

Can we computationally model families of formal mathematical universes and study the transformations between them?

This question leads to several subquestions:

- How can axioms be represented and scored?
- How can different logical universes be modeled?
- How does truth change across formal contexts?
- What is preserved or distorted when a statement moves between universes?
- Can informal mathematical intuition be converted into symbolic structure?
- Can symbolic structures be turned into Lean-style proof sketches?

## Main Modules

### 1. Generative Axiom Engine

The generative axiom engine represents toy axioms as structured data. It will eventually generate, mutate, recombine, score, and filter candidate axiom systems.

Important scores may include complexity, novelty, contradiction risk, expressivity contribution, and stability.

### 2. Toy Logical Universes

The universe layer models different formal environments, including classical, intuitionistic, paraconsistent, many-valued, modal, fuzzy, and generated toy universes.

Each universe has its own assumptions about truth, contradiction, inference, and interpretation.

### 3. Bridge and Transport Engine

The bridge engine studies how statements behave when moved between universes.

It records preservation, distortion, semantic loss, failure modes, and translation compatibility.

### 4. Prime Geometry Lab

The prime geometry layer will explore experimental representations of prime numbers as graphs, curves, and deformation objects.

This is an exploratory computational module, not a proof of number-theoretic conjectures.

### 5. Cognitive Morphism Engine

The cognitive morphism engine studies the transition from informal mathematical intuition to structured symbolic statements.

It will detect objects, relations, operations, ambiguity, universe compatibility, and possible Lean theorem skeletons.

### 6. Lean Experiments

The Lean layer will contain formalization experiments involving propositions, proof objects, theorem skeletons, and eventually reflection-style reasoning.

Early Lean files may include incomplete proof sketches with sorry. Those sketches are not completed proofs; they are formalization starting points.

## Repository Structure

```text
aleph-omega/
├── docs/
│   ├── research_manifesto.md
│   ├── formal_system_model.md
│   ├── universe_design.md
│   ├── axiom_engine_design.md
│   ├── bridge_engine_design.md
│   ├── cognitive_morphism_design.md
│   └── limitations.md
├── src/
│   ├── generative_axioms/
│   ├── toy_topoi/
│   ├── bridges/
│   └── cognitive_morphism/
├── experiments/
├── lean/
├── tests/
├── requirements.txt
└── README.md
```

## Current Status

The repository is currently in the architecture and design phase.

Phase 0 created the GitHub repository, documentation structure, Python package skeleton, experiments folder, Lean folder, and tests folder.

Phase 1 defines the intellectual architecture of the project through research design documents.

Implementation begins in later phases.

## Documentation

- [Research Manifesto](docs/research_manifesto.md)
- [Formal System Model](docs/formal_system_model.md)
- [Universe Design](docs/universe_design.md)
- [Axiom Engine Design](docs/axiom_engine_design.md)
- [Bridge Engine Design](docs/bridge_engine_design.md)
- [Cognitive Morphism Design](docs/cognitive_morphism_design.md)
- [Limitations and Academic Honesty](docs/limitations.md)

## Design Philosophy

Project ℵω follows one main principle:

Represent the mathematical background itself as an object of computation.

Ordinary mathematical software usually works inside a fixed background. Project ℵω makes that background visible, variable, and analyzable.

A statement is not studied only as true or false. It is studied as true, false, unknown, contradictory, necessary, possible, fuzzy, provable, unprovable, or unstable depending on the universe in which it is interpreted.

## Academic Honesty

Project ℵω does not claim to solve the abc conjecture, the Goldbach conjecture, the Riemann hypothesis, or any other major open problem.

It does not claim to replace ZFC, type theory, Lean, or topos theory.

It does not claim that generated axioms are automatically true or that Lean skeletons are completed proofs.

The project is ambitious because it studies formal systems themselves as computational objects.

It is credible because it distinguishes clearly between inspiration, metaphor, experiment, software architecture, and mathematical proof.

## Long-Term Vision

The long-term vision is an experimental platform that can:

- generate candidate axiom systems
- build toy logical universes
- compare truth behavior across universes
- transport statements between formal contexts
- measure preservation and distortion
- produce experiment reports
- convert informal intuition into symbolic structures
- generate Lean-style theorem skeletons

In mature form, Project ℵω aims to become a small but serious computational foundations laboratory.

## Phase 2: Generative Axiom Engine

The first working implementation of the Generative Axiom Engine is complete.

Implemented components:

- `Axiom` data model
- starter axiom library
- heuristic axiom evaluator
- template-based axiom generator
- axiom mutation system
- experiment runner
- unit tests

Run the experiment:

```bash
python3 experiments/run_axiom_engine.py
```

Run the tests:

```bash
python3 -m pytest tests/test_generative_axioms.py
```

The engine can now represent, generate, score, rank, and test experimental axiom candidates.

## Phase 3: Toy Logical Universes

The first working implementation of the Toy Logical Universe layer is complete.

Implemented components:

- truth-value system
- logic-family definitions
- consistency policies
- toy connective algebra
- formal universe data model
- universe object and morphism models
- standard universe library
- universe comparison engine
- universe comparison experiment runner
- unit tests

The project now includes toy versions of:

- classical logic
- intuitionistic logic
- paraconsistent logic
- many-valued logic
- modal logic
- symbolic fuzzy logic
- generated experimental universes

Run the universe comparison experiment:

```bash
python3 experiments/run_universe_comparison.py
```

Run the toy universe tests:

```bash
python3 -m pytest tests/test_toy_topoi.py
```

The universe layer can now represent, compare, and report on different formal environments. These models are intentionally simplified and are used for computational exploration rather than full mathematical formalization.

## Phase 4: Toy Topos Simulator

The first working implementation of the Toy Topos Simulator is complete.

Implemented components:

- internal statement model
- statement kinds and proof statuses
- statement evaluation model
- topos-inspired object model
- topos-inspired morphism model
- toy diagram model
- internal language analyzer
- toy topos simulator
- toy subobject classifier
- simulator experiment runner
- unit tests

Run the toy topos simulator experiment:

```bash
python3 experiments/run_toy_topos_simulator.py
```

Run the toy topos simulator tests:

```bash
python3 -m pytest tests/test_toy_topos_simulator.py
```

The simulator can now evaluate how internal statements behave across different toy formal universes. It estimates universe fit, ambiguity, proof status, truth value, formalization readiness, and toy subobject-classifier membership. These results are heuristic and educational, not full categorical proofs.

## Phase 5: Bridge Translation Engine

The first working implementation of the Bridge Translation Engine is complete.

Implemented components:

- translation result model
- meaning-change model
- translation status model
- bridge map model
- symbol mappings
- feature mappings
- truth-value mappings
- proof-status mappings
- universe-to-universe translator
- distortion analyzer
- bridge translation experiment runner
- unit tests

Run the bridge translation experiment:

```bash
python3 experiments/run_bridge_translations.py
```

Run the bridge tests:

```bash
python3 -m pytest tests/test_bridge_translations.py
```

The bridge engine can now translate statements between toy formal universes and measure what gets preserved, weakened, distorted, or lost. It currently supports starter bridges such as paraconsistent-to-classical, modal-to-classical, and intuitionistic-to-classical translation. The system computes translation confidence, symbol preservation, feature preservation, semantic severity, and an overall distortion index.

These bridge results are heuristic research diagnostics, not formal categorical equivalences or machine-checked theorem-proving results.

## Phase 6: Cognitive Morphism Layer

The first working implementation of the Cognitive Morphism Layer is complete.

Implemented components:

- intuition object model
- intuition kind classification
- clarity and formalization risk scoring
- cognitive morphism model
- preservation and loss model
- informal-to-formal translator
- formalization draft model
- formalization gap analyzer
- cognitive morphism experiment runner
- unit tests

Run the cognitive morphism experiment:

```bash
python3 experiments/run_cognitive_morphism.py
```

Run the cognitive morphism tests:

```bash
python3 -m pytest tests/test_cognitive_morphism.py
```

The cognitive morphism layer models the path from informal mathematical intuition to symbolic statement. It tracks what intuitive content is preserved, lost, or changed during formalization. The system computes conceptual richness, formalization readiness, formalization confidence, meaning drift, review urgency, gap severity, and an overall gap index.

These results are heuristic diagnostics. They are not claims about human cognition, automatic theorem proving, or complete formal correctness.

## Phase 7: Neural-Symbolic Formalization Layer

The first working implementation of the Neural-Symbolic Formalization Layer is complete.

Implemented components:

- formalization target model
- formal target classification
- formalization difficulty and readiness scoring
- Lean-style sketch generator
- proof obligation model
- proof obligation analyzer
- formalization planner
- neural-symbolic experiment runner
- unit tests

Run the neural-symbolic formalization experiment:

```bash
python3 experiments/run_neural_symbolic_formalization.py
```

Run the neural-symbolic tests:

```bash
python3 -m pytest tests/test_neural_symbolic_formalization.py
```

The neural-symbolic layer connects informal mathematical intuitions to formalization targets, Lean-style proof sketches, proof obligations, and ordered action plans. It separates ambition from proof completion by explicitly marking missing definitions, assumptions, semantic encodings, and unresolved `sorry` placeholders.

These results are formalization roadmaps, not completed machine-checked proofs.

## Phase 8: Meta-Theory / System Intelligence Layer

The first working implementation of the Meta-Theory / System Intelligence Layer is complete.

Implemented components:

- system metrics model
- system health grading
- research risk scoring
- global research evaluator
- intelligence report generator
- meta-theory experiment runner
- unit tests

Run the meta-theory intelligence experiment:

```bash
python3 experiments/run_meta_theory_report.py
```

Run the meta-theory tests:

```bash
python3 -m pytest tests/test_meta_theory.py
```

The meta-theory layer evaluates the entire Project ℵω architecture across axiom generation, toy universe simulation, bridge translation, cognitive morphism analysis, and neural-symbolic formalization planning. It produces global system metrics, research risk estimates, strongest and weakest layer rankings, findings, limitations, and recommended next actions.

These results are heuristic system diagnostics, not mathematical proofs or claims of solved open problems.

## Phase 9: Unified Research Report + Output Layer

The first working implementation of the Unified Research Report + Output Layer is complete.

Implemented components:

- research artifact model
- artifact status, risk, and confidence tracking
- artifact collections
- Markdown report generator
- system summary exporter
- full project report experiment
- reporting tests

Run the full project report generator:

```bash
python3 experiments/run_full_project_report.py
```

Run the reporting tests:

```bash
python3 -m pytest tests/test_reporting.py
```

Generated report:

```text
reports/project_aleph_omega_report.md
```

The reporting layer converts Project ℵω outputs into readable research artifacts and Markdown reports. It summarizes system metrics, review requirements, limitations, and recommended next steps.

These reports summarize a computational research framework. They are not mathematical proofs or claims of solved open problems.

## Mathematical Rigor Track

Project ℵω now includes a theorem-driven rigor track.

The first theorem target is the **Finite Bridge Distortion Theorem**:

> If a total bridge translates statements from a finite source universe into a finite target universe, and the source contains a statement requiring a semantic feature absent from the target, then at least one translation is semantically distorted.

Implemented rigor-track files:

- `src/rigor/finite_universe.py`
- `src/rigor/bridge.py`
- `src/rigor/distortion.py`
- `src/rigor/theorem.py`
- `docs/theorem_target.md`
- `docs/bridge_distortion_proof.md`
- `docs/rigor_track.md`

Run rigor-track tests:

```bash
python3 -m pytest tests/test_rigor_finite_universe.py tests/test_rigor_bridge.py tests/test_rigor_distortion.py tests/test_rigor_theorem.py
```

The theorem currently has a finite mathematical statement, executable theorem checks, unit tests, and a hand-written proof. It is not a claim of solving mathematical foundations; it is a precise finite result about semantic distortion under translation between toy logical universes.

## Phase 11: Satisfaction-Based Mathematical Semantics

Project ℵω now includes a stronger satisfaction-based rigor layer.

This layer adds:

- finite truth-value spaces
- semantic operations
- statement interpretations
- validity of interpretations
- designated truth values
- finite satisfaction relation
- satisfaction-based preservation
- satisfaction preservation theorem
- examples and counterexamples

Main theorem:

> A bridge preserves satisfaction exactly when every satisfied source statement has a defined translated target statement that is also satisfied.

Run Phase 11 tests:

```bash
python3 -m pytest tests/test_rigor_semantics.py tests/test_rigor_interpretation.py tests/test_rigor_satisfaction.py tests/test_rigor_preservation.py tests/test_rigor_preservation_theorem.py tests/test_rigor_examples.py
```

Read the proof and examples:

- `docs/satisfaction_preservation_theorem.md`
- `docs/rigor_examples.md`

This phase makes the project more mathematically serious by introducing satisfaction, designated truth values, and preservation failure under translation.

## Phase 12: Categorical / Structural Upgrade

Project ℵω now includes a category-like structural layer.

This layer defines:

- finite logical universes as objects
- finite bridges as morphisms
- identity bridges
- bridge composition
- identity-law checks
- associativity checks
- categorical examples

Run Phase 12 tests:

```bash
python3 -m pytest tests/test_rigor_composition.py tests/test_rigor_category.py tests/test_rigor_identity_laws.py tests/test_rigor_associativity.py tests/test_rigor_category_examples.py
```

Read the category docs:

- `docs/category_structure.md`
- `docs/category_examples.md`

The major conceptual point is that structural validity and semantic preservation are separate. A bridge can obey identity and associativity while still distorting semantic content.

## Phase 13: Functorial Semantics / Preservation Upgrade

Project ℵω now connects finite category-like bridge structure with satisfaction-based semantics.

This layer adds:

- semantic transport along bridges
- preservation under bridge composition
- composition preservation theorem
- distortion accumulation analysis
- functorial semantics examples

Main theorem:

> If `F` preserves satisfaction and `G` preserves satisfaction, then `G ∘ F` preserves satisfaction.

Run Phase 13 tests:

```bash
python3 -m pytest tests/test_rigor_semantic_transport.py tests/test_rigor_composition_preservation.py tests/test_rigor_composition_preservation_theorem.py tests/test_rigor_distortion_accumulation.py tests/test_rigor_functorial_examples.py
```

Read the Phase 13 docs:

- `docs/functorial_semantics.md`
- `docs/composition_preservation_theorem.md`
- `docs/functorial_semantics_examples.md`

This phase strengthens the project by showing that satisfaction-preserving bridge morphisms compose, while non-preserving bridges can create measurable distortion accumulation.

## Phase 14: Finite Model Search / Theorem Stress Testing

Project ℵω now includes a finite model-search layer for theorem stress testing.

This layer adds:

- generated finite logical universes
- richer generated bridge cases
- Bridge Distortion Theorem stress search
- satisfaction preservation search
- combined model-search report generation

Generate the combined model-search report:

python3 -m src.rigor.search_report

Run Phase 14 tests:

python3 -m pytest tests/test_rigor_model_search.py tests/test_rigor_bridge_case_generator.py tests/test_rigor_bridge_distortion_search.py tests/test_rigor_satisfaction_search.py tests/test_rigor_search_report.py

Read the Phase 14 docs:

- `docs/model_search.md`
- `docs/bridge_distortion_search.md`
- `docs/satisfaction_search.md`
- `docs/model_search_report.md`

Careful claim:

> In the generated finite search space, the implemented Bridge Distortion Theorem produced no counterexamples, and the satisfaction layer measured where generated bridge cases preserved or distorted satisfaction.

## Phase 15: Counterexample Laboratory / Failure Taxonomy

Project ℵω now includes a failure laboratory for generated finite semantic cases.

This layer adds:

- finite failure taxonomy
- extraction of counterexample-like semantic failures
- failure laboratory report generation
- theorem boundary analysis

Generate the failure laboratory report:

python3 -m src.rigor.failure_report

Run Phase 15 tests:

python3 -m pytest tests/test_rigor_failure_taxonomy.py tests/test_rigor_failure_extractor.py tests/test_rigor_failure_report.py tests/test_rigor_theorem_boundary.py

Read the Phase 15 docs:

- `docs/failure_lab.md`
- `docs/failure_taxonomy.md`
- `docs/failure_extractor.md`
- `docs/failure_lab_report.md`
- `docs/theorem_boundary_analysis.md`

Careful claim:

> The finite search layer extracts, classifies, and reports generated semantic failure cases, while theorem-boundary analysis distinguishes verified preservation, vacuous preservation, hypothesis failure, structural failure, and semantic distortion.

## Phase 16: Formal Verification Interface / Machine-Checkable Claims

Project ℵω now includes a formal verification interface.

This layer adds:

- formal claim registry
- theorem audit records
- proof obligation tracker
- verification report generation

Generate the verification report:

python3 -m src.rigor.verification_report

Run Phase 16 tests:

python3 -m pytest tests/test_rigor_claim_registry.py tests/test_rigor_theorem_audit.py tests/test_rigor_proof_obligations.py tests/test_rigor_verification_report.py

Read the Phase 16 docs:

- `docs/formal_verification_interface.md`
- `docs/formal_claim_registry.md`
- `docs/theorem_audit.md`
- `docs/proof_obligations.md`
- `docs/verification_report.md`

Careful claim:

> Project ℵω records finite claims, audits theorem-like statements, tracks proof obligations, and separates verified finite results from conjectural generalizations.

## Phase 17: Exportable Research Artifact Layer

Project ℵω now generates polished research artifacts from the codebase.

This layer adds:

- research abstract generation
- theorem inventory generation
- architecture map generation
- final research memo generation

Generate the research artifacts:

python3 -m src.rigor.research_abstract
python3 -m src.rigor.theorem_inventory
python3 -m src.rigor.architecture_map
python3 -m src.rigor.final_research_memo

Run Phase 17 tests:

python3 -m pytest tests/test_rigor_research_abstract.py tests/test_rigor_theorem_inventory.py tests/test_rigor_architecture_map.py tests/test_rigor_final_research_memo.py

Read the Phase 17 docs:

- `docs/research_artifacts.md`
- `docs/research_abstract.md`
- `docs/theorem_inventory.md`
- `docs/architecture_map.md`
- `docs/final_research_memo.md`

Careful claim:

> Project ℵω is a finite computational mathematics framework for studying semantic preservation and distortion across generated finite bridge systems, with theorem-like claims recorded, tested, audited, and bounded by explicit limitations.

## Phase 18: Repository Quality / Reviewer Readiness

Project ℵω now includes reviewer-readiness infrastructure.

This layer adds:

- project health check
- artifact index generation
- reviewer quickstart
- repository checklist

Run reviewer-readiness tools:

python3 -m src.rigor.project_health
python3 -m src.rigor.artifact_index
python3 -m src.rigor.reviewer_quickstart
python3 -m src.rigor.repository_checklist

Run Phase 18 tests:

python3 -m pytest tests/test_rigor_project_health.py tests/test_rigor_artifact_index.py tests/test_rigor_reviewer_quickstart.py tests/test_rigor_repository_checklist.py

Read the Phase 18 docs:

- `docs/reviewer_readiness.md`
- `docs/project_health.md`
- `docs/artifact_index.md`
- `docs/reviewer_quickstart.md`
- `docs/repository_checklist.md`

Careful claim:

> Project ℵω includes reviewer-readiness tools that improve repository completeness, navigation, and reviewability.

## Phase 20: Institution-Theoretic Upgrade / Real Mathematical Anchoring

Project ℵω now includes a finite institution-like formal layer inspired by institution theory.

This layer adds:

- finite signatures
- finite institution-like systems
- finite institution morphisms
- finite institution satisfaction theorem
- finite institution category-like structure
- institution-theoretic exposition
- Lean formalization plan

Run Phase 20 tests:

python3 -m pytest tests/test_rigor_finite_institution.py tests/test_rigor_institution_morphism.py tests/test_rigor_institution_satisfaction_theorem.py tests/test_rigor_institution_category.py tests/test_rigor_institution_exposition.py tests/test_rigor_lean_plan.py

Read the Phase 20 docs:

- `docs/finite_institution.md`
- `docs/institution_morphism.md`
- `docs/institution_satisfaction_theorem.md`
- `docs/institution_category.md`
- `docs/institution_theoretic_upgrade.md`
- `docs/lean_formalization_plan.md`

Careful claim:

> Project ℵω contains a finite institution-like formal layer with finite signatures, finite models, satisfaction relations, satisfaction-preserving morphisms, and a category-like structure of such morphisms.
