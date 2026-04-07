# MCP Servers: Connecting Claude to Your Tools

> MCP (Model Context Protocol) is how Claude gets access to external tools — Gmail, Calendar, files, GitHub, and more. Without it, Claude can only read and write text. With it, Claude can actually do things on your behalf. This guide explains what MCP servers are, how to set them up, and how to use them in skills.

---

## What MCP Servers Are

An MCP server is a small program that runs alongside Claude and exposes a set of tools Claude can call. When you ask Claude to "check your email" or "create a calendar event", it calls a tool provided by an MCP server. The server handles the actual API call and returns the result to Claude.

From Claude's perspective, MCP tools work just like any built-in capability — it can call `gmail_search_messages`, get a list of emails back, and then call `gmail_create_draft` to draft a reply. Claude does not need to know how the server works; it just knows what tools are available and what they do.

---

## How MCP Servers Connect to Claude Code

MCP servers are configured in Claude Code's settings file at `~/.claude/settings.json`. Each server has a name, a launch command, and optionally environment variables for credentials.

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

The Claude browser extension (available from the Chrome Web Store) lets Claude read the content of the current webpage in any Claude.ai session. This is not an MCP server — it runs in the browser — but it fills a similar gap: getting live web content into Claude without a separate API or scraping script. Useful for research tasks, reading paywalled articles, or extracting data from web apps that have no API.

---

Find the full server catalogue at [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers).

---

## Naming Tools in Skills

When writing a skill (see [Guide 02](./02_SKILLS.md)), name the exact MCP tool in the workflow steps. Do not just say "check the calendar" — say `gcal_list_events`. This prevents Claude from improvising a different approach each session.

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

---

## Giving This to Claude

**To audit your current MCP setup:**
> *"What MCP servers do I have configured? List the tools each one exposes and flag any that seem misconfigured."*

**To set up a new server:**
> *"Read 08_MCP_SERVERS.md and help me set up the filesystem MCP server so Claude can read my Documents folder."*

**To check what's needed for a skill:**
> *"I want to build a skill that checks my Gmail for action items. Read 08_MCP_SERVERS.md and tell me what MCP server I need and what tools it uses."*
