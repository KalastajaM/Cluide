#!/usr/bin/env bash
# Claude Code session cleanup — prunes old shell snapshots and reports storage.
#
# This script deliberately does NOT kill processes.
#
# An earlier version tried to reap "zombie" Claude processes by matching command
# lines against the Claude app bundle and treating low instantaneous %cpu as a
# liveness signal. Both halves are unsound:
#
#   * MCP servers are spawned by the desktop app from inside its own bundle, so
#     any pattern broad enough to match the app also matches every MCP server.
#   * An idle stdio MCP server blocked on read sits at 0.0% CPU. That is its
#     healthy state, not a stuck one, so no ps-based signal separates the two.
#
# The observed result was every MCP server being SIGTERM'd on each scheduled run.
# If you genuinely need to reap orphaned CLI processes, match the claude
# executable path specifically, exclude anything under the app bundle, use
# accumulated CPU time rather than %cpu, and confirm the process is actually
# orphaned first — then keep that in a separate, explicitly-invoked script.
#
# It also deliberately does NOT rewrite transcripts. Scrubbing credentials by
# regex requires storing the pattern, and a credential-shaped pattern is the
# credential — in plaintext, in a file that is read, synced and backed up.
# Report matches instead (Phase 5a) and let a human decide.

set -euo pipefail

LOG_FILE="$HOME/.claude/logs/session-cleanup.log"
mkdir -p "$(dirname "$LOG_FILE")"
exec >> "$LOG_FILE" 2>&1

echo "=== session-cleanup $(date '+%Y-%m-%d %H:%M:%S') ==="

# 1. Prune shell snapshots older than 7 days
SNAPSHOT_DIR="$HOME/.claude/shell-snapshots"
PRUNED=0
if [[ -d "$SNAPSHOT_DIR" ]]; then
  while IFS= read -r f; do
    [[ -n "$f" ]] || continue
    rm -f "$f" && PRUNED=$((PRUNED + 1))
  done < <(find "$SNAPSHOT_DIR" -type f -mtime +7)
fi
echo "Shell snapshots pruned: $PRUNED"

# 2. Report transcript count and storage (read-only)
PROJECTS_DIR="$HOME/.claude/projects"
SESSIONS=$(find "$PROJECTS_DIR" -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ')
STORAGE=$(du -sh "$PROJECTS_DIR" 2>/dev/null | cut -f1)
SNAP_STORAGE=$(du -sh "$SNAPSHOT_DIR" 2>/dev/null | cut -f1)
echo "Sessions: $SESSIONS transcripts | Projects storage: ${STORAGE:-n/a} | Snapshots: ${SNAP_STORAGE:-0B}"
echo "=== done ==="
