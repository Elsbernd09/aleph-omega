#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.elan/env"

echo "== Aleph-Omega Generated Mathlib Export Check =="
echo ""

echo "1. Generating Mathlib-targeted finite system export..."
python3 -m src.rigor.mathlib_finite_system_exporter
echo ""

echo "2. Generating Mathlib-targeted preservation morphism export..."
python3 -m src.rigor.mathlib_morphism_exporter
echo ""

echo "3. Rebuilding generated Mathlib index..."
cat > formal/aleph_omega_mathlib/AlephOmegaMathlib/Generated.lean <<'LEAN'
import AlephOmegaMathlib.Generated.ExportedTinyMathlibSystem
import AlephOmegaMathlib.Generated.ExportedTinyMathlibMorphism
LEAN
echo ""

echo "4. Checking experimental Mathlib project with generated exports..."
./scripts/check_mathlib_scaffold.sh
echo ""

echo "Generated Mathlib exports verified successfully."
