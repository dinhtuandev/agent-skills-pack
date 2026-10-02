---
name: debug-fast
description: Debug an error using evidence, not guesswork — read the trace, form ranked hypotheses, prove or kill each one, then fix the root cause. Use whenever the user pastes an error message or stack trace, describes a bug ("works in staging but not prod", "X throws Y when I do Z"), and wants a real fix rather than a guessed patch.
---

# Debug an Error Fast

Do not guess a fix and try it. Guessing wastes the user's time when it's wrong and hides the real bug when it's accidentally right.

If what's "broken" is that unauthorized users can see or change data they shouldn't — that's a security finding, not a functional bug. Fix the one instance here if it's already in front of you, but tell the user this needs a full sweep with `security-audit` rather than treating it as isolated.

## Inputs

- Full error + stack trace
- Steps to reproduce, if known

## Steps

1. Read the stack trace and open the exact files involved — don't reason about the error in the abstract.
2. State expected vs. actual behavior in one line.
3. List 3 hypotheses for the cause, ranked by likelihood.
4. Prove or kill each one with logs or a tiny targeted test — evidence, not vibes. Don't stop at the first plausible-sounding hypothesis without checking it.
5. Fix the root cause, not the symptom. If the fix is "add a null check here," ask whether the null should have been possible at all.
6. Search the repo for the same pattern — if this bug shape exists here, it likely exists elsewhere too.
7. Add a regression test that fails without the fix and passes with it.
8. Tell the user in 2 lines why it broke and why it can't break this way again.

Keep the ranked hypotheses and each one's verdict in `references/hypothesis-ledger.md` as you go — a killed hypothesis on record is what stops the next person from re-testing it, and a bare "alive" list hides which of the three you never actually checked.
