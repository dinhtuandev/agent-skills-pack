# agent-skills-pack — 15 portable Agent Skills

[![validate skills](https://github.com/dinhtuandev/agent-skills-pack/actions/workflows/validate.yml/badge.svg)](https://github.com/dinhtuandev/agent-skills-pack/actions/workflows/validate.yml)

Fifteen skills distilled from a set of prompt cards (write a PRD → turn a task into a skill), packaged in the open **Agent Skills** format: each skill is a folder with a `SKILL.md` (frontmatter `name` + `description`, then the instructions), plus optional `references/` and `evals/`.

Because the format is an open standard, the pack works across coding agents — not just Claude Code. Unlike a prompt card you fill in and paste every time, the agent reads each `description` to decide when the skill applies, then follows it automatically.

Vietnamese version: [README.vi.md](README.vi.md).

## Install

Every Agent Skills client loads a skill the same way: put the skill folder (the one containing `SKILL.md`) into the skills directory that client scans.

1. Clone or download this repo.
2. Copy the skill folders into your client's skills directory.
3. Restart the session — the client loads them, no extra config.

Exact paths differ per client; see the client list and per-client instructions at <https://agentskills.io/clients> rather than guessing.

### Claude Code

- Copy the skill folders into `.claude/skills/` at your project root, or `~/.claude/skills/` to share them across every project.
- Claude Code follows the Agent Skills standard and adds extra frontmatter fields. This pack only uses `name` + `description`, so it stays compatible with every client.

## The 15 skills

| # | Folder | Use it when |
|---|---|---|
| 1 | `write-prd` | Write a full PRD for a feature before any design or code |
| 2 | `create-claude-md` | Scan the repo and write or refresh `CLAUDE.md` (Claude Code only) |
| 3 | `plan-mode` | Force a plan before touching code |
| 4 | `spec-driven-dev` | Lock down a given/when/then spec before coding |
| 5 | `ui-ux-brief` | Produce a full UI/UX brief for a screen or flow |
| 6 | `implementation-plan` | Turn an approved spec or PRD into a step-by-step build sequence |
| 7 | `wire-mcp-server` | Set up an MCP server for a service or API |
| 8 | `connect-database` | Connect a database: schema, migrations, query layer |
| 9 | `security-audit` | Audit for real attack paths, ranked by severity |
| 10 | `debug-fast` | Debug from evidence instead of guessing |
| 11 | `e2e-test` | Write Playwright end-to-end tests for a flow |
| 12 | `cleanup-dead-code` | Find and remove dead code safely |
| 13 | `git-commit` | Split changes into clean conventional commits |
| 14 | `hooks-guardrails` | Set up Claude Code hooks as guardrails (Claude Code only) |
| 15 | `task-to-skill` | Turn a repeated task into a new skill (meta) |

## Verify the pack

Two dependency-free Python scripts (3.9+) check the pack offline — no network, no `claude` CLI:

```bash
python scripts/validate_skills.py     # structure: frontmatter, naming, referenced files, eval schema
python scripts/score_triggers.py      # repeatable trigger baseline + confusion matrix
```

`validate_skills.py` exits 1 on a structural error, so it runs unchanged in CI — see `.github/workflows/validate.yml`. Details and limits: [scripts/README.md](scripts/README.md).

## Contributing

1. Add or edit a skill folder: a `SKILL.md` with `name` (kebab-case, matching the folder) and a `description` that states when to use it *and* when not to.
2. Keep the frontmatter to `name` and `description`. Any other key is a client extension that other agents may ignore.
3. Put reference material in `references/` and per-skill eval cases in `evals/`.
4. Run `python scripts/validate_skills.py` before opening a PR. CI runs the same check plus `score_triggers.py`.

## Version history

The pack went through five revisions before this release: v2 fixed the PRD → spec → plan chain and added templates, v3 added trigger evals, v4 added the offline verification scripts, v5 added output-quality rubrics. The detailed changelog for each revision is written in Vietnamese and lives in [README.vi.md](README.vi.md); the trigger-eval methodology and findings are in [EVAL-REPORT.md](EVAL-REPORT.md), also Vietnamese.

## License

[MIT](LICENSE).
