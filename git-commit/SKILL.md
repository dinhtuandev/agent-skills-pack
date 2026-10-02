---
name: git-commit
description: Split staged changes into clean, properly formatted git commits following conventional commits (or the project's own convention). Use when the user asks to commit their changes, wants help writing a commit message, or says "commit this properly" or "clean up these commits."
---

# Write Clean Git Commits

## Convention

Default to Conventional Commits unless the repo's existing history shows a different pattern — check recent commits before assuming.

## Rules

- **Split unrelated changes into separate commits.** A commit should tell one story.
- **Format**: `type(scope): what changed and why` — types: `feat` / `fix` / `refactor` / `chore` / `docs` / `test`
- **Subject** under 50 characters, imperative mood ("add", not "added" or "adds")
- **Body** explains the *why*, wrapped at 72 characters — the diff already shows the what
- **Reference the ticket ID** if the user has given one or the repo convention expects it
- **Never mix a refactor with a behavior change** in one commit — split them even if it means slightly more commits
- **Never commit secrets, `.env` files, or generated files** — check the staged diff for these before committing anything

## Process

Show the user the plan first — which files go in which commit, with proposed messages — before committing anything. Then commit one at a time, so they can stop you between commits if something looks off.
