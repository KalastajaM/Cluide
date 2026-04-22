#!/usr/bin/env python3
"""
generate_weekplan_html.py — Renders the weekly plan HTML from a JSON data file.

Usage:
    python3 generate_weekplan_html.py --input plan.json --output weekplan.html

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
      "title": "Deep work: VCP analysis",
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
import uuid
from datetime import datetime, timedelta
from jinja2 import Environment

# ============================================================
# USER CONFIG — edit these for your setup
# ============================================================
USER_TIMEZONE_UTC_OFFSET_HOURS = 2           # Local-time → UTC offset used by the ICS export (standard time)
USER_EMAIL_DOMAIN = "example.com"            # Domain used in ICS UIDs
# ============================================================

TEMPLATE = """<!DOCTYPE html>
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
  .badge-soon { background: #fef3c7; color: #92400e; }
  .badge-low  { background: #f3f4f6; color: #6b7280; }
  .badge-high { background: #fee2e2; color: #991b1b; }
  .badge-medium { background: #dbeafe; color: #1e40af; }
  .no-actions { color: #999; font-style: italic; padding: 8px 12px; }

  /* Calendar grid */
  .calendar { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
  .day-col { background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
  .day-col.friday { opacity: 0.65; }
  .day-header { padding: 10px 12px; font-weight: 600; font-size: 12px; background: #374151; color: #fff; }
  .day-header.friday { background: #9ca3af; }
  .day-body { padding: 8px; display: flex; flex-direction: column; gap: 6px; min-height: 120px; }
  .friday-note { color: #9ca3af; font-style: italic; font-size: 11px; padding: 8px 4px; }

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
  <div class="day-col{% if day.name == 'friday' %} friday{% endif %}">
    <div class="day-header{% if day.name == 'friday' %} friday{% endif %}">
      {{ day.label }}<br><span style="font-weight:400; font-size:11px; opacity:0.8;">{{ day.date_fmt }}</span>
    </div>
    <div class="day-body">
      {% if day.name == 'friday' and not day.blocks %}
        <div class="friday-note">No blocks scheduled — typically packed with recurring meetings.</div>
      {% else %}
        {% for block in day.blocks %}
        <div class="block block-{{ block.type }}">
          <div class="block-time">{{ block.start_time }}–{{ block.end_time }}{% if block.duration_min %} ({{ block.duration_min }} min){% endif %}</div>
          <div class="block-title">{{ block.title }}</div>
          {% if block.description %}<div class="block-desc">{{ block.description }}</div>{% endif %}
          {% if block.action_ids %}<div class="block-ids">{{ block.action_ids | join(', ') }}</div>{% endif %}
          {% if block.type != 'meeting' %}
          <button class="ics-btn" onclick="downloadICS({{ block | tojson }})">📅 Add to Outlook</button>
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
var TZ_OFFSET_HOURS = {{ tz_offset_hours }};  // local-time → UTC offset (standard time)
var ICS_UID_DOMAIN  = {{ ics_uid_domain | tojson }};

function pad(n) { return String(n).padStart(2, '0'); }

function toUTC(dateStr, timeStr) {
  // dateStr = "YYYY-MM-DD", timeStr = "HH:MM" (local time)
  var parts = dateStr.split('-');
  var timeParts = timeStr.split(':');
  var d = new Date(Date.UTC(
    parseInt(parts[0]),
    parseInt(parts[1]) - 1,
    parseInt(parts[2]),
    parseInt(timeParts[0]) - TZ_OFFSET_HOURS,  // subtract configured offset for local→UTC
    parseInt(timeParts[1])
  ));
  return d.getUTCFullYear() + pad(d.getUTCMonth()+1) + pad(d.getUTCDate()) + 'T' +
         pad(d.getUTCHours()) + pad(d.getUTCMinutes()) + '00Z';
}

function downloadICS(block) {
  var uid = 'weekplan-' + block.date + '-' + block.start_time.replace(':','') + '@' + ICS_UID_DOMAIN;
  var dtstart = toUTC(block.date, block.start_time);
  var dtend   = toUTC(block.date, block.end_time);
  var desc = (block.description || '').replace(/\n/g, '\\n');
  var ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//WeekPlan//EN',
    'BEGIN:VEVENT',
    'UID:' + uid,
    'DTSTAMP:' + toUTC(block.date, block.start_time),
    'DTSTART:' + dtstart,
    'DTEND:' + dtend,
    'SUMMARY:' + block.title,
    'DESCRIPTION:' + desc,
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
                blocks.append({
                    "type": b.get("type", "deep"),
                    "date": b.get("date", day_date_str),
                    "start_time": b["start_time"],
                    "end_time": b["end_time"],
                    "duration_min": b.get("duration_min"),
                    "title": b["title"],
                    "description": b.get("description", ""),
                    "action_ids": b.get("action_ids", []),
                })

        # Sort by start time
        blocks.sort(key=lambda x: x["start_time"])

        days.append({
            "name": day_name,
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

    env = Environment()
    env.filters["tojson"] = json.dumps
    template = env.from_string(TEMPLATE)

    days = build_days(data)

    html = template.render(
        week_label=data.get("week_label", "Week Plan"),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        open_actions=data.get("open_actions", []),
        days=days,
        tz_offset_hours=USER_TIMEZONE_UTC_OFFSET_HOURS,
        ics_uid_domain=USER_EMAIL_DOMAIN,
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {args.output}")


if __name__ == "__main__":
    main()
