#!/usr/bin/env python3
"""
generate_weekplan_html.py — Renders the weekly plan HTML from a JSON data file.

Usage:
    python3 generate_weekplan_html.py --input plan.json --output weekplan.html

Requires Python 3.9+ (zoneinfo) and jinja2 (pip install jinja2). The time zone comes
from the TIMEZONE row of tasks/daily/CONFIG.md (UTC if unset); block times in the JSON
are local times in that zone, and the ICS export converts each one to UTC for its own date.

Input JSON schema:
{
  "monday_date": "YYYY-MM-DD",
  "week_label": "Week of 30 March 2026",
  "proposed_blocks": [
    {
      "day": "monday",           // monday|tuesday|wednesday|thursday|friday
      "date": "YYYY-MM-DD",     // local date of the block
      "start_time": "HH:MM",    // local 24h
      "end_time": "HH:MM",      // local 24h
      "duration_min": 90,
      "title": "Deep work: quarterly analysis",
      "description": "Work on ...",
      "type": "deep",           // deep|quick|prep|conditional
      "action_ids": ["PA-0013"] // optional
    }
  ],
  "existing_meetings": {
    "monday": [
      {"start_time": "09:00", "end_time": "10:00", "title": "Standup"}
    ],
    "tuesday": [], "wednesday": [], "thursday": [], "friday": []
  },
  "open_actions": [
    {"id": "PA-0013", "title": "Book vacation days", "priority": "SOON", "deadline": "2026-03-31"}
  ]
}
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from jinja2 import Environment

# ============================================================
# USER CONFIG — edit these for your setup
# (the time zone is not set here: it is the TIMEZONE row of CONFIG.md)
# ============================================================
USER_EMAIL_DOMAIN = "example.com"            # Domain used in ICS UIDs
BUSIEST_WEEKDAY = "friday"                   # Lowercase weekday your calendar is reliably packed on (shown faded); "" for none
# ============================================================

CONFIG_MD = Path(__file__).resolve().parent.parent / "daily" / "CONFIG.md"   # holds the TIMEZONE row shared by all four scripts


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


def to_utc_ics(date_str, time_str):
    """Local date + 'HH:MM' in USER_TZ -> ICS UTC stamp (YYYYMMDDTHHMMSSZ), DST-correct for that date.
    Returns None if the date or time cannot be parsed."""
    try:
        local = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M").replace(tzinfo=USER_TZ)
    except (TypeError, ValueError):
        return None
    return local.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Week Plan — {{ week_label }}</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; background: #f5f5f5; color: #222; padding: 24px; }
  h1 { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
  .subtitle { color: #666; margin-bottom: 24px; font-size: 12px; }

  /* Open actions table */
  .section-title { font-size: 14px; font-weight: 600; margin-bottom: 10px; color: #333; }
  table { width: 100%; border-collapse: collapse; margin-bottom: 28px; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
  th { background: #f0f0f0; text-align: left; padding: 8px 12px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #555; border-bottom: 1px solid #ddd; }
  td { padding: 7px 12px; border-bottom: 1px solid #eee; vertical-align: top; }
  tr:last-child td { border-bottom: none; }
  .badge { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 10px; font-weight: 600; }
  .badge-urgent { background: #fee2e2; color: #991b1b; }
  .badge-soon { background: #fef3c7; color: #92400e; }
  .badge-low  { background: #f3f4f6; color: #6b7280; }
  .badge-high { background: #fee2e2; color: #991b1b; }
  .badge-medium { background: #dbeafe; color: #1e40af; }
  .no-actions { color: #999; font-style: italic; padding: 8px 12px; }

  /* Calendar grid */
  .calendar { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
  .day-col { background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
  .day-col.busiest { opacity: 0.65; }
  .day-header { padding: 10px 12px; font-weight: 600; font-size: 12px; background: #374151; color: #fff; }
  .day-header.busiest { background: #9ca3af; }
  .day-body { padding: 8px; display: flex; flex-direction: column; gap: 6px; min-height: 120px; }
  .busiest-note { color: #9ca3af; font-style: italic; font-size: 11px; padding: 8px 4px; }

  /* Blocks */
  .block { border-radius: 5px; padding: 8px 10px; font-size: 12px; }
  .block-time { font-size: 10px; opacity: 0.75; margin-bottom: 2px; }
  .block-title { font-weight: 600; margin-bottom: 3px; }
  .block-desc { font-size: 11px; line-height: 1.4; opacity: 0.85; }
  .block-ids { font-size: 10px; margin-top: 4px; opacity: 0.7; }

  .block-meeting { background: #f3f4f6; border-left: 3px solid #d1d5db; }
  .block-deep { background: #dbeafe; border-left: 3px solid #3b82f6; }
  .block-quick { background: #d1fae5; border-left: 3px solid #10b981; }
  .block-prep { background: #fef3c7; border-left: 3px solid #f59e0b; }
  .block-conditional { background: #fff; border: 1.5px dashed #d1d5db; }

  /* ICS button */
  .ics-btn { display: inline-block; margin-top: 6px; padding: 3px 8px; font-size: 10px; border-radius: 4px; border: 1px solid #9ca3af; background: #fff; color: #374151; cursor: pointer; }
  .ics-btn:hover { background: #f9fafb; }

  /* Legend */
  .legend { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #555; }
  .legend-swatch { width: 12px; height: 12px; border-radius: 3px; }
  .sw-meeting { background: #e5e7eb; border-left: 3px solid #9ca3af; }
  .sw-deep { background: #dbeafe; border-left: 3px solid #3b82f6; }
  .sw-quick { background: #d1fae5; border-left: 3px solid #10b981; }
  .sw-prep { background: #fef3c7; border-left: 3px solid #f59e0b; }
  .sw-conditional { border: 1.5px dashed #d1d5db; background: #fff; }
</style>
</head>
<body>

<h1>📅 Week Plan</h1>
<div class="subtitle">{{ week_label }} &nbsp;·&nbsp; Generated {{ generated_at }} &nbsp;·&nbsp; Calendar events not created automatically — use Add to Outlook buttons.</div>

<!-- Open Actions Table -->
<div class="section-title">Open Actions</div>
{% if open_actions %}
<table>
  <tr><th>ID</th><th>Action</th><th>Priority</th><th>Deadline</th></tr>
  {% for a in open_actions %}
  <tr>
    <td style="white-space:nowrap; color:#6b7280;">{{ a.id }}</td>
    <td>{{ a.title }}</td>
    <td><span class="badge badge-{{ a.priority|lower|replace(' ','') }}">{{ a.priority }}</span></td>
    <td style="white-space:nowrap;">{{ a.deadline or '—' }}</td>
  </tr>
  {% endfor %}
</table>
{% else %}
<table><tr><td class="no-actions">No open actions.</td></tr></table>
{% endif %}

<!-- Legend -->
<div class="section-title">Proposed Schedule</div>
<div class="legend">
  <div class="legend-item"><div class="legend-swatch sw-meeting"></div>Existing meeting</div>
  <div class="legend-item"><div class="legend-swatch sw-deep"></div>Deep work</div>
  <div class="legend-item"><div class="legend-swatch sw-quick"></div>Quick actions</div>
  <div class="legend-item"><div class="legend-swatch sw-prep"></div>Meeting prep</div>
  <div class="legend-item"><div class="legend-swatch sw-conditional"></div>Conditional</div>
</div>

<!-- Calendar -->
<div class="calendar">
  {% for day in days %}
  <div class="day-col{% if day.busiest %} busiest{% endif %}">
    <div class="day-header{% if day.busiest %} busiest{% endif %}">
      {{ day.label }}<br><span style="font-weight:400; font-size:11px; opacity:0.8;">{{ day.date_fmt }}</span>
    </div>
    <div class="day-body">
      {% if day.busiest and not day.blocks %}
        <div class="busiest-note">No blocks scheduled — typically packed with recurring meetings.</div>
      {% else %}
        {% for block in day.blocks %}
        <div class="block block-{{ block.type }}">
          <div class="block-time">{{ block.start_time }}–{{ block.end_time }}{% if block.duration_min %} ({{ block.duration_min }} min){% endif %}</div>
          <div class="block-title">{{ block.title }}</div>
          {% if block.description %}<div class="block-desc">{{ block.description }}</div>{% endif %}
          {% if block.action_ids %}<div class="block-ids">{{ block.action_ids | join(', ') }}</div>{% endif %}
          {% if block.type != 'meeting' and block.dtstart_utc and block.dtend_utc %}
          <button class="ics-btn" onclick='downloadICS({{ block | tojson }})'>📅 Add to Outlook</button>
          {% endif %}
        </div>
        {% endfor %}
        {% if not day.blocks %}
        <div style="color:#bbb; font-style:italic; font-size:11px; padding:4px;">No blocks proposed.</div>
        {% endif %}
      {% endif %}
    </div>
  </div>
  {% endfor %}
</div>

<script>
var ICS_UID_DOMAIN  = {{ ics_uid_domain | tojson }};

// Escape text for an ICS TEXT value (RFC 5545): backslash, semicolon, comma, line breaks.
function icsText(s) {
  return String(s || '').replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
}

function downloadICS(block) {
  // block.dtstart_utc / dtend_utc are computed by the generator for this block's own date (DST-correct)
  var uid = 'weekplan-' + block.date + '-' + block.start_time.replace(':','') + '@' + ICS_UID_DOMAIN;
  var ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//WeekPlan//EN',
    'BEGIN:VEVENT',
    'UID:' + uid,
    'DTSTAMP:' + block.dtstart_utc,
    'DTSTART:' + block.dtstart_utc,
    'DTEND:' + block.dtend_utc,
    'SUMMARY:' + icsText(block.title),
    'DESCRIPTION:' + icsText(block.description),
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n');
  var blob = new Blob([ics], {type: 'text/calendar;charset=utf-8'});
  var a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = block.title.replace(/[^a-zA-Z0-9]/g, '_').substring(0,40) + '.ics';
  a.click();
}
</script>

</body>
</html>
"""

