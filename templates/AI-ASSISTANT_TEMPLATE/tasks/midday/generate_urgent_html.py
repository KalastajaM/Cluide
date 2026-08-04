#!/usr/bin/env python3
"""
generate_urgent_html.py
Generates Actions/ACTIONS_URGENT.html from UrgentScan-Task/urgent_data.json.

Replaces Claude's manual Step 5B — runs as a Python subprocess, consuming
zero Claude tokens for HTML rendering.

Usage (from any directory):
    python3 /path/to/UrgentScan-Task/generate_urgent_html.py
    python3 generate_urgent_html.py --data /path/to/urgent_data.json
    python3 generate_urgent_html.py --output /path/to/ACTIONS_URGENT.html
"""

import json
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ============================================================
# USER CONFIG — edit these for your setup
# ============================================================
USER_TIMEZONE = "Europe/Helsinki"          # IANA timezone name — change to your own
USER_TIMEZONE_UTC_OFFSET_HOURS = 2         # Fallback offset if zoneinfo unavailable (standard time)
# ============================================================

# ─── Path resolution ──────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent   # UrgentScan-Task/
AI_ROOT     = SCRIPT_DIR.parent                  # AI-Assistant/
ACTIONS_DIR = AI_ROOT / "Actions"
HISTORY_DIR = ACTIONS_DIR / "History"

DEFAULT_DATA_PATH   = SCRIPT_DIR / "urgent_data.json"
DEFAULT_OUTPUT_PATH = ACTIONS_DIR / "ACTIONS_URGENT.html"


def parse_args():
    args = {
        "data":   str(DEFAULT_DATA_PATH),
        "output": str(DEFAULT_OUTPUT_PATH),
    }
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("--data", "-d") and i + 1 < len(sys.argv):
            args["data"] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] in ("--output", "-o") and i + 1 < len(sys.argv):
            args["output"] = sys.argv[i + 1]; i += 2
        else:
            i += 1
    return args


# ─── CSS (shared stylesheet, matches generate_actions_html.py) ────────────────
CSS = """\
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; color: #1a1a1a; max-width: 800px; margin: 40px auto; padding: 0 24px; background: #fff; }
  h1 { font-size: 22px; font-weight: 700; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; margin-bottom: 6px; }
  .meta { color: #6b7280; font-size: 12px; margin-bottom: 32px; }
  h2 { font-size: 16px; font-weight: 600; margin-top: 32px; margin-bottom: 10px; padding: 6px 10px; border-radius: 4px; }
  h2.urgent      { background: #fef2f2; color: #991b1b; }
  h2.portal      { background: #fef3c7; color: #92400e; }
  h2.soon        { background: #fffbeb; color: #92400e; }
  h2.briefs      { background: #fdf4ff; color: #6b21a8; }
  h2.meeting     { background: #eff6ff; color: #1e40af; }
  h2.teams       { background: #f0fdf4; color: #166534; }
  h2.suggest     { background: #f5f3ff; color: #5b21b6; }
  h2.drafts      { background: #fff7ed; color: #9a3412; }
  h2.waiting     { background: #f9fafb; color: #374151; }
  h2.resolved    { background: #f0fdf4; color: #166534; }
  h2.profile     { background: #f8fafc; color: #334155; }
  h2.decisions   { background: #fafafa; color: #1a1a1a; }
  h2.improvements{ background: #f0f9ff; color: #0c4a6e; }
  h2.questions   { background: #fefce8; color: #713f12; }
  h2.summary     { background: #f1f5f9; color: #0f172a; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
  th { background: #f1f5f9; text-align: left; padding: 8px 10px; font-weight: 600; border-bottom: 1px solid #e2e8f0; }
  td { padding: 7px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  .badge-urgent { background: #fee2e2; color: #991b1b; padding: 2px 7px; border-radius: 12px; font-size: 11px; font-weight: 600; }
  .badge-soon   { background: #fef3c7; color: #92400e; padding: 2px 7px; border-radius: 12px; font-size: 11px; font-weight: 600; }
  .badge-low    { background: #f1f5f9; color: #475569; padding: 2px 7px; border-radius: 12px; font-size: 11px; font-weight: 600; }
  blockquote { background: #f8fafc; border-left: 3px solid #cbd5e1; margin: 0 0 12px; padding: 10px 14px; border-radius: 0 4px 4px 0; font-style: normal; color: #374151; }
  code { background: #f1f5f9; padding: 1px 5px; border-radius: 3px; font-size: 12px; }
  strong { font-weight: 600; }
  p { margin: 6px 0 10px; }
  ul, ol { margin: 6px 0 10px; padding-left: 20px; }
  li { margin-bottom: 3px; }
  hr { border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }
  .section-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #9ca3af; margin-bottom: 4px; }
  .clear-box { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 20px 24px; margin-top: 24px; color: #166534; font-size: 15px; }
  .clear-box .icon { font-size: 24px; margin-right: 8px; }
  .note-box { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 16px; margin-top: 16px; font-size: 13px; color: #475569; }
  .urgent-card { background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px; padding: 14px 18px; margin: 12px 0; }
  .urgent-card .card-title { font-size: 15px; font-weight: 600; color: #991b1b; margin-bottom: 6px; }
  .urgent-card .card-meta { font-size: 12px; color: #6b7280; margin-bottom: 8px; }
  .urgent-card .card-action { margin-top: 8px; font-weight: 600; }
  .draft-block { background: #fff; border: 1px solid #e5e7eb; border-radius: 4px; padding: 10px 14px; margin-top: 10px; font-size: 13px; white-space: pre-wrap; }
  .draft-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #9ca3af; margin-bottom: 4px; }
  .flag-card { background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 12px 16px; margin: 10px 0; font-size: 13px; }"""


