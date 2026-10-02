# Output eval — implementation-plan

Tests **what the plan contains**, not whether the skill triggered (that is
`evals/trigger-eval.json`).

## Case A — a plan from an approved spec

Input: `the spec at docs/spec-checkout.md is approved, give me a step-by-step build sequence`
Artifact: the plan shown in chat / saved under `docs/`

| # | Check | Pass condition |
|---|---|---|
| 1 | Every template section present | the plan has the H2 sections of `references/plan-template.md`: Build sequence, Risks & open unknowns, Done when |
| 2 | Every step carries five fields | each step lists Files, Change, Migration/new dependency, Verify, Rollback |
| 3 | Verify is a real check | every step has an exact command or an observable behavior, not "test it works" |
| 4 | Rollback is concrete | each risky step's rollback is an actual command/action, never "revert if needed" |
| 5 | Riskiest unknown early | the step most likely to fail is not buried at the end |
| 6 | App stays runnable | the sequence can be stopped after any single step without leaving the app broken |
| 7 | Sized | every step is marked S / M / L |

## Case B — stops for approval

After writing the plan, the skill stops and waits for "go" — it does not start
editing files in the same turn.
