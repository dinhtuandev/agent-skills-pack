---
name: e2e-test
description: Write Playwright end-to-end tests for a user flow, prioritizing the flows that actually matter (signup, checkout, core actions). Use when the user wants E2E tests, browser tests, or Playwright coverage for a flow, wants to verify something works end to end, or wants CI test coverage before a release.
---

# E2E Test Your Application

If the ask is "given/when/then for X" with no mention of tests, code, or CI, and no implementation exists yet — that's likely a request for a spec document, not test code. Check for `spec-driven-dev` first; this skill is for writing runnable Playwright tests, not a behavior-contract document.

## Inputs

- **Flow** to test
- **Stack** and **CI** (GitHub Actions or other) — infer from the repo if already set up

## Rules

- **Money paths first**: signup, checkout, or whatever the core action of the app actually is — test these before anything peripheral.
- **Test what the user sees, not implementation details.** A test that breaks because a div became a section, with no behavior change, is a bad test.
- **Selectors**: roles and labels (`getByRole`, `getByLabel`). Never brittle CSS class chains that break on a restyle.
- **One unhappy path per flow**: bad input, network failure, or expired session — not just the happy path.
- **Tests stay independent** — any order, zero shared state, each test seeds its own data.
- **Headless in CI, headed locally** for debugging.
- **Screenshots + traces on failure only** — don't bloat every run with artifacts nobody will look at.

`references/test-skeleton.md` has the file shape to start from — role/label selectors, one seeded `beforeEach`, and the one unhappy path per flow.

## After writing

Run the suite, show the user the actual results, fix what fails, and tell them plainly what the suite still does *not* cover — don't imply full coverage if it isn't there.
