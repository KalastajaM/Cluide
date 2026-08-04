#!/usr/bin/env python3
"""
generate_actions_html.py
Converts Actions/ACTIONS.md → Actions/ACTIONS.html with archiving.

Replaces Claude's manual Step 8 (HTML generation) entirely — runs as a
Python subprocess, consuming zero Claude tokens for HTML rendering.

Usage:
    python3 generate_actions_html.py
    python3 generate_actions_html.py --input /path/to/ACTIONS.md --output /path/to/ACTIONS.html

Paths default to siblings of this script's parent:
    <AI-Assistant>/Actions/ACTIONS.md  →  <AI-Assistant>/Actions/ACTIONS.html
"""

import re
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ============================================================
# USER CONFIG — edit these for your setup
# ============================================================
USER_TIMEZONE = "Europe/Helsinki"                # IANA timezone name — change to your own
USER_TIMEZONE_UTC_OFFSET_HOURS = 2               # Fallback offset if zoneinfo unavailable (standard time)
BRIEFING_TITLE = "Business Assistant Briefing"   # Title on the HTML briefing pages
# ============================================================

# ─── Path resolution ──────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent   # tasks/daily/
AI_ROOT     = SCRIPT_DIR.parent.parent           # AI-Assistant/
ACTIONS_DIR = AI_ROOT / "Actions"
HISTORY_DIR = ACTIONS_DIR / "History"

def parse_args():
    args = {
        "input":  str(ACTIONS_DIR / "ACTIONS.md"),
        "output": str(ACTIONS_DIR / "ACTIONS.html"),
    }
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] in ("--input", "-i") and i + 1 < len(sys.argv):
            args["input"] = sys.argv[i + 1]; i += 2
        elif sys.argv[i] in ("--output", "-o") and i + 1 < len(sys.argv):
            args["output"] = sys.argv[i + 1]; i += 2
        else:
            i += 1
    return args

