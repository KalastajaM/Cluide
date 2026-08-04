# Output Formats by Template Type

This reference defines the exact file structure and content expectations for each template type produced by the template-exporter skill.

---

## Chat System Prompt

**Use when:** The source is a system prompt, persona definition, or instruction block intended for a Claude chat (claude.ai or API system prompt).

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
> Copy the contents of `system-prompt.md` into the System Prompt field when creating a new Claude chat at claude.ai, or pass it as the `system` parameter in your API call.

---

## Cowork Task

**Use when:** The source is a single Cowork task definition — a TASK.md file or equivalent step-by-step automation workflow.

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

## Cowork Project

**Use when:** The source is a multi-task Cowork project — a project config with multiple tasks, possibly a shared context or knowledge file.

**Folder structure:**
```
template-[name]/
├── README.md
├── SETUP.md
├── project.md
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
- One file per task, following the Cowork Task spec above
- Files named `task-[nn]-[short-name].md` for clarity
- Order files to reflect logical execution order (not alphabetical if different)

**README "How to use it" section should say:**
> Create a new Cowork project. Import `project.md` as the project config, then add each file in `tasks/` as a separate task. Customize all `[PLACEHOLDER: ...]` values before running.

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
> Copy `SKILL.md` (and the `references/` folder if present) into your `.claude/skills/[skill-name]/` directory. Customize all `[PLACEHOLDER: ...]` values. The skill will be available in Claude Code automatically.
