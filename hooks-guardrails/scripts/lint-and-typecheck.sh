#!/usr/bin/env bash
# PostToolUse hook: run lint + typecheck after a file edit, and surface
# failures so they get fixed in the same turn instead of piling up.
#
# Replace the two commands below with whatever this project actually uses
# (npm run lint / ruff check / mypy / tsc --noEmit / etc.) — check
# package.json scripts or the CI config first rather than guessing.

set -uo pipefail

LINT_CMD="npm run lint --silent"
TYPECHECK_CMD="npm run typecheck --silent"

lint_output=$($LINT_CMD 2>&1)
lint_status=$?

typecheck_output=$($TYPECHECK_CMD 2>&1)
typecheck_status=$?

if [ $lint_status -ne 0 ] || [ $typecheck_status -ne 0 ]; then
  echo "--- Lint output ---" >&2
  echo "$lint_output" >&2
  echo "--- Typecheck output ---" >&2
  echo "$typecheck_output" >&2
  exit 1
fi

exit 0
