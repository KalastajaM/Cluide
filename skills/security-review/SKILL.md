---
name: security-review
description: >
  Run a phased security audit of Claude Code configuration and a target project.
  Use when the user asks to: review security, audit Claude Code setup, check for
  exposed credentials, set up security hooks, harden their Claude environment,
  scan a project for secrets, or anything like "check if my setup is secure",
  "audit my Claude config", "set up security hooks", "scan for credentials".
  Accepts an optional project path argument to scope project-level checks.
args:
  - name: project
    description: Absolute path to the project to audit (optional, defaults to current working directory)
---

# Claude Code Security Review

You are conducting a structured security audit of the user's Claude Code environment.
Work through phases sequentially. **Read-only phases run automatically. Mutating phases
(marked APPROVAL REQUIRED) must pause and ask the user before creating any files,
installing software, or modifying configuration.**

At the end of each phase, print a summary and ask: "Proceed to Phase N+1, skip it, or stop?"

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
# .env files not in .gitignore
cd "$PROJECT"
find . -name '.env*' -not -path './.git/*' | head -20

# Hardcoded secret patterns in source
grep -rn --include="*.js" --include="*.ts" --include="*.py" --include="*.sh" \
  -E "(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*['\"][^'\"]{8,}" . \
  --exclude-dir=node_modules --exclude-dir=.git 2>/dev/null | head -20

# .gitignore coverage
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

**Ask the user:** "Create `.claude/hooks/security-precheck.sh` and wire it into your
Claude settings? (yes/no)"

If approved, write exactly this file to `~/.claude/hooks/security-precheck.sh`:

```bash
#!/usr/bin/env bash
# Claude Code PreToolUse security gate
# Blocks dangerous Bash commands before execution
# Input: JSON on stdin with .tool_input.command

set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

block() {
  echo "{\"decision\":\"block\",\"reason\":\"$1\"}"
  exit 0
}

# 1. Dangerous flags
echo "$CMD" | grep -qE -- '--dangerously-skip-permissions|--no-verify.*git|--force.*push' && \
  block "Blocked: dangerous flag detected"

# 2. Pipe-to-shell (supply chain attack vector)
echo "$CMD" | grep -qE 'curl.+\|\s*(bash|sh|zsh)|wget.+\|\s*(bash|sh|zsh)' && \
  block "Blocked: pipe-to-shell pattern (curl|wget piped to shell)"

# 3. Sensitive directory deletion
echo "$CMD" | grep -qE 'rm\s+-[a-z]*rf?\s+(/|~/|/Users/[^/]+/?$|~/?$|\$HOME/?$)' && \
  block "Blocked: rm -rf on root or home directory"
echo "$CMD" | grep -qP 'rm\s+-[a-z]*rf?\s+.*(/\.ssh|/\.gnupg|/\.claude)(\s|$)' 2>/dev/null && \
  block "Blocked: rm -rf on sensitive dot-directory"

# 4. World-writable permissions
echo "$CMD" | grep -qE 'chmod\s+(777|a\+rwx|o\+w)' && \
  block "Blocked: world-writable chmod"

# 5. Credential exfiltration via network
echo "$CMD" | grep -qiE '(curl|wget|nc|netcat).*(API_KEY|TOKEN|PASSWORD|SECRET|CREDENTIAL)' && \
  block "Blocked: possible credential exfiltration via network tool"

# Allow
exit 0
```

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

**Ask the user:** "Install Socket CLI (npm supply chain scanner) and pip-audit (Python CVE scanner)? (yes/no)"

If approved:
```bash
# Socket CLI for npm
npm install -g @socket/cli 2>/dev/null && echo "Socket CLI installed" || echo "Socket CLI install failed (npm not found?)"

# pip-audit via pipx (isolated, no conflict with system Python)
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
# npm
[ -f package-lock.json ] && socket npm:report . 2>/dev/null | head -30
# Python
[ -f requirements.txt ] && pip-audit -r requirements.txt 2>/dev/null | head -30
```

---

## Phase 4: File-Level Malware Scanning (APPROVAL REQUIRED)

**Explain first:** ClamAV scans downloaded files and newly written files for known malware
signatures. The PostToolUse hook triggers a scan after curl/wget/download commands.

**Ask the user:** "Install ClamAV and set up automatic file scanning? (yes/no)"

