# Experiments

This folder contains runnable experiments for Project ℵω.

## Implemented Experiments

### Generative Axiom Engine

Run:

python3 experiments/run_axiom_engine.py

This experiment:

- loads the starter axiom library
- generates additional candidate axioms
- mutates seed axioms
- scores all candidates
- ranks them by heuristic research interest
- prints a research-style output table

The scores are not mathematical proofs. They are computational instruments for comparing candidate assumptions inside toy formal-system experiments.

## Planned Experiments

Future experiments may include:

- logical universe comparison
- statement transport
- bridge distortion analysis
- prime geometry simulations
- cognitive morphism parsing
- Lean sketch generation

### Toy Logical Universe Comparison

Run:

python3 experiments/run_universe_comparison.py

This experiment:

- loads the standard toy universe library
- prints a universe inventory
- compares universes pairwise
- ranks the most compatible universe transports
- ranks the most difficult universe transports
- gives a detailed paraconsistent-to-classical translation example
- displays toy connective behavior across universes

The comparison scores are heuristic. They are not formal equivalence proofs. They are designed to make structural differences between toy logical universes explicit.

### Toy Topos Simulator

Run:

python3 experiments/run_toy_topos_simulator.py

This experiment:

- loads the standard toy universe library
- loads starter internal statements
- evaluates each statement across each universe
- computes universe-fit, ambiguity, and formalization-readiness scores
- builds cross-universe statement profiles
- classifies results using a toy subobject classifier
- ranks the strongest statement-universe fits
- ranks the most ambiguous evaluations

The simulator is a simplified computational model. It does not implement full topos theory. Its purpose is to make internal statement behavior across different toy universes inspectable.

### Bridge Translation Engine

Run:

```bash
python3 experiments/run_bridge_translations.py
```

This experiment:

- loads starter bridge maps
- loads source and target universes
- finds statements belonging to each bridge source universe
- translates statements into target universes
- tracks preserved symbols, lost symbols, added symbols, preserved features, and lost features
- tracks truth-value and proof-status changes
- computes translation confidence
- generates distortion reports
- ranks the best translations
- ranks the most distorted translations
- prints bridge-level interpretation summaries

The bridge experiment is a heuristic diagnostic system. It is designed to show how meaning can be preserved, weakened, or lost when statements move between toy universes. It is not a proof of formal equivalence.

### Cognitive Morphism Layer

Run:

```bash
python3 experiments/run_cognitive_morphism.py
```

This experiment:

- loads starter informal mathematical intuitions
- converts each intuition into a starter symbolic statement
- generates cognitive morphisms from intuition to statement
- tracks preserved properties, lost properties, added formal structure, preserved metaphors, and lost metaphors
- estimates formalization confidence and meaning drift
- analyzes formalization gaps
- ranks the strongest formalizations
- ranks the largest formalization gaps
- identifies drafts requiring human review

The cognitive morphism experiment is a heuristic diagnostic system. It is designed to make the informal-to-formal transition inspectable. It is not automatic theorem proving and not a claim of complete formal correctness.
