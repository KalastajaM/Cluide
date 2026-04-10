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
