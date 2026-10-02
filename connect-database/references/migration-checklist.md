# Migration Checklist — [feature / change]

One block per migration. A migration without a documented rollback is not done.

## Migration: [name]

- **File:** `[path/to/migration]`
- **Change:** [tables/columns/indexes added or altered]
- **Forward:** `[exact command to apply]`
- **Rollback:** `[exact command or SQL to undo]`
- **Data risk:** [does it drop/rename a column, backfill, or lock a big table?]
- **Verify:** [query or check that proves it applied]

(repeat per migration)

## Environment variables

| Name | Added to `.env.example` | Committed with a real value? |
|---|---|---|
| | yes / no | must be **no** |

## Round-trip proof

- [ ] Seeded one row
- [ ] Read it back
- [ ] Actual output pasted below

```text
[paste the real output here — a connection isn't done until something
round-tripped through it]
```

## Access rules (multi-tenant only)

- [ ] Row-level security / access rules in place, not deferred to "later"

## Connection pooling

- [ ] Set up if the deployment target is serverless
