
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
