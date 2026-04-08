# About

- Name: [YOUR_NAME]
- Role: [YOUR_ROLE]
- Timezone: [YOUR_TIMEZONE]
- Language: [PREFERRED_LANGUAGE — e.g. "English responses always"]

# Context

[2–4 lines describing the scope of this project: what domain, what goals, what Claude helps with here. Be specific.]

# Communication Style

- [Style preference 1 — e.g. "Direct and practical, no filler"]
- [Style preference 2 — e.g. "Prose for conversational replies, lists only when content is genuinely list-like"]
- [Style preference 3 — e.g. "No emojis unless asked"]

# Critical Rules

- [Hard constraint 1 — e.g. "Never take external actions (send messages, create records) without explicit confirmation"]
- [Hard constraint 2]
- [Add only rules that override default behavior — don't list things Claude would do anyway]

# Knowledge Files

The assistant maintains structured files in this folder. Read the relevant files before answering questions or starting tasks — do not rely on conversation context alone.

## File Map

| File | What it contains |
|------|-----------------|
| `Profile/PROFILE_SUMMARY.md` | Compact digest: who I am, active priorities, key contacts. **Read first for any task.** |
| `Profile/PROFILE_detail.md` | Full detail: people, projects, patterns, history |
| `Knowledge/INDEX.md` | Index of all topic knowledge files |
| `Knowledge/[TOPIC].md` | Per-topic file: key facts, decisions, current status, open questions |

*Add rows as new files are created. Remove rows for files that no longer exist.*

## Common Lookup Patterns

- **"What's the status of [project/topic]?"** → Read `Knowledge/INDEX.md`, then the relevant `Knowledge/[TOPIC].md`
- **"Who is [person]?"** → Read `Profile/PROFILE_detail.md`
- **"What are the open action items?"** → Read `Profile/PROFILE_SUMMARY.md` (open items section)
- **General context** → Always start with `Profile/PROFILE_SUMMARY.md`
