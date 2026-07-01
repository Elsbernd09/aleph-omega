# Finite Satisfaction Preservation Theorem

## Purpose

This document states and proves a satisfaction-based theorem for Project ℵω.

The earlier Bridge Distortion Theorem used semantic feature loss. This theorem strengthens the framework by using a satisfaction relation.

---

## Definitions

Let `U` and `V` be finite logical universes.

Let `B` be a finite bridge from statements of `U` to statements of `V`.

Let `I_U` be an interpretation of statements in `U`.

Let `I_V` be an interpretation of statements in `V`.

A statement `s` is satisfied under an interpretation when:

1. the universe supports all features required by `s`;
2. `s` has a valid assigned truth value;
3. the assigned truth value is designated.

---

## Theorem

### Finite Satisfaction Preservation Theorem

A bridge `B` preserves satisfaction from `I_U` to `I_V` exactly when:

```text
for every s in statements(U),
if s is satisfied under I_U,
then B(s) is defined and B(s) is satisfied under I_V.
