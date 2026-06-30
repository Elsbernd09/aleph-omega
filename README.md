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
