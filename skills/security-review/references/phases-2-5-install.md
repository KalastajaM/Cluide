# Security Review — Phases 2 to 5 (the mutating phases)

> Loaded on demand by `SKILL.md`. Every phase here **installs software, writes hook files, or
> modifies `~/.claude/settings.json`**, so each one is gated: explain first, ask with
> `AskUserQuestion` buttons, and act only on an explicit yes. A user who declines all four still
> gets a complete audit — Phases 0, 1, 6 and 7 cover it.
>
> Phase numbers are stable and are cited from `12_SECURITY.md`. Do not renumber them.
>
> `$SKILL_DIR` and `$PROJECT` are set in `SKILL.md` § Setup. **Always write
> `"$SKILL_DIR/references/…"` rather than a bare `references/…`** — Phase 1f leaves the shell in
> `$PROJECT`, where a relative path silently resolves to the wrong place or to nothing.

---

## Phase 2: PreToolUse Hook — Execution Guard (APPROVAL REQUIRED)

**Explain first:** This hook intercepts every Bash command Claude tries to run and blocks
dangerous patterns before they execute. It prevents: pipe-to-shell installs, credential
exfiltration, dangerous flag usage, recursive deletion of critical directories, and
world-writable permission changes (`chmod 777`-style).

Use `AskUserQuestion` with buttons: "Create `~/.claude/hooks/security-precheck.sh` and wire it into your Claude settings?"
> Buttons: `Yes` / `No`

If approved:

```bash
mkdir -p ~/.claude/hooks
cp "$SKILL_DIR/references/hook-security-precheck.sh" ~/.claude/hooks/security-precheck.sh
chmod +x ~/.claude/hooks/security-precheck.sh
```

Then wire it into `~/.claude/settings.json`. **Do not paste a `hooks` block over the file** — the
user may already have hooks configured, and an overwrite silently drops them. Merge instead, and
show the result before writing:

```bash
python3 - <<'PY'
import json, os, pathlib
p = pathlib.Path.home() / ".claude" / "settings.json"
d = json.loads(p.read_text()) if p.exists() else {}
entry = {"matcher": "Bash", "hooks": [{"type": "command", "command": "~/.claude/hooks/security-precheck.sh"}]}
pre = d.setdefault("hooks", {}).setdefault("PreToolUse", [])
if not any(h.get("command") == entry["hooks"][0]["command"]
           for m in pre for h in m.get("hooks", [])):
    pre.append(entry)
print(json.dumps(d, indent=2))          # review this before writing
# p.write_text(json.dumps(d, indent=2))  # uncomment only after the user approves the diff
PY
```

Print the proposed JSON, get the user's yes, then re-run with the write line uncommented. The
membership test makes a re-run idempotent.

How it works: the hook receives the tool call as JSON on stdin (`.tool_input.command`);
exit 0 allows the command, exit 2 blocks it and feeds stderr back to Claude as the reason.

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
npm install -g socket 2>/dev/null && echo "Socket CLI installed" || echo "Socket CLI install failed (npm not found?)"
pipx install pip-audit 2>/dev/null && echo "pip-audit installed" || echo "pip-audit install failed (pipx not found?)"
```

Add the Socket check to the PreToolUse hook (append before the final `exit 0`). Skip this if
Phase 2 was declined — there is no hook to extend:
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

Run an initial scan on `$PROJECT`, in a subshell so the working directory survives:
```bash
( cd "$PROJECT"
  [ -f package-lock.json ] && socket npm:report . 2>/dev/null | head -30
  [ -f requirements.txt ] && pip-audit -r requirements.txt 2>/dev/null | head -30 )
```

---

## Phase 4: File-Level Malware Scanning (APPROVAL REQUIRED)

**Explain first:** ClamAV scans the Downloads folder and `/tmp` for known malware
signatures. The PostToolUse hook triggers the scan after curl/wget/download-type commands.

Use `AskUserQuestion` with buttons: "Install ClamAV and set up automatic file scanning?"
> Buttons: `Yes` / `No`

If approved (macOS; on Linux use the distribution's `clamav` package and its own config paths):
```bash
brew install clamav 2>/dev/null && \
  cp /opt/homebrew/etc/clamav/freshclam.conf.sample /opt/homebrew/etc/clamav/freshclam.conf && \
  freshclam && echo "ClamAV ready"
```

```bash
mkdir -p ~/.claude/hooks
cp "$SKILL_DIR/references/hook-security-scan.sh" ~/.claude/hooks/security-scan.sh
chmod +x ~/.claude/hooks/security-scan.sh
```

Wire `PostToolUse` in `~/.claude/settings.json` with the same merge-and-review procedure as
Phase 2 — change `PreToolUse` to `PostToolUse` and the command to `security-scan.sh`. Do not
overwrite the file.

**Limitation:** ClamAV uses signature-based detection — it misses novel or obfuscated malware.
It catches known threats, not zero-days.

---

## Phase 5: Credential Hygiene & Session Cleanup (APPROVAL REQUIRED)

### 5a. Credential scrub in transcripts

Use `AskUserQuestion` with buttons: "Scan session transcripts for exposed credentials and report findings?"
> Buttons: `Yes` / `No`

If approved, scan the session transcripts under `~/.claude/projects/` (one `.jsonl` file per session, grouped by project) for credential patterns:
```bash
grep -rl --include="*.jsonl" -E "(PASSWORD|SECRET|API_KEY|TOKEN)\s*[:=]\s*\S{8,}" \
  ~/.claude/projects/ 2>/dev/null | head -10
```
Report findings. Do NOT auto-delete — let the user decide.

Report matches only, and never persist one. A script that stores a credential pattern in order to scrub it is storing the credential, in plaintext, in a file that gets read, synced and backed up.

### 5b. Session cleanup script

Use `AskUserQuestion` with buttons: "Install a maintenance script that prunes shell snapshots older than 7 days and reports transcript storage?"
> Buttons: `Yes` / `No`

If approved:
```bash
mkdir -p ~/.claude/hooks
cp "$SKILL_DIR/references/hook-session-cleanup.sh" ~/.claude/hooks/session-cleanup.sh
chmod +x ~/.claude/hooks/session-cleanup.sh
```

**Never add process-killing to this script.** Read the header comment in
`references/hook-session-cleanup.sh` first: any pattern broad enough to match the Claude
app also matches every MCP server the app spawns, and an idle stdio MCP server sits at
0.0% CPU as its healthy state, so `%cpu` is not a liveness signal. An earlier version of
this script SIGTERM'd a user's entire MCP fleet on every scheduled run for weeks.

Despite the `hook-` filename this is **not** wired to a hook event — it is a standalone job
that does nothing until something runs it. If the user wants it scheduled, ask first, then
record the label and interval here so the installed copy and this reference cannot silently
diverge:

```bash
# macOS example — label com.user.claude-session-cleanup, daily at 09:00
launchctl bootout gui/$UID/com.user.claude-session-cleanup 2>/dev/null || true
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/com.user.claude-session-cleanup.plist
```

Every time this phase runs, check the installed copy against the reference and report drift
before offering to overwrite:
```bash
diff ~/.claude/hooks/session-cleanup.sh "$SKILL_DIR/references/hook-session-cleanup.sh" \
  && echo "session-cleanup: in sync" \
  || echo "session-cleanup: DRIFT — installed copy differs from this reference"
```
