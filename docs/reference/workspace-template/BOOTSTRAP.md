---
title: "BOOTSTRAP.md Template"
summary: "First-run interview for new workspaces — seeds memory, user model, and learning loop"
read_when:
  - Bootstrapping a workspace manually
  - Running openclaw onboard for the first time
---

# BOOTSTRAP.md — First-Run Setup Interview

When this workspace is new and IDENTITY.md/SOUL.md are empty or minimal, run this interview.
The goal is to seed MEMORY.md, USER.md, SOUL.md, and IDENTITY.md with enough context
for the learning loop to start compounding immediately instead of cold-starting.

## Phase 1: Identity (→ IDENTITY.md + SOUL.md)

Ask in a natural, conversational flow — not a rigid questionnaire:

1. **Who are you?** — Name, role, what you do day to day
2. **What should I call you?** — Preferred name, formal or casual
3. **What's my role?** — What kind of assistant do you need? (developer tool, executive assistant, research partner, client ops, etc.)
4. **Personality** — How should I communicate? (direct/verbose, formal/casual, proactive/reactive)
5. **Boundaries** — Anything I should never do? Topics to avoid? Channels I shouldn't message on?

Write answers to IDENTITY.md (structured fields) and SOUL.md (personality/boundaries).

## Phase 2: Work Context (→ MEMORY.md)

6. **What are you working on?** — Current projects, clients, engagements. Populate MEMORY.md "Active Projects" section.
7. **What's your tech stack?** — Infrastructure, tools, platforms. Populate MEMORY.md "Environment & Infrastructure" section.
8. **Any recurring tasks?** — Things you do daily/weekly that I should know about. These are early candidates for skill extraction.
9. **Known gotchas?** — Hard-won lessons, things that always trip you up, workarounds for broken tools. Populate MEMORY.md "Learned Patterns & Lessons" section.

## Phase 3: Preferences (→ USER.md)

10. **Timezone and work hours?** — When are you active? Any async preferences?
11. **Communication style?** — How do you like responses? (brief vs detailed, lists vs prose, always show options vs just decide)
12. **Feedback signals?** — What does "ok" mean from you? What does silence mean? How do you say "this is wrong"? Seed the USER.md "Behavioral Model → Feedback Signals" section.

## Phase 4: Learning Loop Orientation

After the interview, explain the learning loop briefly:

> "I have a learning system built in. When I complete complex tasks, I'll evaluate what worked
> and save the approach as a reusable skill. Over time, I'll get faster and more accurate at
> the kinds of tasks you give me regularly.
>
> You can check on this anytime with `/skills list` or `/skills health`.
> I'll also send you a monthly summary of what I've learned."

Then:

1. Create the `skills/SKILL_INDEX.md` file from the template (empty, ready for population)
2. Create the `memory/` directory if it doesn't exist
3. Set up today's first daily log at `memory/YYYY-MM-DD.md`
4. If the user mentioned recurring tasks (question 8), note them as skill candidates in the daily log:
   `Potential skill candidates from onboarding: [list]`

## Phase 5: Confirmation

Summarize what you've set up:

```
✅ Setup complete! Here's what I've configured:

Identity: [name/role from IDENTITY.md]
Personality: [brief summary from SOUL.md]
Projects: [count] active projects loaded
Infrastructure: [key tools/platforms noted]
Patterns: [count] known patterns seeded
Preferences: [brief summary from USER.md]
Learning loop: Active — I'll start building skills from our work together

Anything you want to adjust before we get started?
```
