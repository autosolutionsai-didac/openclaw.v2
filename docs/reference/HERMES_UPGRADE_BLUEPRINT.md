# OpenClaw × Hermes: Implementation Blueprint
## Porting the Learning Loop & Multi-Layer Memory into Your OpenClaw Infrastructure

**Author**: AutoSolutions.ai  
**Date**: April 4, 2026  
**Status**: Strategy Document — Ready for Discussion

---

## Executive Summary

This document maps every Hermes Agent advantage to concrete OpenClaw implementation points. The goal isn't to replace OpenClaw — it's to graft Hermes's five killer capabilities onto OpenClaw's existing architecture:

1. **The Closed Learning Loop** (autonomous skill creation from successful tasks)
2. **Multi-Layer Memory** (beyond flat MEMORY.md)
3. **Progressive Skill Disclosure** (token-efficient skill loading)
4. **Skill Refinement** (existing skills get better over time)
5. **User Modeling** (Honcho-style dialectic preferences)

Each section identifies: what changes, which file(s), the implementation approach, and the effort level.

---

## Current OpenClaw Architecture (Baseline)

```
~/.openclaw/workspace/
├── SOUL.md              # Identity, personality, boundaries
├── IDENTITY.md          # Structured name/role/goals
├── AGENTS.md            # Operating rules, procedures, workflows
├── USER.md              # User preferences, timezone, context
├── TOOLS.md             # Environment notes for skills
├── HEARTBEAT.md         # Periodic task definitions
├── MEMORY.md            # Curated long-term memory
├── BOOTSTRAP.md         # First-run interview
├── BOOT.md              # Session startup ritual (optional)
├── memory/              # Daily logs
│   ├── 2026-04-01.md
│   ├── 2026-04-02.md
│   └── ...
└── skills/              # Manually authored SKILL.md files
    ├── some-skill/
    │   └── SKILL.md
    └── ...
```

**Key limitation**: Skills are manually authored. Memory is flat files. No outcome evaluation. No skill extraction. No progressive disclosure. The agent starts every session equally dumb — it never compounds learning.

---

## MODIFICATION 1: The Learning Loop Engine

### What Hermes Does

After completing a complex task (5+ tool calls), Hermes:
1. Evaluates the outcome against the original goal
2. If successful AND non-trivial, extracts the approach as a structured skill
3. Stores it in `~/.hermes/skills/` with YAML frontmatter + markdown
4. On future tasks, searches the skill library BEFORE planning
5. Refines existing skills when it finds better approaches

### How to Implement in OpenClaw

#### A. Modify `AGENTS.md` — Add the Learning Loop Protocol

Add a new section to AGENTS.md that instructs the agent to self-evaluate and extract skills after complex task completions:

```markdown
## Post-Task Learning Protocol

After completing any task that involved 5 or more tool calls, file operations,
or multi-step reasoning:

### Step 1: Outcome Evaluation
Ask yourself:
- Did the task complete successfully?
- Did the user accept the result without significant corrections?
- Was the approach non-trivial (not a simple lookup or single-step action)?

If all three are YES, proceed to Step 2.

### Step 2: Pattern Recognition
Identify:
- What class of problem was this? (e.g., "n8n workflow debugging", "client report generation", "API integration troubleshooting")
- What was the sequence of steps that worked?
- Were there dead ends or errors I recovered from? What was the recovery pattern?
- What context was essential to success?

### Step 3: Skill Extraction Check
Search skills/ for an existing skill that covers this problem class:
- If a matching skill EXISTS → go to Step 4 (Refinement)
- If NO matching skill → go to Step 5 (Creation)

### Step 4: Skill Refinement
Read the existing skill. Compare your approach to what the skill recommends.
If your approach was meaningfully better (fewer steps, handled edge cases, avoided a pitfall):
- Update the skill with the improved approach
- Add the new edge case / pitfall to the skill
- Increment the version in frontmatter
- Log the refinement in memory/YYYY-MM-DD.md

### Step 5: Skill Creation
Create a new skill following the Extracted Skill Template (see below).
- Save to skills/learned/<category>/<skill-name>/SKILL.md
- Log the creation in memory/YYYY-MM-DD.md
- Notify the user: "I learned a new pattern: [skill-name]. I'll use it next time."

### Step 6: Pre-Task Skill Search (EVERY task)
Before starting any non-trivial task:
- Scan skills/learned/ for relevant patterns
- If found, load the skill and use it to inform your approach
- Reference the skill in your planning: "Using learned pattern: [skill-name]"
```

