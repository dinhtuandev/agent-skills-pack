---
name: ui-ux-brief
description: Produce a full UI/UX design brief for a screen or user flow before it gets built. Use when the user asks for a UI/UX brief, wants to think through the design of a screen or flow, or needs layout, component states, typography/color tokens, motion, and accessibility documented before implementation starts.
---

# Full UI & UX Design Brief

This is a design document, not a mood board — every section should be specific enough that someone could build the screen from it without guessing.

## Before writing

Get the screen/flow, audience, and brand direction (colors/fonts/vibe) — infer brand from an existing design system or repo if one exists, ask only for what isn't already established.

## Deliver

Use the structure in `references/brief-template.md`. It covers:

1. **User journey** — step by step through the flow, from entry to completion
2. **Layout per screen** — hierarchy, spacing, breakpoints
3. **Component inventory** — every component with every state: default, hover, empty, error, loading. A component brief that only covers the happy state is incomplete.
4. **Typography + color tokens** — named values, not vague descriptions
5. **Motion** — what animates, duration, easing
6. **Accessibility notes** — contrast, focus order, screen-reader labels, keyboard nav

If the deliverable is meant to be saved and referenced later (rather than a one-off answer in chat), save it as `docs/design-brief-[screen-slug].md`.

## Reference, don't copy

If the user names 2-3 products they admire, study their *patterns* for direction (information density, interaction models, visual weight) — but never reproduce their actual designs, layouts, or assets. The brief should read as this product's own design language, informed by good examples, not a clone.

## Done when

Every deliverable above is filled in and specific enough that a developer or designer could execute it without asking a follow-up question about intent.
