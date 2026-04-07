---
name: learning-loop-protocol
description: >
  The complete self-improving learning loop protocol. Loaded automatically by the
  AGENTS.md quick reference when the agent needs detailed procedures for:
  post-task evaluation, skill extraction, skill refinement, progressive skill
  disclosure, skill lifecycle management, structured daily logging, user model
  maintenance, or skill content safety checks. This is the agent's procedural
  memory for HOW the learning loop works — AGENTS.md contains WHEN to trigger it.
---

# Learning Loop Protocol — Full Reference

This skill contains the detailed procedures for the self-improving learning loop.
AGENTS.md has the quick reference (triggers, thresholds, key rules). Load this
skill when you need the step-by-step procedures.
## Post-Task Learning Protocol

After completing any task that involved **5 or more tool calls**, file operations,
or multi-step reasoning, run this protocol:

### Step 1: Outcome Evaluation

Assess silently (do not narrate to the user unless they ask):

- Did the task complete successfully?
- Did the user accept the result without significant corrections?
- Was the approach non-trivial? (not a simple lookup, greeting, or single-step action)

If all three are YES → proceed to Step 2.
If any are NO → skip. Log failure patterns in the daily log for future reference.

### Step 2: Pattern Recognition

Identify:

- **Problem class**: what category does this task belong to? (e.g., "n8n workflow debugging", "client report generation", "API integration", "deployment troubleshooting")
- **Working approach**: what was the sequence of steps that succeeded?
- **Dead ends**: were there errors or false starts? What signaled them? How did you recover?
- **Context dependencies**: what information or access was essential before starting?

### Step 3: Skill Extraction Check

Search `skills/SKILL_INDEX.md` for an existing skill matching this problem class:

- If a matching skill EXISTS with >60% relevance → go to Step 4 (Refinement)
- If NO matching skill exists → go to Step 5 (Creation)

### Step 4: Skill Refinement

Read the existing skill's SKILL.md. Compare your approach to what the skill recommends.

