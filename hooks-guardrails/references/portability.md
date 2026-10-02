# Hook portability (Windows / macOS / Linux)

The example hooks in `scripts/` are POSIX bash. Claude Code runs a hook through
the platform's shell, so what works on one machine may not start on another.

## What each hook needs

| Hook script | Requires | If missing |
|---|---|---|
| `protect-paths.sh` | `bash`, plus `jq` on PATH | hook errors instead of blocking — safer, but silent |
| `lint-and-typecheck.sh` | `bash` | same: no guard, no visible error |

A silently non-firing guard is the failure mode to watch for. After wiring a
hook, trigger it on purpose and confirm it actually ran (see the skill's Rules).

## Windows

- `.sh` hooks need **Git Bash** or **WSL** on PATH. Without them the command
  fails to start and the guard is simply absent.
- If `jq` is not installed, swap the stdin parse for the standard library —
  e.g. read the JSON with `python -c "import json,sys; print(json.load(sys.stdin)['tool_input']['file_path'])"`.
- Prefer absolute, forward-slashed paths in `command`; `$CLAUDE_PROJECT_DIR`
  expands to a Windows path with backslashes, which some tools mis-handle.

## Minimal jq-free path check (works anywhere Python does)

```bash
python - "$@" <<'PY'
import json, re, sys
data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
protected = [r"(^|/)\.env($|\.)", r"(^|/)migrations/", r"prod.*\.(json|ya?ml)$"]
if any(re.search(p, path, re.I) for p in protected):
    sys.stderr.write(f"blocked: {path} is a protected path\n")
    sys.exit(2)   # exit 2 is what denies a PreToolUse action
PY
```

Remember: for `PreToolUse` only exit code `2` denies the action; any other
non-zero exit is treated as a hook error and does **not** block.
