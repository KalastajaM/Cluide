# MCP Servers: Connecting Claude to Your Tools

*Last reviewed: April 2026*

> MCP (Model Context Protocol) is how Claude gets access to external tools — Gmail, Calendar, files, GitHub, and more. Without it, Claude can only read and write text. With it, Claude can actually do things on your behalf. This guide explains what MCP servers are, how to set them up, and how to use them in skills.

---

## What MCP Servers Are

An MCP server is a small program that runs alongside Claude and exposes a set of tools Claude can call. When you ask Claude to "check your email" or "create a calendar event", it calls a tool provided by an MCP server. The server handles the actual API call and returns the result to Claude.

From Claude's perspective, MCP tools work just like any built-in capability — it can call `gmail_search_messages`, get a list of emails back, and then call `gmail_create_draft` to draft a reply. Claude does not need to know how the server works; it just knows what tools are available and what they do.

---

## How MCP Servers Connect to Claude Code

MCP servers are configured in a settings file. Claude Code supports two scopes:

- **Global** (`~/.claude/settings.json`) — available in every project on the machine
- **Project-level** (`.claude/settings.json` inside a project folder) — available only when working in that project

Use project-level config when a server is only relevant to a specific project, or when you want different credentials per project. Use global config for servers you use everywhere (filesystem, GitHub, etc.).

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

The Claude in Chrome MCP server (`mcp__Claude_in_Chrome__*`) gives Claude full control of your browser — navigating pages, clicking, filling forms, taking screenshots, reading page content, and extracting data. It is installed via the Claude browser extension (Chrome Web Store) and exposes a rich tool set that goes well beyond passive page reading.

Key tools: `navigate`, `read_page`, `get_page_text`, `find`, `left_click`, `form_input`, `javascript_tool`, `screenshot`, `tabs_create`, `tabs_context`

**When to use Claude in Chrome over other options:**
- The target is a web app with no dedicated MCP and no API
- You need to interact with a page (click, fill, navigate), not just read it
- You want Claude to extract structured data from a live web interface

**Limitation:** Browsers are granted at "read" tier in computer use — if you need to click or type in a browser, use the Claude in Chrome MCP rather than the computer use MCP.

Configure by installing the Claude browser extension from the Chrome Web Store and connecting it in your Claude settings.

---

### Computer Use

The computer use MCP (`mcp__computer-use__*`) gives Claude direct control of your desktop — taking screenshots, moving the mouse, clicking, typing, scrolling, and opening applications. Unlike the Claude in Chrome MCP (which is browser-scoped), computer use works across all native apps.

Key tools: `screenshot`, `left_click`, `type`, `scroll`, `key`, `open_application`, `request_access`

**Access control — tiers by app category:**
- **Browsers** (Chrome, Safari, Firefox…) → read-only; use the Claude in Chrome MCP instead for interaction
- **Terminals and IDEs** (Terminal, VS Code…) → click-only; use the Bash tool for commands
- **All other apps** (Mail, Notes, Maps, Finder, any native desktop app) → full access

**Before using:** call `request_access` with the list of applications you need. The user approves each explicitly.

**When to use computer use:**
- Native desktop apps with no dedicated MCP (e.g. Maps, Photos, System Settings, third-party apps)
- Cross-app workflows that span multiple native applications
- Anything that requires interacting with the screen as a human would

---

**Finding more servers:** The full MCP server catalogue is at [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers). If you're using Claude.ai (the web interface) rather than Claude Code, Claude.ai has a built-in integrations browser where you can discover and enable integrations directly — no `settings.json` required.

---

## Naming Tools in Skills

When writing a skill (see [Guide 03](./03_SKILLS.md)), name the exact MCP tool in the workflow steps. Do not just say "check the calendar" — say `gcal_list_events`. This prevents Claude from improvising a different approach each session.

**Weak (undertriggers consistent behaviour):**
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

Not sure which MCP tools are available in your setup? Ask Claude directly:

> *"What MCP tools do you have access to? List them by server."*

Claude will enumerate the connected servers and their tools. This is useful when writing new skills — you can confirm the exact tool name before writing it into a workflow step.

---

## Credentials and Security

MCP server credentials (API keys, OAuth tokens) live in `settings.json` or in environment variables. A few rules:

- **Never put credentials in CLAUDE.md, skill files, or memory files** — those may be read back in session output. Credentials belong only in `settings.json` under the `env` block, or in a `.env` file loaded by the server.
- **Use read-only tokens where possible.** A Gmail token with read-only access is safer than one with send permission, for any skill that doesn't need to send.
- **Rotate tokens periodically.** A token in a config file is easy to forget. Set a reminder to rotate it every 6–12 months.

For the full credential hygiene treatment — including exposure response procedures, rotation schedules, and what to do if a key leaks — see [Guide 12](./12_SECURITY.md).

---

## Troubleshooting by Server

When an MCP tool fails, the cause is usually one of a handful of known issues per server. Check the table below before deeper investigation.

