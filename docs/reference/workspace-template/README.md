# OpenClaw Golden Workspace — Learning Loop Edition

This is a complete, pre-configured workspace template with the Hermes-inspired
self-improving learning loop built in. Copy this directory to create a new agent
workspace that learns from experience from day one.

## Quick Setup

```bash
# For a new agent workspace:
cp -r docs/reference/workspace-template/ ~/.openclaw/workspace/

# For a named agent:
cp -r docs/reference/workspace-template/ ~/.openclaw/workspace-<agent-name>/
```

Then update `IDENTITY.md` and `SOUL.md` with the agent's specific identity, and
`USER.md` with your preferences.

## What's Included

### Core Identity & Behavior
- **SOUL.md** — Agent personality + Learning & Growth identity
- **IDENTITY.md** — Structured name/role/goals
- **AGENTS.md** — Operating rules + Post-Task Learning Protocol + Progressive Skill Disclosure + Skill Lifecycle Management + Episodic Daily Logs + User Model Maintenance
- **USER.md** — User preferences + Behavioral Model (auto-populated over time)
- **TOOLS.md** — Environment-specific notes

### Learning Loop Infrastructure
- **BOOT.md** — Session startup ritual (loads skill index, memory, user model)
- **HEARTBEAT.md** — Periodic learning maintenance (weekly skill rebuild, memory compaction, monthly health reports)
- **MEMORY.md** — Layered memory structure (environment, projects, patterns, conventions, open loops)
- **skills/templates/LEARNED_SKILL_TEMPLATE.md** — Template for auto-extracted skills
- **skills/templates/SKILL_INDEX_TEMPLATE.md** — Progressive disclosure index (Level 0)
- **skills/learned/** — Directory for auto-extracted skills (populated by the agent)

### Memory
- **memory/** — Daily logs directory (agent creates files as `YYYY-MM-DD.md`)

## How the Learning Loop Works

1. **Session start** (BOOT.md): Agent loads skill index + memory + user model
2. **Pre-task** (AGENTS.md): Agent searches skill index for matching patterns
3. **Task execution**: Agent works normally, using any matched skills as guidance
4. **Post-task** (AGENTS.md): If 5+ tool calls → evaluate outcome → extract/refine skill
5. **Weekly** (HEARTBEAT.md): Rebuild skill index, compact memory, review behavioral model
6. **Monthly** (HEARTBEAT.md): Generate skill health report

## Enabling Boot Hooks

For BOOT.md to run automatically, enable internal hooks in your openclaw config:

```json
{
  "hooks": {
    "internal": {
      "enabled": true
    }
  }
}
```

## Customizing for a Specific Agent

1. Edit `SOUL.md` — set the agent's personality, boundaries, and role
2. Edit `IDENTITY.md` — set name, role label, goals
3. Edit `USER.md` — fill in your timezone, preferences, work context
4. Edit `TOOLS.md` — add environment-specific notes (servers, APIs, paths)
5. Edit `MEMORY.md` — seed with relevant infrastructure and project context
6. Optionally pre-seed `skills/learned/` with known patterns (see HERMES_UPGRADE_BLUEPRINT.md)

## Requirements

- OpenClaw v2026.3+ (workspace skills support)
- `hooks.internal.enabled: true` in config (for BOOT.md startup ritual)
- Heartbeat enabled (for learning maintenance tasks)