**Effort**: Medium. This is purely prompt engineering — no code changes to OpenClaw core. It goes directly into AGENTS.md.

**Risk**: Token consumption. Every post-task evaluation burns tokens. Mitigate by making the evaluation conditional on complexity thresholds.

#### B. Create the Extracted Skill Template

Add a template file that the agent uses when creating skills from experience:

**File**: `~/.openclaw/workspace/templates/LEARNED_SKILL_TEMPLATE.md`

```markdown
---
name: <skill-name>
description: <one-line description for skill index>
category: <problem-class>
source: learned
version: 1
created: <YYYY-MM-DD>
last_refined: <YYYY-MM-DD>
times_used: 0
success_rate: 100%
trigger_patterns:
  - "<when should this skill be loaded>"
  - "<alternate trigger phrase>"
---

# <Skill Name>

## When to Use
<1-2 sentences describing the problem class this skill addresses>

## Approach
<Numbered steps — the working approach, ordered by most common workflow first>

1. ...
2. ...
3. ...

## Key Decision Points
<Where the approach branches based on context>

- If X → do Y
- If A → do B

## Pitfalls & Recovery
<Dead ends encountered, how to recognize them, how to recover>

- **Pitfall**: <description>
  - **Signal**: <how you know you hit it>
  - **Recovery**: <what to do instead>

## Context Requirements
<What information/access is needed before starting>

## Verification
<How to confirm the task succeeded>
```

**Effort**: Low. Template file only.

#### C. Create the Skill Index System (Progressive Disclosure)

This is the most impactful Hermes feature to port. Instead of loading all skills into context, maintain a lightweight index.

**File**: `~/.openclaw/workspace/skills/SKILL_INDEX.md`

This file is auto-generated by the agent and loaded at session start. It contains ONLY names and descriptions (~3,000 tokens for dozens of skills vs. 50,000+ tokens for full skill contents).

```markdown
# Skill Index
<!-- Auto-generated. Do not edit manually. Agent rebuilds on skill changes. -->
<!-- Last updated: 2026-04-04 -->

## Learned Skills (Auto-Extracted)

| Skill | Category | Description | Uses | Success |
|-------|----------|-------------|------|---------|
| trimble-xml-import-debug | n8n-workflows | Debug Trimble XML Order Import OAuth and CE-ID issues | 3 | 100% |
| netsuite-suiteql-patterns | integrations | SuiteQL query patterns for NetSuite MCP | 5 | 80% |
| frank-body-reporting | client-ops | YOY Mecca sales dashboard generation | 2 | 100% |
| openclaw-config-troubleshoot | agent-config | Fix OpenClaw multi-agent config schema issues | 4 | 75% |
| vps-deployment-hetzner | infrastructure | Deploy services on Hetzner VPS via SSH | 6 | 83% |

## Manual Skills (Pre-Authored)

| Skill | Description |
|-------|-------------|
| n8n-workflow-patterns | Proven architectural patterns for n8n workflows |
| sow-writer | Generate SOW documents in AutoSolutions format |
| ai-transformation-consulting | McKinsey-style AI audit methodology |
| ... | ... |
```

**How it works in practice**:

1. **Session start**: Agent loads SKILL_INDEX.md (Level 0 — names and descriptions only)
2. **Task received**: Agent scans index for relevant skills
3. **Match found**: Agent loads the FULL SKILL.md of matched skill(s) (Level 1)
4. **No match**: Agent proceeds without skill guidance, triggers learning loop post-task

