# Python-to-Lean Preservation Morphism Exporter

## Purpose

Phase 31C creates the first Python-to-Lean exporter for satisfaction-preserving morphisms.

The exporter generates two finite Lean systems and a Lean preservation morphism between them.

## Location

```text
src/rigor/lean_morphism_exporter.py
formal/generated/ExportedTinyMorphism.lean
```

## What It Exports

- source finite system
- target finite system
- sentence translation
- model map
- preservation theorem
- PreservationMorphism object

## Verification

Run:

```bash
python3 -m src.rigor.lean_morphism_exporter
lean formal/generated/ExportedTinyMorphism.lean
```

## Why This Matters

This connects Python finite semantic data to Lean-checkable preservation morphisms.

The Python layer can now generate not only finite systems, but also machine-checkable semantic translations between systems.

## Strongest Claim

Project Aleph-Omega now has a Python-to-Lean exporter that generates Lean-checkable finite satisfaction-preserving morphisms.

## Boundary

This exporter currently supports total finite model maps and total finite sentence translations.
