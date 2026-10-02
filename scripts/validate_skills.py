#!/usr/bin/env python3
"""Structural validator for this Claude Code skills pack.

Usage (from the pack root):
    python scripts/validate_skills.py            # validate every skill folder
    python scripts/validate_skills.py write-prd  # validate one skill

What it is
----------
v3 shipped a *manual* lint of the 15 descriptions (see EVAL-REPORT.md). This is
the same lint, made mechanical and repeatable: the cheap regression gate you run
after editing any SKILL.md, before the slower, CLI-bound trigger loop.

It does NOT test triggering. For that see `scripts/score_triggers.py`
(deterministic offline baseline) and EVAL-REPORT.md (the real `claude -p` loop).

Exit code 0 = no errors; 1 = at least one error. Warnings never fail the run.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# paths the body tells Claude to open, e.g. `references/foo.md`
RESOURCE_RE = re.compile(r"`((?:references|scripts|assets)/[^`\n]+)`")
TRIGGER_CUE_RE = re.compile(
    r"\b(use when|use whenever|use for|use this|whenever|asks? (?:for|to)|"
    r"wants? (?:to|a|an)|says|request(?:s|ed)?|invoke|trigger)\b",
    re.I,
)

DESCRIPTION_LIMIT = 1024  # Claude Code hard limit
DESCRIPTION_MIN = 120     # below this a description usually under-triggers
BODY_MIN = 400


def parse_frontmatter(text: str):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    fields = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, text[m.end():]


def validate_eval(skill_dir: Path):
    eval_path = skill_dir / "evals" / "trigger-eval.json"
    if not eval_path.is_file():
        return ["no evals/trigger-eval.json"]
    try:
        data = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"evals/trigger-eval.json is not valid JSON: {exc}"]
    if not isinstance(data, list) or not data:
        return ["evals/trigger-eval.json must be a non-empty list"]
    problems = []
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            problems.append(f"eval #{i} is not an object")
            continue
        if not isinstance(item.get("query"), str) or not item["query"].strip():
            problems.append(f"eval #{i} has no non-empty `query`")
        if not isinstance(item.get("should_trigger"), bool):
            problems.append(f"eval #{i} `should_trigger` must be true/false")
    n_yes = sum(1 for i in data if isinstance(i, dict) and i.get("should_trigger") is True)
    n_no = sum(1 for i in data if isinstance(i, dict) and i.get("should_trigger") is False)
    if n_yes == 0:
        problems.append("eval set has no should_trigger=true cases")
    if n_no == 0:
        problems.append("eval set has no should_trigger=false cases")
    return problems


def validate_skill(skill_dir: Path):
    errors, warnings = [], []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: no SKILL.md"], []

    fields, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if fields is None:
        return ["SKILL.md does not start with `---` YAML frontmatter"], []

    name = fields.get("name", "")
    description = fields.get("description", "")

    if not name:
        errors.append("frontmatter is missing `name`")
    elif not KEBAB_RE.match(name):
        errors.append(f"name `{name}` is not kebab-case")
    elif name != skill_dir.name:
        errors.append(f"name `{name}` != folder `{skill_dir.name}`")

    if not description:
        errors.append("frontmatter is missing `description`")
    else:
        if len(description) > DESCRIPTION_LIMIT:
            errors.append(
                f"description is {len(description)} chars, over the {DESCRIPTION_LIMIT} limit"
            )
        if len(description) < DESCRIPTION_MIN:
            warnings.append(
                f"description is only {len(description)} chars - likely to under-trigger"
            )
        if not TRIGGER_CUE_RE.search(description):
            warnings.append("description has no explicit 'use when/wants/asks' trigger cue")

    # Agent Skills standard only guarantees `name` and `description`; any other
    # frontmatter key is a client extension other agents are free to ignore.
    extra_keys = sorted(set(fields) - {"name", "description"})
    if extra_keys:
        warnings.append(
            f"non-standard frontmatter key(s): {', '.join(extra_keys)} - "
            "other Agent Skills clients may ignore them"
        )

    if len(body.strip()) < BODY_MIN:
        warnings.append(f"body is only {len(body.strip())} chars - thin for a skill")

    for resource in sorted(set(RESOURCE_RE.findall(body))):
        if not (skill_dir / resource).exists():
            errors.append(f"body points at `{resource}` but the file does not exist")

    for extra in ("references", "assets"):
        d = skill_dir / extra
        if d.is_dir() and not any(d.iterdir()):
            warnings.append(f"`{extra}/` exists but is empty")

    # a skill that ships a template should also carry an output-quality rubric
    refs = skill_dir / "references"
    templates = sorted(refs.glob("*-template.md")) if refs.is_dir() else []
    if templates and not (skill_dir / "evals" / "output-eval.md").is_file():
        warnings.append(
            "has references/*-template.md but no evals/output-eval.md - output quality stays unverified"
        )

    errors.extend(validate_eval(skill_dir))
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", help="skill folders (default: all)")
    parser.add_argument("--root", default=None, help="pack root (default: parent of scripts/)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    if args.skills:
        skill_dirs = [root / s for s in args.skills]
    else:
        skill_dirs = sorted(
            d for d in root.iterdir()
            if d.is_dir() and not d.name.startswith(".") and d.name not in {"scripts", "docs"}
        )

    total_errors = total_warnings = 0
    for skill_dir in skill_dirs:
        if not skill_dir.is_dir():
            print(f"FAIL  {skill_dir.name}: not a directory")
            total_errors += 1
            continue
        errors, warnings = validate_skill(skill_dir)
        print(f"{'ok  ' if not errors else 'FAIL'}  {skill_dir.name}")
        for e in errors:
            print(f"        error: {e}")
        for w in warnings:
            print(f"        warn : {w}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    print()
    print(f"{len(skill_dirs)} skill(s): {total_errors} error(s), {total_warnings} warning(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