**Implementation in AGENTS.md**:

```markdown
## Skill Loading Protocol (Progressive Disclosure)

### On Session Start
- Read skills/SKILL_INDEX.md — this is your skill library overview
- Do NOT read individual SKILL.md files yet
- The index costs ~3,000 tokens. Individual skills cost 2,000-10,000 each.

### Before Starting Any Task
- Search SKILL_INDEX.md for skills matching the task type
- If a match is found with success_rate > 60%:
  - Read the full SKILL.md for that skill
  - Use it to inform your approach
  - After task completion, update times_used and success_rate in the index

### Index Maintenance
- After creating or refining a skill, regenerate the relevant row in SKILL_INDEX.md
- If the index file doesn't exist, create it by scanning all skills/ directories
```

**Effort**: Medium. Requires discipline in AGENTS.md instructions and the agent reliably following the protocol. No code changes.

---

## MODIFICATION 2: Multi-Layer Memory Architecture

### What Hermes Does

Hermes has FIVE memory layers vs. OpenClaw's two (MEMORY.md + daily logs):

1. **MEMORY.md** — curated environment facts, conventions, lessons
2. **USER.md** — communication preferences, decision patterns, formatting prefs
3. **FTS5 SQLite search** — full-text search over ALL past sessions
4. **Honcho dialectic user modeling** — deepens understanding of user across sessions
5. **ChromaDB episodic memory** — vector store for timestamped task execution records

### How to Implement in OpenClaw

OpenClaw already has MEMORY.md, USER.md, and daily logs. The gaps are: structured search, user modeling, and episodic memory.

#### A. Restructure MEMORY.md into Layered Memory

Replace the flat MEMORY.md with a structured format that separates concerns:

**File**: `~/.openclaw/workspace/MEMORY.md`

```markdown
# Long-Term Memory

## Environment & Infrastructure
<!-- Facts about the technical environment that rarely change -->
- OpenClaw runs on Hetzner VPS (Ubuntu 24, IP: x.x.x.x)
- n8n cloud instance: autosolutions-ai-cloud.app.n8n.cloud
- GitHub org: autosolutionsai-didac
- Primary stack: OpenClaw + n8n + Claude + Hetzner/Hostinger

## Active Clients & Projects
<!-- Current engagements — review weekly -->
- Frank Body: NetSuite integration, PO automation, Mecca dashboard
- Fleet Repair Solutions: Trimble XML Order Import workflow (ID: clTQKBnwjOOgcEN2)
- Finques Teixidor: Barcelona property management, OpenClaw agent + SQLite
- Twist Broadband: Content generation pipeline with AURORA agent

## Learned Patterns & Lessons
<!-- Extracted from successful tasks — the "wisdom" layer -->
- Trimble API: Always check CE-ID header before OAuth token refresh
- n8n Gmail triggers: Fail silently on token expiry — add explicit token check node
- NetSuite SuiteQL: Use savedSearchId when possible, raw queries timeout on large datasets
- Frank Body reports: Always pull YOY data before generating — client expects comparisons

## Conventions & Preferences
<!-- How we work — communication, formatting, tooling choices -->
- Didac prefers concise, actionable outputs — no fluff
- SOWs use AutoSolutions.ai template (see sow-writer skill)
- LinkedIn posts: polished but authentic, avoid corporate buzzwords
- Code: Python for scripts, TypeScript for n8n Code nodes when possible

## Open Loops
<!-- Things started but not finished — check daily -->
- [ ] Fleet Repair: circular JSON error in Trimble workflow not fully resolved
- [ ] Frank Body: NetSuite MCP OAuth role needs production token
- [ ] Executive Pulse: Raspberry Pi voice interface — TTS latency issue
```

**Effort**: Low. Restructure existing content.

#### B. Enhance USER.md with Honcho-Style Dialectic Modeling

Hermes's USER.md goes beyond preferences — it builds a behavioral model that deepens over sessions. Implement this by adding a "behavioral observations" section that the agent updates:

**Additions to USER.md**:

```markdown
## Behavioral Model
<!-- Updated by agent after interactions. Captures HOW the user works, not just what they prefer. -->

### Communication Patterns
- Sends rapid-fire messages when iterating — wait for full context before responding
- Uses voice-to-text frequently — expect autocorrect artifacts (e.g., "Asian" = "Agent")
- When frustrated, messages get shorter — switch to more structured responses
- Prefers to see options before making decisions, but hates long lists

### Decision Patterns
- Makes technology decisions quickly when shown a clear comparison
- Prioritizes "can I ship this to a client this week?" over theoretical elegance
- Will invest in infrastructure if the ROI story is clear
- Delegates implementation details but stays deeply involved in architecture

### Work Rhythms
- Most active Barcelona business hours (9am-7pm CET)
- Evening sessions tend to be more exploratory/strategic
- Maintains US client relationships — sometimes works US hours
- Weekend work is common but focused on personal projects (OpenClaw, Skool community)

### Feedback Signals
- "Perfect" = genuinely satisfied, move on
- "Ok" = acceptable but not excited — could be better
- "Let me think about it" = needs to be convinced, provide more evidence
- No response + new topic = implicitly accepted but low-priority
```

**Implementation in AGENTS.md**:

```markdown
## User Model Maintenance

After every substantive interaction (not simple Q&A):
- Review USER.md behavioral model
- If you observed a new pattern (communication, decision, feedback style):
  - Add it to the appropriate section
  - Keep observations factual, not interpretive
  - Max 3-4 bullet points per section (replace least useful if full)
- If an existing observation proved wrong, update it
- Do NOT update on every session — only when genuinely new signal appears
```

**Effort**: Low-Medium. Prompt engineering + initial USER.md restructuring.

#### C. Session Search Enhancement via Memory Skill

OpenClaw already has `memory_search` (keyword + semantic). Enhance it with a structured search skill that mimics Hermes's FTS5 approach:

**File**: `~/.openclaw/workspace/skills/memory-search-enhanced/SKILL.md`

```markdown
---
name: memory-search-enhanced
description: >
  Enhanced memory search that searches across daily logs, MEMORY.md, skills,
  and session history with structured result ranking. Use before starting any
  task that might benefit from prior context.
---

# Enhanced Memory Search

## Before Any Non-Trivial Task

1. Search memory/ directory for relevant daily logs (last 7 days first, then expand)
2. Search MEMORY.md "Learned Patterns" section for relevant lessons
3. Search skills/SKILL_INDEX.md for applicable skills
4. Search TOOLS.md for environment-specific constraints

## Search Strategy

- Start with specific terms (client name, tool name, error message)
- If no results, broaden to problem class ("OAuth", "XML parsing", "deployment")
- If still no results, check open loops in MEMORY.md
- Combine findings into a brief context summary before starting the task

## Result Ranking

Prioritize in this order:
1. Learned patterns from MEMORY.md (highest signal — these are curated)
2. Matching skills from SKILL_INDEX.md (structured approaches)
3. Recent daily logs (last 3 days — highest recency)
4. Older daily logs (pattern matching, not recency)
```

**Effort**: Low. Skill file only.

#### D. Episodic Memory via Structured Daily Logs

Hermes uses ChromaDB for timestamped task execution records. OpenClaw can approximate this without a vector DB by structuring daily logs as machine-parseable records:

**Enhanced daily log format** (`memory/YYYY-MM-DD.md`):

```markdown
# 2026-04-04

## Task: Debug Trimble XML Import Workflow
- **Time**: 10:30-11:45 CET
- **Type**: n8n-workflow-debugging
- **Client**: Fleet Repair Solutions
- **Outcome**: SUCCESS
- **Tool calls**: 8
- **Approach**: Checked OAuth token → found expired → refreshed → CE-ID header missing → added header node → tested → passed
- **Skill used**: trimble-xml-import-debug (v2)
- **Skill updated**: Yes — added CE-ID header step
- **Key learning**: Trimble API returns 200 with empty body when CE-ID missing (not a proper error)

## Task: Generate Frank Body Weekly Report
- **Time**: 14:00-14:30 CET
- **Type**: client-reporting
- **Client**: Frank Body
- **Outcome**: SUCCESS
- **Tool calls**: 4
- **Approach**: Pulled SuiteQL data → compared YOY → generated markdown → formatted
- **Skill used**: frank-body-reporting (v1)
- **Skill updated**: No
- **Key learning**: None (routine execution)
```

