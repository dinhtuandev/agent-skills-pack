# Output eval — spec-driven-dev

Tests **what the spec contains**, not whether the skill triggered (that is
`evals/trigger-eval.json`).

## Case A — a spec written from a PRD

Input: `spec out the password reset flow: expired token, wrong email, rate limited`
Artifact: `docs/spec-password-reset.md`

| # | Check | Pass condition |
|---|---|---|
| 1 | Every template section present | the file has every H2 in `references/spec-template.md`: Behavior, API contract, Data, UI states, Non-goals, Acceptance checklist |
| 2 | Behavior is given/when/then | every Behavior case has explicit **Given / When / Then** lines, not prose paragraphs |
| 3 | Failure paths, not just happy path | at least the expired-token, wrong-email, and rate-limited cases each appear as their own case |
| 4 | Error shapes are concrete | the API contract lists specific status codes and error bodies, not "handles errors" |
| 5 | UI states complete | the UI states table has non-empty Loading, Empty, Error and Success rows |
| 6 | Non-goals non-empty | the Non-goals section names at least one thing this spec deliberately excludes |
| 7 | Acceptance checklist is checkable | every acceptance line is a checkbox a person can tick, not prose |

## Case B — implementing later must be unambiguous

A reader who was not in the conversation can implement the feature from the spec
without asking a question about intent.
