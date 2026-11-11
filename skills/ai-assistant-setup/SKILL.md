---
name: ai-assistant-setup
description: >
  Guide set for designing a persistent assistant setup on Claude, ChatGPT/Codex or Gemini:
  project instructions and AGENTS.md, skills, memory, scheduled and self-improving tasks, MCP
  connections, security, personal data projects, LLM wikis and second brains, company
  policies, behaviour tests, multi-project and dual-platform layouts, action authority,
  importing or retiring a setup. Use when the user is designing, restructuring or
  troubleshooting such a setup ("how should I set up Claude to...", "create a skill for...",
  "where should this rule live", "Claude keeps forgetting...", "make this project work in Codex
  too"). Do NOT use for improving the wording of one prompt, instruction file or skill
  description (`prompt-improver`), or when an installed skill owns the request:
  `cowork-optimizer` (make one task cheaper), `dispatch` (model tiers), `git-guru` (git),
  `template-exporter` (shareable templates), `review-protocol` (reviewing a document or decision).
---

# Assistant Setup (Claude, ChatGPT/Codex, Gemini)

Help the user build or improve a persistent assistant setup by applying the bundled guides to
their actual files. Load only the guides the request needs.

**What this folder contains.** `references/` holds the complete Cluide guide set (`00`–`35`)
and `references/00_INDEX.md`, which describes every guide and the reading tracks. Nothing else
is needed to run the skill. The Cluide repository also has runnable `tasks/` and copy-paste
`templates/`; they are not bundled. When they are reachable (a Cluide checkout in the working
folder), prefer them. When they are not, follow the guide directly and build the files from what
it describes; the result is the same in substance but you write the structure yourself, so say so.
Do not report the missing folders as a fault. A guide link to `tasks/` or
`templates/` is a pointer to that optional checkout.

## Which guide to load

When the request does not clearly match a row, read `references/00_INDEX.md` first.

| Guide | Load when the user... |
|---|---|
| `00_QUICKSTART.md` | is starting from nothing and wants the shortest route |
| `01_PROJECT_INSTRUCTIONS.md` | writes or fixes `AGENTS.md`, `CLAUDE.md` or app project instructions, or the assistant misbehaves session to session (`01_CLAUDE_MD.md` is a pointer to it) |
| `02_PROMPTING_BASICS.md` | wants instructions that are followed reliably |
| `03_SKILLS.md` | creates or improves a skill: purpose, trigger description, workflow, output (if a dedicated skill-building skill is installed, it can handle evals and packaging) |
| `04_MEMORY_AND_PROFILE.md` | wants the assistant to remember across sessions |
| `05_MCP_SERVERS.md` | connects email, calendar or other tools |
| `06_TASK_EFFICIENCY_GUIDE.md` | builds a scheduled task and wants it cheap from the start |
| `07_TASK_LEARNING_GUIDE.md` | wants a task that improves from feedback (template install: Part 9; `08_SELFIMPROVE_TEMPLATE.md` is a pointer to it) |
| `09_MULTI_TASK_ORCHESTRATION.md` | has several tasks sharing state or handing off |
| `10_COST_PERFORMANCE.md` | worries about cost, decides which model a task should use, or tracks what tasks spend |
| `11_GIT_INTEGRATION.md` | wants assistant state under version control |
| `12_SECURITY.md` | asks about credentials, MCP trust, hooks, prompt injection or what to exclude |
| `13_DEV_EXECUTION_WORKFLOW.md` | develops in one interface and runs tasks in another |
| `14_PERSONAL_DATA_LAYER.md` | wants the assistant to work with personal data (finances, health, investments) |
| `15_LLM_WIKI.md` | builds a compounding knowledge base |
| `16_BEST_PRACTICES.md` | wants an overview of what matters most |
| `17_TROUBLESHOOTING.md` | reports something not working |
| `18_END_TO_END_WALKTHROUGH.md` | wants one narrative route through the whole system |
| `19_OUTPUT_FORMATTING.md` | decides how output is formatted for its destination |
| `20_INTERACTIVE_PROMPTING.md` | builds an interactive workflow with questions and plan mode |
| `21_COMPANY_POLICIES.md` | applies organisational policies as tiered guardrails |
| `22_HELPER_APPS.md` | vibe-codes a small personal tool over many sessions |
| `23_MULTI_PROJECT_SETUPS.md` | has several projects sharing facts |
| `24_PROJECT_FOLDER_STRUCTURE.md` | has a project getting messy, or wants a standard layout |
| `25_PROJECT_INSTRUCTION_LAYERS.md` | decides what goes in app-side fields versus files, or those have drifted |
| `26_CONTEXT_SCOPING.md` | wants "fresh eyes" on a deliverable, decides what a session or reviewer should see, or builds a high-stakes one-shot prompt |
| `27_INDEPENDENT_JUDGMENT.md` | wants a real second opinion on something they already have a view about |
| `28_SECOND_BRAIN.md` | wants an assistant to use scattered notes, or asks about a "second brain" |
| `29_SPEC_BEFORE_REBUILD.md` | has something built ad hoc where each fix costs more than the last |
| `30_CONTROLLED_DOCUMENTS.md` | reviews or manages documents with an owner, version and approver |
| `31_BEHAVIOUR_TESTS.md` | asks whether a rule or skill still works after a model launch or an edit, or wants regression tests |
| `32_ACTION_AUTHORITY.md` | decides what a task may do without asking |
| `33_RETIRING_AND_LEAVING.md` | retires a project or task, or is leaving an organisation or account |
| `34_IMPORTING_FROM_OTHER_ASSISTANTS.md` | moves a setup in from, or out to, another assistant |
| `35_DUAL_PLATFORM_PROJECTS.md` | runs one project from more than one assistant, has `CLAUDE.md` and `AGENTS.md` drifting apart, asks whether a skill or scheduled task works in another product, or had a job run twice; §9 holds the dated product facts |

## How to handle a request

> **Clarifying questions:** for any step with a fixed set of options, use the current surface's
> question tool when available, otherwise ask a concise question in chat.

1. **Identify the surface** before choosing a setup: Claude Code, Claude conversational or Cowork,
   ChatGPT project, Codex workspace, a Google surface (Antigravity, Gemini app), or more
   than one. Record file access, native skill support, available tools and scheduler access.
   Guide 35 owns coexistence, Guide 01 shared policy, Guide 25 the app bootstrap. A file upload is
   not an installed skill, and a missing Claude file is not a defect in an OpenAI or Google
   project. Google routes are documented in the guides but untested: say so when you rely on one,
   and verify any product fact against current official documentation.
2. **Classify the request:** start fresh, create something new, improve something existing, fix
   something broken, or learn. For improve and fix, ask for the relevant files and read them before
   recommending anything.
3. **Load the guide(s).** One guide for a focused request. For "set up everything", start from
   `00_QUICKSTART.md`, then build the layers 01 → 03 → 04, helping the user finish each before the
   next.
4. **Act.** If a Cluide `tasks/` folder is reachable, run the matching task (`tasks/README.md`
   routes them); it carries its own approval gates and restore points. Otherwise follow the guide.
   Create real files adapted to the user's domain and names; never leave placeholders such as
   `{project_name}` in a file you hand over.

## Starting structures

Guide 24 gives the standard project layout, Guide 06 and Guide 07 Part 9 what a scheduled task's
files hold, and Guide 14 the data-project stubs. Where the Cluide `templates/` folder is reachable, copy from it instead:
`PROJECT_TEMPLATE/` with `BLOCKS.md` (any project), `TASK_TEMPLATE/` (scheduled task),
`AI-ASSISTANT_TEMPLATE/` (Microsoft 365 business assistant), `PMO_TEMPLATE/` (programme
registers).

## A new personal data project

Follow Guide 14: interview (purpose, where data lives, what the assistant should do); recommend
which of its five patterns apply, one line of reason each, and confirm; create the structure, a
stub for each selected pattern, shared policy, native adapters and `.gitignore`; set up git, and a GitHub repo if `gh` is available
and the user wants one; end with numbered next steps. Keep its design rules: store facts, not
computed values; always include `last_updated`; the assistant reads data through feeder scripts,
never raw files.

## Improving an existing setup

1. Ask for the relevant files (`AGENTS.md`, `CLAUDE.md`, app bootstrap, task, skill and data
   files), what the setup is for and where it hurts, not what the user thinks is wrong; their
   diagnosis anchors yours. For a review or second opinion, load Guide 27.
2. Read the files and assess both ways: what is sound and must survive editing, and what is missing
   or working against them.
3. Write findings down before discussing them: file and line, what is wrong, severity (blocker /
   material / minor), confidence, and the evidence that would make you drop it. A finding with no
   answer to that last one is an opinion; leave it out.
4. Say plainly when nothing needs changing. Implement only after confirmation.

Common fixes: instruction file too long or vague (01); skill not triggering (03); task loading too
much context (06); data read raw instead of through feeders (14); no git for assistant state (11);
no self-improvement on a running task (07, Part 9).

## Style

Create files rather than describing them, use the user's real names and structures, and summarise
what you did. With a less technical user, say in one sentence what each file is for before creating
it.
