---
name: skill-autoresearch-polish
description: >
  Connect the learning loop to the autoresearch methodology for iterative skill improvement.
  Use when a learned skill reaches VALIDATED status (2+ uses, >75% success) and the user wants
  to polish it to production-grade quality. Also use when the user says "improve this skill",
  "run autoresearch on a skill", "polish my learned skills", or "make this skill better".
  This skill bridges auto-extracted skills with the autoresearch loop for systematic refinement.
---

# Skill Autoresearch Polish

Bridge between the learning loop (runtime skill extraction) and the autoresearch loop (batch skill improvement). The learning loop creates rough skills from experience. This skill polishes them into production-grade patterns.

## The Skill Improvement Pipeline

```
Phase 1: Learning Loop (automatic, every session)
  Task → Evaluation → Skill Extraction → DRAFT skill stored

Phase 2: Autoresearch Polish (on-demand, this skill)
  DRAFT/VALIDATED skill → Test prompts → Score → Experiment → Keep/Discard → Repeat
  Result: MATURE skill with high success rate

Phase 3: Cross-Skill Learning (periodic)
  Multiple MATURE skills in same category → Extract meta-patterns → Category guidance
```

## When to Trigger

- A learned skill reaches **VALIDATED** status (2+ uses, >75% success rate)
- The user explicitly asks to improve a learned skill
- A skill's success rate drops below 70% after being VALIDATED (regression)
- Multiple skills in the same category exist and could be consolidated

## How to Run

### Step 1: Select the Skill

Pick the skill to polish. Good candidates:
- VALIDATED skills with the most `times_used` (highest impact)
- Skills with success rate between 60-80% (most room for improvement)
- Skills the user relies on frequently

### Step 2: Generate Test Prompts from Usage History

Search daily logs for every task that used this skill (search by skill name in "Skill used" field).

Extract real scenarios as test prompts:
- The original task description becomes the test prompt
- The outcome (SUCCESS/PARTIAL/FAILED) becomes expected behavior
- Any pitfalls encountered become edge case tests

Target: 5-10 test prompts for the eval set. Include:
- 3-4 happy path scenarios (tasks where the skill worked well)
- 2-3 edge cases (tasks where the skill needed adaptation)
- 1-2 adversarial cases (tasks where the skill might fail)

### Step 3: Run the Autoresearch Loop

Set up the autoresearch loop with:

- **Artifact**: the skill's SKILL.md file
- **Metric**: pass rate on test prompts (0-100%)
  - A "pass" means: Claude, given only the skill, produces the correct approach for the test prompt
- **Budget**: run each test prompt through Claude with the skill loaded, score pass/fail
- **Fixed files**: the test prompts (eval set) do not change during the loop

Run experiments:
1. **Baseline**: score the current skill against all test prompts
2. **Add concrete examples**: include real tool call sequences from successful executions
3. **Strengthen decision points**: add if/then branches for edge cases found in logs
4. **Add pitfalls from failures**: document what went wrong and recovery steps
5. **Tighten trigger patterns**: make the skill description more specific about when to load
6. **Remove redundancy**: cut anything Claude already knows (the skill should add knowledge, not repeat training data)

### Step 4: Graduation

When the skill reaches >85% pass rate on the eval set:

1. Update the skill's state to **MATURE** in the frontmatter
2. Increment the version number
3. Update `skills/SKILL_INDEX.md` with the new stats
4. Log: "Polished skill: [name] — graduated to MATURE (X% → Y% pass rate)"

### Step 5: Cross-Skill Learning (When 3+ Skills Share a Category)

After polishing multiple skills in the same category:

1. Review all MATURE skills in that category
2. Identify common patterns across them (e.g., "always check OAuth token first" appears in 3 different n8n debugging skills)
3. Extract meta-patterns into a category-level README at `skills/learned/<category>/README.md`
4. Keep individual skills for specific procedures; the README captures shared wisdom
5. Future skill creation in this category should reference the README

Example category README:
```markdown
# n8n Debugging — Shared Patterns

Common patterns observed across all n8n debugging skills:

1. Always check OAuth token validity before investigating other errors
2. Gmail triggers fail silently on token expiry — add explicit token check
3. Use $executionId (not $guid) for unique identifiers in expressions
4. CloudEvents API requires proper GUID format for ce-id header
5. Circular JSON errors usually mean a node is referencing its own output
```

## Integration with Existing Autoresearch Loop

This skill is designed to work with the `autoresearch-loop` methodology. If you have the autoresearch-loop skill available:

- Use it directly: "Run autoresearch on `skills/learned/n8n-debugging/trimble-xml-import-debug/SKILL.md`"
- The autoresearch loop handles the iteration mechanics
- This skill provides the domain-specific guidance for WHAT to test and HOW to improve agent skills specifically

If you don't have autoresearch-loop available, follow Steps 2-4 above manually — the methodology is the same, just without the automated iteration framework.