# ─── HTML escaping ────────────────────────────────────────────────────────────
def h(text) -> str:
    if text is None:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


# ─── Archiving ────────────────────────────────────────────────────────────────
HISTORY_KEEP = 14  # max archived files per prefix

def _local_timestamp() -> str:
    """Return a YYYY-MM-DD_HHMM timestamp in the user's local timezone."""
    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo(USER_TIMEZONE)
        return datetime.now(tz).strftime("%Y-%m-%d_%H%M")
    except Exception:
        pass
    # Fallback: try bash/TZ (works on Unix with tzdata installed)
    try:
        ts = subprocess.check_output(
            ["bash", "-c", f'TZ={USER_TIMEZONE} date +"%Y-%m-%d_%H%M"'],
            text=True, stderr=subprocess.DEVNULL
        ).strip()
        if ts:
            return ts
    except Exception:
        pass
    # Final fallback: UTC + configured offset
    approx = datetime.now(timezone.utc) + timedelta(hours=USER_TIMEZONE_UTC_OFFSET_HOURS)
    return approx.strftime("%Y-%m-%d_%H%M")

def archive_existing(output_path: Path):
    """Copy existing ACTIONS_URGENT.html to History/ before overwriting."""
    if not output_path.exists():
        return
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    ts = _local_timestamp()
    archive_name = f"ACTIONS_URGENT-{ts}.html"
    shutil.copy2(output_path, HISTORY_DIR / archive_name)
    print(f"Archived  \u2192 {HISTORY_DIR / archive_name}")

def rotate_history(prefix: str, keep: int = HISTORY_KEEP):
    """Delete oldest archived files beyond the keep limit."""
    files = sorted(HISTORY_DIR.glob(f"{prefix}-*.html"), key=lambda p: p.stat().st_mtime)
    for old in files[:-keep]:
        old.unlink()


