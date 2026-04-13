# WeeklyPlanner Task Reference

Read on demand — not loaded on every run. Referenced by TASK.md.

---

## § HTML Week Plan Format

Generate a calendar-booking-friendly HTML file with the following structure:

**Layout:** Five-column layout (one column per day, Mon–Fri).

**Existing meetings:** Shown as light grey blocks.

**Proposed work blocks:** Shown as coloured cards, colour-coded by type:
- Deep work → blue
- Quick actions → green
- Meeting prep → amber
- Conditional → dashed grey

**Each proposed block card must include:**
- Start time, end time, duration
- Title
- Brief description
- A **📅 Add to Outlook** button

**ICS button behaviour:** The button uses a JavaScript Blob to generate and download a `.ics` file (iCalendar format) for that block when clicked. Use UTC times in the `.ics` (convert from local time by subtracting `[YOUR_UTC_OFFSET_HOURS]` hours). Each VEVENT must include: `SUMMARY`, `DTSTART`, `DTEND`, `DESCRIPTION`, and `UID`.

**Friday column:** Visually muted with a note that no blocks are scheduled unless a hard deadline forces one.

**Top of page:** Include a legend and an open actions table.
