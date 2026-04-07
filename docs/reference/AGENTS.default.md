---
title: "Default AGENTS.md"
summary: "Default OpenClaw agent instructions and skills roster for the personal assistant setup"
read_when:
  - Starting a new OpenClaw agent session
  - Enabling or auditing default skills
---

# AGENTS.md - OpenClaw Personal Assistant (default)

## First run (recommended)

OpenClaw uses a dedicated workspace directory for the agent. Default: `~/.openclaw/workspace` (configurable via `agents.defaults.workspace`).

1. Create the workspace (if it doesn’t already exist):

```bash
mkdir -p ~/.openclaw/workspace
```

2. Copy the default workspace templates into the workspace:

```bash
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3. Optional: if you want the personal assistant skill roster, replace AGENTS.md with this file:

```bash
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4. Optional: choose a different workspace by setting `agents.defaults.workspace` (supports `~`):

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

## Safety defaults

- Don’t dump directories or secrets into chat.
- Don’t run destructive commands unless explicitly asked.
- Don’t send partial/streaming replies to external messaging surfaces (only final replies).

## Session start (required)

- Read `SOUL.md`, `USER.md`, and today+yesterday in `memory/`.
- Read `MEMORY.md` when present; only fall back to lowercase `memory.md` when `MEMORY.md` is absent.
- Do it before responding.

## Soul (required)

- `SOUL.md` defines identity, tone, and boundaries. Keep it current.
- If you change `SOUL.md`, tell the user.
- You are a fresh instance each session; continuity lives in these files.

## Shared spaces (recommended)

- You’re not the user’s voice; be careful in group chats or public channels.
- Don’t share private data, contact info, or internal notes.

## Memory system (recommended)

- Daily log: `memory/YYYY-MM-DD.md` (create `memory/` if needed).
- Long-term memory: `MEMORY.md` for durable facts, preferences, and decisions.
- Lowercase `memory.md` is legacy fallback only; do not keep both root files on purpose.
- On session start, read today + yesterday + `MEMORY.md` when present, otherwise `memory.md`.
- Capture: decisions, preferences, constraints, open loops.
- Avoid secrets unless explicitly requested.

## Tools & skills

- Tools live in skills; follow each skill’s `SKILL.md` when you need it.
- Keep environment-specific notes in `TOOLS.md` (Notes for Skills).

## Backup tip (recommended)

If you treat this workspace as Clawd’s “memory”, make it a git repo (ideally private) so `AGENTS.md` and your memory files are backed up.

```bash
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optional: add a private remote + push
```

## What OpenClaw Does

- Runs WhatsApp gateway + Pi coding agent so the assistant can read/write chats, fetch context, and run skills via the host Mac.
- macOS app manages permissions (screen recording, notifications, microphone) and exposes the `openclaw` CLI via its bundled binary.
- Direct chats collapse into the agent's `main` session by default; groups stay isolated as `agent:<agentId>:<channel>:group:<id>` (rooms/channels: `agent:<agentId>:<channel>:channel:<id>`); heartbeats keep background tasks alive.

## Core Skills (enable in Settings → Skills)

- **mcporter** — Tool server runtime/CLI for managing external skill backends.
- **Peekaboo** — Fast macOS screenshots with optional AI vision analysis.
- **camsnap** — Capture frames, clips, or motion alerts from RTSP/ONVIF security cams.
- **oracle** — OpenAI-ready agent CLI with session replay and browser control.
- **eightctl** — Control your sleep, from the terminal.
- **imsg** — Send, read, stream iMessage & SMS.
- **wacli** — WhatsApp CLI: sync, search, send.
- **discord** — Discord actions: react, stickers, polls. Use `user:<id>` or `channel:<id>` targets (bare numeric ids are ambiguous).
- **gog** — Google Suite CLI: Gmail, Calendar, Drive, Contacts.
- **spotify-player** — Terminal Spotify client to search/queue/control playback.
- **sag** — ElevenLabs speech with mac-style say UX; streams to speakers by default.
- **Sonos CLI** — Control Sonos speakers (discover/status/playback/volume/grouping) from scripts.
- **blucli** — Play, group, and automate BluOS players from scripts.
- **OpenHue CLI** — Philips Hue lighting control for scenes and automations.
- **OpenAI Whisper** — Local speech-to-text for quick dictation and voicemail transcripts.
- **Gemini CLI** — Google Gemini models from the terminal for fast Q&A.
- **agent-tools** — Utility toolkit for automations and helper scripts.