**Implementation in AGENTS.md**:

```markdown
## Daily Log Format (Episodic Memory)

When logging tasks to memory/YYYY-MM-DD.md, use the structured format:

## Task: <descriptive title>
- **Time**: <start-end>
- **Type**: <problem-class>
- **Client**: <if applicable>
- **Outcome**: SUCCESS | PARTIAL | FAILED
- **Tool calls**: <count>
- **Approach**: <one-line summary of what worked>
- **Skill used**: <skill name> (v<version>) | None
- **Skill updated**: Yes | No
- **Key learning**: <one line, or "None" for routine tasks>

This format enables pattern search across days. When searching for how a past task
was completed, search daily logs for the Type or Client fields.
```

**Effort**: Low. Format change in AGENTS.md instructions.

---

## MODIFICATION 3: Skill Lifecycle Management

### What Hermes Does

Skills in Hermes have a lifecycle: creation → usage → refinement → deprecation. The `skill_manage` tool handles CRUD operations with security scanning. Skills track usage stats and get refined when better approaches are discovered.

### How to Implement in OpenClaw

#### A. Add Skill Lifecycle Tracking to AGENTS.md

```markdown
## Skill Lifecycle

### Skill States
- **DRAFT**: Just created from a task. Used 0 times. May be rough.
- **VALIDATED**: Used 2+ times with >75% success. Reliable.
- **MATURE**: Used 5+ times with >80% success. Production-grade.
- **DEPRECATED**: Superseded by a better skill or no longer relevant.

### After Using a Skill
Update the skill's frontmatter:
- Increment `times_used`
- Recalculate `success_rate` based on outcome
- If approach was modified during use, update the skill body
- If the skill failed, add the failure pattern to "Pitfalls & Recovery"
- Update `last_refined` date

### Skill Hygiene (Monthly via Heartbeat)
- Review all learned skills with success_rate < 50% — consider deprecating
- Review all skills not used in 60+ days — still relevant?
- Merge overlapping skills if they cover the same problem class
- Rebuild SKILL_INDEX.md from current skill directories
```

#### B. Directory Structure for Learned vs. Manual Skills

```
~/.openclaw/workspace/
├── skills/
│   ├── SKILL_INDEX.md           # Auto-generated index (Level 0)
│   ├── manual/                  # Pre-authored skills (your existing skills)
│   │   ├── n8n-workflow-patterns/
│   │   ├── sow-writer/
│   │   └── ai-transformation-consulting/
│   └── learned/                 # Auto-extracted by the learning loop
│       ├── n8n-debugging/
│       │   ├── trimble-xml-import-debug/
│       │   │   └── SKILL.md
│       │   └── gmail-trigger-token-fix/
│       │       └── SKILL.md
│       ├── client-ops/
│       │   └── frank-body-reporting/
│       │       └── SKILL.md
│       └── infrastructure/
│           └── vps-deployment-hetzner/
│               └── SKILL.md
```

**Effort**: Low. Directory restructure + AGENTS.md instructions.

---

## MODIFICATION 4: HEARTBEAT.md — Add Learning Loop Maintenance

### Current State

OpenClaw's Heartbeat runs on a timer (default 30min), reads HEARTBEAT.md, and decides whether to act. Currently used for proactive monitoring.

### Enhancement

Add learning loop maintenance tasks to the Heartbeat cycle:

**Additions to HEARTBEAT.md**:

