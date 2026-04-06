---
title: "BOOT.md Template"
summary: "Workspace template for BOOT.md"
read_when:
  - Adding a BOOT.md checklist
---

# BOOT.md

Add short, explicit instructions for what OpenClaw should do on startup (enable `hooks.internal.enabled`).
If the task sends a message, use the message tool and then reply with the exact
silent token `NO_REPLY` / `no_reply`.

## Session Startup Ritual

On every session start, perform these steps silently (do not narrate to the user):

### 1. Load Memory Context

- Read `MEMORY.md` — focus on "Open Loops" and "Learned Patterns" sections
- Read today's daily log `memory/YYYY-MM-DD.md` if it exists
- Read yesterday's daily log if today's doesn't exist yet

### 2. Load Skill Index (Progressive Disclosure — Level 0)

- If `skills/SKILL_INDEX.md` exists — read it (names and descriptions only, ~3K tokens)
- If it doesn't exist but `skills/learned/` has content — generate SKILL_INDEX.md by scanning all skill directories
- Do NOT read individual SKILL.md files at this stage

### 3. Check USER.md Behavioral Model

- Read `USER.md` — note communication preferences and behavioral patterns
- Apply these preferences to the current session without mentioning them

### 4. Review Open Loops

- If MEMORY.md has items in "Open Loops" — be ready to reference them if the user asks about ongoing work
- Do NOT proactively bring up open loops unless the user's message relates to one

### 5. Ready

Proceed to handle the user's message. The learning loop (post-task evaluation, skill extraction) runs at the END of tasks, not at startup.
