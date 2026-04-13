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
args:
  - name: project
    description: Absolute path to the project to audit (optional, defaults to current working directory)
---

# Claude Code Security Review

You are conducting a structured security audit of the user's Claude Code environment.
Work through phases sequentially. **Read-only phases run automatically. Mutating phases
(marked APPROVAL REQUIRED) must pause and ask the user before creating any files,
installing software, or modifying configuration.**

At the end of each phase, print a summary and use `AskUserQuestion` with buttons: `Proceed to Phase N+1` / `Skip` / `Stop`

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

---

## Setup

Determine the target project path:
- If the user provided a `project` argument, use that path
- Otherwise, use the current working directory

Store this as `$PROJECT` for use throughout.

---

## Phase 0: Immediate Flags (read-only)

Run these three checks immediately — they catch the highest-risk issues first.
Do not wait for Phase 1.

**0a. Plaintext credentials in `~/.claude/settings.json`**
```bash
python3 -c "
import json, sys, re
try:
    d = json.load(open('/Users/' + __import__('os').getenv('USER') + '/.claude/settings.json'))
    for name, srv in d.get('mcpServers', {}).items():
        env = srv.get('env', {})
        for k, v in env.items():
            if any(kw in k.upper() for kw in ['PASSWORD','SECRET','TOKEN','KEY','CREDENTIAL']):
                print(f'  HIGH: MCP server [{name}] has plaintext {k} in settings.json')
except: pass
"
```

**0b. `.env` files tracked by git in `$PROJECT`**
```bash
cd "$PROJECT" && git ls-files 2>/dev/null | grep -i '\.env'
```
Any result is HIGH risk — `.env` files should never be committed.

**0c. Shell history credential patterns**
```bash
grep -E "(PASSWORD|SECRET|API_KEY|TOKEN)\s*=" ~/.zsh_history ~/.bash_history 2>/dev/null | head -5
```

Print findings as a table:
```
| Location              | Finding                              | Risk   |
|-----------------------|--------------------------------------|--------|
| settings.json         | Plaintext PASSWORD for [server name] | HIGH   |
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
Read `~/.claude/settings.json` and any `$PROJECT/.mcp.json`. For each server, note:
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
Check for `bypassPermissionsMode` or stale permission entries.

**1f. Project-specific checks (if `$PROJECT` is set)**
```bash
cd "$PROJECT"
find . -name '.env*' -not -path './.git/*' | head -20
grep -rn --include="*.js" --include="*.ts" --include="*.py" --include="*.sh" \
  -E "(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*['\"][^'\"]{8,}" . \
  --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | head -20
cat .gitignore 2>/dev/null | grep -E "\.env|secret|credential" || echo ".gitignore: no secret patterns found"
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
| settings.json         | Plaintext PASSWORD ([server-name] MCP)     | HIGH   |
| PreToolUse hook       | Not configured — no execution guard        | MEDIUM |
| Shell snapshots       | 47 snapshots, 230MB                        | LOW    |
| MCP transport         | stdio only — no network exposure           | LOW    |
```

---

## Phase 2: PreToolUse Hook — Execution Guard (APPROVAL REQUIRED)

**Explain first:** This hook intercepts every Bash command Claude tries to run and blocks
dangerous patterns before they execute. It prevents: pipe-to-shell installs, credential
exfiltration, dangerous flag usage, and recursive deletion of critical directories.

Use `AskUserQuestion` with buttons: "Create `.claude/hooks/security-precheck.sh` and wire it into your Claude settings?"
> Buttons: `Yes` / `No`

If approved, copy `references/hook-security-precheck.sh` to `~/.claude/hooks/security-precheck.sh`.

Then make it executable and wire it into `~/.claude/settings.json`:
```bash
chmod +x ~/.claude/hooks/security-precheck.sh
```

Add to `~/.claude/settings.json` under `hooks`:
```json
"hooks": {
  "PreToolUse": [
    {
      "matcher": "Bash",
      "hooks": [
        {
          "type": "command",
          "command": "~/.claude/hooks/security-precheck.sh"
        }
      ]
    }
  ]
}
```

**Limitation:** This hook catches patterns, not intent. A determined attacker with shell
access can bypass it. It's a speed-bump against accidents and simple prompt injections,
not a security boundary.

---

## Phase 3: Supply Chain Protection (APPROVAL REQUIRED)

**Explain first:** npm/pip packages can run arbitrary code during install via lifecycle
scripts (postinstall). This phase adds scanning tools that check packages before they run.

Use `AskUserQuestion` with buttons: "Install Socket CLI (npm supply chain scanner) and pip-audit (Python CVE scanner)?"
> Buttons: `Yes` / `No`

If approved:
```bash
npm install -g @socket/cli 2>/dev/null && echo "Socket CLI installed" || echo "Socket CLI install failed (npm not found?)"
pipx install pip-audit 2>/dev/null && echo "pip-audit installed" || echo "pip-audit install failed (pipx not found?)"
```

Add Socket check to the PreToolUse hook (append before the final `exit 0`):
```bash
# 6. Socket CLI scan for npm/bun installs
if echo "$CMD" | grep -qE '(npm|bun)\s+install'; then
  PKG=$(echo "$CMD" | grep -oE '[a-z@][a-zA-Z0-9@/_-]+' | tail -1)
  if [ -n "$PKG" ] && command -v socket &>/dev/null; then
    socket npm:report "$PKG" 2>/dev/null | grep -i "high\|critical" && \
      block "Blocked: Socket CLI flagged $PKG as high/critical risk"
  fi
