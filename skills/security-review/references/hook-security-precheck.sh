#!/usr/bin/env bash
# Claude Code PreToolUse security gate
# Blocks dangerous Bash commands before execution
# Input: JSON on stdin with .tool_input.command
# Output: reason on stderr + exit 2 to block; exit 0 to allow
# (Exit 2 is the only blocking exit code — other non-zero exits do NOT block.)

set -euo pipefail

INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

block() {
  echo "$1" >&2
  exit 2
}

# 1. Dangerous flags
# Note: the short form `git commit -n` (= --no-verify) is not caught — too many false positives.
echo "$CMD" | grep -qE -- '--dangerously-skip-permissions|git[[:space:]].*--no-verify|git[[:space:]]+push.*([[:space:]]--force|[[:space:]]-f([[:space:]]|$))' && \
  block "Blocked: dangerous flag detected"

# 2. Pipe-to-shell (supply chain attack vector)
echo "$CMD" | grep -qE 'curl.+\|\s*(bash|sh|zsh)|wget.+\|\s*(bash|sh|zsh)' && \
  block "Blocked: pipe-to-shell pattern (curl|wget piped to shell)"

# 3. Sensitive directory deletion
# Blocks recursive rm on: / and /*, a home directory or one of its direct children (~, ~/Documents,
# $HOME, /Users/x, /home/x/y), and a system directory or its direct child (/etc, /usr/local).
# Deeper paths (/tmp/x, ./build, /Users/x/projects/app/dist) are allowed. Quotes are stripped first.
# Portable ERE (no grep -P: BSD/macOS grep lacks it, and the check would silently never fire)
RM_CMD=$(echo "$CMD" | tr -d "\"'")
RM_REC='(^|[^[:alnum:]_])rm[[:space:]]+(-[^[:space:]]+[[:space:]]+)*-([a-zA-Z]*[rR][a-zA-Z]*|-recursive)([[:space:]]+[^[:space:];&|]+)*[[:space:]]+'
RM_SYS='(bin|boot|dev|etc|lib|lib32|lib64|opt|proc|root|run|sbin|srv|sys|usr|var|home|Users|Applications|Library|System|Volumes|private)'
echo "$RM_CMD" | grep -qE "${RM_REC}"'(/\*?|~(/[^[:space:]/;&|]+)?/?|(\$HOME|\$\{HOME\})(/[^[:space:]/;&|]+)?/?|/(Users|home)/[^[:space:]/;&|]+(/[^[:space:]/;&|]+)?/?|/'"${RM_SYS}"'(/[^[:space:]/;&|]+)?/?)([[:space:]]|$)' && \
  block "Blocked: rm -rf on root, home or system directory"
echo "$RM_CMD" | grep -qE "${RM_REC}"'([^[:space:];&|]*/)\.(ssh|gnupg|claude)/?([[:space:]]|$)' && \
  block "Blocked: rm -rf on sensitive dot-directory"

# 4. World-writable permissions
echo "$CMD" | grep -qE 'chmod[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*(0?777|a\+rwx|o\+w)' && \
  block "Blocked: world-writable chmod"

# 5. Credential exfiltration via network
echo "$CMD" | grep -qiE '(curl|wget|nc|netcat).*(API_KEY|TOKEN|PASSWORD|SECRET|CREDENTIAL)' && \
  block "Blocked: possible credential exfiltration via network tool"

# Allow
exit 0
