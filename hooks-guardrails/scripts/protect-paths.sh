#!/usr/bin/env bash
# PreToolUse hook: block edits to protected paths.
# Reads the tool call JSON from stdin, checks the target file path against
# a list of protected patterns, and exits with code 2 to block the edit.
# (Only exit code 2 denies a PreToolUse action; any other non-zero exit is
# treated as a hook error and does NOT block.)
#
# Wire this in settings.json under hooks.PreToolUse for the Edit/Write tools.
# Customize PROTECTED_PATTERNS for the project — this is a starting point,
# not a fixed list.
#
# Requires `jq` on PATH (used to read the tool-call JSON on stdin). If jq is
# missing the hook errors out instead of blocking, which is safer but silent —
# install jq or swap the parse for python -c.

set -euo pipefail

PROTECTED_PATTERNS=(
  "*/migrations/*"
  ".env"
  ".env.*"
  "*/prod.config.*"
)

# Claude Code passes the tool call as JSON on stdin; pull the file path out.
FILE_PATH=$(jq -r '.tool_input.file_path // .tool_input.path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0 # no file path in this tool call — nothing to check
fi

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == $pattern ]]; then
    # Exit code 2 specifically means "deny" for PreToolUse hooks — a plain
    # non-zero exit is just treated as a hook error, not a block.
    echo "Blocked: '$FILE_PATH' matches protected pattern '$pattern'. Ask the user directly before editing this file." >&2
    exit 2
  fi
done

exit 0
