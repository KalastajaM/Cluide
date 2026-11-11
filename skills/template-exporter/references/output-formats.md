# Output Formats by Template Type

The exact file structure and content expectations for each template type the template-exporter skill produces, followed by per-platform install routes for the README. Every file uses the single placeholder format `[PLACEHOLDER: description — EXAMPLE: "..."]`.

---

## Chat System Prompt

**Use when:** the source is a system prompt, persona, custom instructions, or instruction block for a chat (a Claude, ChatGPT or Gemini project or notebook, or an API system prompt).

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
└── system-prompt.md
```

**`system-prompt.md` contents:**
- The full prompt text, sanitized
- A placeholder for every customisable value
- Brief HTML comments (`<!-- ... -->`) where intent may not be obvious to a new reader; tell the README reader to delete them before pasting if the target field shows them literally
- No conversation history, examples or sample user messages — those belong in README.md under "Notes"

**README "How to use it":** paste `system-prompt.md` into the target platform's project or custom-instructions field (see Platform install routes), or supply it as the `system` / `system_instruction` parameter for the API. App fields and API parameters are different interfaces; test the result in a fresh chat.

---

## Assistant Task

**Use when:** the source is a single task definition — a `TASK.md` file or equivalent step-by-step workflow, scheduled or on demand.

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
├── task.md
└── [companion files the task reads, by relative path]
```

**`task.md` contents:**
- Task name and one-line description
- Full step list with tool calls, conditionals and output instructions — sanitized
- Placeholders for tool or connector names, file paths, the schedule, and domain-specific values
- Companion files (a reference schema, a prompt fragment, an empty state file with headers only) included in the folder and referenced by relative path

**Notes:**
- Leave runtime state out: `IMPROVEMENTS.md`, `RUN_LOG.md`, outputs, logs.
- The schedule is a placeholder (`[PLACEHOLDER: when it runs — EXAMPLE: "weekdays at 07:30"]`), never an active registration. The README tells the recipient to run the task once by hand before scheduling it.
- If the task uses a skill, the README names it and says it must be installed separately.

---

## Assistant Project

**Use when:** the source is a project with instructions plus several tasks, shared context files or a folder structure.

**Folder structure — single platform:**
```
template-[name]/
├── README.md
├── SETUP.md
├── project.md            # human-readable: purpose, tasks and their roles, schedule overview
├── instructions.md       # the project instructions text, as pasted into the app or used as the root instruction file
├── context/              # optional: shared knowledge files, sanitized
└── tasks/
    ├── task-01-[short-name].md
    └── ...
```

**Add these when the template targets more than one platform, or when the source already has them:**
```
├── AGENTS.md             # shared policy that carries its own text (read natively by Codex, Antigravity and recent Claude Code)
├── CLAUDE.md             # thin Claude adapter: @AGENTS.md plus Claude-only items, labelled
└── PLATFORM_SETUP.md     # per-platform bootstrap steps, known gaps, and a blank scheduler-owner table
```

In that case `AGENTS.md` replaces `instructions.md`. Do not add a `GEMINI.md` beside `AGENTS.md`: their precedence in one directory is undocumented.

**`project.md` contents:**
- Project name and purpose
- List of tasks and their roles, in execution order
- Shared configuration (context files, tools, connectors, schedule overview)
- Placeholders for project name, owner and shared paths

**`tasks/` subfolder:** one file per task following the Assistant Task spec, named `task-[nn]-[short-name].md`, numbered in logical execution order.

**Scheduler-owner table** (in `PLATFORM_SETUP.md`, or in README.md for a single-platform project) — blank, for the recipient to fill:

| Task | Runs on (one platform only) | Schedule | Registered? |
|------|-----------------------------|----------|-------------|
| task-01-[short-name] | | | |

One owner per job: the same task registered on two schedulers runs twice.

**README "How to use it":** customise placeholders, then follow the platform route below (or `PLATFORM_SETUP.md`). Supply `project.md` as context, not as a native configuration format. Verify the instructions loaded by asking a fresh session what its project instructions say. Register only the tasks you choose, each on one scheduler, after a manual test run.

---

## Skill

**Use when:** the source is a `SKILL.md` file, with or without `references/`, `scripts/` or other subfolders.

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
└── [skill-name]/
    ├── SKILL.md
    ├── references/       # if present in the source
    └── scripts/          # if present in the source
```

Nest the skill in its own folder so the recipient can install that folder unchanged; several platforms require the folder name to match the skill's `name`.

**`SKILL.md` contents:**
- Full skill definition with frontmatter (`name`, `description`) — sanitized
- Placeholders for domain-specific instructions, tool names or file paths
- Keep the `description` functionally accurate: it decides when the skill triggers. Keep it within 1024 characters, the Agent Skills specification limit, so the same file installs on every platform
- Keep platform-specific frontmatter keys or metadata files (for example Codex `agents/openai.yaml`) and label them in the README; they are not portable permission controls

**Subfolders:** preserve filenames and structure exactly and sanitize contents by the same rules. Note in the README any reference file over ~300 lines that may need splitting, and any script's runtime requirement (for example Python 3).

**README "How to use it":** customise placeholders, then install the complete `[skill-name]/` folder by the target platform's route below. Verify the skill is discovered and behaves as expected after installation.

---

## Platform Install Routes

Documented as of October 2026; the Antigravity row was re-checked in November 2026. Install paths and menus change; check the platform's current documentation before relying on a row, and mark in the README which routes were actually tested.

| Platform | Instructions / system prompt | Skills | Scheduled tasks |
|----------|------------------------------|--------|-----------------|
| Claude app (chat projects, Cowork) | Project instructions field; files as project knowledge or a connected folder | The skill installation surface available to the account (typically uploading the zipped skill folder) | Cowork scheduled tasks |
| Claude Code | `CLAUDE.md` (or `AGENTS.md`, read natively in recent versions when no `CLAUDE.md` exists) | `.claude/skills/<name>/` (project) or `~/.claude/skills/<name>/` (personal) | Not native; use the Claude app or an external scheduler |
| ChatGPT | Project instructions; files as project sources | The skill or plugin installation surface available to the account | ChatGPT scheduled tasks |
| Codex | `AGENTS.md` | `.agents/skills/<name>/` (repository) or `~/.agents/skills/<name>/` (personal) | Codex scheduled tasks |
| Gemini app | Notebook instructions; files as notebook sources | Upload a `SKILL.md`, or a folder or `.zip` holding one, on the Skills page (personal accounts) | Scheduled actions; Tasks have their own schedules (*re-verify* availability) |
| Antigravity | `AGENTS.md` (no `GEMINI.md` beside it) | `.agents/skills/<name>/` (workspace); `~/.gemini/config/skills/<name>/` (global, read by the app, IDE and CLI) | Antigravity Automations |
| API | `system` (Anthropic), instructions parameter (OpenAI), `system_instruction` (Gemini) | Per the vendor's skills API | Not applicable |

Where a platform offers no skill installation, the recipient can supply the skill folder as a source and invoke it explicitly; that is not automatic discovery, and the README should say so. An uploaded file is a copy: tell the recipient to re-upload after editing the template.
