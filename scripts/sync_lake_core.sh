#!/usr/bin/env bash
set -euo pipefail

MAIN_CORE="formal/lean/AlephOmegaCore.lean"
LAKE_CORE="formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean"

if [[ ! -f "$MAIN_CORE" ]]; then
  echo "Missing main Lean core: $MAIN_CORE"
  exit 1
fi

mkdir -p "$(dirname "$LAKE_CORE")"
cp "$MAIN_CORE" "$LAKE_CORE"

echo "Synced $MAIN_CORE -> $LAKE_CORE"
