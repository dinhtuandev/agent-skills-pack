---
name: create-claude-md
description: Scan a codebase and generate or refresh its CLAUDE.md project-memory file. Use whenever the user asks to create a CLAUDE.md, set up project instructions for Claude Code, document a repo's conventions for future sessions, or onboard Claude to a new codebase — even if phrased casually like "scan this repo and leave yourself notes."
---

# Create CLAUDE.md

CLAUDE.md is read by every future session on this repo. Everything in it must be true of *this* codebase specifically — nothing generic, nothing invented.

## Workflow

1. **Scan before writing anything.** Read the manifest (`package.json`, `pom.xml`, `requirements.txt`, etc.), the folder structure, config files, and a representative sample of source files and tests. Don't draft from assumptions about "how projects like this usually look."
2. **Draft the sections below**, each grounded in something you actually read:
   - What this project is, in 2 lines
   - Tech stack + the versions that matter (pull real version numbers from the manifest, not guesses)
   - Commands: dev / build / test / lint — copy them from package scripts or the actual CI config
   - Architecture: where things live and why (based on the real folder layout)
   - Code conventions you actually detect in the code (naming, error handling patterns, file organization) — not generic style-guide advice
   - Hard rules: what to never touch without asking — infer candidates (migrations, auth, payment code, generated files) but confirm anything you're not sure is actually off-limits
   - Gotchas a new engineer would hit in week 1 — things you noticed while scanning that aren't obvious from the code alone
3. **Write every rule as a short imperative** ("Use `zod` for all API input validation", not "This project generally prefers to validate input").

## Ask vs. infer

Infer: stack, versions, commands, folder layout, conventions visible in the code.
Ask: anything you can't verify by reading — especially "hard rules" about what's off-limits, since guessing wrong there is worse than leaving a gap. If unsure about a rule, ask instead of inventing it.

## Done when

`CLAUDE.md` exists at the project root, every line is traceable to something in the repo, and nothing in it is boilerplate that would apply equally to any other project.
