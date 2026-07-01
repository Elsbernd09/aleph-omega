#!/usr/bin/env bash
set -euo pipefail

source "$HOME/.elan/env"

./scripts/check_lake_sync.sh

cd formal/aleph_omega_lake
lake build

echo "Aleph-Omega Lake project built successfully."