# ─── CSS (matches ACTIONS.html embedded stylesheet) ───────────────────────────
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
  .conflict-badge  { background: #fee2e2; color: #991b1b; padding: 1px 6px; border-radius: 8px; font-size: 11px; font-weight: 600; margin-left: 6px; }
  .new-badge       { background: #dcfce7; color: #166534; padding: 1px 6px; border-radius: 8px; font-size: 11px; font-weight: 600; margin-left: 6px; }
  .resolved-badge  { background: #d1fae5; color: #065f46; padding: 1px 6px; border-radius: 8px; font-size: 11px; font-weight: 600; margin-left: 6px; }
  h3 { font-size: 14px; font-weight: 600; margin: 18px 0 6px; color: #1e293b; }
  h4 { font-size: 13px; font-weight: 600; margin: 14px 0 4px; color: #374151; }"""

# ─── Emoji → CSS class ────────────────────────────────────────────────────────
# Order matters: check longer multi-codepoint emoji first
EMOJI_CLASSES = [
    ("🗂️", "decisions"),
    ("⏳",  "summary"),
    ("🔴",  "urgent"),
    ("🔑",  "portal"),
    ("🟡",  "soon"),
    ("📋",  "briefs"),
    ("📅",  "meeting"),
    ("💬",  "teams"),
    ("💡",  "suggest"),
    ("📝",  "drafts"),
    ("🔄",  "waiting"),
    ("✅",  "resolved"),
    ("📊",  "profile"),
    ("🔧",  "improvements"),
    ("❓",  "questions"),
]

def get_h2_class(heading_text: str) -> str:
    for emoji, cls in EMOJI_CLASSES:
        if heading_text.startswith(emoji):
            return cls
    return ""

# ─── HTML escaping ────────────────────────────────────────────────────────────
def html_escape(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text

# ─── Inline markdown rendering ────────────────────────────────────────────────
# Badge replacements run on already-escaped text (emoji survive html_escape).
#
# Priority labels in ACTIONS.md are written as plain uppercase words (URGENT /
# SOON / LOW), optionally followed by annotation emoji (🔑 🔄 etc.) and
# optionally preceded by a colored-circle emoji (🔴 🟡 🔵).  All three forms
# must render as the same styled badge; trailing annotation emoji are preserved.
#
# Correct forms handled:
#   "SOON"       "SOON 🔑"    "🟡 SOON"    "🟡SOON"
#   "LOW"        "LOW 🔑"     "🔵 LOW"
#   "URGENT"     "🔴 URGENT"
_BADGE_PATTERNS = [
    # Leading emoji (if present) is consumed; trailing annotation emoji preserved.
    (r"(?:🔴\s*)?\bURGENT\b", '<span class="badge-urgent">URGENT</span>'),
    (r"(?:🟡\s*)?\bSOON\b",   '<span class="badge-soon">SOON</span>'),
    (r"(?:⚪\s*)?\bLOW\b",    '<span class="badge-low">LOW</span>'),
    # "(new this run)" annotation → green NEW badge
    (r"\(new this run\)", '<span class="new-badge">NEW</span>'),
]

def apply_inline(text: str) -> str:
    """Apply inline formatting to already-HTML-escaped text."""
    # Priority badges first
    for pattern, repl in _BADGE_PATTERNS:
        text = re.sub(pattern, repl, text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text* (single star, not adjacent to another star)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code: `text`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links: [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text

def process_inline(text: str) -> str:
    """Escape HTML then apply inline formatting."""
    return apply_inline(html_escape(text))

# ─── Table rendering ──────────────────────────────────────────────────────────
def _is_separator_row(cells):
    """True if this is a markdown table separator line (|---|---|)."""
    return all(re.match(r'^[-:]+$', c.strip()) for c in cells if c.strip())

def parse_table(lines: list) -> str:
    rows = []
    for line in lines:
        raw = line.strip()
        if raw.startswith('|'):
            raw = raw[1:]
        if raw.endswith('|'):
            raw = raw[:-1]
        cells = [c.strip() for c in raw.split('|')]
        rows.append(cells)

    if not rows:
        return ""

    out = ["<table>"]
    data_start = 0

    # Detect header + separator pattern
    if len(rows) >= 2 and _is_separator_row(rows[1]):
        out.append("  <tr>" + "".join(f"<th>{process_inline(c)}</th>" for c in rows[0]) + "</tr>")
        data_start = 2
    elif len(rows) >= 1 and _is_separator_row(rows[0]):
        # Separator with no header — skip
        data_start = 1

    for row in rows[data_start:]:
        if _is_separator_row(row):
            continue  # extra separator lines
        out.append("  <tr>" + "".join(f"<td>{process_inline(c)}</td>" for c in row) + "</tr>")

    out.append("</table>")
    return "\n".join(out)

# ─── Main converter ───────────────────────────────────────────────────────────
def convert_md_to_html(md_text: str) -> str:
    """Convert ACTIONS.md markdown to HTML body content."""
    lines = md_text.splitlines()
    out = []
    i = 0
    first_blockquote = True  # first blockquote → .meta paragraph

    # Accumulated paragraph lines
    para = []

    # Open list state
    in_ul = False
    in_ol = False

    def flush_para():
        nonlocal para
        if para:
            out.append(f"<p>{process_inline(' '.join(para))}</p>")
            para = []

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def close_ol():
        nonlocal in_ol
        if in_ol:
            out.append("</ol>")
            in_ol = False

    def flush_all():
        flush_para()
        close_ul()
        close_ol()

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        # ── Empty line ──
        if not s:
            flush_para()
            # Look ahead: if next non-empty line is a list item of the same type,
            # keep the list open (avoids restarting counter for numbered lists).
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            next_s = lines[j].strip() if j < len(lines) else ""
            next_is_ul = bool(re.match(r'^[-*]\s+', next_s))
            next_is_ol = bool(re.match(r'^\d+\.\s+', next_s))
            if not (in_ul and next_is_ul):
                close_ul()
            if not (in_ol and next_is_ol):
                close_ol()
            i += 1
            continue

        # ── Horizontal rule ──
        if s == "---":
            flush_all()
            out.append("<hr>")
            i += 1
            continue

        # ── ATX Headings ──
        m = re.match(r'^(#{1,4})\s+(.*)', s)
        if m:
            flush_all()
            level = len(m.group(1))
            heading = m.group(2).strip()
            if level == 1:
                out.append(f"<h1>{html_escape(heading)}</h1>")
            elif level == 2:
                cls = get_h2_class(heading)
                cls_attr = f' class="{cls}"' if cls else ""
                out.append(f"<h2{cls_attr}>{html_escape(heading)}</h2>")
            elif level == 3:
                out.append(f"<h3>{html_escape(heading)}</h3>")
            else:
                out.append(f"<h4>{html_escape(heading)}</h4>")
            i += 1
            continue

        # ── Blockquote ──
        if s.startswith("> "):
            flush_all()
            bq_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                bq_lines.append(lines[i].strip()[2:])
                i += 1
            content = "<br>\n".join(process_inline(l) for l in bq_lines)
            if first_blockquote:
                out.append(f'<p class="meta">{content}</p>')
                first_blockquote = False
            else:
                out.append(f"<blockquote>{content}</blockquote>")
            continue

        # ── Table ──
        if s.startswith("|"):
            flush_all()
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(parse_table(tbl))
            continue

        # ── Unordered list item ──
        ul_m = re.match(r'^[-*]\s+(.*)', s)
        if ul_m:
            flush_para()
            close_ol()
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"  <li>{process_inline(ul_m.group(1))}</li>")
            i += 1
            continue

        # ── Ordered list item ──
        ol_m = re.match(r'^\d+\.\s+(.*)', s)
        if ol_m:
            flush_para()
            close_ul()
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"  <li>{process_inline(ol_m.group(1))}</li>")
            i += 1
            continue

        # ── Regular paragraph text ──
        close_ul()
        close_ol()
        para.append(s)
        i += 1

    flush_all()
    return "\n".join(out)

# ─── Archiving ────────────────────────────────────────────────────────────────
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
    """Copy existing HTML to History/ before overwriting."""
    if not output_path.exists():
        return
    history_dir = output_path.parent / "History"
    history_dir.mkdir(parents=True, exist_ok=True)
    ts = _local_timestamp()
    archive_name = f"{output_path.stem}-{ts}{output_path.suffix}"
    shutil.copy2(output_path, history_dir / archive_name)
    print(f"Archived  → {history_dir / archive_name}")

# ─── Archive rotation ────────────────────────────────────────────────────────
HISTORY_KEEP = 14  # max archived files per prefix (e.g. ACTIONS-*.html)

def rotate_history(history_dir: Path, prefix: str, keep: int = HISTORY_KEEP):
    """Delete oldest archived files beyond the keep limit."""
    files = sorted(history_dir.glob(f"{prefix}-*.html"), key=lambda p: p.stat().st_mtime)
    for old in files[:-keep]:
        try:
            old.unlink()
        except OSError:
            pass  # ignore permission errors on read-only mounts

# ─── Title extraction ─────────────────────────────────────────────────────────
def extract_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return BRIEFING_TITLE

# ─── Entry point ─────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    input_path  = Path(args["input"])
    output_path = Path(args["output"])

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    md_text = input_path.read_text(encoding="utf-8")
    title   = extract_title(md_text)
    body    = convert_md_to_html(md_text)

    # Inject editor link after the first <h1>
    editor_link = '<p style="font-size:12px;color:#6b7280;margin-top:-4px;margin-bottom:4px;"><a href="../tasks/daily/ACTIONS_EDITOR.html">Actions Editor \u2192</a></p>'
    body = re.sub(r'(<h1>[^<]*</h1>)', r'\1\n' + editor_link, body, count=1)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_escape(title)}</title>
  <style>
{CSS}
  </style>
</head>
<body>
{body}
</body>
</html>
"""

    archive_existing(output_path)
    output_path.write_text(html, encoding="utf-8")
    print(f"Written   → {output_path}")

    # Rotate archive
    history_dir = output_path.parent / "History"
    if history_dir.exists():
        rotate_history(history_dir, output_path.stem)


if __name__ == "__main__":
    main()
