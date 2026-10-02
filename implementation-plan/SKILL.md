---
name: implementation-plan
description: Turn an approved spec or PRD into a numbered, step-by-step implementation build sequence. Use when the user has an approved spec/PRD and wants an implementation plan, a build sequence, or the work broken into small verifiable steps executed one at a time.
---

# Implementation Plan

This turns an approved design document into an executable sequence — not a to-do list, a sequence where each step leaves the app in a working state.

## Input

The approved spec or PRD. Check `docs/spec-*.md` and `docs/prd-*.md` first — if either exists, read it fully before planning rather than asking the user to re-paste it. Only ask if neither file exists and none was referenced in the conversation.

## Rules

- **Sequence steps so the app compiles and runs after every single step.** No step should leave the codebase in a broken intermediate state.
- **Each step lists**: files touched, what changes, and how the user verifies it worked (a command to run, a page to check, a specific behavior to confirm).
- **Flag steps needing a migration or new dependency** explicitly — these carry more risk and the user should see them coming.
- **Put the riskiest unknowns first.** If something might not work the way you expect, find out in step 2, not step 9.
- **Size each step**: S / M / L, so the user knows what they're committing to before saying go.

## Output

Use the structure in `references/plan-template.md` so every step carries the same five fields — files, change, migration/dependency flag, verify, rollback — instead of re-inventing the shape each run.

A numbered build sequence. Execute one step at a time and wait for the user's "go" between steps — don't chain multiple steps together even if the next one seems obvious.
