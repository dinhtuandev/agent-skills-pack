# scripts/ — offline pack checks

Two scripts that run **without network and without the `claude` CLI** — the repeatable replacement for the manual audit described in `../EVAL-REPORT.md`.

| Script | Answers | Exit code |
|---|---|---|
| `validate_skills.py` | "Is the skill structure still correct?" | 1 on error |
| `score_triggers.py` | "Did a description edit shift the triggering?" | always 0 |

## Run

From the pack root:

```bash
python scripts/validate_skills.py            # all 15 skills
python scripts/validate_skills.py write-prd  # one skill
python scripts/score_triggers.py             # baseline + confusion
python scripts/score_triggers.py --verbose   # print every misprediction
```

Nothing to install — standard library only, Python 3.9+.

## What validate_skills.py checks

Errors (non-zero exit):
- missing `SKILL.md`, or a file that does not open with `---` frontmatter
- missing `name` / `description`
- `name` not kebab-case, or not matching the folder name
- `description` longer than 1024 characters (the Claude Code limit)
- the body references a `references/...`, `scripts/...` or `assets/...` path that does not exist
- missing `evals/trigger-eval.json`, invalid schema, or no `should_trigger` true/false cases

Warnings (do not fail): description shorter than 120 characters, no explicit trigger cue ("use when / wants / asks / says..."), thin body, empty folder, and a skill that ships `references/*-template.md` but has no `evals/output-eval.md` — that last one means the skill's output quality is unverified.

To convince yourself the script works, point a throwaway skill folder at a file that does not exist — it must exit 1:

```bash
mkdir -p _tmp/references
printf '%s\n' \
  '---' \
  'name: tmp' \
  'description: A deliberately long enough description for the validator to accept this as a real skill description string here.' \
  '---' '' \
  'See `references/khong-ton-tai.md` for the missing thing.' > _tmp/SKILL.md
python scripts/validate_skills.py _tmp; echo "exit=$?"   # expect exit=1
rm -rf _tmp
```

## What score_triggers.py measures

For **every query in every eval file**, it scores that query against **all 15 descriptions at once** with BM25, takes the top-scoring description, and compares it with the expected skill. Output: overall accuracy, per-skill recall, and a confusion table (which skill stole which query).

This is a **lexical baseline**, not the real model. Its value is that it is **repeatable**: edit a description, run it again, and if accuracy drops or a new confusion appears, two descriptions have started colliding — exactly the class of bug the v3 audit had to find by eye.

## Limits (read before trusting the numbers)

- Both scripts only read files on disk. They do not prove any Agent Skills client will load the skills correctly — only that the files follow the format and that the descriptions do not collide lexically.
- The real benchmark loop (variance, train/test split, scoring with a different model) still needs `claude -p` inside Claude Code — commands in `../EVAL-REPORT.md`.
- Both scripts were run when this pack was released (2026-10-02): `validate_skills.py` → `15 skill(s): 0 error(s), 0 warning(s)`; `score_triggers.py` → 83.3% (155/186). CI re-runs them on every push.
