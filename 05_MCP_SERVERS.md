# MCP Servers: Connecting Claude to Your Tools

> MCP (Model Context Protocol) is how Claude gets access to external tools — Gmail, Calendar, files, GitHub, and more. Without it, Claude can only read and write text. With it, Claude can actually do things on your behalf. This guide explains what MCP servers are, how to set them up, and how to use them in skills.

---

## What MCP Servers Are

An MCP server is a small program that runs alongside Claude and exposes tools Claude can call. When you ask Claude to "check your email" or "create a calendar event", it calls a tool provided by an MCP server. The server handles the actual API call and returns the result.

From Claude's perspective, MCP tools work like built-in capabilities — call `gmail_search_messages`, get a list of emails, then call `gmail_create_draft` to draft a reply. Claude doesn't need to know how the server works; it just knows what tools are available.

---

## How MCP Servers Connect to Claude

Cowork and Claude Code configure MCP servers differently. The JSON shape — a `mcpServers` object with a launch command, args, and optional `env` for credentials — is shared, but where it lives is not. (Note: `settings.json` is *not* where MCP servers go in either product — it holds permissions, hooks, and env, never `mcpServers`.)

### In Cowork (Claude Desktop)

- **Remote connectors** — added through **Settings → Connectors** in the app (the connector directory, or a custom connector pointing at a remote MCP server URL). OAuth is handled in-app. This is the primary mechanism for Gmail, Calendar, Drive, Atlassian, and most SaaS tools.
- **Local servers** — added via **Settings → Developer**, which opens `claude_desktop_config.json` (macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`; Windows: `%APPDATA%\Claude\claude_desktop_config.json`). This file takes the `mcpServers` block shown below. Servers configured here are bridged by the desktop app into Cowork sessions.
- **Desktop extensions** (`.mcpb`) — installable local servers from the Connectors settings page, no JSON editing required.
- **Plugins** — can bundle MCP servers via their own `.mcp.json`.

### In Claude Code

Servers are registered with the `claude mcp add` command, which supports three scopes:

- **local** (default) — stored in `~/.claude.json`, available only in the current project, private to you
- **project** — written to `.mcp.json` at the project root; version-controllable and shared with anyone who clones the repo
- **user** — available to you across all projects on the machine

```bash
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
claude mcp add --transport http github https://api.githubcopilot.com/mcp/   # remote server
claude mcp add --scope project mytool -- npx -y some-mcp-server             # shared via .mcp.json
```

Use project scope when a server is only relevant to one project; use user scope for servers you use everywhere. Inspect with `claude mcp list` or the `/mcp` command in a session.

**Minimal example** (this block lives in `.mcp.json` for Claude Code project scope, or in `claude_desktop_config.json` for Cowork local servers):

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/you/Documents"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

Servers that need credentials take an `env` block alongside `command`/`args` (e.g. `"env": {"MY_API_TOKEN": "..."}`) — check each server's README for the exact variable names.

At startup, each configured server is launched and its tools discovered. You can see which tools are available by asking Claude: *"What tools do you have available?"*

---

## Common MCP Servers

Servers are grouped by context. Most setups need one block from Personal or Business, plus the Universal servers at the bottom.

---

### Personal (Google Workspace)

#### Google Workspace
**Via:** Google's official MCP server

Google publishes an official MCP server covering Gmail, Google Calendar, Google Drive, Docs, and Sheets. Set it up following the Google Workspace MCP documentation, or add it as a custom connector in Claude (Settings → Connectors) — it handles OAuth authentication and exposes the full Workspace API surface. In Cowork, the built-in Gmail/Calendar/Drive connectors are the easiest route.

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
Read channel history, search messages, and post to channels. Useful for assistants that monitor team communication.

The easiest route is the **Slack connector** in Cowork / Claude (Settings → Connectors) — OAuth handled in-app, no JSON. If you need a local server, pick a maintained one from the MCP Registry (see "Finding more servers" below). Avoid the old `@modelcontextprotocol/server-slack` npm package — it has been archived and unmaintained since early 2025.

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
**Via:** GitHub's official MCP server

Access to GitHub repositories, issues, and pull requests. GitHub hosts an official remote server — no local install, OAuth handled on connect:

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

In Cowork, add the same URL as a custom connector (Settings → Connectors). If you need a local server (e.g. for GitHub Enterprise), use GitHub's official `github/github-mcp-server` binary. The old `@modelcontextprotocol/server-github` npm package is archived — don't use it in new setups.

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

**Finding more servers:** The maintained discovery points are the official MCP Registry at [registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) and the reference server repo at [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers). If you're using Claude.ai (the web interface) or Cowork, the built-in connector directory lets you discover and enable integrations directly — no JSON required.

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

MCP server credentials (API keys, OAuth tokens) live in the MCP config file (`claude_desktop_config.json` for Cowork local servers, `.mcp.json` or `~/.claude.json` for Claude Code) or in environment variables. Rules:

- **Never put credentials in CLAUDE.md, skill files, or memory files** — those get read back in session output. Credentials belong only in the server's `env` block in the MCP config, or in a `.env` file loaded by the server.
- **Use read-only tokens where possible.** A read-only Gmail token is safer than one with send permission, for any skill that only reads.
- **Rotate tokens periodically.** Set a reminder to rotate every 6-12 months.

For the full credential hygiene treatment — including exposure response procedures, rotation schedules, and what to do if a key leaks — see [Guide 12](./12_SECURITY.md).

---

## Troubleshooting by Server

When an MCP tool fails, the cause is usually one of a handful of known issues per server. Start with the general diagnostic checklist, then check the per-server sections.

---

### General: Server Not Responding

Run through this checklist for any server that appears dead:

1. **Is the server process running?** Ask Claude: *"What MCP tools do you have available?"* If a server's tools are missing, it never started.
2. **Check config syntax.** A trailing comma or missing quote kills the entire config. Validate the file your server lives in — Cowork: `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool`; Claude Code: `.mcp.json` or run `claude mcp list`.
3. **Check the launch command.** Run the server's `command` + `args` manually in a terminal. If it errors, you'll see the real failure (missing dependency, wrong Node version, etc.).
4. **Node/npx version.** Most MCP servers require Node 18+. Run `node --version`. If outdated, update Node before anything else.
5. **Network.** Servers that use OAuth need internet access at launch to validate tokens. VPN, proxy, or firewall changes can break a previously working server.
6. **Restart.** MCP servers launch once at startup. If you changed config or fixed a dependency, restart the session (Claude Code) or the desktop app (Cowork).

---

### Gmail / Google Workspace

| Symptom | Cause | Fix |
|---|---|---|
| `gmail_search_messages` returns empty | Query syntax wrong or date format mismatch | Use Gmail search syntax: `after:2026/04/01`, not ISO dates. Test the query in Gmail's web search bar first. |
| Authentication error / 401 | OAuth token expired | Re-authenticate via the OAuth flow. Note: if your OAuth app is in Testing status, Google expires refresh tokens after 7 days regardless of activity — publish the app to stop this. |
| 403 "insufficient permissions" | Token missing required scope | Re-run OAuth and ensure `gmail.readonly` (or `gmail.modify` for drafts/send) is granted. |
| 429 / rate limit | Too many API calls in a short window | Reduce fetch windows, narrow queries, add 2-second pauses between batch reads. |
| `gmail_create_draft` fails silently | Token has read-only scope | You need `gmail.compose` or `gmail.modify` scope. Re-authorize. |
| Server starts but tools list is empty | Google Cloud project API not enabled | Go to Google Cloud Console > APIs & Services > enable Gmail API and Calendar API for the project linked to your OAuth client. |

**Diagnostic step:** Run `gmail_get_profile` first. If that works, auth is fine and the problem is in query syntax or scope. If it fails, the token is bad.

---

### Google Calendar

| Symptom | Cause | Fix |
|---|---|---|
| Event creation succeeds but event doesn't appear | Wrong calendar ID | Call `list_calendars` to get the correct ID. The primary calendar ID is usually the user's email address. |
| Events missing from `list_events` | Query window too narrow or wrong timezone | Specify timezone explicitly. Default may differ from your local zone. |
| "Not Found" on event operations | Calendar ID contains special characters not URL-encoded | Use the ID exactly as returned by `list_calendars`, not a display name. |
| Write operations return 403 | Token has read-only scope | Re-authorize with `calendar.events` scope (not just `calendar.readonly`). |

---

### Microsoft 365 / Outlook

| Symptom | Cause | Fix |
|---|---|---|
| 401 on any call | Azure AD token expired | M365 tokens expire after 60–90 minutes. The server should auto-refresh; if it doesn't, restart the server process. |
| `outlook_email_search` returns nothing | Search syntax differs from Gmail | M365 uses OData `$filter` or KQL syntax, not Gmail query strings. Use `subject:meeting` not `subject:(meeting)`. |
| "Insufficient privileges" / 403 | App registration missing required Graph API permission | In Azure Portal > App registrations > API permissions, add the needed delegated or application permission (e.g., `Mail.Read`, `Calendars.ReadWrite`). Admin consent may be required. |
| Tenant mismatch errors | Personal vs. work account confusion | Ensure the OAuth flow targets the correct tenant (common, organizations, or a specific tenant ID). |
| Server starts but only some tools appear | Server version doesn't cover all M365 services | Check you're running the latest server version. Some community servers only cover mail, not calendar or Teams. |

**Diagnostic step:** Call any read-only tool (like `outlook_email_search` with a simple query). If auth works for read but not write, it's a permissions issue, not a token issue.

---

### Atlassian (Jira + Confluence)

| Symptom | Cause | Fix |
|---|---|---|
| "Site not found" or 404 | Wrong site URL in configuration | The site URL must be your Atlassian cloud domain: `https://yourcompany.atlassian.net`. No trailing slash. |
| JQL queries return empty | JQL syntax error treated as zero results | Test your JQL in Jira's issue search first. Common mistake: unquoted strings with spaces. |
| `createJiraIssue` fails with 400 | Missing required field for that project's issue type | Each project/issue-type can have mandatory custom fields. Fetch the create metadata first or check the project's field configuration. |
| 401 after working previously | API token revoked or email changed | Regenerate the token at id.atlassian.com > Security > API tokens. Update the server's `env` block in your MCP config. |
| Confluence page creation fails | Space key wrong or doesn't exist | Space keys are case-sensitive uppercase strings (e.g., `ENG`, not `eng` or `Engineering`). |

---

### Filesystem

| Symptom | Cause | Fix |
|---|---|---|
| "Path not in allowed list" | Requested path not in server args | Add the directory to the `args` array in your MCP config. The server only exposes explicitly listed paths and their children. |
| "Permission denied" | macOS file permissions or TCC restriction | Check Finder > Get Info permissions. On macOS, some folders (Desktop, Documents) require explicit app access in System Settings > Privacy. |
| Symlinks not followed | Server doesn't resolve symlinks by default | Add the symlink's real target path to the allowed list, or use the resolved absolute path in your skill. |
| Large file read hangs or times out | File exceeds server buffer | Avoid reading files >10 MB through MCP. Use the Bash tool or `head`/`tail` for large files. |

---

### Claude in Chrome

| Symptom | Cause | Fix |
|---|---|---|
| Tools unavailable at session start | Extension disconnected or Chrome not running | Open Chrome. Click the Claude extension icon to reconnect. Restart Claude Code after reconnecting. |
| `navigate` times out | Page load takes too long (heavy SPA, auth redirect) | Increase patience; if a page requires login, complete the login via extension tools first, then navigate. |
| `read_page` returns empty or partial content | Page content loaded dynamically after initial render | Wait 2–3 seconds after navigate, or use `javascript_tool` to check for a specific element before reading. |
| "Target closed" error | Tab was closed externally while Claude was using it | Call `tabs_create_mcp` to open a fresh tab and retry. |
| Extension version mismatch | Extension auto-updated, breaking protocol | Update Claude Code to the latest version. If still broken, uninstall and reinstall the extension. |

---

### Computer Use

| Symptom | Cause | Fix |
|---|---|---|
| Click/type blocked with tier error | App is in a restricted tier | Browsers are read-only (use Claude in Chrome). Terminals are click-only (use Bash tool for commands). |
| `request_access` denied | User declined the permission prompt | Ask the user to approve access. Explain which app you need and why. |
| Clicks land in wrong position | Screen resolution or scaling mismatch | Call `screenshot` to verify coordinates visually. On Retina displays, coordinates are in logical (not physical) pixels. |
| `open_application` says app not found | App name doesn't match macOS bundle name | Use the exact name from /Applications (e.g., "Google Chrome" not "Chrome", "Microsoft Teams" not "Teams"). |
| Screenshot shows stale content | Animation or transition in progress | Call `wait` with 1–2 seconds before taking the screenshot. |

---

### Common Misconfigurations

These mistakes cut across servers and cause silent failures:

| Misconfiguration | Effect | Fix |
|---|---|---|
| Tool name in skill doesn't match actual tool | Claude improvises a different approach or errors | Ask *"What MCP tools do you have?"* and copy the exact name into your skill. Tool names change between server versions. |
| Expired OAuth token in MCP config | Server starts but every call returns 401 | Re-run the OAuth flow. Don't manually paste tokens that will expire — use refresh-token-based setups where possible. |
| Wrong `env` variable name | Server launches but can't authenticate | Check the server's README for the exact variable names. `GITHUB_TOKEN` vs `GITHUB_PERSONAL_ACCESS_TOKEN` matters. |
| Credentials in `CLAUDE.md` instead of the MCP config | Keys exposed in session output and potentially git | Move credentials to the server's `env` block or a `.env` file. Add `.env` (and `.mcp.json` if it holds secrets) to `.gitignore`. |
| Server args missing required path/URL | Server starts but scopes are empty | Filesystem needs explicit paths; Atlassian needs the site URL. Check args match the server's expected positional arguments. |

---

## Rate Limits and Backoff

Most MCP servers proxy external APIs with rate limits. Hitting a limit mid-task silently degrades results — a search returns nothing, a batch of reads stops halfway. Key limits:

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

When an MCP tool fails, choose one of three responses based on the failure type:

**Retry** — for transient errors (timeouts, rate limits, 5xx). Retry once after a short pause. If still failing, fall through to skip or abort.

**Skip gracefully** — for non-critical data. Log what was skipped and continue. Example: a daily briefing that can't fetch calendar events should still deliver the email summary.

**Abort with log entry** — for errors that make the rest of the task meaningless (auth failures, missing permissions, critical data source empty). Log clearly and stop.

**Template instruction block** — paste this into any skill that calls MCP tools:

```markdown
## Error handling
- Transient errors (timeout, 429, 5xx): retry once after 5 seconds. If still failing, skip and note in output.
- Auth errors (401, 403): stop immediately. Log: "[tool name] auth failed — check token in the MCP config."
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
