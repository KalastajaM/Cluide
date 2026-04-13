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

Check what MCP servers are currently configured:

```bash
# Global settings
cat ~/.claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A5 '"mcpServers"' || echo "no global settings"

# Project-level settings
cat .claude/settings.json 2>/dev/null | python3 -m json.tool | grep -A5 '"mcpServers"' || echo "no project settings"
```

Also ask Claude to list its currently available tools:
> "What MCP tools do you currently have access to? List them by server."

Report findings in a brief summary:
```
Currently configured MCP servers:
  Global: [list or "none"]
  Project: [list or "none"]

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
- **Global or project-level?** Global = available in every project. Project = only here.
- **Credentials needed?** (API key, OAuth token, directory path)

### Step 3 — Set up each server

For each server the user wants to add:

**a) Check if `npx` / `node` is available** (required for most servers):
```bash
node --version && npx --version || echo "Node.js not installed — required for most MCP servers"
```
If missing, tell the user: "Node.js is required. Install it from nodejs.org, then re-run this task."

**b) Determine the target settings.json** — global (`~/.claude/settings.json`) or project (`.claude/settings.json`).

**c) Read the target settings.json** if it exists, or start with `{}`.

**d) Add the server entry** under `mcpServers`. Use the templates below. Pin versions where possible (replace `@latest` with a specific version after confirming).

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

**e) Write the updated settings.json** — merge the new server entry without overwriting existing entries.

**Security reminder** — after adding any credential to settings.json, say:
> "Credentials are now in `settings.json`. Make sure this file is in `.gitignore` if the project is on GitHub, or use a keychain reference instead of a plain-text token."

### Step 4 — Verify

After adding each server:
```bash
# Restart will be needed — remind the user
echo "Restart Claude Code to pick up the new server configuration."
```

Tell the user:
> "After restarting Claude Code, ask: 'What MCP tools do you have access to?' to confirm the new server is connected."

### Step 5 — Confirm

Tell the user:
- Which servers were added and where (global vs. project)
- Which tools each server exposes
- Any servers that were skipped and why
- "To add more servers later, re-run this task or edit the relevant `settings.json` directly."
