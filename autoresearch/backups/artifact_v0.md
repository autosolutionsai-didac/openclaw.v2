<!-- ═══════════════════════════════════════════════════════════════════════════
     HERMES-INSPIRED LEARNING LOOP — AutoSolutions.ai Enhancement
     Append this entire block to the end of your AGENTS.md
     ═══════════════════════════════════════════════════════════════════════════ -->

## Post-Task Learning Protocol

After completing any task that involved **5 or more tool calls**, file operations,
or multi-step reasoning, run this protocol:

### Step 1: Outcome Evaluation

Assess silently (do not narrate this to the user unless they ask):

- Did the task complete successfully?
- Did the user accept the result without significant corrections?
- Was the approach non-trivial? (not a simple lookup, greeting, or single-step action)

If all three are YES → proceed to Step 2.
If any are NO → skip to Step 6 (pre-task search still applies next time).

### Step 2: Pattern Recognition

Identify:

- **Problem class**: what category does this task belong to? (e.g., "n8n workflow debugging", "client report generation", "API integration", "deployment troubleshooting")
- **Working approach**: what was the sequence of steps that succeeded?
- **Dead ends**: were there errors or false starts? What signaled them? How did you recover?
- **Context dependencies**: what information or access was essential before starting?

### Step 3: Skill Extraction Check

Search `skills/SKILL_INDEX.md` (if it exists) for an existing skill matching this problem class:

- If a matching skill EXISTS with >60% relevance → go to Step 4 (Refinement)
- If NO matching skill exists → go to Step 5 (Creation)

### Step 4: Skill Refinement

Read the existing skill's SKILL.md. Compare your approach to what the skill recommends.

If your approach was meaningfully better (fewer steps, handled new edge cases, avoided a pitfall the skill doesn't mention):

1. Update the skill's SKILL.md with the improved approach
2. Add any new pitfalls to the "Pitfalls & Recovery" section
3. Increment `version` in the YAML frontmatter
4. Update `last_refined` date
5. Recalculate `success_rate` based on this outcome
6. Log in today's daily memory: `Refined skill: [skill-name] v[N] → v[N+1] — [what changed]`

If your approach matched the skill → just increment `times_used` and update `success_rate`.

### Step 5: Skill Creation

Create a new skill using the template at `skills/templates/LEARNED_SKILL_TEMPLATE.md`:

1. Choose a descriptive kebab-case name (e.g., `trimble-xml-import-debug`)
2. Assign a category directory (e.g., `n8n-debugging/`, `client-ops/`, `infrastructure/`)
3. Save to `skills/learned/<category>/<skill-name>/SKILL.md`
4. Add an entry to `skills/SKILL_INDEX.md` (create the index if it doesn't exist)
5. Log in today's daily memory: `Created skill: [skill-name] — [one-line description]`
6. Inform the user briefly: "I learned a new pattern: **[skill-name]**. I'll use it next time I encounter something similar."

**Creation threshold**: Only create skills for genuinely reusable patterns. Don't create skills for one-off tasks, simple lookups, or tasks unlikely to recur. When in doubt, skip creation — a few high-quality skills beat many vague ones.

### Step 6: Pre-Task Skill Search (EVERY non-trivial task)

Before starting any task that looks like it will require 3+ steps:

1. Read `skills/SKILL_INDEX.md` (Level 0 — names and descriptions only, ~3K tokens)
2. If a skill matches the incoming task with reasonable relevance:
   - Read the full `SKILL.md` for that skill (Level 1 — full content)
   - Use it to inform your approach — don't follow blindly, but treat it as strong prior knowledge
   - Note which skill you're using: "Using learned pattern: **[skill-name]**"
3. If no skill matches → proceed normally, and evaluate for skill extraction post-task

---

## Skill Loading Protocol (Progressive Disclosure)

Skills consume tokens. Load them efficiently.

### Level 0 — Index Only (Session Start)

On session start, if `skills/SKILL_INDEX.md` exists, read it. This is your skill library overview.
The index contains only names, categories, descriptions, usage counts, and success rates.
Cost: ~3,000 tokens for dozens of skills. Do NOT read individual SKILL.md files at session start.

### Level 1 — Full Skill (On Demand)

When a task matches a skill in the index:

- Read the full SKILL.md for that specific skill
- Cost: 2,000–10,000 tokens per skill
- Load at most 2 skills per task (pick the most relevant)

### Level 2 — Skill References (Rare)

If a skill has a `references/` directory with additional docs:

- Only read these if the Level 1 content explicitly references them
- This is for complex skills with supplementary material

### Index Maintenance

After creating or refining a skill:

- Regenerate the relevant row in `skills/SKILL_INDEX.md`
- If the index doesn't exist, create it by scanning all `skills/` directories
- Keep the index sorted by category, then alphabetically within category

---

## Skill Lifecycle Management

### Skill States

- **DRAFT**: Just created from a single task. Used 0–1 times. May be rough or overfitted.
- **VALIDATED**: Used 2+ times with >75% success rate. Considered reliable.
- **MATURE**: Used 5+ times with >80% success rate. Production-grade knowledge.
- **DEPRECATED**: Superseded by a better skill, or no longer relevant. Keep file but mark in frontmatter.

### After Using Any Skill

Update the skill's YAML frontmatter:

- Increment `times_used`
- Recalculate `success_rate`: `(successes / times_used) * 100`
- Update `last_used` date
- If the approach was modified during use, update the skill body (this counts as a refinement)
- If the skill's approach failed, add the failure pattern to "Pitfalls & Recovery"

### Skill Hygiene (via Heartbeat — Monthly)

During the monthly learning maintenance heartbeat:

- Review all learned skills with `success_rate < 50%` → deprecate or rewrite
- Review all skills not used in 60+ days → still relevant? Deprecate if not.
- Merge overlapping skills that cover the same problem class
- Rebuild `skills/SKILL_INDEX.md` from current skill directories
- Report skill health to user (see HEARTBEAT.md learning section)

---

## Structured Daily Log Format (Episodic Memory)

When logging tasks to `memory/YYYY-MM-DD.md`, use this structured format for any non-trivial task:

```markdown
## Task: <descriptive title>
- **Time**: <HH:MM start – HH:MM end, timezone>
- **Type**: <problem-class matching skill categories>
- **Client**: <client name, or "Internal" / "Personal">
- **Outcome**: SUCCESS | PARTIAL | FAILED
- **Tool calls**: <count>
- **Approach**: <one-line summary of what worked>
- **Skill used**: <skill-name> (v<version>) | None
- **Skill created**: <new-skill-name> | No
- **Skill refined**: <skill-name> v<old>→v<new> | No
- **Key learning**: <one line, or "None — routine execution">
```

This format enables pattern search across days. When searching for how a past problem was solved, search daily logs by the **Type** or **Client** fields.

For simple interactions (quick Q&A, greetings, status checks), a brief one-line entry is sufficient — no need for the full structured format.

---

## User Model Maintenance

The USER.md file contains a Behavioral Model section that captures how the user works, communicates, and makes decisions. This model improves the agent's effectiveness over time.

### When to Update

After substantive interactions (not simple Q&A), review the behavioral model:

- If you observed a genuinely new pattern in communication, decision-making, or work style → add it
- If an existing observation proved wrong or outdated → update it
- Keep observations factual and specific, not interpretive
- Max 3–5 bullet points per subsection (replace least useful if full)

### When NOT to Update

- After every single session (too noisy)
- Based on a single data point (wait for confirmation across 2+ interactions)
- With interpretive or judgmental observations ("user is impatient" → instead: "shorter messages during iteration suggest preference for faster back-and-forth")
