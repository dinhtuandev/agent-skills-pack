---
name: plan-mode
description: Enter a strict read-only planning mode before touching any code on a non-trivial task. Use when the user says "plan mode", "ultra plan mode", asks to plan before implementing, or hands over a task that spans multiple files, has real risk (auth, payments, prod data), or unclear scope. In this mode, never edit a file until the plan is explicitly approved.
---

# Ultra Plan Mode

No code changes in this mode. Not a draft PR, not a "quick fix while I'm in there" — read and plan only, until the user approves.

If `docs/spec-*.md` or `docs/prd-*.md` already exists and is approved for this task, the design decisions are made — use `implementation-plan` instead, which turns that into a step sequence. Reach for plan mode when there's no approved document yet, or the ask is explicitly "plan mode" / risk-driven rather than spec-driven.

## Inputs

- **Task**: what needs to happen
- **Constraints**: deadline, stack, no-go zones — ask if not already stated, but don't block on this if the task is otherwise clear enough to plan

## Steps

1. Read every file the task touches. List them with one line each on what they do *today*.
2. Map current behavior vs. target behavior explicitly — don't jump straight to a solution.
3. Propose 2-3 approaches with real tradeoffs: complexity, risk, blast radius. Not one obvious option dressed up as three.
4. Pick one and justify it in 3 lines.
5. Break the chosen approach into steps small enough to verify one at a time, each with its own check (what "this step worked" looks like).
6. List risks + the exact rollback for each risky step — not "revert if needed," the actual command or action.
7. Flag anything touching auth, payments, or production data for explicit sign-off before it's in scope. If the user hasn't told you which areas are sensitive for this project, default to auth/payments/prod-data and ask if there's anything else to add to that list.

## Stop condition

After the plan is written, stop and show it. Do not open, edit, or create a single file until the user explicitly approves — a short "go" or "approved" is enough, but silence or a tangential reply is not.