DAYS_ORDER = ["monday", "tuesday", "wednesday", "thursday", "friday"]
DAY_LABELS = {
    "monday": "Monday", "tuesday": "Tuesday", "wednesday": "Wednesday",
    "thursday": "Thursday", "friday": "Friday"
}


def fmt_date(date_str):
    """Format YYYY-MM-DD as '30 Mar' """
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return d.strftime("%-d %b")
    except Exception:
        return date_str


def build_days(data):
    monday_date = datetime.strptime(data["monday_date"], "%Y-%m-%d")
    existing = data.get("existing_meetings", {})
    proposed = data.get("proposed_blocks", [])

    days = []
    for i, day_name in enumerate(DAYS_ORDER):
        day_date = monday_date + timedelta(days=i)
        day_date_str = day_date.strftime("%Y-%m-%d")

        blocks = []

        # Existing meetings
        for m in existing.get(day_name, []):
            blocks.append({
                "type": "meeting",
                "date": day_date_str,
                "start_time": m["start_time"],
                "end_time": m["end_time"],
                "duration_min": None,
                "title": m["title"],
                "description": m.get("description", ""),
                "action_ids": [],
            })

        # Proposed blocks
        for b in proposed:
            if b.get("day", "").lower() == day_name:
                block_date = b.get("date", day_date_str)
                blocks.append({
                    "type": b.get("type", "deep"),
                    "date": block_date,
                    "start_time": b["start_time"],
                    "end_time": b["end_time"],
                    "duration_min": b.get("duration_min"),
                    "title": b["title"],
                    "description": b.get("description", ""),
                    "action_ids": b.get("action_ids", []),
                    # UTC stamps for the ICS export, computed per block date (DST-correct)
                    "dtstart_utc": to_utc_ics(block_date, b["start_time"]),
                    "dtend_utc": to_utc_ics(block_date, b["end_time"]),
                })

        # Sort by start time
        blocks.sort(key=lambda x: x["start_time"])

        days.append({
            "name": day_name,
            "busiest": day_name == BUSIEST_WEEKDAY.strip().lower(),
            "label": DAY_LABELS[day_name],
            "date_fmt": fmt_date(day_date_str),
            "blocks": blocks,
        })

    return days


def main():
    parser = argparse.ArgumentParser(description="Generate weekly plan HTML from JSON data.")
    parser.add_argument("--input", required=True, help="Path to plan JSON file")
    parser.add_argument("--output", required=True, help="Path to output HTML file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Autoescape is on: meeting and action titles come from email and calendar data and are
    # untrusted. Jinja's built-in tojson filter is HTML-safe inside a single-quoted attribute.
    env = Environment(autoescape=True)
    template = env.from_string(TEMPLATE)

    days = build_days(data)

    html = template.render(
        week_label=data.get("week_label", "Week Plan"),
        generated_at=datetime.now(USER_TZ).strftime("%Y-%m-%d %H:%M"),
        open_actions=data.get("open_actions", []),
        days=days,
        ics_uid_domain=USER_EMAIL_DOMAIN,
    )

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()
