# MCP Servers: Connecting Claude to Your Tools

> MCP (Model Context Protocol) is how Claude gets access to external tools — Gmail, Calendar, files, GitHub, and more. Without it, Claude can only read and write text. With it, Claude can actually do things on your behalf. This guide explains what MCP servers are, how to set them up, and how to use them in skills.

---

## What MCP Servers Are

An MCP server is a small program that runs alongside Claude and exposes a set of tools Claude can call. When you ask Claude to "check your email" or "create a calendar event", it calls a tool provided by an MCP server. The server handles the actual API call and returns the result to Claude.

From Claude's perspective, MCP tools work just like any built-in capability — it can call `gmail_search_messages`, get a list of emails back, and then call `gmail_create_draft` to draft a reply. Claude does not need to know how the server works; it just knows what tools are available and what they do.

---

## How MCP Servers Connect to Claude Code

MCP servers are configured in a settings file. Claude Code supports two scopes:

- **Global** (`~/.claude/settings.json`) — available in every project
- **Project-level** (`.claude/settings.json` inside a project folder) — available only in that project

Use project-level config when a server is only relevant to one project. Use global config for servers you use everywhere.

Each server has a name, a launch command, and optionally environment variables for credentials.

**Minimal example:**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    }
  }
}
```

When Claude Code starts, it launches each configured server and discovers the tools it exposes. You can see which tools are available by asking Claude: *"What tools do you have available?"*

---

## Common MCP Servers

Servers are grouped by context. Most setups need one block from Personal or Business, plus the Universal servers at the bottom.

---

### Personal (Google Workspace)

#### Google Workspace
**Via:** Google's official MCP server

Google publishes an official MCP server covering Gmail, Google Calendar, Google Drive, Docs, and Sheets. Set it up through Google AI Studio or the Google Workspace MCP documentation — it handles OAuth authentication and exposes the full Workspace API surface.

Typical tools: `gmail_search_messages`, `gmail_read_message`, `gmail_create_draft`, `gcal_list_events`, `gcal_create_event`, `drive_search_files`, `drive_read_file`

---

### Business (Microsoft 365 / Atlassian / Slack)

#### Microsoft 365
Covers Outlook (email), Teams (chat and meetings), SharePoint, and OneDrive. Both Anthropic and community-maintained MCP servers exist for M365. Authentication goes through Azure Active Directory / Microsoft OAuth.

Typical tools: `outlook_email_search`, `outlook_calendar_search`, `chat_message_search`, `find_meeting_availability`, `sharepoint_search`, `sharepoint_folder_search`

---

#### Atlassian (Jira + Confluence)
Atlassian publishes an official MCP server covering both Jira and Confluence. Useful for assistants that track project work, bugs, or documentation.

Typical tools: `searchJiraIssuesUsingJql`, `getJiraIssue`, `createJiraIssue`, `editJiraIssue`, `getConfluencePage`, `searchConfluenceUsingCql`, `createConfluencePage`

---

#### Slack
**Package:** `@modelcontextprotocol/server-slack`

Read channel history, search messages, and post to channels. Useful for assistants that monitor team communication.

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

---

### Universal

#### Filesystem
**Package:** `@modelcontextprotocol/server-filesystem`

Gives Claude read/write access to specific directories on your machine. Required for any skill that reads or writes local files.

```json
"filesystem": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/Documents", "/Users/you/Projects"]
}
```

Key tools: `read_file`, `write_file`, `list_directory`, `search_files`

---

#### GitHub
**Package:** `@modelcontextprotocol/server-github`

Access to GitHub repositories, issues, and pull requests.

```json
"github": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
  }
}
```

Key tools: `list_issues`, `create_issue`, `get_pull_request`, `search_code`

---

#### Memory
**Package:** `@modelcontextprotocol/server-memory`

Persistent key-value store Claude can read and write across sessions — an alternative to file-based memory for lightweight state.

---

### Claude in Chrome

The Claude in Chrome MCP server (`mcp__Claude_in_Chrome__*`) gives Claude full control of your browser — navigating pages, clicking, filling forms, taking screenshots, reading page content, and extracting data. Installed via the Claude browser extension (Chrome Web Store).

Key tools: `navigate`, `read_page`, `get_page_text`, `find`, `form_input`, `javascript_tool`, `screenshot`

Use when the target is a web app with no dedicated MCP and no API, or when you need to interact with a page (click, fill, navigate). Browsers are read-only in computer use — use Claude in Chrome for browser interaction.

---

### Computer Use

The computer use MCP (`mcp__computer-use__*`) gives Claude direct control of your desktop — screenshots, mouse, keyboard, scrolling, opening applications. Works across all native apps.

Key tools: `screenshot`, `left_click`, `type`, `scroll`, `key`, `open_application`, `request_access`

**Access tiers by app category:**
- **Browsers** → read-only (use Claude in Chrome for interaction)
- **Terminals and IDEs** → click-only (use Bash tool for commands)
- **All other apps** → full access

Call `request_access` before using — the user approves each app explicitly. Use for native desktop apps with no dedicated MCP or cross-app workflows.

---

**Finding more servers:** The full MCP server catalogue is at [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers). Claude.ai (the web interface) also has a built-in integrations browser.

---

## Naming Tools in Skills

When writing a skill (see [Guide 03](./03_SKILLS.md)), name the exact MCP tool in the workflow steps. Do not just say "check the calendar" — say `gcal_list_events`. This prevents Claude from improvising a different approach each session.

**Weak (inconsistent behaviour):**
```markdown
Step 2: Check the calendar for conflicts.
```

**Strong (names the exact tool):**
```markdown
Step 2: Call `gcal_list_events` with the date range for the next 7 days.
        If the call fails, note the error and skip conflict checking this run.
