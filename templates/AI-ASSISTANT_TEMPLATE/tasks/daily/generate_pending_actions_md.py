#!/usr/bin/env python3
"""
generate_pending_actions_md.py
Converts tasks/daily/pending_actions.json → Actions/PENDING_ACTIONS.md

Replaces Claude's manual Step 6 (markdown generation) — runs as a Python
subprocess, consuming zero Claude tokens for this deterministic transformation.

Usage:
    python3 generate_pending_actions_md.py
    python3 generate_pending_actions_md.py --json /path/to/pending_actions.json --output /path/to/PENDING_ACTIONS.md

Paths default to siblings of this script's location:
    <AI-Assistant>/tasks/daily/pending_actions.json
    <AI-Assistant>/Actions/PENDING_ACTIONS.md

The time zone comes from the TIMEZONE row of tasks/daily/CONFIG.md (UTC if unset).
"""

import json
import sys
from pathlib import Path
from datetime import date, datetime, timezone

# ─── Path resolution ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent   # tasks/daily/
AI_ROOT    = SCRIPT_DIR.parent.parent          # AI-Assistant/
CONFIG_MD  = SCRIPT_DIR / "CONFIG.md"          # holds the TIMEZONE row shared by all four scripts

# ─── Time zone (one value, read from CONFIG.md) ───────────────────────────────
def load_timezone():
    """Zone named by the TIMEZONE row of CONFIG.md; UTC if the row is unset or unknown.
    zoneinfo applies daylight saving time per date."""
    name = ""
    try:
        for line in CONFIG_MD.read_text(encoding="utf-8").splitlines():
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0] == "TIMEZONE":
                name = cells[1]
                break
    except OSError:
        pass
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        print(f"Note: TIMEZONE in {CONFIG_MD.name} is unset or unknown ({name or 'missing'}); using UTC.")
        return timezone.utc

USER_TZ = load_timezone()

def parse_args():
    args = {
        "json":   str(SCRIPT_DIR / "pending_actions.json"),
        "output": str(AI_ROOT / "Actions" / "PENDING_ACTIONS.md"),
    }
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("--json", "-j") and i + 1 < len(sys.argv):
            args["json"] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] in ("--output", "-o") and i + 1 < len(sys.argv):
            args["output"] = sys.argv[i + 1]; i += 2
        else:
            i += 1
    return args

# ─── Date helpers (local timezone) ───────────────────────────────────────────

def today_local():
    """Return today's date in the user's configured timezone."""
    return datetime.now(USER_TZ).date()

def parse_date(s):
    """Parse ISO date string (YYYY-MM-DD or ISO 8601) → date or None."""
    if not s:
        return None
    try:
        return date.fromisoformat(str(s)[:10])
    except (ValueError, TypeError):
        return None

def deadline_display(deadline_str, today):
    d = parse_date(deadline_str)
    if d is None:
        return "—"
    if d < today:
        return f"{d.isoformat()} 🔴"
    if d == today:
        return f"{d.isoformat()} ⚠️"
    return d.isoformat()

def deadline_sort_key(pa, today):
    """Sort: overdue/today → no deadline → future ascending."""
    d = parse_date(pa.get("deadline"))
    if d is None:
        return (1, date(9999, 12, 31))
    if d <= today:
        return (0, d)   # overdue or due today: earliest first
    return (2, d)       # future: ascending

# ─── PA classification ────────────────────────────────────────────────────────

PRIORITY_ORDER = {"URGENT": 0, "SOON": 1, "LOW": 2}

def pa_priority(pa):
    """URGENT / SOON / LOW; a missing or unrecognised priority is shown as LOW."""
    p = str(pa.get("priority") or "").strip().upper()
    return p if p in PRIORITY_ORDER else "LOW"

def priority_rank(pa):
    return PRIORITY_ORDER[pa_priority(pa)]

def cell(text):
    """Make text safe for one Markdown table cell."""
    return str(text or "").replace("|", "\\|").replace("\n", " ")

