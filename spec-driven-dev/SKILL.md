---
name: spec-driven-dev
description: Write a precise behavior spec for a feature before writing any code, then implement exactly to that spec. Use when the user wants spec-driven development, asks to "write a spec for X," or wants a given/when/then behavior contract, API shape, and acceptance checklist locked down before implementation starts.
---

# Spec-Driven Development

The spec is the source of truth — not the code. Once approved, code that quietly diverges from the spec is a bug even if it "works."

If the user wants runnable test code rather than a document to review before implementation starts, that's `e2e-test`, not this. This skill's output is a markdown file; if there's already an approved spec and the ask is to verify the built feature against it, that's testing, not spec-writing.

## Before writing

Get the feature and its context: who uses it, why it's needed now. If this is following a `write-prd` skill run, read the PRD at `docs/prd-*.md` first rather than re-deriving it.

## Spec format

Use the structure in `references/spec-template.md`. It covers:

- **Behavior**: given/when/then for every case — happy path, edge cases, and failure states, not just the main flow
- **API contract**: inputs, outputs, error shapes, status codes
- **Data**: schema changes and migrations needed
- **UI states**: loading, empty, error, success
- **Non-goals**: what this spec deliberately does *not* cover — as important as what it does
- **Acceptance checklist**: a line-by-line list the user can verify against, not prose

Save the file as `docs/spec-[feature-slug].md` — the same naming pattern as the PRD, so `implementation-plan` (and anyone else) can find it by convention instead of asking "where's the spec?"

## After approval

Implement exactly what the spec says. If reality forces a deviation mid-implementation (an API doesn't behave as assumed, a constraint was missed):
1. Stop.
2. Update the spec document to reflect the new reality.
3. Get explicit ok on the updated spec.
4. Only then continue implementing.

Never let the code drift ahead of the spec silently — if they disagree, the spec needs to change first, in the open, not the other way around.
