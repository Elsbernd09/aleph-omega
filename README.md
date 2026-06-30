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