```markdown
## Learning Loop Maintenance (Weekly)

### Skill Index Rebuild
Every Sunday at 9:00 CET:
- Scan all skills in skills/learned/ and skills/manual/
- Rebuild skills/SKILL_INDEX.md with current stats
- Flag skills with success_rate < 50% for review
- Flag skills not used in 60+ days

### Memory Compaction
Every Sunday at 9:30 CET:
- Review daily logs from the past week
- Extract any uncaptured patterns to MEMORY.md "Learned Patterns"
- Archive daily logs older than 30 days to memory/archive/
- Update USER.md behavioral model if new patterns observed

### Skill Health Report
Every Sunday at 10:00 CET:
- Generate a brief report to user:
  - Skills created this week: N
  - Skills refined this week: M
  - Total learned skills: X
  - Highest-performing skill: <name> (Y% success, Z uses)
  - Skills needing attention: <list>
- Deliver via primary messaging channel
```

**Effort**: Low. HEARTBEAT.md additions only.

---

## MODIFICATION 5: SOUL.md — Add Learning Identity

### Current State

SOUL.md defines personality and boundaries. It doesn't reference the learning system.

### Enhancement

Add a section to SOUL.md that makes learning part of the agent's core identity:

```markdown
## Learning & Growth

You are not just a task executor — you are a learning system. Every complex task
is an opportunity to become more capable.

### Core Learning Behaviors
- After completing complex work, always evaluate what you learned
- When you discover a better approach, capture it as a skill
- Before starting work, check if you've solved something similar before
- Track what works and what doesn't — be honest about failures
- Share what you learn with the user ("I noticed a pattern...")

### Learning Boundaries
- Never modify SOUL.md or core identity files based on learned patterns
- Skills are about HOW to do things, not about WHO you are
- If a learned pattern conflicts with SOUL.md boundaries, SOUL.md wins
- Don't over-extract — routine tasks don't need skills
- Quality > quantity: one good skill beats ten vague ones

### Transparency
- When using a learned skill, mention it: "Using my pattern for [X]..."
- When creating a new skill, inform the user
- When a skill fails, acknowledge it and update the skill
- Share your skill health report weekly
```

**Effort**: Low. SOUL.md additions.

---

## MODIFICATION 6: Autoresearch Integration for Skill Self-Improvement

Your existing `autoresearch-loop` skill is a perfect complement to the learning loop. Connect them:

### How They Work Together

```
Learning Loop (runtime):
  Task → Evaluation → Skill Extraction → Storage → Future Retrieval

Autoresearch Loop (batch improvement):
  Skill → Test Prompts → Score → Experiment → Test → Keep/Discard → Repeat
```

The learning loop creates rough skills from experience. The autoresearch loop polishes them into production-grade patterns.

### Implementation

Add to AGENTS.md:

```markdown
## Skill Improvement Pipeline

### Phase 1: Learning Loop (Automatic, Every Session)
- Extract skills from complex task completions
- Skills start as DRAFT with limited testing

### Phase 2: Autoresearch Refinement (On-Demand)
When a learned skill reaches VALIDATED status (2+ uses, >75% success):
- User can trigger: "Run autoresearch on [skill-name]"
- The autoresearch loop takes the skill as its artifact
- Test prompts are generated from the skill's usage history
- The skill is iteratively improved until convergence

### Phase 3: Cross-Skill Learning
After multiple skills in the same category are refined:
- Look for common patterns across skills in the category
- Extract meta-patterns into category-level guidance
- Example: All "n8n-debugging" skills share "check OAuth first" → add to category README
```

**Effort**: Low. Connecting two existing systems via AGENTS.md instructions.

---

## Implementation Priority & Roadmap

### Phase 1: Foundation (This Week) — ~2 hours
1. Restructure MEMORY.md into layered format
2. Enhance USER.md with behavioral model section
3. Create `templates/LEARNED_SKILL_TEMPLATE.md`
4. Create `skills/learned/` directory structure
5. Create initial `skills/SKILL_INDEX.md`

