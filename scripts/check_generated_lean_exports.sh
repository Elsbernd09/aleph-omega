#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.elan/env"

echo "== Aleph-Omega Generated Lean Export Check =="
echo ""

echo "1. Generating finite system Lean export..."
python3 -m src.rigor.lean_finite_system_exporter
echo ""

echo "2. Generating preservation morphism Lean export..."
python3 -m src.rigor.lean_morphism_exporter
echo ""

echo "3. Checking generated finite system Lean file..."
lean formal/generated/ExportedTinySystem.lean
echo ""

echo "4. Checking generated preservation morphism Lean file..."
lean formal/generated/ExportedTinyMorphism.lean
echo ""

echo "Generated Lean exports verified successfully."
