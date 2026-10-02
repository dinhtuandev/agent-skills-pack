#!/usr/bin/env python3
"""Deterministic offline baseline trigger scorer for the 15-skill pack.

Why this exists
---------------
v3's EVAL-REPORT.md judged triggers *by hand*, once, with no repeatable number.
This script gives a fast, offline number you can diff after any description
edit: it ranks every eval query against ALL skill descriptions at once and
reports accuracy plus which skill stole which query.

It is a lexical BM25 baseline, NOT the real model. A high score here does not
prove Claude Code will trigger correctly; a *drop* after an edit is still a
strong signal that you made two descriptions collide.

Usage (from the pack root):
    python scripts/score_triggers.py
    python scripts/score_triggers.py --verbose   # list every misprediction
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "to", "of", "in", "on", "is", "it",
    "this", "that", "with", "when", "use", "using", "you", "your", "i", "we",
    "me", "my", "our", "can", "u", "need", "want", "so", "be", "as", "at",
    "by", "from", "not", "no", "do", "does", "if", "then", "just", "get",
    "got", "make", "made", "up", "out", "about", "into", "than", "also",
}


def tokenize(text: str):
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS and len(t) > 1]


def parse_frontmatter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip()
    return fields


class BM25:
    def __init__(self, docs, k1=1.2, b=0.75):
        self.docs = [Counter(d) for d in docs]
        self.k1, self.b = k1, b
        self.n = len(docs)
        self.avg = sum(sum(c.values()) for c in self.docs) / max(self.n, 1)
        df = Counter()
        for c in self.docs:
            df.update(c.keys())
        self.idf = {t: math.log((self.n - f + 0.5) / (f + 0.5) + 1.0) for t, f in df.items()}

    def score(self, query_tokens, i):
        c = self.docs[i]
        dl = sum(c.values()) or 1
        s = 0.0
        for t in query_tokens:
            tf = c.get(t)
            if not tf:
                continue
            s += self.idf.get(t, 0.0) * (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * dl / (self.avg or 1))
            )
        return s


def load_pack(root: Path):
    skills = []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in {"scripts", "docs"}:
            continue
        md = d / "SKILL.md"
        if not md.is_file():
            continue
        fields = parse_frontmatter(md.read_text(encoding="utf-8"))
        skills.append((d.name, tokenize(d.name + " " + fields.get("description", ""))))
    return skills


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    skills = load_pack(root)
    if not skills:
        print("no skills found under", root)
        return 2

    names = [n for n, _ in skills]
    model = BM25([toks for _, toks in skills])

    total = correct = 0
    tp, fn, fp, confusions = Counter(), Counter(), Counter(), Counter()

    for name, _ in skills:
        eval_path = root / name / "evals" / "trigger-eval.json"
        if not eval_path.is_file():
            continue
        for item in json.loads(eval_path.read_text(encoding="utf-8")):
            q = item.get("query", "")
            qs = tokenize(q)
            scores = [model.score(qs, i) for i in range(len(skills))]
            predicted = names[max(range(len(skills)), key=lambda i: scores[i])]
            total += 1
            if item.get("should_trigger"):
                if predicted == name:
                    correct += 1
                    tp[name] += 1
                else:
                    fn[name] += 1
                    confusions[(name, predicted)] += 1
                    if args.verbose:
                        print(f"  FN  [{name}] {q!r} -> predicted {predicted}")
            else:
                if predicted != name:
                    correct += 1
                else:
                    fp[name] += 1
                    confusions[(name, name)] += 1
                    if args.verbose:
                        print(f"  FP  [{name}] {q!r} -> predicted {predicted}")

    acc = correct / total if total else 0.0
    print(f"baseline trigger accuracy: {acc:.1%}  ({correct}/{total})")
    print()
    print(f"{'skill':<20}{'recall(say yes)':>17}{'false-yes':>11}")
    for name, _ in skills:
        pos = tp[name] + fn[name]
        rec = f"{tp[name]}/{pos}" if pos else "n/a"
        print(f"{name:<20}{rec:>17}{fp[name]:>11}")

    if confusions:
        print()
        print("top confusions (expected -> predicted):")
        for (a, b), c in confusions.most_common(10):
            print(f"  {a} -> {b}: {c}")

    print()
    print("NOTE: lexical baseline, not the real model. Treat a *drop* vs. the")
    print("last run as the signal, not the absolute number. See EVAL-REPORT.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
