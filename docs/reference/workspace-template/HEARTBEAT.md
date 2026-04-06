---
title: "HEARTBEAT.md Template"
summary: "Workspace template for HEARTBEAT.md"
read_when:
  - Bootstrapping a workspace manually
---

# HEARTBEAT.md Template

```markdown
# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
```
<!-- ═══════════════════════════════════════════════════════════════════════════
     LEARNING LOOP MAINTENANCE — AutoSolutions.ai Enhancement
     Add these tasks to your HEARTBEAT.md
     ═══════════════════════════════════════════════════════════════════════════ -->

## Learning Loop Maintenance

### Weekly: Skill Index Rebuild (Sundays)

1. Scan all skills in `skills/learned/` and `skills/` (manual skills)
2. Rebuild `skills/SKILL_INDEX.md` with current stats from each skill's frontmatter
3. Flag skills with `success_rate < 50%` — add note: "⚠️ Needs review"
4. Flag skills with `last_used` older than 60 days — add note: "🕐 Unused"
5. If any skills were flagged, mention in daily log

### Weekly: Memory Compaction (Sundays)

1. Review daily logs from the past 7 days
2. Extract any uncaptured patterns to `MEMORY.md` → "Learned Patterns" section
3. If daily logs older than 30 days exist, summarize key learnings from them to MEMORY.md and archive the originals to `memory/archive/YYYY-MM/`
4. Review USER.md behavioral model — update if new patterns confirmed this week

### Monthly: Skill Health Report (First Monday)

Generate a brief skill health report and deliver to the primary messaging channel:

```
📊 Learning Loop — Monthly Health Report

Skills created this month: N
Skills refined this month: M
Total learned skills: X (Y active, Z deprecated)

Top performers:
  - [skill-name]: Y% success, Z uses
  - [skill-name]: Y% success, Z uses

Needs attention:
  - [skill-name]: low success rate (X%)
  - [skill-name]: unused for 60+ days

Memory stats:
  - Daily logs: N files
  - MEMORY.md size: ~X lines
  - Behavioral model observations: N total
```
