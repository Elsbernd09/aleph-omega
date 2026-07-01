#!/usr/bin/env bash
set -euo pipefail

MAIN_CORE="formal/lean/AlephOmegaCore.lean"
LAKE_CORE="formal/aleph_omega_lake/AlephOmega/AlephOmegaCore.lean"

if [[ ! -f "$MAIN_CORE" ]]; then
  echo "Missing main Lean core: $MAIN_CORE"
  exit 1
fi

if [[ ! -f "$LAKE_CORE" ]]; then
  echo "Missing Lake Lean core: $LAKE_CORE"
  exit 1
fi

if ! cmp -s "$MAIN_CORE" "$LAKE_CORE"; then
  echo "Lean core files are out of sync."
  echo "Run: ./scripts/sync_lake_core.sh"
  exit 1
fi

echo "Lean core files are synchronized."
