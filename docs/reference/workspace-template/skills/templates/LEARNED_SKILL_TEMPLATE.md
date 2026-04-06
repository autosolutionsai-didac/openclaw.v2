---
# LEARNED SKILL TEMPLATE
# Copy this file when creating a new skill from experience.
# Save to: skills/learned/<category>/<skill-name>/SKILL.md
#
# All fields in the frontmatter are required for the learning loop to track.
# The agent updates times_used, success_rate, and last_refined automatically.

name: <skill-name-kebab-case>
description: >
  <One-line description for the skill index. Be specific about what problem
  this skill solves, not vague. "Debug Trimble XML import OAuth failures"
  not "Help with API stuff">
category: <problem-class>
source: learned
state: DRAFT
version: 1
created: <YYYY-MM-DD>
last_refined: <YYYY-MM-DD>
last_used: <YYYY-MM-DD>
times_used: 1
success_rate: 100
trigger_patterns:
  - "<natural language description of when to load this skill>"
  - "<alternate trigger — different way to describe the same problem>"
---

# <Skill Name — Human Readable>

## When to Use

<1-2 sentences describing the problem class this skill addresses.
Include specific signals that indicate this skill is relevant.>

## Approach

<Numbered steps — the working approach that succeeded.
Put the most common workflow first. Be concrete, not abstract.>

1. ...
2. ...
3. ...

## Key Decision Points

<Where the approach branches based on context. Use if/then format.>

- If <condition X> → <do Y>
- If <condition A> → <do B instead>

## Pitfalls & Recovery

<Dead ends encountered during the original task, how to recognize them,
and how to recover. This section grows over time as the skill is refined.>

- **Pitfall**: <description of what went wrong>
  - **Signal**: <how you know you've hit this pitfall>
  - **Recovery**: <what to do instead>

## Context Requirements

<What information, access, or setup is needed before this skill can be applied.
Example: "Requires access to the n8n instance and the workflow ID">

## Verification

<How to confirm the task succeeded after following this skill's approach.
Be specific: "Check the API returns 200 with a non-empty body" not just "verify it works">
