---
name: task-to-skill
description: Turn a repetitive manual task into a reusable Claude Code skill saved to .claude/skills/[name]/SKILL.md. Use when the user describes something they keep doing by hand and wants it automated or made repeatable, says "turn this into a skill" / "make this a skill", or wants a workflow captured so future sessions handle it the same way without re-explaining it.
---

# Turn a Task Into a Skill

If the task was just described or performed earlier in this conversation, extract the workflow from what already happened — the steps taken, the format used, any corrections the user made — before asking questions. Fill genuine gaps with the user, don't just theorize about intent.

## Steps

1. Get the task and its steps, if not already clear from context.
2. Create `.claude/skills/[name]/SKILL.md` — kebab-case name, one skill per folder.
3. **Frontmatter**: `name` + a `description` that states what the skill does *and* the actual trigger phrases the user says — not a generic paraphrase. Make it a little assertive about when to use it, since skills that undersell themselves in their own description don't get triggered when they should.
4. **Body**: a numbered workflow, the user's actual conventions (not generic best practice), and edge cases worth calling out.
5. **Ask vs. infer**: state explicitly what the skill should ask the user for each time vs. what it should figure out on its own from context/repo state.
6. **Done criteria**: what "finished" looks like for this task, concretely enough to check against.

## After drafting

Dry-run the skill against a real example and refine it until the output matches how the user actually does the task by hand — not a plausible-looking approximation of it.

If a `skill-creator` skill is available and the user wants to go further than one dry run — proper test cases, comparing trigger phrasing, iterating on description accuracy — hand off to it rather than reinventing that loop here. This skill's job is fast, faithful capture of a workflow that already exists; treat rigorous testing and description tuning as skill-creator's job.