| Server | Symptom | Likely cause | Fix |
|---|---|---|---|
| **Gmail** | `gmail_search_messages` returns empty | Query syntax wrong or date format mismatch | Use Gmail search syntax: `after:2026/04/01`, not ISO dates. Test the query in Gmail's web search bar first. |
| **Gmail** | Authentication error / 401 | OAuth token expired | Re-authenticate: remove and re-add the server in settings, or re-run the OAuth flow. Tokens typically expire after 7 days of inactivity. |
| **Gmail** | 429 / rate limit error | Too many API calls in a short window | Gmail API allows ~250 quota units/second. Reduce fetch windows, use narrower search queries, or add a 2-second pause between batch reads. |
| **Calendar** | Event creation returns success but event doesn't appear | Wrong calendar ID or insufficient permissions | Check the calendar ID with `list_calendars` first. Ensure the token has write scope, not just read. |
| **GitHub** | 403 Forbidden on a private repo | Token scope too narrow | Generate a new token with `repo` scope (not just `public_repo`). |
| **GitHub** | 403 on issue/PR creation | Token has read-only permissions | Regenerate with `repo` + `write` permissions. |
| **Filesystem** | "Path not in allowed list" error | Requested path not included in server args | Add the directory to the `args` array in `settings.json`. The server only allows access to explicitly listed paths. |
| **Claude in Chrome** | Tools unavailable or timing out | Extension disconnected or Chrome not running | Check that Chrome is open and the Claude extension is active. Restart the extension if needed. |
| **Slack** | Empty channel history | Bot not added to the channel | Invite the bot to the channel with `/invite @your-bot-name` in Slack. |
| **Computer use** | Click/type blocked | App is in a restricted tier (read-only or click-only) | Browsers are read-only, terminals are click-only. Use Claude in Chrome for browser interaction, Bash tool for terminal commands. |

---

## Rate Limits and Backoff

Most MCP servers proxy external APIs that enforce rate limits. Hitting a limit mid-task silently degrades results — a search returns nothing, a batch of reads stops halfway. Know the limits for your most-used servers:

| Server | Limit | Practical impact |
|---|---|---|
| Gmail API | ~250 quota units/second; daily quota varies by account type | Reading 50 emails in rapid succession can hit the per-second limit. Batch in groups of 10 with short pauses. |
| GitHub API | 5,000 requests/hour (authenticated) | Rarely hit in normal use. Watch out when scanning many repos or issues in a loop. |
| Google Calendar | ~500 requests/100 seconds | Fine for personal use. Can be hit by tasks that poll calendars in a tight loop. |
| Slack | Varies by method; typically 1–20 requests/minute for posting | Read operations are more generous. Writing (posting messages) is throttled aggressively. |

**Pattern for skills that use MCP tools:**

Add this to any skill step that calls an external MCP tool:

```markdown
If the tool call fails with a rate limit or timeout error:
  1. Wait 5 seconds and retry once.
  2. If it still fails, log the error and skip this step gracefully.
  3. Do not retry more than once — repeated retries waste tokens and rarely succeed.
```

**Reducing API pressure:**
- Use search filters to narrow results before fetching (e.g., `after:2026/04/01 label:inbox` instead of fetching all mail)
- Fetch only the fields you need (subjects and dates, not full message bodies) when scanning
- Batch related queries into a single broader search rather than many narrow ones

---

## Error Handling Patterns

When an MCP tool fails, there are three valid responses. Choose based on the failure type:

**Retry** — for transient errors (timeouts, rate limits, temporary network issues). Retry once after a short pause. If the retry also fails, fall through to skip or abort.

**Skip gracefully** — for non-critical data that is nice to have but not essential. Log what was skipped and continue. Example: a daily briefing skill that can't fetch calendar events should still deliver the email summary rather than failing entirely.

**Abort with log entry** — for errors that make the rest of the task meaningless. Authentication failures, missing permissions, or a critical data source returning nothing. Log the error clearly and stop.

**Template instruction block** — paste this into any skill that calls MCP tools:

```markdown
## Error handling
- Transient errors (timeout, 429, 5xx): retry once after 5 seconds. If still failing, skip and note in output.
- Auth errors (401, 403): stop immediately. Log: "[tool name] auth failed — check token in settings.json."
- Empty results when data is expected: note in output ("Calendar returned no events for this period — verify calendar ID"). Continue with available data.
- Do not retry more than once. Do not silently swallow errors — always surface what happened.
```

---

## Giving This to Claude

**To audit your current MCP setup:**
> *"What MCP servers do I have configured? List the tools each one exposes and flag any that seem misconfigured."*

**To set up a new server:**
> *"Read 05_MCP_SERVERS.md and help me set up the filesystem MCP server so Claude can read my Documents folder."*

**Faster alternative:** `tasks/setup-mcp.md` audits your current setup and guides you through adding new servers end-to-end without reading the guide first.

**To check what's needed for a skill:**
> *"I want to build a skill that checks my Gmail for action items. Read 05_MCP_SERVERS.md and tell me what MCP server I need and what tools it uses."*