# ─── HTML body builder ────────────────────────────────────────────────────────
def build_body(data: dict) -> str:
    scan_time  = data.get("scan_time_hel", "")
    urgent     = data.get("urgent_items", [])
    new_flags  = data.get("new_flags", [])
    notable    = data.get("notable_non_urgent", [])
    emails_n   = data.get("emails_scanned", 0)
    teams_n    = data.get("teams_scanned", 0)
    flags_note = data.get("flags_note", "")
    last_utc   = data.get("last_scan_utc", "")
    start_utc  = data.get("scan_start_utc", "")
    n_urgent   = len(urgent)

    parts = []

    # ── Header ──
    parts.append(f'<h1>Urgent scan \u2014 {h(scan_time)}</h1>')
    item_word = "item" if n_urgent == 1 else "items"
    parts.append(
        f'<p class="meta">{n_urgent} new urgent {item_word}'
        f' &nbsp;|&nbsp; <a href="ACTIONS.html">&#8592; View full morning briefing</a>'
        f' &nbsp;|&nbsp; <a href="../tasks/daily/ACTIONS_EDITOR.html">Actions Editor &#8594;</a></p>'
    )

    # ── Main content ──
    if n_urgent == 0 and not new_flags:
        parts.append('<div class="clear-box">')
        parts.append('  <span class="icon">&#x2705;</span> Nothing urgent since morning briefing. Next full briefing tomorrow at 07:00.')
        parts.append('</div>')
    else:
        # Urgent item cards
        if urgent:
            parts.append(f'<h2 class="urgent">&#x1F534; Urgent \u2014 Act Today ({n_urgent})</h2>')
            for item in urgent:
                pa_id   = h(item.get("pa_id", ""))
                title   = h(item.get("title", ""))
                context = h(item.get("context", ""))
                action  = h(item.get("action", ""))
                draft   = item.get("draft")
                channel = item.get("draft_channel") or ""

                parts.append('<div class="urgent-card">')
                parts.append(f'  <div class="card-title">{pa_id} &middot; {title}</div>')
                if context:
                    parts.append(f'  <p>{context}</p>')
                if action:
                    parts.append(f'  <div class="card-action">&#x27A1; {action}</div>')
                if draft:
                    label = channel.capitalize() if channel else "Draft"
                    parts.append(f'  <div class="draft-label">{h(label)}</div>')
                    parts.append(f'  <div class="draft-block">{h(draft)}</div>')
                parts.append('</div>')

        # New flagged items
        if new_flags:
            parts.append(f'<h2 class="portal">&#x1F3F3;&#xFE0F; New Flagged Items ({len(new_flags)})</h2>')
            for flag in new_flags:
                subject  = h(flag.get("subject", ""))
                sender   = h(flag.get("sender", ""))
                due_date = h(flag.get("due_date", ""))
                context  = h(flag.get("context", ""))

                parts.append('<div class="flag-card">')
                parts.append(f'  <strong>{subject}</strong>')
                meta_bits = []
                if sender:
                    meta_bits.append(f"From: {sender}")
                if due_date:
                    meta_bits.append(f"Due: {due_date}")
                if meta_bits:
                    parts.append(f'  <div class="card-meta">{" &nbsp;|&nbsp; ".join(meta_bits)}</div>')
                if context:
                    parts.append(f'  <p>{context}</p>')
                parts.append('</div>')

    # ── Note box — always shown ──
    parts.append('<div class="note-box">')
    parts.append(f'  <strong>Window scanned:</strong> {h(last_utc)} &rarr; {h(start_utc)}<br>')

    stats_line = (
        f'  <strong>Emails reviewed:</strong> {emails_n}'
        f' &nbsp;|&nbsp; <strong>Teams messages reviewed:</strong> {teams_n}'
    )
    if flags_note:
        stats_line += f' &nbsp;|&nbsp; <strong>Flagged items:</strong> {h(flags_note)}'
    parts.append(stats_line + '<br>')

    if notable:
        parts.append('  <br>')
        parts.append('  <strong>Notable but non-urgent:</strong>')
        parts.append('  <ul style="margin-top:6px;">')
        for item in notable:
            subject = h(item.get("subject", ""))
            sender  = h(item.get("sender", ""))
            note    = h(item.get("note", ""))
            sender_bit = f" ({sender})" if sender else ""
            parts.append(f'    <li><strong>{subject}</strong>{sender_bit} &mdash; {note}</li>')
        parts.append('  </ul>')

    parts.append('</div>')

    return "\n".join(parts)


# ─── Entry point ─────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    data_path   = Path(args["data"])
    output_path = Path(args["output"])

    if not data_path.exists():
        print(f"ERROR: Data file not found: {data_path}", file=sys.stderr)
        sys.exit(1)

    data      = json.loads(data_path.read_text(encoding="utf-8"))
    scan_time = data.get("scan_time_hel", "")
    body      = build_body(data)

    archive_existing(output_path)
    rotate_history("ACTIONS_URGENT")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Urgent Scan \u2014 {h(scan_time)}</title>
<style>
{CSS}
</style>
</head>
<body>

{body}

</body>
</html>"""

    output_path.write_text(html, encoding="utf-8")
    print(f"Generated \u2192 {output_path}")


if __name__ == "__main__":
    main()
