# Task: Setup MCP Servers

> **Portable task** — copy this file to any project's `tasks/` directory and run:
> `Assistant, run tasks/setup-mcp.md`
> **Source guide:** `05_MCP_SERVERS.md`

## Runtime route

Name the target surface and available tools before running steps. Claude-only policy lives in `CLAUDE.md`; Codex uses `AGENTS.md`; dual-platform shares `AGENTS.md` through a thin Claude adapter. References below to editing project rules mean that selected policy, not duplicated adapters. ChatGPT source projects use project instructions and dated sources; without write access, return replacement artifacts and record refresh as pending.

Execute only the selected native branch. Claude commands/settings/hooks are Claude-only; never install them as an OpenAI fix. Missing access is **unverified**; an unnecessary capability is **N/A**. Use an available, permitted question tool or concise chat, reusing existing answers and authorization. Unattended runs record unresolved decisions. Report applied versus drafted changes and fresh-session verification per supported surface; untested is not passed.

## Native implementation

Inventory the tools actually exposed in this session before installing anything; existing connectors may already meet the need. Never print credential-bearing configuration values.

**Codex route (replaces Claude commands in Steps 1 and 3):** inspect the runtime's MCP tools and configured server names; verify `codex mcp --help` if the CLI is available. Select documented user/project scope, then add the server through the available native integration tool or the documented `mcp_servers` table in Codex configuration. Preserve unrelated settings, use environment/secret references instead of inline credentials, and follow the server's actual transport/auth documentation. Reconnect as needed, list discovered tools, and run one harmless read test. Record config scope, authentication status and result. The specific CLI syntax and config keys must be re-checked against [Codex MCP](https://learn.chatgpt.com/docs/mcp); if that source cannot be fetched, use CLI help or mark configuration unverified and stop before writing it.

**ChatGPT route:** find the requested app in the available app/connector catalog and use its supported connection flow; for custom MCP, verify the plan/admin permissions and currently documented connection UI first. Complete OAuth in the native flow. Inspect exposed tools and perform a harmless read. Do not edit local Claude JSON or claim an upload connects a server. If the connector is unavailable, identify the missing grant/feature and return the setup instructions for that surface.

**Claude Code/Cowork:** use the labelled native branches below. Node is needed only for a server whose launch command requires it; remote HTTP/OAuth connectors do not require a local Node installation. Tool names in examples are illustrative until matched to actual discovery.

## Purpose
Audit the current MCP server configuration, identify what's connected and working, and guide setup of additional servers the user wants. MCP servers are what give Claude access to external tools — Gmail, Calendar, GitHub, filesystem, and more.

---

## Instructions

> **Clarifying questions:** use an available question tool when the runtime permits it; otherwise ask concisely in chat. Reuse answers already supplied.

### Step 1 — Audit current state

For the Claude branch, determine the environment — Cowork or Claude Code — since MCP servers are configured differently in each (note: `settings.json` holds permissions/hooks/env in Claude Code, never `mcpServers`).

**In Claude Code:**

```bash
# Registered servers across all scopes (local: ~/.claude.json, project: .mcp.json, user)
claude mcp list

# Project-scoped servers, if any
python3 -c 'import json,pathlib; p=pathlib.Path(".mcp.json"); print(list(json.loads(p.read_text()).get("mcpServers",{})) if p.exists() else "no project .mcp.json")'
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

**Codex/ChatGPT:** execute the native implementation above, then continue at Step 4 using that surface’s reconnect/discovery process. The commands and JSON templates below are **Claude Code/Cowork only**.

For each server the user wants to add:

**a) For a local server launched with Node only, check `npx` / `node`:
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

**GitHub** — use GitHub's official server, not the archived `@modelcontextprotocol/server-github` npm package:
- **Remote (recommended)** — Claude Code: `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` (OAuth handled on connect — no token to paste). Cowork: add the same URL as a custom connector (Settings → Connectors).
- **Local / GitHub Enterprise** — run GitHub's official `github/github-mcp-server` binary and pass a fine-grained token via its `env`; grant only the scopes needed (read-only if the use case allows).

**Slack** — prefer the built-in **Slack connector** (Settings → Connectors in Cowork / Claude): OAuth handled in-app, no JSON. The old `@modelcontextprotocol/server-slack` npm package is archived; if you need a local server, pick a maintained one from the MCP Registry (see Step 5).

**Google Workspace / Microsoft 365 / Atlassian:**
These require OAuth setup through the vendor's developer portal. Tell the user:
> "Google/Microsoft/Atlassian MCP servers require OAuth credentials from the vendor's developer console. I can walk you through the steps — which would you like to start with?"
Guide the relevant setup steps based on their choice.

**e) Write the updated config** — merge the new server entry without overwriting existing entries (not needed when using `claude mcp add`).

**Security reminder** — after adding any credential to a config file, say:
> "Credentials are now in `[config file]`. If this file lives in a git repo (e.g. `.mcp.json`), make sure it's in `.gitignore`, or keep tokens out of it and export them from your shell profile instead."

### Step 4 — Verify

For Codex/ChatGPT use native reconnection and verify one harmless read. The following restart instructions apply to Claude.

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
