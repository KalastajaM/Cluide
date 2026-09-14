# Output Formats by Template Type

This reference defines the exact file structure and content expectations for each template type produced by the template-exporter skill.

---

## Chat System Prompt

**Use when:** The source is a system prompt, persona definition, or instruction block intended for an assistant chat (claude.ai or API system prompt).

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
└── system-prompt.md
```

**`system-prompt.md` contents:**
- The full system prompt text, sanitized
- `[PLACEHOLDER: ...]` markers for every customizable value
- Brief inline comments (HTML comments `<!-- ... -->`) where intent may not be obvious to a new reader
- Do NOT include conversation history, examples, or sample user messages here — those belong in README.md under "Notes"

**README "How to use it" section should say:**
> Use the selected surface’s documented project/custom-instruction route, or supply the text as an explicit source. API integrations must use that API’s documented instruction parameter. Verify the resulting behavior; app fields and API messages are different interfaces.

---

## Assistant Task

**Use when:** The source is a single Assistant task definition — a TASK.md file or equivalent step-by-step automation workflow.

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
└── task.md
```

**`task.md` contents:**
- Task name and one-line description
- Full step list with tool calls, conditionals, and output instructions — sanitized
- `[PLACEHOLDER: ...]` markers for: tool names, file paths, schedule triggers, and any domain-specific values
- Any companion files the task references (e.g. a reference schema, a prompt fragment) should be included as additional files in the folder and referenced by relative path

**Notes:**
- If the task has an `IMPROVEMENTS.md` or `RUN_LOG.md`, do NOT include them in the template — these are runtime state, not definition.
- If the task references a skill, include a note in README.md that the skill must be installed separately.

---

## Project (Claude, ChatGPT, or Codex)

**Use when:** The source is a multi-task assistant project — a project config with multiple tasks, possibly a shared context or knowledge file.

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
├── AGENTS.md             # shared policy
├── CLAUDE.md             # thin native adapter
├── PLATFORM_SETUP.md     # per-surface bootstrap, gaps, blank scheduler ownership
├── project.md            # human-readable project description, not imported config
└── tasks/
    ├── task-01.md
    ├── task-02.md
    └── ...
```

**`project.md` contents:**
- Project name and purpose
- List of tasks and their roles
- Any shared configuration (shared context file, shared tools, schedule overview)
- `[PLACEHOLDER: ...]` for project name, owner, shared paths

**`tasks/` subfolder:**
- One file per task, following the Assistant Task spec above
- Files named `task-[nn]-[short-name].md` for clarity
- Order files to reflect logical execution order (not alphabetical if different)

**README "How to use it" section should say:**
> Customise placeholders, then follow PLATFORM_SETUP.md for the selected surface. Supply project.md as context, not as an assumed native configuration format. Verify the shared policy in a new session. Task files are definitions: register only the jobs you choose, on one scheduler each, after a manual test.

---

## Skill

**Use when:** The source is a SKILL.md file, with or without a `references/` subfolder.

**Folder structure — simple skill (no references):**
```
template-[name]/
├── README.md
├── SETUP.md
└── SKILL.md
```

**Folder structure — skill with references:**
```
template-[name]/
├── README.md
├── SETUP.md
├── SKILL.md
└── references/
    ├── 01_reference-file.md
    └── ...
```

**`SKILL.md` contents:**
- Full skill definition with frontmatter (`name`, `description`) — sanitized
- `[PLACEHOLDER: ...]` for any domain-specific instructions, tool names, or file paths
- Preserve the original frontmatter `description` field structure — it is used for skill triggering and should remain functionally accurate

**References subfolder:**
- Preserve the original filenames and folder structure exactly
- Sanitize contents following the same rules as Step 2
- If a reference file is very large (>300 lines), note in README.md that it may need to be split for token efficiency

**README "How to use it" section should say:**
> Customise placeholders and install the complete skill folder through the target surface’s supported mechanism. Claude Code uses `.claude/skills/`; Codex repository skills use `.agents/skills/`. For a conversational source-only route, supply the workflow and invoke it explicitly. Verify discovery and behavior after installation; never treat Claude-specific metadata as a portable permission control.
