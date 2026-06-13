# Task: Setup MCP Servers

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Claude, run tasks/setup-mcp.md`
> **Source guide:** `05_MCP_SERVERS.md`

## Purpose
Audit the current MCP server configuration, identify what's connected and working, and guide setup of additional servers the user wants. MCP servers are what give Claude access to external tools — Gmail, Calendar, GitHub, filesystem, and more.

---

## Instructions

> **Clarifying questions:** For any step with a fixed set of options, use `AskUserQuestion` with buttons instead of plain text.

### Step 1 — Audit current state

First determine the environment — Cowork or Claude Code — since MCP servers are configured differently in each (note: `settings.json` holds permissions/hooks/env in Claude Code, never `mcpServers`).

**In Claude Code:**

```bash
# Registered servers across all scopes (local: ~/.claude.json, project: .mcp.json, user)
claude mcp list

# Project-scoped servers, if any
cat .mcp.json 2>/dev/null | python3 -m json.tool || echo "no project .mcp.json"
```

**In Cowork:** remote connectors are managed in Settings → Connectors; local servers live in `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`). Check the local config if accessible, and otherwise rely on the tool listing below.

In both environments, also list currently available tools:
> "What MCP tools do you currently have access to? List them by server."

Report findings in a brief summary:
```
Environment: [Cowork | Claude Code]
Currently configured MCP servers: [list by scope/source, or "none"]
Active tools: [list by server, or "none detected"]
```

### Step 2 — Ask what the user wants

Present the most common MCP servers and ask which the user wants to set up:

> "Which of these would you like to connect? (You can also say 'all that apply' or describe what you want to do and I'll suggest the right server.)"
>
> **Personal (Google Workspace):**
> - Gmail + Google Calendar + Drive — official Google MCP server, handles all Google Workspace tools
>
> **Business:**
> - Microsoft 365 (Outlook, Teams, SharePoint)
> - Atlassian (Jira + Confluence)
> - Slack
>
> **Universal:**
> - Filesystem — lets Claude read/write local files and directories
> - GitHub — access to repos, issues, pull requests
>
> **Browser & Desktop:**
> - Claude in Chrome — full browser control for web apps without APIs
> - Computer Use — native desktop app control

For each server the user wants, also ask:
- **Scope?** Claude Code: user scope = every project, project scope = `.mcp.json` here (shareable via git), local scope = this project, private. Cowork: local servers in `claude_desktop_config.json` apply to all sessions; remote connectors are account-level.
- **Credentials needed?** (API key, OAuth token, directory path)

**In Cowork:** for Gmail/Calendar/Drive, Microsoft 365, Atlassian, and Slack, prefer the built-in connectors (Settings → Connectors) — OAuth is handled in-app and no JSON editing is needed. Only fall back to manual config for servers without a connector.

### Step 3 — Set up each server

For each server the user wants to add:

**a) Check if `npx` / `node` is available** (required for most servers):
```bash
node --version && npx --version || echo "Node.js not installed — required for most MCP servers"
```
If missing, tell the user: "Node.js is required. Install it from nodejs.org, then re-run this task."

**b) Determine the target config** — Claude Code: prefer `claude mcp add` (with `--scope project` to write `.mcp.json`, or `--scope user` for everywhere); Cowork local servers: `claude_desktop_config.json`.

**c) If editing a JSON file directly** (Cowork local config, or project `.mcp.json`), read it first, or start with `{}`.

**d) Add the server entry** under `mcpServers` (or pass the equivalent to `claude mcp add`). Use the templates below. Pin versions where possible (replace `@latest` with a specific version after confirming).

**Filesystem:**
```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/directory"]
}
```
Ask the user which directories Claude should have access to.

**GitHub:**
```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
  }
}
```
Ask the user to provide their GitHub personal access token. Remind them: use a token with only the scopes needed (read-only if the use case allows).

**Slack:**
```json
"slack": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-slack"],
  "env": {
    "SLACK_BOT_TOKEN": "xoxb-...",
    "SLACK_TEAM_ID": "T..."
  }
}
```

**Google Workspace / Microsoft 365 / Atlassian:**
These require OAuth setup through the vendor's developer portal. Tell the user:
> "Google/Microsoft/Atlassian MCP servers require OAuth credentials from the vendor's developer console. I can walk you through the steps — which would you like to start with?"
Guide the relevant setup steps based on their choice.

**e) Write the updated config** — merge the new server entry without overwriting existing entries (not needed when using `claude mcp add`).

**Security reminder** — after adding any credential to a config file, say:
> "Credentials are now in `[config file]`. If this file lives in a git repo (e.g. `.mcp.json`), make sure it's in `.gitignore`, or keep tokens out of it and export them from your shell profile instead."

### Step 4 — Verify

After adding each server:
Remind the user: restart the Claude Code session (or the desktop app, for Cowork) to pick up the new server configuration.

Tell the user:
> "After restarting, ask: 'What MCP tools do you have access to?' to confirm the new server is connected."

### Step 5 — Confirm

Tell the user:
- Which servers were added and where (scope / config file)
- Which tools each server exposes
- Any servers that were skipped and why
- "To add more servers later, re-run this task, use `claude mcp add` (Claude Code), or Settings → Connectors / Developer (Cowork)."
