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

## Common MCP Servers for Personal Assistants

### Filesystem
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

### GitHub
**Package:** `@modelcontextprotocol/server-github`

Gives Claude access to GitHub repositories, issues, and pull requests. Useful for developer assistants.

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

### Gmail and Google Calendar
**Via:** Zapier MCP or a custom Google OAuth server

Google does not currently publish an official MCP server, but there are two approaches:

1. **Zapier MCP** — connects Claude to thousands of apps including Gmail and Google Calendar via Zapier's action system. Configure at [zapier.com/mcp](https://zapier.com/mcp). Simpler to set up; action set is limited.

2. **Custom OAuth server** — build or use a community server that handles Google OAuth directly. More powerful; requires more setup.

Once connected, typical tools include: `gmail_search_messages`, `gmail_read_message`, `gmail_create_draft`, `gcal_list_events`, `gcal_create_event`.

---

### Other useful servers

| Server | What it does | Package / source |
|--------|-------------|-------------------|
| **Brave Search** | Web search | `@modelcontextprotocol/server-brave-search` |
| **Slack** | Read and post messages | `@modelcontextprotocol/server-slack` |
| **PostgreSQL** | Query a database | `@modelcontextprotocol/server-postgres` |
| **Puppeteer** | Browser automation, web scraping | `@modelcontextprotocol/server-puppeteer` |
| **Memory** | Persistent key-value memory across sessions | `@modelcontextprotocol/server-memory` |

Find the full list at [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers).

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
