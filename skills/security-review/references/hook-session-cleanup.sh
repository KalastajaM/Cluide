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
