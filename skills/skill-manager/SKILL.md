---
name: skill-manager
description: >
  Manage the learned skill library: list, inspect, deprecate, merge, rename, and audit skills.
  Use when the user says "list my skills", "show skill health", "deprecate a skill",
  "merge these skills", "what skills do I have", "clean up skills", "skill status",
  or any request to manage, organize, or maintain the learned skill library.
  Also triggers on slash commands: /skills list, /skills health, /skills inspect, /skills deprecate.
---

# Skill Manager

Structured operations for managing the learned skill library. The learning loop creates and
refines skills automatically — this skill handles explicit management operations.

## Commands

### /skills list

Display all skills organized by state and category:

```
📚 Skill Library

MATURE (production-grade):
  ✅ [skill-name] — [description] (X uses, Y% success)

VALIDATED (reliable):
  ✔️ [skill-name] — [description] (X uses, Y% success)

DRAFT (new):
  📝 [skill-name] — [description] (X uses, Y% success)

DEPRECATED:
  ⛔ [skill-name] — [reason] (deprecated YYYY-MM-DD)

Total: X active skills, Y deprecated
```

Implementation: scan `skills/learned/` directories, read each SKILL.md frontmatter.

### /skills health

Generate a health report without waiting for the monthly Heartbeat:

1. Scan all learned skills
2. Report: total count by state, average success rate, most/least used
3. Flag issues: skills with <50% success, skills unused >60 days, overlapping skills
4. Suggest actions: "Consider deprecating X", "Y and Z could be merged"

### /skills inspect [skill-name]

Show full details for a specific skill:

- Frontmatter metadata (state, version, usage stats)
- Full content preview
- Usage history (search daily logs for "Skill used: [name]")
- Refinement history (search daily logs for "Refined skill: [name]")

### /skills deprecate [skill-name]

Deprecate a skill:

1. Read the skill's current frontmatter
2. Set `state: DEPRECATED` and add `deprecated_date` and `deprecated_reason`
3. Move entry to bottom of SKILL_INDEX.md with DEPRECATED state
4. Log in daily memory: "Deprecated skill: [name] — [reason]"
5. Do NOT delete the file — deprecated skills stay for reference

### /skills merge [skill-a] [skill-b]

Merge two overlapping skills into one:

1. Read both skills fully
2. Identify overlapping vs. unique content
3. Create a new merged skill that combines:
   - All approaches from both (deduplicated)
   - All pitfalls from both
   - Combined trigger patterns
   - Higher of the two version numbers + 1
   - Combined usage stats (sum times_used, weighted average success_rate)
4. Deprecate the two originals (reason: "Merged into [new-skill-name]")
5. Update SKILL_INDEX.md
6. Log the merge in daily memory

### /skills rename [old-name] [new-name]

Rename a skill:

1. Create new directory with new name
2. Copy all files
3. Update name in SKILL.md frontmatter
4. Update SKILL_INDEX.md
5. Remove old directory
6. Log the rename

### /skills audit

Run a comprehensive audit:

1. Verify all learned skills have valid frontmatter (required fields present)
2. Check SKILL_INDEX.md matches actual skill directories (no orphans, no missing entries)
3. Verify no skills reference credentials, API keys, or sensitive data in their content
4. Check for skills with contradictory approaches in the same category
5. Report findings with suggested fixes

## Skill State Transitions

Valid transitions:
- DRAFT → VALIDATED (automatic: 2+ uses, >75% success)
- DRAFT → DEPRECATED (manual: via /skills deprecate)
- VALIDATED → MATURE (via autoresearch polish, >85% pass rate on eval set)
- VALIDATED → DRAFT (regression: success rate drops below 60%)
- VALIDATED → DEPRECATED (manual or hygiene cleanup)
- MATURE → DEPRECATED (manual: superseded or no longer relevant)
- DEPRECATED → (no transitions out — create a new skill instead)

## Index Rebuild

After any management operation that changes skill state, names, or counts:

1. Rebuild `skills/SKILL_INDEX.md` from current directory contents
2. Verify all entries match actual files
3. Sort by category, then alphabetically within category

## Error Handling & Edge Cases

- **Skill not found**: If `/skills inspect [name]` can't find the skill, search by partial name and suggest matches. Don't fail silently.
- **Corrupted frontmatter**: If a SKILL.md has invalid YAML frontmatter, flag it in `/skills audit` and offer to rebuild from the markdown body.
- **Merge conflicts**: If merging two skills and both have scripts/ with the same filename, keep both with suffixed names and flag for manual review.
- **Deprecating a skill in active use**: If the skill was used in the last 7 days, warn the user before deprecating: "This skill was used 3 days ago. Still deprecate?"
- **Index out of sync**: If `/skills list` finds skills on disk not in the index, auto-add them. If index references skills that don't exist on disk, remove the stale entries.
- **Empty skill library**: If no learned skills exist yet, `/skills list` should display a helpful message explaining how skills are created, not just an empty table.
