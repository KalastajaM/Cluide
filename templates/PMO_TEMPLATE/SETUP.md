# Setup Prompt

Paste this prompt into a Claude or OpenAI session to set up the **PMO Project** workspace automatically.

---

You are being given a template folder to set up. Follow these steps exactly:

1. Read every file in the copied template folder. The template files themselves are the single source of truth — this prompt embeds no copy of any of them.
2. List every `[PLACEHOLDER: ...]` (and bare `[PLACEHOLDER]`) in every file of the copied folder, grouped by file, and collect all values before substituting. This includes `AGENTS.md`, `PROJECT_GUIDE.md`, `project.md`, the registers under `PMO/`, and `Charter/Initiative_Charter.md`. Ask for short values (names, IDs, dates, gate names, the financial model filename, your name, role and timezone) one group at a time. For the long-form charter sections (context, decisions, objectives, risks, implementation steps, KPIs, financial benefit and costs, planning calculations, governance), point the user at `Charter/Initiative_Charter.md` to fill in; do not paraphrase or restate its content here.
3. Once all values are collected, substitute every placeholder with the provided value, editing the copied files in place.
4. Report which placeholders remain unfilled, file by file, so the user can complete them.

`project.md` holds the app-side project description/instructions text (the Guide 25 layer). After its placeholders are filled, apply the appropriate surface bootstrap from `PLATFORM_SETUP.md`; record the applied settings separately per surface.

Start by listing every placeholder you found, grouped by file, and ask the user to provide values for each.
