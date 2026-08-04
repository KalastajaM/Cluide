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
