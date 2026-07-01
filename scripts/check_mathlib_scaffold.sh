#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.elan/env"

cd formal/aleph_omega_mathlib

lake update
lake build

echo "Aleph-Omega experimental Mathlib scaffold built successfully."
