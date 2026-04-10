# Cluide — The Claude Guide: Project Instructions

## About This Project

This folder contains a complete operational framework for building, running, and improving a persistent AI assistant with Claude. It includes architecture guides, runnable setup and audit tasks, installable skills, and copy-paste templates — covering the full lifecycle from initial setup to scheduled automation, self-improvement, and security. The guides are both human-readable and intended as direct input to Claude.

**When working in this project, apply the guides to your own behavior.** You have access to all of them as context. Use them:

- When asked to help set up or improve a Claude assistant, follow the patterns described in the relevant guide
- When writing or editing `CLAUDE.md` files, skills, tasks, or memory files for the user, apply the structure and principles from the guides
- When something you're doing is covered by a guide, do it the way the guide describes — don't invent a different approach

**Guide map** (read `00_INDEX.md` for full descriptions):

| Guide | Topic |
|---|---|
| `01_CLAUDE_MD.md` | Writing effective CLAUDE.md files |
| `02_SKILLS.md` | Designing skills |
| `03_MEMORY_AND_PROFILE.md` | Memory and profile files |
| `04_TASK_EFFICIENCY_GUIDE.md` | Making tasks run efficiently |
| `05_TASK_LEARNING_GUIDE.md` | Tasks that learn and improve over time |
| `06_SELFIMPROVE_TEMPLATE.md` | Self-improving task template |
| `07_BEST_PRACTICES.md` | General best practices |
| `08_MCP_SERVERS.md` | MCP server setup and usage |
| `09_GIT_INTEGRATION.md` | Git integration, `.gitignore`, `.claudeignore` |
| `10_DEV_EXECUTION_WORKFLOW.md` | Development execution workflow |
| `11_PERSONAL_DATA_LAYER.md` | Personal data and profile layer |
| `12_LLM_WIKI.md` | LLM wiki pattern |
| `13_SECURITY.md` | Security best practices for Claude Code and Cowork |
| `14_TROUBLESHOOTING.md` | Diagnosing and fixing common problems |
| `15_PROMPTING_BASICS.md` | Writing instructions that produce consistent output |
| `16_MULTI_TASK_ORCHESTRATION.md` | Coordinating multiple tasks with shared state |
| `17_COST_PERFORMANCE.md` | Tracking token usage, budgeting, and cost monitoring |

When the user asks a question or makes a request that a guide covers, read the relevant guide before responding.

---

## File Hygiene

When creating new files, check whether they belong in `.gitignore` or `.claudeignore`:
- **Add to `.gitignore`**: run logs, output files, auto-generated bundles, any file containing personal data (paths, names, company names)
- **Add to `.claudeignore`**: large generated files that don't need to be loaded as context (compiled skill bundles, output archives, etc.)

If a newly created file should be ignored but is already tracked by git, run `git rm --cached <file>` to untrack it.
