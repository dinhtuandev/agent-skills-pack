---
name: cleanup-dead-code
description: Find and safely remove dead code — unused exports, unreachable branches, stale dependencies, dead CSS. Use when the user asks to clean up dead code, remove unused code, prune a repo, or find things nothing imports anymore.
---

# Clean Up Dead Code

Deleting code is higher-risk than writing it — a wrong deletion is often silent until it isn't. Move carefully.

## Scope

Confirm whole repo vs. a specific folder if not already stated.

## Look for

- Unused exports, components, hooks, utils
- Unreachable branches and commented-out blocks
- `package.json` dependencies nothing imports
- Stale feature flags stuck permanently on or off
- Duplicate logic that should merge into one implementation
- Dead CSS classes and unused assets

## Rules

- **Verify with a search before every deletion.** Dynamic imports and string references (`require(variableName)`, a class name built from a template string) don't show up in a naive "find usages" and will break silently if missed.
- **Delete in small commits**, running the build and test suite after each one — not one giant deletion commit at the end.
- **Report** total lines removed, plus anything you weren't 100% sure about (leave those in, flagged, rather than guessing).

`references/cleanup-report.md` has the report shape to fill in — removed / left in place / not touched, each with the evidence (the search that came back empty) beside it.