If approved:
```bash
brew install clamav 2>/dev/null && \
  cp /opt/homebrew/etc/clamav/freshclam.conf.sample /opt/homebrew/etc/clamav/freshclam.conf && \
  freshclam && echo "ClamAV ready"
```

Write `~/.claude/hooks/security-scan.sh`:
```bash
#!/usr/bin/env bash
# Claude Code PostToolUse malware scan hook
set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Only scan after download commands
echo "$CMD" | grep -qE '(curl|wget|pip install|npm install|brew install)' || exit 0

# Scan Downloads folder and /tmp
command -v clamscan &>/dev/null || exit 0
clamscan --quiet --recursive ~/Downloads /tmp 2>/dev/null && echo "[security-scan] Clean" || \
  echo "[security-scan] WARNING: ClamAV found suspicious file"

exit 0
```

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

Ask: "Scan session transcripts for exposed credentials and report findings? (yes/no)"

If approved, scan `~/.claude/sessions/` for credential patterns:
```bash
grep -rl --include="*.jsonl" -E "(PASSWORD|SECRET|API_KEY|TOKEN)\s*[:=]\s*\S{8,}" \
  ~/.claude/sessions/ 2>/dev/null | head -10
```
Report findings. Do NOT auto-delete — let the user decide.

**5b. Session cleanup hook**

Ask: "Create a session cleanup script that kills zombie processes and prunes old shell snapshots? (yes/no)"

If approved, write `~/.claude/hooks/session-cleanup.sh`:
```bash
#!/usr/bin/env bash
# Claude Code session cleanup
# Kills zombie Claude processes (0% CPU, >2h) and prunes old shell snapshots

# Kill zombie claude processes
ps aux | awk '/claude/ && $3 == "0.0" {
  cmd = "ps -o etime= -p " $2
  cmd | getline etime
  close(cmd)
  split(etime, t, ":")
  if (length(t) >= 3 || (length(t) == 2 && t[1]+0 >= 120)) {
    print "Killing zombie Claude PID " $2 " (elapsed: " etime ")"
    system("kill " $2)
  }
}'

# Prune shell snapshots older than 7 days
find ~/.claude/shell-snapshots/ -type f -mtime +7 -delete 2>/dev/null
REMAINING=$(ls ~/.claude/shell-snapshots/ 2>/dev/null | wc -l | tr -d ' ')
echo "[session-cleanup] Shell snapshots remaining: $REMAINING"

# Session count
SESSIONS=$(ls ~/.claude/sessions/ 2>/dev/null | wc -l | tr -d ' ')
SIZE=$(du -sh ~/.claude/sessions/ 2>/dev/null | cut -f1)
echo "[session-cleanup] Sessions: $SESSIONS, Storage: $SIZE"
```

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

## File Inventory

| File | Purpose |
|------|---------|
| ~/.claude/hooks/security-precheck.sh | PreToolUse execution guard |
| ~/.claude/hooks/security-scan.sh | PostToolUse malware scan |
| ~/.claude/hooks/session-cleanup.sh | Session and zombie cleanup |

## Maintenance Schedule

| Task | Frequency | Method |
|------|-----------|--------|
| ClamAV signature update | Daily | freshclam (auto via launchd) |
| Shell snapshot prune | Per session | session-cleanup.sh hook |
| Transcript credential scan | Quarterly | Manual run of Phase 5a |
| MCP server review | When adding new server | Run Phase 6 |
| Full re-audit | Quarterly | Re-run /security-review |

## Checklist: Adding a New MCP Server

- [ ] Is the source known and trusted?
- [ ] Is the version pinned?
- [ ] Does it need secrets? → Store in keychain, not env block
- [ ] Is transport stdio or HTTP? → HTTP requires auth review
- [ ] Run Phase 6 MCP audit after adding
```

---

## Final Verification

After all selected phases, run:
```bash
# Confirm hooks exist and are executable
ls -la ~/.claude/hooks/*.sh 2>/dev/null || echo "No hooks installed"

# Confirm hooks are wired in settings
python3 -c "
import json
d = json.load(open('/Users/' + __import__('os').getenv('USER') + '/.claude/settings.json'))
hooks = d.get('hooks', {})
print('PreToolUse:', 'configured' if 'PreToolUse' in hooks else 'MISSING')
print('PostToolUse:', 'configured' if 'PostToolUse' in hooks else 'MISSING')
"
```

Print a final summary: which phases ran, which were skipped, top 3 remaining risks to address.
