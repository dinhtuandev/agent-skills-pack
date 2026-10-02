---
name: connect-database
description: Connect an application to a database — client setup, schema/migrations, and typed query helpers. Use when the user wants to wire up a database, design or add tables, write migrations, set up row-level security for a multi-tenant app, or build the data layer for an app.
---

# Connect Your Database

## Steps

1. **Pick the client that fits the stack** and justify it in one line — don't default to the trendiest ORM if the stack already implies something else.
2. **Env vars**: name them clearly, add to `.env.example`, never commit real values.
3. **Schema**: design tables for the relevant entities with types, relations, and indexes on the queries that will actually run hot. If the user prefers writing DDL and triggers by hand rather than relying on an ORM's generated migrations, write raw SQL migrations and hand-authored triggers instead — ask if unclear which they want for this project.
4. **Create and run the migrations**, and show the exact rollback for each one — a migration without a documented rollback isn't done.
5. **Centralize data access — don't scatter raw SQL through components or route handlers.** A typed query helper per table is the default if nothing else is established, but match whatever pattern the codebase already uses (repository classes, GraphQL resolvers, the ORM's own generated methods). The goal is one place to change a query, not a specific file shape.
6. **Access rules / row-level security** if the app is multi-tenant — don't skip this because it's "for later."
7. **Connection pooling** if the deployment target is serverless.

## Prove it

Seed one row, read it back, and show the actual output. A database connection isn't done until something round-tripped through it.

`references/migration-checklist.md` has the per-migration record to fill in — forward command, rollback, data risk, and the round-trip proof pasted in.
