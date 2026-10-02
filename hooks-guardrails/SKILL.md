---
name: hooks-guardrails
description: Set up Claude Code hooks (PostToolUse, PreToolUse, Stop, Notification) as automated guardrails for a project. Use when the user wants lint/typecheck-on-edit, wants to protect certain paths (migrations, .env, prod config) from being touched, wants tests to run before a session ends, or wants a notification when input is needed — i.e. whenever they mention Claude Code hooks or guardrails. Claude Code only — hooks don't fire in claude.ai or Cowork sessions.
---

# Hooks as Guardrails

Hooks turn rules the user would otherwise have to repeat every session into something enforced automatically.

**Compatibility:** this is Claude Code specific. Hooks read `.claude/settings.json` and run at Claude Code's tool-call lifecycle — they don't exist as a concept in claude.ai or Cowork. If the user is in one of those, say so rather than writing a hook that will silently never fire.

Also distinct from **git hooks** (husky, pre-commit — these run on `git commit`, not on Claude's tool calls) and **React hooks** (`useEffect` etc.) — same word, unrelated mechanisms. If the request doesn't mention PostToolUse/PreToolUse/Stop/Notification or Claude Code specifically, check which one is actually meant before wiring anything.

**Platform:** the `.sh` examples need bash — on Windows that means Git Bash or WSL on PATH, and `protect-paths.sh` additionally needs `jq`. `references/portability.md` has a jq-free path check that works wherever Python does, so a guard doesn't silently fail to start.

## Inputs

Stack + package manager, so the right lint/typecheck/test commands get wired in.

## Set up

- **PostToolUse**: run lint + typecheck after every file edit, and feed errors straight back so they get fixed in the same turn rather than piling up.
- **PreToolUse**: block edits to protected paths — migrations, `.env`, prod config are sensible defaults; confirm the exact list with the user for this project.
- **Stop**: run the test suite before a session ends, so broken code doesn't get left behind silently.
- **Notification**: ping the user (sound, Slack, or whatever they specify) when their input is needed.

`references/settings-example.json` and `scripts/` have working examples of each of these — start from them and adapt rather than writing the JSON shape from memory, since a subtly wrong field name means the hook silently never fires.

## Rules

- Write the hook scripts and the corresponding `settings.json` entries together — a hook without the settings entry does nothing.
- Keep each script focused on one check. If lint and typecheck need different failure messages or one is much slower than the other, that's a sign to split them into two hooks rather than growing one script — not a fixed line count, just: a hook script should be easy to read in one pass.
- **Exit codes matter and aren't interchangeable.** For `PreToolUse`, exit code `2` specifically means "deny this action" and its stderr is fed back to Claude — any other non-zero code is just treated as a hook error, not a block. For `PostToolUse` and `Stop`, non-zero simply surfaces the failure. Get this wrong and a "blocking" hook silently does nothing.
- After setting each one up, trigger it on purpose and show the user it actually firing — don't just claim it's wired up.
