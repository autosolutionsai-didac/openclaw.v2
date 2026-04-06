---
name: learning-diagnostics
description: >
  Diagnose and debug the learning loop itself. Shows skill counts, success rates,
  memory health, behavioral model completeness, and learning velocity.
  Use when the user asks "learning status", "how's the learning loop", "am I learning",
  "skill stats", "diagnose learning", "learning health", or "/learning status".
  Also use when the learning loop seems to not be working (no skills created after
  many sessions, skills not being used, memory not updating).
---

# Learning Loop Diagnostics

Debug and monitor the self-improving learning system. Think of this as `openclaw doctor`
but for the learning loop.

## Quick Status: /learning status

Generate a compact dashboard:

```
🧠 Learning Loop Status

Skills:
  Total: X learned (Y manual)
  By state: Z MATURE | A VALIDATED | B DRAFT | C DEPRECATED
  Avg success rate: X%
  Last created: [skill-name] (YYYY-MM-DD)
  Last refined: [skill-name] (YYYY-MM-DD)

Memory:
  MEMORY.md: X lines (Y sections populated / Z total)
  Daily logs: N files (oldest: YYYY-MM-DD, newest: YYYY-MM-DD)
  Open loops: N items

User Model:
  Sections populated: X/4 (communication, decisions, rhythms, feedback)
  Total observations: N

Learning Velocity:
  Skills created (last 7 days): N
  Skills refined (last 7 days): M
  Skills used (last 7 days): K
  Tasks logged (last 7 days): T

Health: ✅ Healthy | ⚠️ [issues] | 🔴 [critical issues]
```

### How to Gather This Data

1. **Skills**: scan `skills/learned/` directories, read each SKILL.md frontmatter
2. **Memory**: `wc -l MEMORY.md`, count files in `memory/`, read Open Loops section
3. **User Model**: read USER.md Behavioral Model section, count non-placeholder entries
4. **Learning Velocity**: search last 7 days of daily logs for "Created skill:", "Refined skill:", "Skill used:", and structured task entries

## Deep Diagnostics: /learning diagnose

Run when the learning loop isn't working as expected. Checks each component:

### Check 1: Skill Creation Pipeline

Is the agent actually creating skills?

- Search last 14 days of daily logs for "Created skill:" entries
- If zero: the learning loop post-task protocol may not be triggering
- Common causes:
  - Tasks are too simple (< 5 tool calls) — threshold not met
  - AGENTS.md learning protocol section is missing or truncated (check /context list)
  - Agent is hitting context window limits and the learning protocol gets compacted away

**Fix suggestions:**
- Lower the tool call threshold temporarily (5 → 3) to generate more skills during ramp-up
- Verify AGENTS.md contains the "Post-Task Learning Protocol" section
- Check that bootstrapTotalMaxChars isn't truncating AGENTS.md

### Check 2: Skill Retrieval Pipeline

Is the agent using existing skills?

- Search last 14 days of daily logs for "Skill used:" or "Using learned pattern:" entries
- If zero but skills exist: the pre-task search isn't running
- Common causes:
  - SKILL_INDEX.md doesn't exist or is empty
  - BOOT.md startup ritual isn't loading the index
  - Skill descriptions don't match actual task patterns

**Fix suggestions:**
- Rebuild SKILL_INDEX.md manually: scan all skills, regenerate
- Verify BOOT.md contains the startup ritual
- Review skill trigger_patterns — are they specific enough?

### Check 3: Memory Health

Is memory being maintained?

- Check if daily logs are being created (should have one for each active day)
- Check if logs use the structured format (Type, Outcome, Skill used fields)
- Check MEMORY.md: is "Learned Patterns" section growing?
- Check if memory compaction is running (search for compaction log entries)

**Fix suggestions:**
- If logs exist but aren't structured → AGENTS.md daily log format section may be missing
- If MEMORY.md isn't growing → Heartbeat learning maintenance may not be running
- Verify Heartbeat is enabled and HEARTBEAT.md has the learning maintenance section

### Check 4: User Model Health

Is the behavioral model developing?

- Read USER.md Behavioral Model section
- Count non-placeholder observations across all 4 subsections
- If all still say "No patterns observed yet" after 10+ sessions → model isn't updating

**Fix suggestions:**
- Verify AGENTS.md has the "User Model Maintenance" section
- The model updates after "substantive interactions" — if most sessions are quick Q&A, it may legitimately have little to observe
- Manually seed 1-2 observations to demonstrate the format

### Check 5: Skill Quality

Are skills actually useful?

- List all skills with success_rate < 60%
- List all skills used 3+ times (getting real-world signal)
- Check for duplicate/overlapping skills in the same category
- Check for skills with empty or vague content (< 10 lines of actual instructions)

**Fix suggestions:**
- Low success rate skills: either refine (add pitfalls, fix approach) or deprecate
- Overlapping skills: merge via /skills merge
- Vague skills: run autoresearch polish to add concrete examples and decision points

## Troubleshooting Common Issues

### "No skills are being created"

Most common cause: the learning protocol in AGENTS.md gets compacted out of context
during long sessions. Verify with `/context list` — check that AGENTS.md is fully loaded.

If AGENTS.md is truncated, the solution is to reduce other context pressure:
- Keep MEMORY.md shorter (under 150 lines)
- Remove unused TOOLS.md sections
- Consider moving verbose skill content to references/ subdirectories

### "Skills exist but are never used"

The pre-task skill search depends on SKILL_INDEX.md being loaded at session start.
Check BOOT.md is enabled (`hooks.internal.enabled: true`) and contains the index load step.

Also check: are skill descriptions generic enough to match real tasks? A skill described
as "Fix the Trimble XML import CE-ID header error" won't match "help me debug an n8n workflow".
Better: "Debug Trimble API integration issues including OAuth, CE-ID headers, and XML format errors".

### "Learning loop was working but stopped"

Usually caused by a config change, workspace file edit, or OpenClaw update that
altered file loading behavior. Run `/learning diagnose` to identify which component broke.

### "Token costs seem high"

The learning loop adds overhead: post-task evaluation (~500 tokens), skill index at session
start (~3K tokens), full skill load on match (~2-10K tokens per skill). Total overhead is
typically 5-15K tokens per session — small relative to conversation context but measurable.

If costs are a concern:
- Keep SKILL_INDEX.md lean (max 30 rows)
- Set skill creation threshold higher (7+ tool calls instead of 5)
- Limit to 1 full skill load per task instead of 2
- Run memory compaction more frequently to keep MEMORY.md small
