---
name: security-review
description: >
  Run a phased security audit of Claude Code configuration and a target project.
  Use when the user asks to: review security, audit Claude Code setup, check for
  exposed credentials, set up security hooks, harden their Claude environment,
  scan a project for secrets, or anything like "check if my setup is secure",
  "audit my Claude config", "set up security hooks", "scan for credentials".
  Accepts an optional project path argument (e.g. `/security-review /path/to/project`)
  to scope project-level checks; defaults to the current working directory if omitted.
---

# Claude Code Security Review

You are conducting a structured security audit of the user's Claude Code environment.
Work through phases sequentially. **Read-only phases run automatically. Mutating phases
(marked APPROVAL REQUIRED) must pause and ask the user before creating any files,
installing software, or modifying configuration.**

At the end of each phase, print a summary and use `AskUserQuestion` with buttons: `Proceed to Phase N+1` / `Skip` / `Stop`

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

> **OS scope:** The commands in this skill are macOS-first (`sw_vers`, Homebrew paths). On Linux, adapt package installs (e.g. apt/dnf instead of brew) and paths; Phases 1a and 4 are macOS-specific as written.

---

## Setup

Determine the target project path:
- If the user provided a path argument (e.g. `/security-review /path/to/project`), use that path
- Otherwise, use the current working directory

Store this as `$PROJECT` for use throughout.

Also store `$SKILL_DIR` — the directory containing this `SKILL.md`. Every `references/…` path in
this skill and in `references/phases-2-5-install.md` must be written as `"$SKILL_DIR/references/…"`.
Phase 1f changes the working directory to `$PROJECT`, so a bare `references/…` afterwards resolves
against the target project, where it either finds nothing or — worse for the drift check in Phase
5b — silently compares against the wrong file.

---

## Phase 0: Immediate Flags (read-only)

Run these three checks immediately — they catch the highest-risk issues first.
Do not wait for Phase 1.

**0a. Plaintext credentials in MCP configs**
MCP servers live in `~/.claude.json` and `.mcp.json` (Claude Code) or `claude_desktop_config.json` (Cowork/Desktop) — not `settings.json`. Scan all that exist:
```bash
python3 -c "
import json, os
home = os.path.expanduser('~')
configs = [
    home + '/.claude.json',
    os.environ.get('PROJECT', '.') + '/.mcp.json',
    home + '/Library/Application Support/Claude/claude_desktop_config.json',
]
def scan(d, src):
    for name, srv in d.get('mcpServers', {}).items():
        for k in srv.get('env', {}):
            if any(kw in k.upper() for kw in ['PASSWORD','SECRET','TOKEN','KEY','CREDENTIAL']):
                print(f'  HIGH: MCP server [{name}] has plaintext {k} in {src}')
for path in configs:
    try:
        d = json.load(open(path))
        scan(d, os.path.basename(path))
        for proj in d.get('projects', {}).values():   # ~/.claude.json nests per-project servers
            scan(proj, os.path.basename(path))
    except Exception: pass
"
```

**0b. Sensitive files tracked by git in `$PROJECT`**
```bash
cd "$PROJECT" && git ls-files 2>/dev/null | grep -iE '\.env|secret|credential|key|token'
```
Any result is HIGH risk — `.env` and credential files should never be committed. (Review matches: some may be false positives, e.g. `keyboard.js`.)

**0c. Shell history credential patterns**
```bash
grep -E "(PASSWORD|SECRET|API_KEY|TOKEN)\s*=" ~/.zsh_history ~/.bash_history 2>/dev/null | head -5
```

Print findings as a table:
```
| Location              | Finding                              | Risk   |
|-----------------------|--------------------------------------|--------|
| ~/.claude.json        | Plaintext PASSWORD for [server name] | HIGH   |
```

If no issues found, say "Phase 0: No immediate flags found."

---

## Phase 1: Full Posture Assessment (read-only)

Run all checks, then produce a consolidated risk table.