## Usage Notes

- Prefer the `openclaw` CLI for scripting; mac app handles permissions.
- Run installs from the Skills tab; it hides the button if a binary is already present.
- Keep heartbeats enabled so the assistant can schedule reminders, monitor inboxes, and trigger camera captures.
- Canvas UI runs full-screen with native overlays. Avoid placing critical controls in the top-left/top-right/bottom edges; add explicit gutters in the layout and don’t rely on safe-area insets.
- For browser-driven verification, use `openclaw browser` (tabs/status/screenshot) with the OpenClaw-managed Chrome profile.
- For DOM inspection, use `openclaw browser eval|query|dom|snapshot` (and `--json`/`--out` when you need machine output).
- For interactions, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type require snapshot refs; use `evaluate` for CSS selectors).

<!-- ═══════════════════════════════════════════════════════════════════════════
     SELF-IMPROVING LEARNING LOOP — Quick Reference
     Full procedures: load the `learning-loop-protocol` skill
     ═══════════════════════════════════════════════════════════════════════════ -->

## Learning Loop — Quick Reference

You have a self-improving learning system. This section has the triggers and key rules.
For detailed step-by-step procedures, load the `learning-loop-protocol` skill.

### Post-Task: When to Learn

After any task with **5+ tool calls** that completed **successfully** and was **non-trivial**:

1. Check `skills/SKILL_INDEX.md` for a matching skill
2. If match → **refine** the existing skill (update approach, add pitfalls, bump version)
3. If no match → **create** a new skill from the template at `skills/templates/LEARNED_SKILL_TEMPLATE.md`
4. Log the result in today's structured daily log (`memory/YYYY-MM-DD.md`)

**Don't create skills for**: simple lookups, generic Claude capabilities, one-off tasks, or tasks under 5 tool calls.

### Pre-Task: When to Search

Before any task that looks like 3+ steps:

1. Read `skills/SKILL_INDEX.md` (loaded at session start via BOOT.md — Level 0, ~3K tokens)
2. If a skill matches → load its full SKILL.md (Level 1, max 2 skills per task)
3. Mention which skill you're using: "Using learned pattern: **[skill-name]**"
4. Skills are guidance, not mandates — the user can override any step

### Skill Lifecycle

- **DRAFT** (0-1 uses) → **VALIDATED** (2+ uses, >75% success) → **MATURE** (autoresearch polished, >85% eval)
- **Regression**: MATURE → VALIDATED if success drops below 70%. VALIDATED → DRAFT if below 60%.
- **PARTIAL outcomes** count as 0.5 for success rate (e.g., 6 SUCCESS + 1 PARTIAL + 1 FAIL = 81.25%)

### Skill Safety

Before saving any skill, verify: no literal credentials, no SOUL.md/IDENTITY.md modifications, no data exfiltration, no unguarded destructive commands. Strip violations before saving.

### Daily Log Format

For tasks with 3+ tool calls, use the structured format (see `learning-loop-protocol` skill for template). For simple interactions, a brief one-line entry is fine.

### User Model

USER.md has a Behavioral Model the agent updates over time. Only update on confirmed patterns (2+ observations), not single data points. Keep it factual, max 3-5 bullets per section.

### Context Pressure

If the conversation exceeds ~100K tokens: load max 1 skill, use brief log format, defer skill creation to next session. Never skip daily logging.