def is_portal(pa):
    if pa.get("sub_status") == "PORTAL_PENDING":
        return True
    rc = pa.get("resolution_check") or {}
    return rc.get("type") == "portal"

# ─── Formatting ───────────────────────────────────────────────────────────────

def truncate(text, max_len=350):
    if not text:
        return ""
    text = str(text).replace("\n", " ").strip()
    return text if len(text) <= max_len else text[:max_len - 1] + "…"

def format_pa_full(pa, today):
    """Full PA block for display in its primary section."""
    pid      = pa.get("id", "")
    title    = pa.get("title", "")
    priority = pa_priority(pa)
    source   = pa.get("source", "")
    sub      = pa.get("sub_status") or ""
    deadline = pa.get("deadline")
    action   = pa.get("action", "")
    draft    = pa.get("draft")
    draft_ch = pa.get("draft_channel", "")

    # Priority badge
    badge = priority
    if is_portal(pa):
        badge += " 🔑"
    elif sub == "WAITING_OTHER":
        badge += " 🔄"

    dl_str = deadline_display(deadline, today)

    lines = [
        f"**{pid}** — {title}",
        f"Priority: {badge} | Deadline: {dl_str} | Source: {source}",
    ]
    if action:
        lines.append(truncate(action, 400))
    if draft:
        channel = draft_ch.upper() if draft_ch else "DRAFT"
        lines.append(f"**{channel} draft ready** — see ACTIONS.md for full text")
    lines.append("")
    return "\n".join(lines)