fi
```

Run an initial scan on `$PROJECT`:
```bash
cd "$PROJECT"
[ -f package-lock.json ] && socket npm:report . 2>/dev/null | head -30
[ -f requirements.txt ] && pip-audit -r requirements.txt 2>/dev/null | head -30
```

---

## Phase 4: File-Level Malware Scanning (APPROVAL REQUIRED)

**Explain first:** ClamAV scans downloaded files and newly written files for known malware
signatures. The PostToolUse hook triggers a scan after curl/wget/download commands.

Use `AskUserQuestion` with buttons: "Install ClamAV and set up automatic file scanning?"
> Buttons: `Yes` / `No`

If approved:
```bash
brew install clamav 2>/dev/null && \
  cp /opt/homebrew/etc/clamav/freshclam.conf.sample /opt/homebrew/etc/clamav/freshclam.conf && \
  freshclam && echo "ClamAV ready"
```

Copy `references/hook-security-scan.sh` to `~/.claude/hooks/security-scan.sh`, then:
```bash
chmod +x ~/.claude/hooks/security-scan.sh
```

Wire PostToolUse in `~/.claude/settings.json`:
```json
"PostToolUse": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "command",
        "command": "~/.claude/hooks/security-scan.sh"
      }
    ]
  }
]
```

**Limitation:** ClamAV uses signature-based detection — it misses novel or obfuscated malware.
It catches known threats, not zero-days.

---

## Phase 5: Credential Hygiene & Session Cleanup (APPROVAL REQUIRED)

**5a. Credential scrub in transcripts**

Use `AskUserQuestion` with buttons: "Scan session transcripts for exposed credentials and report findings?"
> Buttons: `Yes` / `No`

If approved, scan `~/.claude/sessions/` for credential patterns:
```bash
grep -rl --include="*.jsonl" -E "(PASSWORD|SECRET|API_KEY|TOKEN)\s*[:=]\s*\S{8,}" \
  ~/.claude/sessions/ 2>/dev/null | head -10
```
Report findings. Do NOT auto-delete — let the user decide.

**5b. Session cleanup hook**

Use `AskUserQuestion` with buttons: "Create a session cleanup script that kills zombie processes and prunes old shell snapshots?"
> Buttons: `Yes` / `No`

If approved, copy `references/hook-session-cleanup.sh` to `~/.claude/hooks/session-cleanup.sh`, then:
```bash
chmod +x ~/.claude/hooks/session-cleanup.sh
```

---

## Phase 6: MCP Server Audit (read-only)

For each MCP server in `~/.claude/settings.json` and `$PROJECT/.mcp.json`, assess and report:

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
- Recommendation: Move credential to system keychain or password manager CLI; reference via
  $(op read "op://vault/[server-name]/password") in the env block
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
| MCP server credentials | HIGH | Plaintext secrets in settings.json |
| PreToolUse hook | [ACTIVE/MISSING] | Execution guard status |
| PostToolUse scan | [ACTIVE/MISSING] | Malware scan status |
| Shell snapshots | LOW | Auto-pruned at 7 days |
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

- If `~/.claude/settings.json` does not exist: skip credential and hook checks in Phases 0–2 and note "No global settings file found — Claude Code may not be configured yet."
- If `$PROJECT` is not a git repository: skip `.env` tracking check (0b) and `.gitignore` coverage (1f); note "Not a git repo — git-based checks skipped."
- If the user declines all APPROVAL REQUIRED phases: produce the Phase 0 + Phase 1 read-only report and the Phase 7 governance doc. Do not treat declining as an error.
- If a scanning tool (Socket CLI, ClamAV, pip-audit) fails to install: log the failure, skip that specific check, and continue with remaining phases. Do not abort the entire audit.
- If `~/.claude/hooks/` already contains a `security-precheck.sh`: read it, compare to the reference version, and use `AskUserQuestion` with buttons: "An existing hook is already installed."
  > Buttons: `Replace with updated version` / `Keep current` / `Show diff`

---

## Final Verification

After all selected phases, run:
```bash
ls -la ~/.claude/hooks/*.sh 2>/dev/null || echo "No hooks installed"
python3 -c "
import json
d = json.load(open('/Users/' + __import__('os').getenv('USER') + '/.claude/settings.json'))
hooks = d.get('hooks', {})
print('PreToolUse:', 'configured' if 'PreToolUse' in hooks else 'MISSING')
print('PostToolUse:', 'configured' if 'PostToolUse' in hooks else 'MISSING')
"
```

Print a final summary: which phases ran, which were skipped, top 3 remaining risks to address.