```

Also state clearly what to do when a tool is unavailable or returns an error — a fallback or a graceful skip is better than crashing the skill.

---

## Checking What Tools You Have

Ask Claude directly:

> *"What MCP tools do you have access to? List them by server."*

Claude enumerates connected servers and their tools. Use this when writing skills — confirm the exact tool name before writing it into a workflow step.

---

## Credentials and Security

MCP server credentials (API keys, OAuth tokens) live in `settings.json` or in environment variables. A few rules:

- **Never put credentials in CLAUDE.md, skill files, or memory files** — those may be read back in session output. Credentials belong only in `settings.json` under the `env` block, or in a `.env` file loaded by the server.
- **Use read-only tokens where possible.** A Gmail token with read-only access is safer than one with send permission, for any skill that doesn't need to send.
- **Rotate tokens periodically.** Set a reminder to rotate every 6-12 months.

For the full credential hygiene treatment — including exposure response procedures and rotation schedules — see [Guide 12](./12_SECURITY.md).

---

## Troubleshooting by Server

When an MCP tool fails, start with this general checklist, then check the per-server notes.

**General diagnostic:**
1. Ask Claude: *"What MCP tools do you have available?"* If a server's tools are missing, it never started.
2. Validate `settings.json` syntax: `cat ~/.claude/settings.json | python3 -m json.tool`
3. Run the server's command manually in a terminal to see the real error.
4. Check Node version (`node --version`) — most servers require Node 18+.
5. Restart Claude Code after config or dependency changes.

**Common per-server issues:**

| Server | Common problem | Fix |
|---|---|---|
| Gmail / Google Workspace | Token expired (401) | Re-authenticate via OAuth. Tokens expire after ~7 days of inactivity. Run `gmail_get_profile` to test auth. |
| Gmail | Empty search results | Use Gmail query syntax (`after:2026/04/01`), not ISO dates. Test in Gmail's web search first. |
| Google Calendar | Events missing | Specify timezone explicitly. Check calendar ID via `list_calendars`. |
| Microsoft 365 | 401 on any call | M365 tokens expire after 60–90 min. Restart server process if auto-refresh fails. |
| Atlassian | "Site not found" / 404 | Site URL must be `https://yourcompany.atlassian.net` — no trailing slash. |
| Filesystem | "Path not in allowed list" | Add the directory to the `args` array in `settings.json`. |
| Claude in Chrome | Tools unavailable | Open Chrome, click extension icon to reconnect, restart Claude Code. |
| Computer Use | Click/type blocked | Check tier restrictions — browsers are read-only, terminals are click-only. |

**Cross-server misconfigurations:**

| Mistake | Fix |
|---|---|
| Tool name in skill doesn't match actual tool | Ask *"What MCP tools do you have?"* and copy the exact name. |
| Wrong `env` variable name | Check the server's README — `GITHUB_TOKEN` vs `GITHUB_PERSONAL_ACCESS_TOKEN` matters. |
| Credentials in `CLAUDE.md` instead of `settings.json` | Move to `settings.json` `env` block or `.env` file. |

---

## Rate Limits and Error Handling

Most MCP servers proxy APIs with rate limits. Add this to any skill step that calls an external MCP tool:

```markdown
If the tool call fails with a rate limit or timeout error:
  1. Wait 5 seconds and retry once.
  2. If it still fails, log the error and skip this step gracefully.
  3. Do not retry more than once.
```

**Error response strategy:**
- **Transient errors** (timeout, 429, 5xx): retry once after 5 seconds, then skip.
- **Auth errors** (401, 403): stop immediately, log which tool failed.
- **Empty results when data expected**: note in output, continue with available data.

---

## Giving This to Claude

**To audit your current MCP setup:**
> *"What MCP servers do I have configured? List the tools each one exposes and flag any that seem misconfigured."*

**To set up a new server:**
> *"Read 05_MCP_SERVERS.md and help me set up the filesystem MCP server so Claude can read my Documents folder."*

**To check what's needed for a skill:**
> *"I want to build a skill that checks my Gmail for action items. Read 05_MCP_SERVERS.md and tell me what MCP server I need and what tools it uses."*
