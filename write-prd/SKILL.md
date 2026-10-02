---
name: write-prd
description: Write a full product requirements document (PRD) for a feature before any design, technical spec, or implementation work starts. Use whenever the user asks for a PRD, wants to define a feature at the product level (problem, users, scope, success metrics), says "write the PRD for X" or "define this feature for me", or hands over a rough feature idea that needs to become a scoped, reviewable document. Always use this when the deliverable is meant to be saved and referenced by later prompts (specs, implementation plans). Not for a technical given/when/then spec — that's spec-driven-dev.
---

# Write a Full PRD

A PRD here is a working document other prompts will read later (spec, UI brief, implementation plan), not a pitch deck. Optimize for someone skimming it in two minutes and being able to start work from it.

## Before writing

Confirm three things — infer what you can from the conversation and the repo, ask only for what's genuinely missing:
- **Feature**: what is being built, in the user's own words
- **Users**: who actually uses this
- **Stack**: check `package.json` / `pom.xml` / `requirements.txt` / existing docs before asking

## Sections to include

Use the structure in `references/prd-template.md` — it keeps headers consistent so downstream skills (spec-driven-dev, implementation-plan) can find sections by name instead of guessing at your phrasing each time. The sections:

1. **Problem statement + success metrics** — what's broken today, how you'll know it's fixed
2. **User stories with acceptance criteria** — as-a/I-want/so-that, each with a checkable "done" condition
3. **Scope** — what ships in v1, and an explicit list of what does *not*
4. **Data model changes** — new/changed entities, fields, relations
5. **Edge cases + failure states** — what happens when things go wrong, not just the happy path
6. **Open questions** — anything you're genuinely unsure about goes here, not silently decided

## Rules

- Keep it under two pages. If a section is running long, that's a sign it belongs in the spec, not the PRD.
- Be specific — no "robust", "seamless", "intuitive", or other filler adjectives that don't constrain a design decision.
- Product-level tradeoffs (what's in v1, what a user story really needs) are the user's call — put them in Open Questions rather than deciding unilaterally.
- Save the file as `docs/prd-[feature-slug].md` so later prompts (spec, implementation plan) can reference it by path.

## Done when

The PRD is saved to `docs/`, every section above is filled in (or the gap is logged as an open question), and someone who wasn't in this conversation could read it and know what's being built and why.
