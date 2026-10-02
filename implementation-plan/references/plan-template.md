# Implementation Plan: [Feature Name]

**Source:** `docs/spec-[feature-slug].md` | `docs/prd-[feature-slug].md` (approved)
**Approach chosen:** [one line] — [why, 2 more lines]
**App stays runnable after every step:** yes — the sequence is ordered so nothing lands broken mid-way.

## Build sequence

### Step 1 — [name] (S / M / L)
- **Files:** `path/a`, `path/b`
- **Change:** [what changes, in one or two lines]
- **Migration / new dependency:** none | [what, and why it carries extra risk]
- **Verify:** [exact command to run, or the page/behavior to check]
- **Rollback:** [the actual action or command, not "revert if needed"]

### Step 2 — [name] (S / M / L)
- **Files:**
- **Change:**
- **Migration / new dependency:**
- **Verify:**
- **Rollback:**

(repeat — riskiest unknown as early as the app allows)

## Risks & open unknowns

| Risk | Where it bites | Mitigation |
|---|---|---|
| | | |

## Done when

- [ ] Every step above verified with its own command/check
- [ ] The acceptance checklist in the source spec is satisfied line by line

---

*Execute one step at a time and wait for "go" between steps — see the rules in
the implementation-plan skill.*
