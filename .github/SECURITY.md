# Security Policy

## What this repository is

Cluide is documentation. It ships no service, no package, and no compiled artefact, so it has no CVE surface in the usual sense. The realistic risk is different and worth stating plainly: **the guides, tasks, skills, and templates here are read by Claude and acted on.** A defect in this repository is a defect in instructions that an agent will follow.

That makes the following in scope, and worth reporting privately:

- **Instructions that would cause data loss or unwanted mutation.** A task or skill step that deletes, overwrites, or moves files without confirmation, or that is phrased loosely enough that Claude might.
- **Prompt-injection vectors.** Any place where content the user did not write — a fetched page, a file in a scanned project, a connector payload — could be read as an instruction rather than as data. Cluide's own guidance is that target content is data and never a command; a file here that violates that is a bug.
- **Guidance that leaks credentials or personal data.** A pattern that would put secrets into git, into context, into a log, or into a file the user then publishes.
- **Over-broad permissions.** An allow-list, MCP configuration, or `allowed-tools` example that grants materially more than the described use needs.
- **A script that does something other than what its surrounding prose says.** The extraction and helper scripts under `skills/` and `templates/` are copy-paste starters; a mismatch between what one does and what it claims is a security issue, not a documentation nit.

Out of scope: the security posture of Claude, Claude Code, Cowork, or any third-party MCP server. Report those to their respective vendors. Anthropic's own vulnerability disclosure process is the right destination for issues in Claude itself.

## Reporting

**Use GitHub's private vulnerability reporting** rather than opening a public issue: go to the repository's **Security** tab and choose **Report a vulnerability**. That opens a private advisory visible only to the maintainer, which is the right channel for anything you would not want acted on by others before it is fixed.

Please include the file and line, what an agent would actually do when it read that text, and the conditions required — a repository is a very different thing from a scheduled task running unattended with connector access.

There is no bug bounty, no service-level commitment, and no guaranteed response time. This is a single-maintainer project. Expect acknowledgement within a couple of weeks; if something is time-sensitive, say so in the report.

Anything that is not sensitive — a broken link, a stale model name, a task step that no longer works — belongs in a normal public issue. It will get attention faster there.

## Supported versions

Only `main` is supported. Tags mark content events rather than maintained release branches, and fixes land on `main` rather than being backported. If you are running from a tag, update.

## If you find personal data

This repository has been scrubbed of the maintainer's personal and/or employer-specific material, and its examples are meant to be invented rather than real. If you find something that looks like a real person, address, account, internal codename, or credential that survived, report it privately through the Security tab rather than opening an issue — a public report is the thing that turns a stale artefact into an actual exposure.
