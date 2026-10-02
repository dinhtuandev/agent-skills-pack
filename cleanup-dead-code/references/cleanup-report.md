# Dead Code Cleanup — [scope] — [date]

**Scope:** [whole repo | path]
**Build + tests after cleanup:** [command run + result]

## Summary

- Lines removed: [n]
- Files touched: [n]
- Dependencies removed: [n]
- Left in place, flagged: [n]

## Removed

| Item | Kind (export / branch / dep / CSS / asset) | Evidence nothing references it |
|---|---|---|
| | | e.g. `rg "oldHelper"` → 0 hits across `src/` |

## Left in place (flagged, not deleted)

| Item | Why it looked dead | Why it was kept |
|---|---|---|
| | | e.g. referenced via `require(variableName)` / template-string class name |

## Not touched

[Anything outside scope, so nobody reads silence as a clean sweep.]

---

*Delete in small commits with build + tests after each one — see the rules in
the cleanup-dead-code skill.*