If your approach was meaningfully better (fewer steps, handled new edge cases, avoided a pitfall the skill doesn't mention):

1. Update the skill's SKILL.md with the improved approach
2. Add any new pitfalls to the "Pitfalls & Recovery" section
3. Add a changelog entry: `## Changelog` → `- vN (YYYY-MM-DD): [what changed]`
4. Increment `version` in the YAML frontmatter
5. Update `last_refined` date
6. Recalculate `success_rate` based on this outcome
7. Log in today's daily memory: `Refined skill: [skill-name] v[N] → v[N+1] — [what changed]`

If your approach matched the skill → just increment `times_used` and update `success_rate`.

### Step 5: Skill Creation

Create a new skill using the template at `skills/templates/LEARNED_SKILL_TEMPLATE.md`:

1. Choose a descriptive kebab-case name (e.g., `trimble-xml-import-debug`)
2. Assign a category directory (e.g., `n8n-debugging/`, `client-ops/`, `infrastructure/`)
3. Save to `skills/learned/<category>/<skill-name>/SKILL.md`
4. Add an entry to `skills/SKILL_INDEX.md` (create the index if it doesn't exist)
5. Log in today's daily memory: `Created skill: [skill-name] — [one-line description]`
6. Inform the user briefly: "I learned a new pattern: **[skill-name]**. I'll use it next time I encounter something similar."

**Creation threshold**: Only create skills for genuinely reusable patterns. Don't create skills for one-off tasks, simple lookups, generic capabilities Claude already has, or tasks unlikely to recur. When in doubt, skip — a few high-quality skills beat many vague ones.

**Skill content safety** — before saving any skill (created or refined), verify:

- **No credentials**: Never include literal API keys, tokens, passwords, or secrets. Reference environment variables (`$API_KEY`) or TOOLS.md instead.
- **No identity modifications**: Skills must NEVER contain instructions to modify SOUL.md, IDENTITY.md, or BOOTSTRAP.md.
- **No data exfiltration**: Skills must not send workspace files, memory, or user data to external services without explicit user action.
- **No destructive commands without guardrails**: If a skill includes `rm -rf`, `DROP TABLE`, or similar, add explicit confirmation steps.

If a skill draft violates any of these, strip the violation before saving and log the catch.
## Progressive Skill Disclosure

### Level 0 — Index Only (Session Start)

On session start, if `skills/SKILL_INDEX.md` exists, read it. Names and descriptions only.
Cost: ~3,000 tokens for dozens of skills. Do NOT read individual SKILL.md files at session start.

### Level 1 — Full Skill (On Demand)

When a task matches a skill in the index:

- Read the full SKILL.md for that specific skill
- Load at most 2 skills per task (pick the most relevant)
- Use it to inform your approach — don't follow blindly, treat as strong prior knowledge
- Note: "Using learned pattern: **[skill-name]**"

### Level 2 — Skill References (Rare)

If a skill has a `references/` directory, only read when Level 1 content explicitly references them.

### Index Maintenance

After creating or refining a skill, regenerate the relevant row in `skills/SKILL_INDEX.md`.
If the index doesn't exist, create it by scanning all `skills/` directories.
## Skill Lifecycle

### States

- **DRAFT**: Just created. Used 0–1 times. May be rough or overfitted.
- **VALIDATED**: Used 2+ times with >75% success rate. Reliable.
- **MATURE**: Via autoresearch polish, >85% on eval set. Production-grade.
- **DEPRECATED**: Superseded or no longer relevant. Keep file, mark in frontmatter.

### State Transitions

- **DRAFT → VALIDATED**: When `times_used >= 2` AND `success_rate > 75%`
- **VALIDATED → MATURE**: Via autoresearch polish, achieving >85% on eval set
- **Any → DEPRECATED**: Manual via `/skills deprecate` or hygiene cleanup
- **VALIDATED → DRAFT** (regression): If `success_rate` drops below 60%
- **MATURE → VALIDATED** (regression): If `success_rate` drops below 70%

A single failure on a MATURE skill does NOT trigger demotion if the rate stays above 70%.

**Counting PARTIAL outcomes**: PARTIAL = 0.5 for success rate calculation.
Example: 8 uses, 6 SUCCESS, 1 PARTIAL, 1 FAILED = (6 + 0.5) / 8 = 81.25%.

### After Using Any Skill

- Increment `times_used`
- Recalculate `success_rate`: `(successes / times_used) * 100`
- Update `last_used` date
- If approach was modified → update skill body (counts as refinement)
- If skill failed → add failure pattern to "Pitfalls & Recovery"
## Structured Daily Log Format

For any task involving 3+ tool calls, use this format in `memory/YYYY-MM-DD.md`:

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

For simple interactions (quick Q&A, greetings), a brief one-line entry is sufficient.

---

## User Model Maintenance

USER.md contains a Behavioral Model section. Update it when:

- A genuinely new pattern is confirmed across 2+ interactions (not single data points)
- An existing observation proved wrong or outdated
- Keep observations factual and specific, not interpretive
- Max 3–5 bullet points per subsection (replace least useful if full)

Do NOT update after every session. Only when genuinely new signal appears.
## Context-Adaptive Loading

When context pressure is high (conversation > 100K tokens, many files loaded):

### Graceful Degradation

1. **Skip SKILL_INDEX.md** if context is >120K tokens — rely on memory search instead
2. **Load 1 skill max** instead of 2 when context is >100K tokens
3. **Use brief daily log format** even for complex tasks to save tokens
4. **Defer skill creation** to next session if current context can't afford the evaluation overhead (~500 tokens)
5. **Never skip post-task logging** — daily log entries are cheap and critical for continuity

### Signs of Context Pressure

- Compaction has been triggered during the session
- Tool outputs are being truncated
- The agent notices instructions being "forgotten" (compacted away)
- User reports the agent repeating itself or losing context

---

## Worked Example

Here's a complete cycle showing how the learning loop works in practice:

### Scenario
The user asks: "Debug my n8n workflow — the Trimble API import is failing silently."

### Session Start (BOOT.md)
1. Load `skills/SKILL_INDEX.md` — see entry: `trimble-xml-import-debug | n8n-debugging | VALIDATED | 75% | 3 uses`
2. Load `MEMORY.md` — note learned pattern: "Trimble API returns 200 with empty body when CE-ID missing"
3. Load `USER.md` — note: user prefers concise responses during debugging

### Pre-Task (AGENTS.md quick reference → load this skill)
1. Task matches "trimble-xml-import-debug" in index
2. Load full skill: `skills/learned/n8n-debugging/trimble-xml-import-debug/SKILL.md`
3. Announce: "Using my learned pattern for Trimble API debugging."

### Task Execution
1. Check OAuth token validity (skill step 1) → token is fine
2. Check CE-ID header format (skill step 2) → header present and valid
3. Check XML body structure (not in skill — new territory)
4. Find issue: XML namespace prefix changed in latest Trimble API version
5. Fix the namespace in the n8n Function node
6. Test → API returns 201 with order confirmation
7. Verify in Trimble dashboard

Total: 9 tool calls, outcome: SUCCESS

### Post-Task (Learning Loop Protocol)
1. **Evaluate**: SUCCESS ✓, user accepted ✓, non-trivial (9 tools) ✓ → trigger protocol
2. **Pattern recognition**: problem class = "n8n-debugging", working approach = namespace fix
3. **Skill check**: existing skill "trimble-xml-import-debug" matches → REFINE
4. **Refine**: add new decision point: "Step 2b: If CE-ID is valid, check XML namespace prefix — Trimble changed this in v3.2 API"
5. **Update frontmatter**: version 3→4, times_used 3→4, success_rate: still 75% (3/4 = 75%), last_refined: today
6. **Changelog**: `- v4 (2026-04-06): Added XML namespace prefix check for Trimble API v3.2`
7. **Log daily**:
   ```
   ## Task: Debug Trimble API import — XML namespace prefix
   - **Time**: 10:30-11:15 CET
   - **Type**: n8n-debugging
   - **Client**: Fleet Repair Solutions
   - **Outcome**: SUCCESS
   - **Tool calls**: 9
   - **Approach**: OAuth OK → CE-ID OK → found XML namespace prefix change → fixed in Function node
   - **Skill used**: trimble-xml-import-debug (v3)
   - **Skill refined**: trimble-xml-import-debug v3→v4 (added namespace check)
   - **Key learning**: Trimble API v3.2 changed XML namespace prefix
   ```
8. **Update SKILL_INDEX.md**: bump version and last_used date