**1a. OS and privilege**
```bash
sw_vers && whoami && groups $(whoami) | grep -q admin && echo "IS ADMIN" || echo "not admin"
```

**1b. Running Claude Code processes**
```bash
ps aux | grep -i "claude" | grep -v grep
```
Flag any process with 0% CPU running >2h as a zombie.

**1c. MCP server inventory**
Read `~/.claude.json`, any `$PROJECT/.mcp.json`, and (if present) `~/Library/Application Support/Claude/claude_desktop_config.json`. For each server, note:
- Transport type (stdio vs HTTP)
- Whether env block contains secrets (flag if so)
- Whether version is pinned

**1d. Current hooks**
```bash
ls ~/.claude/hooks/ 2>/dev/null && cat ~/.claude/hooks/*.sh 2>/dev/null || echo "No hooks configured"
```
Note which of PreToolUse / PostToolUse hooks are missing.

**1e. Permission mode**
```bash
cat ~/.claude/settings.local.json 2>/dev/null || echo "No settings.local.json"
```
Check for `permissions.defaultMode` set to `"bypassPermissions"`, or stale permission entries.

**1f. Project-specific checks (if `$PROJECT` is set)**

Run in a subshell so the working directory does not leak into later phases:
```bash
( cd "$PROJECT"
  find . -name '.env*' -not -path './.git/*' | head -20
  grep -rn --include="*.js" --include="*.ts" --include="*.py" --include="*.sh" \
    -E "(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*['\"][^'\"]{8,}" . \
    --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | head -20
  cat .gitignore 2>/dev/null | grep -E "\.env|secret|credential" || echo ".gitignore: no secret patterns found" )
```

**1g. Shell snapshots**
```bash
ls -la ~/.claude/shell-snapshots/ 2>/dev/null | wc -l && \
du -sh ~/.claude/shell-snapshots/ 2>/dev/null
```
Report count and size; flag if >100 snapshots.

Print consolidated risk table:
```
| Area                  | Finding                                    | Risk   |
|-----------------------|--------------------------------------------|--------|
| ~/.claude.json        | Plaintext PASSWORD ([server-name] MCP)     | HIGH   |
| PreToolUse hook       | Not configured — no execution guard        | MEDIUM |
| Shell snapshots       | 47 snapshots, 230MB                        | LOW    |
| MCP transport         | stdio only — no network exposure           | LOW    |
```

---

## Phases 2-5: the mutating phases (APPROVAL REQUIRED)

These four install software, write hook files, or modify `~/.claude/settings.json`. Their
procedures live in **`references/phases-2-5-install.md`** — read it when the user opts into one,
not before. A user who declines all four still gets a complete audit from Phases 0, 1, 6 and 7,
so do not treat declining as a failed run.

| Phase | What it does | Reads/writes |
|---|---|---|
| **2** | PreToolUse execution guard — installs `security-precheck.sh` and merges it into `settings.json` | `~/.claude/hooks/`, `~/.claude/settings.json` |
| **3** | Supply chain — Socket CLI and pip-audit, plus an npm-install check appended to the Phase 2 hook | global npm/pipx, the Phase 2 hook |
| **4** | File-level malware scanning — ClamAV and a PostToolUse scan hook | Homebrew, `~/.claude/hooks/`, `~/.claude/settings.json` |
| **5** | Credential hygiene in transcripts (5a, read-only scan) and the session cleanup script (5b) | `~/.claude/projects/` (read), `~/.claude/hooks/` |

**Phase numbers are a cited surface.** `12_SECURITY.md` points readers at Phases 0b, 2, 3, 5 and 6
by number. Moving a phase into a reference file is fine; renumbering one is not.

Ask before each, with `AskUserQuestion` buttons, and act only on an explicit yes.

---

## Phase 6: MCP Server Audit (read-only)

For each MCP server in `~/.claude.json`, `$PROJECT/.mcp.json`, and (if present) `claude_desktop_config.json`, assess and report:

| Field | What to check |
|---|---|
| Transport | stdio (local) = LOW risk; HTTP = MEDIUM/HIGH depending on auth |
| Source | Official/known = LOW; unknown GitHub = HIGH |
| Version pinning | Pinned = LOW; `latest` or no pin = MEDIUM |
| Secrets in env | Any plaintext secret = HIGH |
| Network exposure | Accessible over network? Rate as HIGH |

Print a per-server risk card:
```
### MCP: [server-name]
- Transport: stdio (local process)
- Source: local file (/Users/.../dist/index.js)
- Version pinning: not applicable (local build)
- Secrets in env: YES — [SERVER]_PASSWORD in plaintext → HIGH RISK
- Recommendation: Move credential to system keychain or password manager CLI, and launch the
  server via a wrapper script that exports it, e.g.
  `MY_TOKEN="$(op read 'op://vault/[server-name]/password')" exec npx ...`
  (Note: `$(...)` inside the JSON env block is NOT expanded — the literal text becomes the value.)
```

---

## Phase 7: Governance & Documentation (read-only — outputs a report)

Generate a security documentation file at `$PROJECT/SECURITY_AUDIT.md` (or `~/CLAUDE_SECURITY_AUDIT.md` if no project):

```markdown
# Claude Code Security Audit
Generated: [date]

## Attack Surface

| Area | Risk | Notes |
|------|------|-------|
| MCP server credentials | HIGH | Plaintext secrets in MCP config files |
| PreToolUse hook | [ACTIVE/MISSING] | Execution guard status |
| PostToolUse scan | [ACTIVE/MISSING] | Malware scan status |
| Shell snapshots | LOW | Auto-pruned at 7 days (verify current behavior) |
| Session transcripts | MEDIUM | Manual review recommended |

## Maintenance Schedule

| Task | Frequency | Method |
|------|-----------|--------|
| ClamAV signature update | Daily | freshclam (auto via launchd) |
| Shell snapshot prune | Per session | session-cleanup.sh hook |
| Transcript credential scan | Quarterly | Manual run of Phase 5a |
| MCP server review | When adding new server | Run Phase 6 |
| Full re-audit | Quarterly | Re-run /security-review |
```

---

## Edge Cases

- If `~/.claude/settings.json` does not exist: skip the hook checks and note "No global settings file found — Claude Code may not be configured yet." (Credential checks in 0a use the MCP config files, not settings.json.)
- If `$PROJECT` is not a git repository: skip `.env` tracking check (0b) and `.gitignore` coverage (1f); note "Not a git repo — git-based checks skipped."
- If the user declines all APPROVAL REQUIRED phases: produce the Phase 0 + Phase 1 read-only report and the Phase 7 governance doc. Do not treat declining as an error.
- If a scanning tool (Socket CLI, ClamAV, pip-audit) fails to install: log the failure, skip that specific check, and continue with remaining phases. Do not abort the entire audit.
- If `~/.claude/hooks/` already contains a `security-precheck.sh`: read it, compare to `"$SKILL_DIR/references/hook-security-precheck.sh"`, and use `AskUserQuestion` with buttons: "An existing hook is already installed."
  > Buttons: `Replace with updated version` / `Keep current` / `Show diff`

---

## Final Verification

After all selected phases, run:
```bash
ls -la ~/.claude/hooks/*.sh 2>/dev/null || echo "No hooks installed"
python3 -c "
import json, pathlib
p = pathlib.Path.home() / '.claude' / 'settings.json'
hooks = json.loads(p.read_text()).get('hooks', {}) if p.exists() else {}
print('PreToolUse:', 'configured' if 'PreToolUse' in hooks else 'MISSING')
print('PostToolUse:', 'configured' if 'PostToolUse' in hooks else 'MISSING')
"
```

Print a final summary: which phases ran, which were skipped, top 3 remaining risks to address.