### Phase 2: Learning Loop (Next Week) — ~3 hours
6. Add Post-Task Learning Protocol to AGENTS.md
7. Add Skill Loading Protocol (Progressive Disclosure) to AGENTS.md
8. Add Skill Lifecycle management rules to AGENTS.md
9. Update daily log format for episodic memory
10. Add learning identity section to SOUL.md

### Phase 3: Maintenance & Polish (Week 3) — ~2 hours
11. Add learning loop maintenance to HEARTBEAT.md
12. Create `memory-search-enhanced` skill
13. Connect autoresearch loop for skill refinement
14. Test the full loop with a real client task
15. Tune thresholds (tool call count, success rate cutoffs)

### Phase 4: Advanced (Ongoing)
16. Build a custom OpenClaw plugin for skill_manage equivalent (optional — AGENTS.md instructions may be sufficient)
17. Add vector search over daily logs if keyword search proves insufficient
18. Create a "skill export" format compatible with agentskills.io for cross-agent portability
19. Build a Skool community asset: "OpenClaw Learning Loop Starter Kit"

---

## What We're NOT Doing (And Why)

| Hermes Feature | Skip? | Reason |
|---|---|---|
| ChromaDB vector store | Yes (for now) | OpenClaw's memory_search with keyword + semantic is sufficient. Add vector DB only if search quality proves insufficient. |
| Multiple execution backends (Docker, Modal, SSH) | Yes | OpenClaw's single process + shell access works for your VPS setup. Not a bottleneck. |
| FTS5 SQLite for sessions | Partial | OpenClaw's session storage + memory_search approximates this. Structured daily logs close most of the gap. |
| 400+ model routing | Yes | You're on Claude primarily. OpenClaw supports major providers already. |
| Natural language cron | Partial | HEARTBEAT.md covers this. More sophisticated scheduling can come later. |
| DSPy + GEPA evolutionary optimization | Yes (for now) | Your autoresearch loop covers the same intent. DSPy adds complexity without clear benefit for skill improvement at your scale. |
| Built-in migration tool | N/A | You're enhancing OpenClaw, not migrating away from it. |

---

## Risk Mitigation

**Token bloat**: The learning loop adds evaluation overhead. Mitigate:
- Only trigger on 5+ tool call tasks (match Hermes threshold)
- Progressive disclosure keeps skill loading cheap (~3K tokens for index)
- Set a max of 20 learned skills before mandatory curation

**Skill sprawl**: Too many low-quality skills degrade performance. Mitigate:
- Lifecycle states (DRAFT → VALIDATED → MATURE → DEPRECATED)
- Weekly hygiene via Heartbeat
- Success rate tracking with deprecation threshold (< 50%)

**Context window pressure**: More memory layers = more tokens at session start. Mitigate:
- SKILL_INDEX.md is the only new file loaded at startup (~3K tokens)
- Behavioral model in USER.md adds ~500 tokens
- Structured MEMORY.md may actually be shorter than unstructured version
- Total added context budget: ~4K tokens (well within 150K bootstrapTotalMaxChars)

**Agent compliance**: The learning loop is prompt-engineered, not code-enforced. The agent might skip steps. Mitigate:
- Start with Claude Opus for highest instruction-following reliability
- Review first 10 learned skills manually to calibrate quality
- If compliance is inconsistent, consider a custom OpenClaw plugin (Phase 4)

---

## Next Steps

1. **Review this document together** — identify any modifications or priorities you'd change
2. **Pick one agent to pilot** — suggest starting with your personal AutoSolutions agent or the Executive Pulse agent
3. **Implement Phase 1** — restructure memory + create templates (~2 hours)
4. **Run a real task** through the enhanced system and observe the learning loop
5. **Iterate** — tune thresholds, fix compliance issues, add skills
6. **Package as a community asset** — "OpenClaw Learning Loop Kit" for Skool / ClawHub

---

*This blueprint keeps 100% of your existing OpenClaw infrastructure intact. Every modification is additive — new sections in existing files, new skill directories, new templates. Nothing breaks if you roll back.*
