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
