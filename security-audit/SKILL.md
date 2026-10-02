---
name: security-audit
description: Run an adversarial security audit on a codebase — hunting for real, exploitable gaps with exact file:line references, not generic advice. Use when the user asks for a security review, wants to find vulnerabilities, says "audit this for security gaps" / "find security issues," or wants an auth/injection/IDOR/secrets sweep before shipping.
---

# Find Security Gaps

Audit like you're trying to get in, not like you're filling out a checklist. This is a review of the user's own code at their request — treat it as a defensive exercise.

## Scope

This skill covers static review of code the user owns or has the right to review — not probing a live system, and not a target the user only describes without owning. If a request drifts toward testing someone else's production system or building a general-purpose exploit tool rather than fixing a finding in front of you, that's outside this skill.

Confirm the priority areas — auth, payments, user data, or others — before diving in if not already specified.

If the user describes this as a bug — "users can see data that isn't theirs," "this endpoint returns stuff it shouldn't" — that's an IDOR/auth finding, not a one-off fix. Treat it as the entry point to a full sweep here rather than sending them to `debug-fast` for a single-instance patch.

## Check

- **Secrets** in code, config files, or git history (not just the current working tree)
- **Injection**: SQL, XSS, command injection, path traversal
- **Auth**: routes missing auth checks, weak session handling, broken/open redirects
- **IDOR**: can user A read or modify user B's data by changing an ID?
- **File uploads + input validation** on every form and endpoint that accepts user input
- **Dependency CVEs** — actually run the audit tool for the stack and read the output, don't skip straight to "looks fine"
- **Rate limiting** on expensive or abusable endpoints
- **What leaks through error messages and logs** — stack traces, internal paths, PII in log lines

## Output

Use `references/findings-report.md` for the report shape — the summary counts, and the "checked, no issue found" and "not covered" sections matter as much as the findings themselves, because silence otherwise reads as a clean bill.

Rank findings by severity with the exact `file:line`. Fix the critical ones now, in this session. List the rest as tickets with rough effort estimates — don't leave the user with a wall of findings and no sense of what to do first.

For each finding, include just enough to prove it's real and guide the fix — the vulnerable line, the request shape or input that triggers it, and expected vs. actual behavior. That's different from a polished, ready-to-run exploit script; the audit's job is convincing the user and pointing at the fix, not producing standalone attack tooling.