def format_pa_xref(pa):
    """One-line cross-reference for PAs already shown in 🔑 section."""
    return f"**{pa['id']}** (see above — 🔑 section)\n"

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    args   = parse_args()
    today  = today_local()

    with open(args["json"], encoding="utf-8") as f:
        data = json.load(f)

    next_id     = data.get("next_id", "PA-????")
    open_pas    = data.get("open", [])
    snoozed     = data.get("snoozed", [])
    resolved    = data.get("resolved_last_30_days", [])

    # ── Classify open PAs ────────────────────────────────────────────────────
    portal_pas  = [p for p in open_pas if is_portal(p)]
    other_pas   = [p for p in open_pas if not is_portal(p)]

    def group(priority):
        return sorted(
            [p for p in other_pas if pa_priority(p) == priority],
            key=lambda p: deadline_sort_key(p, today)
        )

    urgent_pas = group("URGENT")
    soon_pas   = group("SOON")
    low_pas    = group("LOW")

    # Portal PAs also appear as cross-refs in their priority section
    portal_by_priority = {
        "URGENT": sorted([p for p in portal_pas if pa_priority(p) == "URGENT"],
                         key=lambda p: deadline_sort_key(p, today)),
        "SOON":   sorted([p for p in portal_pas if pa_priority(p) == "SOON"],
                         key=lambda p: deadline_sort_key(p, today)),
        "LOW":    sorted([p for p in portal_pas if pa_priority(p) == "LOW"],
                         key=lambda p: deadline_sort_key(p, today)),
    }

    # ── Build output ─────────────────────────────────────────────────────────
    out = []

    out.append("# Pending Actions [GENERATED VIEW]")
    out.append("> Source of truth is pending_actions.json. Do not edit — regenerated each run.")
    out.append("> To resolve: tell the assistant \"mark PA-NNNN as done\".")
    out.append("")
    out.append("## Action Counter")
    out.append(f"**{len(open_pas)} open** (generated {today.isoformat()}) | Next ID: {next_id}")
    out.append("")

    # ── Summary table ─────────────────────────────────────────────────────────
    # All open PAs in priority order: URGENT → SOON → LOW; within group: overdue → today → no deadline → future ascending
    all_open_sorted = (
        sorted(portal_by_priority["URGENT"] + urgent_pas, key=lambda p: deadline_sort_key(p, today)) +
        sorted(portal_by_priority["SOON"]   + soon_pas,   key=lambda p: deadline_sort_key(p, today)) +
        sorted(portal_by_priority["LOW"]    + low_pas,    key=lambda p: deadline_sort_key(p, today))
    )
    if all_open_sorted:
        out.append("## Summary Table")
        out.append("")
        out.append("| ID | Priority | Deadline | Topic | Action |")
        out.append("|----|----------|----------|-------|--------|")
        for pa in all_open_sorted:
            pid      = pa.get("id", "")
            priority = pa_priority(pa)
            if is_portal(pa):
                priority += " 🔑"
            elif pa.get("sub_status") == "WAITING_OTHER":
                priority += " 🔄"
            dl_str   = deadline_display(pa.get("deadline"), today)
            # Topic: strip leading [TAG] from title for brevity, keep rest
            title    = pa.get("title", "")
            action   = str(pa.get("action") or "")
            # Truncate action to ~80 chars for table readability
            action_short = action if len(action) <= 80 else action[:77] + "…"
            out.append(f"| {cell(pid)} | {priority} | {dl_str} | {cell(title)} | {cell(action_short)} |")
        out.append("")

    out.append("---")
    out.append("")

    # 🔑 Portal
    if portal_pas:
        sorted_portal = sorted(portal_pas, key=lambda p: (priority_rank(p), deadline_sort_key(p, today)))
        out.append("## 🔑 In Your Court (portal/action required)")
        out.append("")
        for pa in sorted_portal:
            out.append(format_pa_full(pa, today))
        out.append("---")
        out.append("")

    # 🔴 Urgent
    all_urgent = sorted(urgent_pas + portal_by_priority["URGENT"],
                        key=lambda p: deadline_sort_key(p, today))
    if all_urgent:
        out.append("## 🔴 Urgent / Time-Sensitive")
        out.append("")
        for pa in all_urgent:
            out.append(format_pa_xref(pa) if is_portal(pa) else format_pa_full(pa, today))
        out.append("---")
        out.append("")

    # 🟡 Soon
    all_soon = sorted(soon_pas + portal_by_priority["SOON"],
                      key=lambda p: deadline_sort_key(p, today))
    if all_soon:
        out.append("## 🟡 Needs Attention Soon")
        out.append("")
        for pa in all_soon:
            out.append(format_pa_xref(pa) if is_portal(pa) else format_pa_full(pa, today))
        out.append("---")
        out.append("")

    # 🔵 Low
    all_low = sorted(low_pas + portal_by_priority["LOW"],
                     key=lambda p: deadline_sort_key(p, today))
    if all_low:
        out.append("## 🔵 Low Priority")
        out.append("")
        for pa in all_low:
            out.append(format_pa_xref(pa) if is_portal(pa) else format_pa_full(pa, today))
        out.append("---")
        out.append("")

    # 💤 Snoozed
    if snoozed:
        out.append("## 💤 Snoozed")
        out.append("")
        for pa in snoozed:
            pid   = pa.get("id", "")
            title = pa.get("title", "")
            reminder = pa.get("reminder_date") or "?"
            out.append(f"**{pid}** — {title} (reminder: {reminder})\n")
        out.append("---")
        out.append("")

    # ✅ Resolved
    if resolved:
        out.append("## ✅ Recently Resolved (last 30 days)")
        out.append("")
        out.append("| Date | ID | Resolution |")
        out.append("|------|----|------------|")
        for r in resolved:
            rid        = r.get("id", "")
            rdate      = r.get("resolved_date", "")
            resolution = cell(r.get("resolution"))
            if len(resolution) > 160:
                resolution = resolution[:157] + "…"
            out.append(f"| {rdate} | {rid} | {resolution} |")
        out.append("")

    output = "\n".join(out)
    Path(args["output"]).parent.mkdir(parents=True, exist_ok=True)
    Path(args["output"]).write_text(output, encoding="utf-8")
    print(f"Written: {args['output']}")
    print(f"Stats: {len(open_pas)} open | {len(portal_pas)} portal | {len(resolved)} resolved (30d)")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
