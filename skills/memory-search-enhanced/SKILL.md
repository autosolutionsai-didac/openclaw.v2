---
name: memory-search-enhanced
description: >
  Structured memory retrieval across daily logs, MEMORY.md, skill index, and TOOLS.md.
  Use before starting any non-trivial task that might benefit from prior context, past
  approaches, or learned patterns. Also use when the user asks "have we done this before",
  "what did we try last time", "how did we fix that", or references a past task.
---

# Enhanced Memory Search

Structured retrieval that searches all memory layers before starting work.
Prevents re-inventing approaches that already exist as learned skills or logged patterns.

## When to Use

- Before any task that looks like it could match a prior pattern
- When the user references past work ("that thing we did", "last time", "the Trimble fix")
- When encountering an error that might have been solved before
- When starting work for a client you've worked with before

## Search Protocol

### Step 1: Skill Index Search (fastest, highest signal)

Search `skills/SKILL_INDEX.md` for skills matching the task type.

- Match by problem class (e.g., "n8n debugging", "deployment", "API integration")
- Match by client name if applicable
- Match by technology (e.g., "OAuth", "XML", "NetSuite")
- If match found with success_rate > 60% → load full SKILL.md (Level 1)

### Step 2: MEMORY.md Learned Patterns

Search the "Learned Patterns & Lessons" section of MEMORY.md.

- These are high-level insights, not full procedures
- Look for relevant one-liners that might prevent common mistakes
- Example: "Trimble API returns 200 with empty body when CE-ID missing"

### Step 3: Daily Log Search (recent context)

Use `memory_search` to search across daily logs:

- Start with the last 7 days (highest recency relevance)
- Search by task Type field, client name, or error message
- If no results in 7 days, expand to 30 days
- Look for structured task entries with matching problem class

### Step 4: TOOLS.md Environment Check

Check TOOLS.md for environment-specific constraints relevant to the task.

- Host quirks, path conventions, risky commands
- API endpoint URLs, credential locations
- Platform-specific notes

## Search Strategy Tips

- **Specific first**: search for exact terms (client name, tool name, error message)
- **Broaden if needed**: fall back to problem class ("OAuth", "XML parsing", "deployment")
- **Combine findings**: synthesize a brief context summary before starting the task
- **Don't over-search**: if the task is clearly novel, skip to execution and let the learning loop capture it afterward

## Output

After searching, produce a brief internal context summary (do not narrate the full search to the user):

```
Context loaded:
- Skill: [skill-name] v[N] (if applicable)
- Relevant pattern: [one-line from MEMORY.md] (if applicable)
- Prior approach: [from daily log] (if applicable)
- Environment note: [from TOOLS.md] (if applicable)
```

Then proceed with the task, informed by this context.
