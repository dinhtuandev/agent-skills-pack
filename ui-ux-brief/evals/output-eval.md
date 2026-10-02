# Output eval — ui-ux-brief

Tests **what the brief contains**, not whether the skill triggered (that is
`evals/trigger-eval.json`).

## Case A — a screen brief

Input: `full UI/UX brief for the 'invite teammates' modal before engineering builds it`
Artifact: `docs/design-brief-invite-teammates.md`

| # | Check | Pass condition |
|---|---|---|
| 1 | Every template section present | the file has every H2 in `references/brief-template.md`: User journey, Layout per screen, Component inventory, Typography + color tokens, Motion, Accessibility notes |
| 2 | All component states covered | each row of the component inventory fills Default, Hover, Empty, Error and Loading — not just the happy state |
| 3 | Tokens are named values | typography/color entries are concrete values (e.g. `#1F2933`, `16px/1.5`), not "brand blue" |
| 4 | Motion is specified | each animated element names a duration and an easing, not "animates nicely" |
| 5 | Accessibility is actionable | contrast ratios, focus order, screen-reader labels and keyboard nav are all present |
| 6 | Informed, not copied | if a reference product is named, the brief names the *pattern* borrowed, not a reproduced layout or asset |

## Case B — a named-inspiration flow

Input: `we like Linear and Stripe's onboarding, brief our own onboarding flow`

- The brief reads as this product's own design language.
- No Linear or Stripe layout, screen or asset is reproduced.
