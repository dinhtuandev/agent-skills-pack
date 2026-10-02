# Output eval — write-prd

Tests **what the PRD contains**, not whether the skill triggered (that is
`evals/trigger-eval.json`). Run the skill with the input below, then check the
saved file against every row.

## Case A — a mature feature idea

Input: `write the PRD for a saved-searches feature`
Artifact: `docs/prd-saved-searches.md`

| # | Check | Pass condition |
|---|---|---|
| 1 | Every template section present | the file has every H2 in `references/prd-template.md`: Problem statement, Success metrics, Users, User stories, Scope, Data model changes, Edge cases + failure states, Open questions |
| 2 | Metrics are measurable | Success metrics names a number or a rate, not "improved UX" |
| 3 | Acceptance criteria are checkable | every user story has at least one criterion that is plainly true/false |
| 4 | Non-goals are explicit | Scope has a non-empty "Explicitly not in v1" list |
| 5 | Failure states covered | the Edge cases table has at least one non-happy-path row |
| 6 | No filler adjectives | none of: robust, seamless, intuitive, world-class |
| 7 | Undecided things stay undecided | anything unresolved sits in Open questions, not silently decided |

## Case B — a vague one-liner

Input: `define this feature for me: users should be able to export data as CSV`

- The skill asks for the missing pieces (users, success metrics) instead of inventing them.
- The resulting PRD is under two pages.
