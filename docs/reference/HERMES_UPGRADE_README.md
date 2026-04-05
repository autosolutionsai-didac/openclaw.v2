# OpenClaw Hermes Learning Loop Upgrade

## What This Is

This upgrade adds Hermes Agent's self-improving capabilities to OpenClaw via workspace file modifications. No TypeScript/Node.js core changes required — everything works through the prompt engineering layer (AGENTS.md, SOUL.md, USER.md, HEARTBEAT.md) and new skill infrastructure.

## File Map

### Files to APPEND to (add content at the end of existing file)

| File | What's Added |
|------|-------------|
| `docs/reference/AGENTS.default.md` | Post-Task Learning Protocol, Skill Loading Protocol, Skill Lifecycle, Daily Log Format, User Model Maintenance |
| `docs/reference/templates/AGENTS.md` | Same additions (template version) |
| `docs/reference/templates/SOUL.md` | Learning & Growth identity section |
| `docs/reference/templates/USER.md` | Behavioral Model section |

### Net-New Files (create these)

| File | Purpose |
|------|---------|
| `docs/reference/templates/HEARTBEAT.learning.md` | Learning loop maintenance tasks for Heartbeat |
| `skills/templates/LEARNED_SKILL_TEMPLATE.md` | Template the agent uses when extracting skills from experience |
| `skills/templates/SKILL_INDEX_TEMPLATE.md` | Template for the progressive disclosure skill index |
| `skills/learned/.gitkeep` | Empty directory for auto-extracted skills |

### How to Apply

1. Copy all net-new files into your repo at the paths shown above
2. For APPEND files: open the existing file, paste the content from the corresponding `_APPEND_` file at the bottom
3. Commit with message: `feat: add Hermes-inspired learning loop to workspace templates`
4. When you `openclaw onboard` a new agent or copy templates to a workspace, the learning loop is active

### For Existing Agents

To upgrade an already-running agent workspace (`~/.openclaw/workspace/`):
1. Append the AGENTS additions to your workspace's `AGENTS.md`
2. Append the SOUL additions to your workspace's `SOUL.md`
3. Append the USER additions to your workspace's `USER.md`
4. Copy `HEARTBEAT.learning.md` content into your `HEARTBEAT.md`
5. Create `skills/learned/` directory in the workspace
6. Copy `LEARNED_SKILL_TEMPLATE.md` to `skills/templates/`
7. The agent will auto-generate `skills/SKILL_INDEX.md` on first use
