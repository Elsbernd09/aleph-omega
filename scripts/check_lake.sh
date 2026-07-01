#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.elan/env"

cd formal/aleph_omega_lake
lake build

echo "Aleph-Omega Lake project built successfully."
